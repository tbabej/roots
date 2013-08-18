from django.contrib import admin


class PrettyFilterAdmin(admin.ModelAdmin):

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"
