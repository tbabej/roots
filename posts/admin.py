from reversion import VersionAdmin
from django.contrib import admin

from base.admin import PrettyFilterAdmin
from base.util import admin_commentable

from models import Post


# Reversion-enabled Admin for problems
@admin_commentable
class PostAdmin(PrettyFilterAdmin, VersionAdmin):

    list_display = ('title',
                    'competition',
                    'added_by',
                    'added_at',
                    )

    list_filter = ('competition', 'added_at', 'added_by')
    search_fields = ['text', 'title']
    readonly_fields = ('added_by', 'modified_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'competition', 'text')
        }),
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
