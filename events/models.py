from django.db import models
from django.contrib import admin


# Event-related models
class Event(models.Model):
    name = models.CharField(max_length=100)
    galerry = models.ForeignKey('posts.Gallery')
    registered_user = models.ManyToManyField('users.User',
                                             through='EventUserRegistration')
    registered_org = models.ManyToManyField('users.Organizer',
                                            through='EventOrgRegistration',
                                            related_name='organizers')

    def __unicode__(self):
        return self.name


class EventUserRegistration(models.Model):
    event = models.ForeignKey('events.Event')
    user = models.ForeignKey('users.User')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" goes to " +
               self.event.__unicode__())


class EventOrgRegistration(models.Model):
    event = models.ForeignKey('events.Event')
    organizer = models.ForeignKey('users.Organizer')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.event.__unicode__())


class Camp(Event):
    location = models.CharField(max_length=100)  # temporary placeholder

    def __unicode__(self):
        return self.location


# Register to the admin site
admin.site.register(Event)
admin.site.register(EventUserRegistration)
admin.site.register(EventOrgRegistration)
admin.site.register(Camp)