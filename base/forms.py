from django import forms
from django.core.exceptions import ValidationError

from base.widgets import MultiFileInput


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': (u"Ensure at least %(min_num)s files are uploaded "
                     "(received %(num_files)s)."),
        'max_num': (u"Ensure at most %(max_num)s files are uploaded "
                    "(received %(num_files)s)."),
        'max_size': (u"File: %(uploaded_file_name)s, "
                       "exceeded maximum upload size."),
        'max_total_size': u"Upload exceeded maximum total upload size."
    }

    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.max_file_size = kwargs.pop('max_size', None)
        self.max_total_size = kwargs.pop('max_total_size', None)

        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    def validate(self, data):
        super(MultiFileField, self).validate(data)

        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0

        # Check the number of uploaded files
        if num_files < self.min_num:
            infodict = dict(min_num=self.min_num, num_files=num_files)
            raise ValidationError(self.error_messages['min_num'] % infodict)

        elif self.max_num and num_files > self.max_num:
            infodict = dict(max_num=self.max_num, num_files=num_files)
            raise ValidationError(self.error_messages['max_num'] % infodict)

        # Check sizes of uploaded files per file
        if self.max_file_size:
            for uploaded_file in data:
                if uploaded_file.size > self.max_file_size:
                    infodict = dict(uploaded_file_name=uploaded_file.name)
                    raise ValidationError(self.error_messages['max_size']
                                          % infodict)

        # Check total size of uploaded data
        total_size = sum([f.size for f in data])
        if self.max_total_size and total_size > self.max_total_size:
            raise ValidationError(self.error_messages['max_total_size'])
