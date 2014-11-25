from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _

from djangoratings.fields import RatingField
from sortedm2m.fields import SortedManyToManyField

from base.models import MediaRemovalMixin, ContentTypeRestrictedFileField
from base.storage import OverwriteFileSystemStorage
from base.templatetags.roots_tags import remove_uncomplete_latex
from base.util import with_timestamp, with_author

from competitions.models import Competition
from downloads.models import AccessFilePermissionMixin


# Solution-related models

@with_author
@with_timestamp
class UserSolution(MediaRemovalMixin,
                   AccessFilePermissionMixin,
                   models.Model):
    '''
    Represents a user submitted solution of a given problem.
    '''

    media_root = settings.SENDFILE_ROOT

    @classmethod
    def get_by_filepath(cls, path):
        try:
            return cls.objects.get(solution=path)
        except ObjectDoesNotExist:
            try:
                return cls.objects.get(corrected_solution=path)
            except ObjectDoesNotExist:
                return None

    def can_access_files(self, user):
        if self.user == user:
            # If you are the author, you can access
            return True
        else:
            # If the problem is in the competition you organize, you can access
            # the solution
            organizer_group = self.problem.competition.organizer_group
            return user.groups.filter(id=organizer_group.pk).exists()

    def get_media_files(self):
        return [self.get_solution_path()]

    def get_solution_path(self, *args, **kwargs):
        return 'solutions/' + self.get_id_string()

    def get_corrected_solution_path(self, *args, **kwargs):
        return 'corrected_solutions/' + self.get_id_string()

    def get_id_string(self):
        return '{user}-{problem}.pdf'.format(
                user=self.user.username,
                problem=self.problem.pk,
            )

    # Keep an explicit reference to an User, since somebody else might
    # be entering the solution on the user's behalf
    user = models.ForeignKey('auth.User',
                             verbose_name=_('user'))

    problem = models.ForeignKey('problems.Problem',
                                verbose_name=_('problem'))

    solution = ContentTypeRestrictedFileField(
                                null=True,
                                upload_to=get_solution_path,
                                storage=OverwriteFileSystemStorage(location=settings.SENDFILE_ROOT,
                                                                   base_url=settings.SENDFILE_URL),
                                max_size=settings.ROOTS_MAX_SOLUTION_SIZE,
                                verbose_name=_('solution'))

    corrected_solution = ContentTypeRestrictedFileField(
                                blank=True,
                                null=True,
                                upload_to=get_corrected_solution_path,
                                storage=OverwriteFileSystemStorage(location=settings.SENDFILE_ROOT,
                                                                   base_url=settings.SENDFILE_URL),
                                max_size=settings.ROOTS_MAX_SOLUTION_SIZE,
                                verbose_name=_('corrected solution'))

    score = models.IntegerField(blank=True,
                                null=True,
                                verbose_name=_('score'))

    classlevel = models.CharField(max_length=2,
                                  blank=True,
                                  null=True,
                                  verbose_name=_('class level at the time '
                                                 'of submission'),
                                  choices=(('Z2', 'Z2'),
                                           ('Z3', 'Z3'),
                                           ('Z4', 'Z4'),
                                           ('Z5', 'Z5'),
                                           ('Z6', 'Z6'),
                                           ('Z7', 'Z7'),
                                           ('Z8', 'Z8'),
                                           ('Z9', 'Z9'),
                                           ('S1', 'S1'),
                                           ('S2', 'S2'),
                                           ('S3', 'S3'),
                                           ('S4', 'S4')))

    school = models.ForeignKey('schools.School',
                               blank=True,
                               null=True,
                               verbose_name=_('school'))

    school_class = models.CharField(max_length=20,
                                    blank=True,
                                    null=True,
                                    verbose_name=_('school class'))

    note = models.CharField(max_length=200, blank=True, null=True)

    corrected_by = models.ManyToManyField('auth.User',
                       related_name='usersolutions_corrected_set',
                       verbose_name=_('corrected by'))

    user_modified_at = models.DateTimeField(verbose_name=_('last user modification'),
                                            auto_now=True,
                                            editable=False)

    def __unicode__(self):
        return unicode(_("User solution: {user} - {problem_id}")
                       .format(user=unicode(self.user),
                               problem_id=unicode(self.problem.pk))
               )

    def save(self, *args, **kwargs):
        self.school = self.school or self.user.userprofile.school
        self.school_class = (self.school_class or
                             self.user.userprofile.school_class)
        self.classlevel = self.classlevel or self.user.userprofile.classlevel

        super(UserSolution, self).save(*args, **kwargs)

    class Meta:
        order_with_respect_to = 'problem'
        verbose_name = _('user solution')
        verbose_name_plural = _('user solutions')
        unique_together = ['user', 'problem']


@with_author
@with_timestamp
class OrgSolution(models.Model):
    '''
    Represents an ideal solution of a problem. There can be multiple ideal
    solutions (more organizers trying to solve it, more ways of solving).
    '''

    # Keep an explicit reference to an Organizer, since somebody else might
    # be entering the solution on the organizer's behalf
    organizer = models.ForeignKey('auth.User',
                                  verbose_name=_('organizer'))
    problem = models.ForeignKey('problems.Problem',
                                verbose_name=_('problem'))

    def __unicode__(self):
        return unicode(_("Organizer solution: {user} - {problem_id}")
                         .format(user=unicode(self.organizer),
                                 problem_id=unicode(self.problem.pk))
               )

    class Meta:
        order_with_respect_to = 'problem'
        verbose_name = _('organizer solution')
        verbose_name_plural = _('organizer solutions')


# Problem-related models

@with_author
@with_timestamp
class Problem(models.Model):
    '''
    Represents a problem.
    '''

    def get_rating(self):
        return self.rating.get_rating()
    get_rating.short_description = _('Rating')

    def get_usages(self):
        # FIXME: problemsets that have no event will not be displayed
        sets = self.problemset_set.order_by('-event__start_time')\
                                  .filter(event__isnull=False)

        if sets.exists():
            return sets
        else:
            return []

    def last_used_at(self):
        usages = self.get_usages()

        if usages:
            if usages[0].event:
                return usages[0].event

    def last_five_usages(self):
        usages = self.get_usages()[:5]

        if usages:
            return ', '.join([str(problemset.event) for problemset in usages])
        else:
            return ''

    def times_used(self):
        return len(self.get_usages())

    text = models.TextField(verbose_name=_('problem text'),
                            help_text=_('The problem itself. Please insert it '
                                        'in a valid TeX formatting.'))
    result = models.TextField(verbose_name=_('Result / short solution outline'),
                              help_text=_('The result of the problem. For '
                                          'problems that do not have simple '
                                          'results, a hint or short outline of '
                                          'the solution.'),
                              blank=True,
                              null=True)
    rating = RatingField(range=5,
                         verbose_name=_('rating'))
    severity = models.ForeignKey('problems.ProblemSeverity',
                                 verbose_name=_('severity'))
    category = models.ForeignKey('problems.ProblemCategory',
                                 verbose_name=_('category'))
    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    source = models.CharField(max_length=500,
                              blank=True,
                              null=True,
                              verbose_name=_('problem source'),
                              help_text=_('Source where you found the problem'
                                          '(if not original).'))
    image = models.ImageField(storage=OverwriteFileSystemStorage(),
                              blank=True,
                              null=True,
                              upload_to='problems/',
                              verbose_name=_('image'),
                              help_text=_('Image added to the problem text.'))
    additional_files = models.FileField(
                           blank=True,
                           null=True,
                           upload_to='problems/',
                           storage=OverwriteFileSystemStorage(),
                           verbose_name=_('additional files'),
                           help_text=_('Additional files stored with the '
                                       'problem (such as editable images).'))

    # Fields added via foreign keys:

    #  orgsolution_set
    #  problemset_set
    #  user_set
    #  usersolution_set

    def __unicode__(self):
        return remove_uncomplete_latex(truncatewords(self.text, 10))

    class Meta:
        verbose_name = _('problem')
        verbose_name_plural = _('problems')


class ProblemInSet(models.Model):

    problem = models.ForeignKey('problems.Problem',
                                verbose_name=_('problem'))
    problemset = models.ForeignKey('problems.ProblemSet',
                                   verbose_name=_('problem set'))
    position = models.PositiveSmallIntegerField(verbose_name=_('position'))

    # This is here as a reference for the SortedManyToManyField
    _sort_field_name = 'position'

    def get_rating(self):
        return self.problem.get_rating()

    def get_usages(self):
        return self.problem.get_usages()

    def last_used_at(self):
        return self.problem.last_used_at()

    def last_five_usages(self):
        return self.problem.last_five_usages()

    def times_used(self):
        return self.problem.times_used()

    def get_category(self):
        return self.problem.category

    def get_severity(self):
        return self.problem.severity

    def get_competition(self):
        return self.problem.competition

    get_rating.short_description = _('Rating')
    get_usages.short_description = _('Usages')
    last_used_at.short_description = _('Last used at')
    last_five_usages.short_description = _('Last five usages')
    times_used.short_description = _('Times used')
    get_category.short_description = _('Category')
    get_severity.short_description = _('Severity')
    get_competition.short_description = _('Competition')

    def __unicode__(self):
        return self.problem.__unicode__()

    class Meta:
        verbose_name = _('problem')
        verbose_name_plural = _('problems')
        ordering = ['position']
        unique_together = ['problem', 'problemset']


@with_author
@with_timestamp
class ProblemSet(models.Model):
    '''
    Represents a collections of problems. This can (optionally) be used at
    event or competition, which organizer should mark here.
    '''

    name = models.CharField(max_length=100,
                            verbose_name=('name'))
    description = models.CharField(max_length=400,
                                   blank=True,
                                   null=True,
                                   verbose_name=('description'))
    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    leaflet = models.ForeignKey('leaflets.Leaflet',
                                blank=True,
                                null=True,
                                verbose_name=_('leaflet'))
    event = models.ForeignKey('events.Event',
                              blank=True,
                              null=True,
                              verbose_name=_('event'))

    problems = SortedManyToManyField(Problem,
                                     through='problems.ProblemInSet',
                                     verbose_name=_('problems'),
                                     sort_value_field_name='position')

    def average_severity(self):
        problemset = self.problems.filter(competition=self.competition)
        average = problemset.aggregate(
                      models.Avg('severity__level'))['severity__level__avg']
        return average

    def average_severity_by_competition(self):
        averages = dict()

        for competition in Competition.objects.all():
            problemset = self.problems.filter(competition=competition)
            average = problemset.aggregate(
                          models.Avg('severity__level'))['severity__level__avg']

            if average:
                key = unicode(competition)
                averages[key] = average

        return averages

    def __unicode__(self):
        return self.name

    def get_problem_count(self):
        return self.problems.count()
    get_problem_count.short_description = _("problems")

    def get_average_severity_by_competition(self):
        averages = self.average_severity_by_competition()
        reports = []
        for competition, average in averages.iteritems():
            reports.append("%s (%s)" % (competition, average))

        return ', '.join(reports)
    get_average_severity_by_competition.short_description = _("average "
                                                              "difficulty")

    class Meta:
        verbose_name = _('Problem set')
        verbose_name_plural = _('Problem sets')


class ProblemCategory(models.Model):
    '''
    Represents a category of problems, like geometry or functional equations.
    '''

    name = models.CharField(max_length=50,
                            verbose_name=_('name'))
    competition = models.ForeignKey(
        'competitions.Competition',
        verbose_name=_('competition'),
        help_text=_('The reference to the competition that uses this category. '
                    'It makes sense to have categories specific to each '
                    'competition, since problem types in competitions '
                    'may differ significantly.'))

    # Fields added via foreign keys:
    #     problem_set

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.competition)

    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')


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

    name = models.CharField(max_length=50,
                            verbose_name=_('name'))
    level = models.IntegerField(verbose_name=_('level'))
    competition = models.ForeignKey(
        'competitions.Competition',
        verbose_name=_('competition'),
        help_text=_('The reference to the competition that uses this severity. '
                    'It makes sense to have severities specific to each '
                    'competition, since organizers might have different '
                    'ways of sorting the problems regarding their severity.'))

    def __unicode__(self):
        return unicode(self.level) + ' - ' + self.name

    class Meta:
        ordering = ['level']
        verbose_name = _('severity')
        verbose_name_plural = _('severities')
