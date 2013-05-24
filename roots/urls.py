from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'roots.views.home', name='home'),
    # url(r'^roots/', include('roots.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', direct_to_template,
            {'template': 'profile.html'}),
    url(r'^problems/', include('problems.urls')),
)
