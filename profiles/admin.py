from django.contrib import admin
import reversion

from base.admin import PrettyFilterMixin

from .models import UserProfile, OrganizerProfile


class UserProfileAdmin(PrettyFilterMixin, reversion.VersionAdmin):

    list_display = (
        'user',
        'sex',
        'date_of_birth',
        'school',
        'classlevel',
    )

    list_filter = (
        'sex',
        'school',
        'classlevel'
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'school__name',
        'classlevel'
    )


class OrganizerProfileAdmin(PrettyFilterMixin, reversion.VersionAdmin):

    list_display = (
        'user',
        'motto',
    )

# Register to the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OrganizerProfile, OrganizerProfileAdmin)
