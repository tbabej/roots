from django.contrib import admin
from reversion import VersionAdmin

from base.admin import PrettyFilterMixin, RestrictedCompetitionAdminMixin
from base.util import admin_commentable, editonly_fieldsets

from .models import Post


# Reversion-enabled Admin for problems
@admin_commentable
@editonly_fieldsets
class PostAdmin(RestrictedCompetitionAdminMixin,
                PrettyFilterMixin, VersionAdmin):

    list_display = ('title',
                    'competition',
                    'added_by',
                    'added_at',
                    )

    list_filter = ('competition', 'added_at', 'added_by')
    search_fields = ['text', 'title']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (None, {
            'fields': ('title', 'competition', 'slug', 'text', 'gallery')
        }),
    )

    editonly_fieldsets = (
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('added_by', 'modified_by', 'added_at', 'modified_at')
        }),
    )

    class Media:
        js = [
            'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'grappelli/tinymce_setup/tinymce_setup.js',
        ]

# Register to the admin site
admin.site.register(Post, PostAdmin)
