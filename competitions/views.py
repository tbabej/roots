from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import FormView
from competitions.forms import CompetitionRegistrationForm
from competitions.models import CompetitionUserRegistration


class CompetitionRegistrationView(FormView):

    form_class = CompetitionRegistrationForm
    template_name = 'competitions/competition_registration.html'
    success_url = 'registration/successful/'

    def form_valid(self, form):
        registration = CompetitionUserRegistration()
        registration.competition = form.cleaned_data['competition']
        registration.user = self.request.user.user
        registration.save()
        return super(CompetitionRegistrationView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *arg, **kwarg):
        return super(CompetitionRegistrationView, self).dispatch(*arg, **kwarg)


