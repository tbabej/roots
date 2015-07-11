import datetime
import os
import unicodedata
import subprocess
import shutil

from django.conf import settings
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

    cls_name = cls.__name__

    created_by = models.ForeignKey('auth.User',
                                   related_name=u'%s_created' % cls_name,
                                   verbose_name=_('author'),
                                   null=True,
                                   blank=True,
                                   editable=False)

    modified_by = models.ForeignKey('auth.User',
                                    related_name=u'%s_modified' % cls_name,
                                    verbose_name=_('last modified by'),
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
        try:
            extra_context = extra_context or {}
            extra_context['model_object'] = self.model.objects.get(pk=object_id)
        except self.model.DoesNotExist:
            # If we are not able to get the solution, just do not fail here,
            # change view will deal with it just fine
            pass

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

    stdout, _, rc = run(['xvfb-run', '-a', '-w', '0',
                         'soffice',
                         '--headless',
                         '--invisible',
                         '--nofirststartwizard',
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


def merge_pdf_files(path_root, output_path, filepaths):
    if not filepaths:
        raise ValidationError(u"No PDF files to merge.")
    elif not output_path:
        raise ValidationError(u"No path given.")

    # The place where the merged file will be stored
    new_location = os.path.join(path_root, output_path)

    # If there is only one file, do not even try to merge,
    # just move the file to the new location
    if len(filepaths) == 1:
        shutil.move(filepaths[0], new_location)
        return output_path

    # For more than a one file, try to merge them
    out, err, rc = run(['pdfunite'] +
                       filepaths +
                       [new_location])

    if rc != 0:
        raise ValidationError(u"Failed to merge PDF files.")

    # This is correct, we just want to return the partial path
    return output_path


def convert_files_to_single_pdf(path_root, output_path, files):
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

    merged_file_path = merge_pdf_files(path_root, output_path, new_paths)

    # Remove all temporary files
    for path in to_remove_paths:
        if os.path.exists(path):
            os.unlink(path)

    return merged_file_path


def simple_solution_sum(solutions, *args, **kwargs):
    """
    Returns a simple sum of scores of the given solutions, neglecting the given user.
    """
    return sum([s.score or 0 for s in solutions if s is not None])


def simple_series_solution_sum(series_subtotals, *args, **kwargs):
    """
    Simply adds up the totals from the series themselves.
    """

    return sum(subtotal[-1] or 0 for subtotal in series_subtotals)


class YearSegment(object):
    """
    Represents a segment of a year.
    """

    def __init__(self, year, order, num_segments):
        self.order = order
        self.num_segments = num_segments

        year_start = datetime.date(year, 1, 1)
        year_end = datetime.date(year, 12, 31)

        segment = (year_end - year_start) / num_segments

        if order > num_segments:
            raise ValueError(_("Order cannot be higher tha number of year "
                               "segments."))

        self.start = year_start + (order - 1) * segment
        self.end = year_start + order * segment

    def next(self):
        """
        Returns next segment.
        """
        order = (self.order % self.num_segments) + 1

        # Increment the year if we went over to the next one
        year = self.start.year if order > self.order else self.start.year + 1

        return self.__class__(year, order, self.num_segments)

    def back(self):
        order = ((self.order - 2) % self.num_segments) + 1

        # Decrement the year if we went back
        year = (self.start.year
                if order <= self.order else
                self.start.year - 1)

        return self.__class__(year, order, self.num_segments)

    def __contains__(self, date):
        """
        Returns True if given date is in interval <segment_start, segment_end).
        """

        return self.start <= date < self.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __gt__(self, other):
        return self.start > other.start

    def __ge__(self, other):
        return self.start >= other.start

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __repr__(self):
        return self.__unicode__()

    def __hash__(self):
        return hash(unicode(self))

    def __unicode__(self):
        # This needs to contain all the information that makes a YearSegment
        # unique, since it is used to make a hash

        return u"%s - %s/%s" % (self.start.year,
                                self.order,
                                self.num_segments)

    @classmethod
    def by_date(cls, date, num_segments):
        """
        Returns the year segment that contains this date.
        """

        for segment in cls.by_year(date.year, num_segments):
            if date in segment:
                return segment

    @classmethod
    def by_year(cls, year, num_segments):
        """
        Yields all the year segments in the given year. The number of segments
        in the given year is specified by the num_segments argument.
        """

        for i in range(num_segments):
            yield cls(year, i + 1, num_segments)

    @classmethod
    def between_dates(cls, date_start, date_finish, num_segments):
        """
        Yields all the year segments that occured (even partially) between two
        given dates.
        """

        for year in range(date_start.year, date_finish.year + 1):
            for segment in cls.by_year(year, num_segments):
                if segment.end > date_start and segment.start <= date_finish:
                    yield segment

    @classmethod
    def between_segments(cls, start, finish):
        """
        Returns all segments between given two segments, inclusive.
        """

        for segment in cls.between_dates(start.start,
                                         finish.start,
                                         start.num_segments):
            yield segment
