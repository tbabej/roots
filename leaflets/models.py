from django.db import models
from django.contrib import admin


class Leaflet(models.Model):
    '''
    Represents a given (generated) leaflet.
    '''

    competition = models.ForeignKey('competitions.Competition')
    year = models.IntegerField()
    issue = models.IntegerField()

    # Fields added via foreign keys:

    #  problemset_set

    # TODO: more than one problemset can point to given leaflet, is that a
    #       problem?

    def __unicode__(self):
        return u"Leaflet for " + self.competition.__unicode__()

    class Meta:
        ordering = ['competition', 'year', 'issue']
        verbose_name = 'Leaflet'
        verbose_name_plural = 'Leaflets'


# Register to the admin site
admin.site.register(Leaflet)
