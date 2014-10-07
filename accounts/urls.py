from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('accounts.views',
    url(r'^accounts/home/$', 'home',name='home'),
    url(r'^accounts/login/$', 'login'),
    url(r'^accounts/logout/$', 'logout'),
)
