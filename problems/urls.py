from django.conf.urls import patterns, url

from problems import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='problems_index'),
    url(r'^(?P<problem_id>\d+)/$', views.problem, name='problems_detail')
)