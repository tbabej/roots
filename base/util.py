from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import ugettext_lazy as _


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
                                   verbose_name=_('author'),
                                   blank=True,
                                   null=True,
                                   editable=False)

    modified_by = models.ForeignKey(user_model,
                                    related_name='%s_modified' % cls_name,
                                    verbose_name=_('last_modified_by'),
                                    blank=True,
                                    null=True,
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