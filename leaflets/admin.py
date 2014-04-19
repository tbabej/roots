import reversion

from django.contrib import admin

from base.admin import MediaRemovalAdminMixin, DownloadMediaFilesMixin

from .models import Leaflet


class LeafletAdmin(MediaRemovalAdminMixin,
                   DownloadMediaFilesMixin,
                   reversion.VersionAdmin):

    list_display = ('competition',
                    'year',
                    'issue',
                    )

# Register to the admin site
admin.site.register(Leaflet, LeafletAdmin)