from reversion import VersionAdmin

from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError

from base.admin import PrettyFilterMixin
from base.util import editonly_fieldsets

from .models import (Competition, Season, Series,
                     CompetitionUserRegistration, CompetitionOrgRegistration)


@editonly_fieldsets
class CompetitionAdmin(admin.ModelAdmin):

    list_display = ('name', 'organizer_group', 'added_at')

    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'organizer_group')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at', 'added_by', 'modified_by')
        }),
    )


@editonly_fieldsets
class CompetitionUserRegistrationAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = ('user',
                    'competition',
                    'added_at',
                    )

    list_filter = ('competition',)
    search_fields = ['user']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('competition', 'user', 'added_at')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at', 'added_by', 'modified_by')
        }),
    )


@editonly_fieldsets
class CompetitionOrgRegistrationAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = ('organizer',
                    'competition',
                    'added_at',
                    )

    list_filter = ('competition',)
    search_fields = ['user']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('competition', 'organizer', 'approved')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at', 'added_by', 'modified_by')
        }),
    )


@editonly_fieldsets
class SeasonAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = ('competition',
                    'year',
                    'name',
                    'number',
                    'start',
                    'end',
                    'join_deadline'
                    )

    list_filter = ('competition', 'year', 'join_deadline')
    search_fields = ['name', 'competition']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('competition',
                       'name',
                       'year',
                       'number',
                       'start',
                       'end',
                       'join_deadline',
                       )
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at', 'added_by', 'modified_by')
        }),
    )


@editonly_fieldsets
class SeriesAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = ('season',
                    'name',
                    'number',
                    'submission_deadline',
                    'is_active'
                    )

    list_filter = ('season', 'submission_deadline', 'is_active')
    search_fields = ['name', 'season']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('season', 'name', 'number', 'problemset',
                       'submission_deadline', 'is_active')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at', 'added_by', 'modified_by')
        }),
    )

    actions = ['make_active']

    def make_active(self, request, queryset):
        for series in queryset:
            try:
                series.is_active = True
                series.full_clean()
                series.save()
            except ValidationError, e:
                for message in e.messages:
                    self.message_user(request,
                                      message=message,
                                      level=messages.ERROR)
    make_active.short_description = "Make active"


# Register to the admin site
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionUserRegistration,
                    CompetitionUserRegistrationAdmin)
admin.site.register(CompetitionOrgRegistration,
                    CompetitionOrgRegistrationAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Series, SeriesAdmin)
