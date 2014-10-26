import os
import zipfile
import StringIO

from django.conf import settings
from django.http import HttpResponse

from competitions.models import Competition


class PrettyFilterMixin(object):

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"


class RestrictedCompetitionAdminMixin(object):
    """
    Extends ModelAdmin in the following ways:
        - makes visible only those objects whose competition_field is one of
          the competitions that request.user organizes
        - makes it possible for the user to assign objects to those competitions
          that he organizes

    Following class attributes can be set to modify the behaviour of this mixin:
        - competition_field: Specifies the field that contains the foreign key
                             to the competition that this object belongs to.
                             Note that this can span several objects through
                             foreign keys, that is, it does not need to be
                             a attribute directly on this model.
    """

    competition_field = 'competition'

    def get_queryset(self, request):
        qs = super(RestrictedCompetitionAdminMixin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        # TODO: Investigate adding querysets, for now exclude all objects
        #       associated with the competitions user does not organize

        competitions = [c.id for c
                        in request.user.userprofile.organized_competitions]
        not_organized_competitions = Competition.objects.exclude(
                                                           id__in=competitions)
        kwargs = {self.competition_field + '__in': not_organized_competitions}
        return qs.exclude(**kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:
            if db_field.name == self.competition_field:
                profile = request.user.userprofile
                kwargs["queryset"] = profile.organized_competitions

        return super(RestrictedCompetitionAdminMixin,
                     self).formfield_for_foreignkey(db_field, request, **kwargs)


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

        # Add new delete method only for the superuser, as it is quite dangerous
        if request.user.is_superuser:

            # We use self.__class__ here so that self is not binded, otherwise
            # we would be passing 4 arguments instead of 3 (and self twice)
            new_delete = (self.__class__.delete_selected_with_media,
                          "delete_selected_with_media",
                          "Delete objects with associated media files")

            actions['delete_selected_with_media'] = new_delete

        return actions

    def delete_selected_with_media(self, request, queryset):
        for obj in queryset.all():
            obj.delete()


class DownloadMediaFilesMixin(object):

    def get_actions(self, request):
        actions = super(DownloadMediaFilesMixin, self).get_actions(request)

        # We use self.__class__ here so that self is not binded, otherwise
        # we would be passing 4 arguments instead of 3 (and self twice)
        export = (self.__class__.download_media_files,
                  "download_media_files",
                  "Download associated media files")

        actions['download_media_files'] = export
        return actions

    def download_media_files(self, request, queryset):
        export_file = 'export.zip'

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for obj in queryset.all():
            for filepath in obj.get_media_files():
                filepath = os.path.join(obj.media_root, filepath)

                if os.path.exists(filepath):
                    fdir, fname = os.path.split(filepath)
                    zf.write(filepath, fname)
                else:
                    self.message_user(request, '%s has no file saved at %s' %
                                                (obj, filepath))

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        response = HttpResponse(s.getvalue(),
                                mimetype="application/x-zip-compressed")
        # ..and correct content-disposition
        response['Content-Disposition'] = (
            'attachment; filename=%s' % export_file
            )

        return response
