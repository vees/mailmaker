from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Example:
    (r'html/$', 'potluck.views.complaints_html'),
    (r'csv/$', 'potluck.views.complaints_csv'),
    (r'complaints/$', 'potluck.views.complaints'),
    (r'properties/$', 'potluck.views.properties'),
    (r'public/(?P<report_id>\d+)$', 'potluck.views.public'),
    (r'private/(?P<report_id>\d+)$', 'potluck.views.private'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
)
