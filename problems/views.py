from django.contrib import messages

from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from problems.models import Problem
from problems.forms import UserSolutionForm


class ProblemListView(ListView):

    model = Problem
    context_object_name = 'problems'


class ProblemDetailView(DetailView):

    model = Problem
    context_object_name = 'problem'


class UserSolutionSubmissionView(View):

    form_class = UserSolutionForm

    def get(self, request, *args, **kwargs):
        return redirect('competitions_season_detail', pk=1)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
        else:
            for field, errors in form.errors.iteritems():
                messages.error(request, u"{error}".format(
                                    error=', '.join(errors))
                              )

        return redirect('competitions_season_detail', pk=1)
