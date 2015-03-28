# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.conf.urls import patterns, url, include
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from pandoc_export import views

class PandocExportPlugin(BasePlugin):

    slug = 'export'

    urlpatterns = {
        'article': patterns('',
            url('', include('pandoc_export.urls')),
         )
    }

    article_tab = (_('Export'), "fa fa-file-pdf-o")
    article_view = views.PandocExportListView().dispatch

    markdown_extensions = []

    def __init__(self):
        pass

registry.register(PandocExportPlugin)
