from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.views.generic import TemplateView
from base.views import IndexView, LoginRedirectView
from django.conf import settings
from django.conf.urls.static import static

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern
from filebrowser.sites import site

admin.autodiscover()

# Add basic non-localized patterns
urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='roots_index'),
    url(r'^login/$', LoginRedirectView.as_view(), name='roots_login'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^protected/', include('downloads.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns('',
    # Examples:
    # url(r'^$', 'roots.views.home', name='home'),
    # url(r'^roots/', include('roots.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', IndexView.as_view(), name='roots_index'),
    url(_(r'^admin/filebrowser/'), include(site.urls)),
    url(_(r'^admin/doc/'), include('django.contrib.admindocs.urls')),
    url(_(r'^admin/'), include(admin.site.urls)),
    url(_(r'^grappelli/'), include('grappelli.urls')),
    url(_(r'^accounts/'), include('allauth.urls')),
    url(_(r'^avatar/'), include('avatar.urls')),
    url(_(r'^accounts/profile/'), TemplateView.as_view(
                               template_name='profile.html'),
                               name='roots_profile'),
    url(_(r'^competitions/'), include('competitions.urls')),
    url(_(r'^comments/'), include('fluent_comments.urls')),
    url(_(r'^events/'), include('events.urls')),
    url(_(r'^leaflets/'), include('leaflets.urls')),
    url(_(r'^problems/'), include('problems.urls')),
    url(_(r'^posts/'), include('posts.urls')),
    url(_(r'^photos/'), include('photos.urls')),
    url(_(r'^photos/'), include('photologue.urls')),
    url(_(r'^profiles/'), include('profiles.urls')),
    url(_(r'^schools/'), include('schools.urls')),
    url(_(r'^protected/'), include('downloads.urls'))
)

# Add django-wiki related patterns
urlpatterns += i18n_patterns('',
    (_(r'^wiki/notify/'), get_notify_pattern()),
    (_(r'^wiki/'), get_wiki_pattern()),
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += i18n_patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
