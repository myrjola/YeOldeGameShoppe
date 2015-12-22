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
    url(r'^$', yogsauth.views.login, name='login'),
    url(r'^fb$', yogsauth.views.facebook, name='facebook'),

    # admin
    url(r'^admin/', include(admin.site.urls))
)
