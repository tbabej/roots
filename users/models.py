from django.db import models
from django.contrib import admin


# User-related models
class User(models.Model):
    '''
    Represents an user. Both organizers and participants are considered as
    users. This allows usage of the same accounts for the users that became
    organizers later.
    '''

    login = models.CharField(max_length=50)
    competes = models.ManyToManyField('competitions.Competition',
                    through='competitions.CompetitionUserRegistration')
    solved = models.ManyToManyField('problems.Problem')

    def __unicode__(self):
        return self.login


class Organizer(User):
    '''
    Represents an organizer. Organizer can organize multiple competitions
    or events.
    '''

    motto = models.CharField(max_length=50)

# Register to the admin site
admin.site.register(User)
admin.site.register(Organizer)
