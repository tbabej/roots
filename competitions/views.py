from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from problems.models import UserSolution

from .forms import CompetitionRegistrationForm, SeasonJoinForm
from .models import CompetitionUserRegistration, Season


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


class SeasonDetailView(DetailView):
    model = Season
    context_object_name = 'season'

    def get_context_data(self, *args, **kwargs):
        context = super(SeasonDetailView, self).get_context_data(*args, **kwargs)

        context['solutions'] = dict()

        for series in self.object.series_set.all():

            context['solutions'][series.pk] = dict()

            for problem in series.problemset.problems.all():
                solution = UserSolution.objects.filter(user=self.request.user.pk, problem=problem.pk) or None

                context['solutions'][series.pk][problem.pk] = solution

        return context
        
