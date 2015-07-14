from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class IndexDashboard(Dashboard):
    """
    Custom index dashboard for Roots.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.LinkList(
            _('Administration modules'),
            column=1,
            children=[
                {
                    'title': _('Content management'),
                    'url': reverse('admin_dashboard_content'),
                    'external': False,
                    'description': _(
                        'Add/change static content, such as posts, news '
                        'or galleries.')
                },
                {
                    'title': _('Competition management'),
                    'url': reverse('admin_dashboard_competition'),
                    'external': False,
                    'description': _(
                        'Manage seminar activities, add seasons, '
                        'deal with user solutions and more.')
                },
                {
                    'title': _('Problem database'),
                    'url': reverse('admin_dashboard_problems'),
                    'external': False,
                    'description': _(
                        'Find problem statements. Create problem sets. '
                        'Add new problems to help us grow the database.')
                },
                {
                    'title': _('User and school database'),
                    'url': reverse('admin_dashboard_users'),
                    'external': False,
                    'description': _(
                        'Manage users and their profiles. Edit '
                        'our database of schools.')
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))


class ProblemsDashboard(Dashboard):
    """
    Custom problems dashboard for Roots.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Content'),
            column=1,
            collapsible=False,
            models=(
                'problems.*',
                ),
        ))


class ContentDashboard(Dashboard):
    """
    Custom static content dashboard for Roots.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            _('Content'),
            column=1,
            collapsible=False,
            models=(
                'posts.*',
                'django.contrib.flatpages.*',
                'news.*',
                'leaflets.*',
                'photologue.*',
                ),
            exclude=(
                'photologue.models.PhotoEffect',
                'photologue.models.PhotoSize',
                'photologue.models.Watermark',
                ),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('File management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                    'description': _('Use to upload images or other files '
                                     'to use in posts, news, static pages, '
                                     'and elsewhere on the site.'),
                },
            ]
        ))


class CompetitionDashboard(Dashboard):
    """
    Custom problems dashboard for Roots.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Content'),
            column=1,
            collapsible=False,
            models=(
                'competitions.*',
                'profiles.*',
                ),
        ))
