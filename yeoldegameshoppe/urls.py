from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import (login, logout_then_login,
                                       password_reset, password_reset_done,
                                       password_change, password_change_done,
                                       password_reset_confirm,
                                       password_reset_complete)
from django.views.generic import RedirectView


import yogsauth.views
import yogsgame.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # By default go to the profile page for now
    url(r'^$', RedirectView.as_view(pattern_name='profile', permanent=False)),

    # yogsauth
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', login, {'template_name': 'login.djhtml'},
        name='login'),
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^password_change/$', password_change, name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        name='password_change_done'),
    url(r'^password_reset$', password_reset,
        {'template_name': 'password_reset.djhtml'}, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done,
        name='password_reset_done'),
    url((r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/' +
         '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'),
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete,
        name='password_reset_complete'),
    url(r'^activate/(?P<user_id>\d+)/(?P<activation_key>.+)$',
        yogsauth.views.activate, name='activate'),
    url(r'^send_activation_email', yogsauth.views.send_activation_email,
        name='send_activation_email'),
    url(r'^profile/$', yogsauth.views.profile, name='profile'),
    url(r'^register$', yogsauth.views.register, name='register'),

    # yogsgame
    url(r'^game/(?P<game_id>\d+)$', yogsgame.views.game,
        name='game'),
    url(r'^game/(?P<game_id>\d+)/buy$', yogsgame.views.buy_game,
        name='buy_game'),

    # admin
    url(r'^admin/', include(admin.site.urls))
)
