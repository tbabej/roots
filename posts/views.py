from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):

    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Order posts by the day they were added, from newest, to oldest.
        """

        queryset = super(PostListView, self).get_queryset()
        return queryset.order_by('-added_at')


class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
