import os

from local_settings import *
from base.permissions import wiki_can_read

# Django settings for roots project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# All-auth requirement
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "sekizai.context_processors.sekizai",
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'roots.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'roots.wsgi.application'


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = (
    # Roots specific apps
    'base',
    'competitions',
    'downloads',
    'events',
    'leaflets',
    'photos',
    'posts',
    'problems',
    'profiles',
    'schools',
    # Grapelli comes first
    'grappelli',
    # Non-roots specific apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    #
    # Social authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.twitter',
    # Support for django-extensions
    'django_extensions',
    # Support database migrations
    'south',
    # Use django-ratings
    'djangoratings',
    # Use django-author
    'author',
    # Use django-reversion
    'reversion',
    # Use django-photologue
    'photologue',
    # Use django-debug-toolbar
    'debug_toolbar',
    # Use django-mathjax
    'django_mathjax',
    # Use crispy-forms
    'crispy_forms',
    # Use django-jquery
    'jquery',
    # Use django-jquery-lightbox
    'jquery_lightbox',
    # Use django-sendfile
    'sendfile',
    # Use django-wiki and its requirements
    'django.contrib.humanize',
    'django_notify',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.links',
    'wiki.plugins.help',
    'wiki.plugins.macros',
)

GRAPPELLI_ADMIN_HEADLINE = 'Roots administration'
GRAPPELLI_ADMIN_TITLE = 'Roots'

AUTHOR_CREATED_BY_FIELD_NAME = 'added_by'
AUTHOR_UPDATED_BY_FIELD_NAME = 'modified_by'

# Remove (None) values from the Admin
from django.contrib.admin.views import main
main.EMPTY_CHANGELIST_VALUE = u''

# Set the message tags as classes in Bootstrap
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
        message_constants.DEBUG: 'alert-info',
        message_constants.INFO: 'alert-info',
        message_constants.SUCCESS: 'alert-success',
        message_constants.WARNING: 'alert-warning',
        message_constants.ERROR: 'alert-danger',
    }

# Require email address at sign up
ACCOUNT_EMAIL_REQUIRED = True

# Get the projet root
path_parts = os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]
PROJECT_ROOT = '/'.join(path_parts) + '/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + 'templates/',
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT + 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT + 'static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Django-wiki related settings
WIKI_ATTACHMENTS_EXTENSIONS = ['pdf', 'doc', 'odt', 'docx', 'txt', 'zip',
                               'rar', 'tar', 'gz', 'jpg', 'jpeg', 'png', 'gif',
                               'tex']
WIKI_ANONYMOUS = False  # Do not allow anonymous access
WIKI_CAN_READ = wiki_can_read
WIKI_ACCOUNT_HANDLING = False


# Enable Django-MathJax
MATHJAX_ENABLED = True

MATHJAX_CONFIG_FILE = "TeX-AMS_HTML.js"

MATHJAX_CONFIG_DATA = {
    "tex2jax": {
        "inlineMath":
            [
               ['$', '$'],
            ]
     }
}

# Crispy froms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django-sendfile related settings
SENDFILE_DIR = 'protected/'
SENDFILE_ROOT = os.path.join(MEDIA_ROOT, SENDFILE_DIR)
SENDFILE_URL = MEDIA_URL + SENDFILE_DIR

# Roots-related settings
ROOTS_MAX_SOLUTION_SIZE = 10485760  # 10MB
