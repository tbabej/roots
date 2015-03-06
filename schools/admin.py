from django.contrib import admin
import reversion

from base.admin import PrettyFilterMixin

from .models import Address, School


class AddressAdmin(PrettyFilterMixin, reversion.VersionAdmin):

    list_display = (
        'street',
        'city',
        'region',
    )

    list_filter = (
        'city',
        'region',
    )

    search_fields = (
        'street',
        'city',
        'region',
    )


class SchoolAdmin(PrettyFilterMixin, reversion.VersionAdmin):

    list_display = (
        'name',
        'get_num_competitors',
    )

    list_filter = (
        'address__city',
        'address__region',
    )

    search_fields = (
        'address__city',
        'address__region',
        'address__street',
    )

    raw_id_fields = ('address',)

    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['address'],
    }



# Register to the admin site
admin.site.register(Address, AddressAdmin)
admin.site.register(School, SchoolAdmin)
