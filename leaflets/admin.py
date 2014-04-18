import reversion

from django.contrib import admin

from base.admin import MediaRemovalAdminMixin

from .models import Leaflet


class LeafletAdmin(MediaRemovalAdminMixin, reversion.VersionAdmin):

    list_display = ('competition',
                    'year',
                    'issue',
                    )

# Register to the admin site
admin.site.register(Leaflet, LeafletAdmin)