class PrettyFilterMixin(object):

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"


class MediaRemovalAdminMixin(object):
    """
    This mixin overrides default delete_selected Admin action and replaces it
    with one that actually constructs a model instance from each object in the
    queryset and calls .delete() upon that instance.

    This way, we ensure that overridden delete method by MediaRemovalMixin
    is called.
    """

    def get_actions(self, request):
        actions = super(MediaRemovalAdminMixin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        # We use self.__class__ here so that self is not binded, otherwise
        # we would be passing 4 arguments instead of 3 (and self twice)
        new_delete = (self.__class__.delete_selected_with_media,
                      "delete_selected_with_media",
                      "Deletes objects with associated media files")

        actions['delete_selected_with_media'] = new_delete
        return actions

    def delete_selected_with_media(self, request, queryset):
        for obj in queryset.all():
            obj.delete()
