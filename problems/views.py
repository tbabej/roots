from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from problems.models import Problem
from problems.forms import UserSolutionForm


class ProblemListView(ListView):

    model = Problem
    context_object_name = 'problems'


class ProblemDetailView(DetailView):

    model = Problem
    context_object_name = 'problem'


def user_problem_submission(request):
    if request.method == 'POST':

        submission = UserSolutionForm(request.POST,
                                      request.FILES).save(commit=False)
        submission.user = request.user
        submission.save()

        return redirect('competitions_season_detail', pk=1)
