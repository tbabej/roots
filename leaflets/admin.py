import reversion

from django.contrib import admin

from base.admin import (MediaRemovalAdminMixin, DownloadMediaFilesMixin,
                        RestrictedCompetitionAdminMixin)

from .models import Leaflet


class LeafletAdmin(RestrictedCompetitionAdminMixin,
                   MediaRemovalAdminMixin,
                   DownloadMediaFilesMixin,
                   reversion.VersionAdmin):

    list_display = (
        'competition',
        'year',
        'issue',
    )

    list_filter = (
        'competition',
    )

    search_fields = (
        'competition',
        'user__name',
        'user__first_name',
        'user__last_name'
    )

    fieldsets = (
        (None, {
            'fields': ('competition', 'year', 'issue', 'leaflet')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'added_at', 'modified_by', 'modified_at')
        }),
    )


# Register to the admin site
admin.site.register(Leaflet, LeafletAdmin)
