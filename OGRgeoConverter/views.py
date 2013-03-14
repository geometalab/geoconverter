'''
Functions being called when the user enters a specific URL.
URL-Function mapping is defined in urls.py.
'''

import json
import time
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from OGRgeoConverter.forms import GeoConverterFilesForm, GeoConverterWebservicesForm
from OGRgeoConverter.filesystem import pathcode
from OGRgeoConverter.geoconverter import jobhandler
from OGRgeoConverter.geoconverter import downloadhandler
from OGRgeoConverter.geoconverter import loghandler
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
    
        
def start_conversion_job(request, job_id):
    if request.method == 'POST':
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
        
        jobhandler.add_file_names(session_key, job_id, POST_dict)
        jobhandler.set_export_format(session_key, job_id, export_format)
        jobhandler.set_srs(session_key, job_id, source_srs, target_srs)
        jobhandler.set_simplify_parameter(session_key, job_id, simplify_parameter)
        
        path_code = jobhandler.get_path_code(session_key, job_id)
        downloadhandler.set_download_name(session_key, path_code, download_name)
        
        loghandler.create_log_entry(session_key, path_code)
        lt = time.localtime()
        loghandler.set_start_time(session_key, path_code, time.strftime('%Y-%m-%d %H:%M:%S', lt))
        loghandler.set_input_type(session_key, path_code, 'files')
        loghandler.set_export_format(session_key, path_code, export_format)
        loghandler.set_srs(session_key, path_code, source_srs, target_srs)
        loghandler.set_simplify_parameter(session_key, path_code, simplify_parameter)
        
        return HttpResponse('success')
    else:
        return redirect_to_main_page(request)
    
@csrf_exempt
def process_upload(request, job_id):
    file_name = request.GET['qqfile']
    file_id = request.GET['qqfileid']
    file_data = SimpleUploadedFile(request.GET['qqfile'], request.raw_post_data)
    
    jobhandler.store_file(request.session.session_key, job_id, file_id, file_data)
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
        
def finish_conversion_job(request, job_id):
    if request.method == 'POST':
        session_key = request.session.session_key
        
        jobhandler.create_download_file(session_key, job_id)
        
        path_code = jobhandler.get_path_code(session_key, job_id)
        
        downloadhandler.store_download_item(session_key, path_code)
        
        lt = time.localtime()
        loghandler.set_end_time(session_key, path_code, time.strftime('%Y-%m-%d %H:%M:%S', lt))
        loghandler.set_download_file_size(session_key, path_code, downloadhandler.get_download_file_size(path_code)/1024)
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['path_code'] = path_code
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
        # if count files == 0 response job canceled
    return HttpResponse('success')

def download_output_file(request, *path_code_args):
    file, file_name, file_size = downloadhandler.get_download_file_information(*path_code_args)
    
    response = HttpResponse(file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    response['Content-Length'] = file_size
    
    return response

def remove_download_item(request, *path_code_args):
    #_initialize_session(request)
    
    path_code = pathcode.join_pathcode(*path_code_args)
    
    if path_code != '':
        downloadhandler.remove_download_item(request.session.session_key, path_code)
        return HttpResponse('success')
    
    return HttpResponse('fail')

def convert_webservice(request, job_id):
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
        jobhandler.add_webservice_url(session_key, job_id, webservice_url)
        jobhandler.set_export_format(session_key, job_id, export_format)
        jobhandler.set_srs(session_key, job_id, source_srs, target_srs)
        jobhandler.set_simplify_parameter(session_key, job_id, simplify_parameter)
        
        path_code = jobhandler.get_path_code(session_key, job_id)
        
        # Log start
        
        loghandler.create_log_entry(session_key, path_code)
        lt = time.localtime()
        loghandler.set_start_time(session_key, path_code, time.strftime('%Y-%m-%d %H:%M:%S', lt))
        loghandler.set_input_type(session_key, path_code, 'webservice')
        loghandler.set_export_format(session_key, path_code, export_format)
        loghandler.set_srs(session_key, path_code, source_srs, target_srs)
        loghandler.set_simplify_parameter(session_key, path_code, simplify_parameter)
        
        # Conversion start
        
        jobhandler.process_webservice_urls(session_key, job_id)
        
        jobhandler.create_download_file(session_key, job_id)
        
        downloadhandler.store_download_item(session_key, path_code)
        downloadhandler.set_download_name(session_key, path_code, download_name)
        
        # Conversion end
        
        lt = time.localtime()
        loghandler.set_end_time(session_key, path_code, time.strftime('%Y-%m-%d %H:%M:%S', lt))
        loghandler.set_download_file_size(session_key, path_code, downloadhandler.get_download_file_size(path_code)/1024)
        
        # Log end
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['path_code'] = path_code
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
    return HttpResponse('fail')
