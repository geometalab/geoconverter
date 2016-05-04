'''
Extends main URL dispatcher in GeoConverter.urls
'''

from django.conf.urls import patterns, include, url
from OGRgeoConverter.jobs import jobidentification

urlpatterns = patterns('',
                       url(r'^$',
                           'OGRgeoConverter.views.show_main_page'),
                       url(r'^forms/files/(\w+)/start',
                           'OGRgeoConverter.views.start_conversion_job'),
                       url(r'^forms/files/(\w+)/upload',
                           'OGRgeoConverter.views.process_upload'),
                       url(r'^forms/files/(\w+)/remove/(\d+)',
                           'OGRgeoConverter.views.remove_file'),
                       url(r'^forms/files/(\w+)/finish',
                           'OGRgeoConverter.views.finish_conversion_job'),
                       url(r'^forms/webservices/(\w+)/convert',
                           'OGRgeoConverter.views.convert_webservice'),
                       url(r'^download/' + jobidentification.get_job_id_regex(),
                           'OGRgeoConverter.views.download_output_file'),
                       url(r'^remove/queue-' + jobidentification.get_job_id_regex(),
                           'OGRgeoConverter.views.remove_download_item'),
                       url(r'^remove/(\w+)',
                           'OGRgeoConverter.views.remove_download_item'))
