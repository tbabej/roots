from django.conf.urls import patterns, url

from problems.views import ProblemListView, ProblemDetailView
from problems.views import user_problem_submission

urlpatterns = patterns('',
#    url(r'^$', ProblemListView.as_view(), name='problems_problem_list'),
    url(r'^(?P<pk>\d+)/$', ProblemDetailView.as_view(),
        name='problems_problem_detail'),
    url(r'^submit/$', user_problem_submission,
        name='problems_usersolution_submit')
)
