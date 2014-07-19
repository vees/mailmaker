from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:

    (r'^api/complaints/html/$', 'harfordpark.potluck.views.complaints_html'),
    (r'^api/csv/$', 'harfordpark.potluck.views.complaints_csv'),
    (r'^api/complaints/$', 'harfordpark.potluck.views.complaints'),
    (r'^api/properties/$', 'harfordpark.potluck.views.properties'),
    (r'^public/(?P<report_id>\d+)$', 'harfordpark.potluck.views.public'),
    (r'^private/(?P<report_id>\d+)$', 'harfordpark.potluck.views.private'),
    (r'^$', 'harfordpark.potluck.views.index'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
