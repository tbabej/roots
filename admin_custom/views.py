from django.views.generic.base import TemplateView

from .dashboard import (IndexDashboard
    ProblemsDashboard, ContentDashboard,
    )


class DashboardIndexView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardIndexView, self).get_context_data(*args,
                                                                   **kwargs)
        context['dashboard'] = IndexDashboard()
        return context


class DashboardProblemsView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardProblemsView, self).get_context_data(*args,
                                                                      **kwargs)
        context['dashboard'] = ProblemsDashboard()
        return context


class DashboardContentView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardContentView, self).get_context_data(*args,
                                                                      **kwargs)
        context['dashboard'] = ContentDashboard()
        return context
