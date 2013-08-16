import reversion

from django.db import models
from django.contrib import admin


class Leaflet(models.Model):
    '''
    Represents a given (generated) leaflet.
    '''

    def generate_name(self, filename):
        return "leaflets/{competition}-{year}-{issue}.pdf"\
               .format(competition=self.competition,
                       year=self.year,
                       issue=self.issue)

    def __unicode__(self):
        return "{competition}-{year}-{issue}"\
               .format(competition=self.competition,
                       year=self.year,
                       issue=self.issue)

    competition = models.ForeignKey('competitions.Competition')
    year = models.IntegerField()
    issue = models.IntegerField()
    leaflet = models.FileField(upload_to=generate_name)

    # Fields added via foreign keys:

    #  problemset_set

    # TODO: more than one problemset can point to given leaflet, is that a
    #       problem?

    class Meta:
        ordering = ['competition', '-year', 'issue']
        verbose_name = 'Leaflet'
        verbose_name_plural = 'Leaflets'


class LeafletAdmin(reversion.VersionAdmin):

    list_display = ('competition',
                    'year',
                    'issue',
                    )


# Register to the admin site
admin.site.register(Leaflet, LeafletAdmin)
