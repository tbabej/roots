from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from base import util
from base.models import MediaRemovalMixin


class Leaflet(MediaRemovalMixin, models.Model):
    '''
    Represents a given (generated) leaflet.
    '''

    def get_leaflet_path(self, *args):
        return "leaflets/{name}.pdf".format(name=unicode(self))

    def get_thumbnail_path(self):
        return "leaflets/thumbnails/{name}.jpg".format(name=unicode(self))

    def get_media_files(self):
        return [self.get_leaflet_path(), self.get_thumbnail_path()]

    def __unicode__(self):
        return "{competition}-{year}-{issue}"\
               .format(competition=self.competition,
                       year=self.year,
                       issue=self.issue)

    competition = models.ForeignKey('competitions.Competition')
    year = models.IntegerField()
    issue = models.IntegerField()
    leaflet = models.FileField(upload_to=get_leaflet_path)

    def save(self, *args, **kwargs):
        if self.pk:
            self.leaflet = self.get_leaflet_path()
        return super(Leaflet, self).save(*args, **kwargs)

    # Fields added via foreign keys:

    #  problemset_set

    # TODO: more than one problemset can point to given leaflet, is that a
    #       problem?

    class Meta:
        ordering = ['competition', '-year', 'issue']
        unique_together = ('competition', 'year', 'issue')
        verbose_name = 'Leaflet'
        verbose_name_plural = 'Leaflets'


@receiver(post_save, sender=Leaflet)
def generate_leaflet_thumbnail(sender, instance, created, **kwargs):
    if created:
        source_path = instance.get_leaflet_path()
        dest_path = instance.get_thumbnail_path()

        util.generate_pdf_thumbnail(source= source_path,
                                    destination=dest_path,
                                    height=212,
                                    width=150)
