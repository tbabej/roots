from django.contrib import admin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from reversion import VersionAdmin

from base.admin import (PrettyFilterMixin, MediaRemovalAdminMixin,
                        DownloadMediaFilesMixin,
                        RestrictedCompetitionAdminMixin)
from base.util import admin_commentable, editonly_fieldsets

from competitions.models import Competition, Season, Series

from .models import (Problem, ProblemSet, ProblemSeverity, ProblemCategory,
                     UserSolution, OrgSolution, ProblemInSet)


# Reversion-enabled Admin for problems
@admin_commentable
@editonly_fieldsets
class ProblemAdmin(RestrictedCompetitionAdminMixin,
                   PrettyFilterMixin, VersionAdmin):

    list_display = (
        'text',
        'get_rating',
        'severity',
        'category',
        'competition',
        'added_by',
        'last_used_at',
        'times_used',
    )

    list_filter = (
        'competition',
        'severity',
        'category'
    )
    search_fields = (
        'text',
        'added_by'
    )

    readonly_fields = (
        'added_by',
        'modified_by',
        'added_at',
        'modified_at',
        'last_five_usages',
        'times_used'
    )

    fieldsets = (
        (None, {
            'fields': ('text', 'result', 'source')
        }),
        (_('Problem files'), {
            'fields': ('image', 'additional_files')
        }),
        (_('Problem parameters'), {
            'fields': ('severity', 'category', 'competition')
        }),
    )

    editonly_fieldsets = (
        ('Usage statistics', {
            'classes': ('grp-collapse', 'grp-opened'),
            'fields': ('last_five_usages', 'times_used')
        }),
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'modified_by', 'added_at', 'modified_at')
        }),
    )


class ProblemInSetInline(RestrictedCompetitionAdminMixin, admin.StackedInline):

    model = ProblemInSet
    fields = (
        'position',
        'problem',
        'get_competition',
        'get_category',
        'get_severity',
        'times_used',
        'last_used_at'
    )

    readonly_fields = (
        'get_competition',
        'get_category',
        'get_severity',
         'times_used',
         'last_used_at'
    )

    raw_id_fields = ('problem', )
    verbose_name = 'Problem'
    verbose_name_plural = 'Problems'
    sortable_field_name = "position"

    extra = 0
    competition_field = 'problem__competition'


class AverageSeverityAboveListFilter(admin.SimpleListFilter):
    title = 'Difficulty above'
    parameter_name = 'difficulty_above'

    def lookups(self, request, model_admin):
        severities = ProblemSeverity.objects.all()
        options = []

        for severity in severities:
            options.append((severity.level, severity.name))

        return options

    def queryset(self, request, queryset):
        if self.value():
            pks = [problemset.pk for problemset in queryset
                       if problemset.average_severity() < float(self.value())]

            for pk in pks:
                queryset = queryset.exclude(pk=pk)

        return queryset


class CurrentSeasonProblemFilter(admin.SimpleListFilter):

    title = 'problem in current season'
    parameter_name = 'current_season_problem'

    def lookups(self, request, model_admin):
        for competition in Competition.objects.all():
            # If the competition does not have active season, skip it
            if competition.active_season is None:
                continue

            for series in competition.active_season.series_set.all():
                problems = series.problemset.problems.all()

                for order, problem in enumerate(problems):
                    yield (problem.pk,
                           "%s, %s: %d" % (competition, series, order + 1))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(problem__pk=self.value())
        else:
            return queryset


class CurrentSeasonUserFilter(admin.SimpleListFilter):

    title = 'users competing in current season'
    parameter_name = 'current_season_user'

    def lookups(self, request, model_admin):
        for competition in Competition.objects.all():
            # If the competition does not have active season, skip it
            if competition.active_season is None:
                continue

            for user in competition.active_season.competitors:
                yield (user.pk, "%s: %s" % (competition, user))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__pk=self.value())
        else:
            return queryset


class LimitToCurrentSeasonProblemFilter(admin.SimpleListFilter):

    title = _('limit to following current season/series')
    parameter_name = 'current_season_series'

    def lookups(self, request, model_admin):
        for competition in Competition.objects.all():
            # If the competition does not have active season, skip it
            if competition.active_season is None:
                continue

            # First yield the whole season
            yield (
                "season-%d" % competition.active_season.pk,
                "%s: %s" % (competition, competition.active_season)
            )

            # Yield all the finished series
            for series in competition.active_season.finished_series:
                yield (
                    "series-%d" % series.pk,
                    "%s: %s" % (competition, series)
                )

    def queryset(self, request, queryset):
        value = self.value()

        # Check that any value was passed, if not, return unmodified queryset
        if not value:
            return queryset

        # If a season was selected, allow all problems in that season
        if value.startswith("season"):
            # Fetch the list of the problems in this season
            season_pk = value.split("-")[1]
            season = Season.objects.get(pk=season_pk)
            season_problems = season.problems.values_list('pk', flat=True)

            return queryset.filter(problem__pk__in=season_problems)

        elif value.startswith("series"):
            # Fetch the list of the problems in this series
            series_pk = value.split("-")[1]
            series = Series.objects.get(pk=series_pk)
            series_problems = series.problems.values_list('pk', flat=True)

            return queryset.filter(problem__pk__in=series_problems)

        else:
            # Any other value is invalid, return unmodified queryset
            return queryset


class LimitToSeasonFilter(admin.SimpleListFilter):

    title = _('limit to season')
    parameter_name = 'season'

    def lookups(self, request, model_admin):
        for competition in Competition.objects.all():
            for season in competition.season_set.all():
                # First yield the whole season
                yield (
                    season.pk,
                    "%s" % season
                )

    def queryset(self, request, queryset):
        value = self.value()

        # Check that any value was passed, if not, return unmodified queryset
        if not value:
            return queryset

        # Fetch the list of the problems in this season
        season = Season.objects.get(pk=value)
        season_problems = season.problems.values_list('pk', flat=True)

        return queryset.filter(problem__pk__in=season_problems)


@admin_commentable
@editonly_fieldsets
class ProblemSetAdmin(RestrictedCompetitionAdminMixin,
                      PrettyFilterMixin, VersionAdmin):

    list_display = (
        'name',
        'competition',
        'event',
        'get_problem_count',
        'get_average_severity_by_competition',
    )

    list_filter = (
        'competition',
        'event',
        AverageSeverityAboveListFilter
    )

    search_fields = (
        'name',
        'event__name'
    )

    readonly_fields = (
        'added_by',
        'modified_by',
        'added_at',
        'modified_at',
        'get_average_severity_by_competition'
    )

    ordering = ('modified_at', )
    inlines = (ProblemInSetInline, )

    fieldsets = (
        (None, {
            'fields': ('name', 'competition', 'leaflet', 'event',
                       'get_average_severity_by_competition')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'modified_by', 'added_at', 'modified_at')
        }),
    )


@admin_commentable
@editonly_fieldsets
class UserSolutionAdmin(RestrictedCompetitionAdminMixin,
                        MediaRemovalAdminMixin,
                        DownloadMediaFilesMixin,
                        VersionAdmin):

    def import_from_zip(self, request, queryset):
        return redirect('problems_import_solutions_from_zip')
    import_from_zip.short_description = 'Import solutions from zip'

    actions = ['import_from_zip']

    list_display = (
        'user',
        'problem',
        'solution',
        'score',
    )

    list_filter = (
        CurrentSeasonUserFilter,
        'user',
        CurrentSeasonProblemFilter,
        LimitToCurrentSeasonProblemFilter,
        'problem'
    )

    list_editable = (
        'score',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__username'
    )

    readonly_fields = (
        'added_by',
        'modified_by',
        'added_at',
        'modified_at'
    )

    fieldsets = (
        (None, {
            'fields': ('user', 'problem', 'solution', 'corrected_solution',
                       'classlevel', 'school', 'school_class')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'modified_by', 'added_at', 'modified_at',
                       'corrected_by', 'note')
        }),
    )

    competition_field = 'problem__competition'


@admin_commentable
class ProblemCategoryAdmin(VersionAdmin):

    list_display = (
        'name',
        'competition',
    )

@admin_commentable
class ProblemSeverityAdmin(VersionAdmin):

    list_display = (
        'name',
        'level',
        'competition',
    )


# Register to the admin site
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)
admin.site.register(UserSolution, UserSolutionAdmin)
admin.site.register(OrgSolution)
admin.site.register(ProblemCategory, ProblemCategoryAdmin)
admin.site.register(ProblemSeverity, ProblemSeverityAdmin)
