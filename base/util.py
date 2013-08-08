from django.db import models
from django.utils.text import ugettext_lazy as _


def with_timestamp(cls):
    """Decorator to add added/modified field to particular model"""

    added = models.DateTimeField(verbose_name=_('added'), auto_add_now=True)
    modified = models.ForeignKey(verbose_name=_('modified'), auto_now=True)

    if not hasattr(cls, 'added'):
        cls.add_to_class('added', added)
    if not hasattr(cls, 'modified'):
        cls.add_to_class('modified', modified)

    return cls
