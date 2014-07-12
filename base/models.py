import os

from django.conf import settings
from django.forms import forms
from django.db.models import FileField
from django.template.defaultfilters import filesizeformat


class MediaRemovalMixin(object):
    """
    Removes all files associated with the model, as returned by the
    get_media_files() method.
    """

    # Models that use this mixin need to override this method
    def get_media_files(self):
        raise NotImplemented("Models using MediaRemovalMixin needs to override "
                             "get_media_files method.")

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

# Add ContentTypeRestrictedFileField to South introspection rules
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^base\.models\.ContentTypeRestrictedFileField"])

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
                          Example: ['application/pdf', 'image/jpeg']
        * max_size - a number indicating the maximum file size
                            allowed for upload.
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", None)
        self.max_size = kwargs.pop("max_size", None)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField,
                     self).clean(*args, **kwargs)

        file_obj = data.file
        content_type = file_obj.content_type

        if self.content_types is None or content_type in self.content_types:
            if self.max_size is None or file_obj._size > int(self.max_size):
                raise forms.ValidationError(
                    'Please keep filesize under %s. Current filesize %s' %
                    (filesizeformat(self.max_size),
                     filesizeformat(file_obj._size)))
        else:
            raise forms.ValidationError('Filetype not supported.')

        return data
