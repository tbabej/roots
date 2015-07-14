from django.views.generic.base import TemplateView

from .dashboard import IndexDashboard

class DashboardIndexView(TemplateView):
    template_name = "admin_custom/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardIndexView, self).get_context_data(*args,
                                                                   **kwargs)
        context['dashboard'] = IndexDashboard()
        return context
