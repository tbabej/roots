from sendfile import sendfile
from django.conf import settings
from django.core.exceptions import PermissionDenied


def download_protected_file(request, model_class, path_prefix, path):
    """
    This view allows download of the file at the specified path, if the user
    is allowed to. This is checked by calling the model's can_access_files
    method.
    """

    # filepath is the absolute path, mediapath is relative to media folder
    filepath = settings.SENDFILE_ROOT + path_prefix + path
    filepath_mediapath = settings.SENDFILE_DIR + path_prefix + path

    if request.user.is_authenticated():
        # Superusers can access all files
        if request.user.is_superuser:
            return sendfile(request, filepath)
        else:
            # We need to check can_access_files on particular instance
            obj = model_class.get_by_filepath(filepath_mediapath)

            if obj is not None and obj.can_access_files(request.user):
                return sendfile(request, filepath)

    raise PermissionDenied
