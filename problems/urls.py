from django.conf.urls import patterns, url

from problems.views import ProblemDetailView
from problems.views import UserSolutionSubmissionView
from problems.views import ImportCorrectedSolutionsView


urlpatterns = patterns('',
#    url(r'^$', ProblemListView.as_view(), name='problems_problem_list'),
    url(r'^(?P<pk>\d+)/$', ProblemDetailView.as_view(),
        name='problems_problem_detail'),
    url(r'^submit/$', UserSolutionSubmissionView.as_view(),
        name='problems_usersolution_submit'),
    url(r'^import-solutions/$', ImportCorrectedSolutionsView.as_view(),
        name='problems_import_solutions_from_zip')
)
