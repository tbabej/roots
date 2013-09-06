import os

from django.conf import settings


class MediaRemovalMixin(object):
    """
    Removes all files associated with the model, as returned by the
    get_media_files() method.
    """

    # Models that use this mixin need to override this method
    def get_media_files(self):
        return

    def delete(self):
        for media_file in self.get_media_files():
            path = settings.MEDIA_ROOT + media_file

            if os.path.exists(path):
                os.remove(path)

        return super(MediaRemovalMixin, self).delete()
