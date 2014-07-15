from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import PostListView, PostDetailView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name="posts_post_list"),
    url(_(r'^(?P<slug>[\w-]+)/$'), PostDetailView.as_view(),
        name="posts_post_detail")
)
