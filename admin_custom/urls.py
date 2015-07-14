# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import DashboardIndexView

urlpatterns = patterns('',
    url(_(r'^$'), DashboardIndexView.as_view(),
        name="admin_dashboard_index"),
    url(_(r'dashboards/problems/$'), DashboardProblemsView.as_view(),
        name="admin_dashboard_problems"),
)
