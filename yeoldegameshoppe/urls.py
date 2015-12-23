from django.conf.urls import patterns, include, url
from django.contrib import admin

import yogsauth.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # By default go to login page for now
    url(r'^$', yogsauth.views.auth_login),

    # yogsauth
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login$', yogsauth.views.auth_login, name='login'),
    url(r'^logout$', yogsauth.views.auth_logout, name='logout'),
    url(r'^profile/$', yogsauth.views.profile, name='profile'),
    url(r'^register$', yogsauth.views.register, name='register'),
    url(r'^activate/(?P<user_id>\d+)/(?P<activation_key>.+)$', yogsauth.views.activate,
        name='activate'),

    # admin
    url(r'^admin/', include(admin.site.urls))
)
