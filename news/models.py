from django.db import models
from django.utils.translation import ugettext as _
from base.util import with_author, with_timestamp

from django.contrib.sites.models import Site

@with_author
@with_timestamp
class News(models.Model):
    """
    Represents a short information message.
    """

    heading = models.CharField(max_length=500,
                               verbose_name=_('heading'))
    text = models.CharField(max_length=500,
                            verbose_name=_('text'),
                            null=True,
                            blank=True)
    sites = models.ManyToManyField(Site)

    def get_sites(self):
        return ','.join([site.name for site in self.sites.all()])
    get_sites.short_description = _("Published on sites")

    @staticmethod
    def autocomplete_search_fields():
        return ("heading__icontains",)

    def __unicode__(self):
        return self.heading

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
