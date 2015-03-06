from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.util import with_author, with_timestamp


# Content-related models
@with_author
@with_timestamp
class Post(models.Model):
    '''
    Represents a post on the wall. This can be restricted to certain competition
    or can be general.
    '''

    title = models.CharField(max_length=100,
                             verbose_name=_('title'))
    competition = models.ForeignKey('competitions.Competition',
                                    blank=True,
                                    null=True,
                                    verbose_name=_('competition'))
    text = models.TextField(verbose_name=_('text'))
    slug = models.SlugField(verbose_name=_('slug'))
    gallery = models.ForeignKey('photologue.Gallery',
                                blank=True,
                                null=True,
                                verbose_name=_('associated gallery'),
                                help_text=_('gallery to be previewed with the'
                                            'post'))

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains", "competition__name__icontains")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
