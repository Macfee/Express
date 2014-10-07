from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('logisticsNoManage.views',
    # Examples:
    # url(r'^$', 'Express.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^translate/$', 'translate'),
    url(r'^logisticsNo/$', 'logisticsNoManage'),
    url(r'^logisticsNo/apply/$', 'logisticsNoApply'),
    url(r'^logisticsNo/upload/$', 'logisticsNoUpload'),
    url(r'^$', 'index'),
    url(r'^billCalc/$', 'billCalc'),
    url(r'^batchNote/$', 'batchNote'),
)
