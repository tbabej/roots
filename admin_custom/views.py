from django.views.generic.base import TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from base.util import class_view_decorator

from .dashboard import (IndexDashboard,
    ProblemsDashboard, ContentDashboard,
    CompetitionDashboard, UserDashboard
    )


@class_view_decorator(staff_member_required)
class DashboardIndexView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardIndexView, self).get_context_data(*args,
                                                                   **kwargs)
        context['dashboard'] = IndexDashboard()
        return context


@class_view_decorator(staff_member_required)
class DashboardProblemsView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardProblemsView, self).get_context_data(*args,
                                                                      **kwargs)
        context['dashboard'] = ProblemsDashboard()
        return context


@class_view_decorator(staff_member_required)
class DashboardContentView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardContentView, self).get_context_data(*args,
                                                                      **kwargs)
        context['dashboard'] = ContentDashboard()
        return context


@class_view_decorator(staff_member_required)
class DashboardCompetitionView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardCompetitionView, self).get_context_data(*args,
                                                                      **kwargs)
        context['dashboard'] = CompetitionDashboard()
        return context


@class_view_decorator(staff_member_required)
class DashboardUsersView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardUsersView, self).get_context_data(*args,
                                                                      **kwargs)
        context['dashboard'] = UserDashboard()
        return context
