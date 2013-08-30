from reversion import VersionAdmin
from django.contrib import admin

from base.admin import PrettyFilterAdmin
from base.util import admin_commentable, editonly_fieldsets

from events.models import (Event, EventOrgRegistration, EventUserRegistration,
                           Camp)


@admin_commentable
@editonly_fieldsets
class EventAdmin(PrettyFilterAdmin, VersionAdmin):

    list_display = ('name',
                    'location',
                    'start_time',
                    'end_time',
                    'get_num_users',
                    'get_num_orgs',
                    )

    list_filter = ('start_time', 'added_at', 'added_by')
    search_fields = ['name', 'location']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at',
                       'get_num_users', 'get_num_orgs')

    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'description',
                       'start_time', 'end_time')
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
class EventUserRegistrationAdmin(PrettyFilterAdmin, VersionAdmin):

    list_display = ('event',
                    'user',
                    'added_at'
                    )

    list_filter = ('event', 'user')
    search_fields = ['event', 'user']
    readonly_fields = ('event', 'user')

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
class EventOrgRegistrationAdmin(PrettyFilterAdmin, VersionAdmin):

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
class CampAdmin(PrettyFilterAdmin, VersionAdmin):

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
#admin.site.register(CampUserInvitation, CampUserInvitationAdmin)
