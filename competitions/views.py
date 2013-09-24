from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from .forms import CompetitionRegistrationForm, SeasonJoinForm
from .models import CompetitionUserRegistration


class CompetitionRegistrationView(FormView):

    form_class = CompetitionRegistrationForm
    template_name = 'competitions/competition_registration.html'
    success_url = 'registration/successful/'

    def form_valid(self, form):
        registration = CompetitionUserRegistration()
        registration.competition = form.cleaned_data['competition']
        registration.user = self.request.user.userprofile
        registration.save()
        return super(CompetitionRegistrationView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *arg, **kwarg):
        return super(CompetitionRegistrationView, self).dispatch(*arg, **kwarg)


class SeasonJoinView(FormView):

    form_class = SeasonJoinForm
    template_name = 'competitions/competition_season_join.html'
    success_url = 'registration/successful/'

    def get_form(self, form_class):
        form = super(SeasonJoinView, self).get_form(form_class)

        # Limit the choices only to the competitions user has registered
        form.fields['season'].queryset = form.fields['season'].queryset\
        .filter(competition__in=self.request.user.userprofile.competes.all())

        return form

    def form_valid(self, form):
        #registrationg = CompetitionUserRegistration()
        #registration.competition = form.cleaned_data['competition']
        #registration.user = self.request.user.userprofile
        #registration.save()
        return super(SeasonJoinView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *arg, **kwarg):
        return super(SeasonJoinView, self).dispatch(*arg, **kwarg)
