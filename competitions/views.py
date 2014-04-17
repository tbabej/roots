from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from problems.models import UserSolution
from problems.forms import UserSolutionForm

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

        # Find UserSolution objects for the problems
        context['solutions'] = dict()

        for series in self.object.series_set.all():

            context['solutions'][series.pk] = dict()

            for problem in series.problemset.problems.all():
                solutions = UserSolution.objects.filter(user=self.request.user.pk, problem=problem.pk)
                solution = solutions[0] if solutions else None

                context['solutions'][series.pk][problem.pk] = solution

        # Construct form objects
        context['forms'] = dict()

        for series in self.object.series_set.all():

            context['forms'][series.pk] = dict()

            for problem in series.problemset.problems.all():
                solutions = UserSolution.objects.filter(user=self.request.user.pk, problem=problem.pk)
                if not solutions:
                    form = UserSolutionForm(initial={'problem': problem})
                else:
                    form = UserSolutionForm(instance=solutions[0])

                context['forms'][series.pk][problem.pk] = form

        return context

