from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):

    model = Post
    context_object_name = 'posts'

class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
