'''
Functions being called when the user enters a specific URL.
URL-Function mapping is defined in urls.py.
'''

import json
import time
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from OGRgeoConverter.forms import GeoConverterFilesForm, GeoConverterWebservicesForm
from OGRgeoConverter.jobs import jobidentification
from OGRgeoConverter.jobs import jobhandler
from OGRgeoConverter.geoconverter import downloadhandler
from OGRgeoConverter.geoconverter.downloadhandler import DownloadHandler
from OGRgeoConverter.geoconverter.loghandler import LogHandler
from OGRgeoConverter.geoconverter import sessionhandler
from OGRgeoConverter.filesystem import filemanager


def redirect_to_main_page(request):
    return HttpResponseRedirect(reverse('OGRgeoConverter.views.show_main_page'))

def show_main_page(request):
    if not sessionhandler.is_valid_key(request.session.session_key):
        request.session.flush()
    
    files_form = GeoConverterFilesForm(request.POST, request.FILES)
    
    if 'urlinput' in request.POST:
        webservices_form = GeoConverterWebservicesForm(request.POST, request.POST['urlinput'])
    else:
        webservices_form = GeoConverterWebservicesForm()
    
    download_list = downloadhandler.get_download_items(request.session.session_key)

    return render(request, 'ogr-geo-converter.html', {'files_form': files_form, 'webservices_form': webservices_form, 'download_list': download_list})
    
        
def start_conversion_job(request, client_job_token):
    if request.method == 'POST':
        # Read POST values
        POST_dict = request.POST.dict()
        export_format = POST_dict['export_format'].strip()
        del POST_dict['export_format']
        source_srs = POST_dict['source_srs'].strip()
        del POST_dict['source_srs']
        target_srs = POST_dict['target_srs'].strip()
        del POST_dict['target_srs']
        simplify_parameter = POST_dict['simplify_parameter'].strip()
        del POST_dict['simplify_parameter']
        download_name = POST_dict['download_name'].strip()
        del POST_dict['download_name']
        if len(download_name) > 10: download_name = download_name[0:7] + '...'
        
        session_key = request.session.session_key
        job_identifier = jobidentification.get_new_job_identifier_by_client_job_token(session_key, client_job_token)
        job_id = job_identifier.job_id
        if job_id == '':
            return HttpResponseServerError('Error: Job Token is not valid.')
        
        log_handler = LogHandler(job_identifier)
        download_handler = DownloadHandler(job_identifier)
        
        jobhandler._initialize_job(session_key, client_job_token, job_id)
        
        jobhandler.add_file_names(session_key, client_job_token, POST_dict)
        jobhandler.set_export_format(session_key, client_job_token, export_format)
        jobhandler.set_srs(session_key, client_job_token, source_srs, target_srs)
        jobhandler.set_simplify_parameter(session_key, client_job_token, simplify_parameter)
        
        job_id = jobhandler.get_path_code(session_key, client_job_token)
        download_handler.set_download_caption(download_name)
        
        log_handler.set_start_time()
        log_handler.set_input_type('files')
        log_handler.set_export_format(export_format)
        log_handler.set_source_srs(source_srs)
        log_handler.set_target_srs(target_srs)
        log_handler.set_simplify_parameter(simplify_parameter)
        
        return HttpResponse('success')
    else:
        return redirect_to_main_page(request)
    
@csrf_exempt
def process_upload(request, job_id):
    file_name = request.GET['qqfile']
    file_id = request.GET['qqfileid']
    file_data = SimpleUploadedFile(request.GET['qqfile'], request.raw_post_data)
    
    jobhandler.store_file(request.session.session_key, job_id, file_id, file_data)
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Temporary deactivated because of race condition !!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    jobhandler.process_file(request.session.session_key, job_id, file_id)
    
    response_data = {}
    response_data['success'] = True
    
    # mimetype should be "application/json" but than IE offers the response as download...
    return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
def remove_file(request, job_id, file_id):
    if request.method == 'POST':
        jobhandler.remove_file(request.session.session_key, job_id, file_id)
        return HttpResponse('success')
    else:
        return redirect_to_main_page(request)
        
def finish_conversion_job(request, client_job_token):
    if request.method == 'POST':
        session_key = request.session.session_key
        
        jobhandler.convert_unprocessed_files(session_key, client_job_token)
        
        jobhandler.create_download_file(session_key, client_job_token)
        
        job_id = jobhandler.get_path_code(session_key, client_job_token)
        job_identifier = jobidentification.get_job_identifier_by_job_id(session_key, job_id)
        
        log_handler = LogHandler(job_identifier)
        download_handler = DownloadHandler(job_identifier)
        
        download_handler.add_download_item()
        
        log_handler.set_end_time()
        log_handler.set_download_file_size(download_handler.get_download_file_size()/1024)
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['job_id'] = job_id
        response_data['successful'] = download_handler.download_file_exists()
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
        # if count files == 0 response job canceled
    return HttpResponse('success')

def download_output_file(request, *job_id_args):
    session_key = request.session.session_key
    job_id = jobidentification.join_job_id(*job_id_args)
    job_identifier = jobidentification.get_job_identifier_by_job_id(session_key, job_id)
    
    download_handler = DownloadHandler(job_identifier)
    
    download_file_information = download_handler.get_download_file_information()
    
    if download_file_information != None:
        file, file_name, file_size = download_file_information
        
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['Content-Length'] = file_size
        
        download_handler.set_is_downloaded()
        
        return response
    else:
        return HttpResponseServerError('Error: file does not exist!')

def remove_download_item(request, *job_id_args):
    #_initialize_session(request)
    
    job_id = jobidentification.join_job_id(*job_id_args)
    
    if job_id != '':
        job_identifier = jobidentification.get_job_identifier_by_job_id(request.session.session_key, job_id)
        if job_identifier != None:
            download_handler = DownloadHandler(job_identifier)
            download_handler.remove_download_item()
            return HttpResponse('Item removed')
        else:
            print 'job_identifier = None'
    else:
        print "job_id = ''"
    
    return HttpResponseServerError('Error removing file')

def convert_webservice(request, client_job_token):
    if request.method == 'POST':
        POST_dict = request.POST.dict()
        webservice_url = POST_dict['webservice_url'].strip()
        export_format = POST_dict['export_format'].strip()
        source_srs = POST_dict['source_srs'].strip()
        target_srs = POST_dict['target_srs'].strip()
        simplify_parameter = POST_dict['simplify_parameter'].strip()
        download_name = POST_dict['download_name'].strip()
        if len(download_name) > 10: download_name = download_name[0:7] + '...'
        
        session_key = request.session.session_key
        job_identifier = jobidentification.get_new_job_identifier_by_client_job_token(session_key, client_job_token)
        job_id = job_identifier.job_id
        if job_id == '':
            return HttpResponseServerError('Error: Job Token is not valid.')
        
        log_handler = LogHandler(job_identifier)
        download_handler = DownloadHandler(job_identifier)
        
        jobhandler._initialize_job(session_key, client_job_token, job_id)
        
        jobhandler.add_webservice_url(session_key, client_job_token, webservice_url)
        jobhandler.set_export_format(session_key, client_job_token, export_format)
        jobhandler.set_srs(session_key, client_job_token, source_srs, target_srs)
        jobhandler.set_simplify_parameter(session_key, client_job_token, simplify_parameter)
        
        job_id = jobhandler.get_path_code(session_key, client_job_token)
        
        # Log start
        
        log_handler.set_start_time()
        log_handler.set_input_type('webservice')
        log_handler.set_export_format(export_format)
        log_handler.set_source_srs(source_srs)
        log_handler.set_target_srs(target_srs)
        log_handler.set_simplify_parameter(simplify_parameter)
        
        # Conversion start
        
        jobhandler.process_webservice_urls(session_key, client_job_token)
        
        jobhandler.create_download_file(session_key, client_job_token)
        
        download_handler.add_download_item()
        download_handler.set_download_caption(download_name)
        
        # Conversion end
        
        log_handler.set_end_time()
        log_handler.set_download_file_size(download_handler.get_download_file_size()/1024)
        
        # Log end
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['job_id'] = job_id
        response_data['successful'] = download_handler.download_file_exists()
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
    return HttpResponseServerError('Error: Request not valid.')
