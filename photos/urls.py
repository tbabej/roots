# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import GallerySampleArchiveIndexView

urlpatterns = patterns('',
    url(r'^gallery/$', GallerySampleArchiveIndexView.as_view(),
        name="pl-gallery-archive"),
)