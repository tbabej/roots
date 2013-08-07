from django.db import models
from django.contrib import admin


# Content-related models
class Post(models.Model):
    '''
    Represents a post on the wall. This can be restricted to certain competition
    or can be general.
    '''

    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    competition = models.ForeignKey('competitions.Competition', blank=True)

    def __unicode__(self):
        return self.title


class Gallery(models.Model):
    '''
    Represents a gallery of photos. This can be restricted to certain
    competition or event.
    '''

    name = models.CharField(max_length=50)
    competition = models.ForeignKey('competitions.Competition')
    event = models.ForeignKey('events.Event')
    date = models.DateTimeField()

    def __unicode__(self):
        return self.name

# Register to the admin site
admin.site.register(Post)
admin.site.register(Gallery)
