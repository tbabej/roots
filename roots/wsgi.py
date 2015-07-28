"""
WSGI config for roots project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roots.settings")

paths = [
    '/var/www/roots-env/roots',
    '/var/www/roots-env/lib/python2.7/site-packages'
]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

from django.core.handlers.wsgi import WSGIHandler
import django

class WSGIEnvironment(WSGIHandler):

    def __call__(self, environ, start_response):

        if 'DJANGO_SITE_ID' in environ:
            os.environ['DJANGO_SITE_ID'] = environ['DJANGO_SITE_ID']

        django.setup()
        return super(WSGIEnvironment, self).__call__(environ, start_response)

application = WSGIEnvironment()
