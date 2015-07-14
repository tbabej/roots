# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import (
    DashboardIndexView, DashboardContentView,
    DashboardCompetitionView,
    )

urlpatterns = patterns('',
    url(_(r'^$'), DashboardIndexView.as_view(),
        name="admin_dashboard_index"),
    url(_(r'dashboards/problems/$'), DashboardProblemsView.as_view(),
        name="admin_dashboard_problems"),
    url(_(r'dashboards/content/$'), DashboardContentView.as_view(),
        name="admin_dashboard_content"),
    url(_(r'dashboards/competition/$'), DashboardCompetitionView.as_view(),
        name="admin_dashboard_competition"),
)
