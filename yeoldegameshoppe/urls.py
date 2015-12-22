from django.conf.urls import patterns, include, url

from django.contrib import admin

import yogsauth.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'yeoldegameshoppe.views.home', name='home')
    # url(r'^blog/', include('blog.urls'))

    # yogsauth
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login$', yogsauth.views.auth_login, name='login'),
    url(r'^logout$', yogsauth.views.auth_login, name='logout'),
    url(r'^accounts/profile/$', yogsauth.views.profile, name='profile'),

    # admin
    url(r'^admin/', include(admin.site.urls))
)
