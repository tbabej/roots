import reversion

from base.util import with_timestamp, with_author
from django.contrib import admin
from django.db import models
from djangoratings.fields import RatingField


# Solution-related models

@with_author
@with_timestamp
class UserSolution(models.Model):
    '''
    Represents a user submitted solution of a given problem.
    '''

    # Keep an explicit reference to an User, since somebody else might
    # be entering the solution on the user's behalf
    user = models.ForeignKey('auth.User')
    problem = models.ForeignKey('problems.Problem')

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s solution of " +
                self.problem.__unicode__())

    class Meta:
        order_with_respect_to = 'problem'
        verbose_name = 'User solution'
        verbose_name_plural = 'User solutions'


@with_author
@with_timestamp
class OrgSolution(models.Model):
    '''
    Represents an ideal solution of a problem. There can be multiple ideal
    solutions (more organizers trying to solve it, more ways of solving).
    '''

    # Keep an explicit reference to an Organizer, since somebody else might
    # be entering the solution on the organizer's behalf
    organizer = models.ForeignKey('auth.User')
    problem = models.ForeignKey('problems.Problem')

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s ideal solution of " +
                self.problem.__unicode__())

    class Meta:
        order_with_respect_to = 'problem'
        verbose_name = 'Organizer solution'
        verbose_name_plural = 'Organizer solutions'


# Problem-related models

@with_author
@with_timestamp
class Problem(models.Model):
    '''
    Represents a problem.
    '''

    def get_rating(self):
        return self.rating.get_rating()
    get_rating.short_description = 'Rating'

    text = models.CharField(max_length=1000,
                            help_text='The problem itself. Please insert it '
                                      'in a valid TeX formatting.')
    rating = RatingField(range=5)
    severity = models.ForeignKey('problems.ProblemSeverity')
    category = models.ForeignKey('problems.ProblemCategory')
    competition = models.ForeignKey('competitions.Competition')

    # Fields added via foreign keys:

    #  orgsolution_set
    #  problemset_set
    #  user_set
    #  usersolution_set

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'


# Reversion-enabled Admin for problems
class ProblemAdmin(reversion.VersionAdmin):

    list_display = ('text',
                    'get_rating',
                    'severity',
                    'category',
                    'competition',
                    'author',
                    )

    list_filter = ('competition', 'severity', 'category')
    search_fields = ['text']
    readonly_fields = ('author', 'updated_by', 'added_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('text', 'severity', 'category', 'competition')
        }),
        ('Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('author', 'updated_by', 'added_at', 'modified_at')
        }),
    )


@with_author
@with_timestamp
class ProblemSet(models.Model):
    '''
    Represents a collections of problems. This can (optionally) be used at
    event or competition, which organizer should mark here.
    '''

    competition = models.ForeignKey('competitions.Competition')
    leaflet = models.ForeignKey('leaflets.Leaflet',
                                blank=True, null=True)
    problems = models.ManyToManyField(Problem)

    def __unicode__(self):
        return u"ProblemSet for " + self.competition.__unicode__()

    class Meta:
        verbose_name = 'Set'
        verbose_name_plural = 'Sets'


class ProblemCategory(models.Model):
    '''
    Represents a category of problems, like geometry or functional equations.
    '''

    name = models.CharField(max_length=50)

    # Fields added via foreign keys:

        # problem_set

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProblemSeverity(models.Model):
    '''
    Lets you define custom levels of severity for problems.

    Severity level is represented by its name and level, e.g.:
        easy - 1
        medium -2
        hard - 3
        godlike - 4

    This is not hardcoded so that every organization can use their own
    levels of severity to categorize their problems.
    '''

    name = models.CharField(max_length=50)
    level = models.IntegerField()

    def __unicode__(self):
        return unicode(self.level) + ' - ' + self.name

    class Meta:
        ordering = ['level']
        verbose_name = 'Severity'
        verbose_name_plural = 'Severities'


# Register to the admin site
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemSet)
admin.site.register(UserSolution)
admin.site.register(OrgSolution)
admin.site.register(ProblemCategory)
admin.site.register(ProblemSeverity)
