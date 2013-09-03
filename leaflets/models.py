from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from base import util


class Leaflet(models.Model):
    '''
    Represents a given (generated) leaflet.
    '''

    def generate_name(self, *args):
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


@receiver(post_save)
def generate_leaflet_thumbnail(sender, instance, created, **kwargs):
    if sender == Leaflet and created:
        source_path = instance.generate_name(None)
        dest_path = source_path.replace('leaflets/', 'leaflets/thumbnails/')\
                               .replace('.pdf', '.jpg')

        util.generate_pdf_thumbnail(source=source_path,
                                    destination=dest_path,
                                    height=297,
                                    width=210)
