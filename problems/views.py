# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from problems.models import Problem  # , UserSolution, OrgSolution


def index(request):
    problems = Problem.objects.all()
    context = dict(problem_list=problems)

    return render(request, 'problems/index.html', context)


def problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    context = dict(id=problem.pk,
                   text=problem.text)

    return render(request, 'problems/problem.html', context)