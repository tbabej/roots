import unicodedata

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import ugettext_lazy as _
from django.utils.decorators import method_decorator

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
