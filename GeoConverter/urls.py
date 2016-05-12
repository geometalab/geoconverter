from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'GeoConverter.views.home', name='home'),
                       # url(r'^GeoConverter/', include('GeoConverter.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^$', 'OGRgeoConverter.views.show_main_page'),

                       # All urls starting with "converter" are handled by the following URL dispatcher
                       url(r'^converter/', include('OGRgeoConverter.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       )

# if DEBUG is True it will be served automatically
if settings.DEBUG is False:
    urlpatterns += patterns('',
                            url(r'^' + settings.STATIC_URL[1:] + r'(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}),
                            )
