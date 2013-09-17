from django.conf.urls import patterns, url

from .views import PostListView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name="posts_post_list")
)
