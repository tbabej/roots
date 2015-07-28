# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, View

from wiki.core.http import send_file
from wiki.decorators import get_article
from wiki.views.mixins import ArticleMixin

from pandoc_export.settings import EXPORT_FORMATS

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import pypandoc
import tempfile


class PandocExportListView(ArticleMixin, TemplateView):

    template_name = "wiki/plugins/pandoc_export/index.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(PandocExportListView, self).dispatch(request, article,
                                                          *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PandocExportListView, self).get_context_data(**kwargs)
        context['allowed_formats'] = EXPORT_FORMATS
        return context


class PandocExportView(ArticleMixin, View):

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(PandocExportView, self).dispatch(request, article, *args,
                                                      **kwargs)

    def get(self, request, *args, **kwargs):
        # Load the format and check if it is in the list of allowed ones
        export_format = kwargs.get('format')
        if export_format not in EXPORT_FORMATS:
            raise ValueError("{0} not in allowed formats: {1}"
                             .format(export_format, EXPORT_FORMATS))

        # Get the content
        current_data = self.article.current_revision.content

        # Create a in-memory file
        temp = tempfile.NamedTemporaryFile()

        # Convert it to desired format
        converted_data = pypandoc.convert(current_data, export_format, format='md', outputfile=temp.name)

        # Serve it as an attachment
        response = HttpResponse(FileWrapper(temp), content_type='application/octet-stream')
        header = 'attachment; filename=export.{0}'.format(export_format)
        response['Content-Disposition'] = header

        return response
