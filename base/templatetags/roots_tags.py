from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def url_active(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return "active"
    return "request.path: {req}, urls: {url}".format(
            req=request.path,
            url=", ".join(reverse(url) for url in urls.split())
        )

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

