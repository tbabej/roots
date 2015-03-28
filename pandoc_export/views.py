# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from wiki.core.http import send_file
from wiki.decorators import get_article
from wiki.views.mixins import ArticleMixin


class PandocExportListView(ArticleMixin, TemplateView):

    template_name = "wiki/plugins/pandoc_export/index.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        # Fixing some weird transaction issue caused by adding commit_manually
        # to form_valid
        return super(
            PandocExportListView,
            self).dispatch(
            request,
            article,
            *args,
            **kwargs)
