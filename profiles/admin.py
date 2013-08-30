import reversion
from django.contrib import admin

from base.admin import PrettyFilterAdmin
from profiles.models import UserProfile, OrganizerProfile


class UserProfileAdmin(PrettyFilterAdmin, reversion.VersionAdmin):

    list_display = ('user',
                    'sex',
                    'date_of_birth',
                    'school',
                    'classlevel'
                    )

    list_filter = ('competes', 'sex', 'school', 'date_of_birth',
                   'classlevel')


class OrganizerProfileAdmin(PrettyFilterAdmin, reversion.VersionAdmin):

    list_display = ('user',
                    'motto',
                    )


# Register to the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OrganizerProfile, OrganizerProfileAdmin)
