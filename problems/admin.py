from reversion import VersionAdmin
from django.contrib import admin

from base.admin import PrettyFilterAdmin
from base.util import admin_commentable, editonly_fieldsets

from models import (Problem, ProblemSet, ProblemSeverity, ProblemCategory,
                    UserSolution, OrgSolution, ProblemInSet)


# Reversion-enabled Admin for problems
@admin_commentable
@editonly_fieldsets
class ProblemAdmin(PrettyFilterAdmin, VersionAdmin):

    list_display = ('text',
                    'get_rating',
                    'severity',
                    'category',
                    'competition',
                    'added_by',
                    'last_used_at',
                    'times_used',
                    )

    list_filter = ('competition', 'severity', 'category')
    search_fields = ['text']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at',
                       'last_five_usages', 'times_used')

    fieldsets = (
        (None, {
            'fields': ('text', 'severity', 'category', 'competition')
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


class ProblemInSetInline(admin.StackedInline):

    model = ProblemInSet
    fields = ('position', 'problem',
              'get_competition', 'get_category', 'get_severity', 'times_used',
              'last_used_at')
    readonly_fields = ('get_competition', 'get_category', 'get_severity',
                       'times_used', 'last_used_at')
    raw_id_fields = ('problem', )
    verbose_name = 'Problem'
    verbose_name_plural = 'Problems'
    sortable_field_name = "position"
    extra = 0


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


@admin_commentable
@editonly_fieldsets
class ProblemSetAdmin(PrettyFilterAdmin, VersionAdmin):

    list_display = ('name',
                    'competition',
                    'event',
                    'get_problem_count',
                    'get_average_severity_by_competition',
                    )

    list_filter = ('competition', 'event', AverageSeverityAboveListFilter)
    search_fields = ['name', 'event']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at',
                       'get_average_severity_by_competition')

    ordering = ('modified_at', )
    inlines = [ProblemInSetInline, ]

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


# Register to the admin site
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)
admin.site.register(UserSolution)
admin.site.register(OrgSolution)
admin.site.register(ProblemCategory)
admin.site.register(ProblemSeverity)
