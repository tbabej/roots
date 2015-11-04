from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import reversion

from base.admin import PrettyFilterMixin, ImprovedFilteringVersionAdminMixin
from problems.admin import LimitToSeasonFilter

from competitions.models import Competition, Season
from .models import UserProfile, OrganizerProfile, UserSeasonRegistration


class LimitProfilesToSeasonFilter(LimitToSeasonFilter):

    def queryset(self, request, queryset):
        value = self.value()

        # Check that any value was passed, if not, return unmodified queryset
        if not value:
            return queryset

        # Fetch the list of the problems in this season
        season = Season.objects.get(pk=value)
        season_competitors = season.competitors.values_list('pk', flat=True)

        return queryset.filter(user__pk__in=season_competitors)


class UserProfileAdmin(ImprovedFilteringVersionAdminMixin, reversion.VersionAdmin):

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
        'classlevel',
        LimitProfilesToSeasonFilter,
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'school__name',
        'classlevel'
    )

    raw_id_fields = ('user', 'school')

    autocomplete_lookup_fields = {
        'fk': ['user', 'school'],
    }

class OrganizerProfileAdmin(ImprovedFilteringVersionAdminMixin, reversion.VersionAdmin):

    list_display = (
        'user',
        'motto',
    )

    raw_id_fields = ('user',)

    autocomplete_lookup_fields = {
        'fk': ['user'],
    }

class UserSeasonRegistrationAdmin(ImprovedFilteringVersionAdminMixin, reversion.VersionAdmin):

    list_display = (
        'user',
        'season',
        'school',
        'classlevel',
    )

    list_filter = (
        'school',
        'classlevel',
        LimitProfilesToSeasonFilter,
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'school__name',
        'season__name',
        'classlevel'
    )

    raw_id_fields = ('user', 'school', 'season')

    autocomplete_lookup_fields = {
        'fk': ['user', 'school', 'season'],
    }

# Register to the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSeasonRegistration, UserSeasonRegistrationAdmin)
admin.site.register(OrganizerProfile, OrganizerProfileAdmin)
