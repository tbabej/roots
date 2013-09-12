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

    def delete(self, *args, **kwargs):
        for media_file in self.get_media_files():
            path = settings.MEDIA_ROOT + media_file

            if os.path.exists(path):
                os.remove(path)

        return super(MediaRemovalMixin, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            # Primary key exists, object is being edited
            old_object = self.__class__.objects.get(pk=self.pk)
            path_pairs = zip(old_object.get_media_files(),
                             self.get_media_files())

            # Move each associated file to its new location
            for (old_path, new_path) in path_pairs:
                full_old_path = settings.MEDIA_ROOT + old_path
                full_new_path = settings.MEDIA_ROOT + new_path

                if old_path != new_path and os.path.exists(full_old_path):
                    os.rename(full_old_path, full_new_path)

        return super(MediaRemovalMixin, self).save(*args, **kwargs)
