from django.conf.urls import patterns, url

from problems.views import ProblemListView, ProblemDetailView

urlpatterns = patterns('',
    url(r'^$', ProblemListView.as_view(), name='problems_problem_list'),
    url(r'^(?P<pk>\d+)/$', ProblemDetailView.as_view(),
        name='problems_problem_detail')
)