from django.contrib import admin
from reversion import VersionAdmin

from base.admin import PrettyFilterMixin, RestrictedCompetitionAdminMixin
from base.util import admin_commentable, editonly_fieldsets

from .models import (Event, EventOrgRegistration, EventUserRegistration,
                     Camp)


@admin_commentable
@editonly_fieldsets
class EventAdmin(RestrictedCompetitionAdminMixin,
                 PrettyFilterMixin, VersionAdmin):

    list_display = (
        'name',
        'location',
        'start_time',
        'end_time',
        'registration_end_time',
        'get_num_users',
        'get_num_orgs',
        'started',
    )

    list_filter = (
        'start_time',
        'added_at',
        'added_by'
    )

    search_fields = (
        'name',
        'location'
    )

    readonly_fields = (
        'added_by',
        'modified_by',
        'added_at',
        'modified_at',
        'get_num_users',
        'get_num_orgs'
    )

    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'description',
                       'start_time', 'end_time', 'registration_end_time')
        }),
    )

    editonly_fieldsets = (
        ('Attendance', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('get_num_users', 'get_num_orgs')
        }),
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'modified_by', 'added_at', 'modified_at')
        }),
    )


@admin_commentable
@editonly_fieldsets
class EventUserRegistrationAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = (
        'event',
        'user',
        'added_at'
    )

    list_filter = (
        'event',
    )

    search_fields = (
        'event',
        'user__name',
        'user__first_name',
        'user__last_name'
    )

    readonly_fields = (
        'event',
        'user'
    )

    fieldsets = (
        (None, {
            'fields': ('event', 'user')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at')
        }),
    )


@admin_commentable
@editonly_fieldsets
class EventOrgRegistrationAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = ('event',
                    'organizer',
                    'added_at',
                    )

    list_filter = ('organizer', 'event')
    search_fields = ['organizer', 'event']
    readonly_fields = ('organizer', 'event')

    fieldsets = (
        (None, {
            'fields': ('organizer', 'event')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at')
        }),
    )


@admin_commentable
@editonly_fieldsets
class CampAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = ('name',
                    'location',
                    'start_time',
                    'end_time',
                    'limit',
                    'invitation_deadline',
                    'get_num_users_invited',
                    'get_num_users_signed',
                    'get_num_users_accepted',
                    'get_num_orgs',
                    )

    list_filter = ('name', 'location', 'start_time', 'limit',
                   'invitation_deadline')
    search_fields = ['name', 'location']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at',
                       'get_num_users_invited', 'get_num_users_signed',
                       'get_num_users_accepted', 'get_num_orgs')

    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'description',
                       'start_time', 'end_time', 'limit',
                       'invitation_deadline')
        }),
    )

    # TODO: add inline invitations

    editonly_fieldsets = (
        ('Attendance', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('get_num_users_invited', 'get_num_users_signed',
                       'get_num_users_accepted', 'get_num_orgs')
        }),
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'modified_by', 'added_at', 'modified_at')
        }),
    )


# Register to the admin site
admin.site.register(Event, EventAdmin)
admin.site.register(EventUserRegistration, EventUserRegistrationAdmin)
admin.site.register(EventOrgRegistration, EventOrgRegistrationAdmin)
admin.site.register(Camp, CampAdmin)
# admin.site.register(CampUserInvitation, CampUserInvitationAdmin)
