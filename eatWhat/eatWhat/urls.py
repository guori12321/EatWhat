from django.conf.urls.defaults import *
from eatWhat.views import hello,current_datetime
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	('^hello/$',hello),
	('^time/$',current_datetime),
	(r'^time/plus/(\d{1,2})/$',hour_ahead),
    # Examples:
    # url(r'^$', 'eatWhat.views.home', name='home'),
    # url(r'^eatWhat/', include('eatWhat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
