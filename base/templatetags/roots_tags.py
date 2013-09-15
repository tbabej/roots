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