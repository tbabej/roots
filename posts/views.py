from django.contrib.sites.models import Site

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

        # Display posts only relevant for this site
        current_site = Site.objects.get_current()
        queryset = queryset.filter(sites=current_site)

        # If user does not manage the site, do not display
        # not-published articles
        # TODO: This needs to be done properly with respect
        # to the actual permissions
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)

        return queryset.order_by('-added_at')


class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
