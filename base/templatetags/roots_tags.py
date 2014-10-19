from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.base import TemplateSyntaxError
from django.utils.text import ugettext_lazy as _
from news.models import News

register = template.Library()


@register.simple_tag
def rereverse(request):
    return reverse(request.resolver_match.view_name,
                   args=request.resolver_match.args,
                   kwargs=request.resolver_match.kwargs)

@register.simple_tag
def url_active(request, urls, *args, **kwargs):
    if request.path in (reverse(url, args=list(*args), kwargs=dict(**kwargs))
                        for url in urls.split()):
        return "active"
    else:
        return ""

from django.contrib.sites.models import get_current_site

@register.simple_tag
def current_site(request):
    return get_current_site(request).name


@register.filter
def remove_uncomplete_latex(text):
    # Even number of segments separated by $$ means uncomplete
    # display equation
    if len(text.split('$$')) % 2 == 0:
        # Return the original text
        return '$$'.join(text.split('$$')[:-1])
    elif len(text.split('$')) % 2 == 0:
        return '$'.join(text.split('$')[:-1])
    else:
        return text


class DefineNode(template.Node):
    def __init__(self, name, nodelist):
        self.name = name
        self.nodelist = nodelist

    def __repr__(self):
        return "<DefineNode>"

    def render(self, context):
        context[self.name] = self.nodelist.render(context)
        return ''


@register.tag
def define(parser, token):
    """
    Adds a name to the context for referencing an arbitrarily defined block
    of template code.

    For example:

        {% define my_block %}
        This is the content.
        {% enddefine %}

    Now anywhere in the template:

        {{ my_block }}
    """

    bits = list(token.split_contents())

    if len(bits) != 2:
        raise TemplateSyntaxError("Expected format is: {% define variable %}")

    name = bits[1]
    nodelist = parser.parse(('enddefine',))
    parser.delete_first_token()

    return DefineNode(name, nodelist)


@register.filter
def access(value, arg):
    return value.get(arg, {})


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

# The following comment tags are altered versions of django.contrib.comments's
# template tags. Alternation happens by allowing private comments

from django.contrib.comments.templatetags.comments import BaseCommentNode
from django.utils.encoding import smart_text

class PrivateCommentNode(BaseCommentNode):
    def get_queryset(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.comment_model.objects.none()

        qs = self.comment_model.objects.filter(
            content_type = ctype,
            object_pk    = smart_text(object_pk),
            site__pk     = settings.SITE_ID,
        )

        # The is_public and is_removed fields are implementation details of the
        # built-in comment model's spam filtering system, so they might not
        # be present on a custom comment model subclass. If they exist, we
        # should filter on them.
        field_names = [f.name for f in self.comment_model._meta.fields]
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(is_removed=False)

        return qs


class PrivateCommentListNode(PrivateCommentNode):
    """Insert a list of comments into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return list(qs)


class PrivateCommentCountNode(PrivateCommentNode):
    """Insert a count of comments into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return qs.count()


@register.tag
def get_comment_count_private(parser, token):
    return PrivateCommentCountNode.handle_token(parser, token)


@register.tag
def get_comment_list_private(parser, token):
    return PrivateCommentListNode.handle_token(parser, token)

@register.filter(expects_localtime=True)
def timedelta_to_string(delta, form='days_hours_minutes_seconds'):
    days = delta.days
    hours = (delta.seconds // 3600)
    minutes = (delta.seconds // 60) % 60
    seconds = delta.seconds % 60


    if form == 'days_hours_minutes_seconds':
        template_string = _("{days} days, {hours} hours, {minutes} minutes and {seconds} seconds")
    elif form == 'days_hours_minutes':
        template_string = _("{days} days, {hours} hours and {minutes} minutes")
    elif form == 'days_hours':
        template_string = _("{days} days and {hours} hours")
    elif form == 'days':
        template_string = _("{days} days")
    else:
        return ""

    return template_string.format(days=days, hours=hours, minutes=minutes, seconds=seconds)

@register.assignment_tag
def get_last_news(num=5):
    news = News.objects.order_by('-added_at')[:num]
    return news

@register.filter
def representation(var):
    return repr(var) + " and type: " + str(type(var))