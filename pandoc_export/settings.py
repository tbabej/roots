from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings as django_settings

EXPORT_FORMATS = getattr(
    django_settings,
    'WIKI_PANDOC_EXPORT_FORMATS',
    ['html', 'latex', 'odt', 'docx', 'beamer'])
