import os
import unicodedata
import subprocess

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import models
from django.utils.text import ugettext_lazy as _
from django.utils.decorators import method_decorator

from tempfile import NamedTemporaryFile

from wand.image import Image
from wand.color import Color


def remove_accents(string):
    return unicodedata.normalize('NFKD', unicode(string)).encode('ascii',
                                                                 'ignore')


def with_timestamp(cls):
    """Decorator to add added/modified field to particular model"""

    added_at = models.DateTimeField(verbose_name=_('added at'),
                                    auto_now_add=True,
                                    editable=False)
    modified_at = models.DateTimeField(verbose_name=_('modified at'),
                                       auto_now=True,
                                       editable=False)

    if not hasattr(cls, 'added_at'):
        cls.add_to_class('added_at', added_at)
    if not hasattr(cls, 'modified_at'):
        cls.add_to_class('modified_at', modified_at)

    return cls


def with_author(cls):
    """
    Decorator to add added_by/modified_by field to particular model
    """

    user_model = get_user_model()
    cls_name = cls._meta.verbose_name_plural.lower()

    created_by = models.ForeignKey(user_model,
                                   related_name='%s_created' % cls_name,
                                   verbose_name='author',
                                   null=True,
                                   blank=True,
                                   editable=False)

    modified_by = models.ForeignKey(user_model,
                                    related_name='%s_modified' % cls_name,
                                    verbose_name='last modified by',
                                    null=True,
                                    blank=True,
                                    editable=False)

    if not hasattr(cls, settings.AUTHOR_CREATED_BY_FIELD_NAME):
        cls.add_to_class(settings.AUTHOR_CREATED_BY_FIELD_NAME, created_by)
    if not hasattr(cls, settings.AUTHOR_UPDATED_BY_FIELD_NAME):
        cls.add_to_class(settings.AUTHOR_UPDATED_BY_FIELD_NAME, modified_by)

    return cls


def admin_commentable(cls):
    """
    Adds a comments section to the change view,
    """

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['model_object'] = self.model.objects.get(pk=object_id)
        return super(cls, self).change_view(request,
            object_id, form_url, extra_context=extra_context)

    cls.change_form_template = 'admin/change_form_commentable.html'
    cls.change_view = change_view

    return cls


def editonly_fieldsets(cls):
    """
    Hides edit-only fieldsets when adding a new object.
    """

    def get_fieldsets(self, request, obj=None):
        if obj and hasattr(cls, 'editonly_fieldsets'):
            if cls.fieldsets:
                return cls.fieldsets + cls.editonly_fieldsets
            else:
                return cls.editonly_fieldsets
        else:
            return cls.fieldsets

    cls.get_fieldsets = get_fieldsets

    return cls


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def generate_pdf_thumbnail(source, destination, width, height):

    source = settings.MEDIA_ROOT + source + '[0]'
    destination = settings.MEDIA_ROOT + destination

    with Image(filename=source) as img:
        img.alpha_channel = False
        img.background_color = Color('white')
        img.resize(width, height)
        img.save(filename=destination)


def get_uploaded_filepath(f):
    """
    Returns path to the uploaded file. If the file is small enough for Django
    to handle it using InMemoryUploadedFile, save it and return the path.
    """

    if isinstance(f, TemporaryUploadedFile):
        return f.temporary_file_path()
    else:
        temp_file = NamedTemporaryFile(delete=False)
        #temp_file = open('/home/tbabej/temp/%s' % f.name, 'w')
        for chunk in f.chunks():
            temp_file.write(chunk)
        temp_file.flush()

        return temp_file.name


def run(args):
    child = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = child.communicate()
    rc = child.returncode

    return stdout, stderr, rc


def convert_to_pdf_soffice(filepath):
    """
    Converts file to PDF using soffice. Returns the path of the newly created
    PDF file.
    """

    stdout, _, rc = run(['soffice',
                         '--headless',
                         '--convert-to', 'pdf',
                         '--outdir', '/tmp',
                         filepath])

    if rc != 0:
        raise ValidationError(u"Failed to convert file to PDF file.")

    output_path = stdout.split(' -> ')[1].split(' ')[0]

    return output_path


def convert_to_pdf_convert(filepath):
    """
    Converts file to PDF using convert. Returns the path of the newly created
    PDF file.
    """

    filedir, filename = os.path.split(filepath)
    pdf_path = os.path.join("/tmp", filename + '.pdf')

    out, err, rc = run(['convert', filepath, pdf_path])

    if rc != 0:
        raise ValidationError(u"Failed to convert image to PDF file.")

    return pdf_path


def merge_pdf_files(output_path, filepaths):
    if not filepaths:
        raise ValidationError(u"No PDF files to merge.")
    elif not output_path:
        raise ValidationError(u"No path given.")

    out, err, rc = run(['pdftk'] +
                       filepaths +
                       ['cat', 'output', settings.MEDIA_ROOT + output_path])

    if rc != 0:
        raise ValidationError(u"Failed to merge PDF files.")

    return output_path


def convert_files_to_single_pdf(output_path, files):
    CONTENT_TYPES = {
        'noconvert': ['application/pdf'],
        'soffice': ['application/msword',
                    'application/vnd.openxmlformats-'
                    'officedocument.wordprocessingml.document',
                    'application/vnd.oasis.opendocument.text'],
        'image': ['image/jpeg', 'image/bmp', 'image/gif', 'image/png',
                  'image/tiff']
    }

    EXTENSIONS = {
        'noconvert': ['.pdf'],
        'soffice': ['.doc', 'docx'],
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.png', '.tiff']
    }

    def get_file_category(f):
        for category, types in CONTENT_TYPES.iteritems():
            if f.content_type in types:
                return category

        for category, extensions in EXTENSIONS.iteritems():
            for extension in extensions:
                if f.name.endswith(extension):
                    return category

        raise ValidationError(u"Unable to convert: File format not allowed.")

    if not files:
        raise ValidationError(u"No files to convert.")

    # Convert each file to pdf
    new_paths = []
    to_remove_paths = []

    for f in files:
        if get_file_category(f) == 'noconvert':
            new_paths.append(get_uploaded_filepath(f))
        elif get_file_category(f) == 'soffice':
            new_path = convert_to_pdf_soffice(get_uploaded_filepath(f))
            new_paths.append(new_path)
            to_remove_paths.append(new_path)
        elif get_file_category(f) == 'image':
            new_path = convert_to_pdf_convert(get_uploaded_filepath(f))
            new_paths.append(new_path)
            to_remove_paths.append(new_path)

    merged_file_path = merge_pdf_files(output_path, new_paths)

    # Remove all temporary files
    for path in to_remove_paths:
        if os.path.exists(path):
            os.unlink(path)

    return merged_file_path
