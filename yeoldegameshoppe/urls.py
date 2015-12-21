from django.conf.urls import patterns, include, url

from django.contrib import admin

import hello.views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'yeoldegameshoppe.views.home', name='home')
                       # url(r'^blog/', include('blog.urls'))

                       url(r'^$', hello.views.index, name='index'),
                       url(r'^db', hello.views.db, name='db'),
                       url(r'^admin/', include(admin.site.urls)))
