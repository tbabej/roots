from django.conf.urls import patterns, url

from .views import PostListView, PostDetailView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name="posts_post_list"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(),
        name="posts_post_detail")
)
