from django.db import models
from django.contrib import admin


# Content-related models
class Post(models.Model):
    organizer = models.ForeignKey('users.Organizer')
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Gallery(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

# Register to the admin site
admin.site.register(Post)
admin.site.register(Gallery)
