from django.contrib import admin
from reversion import VersionAdmin
from base.admin import PrettyFilterMixin
from base.util import editonly_fieldsets
from news.models import News


@editonly_fieldsets
class NewsAdmin(PrettyFilterMixin, VersionAdmin):

    list_display = (
        'competition',
        'heading',
        'added_at',
        'added_by',
    )

    list_filter = (
        'competition',
        'added_at'
    )

    search_fields = (
        'heading',
        'text'
    )

    readonly_fields = (
        'added_by',
        'modified_by',
        'added_at',
        'modified_at'
    )

    fieldsets = (
        (None, {
            'fields': ('competition', 'heading', 'text')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_at', 'modified_at', 'added_by', 'modified_by')
        }),
    )

admin.site.register(News, NewsAdmin)
