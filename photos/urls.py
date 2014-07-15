# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import GallerySampleArchiveIndexView

urlpatterns = patterns('',
    url(_(r'^gallery/$'), GallerySampleArchiveIndexView.as_view(),
        name="pl-gallery-archive"),
)