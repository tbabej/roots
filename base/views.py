# Create your views here.
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class BaseView(TemplateView):

    template_name = "base/base.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class SecureBaseView(BaseView):

    template_name = "base/base.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):

    template_name = "base/index.html"
