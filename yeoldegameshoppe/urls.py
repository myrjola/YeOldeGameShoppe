from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from django.views.generic import RedirectView


import yogsauth.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # By default go to login page for now
    url(r'^$', RedirectView.as_view(pattern_name='login', permanent=False)),

    # yogsauth
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login$', login, {'template_name': 'login.djhtml'},
        name='login'),
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^profile/$', yogsauth.views.profile, name='profile'),
    url(r'^register$', yogsauth.views.register, name='register'),
    url(r'^activate/(?P<user_id>\d+)/(?P<activation_key>.+)$',
        yogsauth.views.activate, name='activate'),

    # admin
    url(r'^admin/', include(admin.site.urls))
)
