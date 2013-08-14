from django.db import models
from django.contrib import admin
from base.util import with_author, with_timestamp


# Content-related models
@with_author
@with_timestamp
class Post(models.Model):
    '''
    Represents a post on the wall. This can be restricted to certain competition
    or can be general.
    '''

    title = models.CharField(max_length=100)
    competition = models.ForeignKey('competitions.Competition', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


# Register to the admin site
admin.site.register(Post)
