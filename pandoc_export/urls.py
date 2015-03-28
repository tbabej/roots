from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import patterns, url

from wiki_pandoc import views

urlpatterns = patterns('',
    url(r'^$', views.PandocExportListView.as_view(), name='pandoc_export_list'),
#    url(r'^(?P<format>[\w-]+/$', views.PandocExportView.as_view(), name='pandoc_export'),
)
