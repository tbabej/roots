from django.contrib import admin
import reversion

from base.admin import PrettyFilterMixin

from .models import UserProfile, OrganizerProfile


class UserProfileAdmin(PrettyFilterMixin, reversion.VersionAdmin):

    list_display = ('user',
                    'sex',
                    'date_of_birth',
                    'school',
                    'classlevel'
                    )

    list_filter = ('sex', 'school', 'date_of_birth',
                   'classlevel')


class OrganizerProfileAdmin(PrettyFilterMixin, reversion.VersionAdmin):

    list_display = ('user',
                    'motto',
                    )


# Register to the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OrganizerProfile, OrganizerProfileAdmin)
