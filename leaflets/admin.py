import reversion

from django.contrib import admin

from .models import Leaflet


class LeafletAdmin(reversion.VersionAdmin):

    list_display = ('competition',
                    'year',
                    'issue',
                    )


# Register to the admin site
admin.site.register(Leaflet, LeafletAdmin)