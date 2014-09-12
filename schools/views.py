from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from base.util import class_view_decorator

from .forms import AddressForm, SchoolForm


@class_view_decorator(login_required)
class SchoolCreateView(TemplateView):

    template_name = 'schools/school_create_form.html'

    address_form = None
    school_form = None

    @property
    def forms(self):
        return (
            self.school_form,
            self.address_form,
        )

    def set_forms(self):
        if all(form is not None for form in self.forms):
            return

        if self.request.POST:
            self.address_form = AddressForm(self.request.POST)
            self.school_form = SchoolForm(self.request.POST)
        else:
            self.address_form = AddressForm()
            self.school_form = SchoolForm()

    def get_context_data(self, **kwargs):
        context = super(SchoolCreateView, self).get_context_data(**kwargs)

        self.set_forms()

        context_forms = {
            'address_form': self.address_form,
            'school_form': self.school_form,
            }

        context.update(context_forms)

        return context

    def post(self, request, *args, **kwargs):
        self.set_forms()

        if all(form.is_valid() for form in self.forms):
            address = self.address_form.save()
            school = self.school_form.save(commit=False)
            school.address = address
            school.save()

        messages.success(request, _("School successfully added."))

        return self.get(request)
