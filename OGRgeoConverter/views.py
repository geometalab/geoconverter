'''
Functions being called when the user enters a specific URL.
URL-Function mapping is defined in urls.py.
'''

import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf.global_settings import LANGUAGES
from django.utils import translation
from OGRgeoConverter.forms import GeoConverterFilesForm, GeoConverterWebservicesForm
from OGRgeoConverter.jobs import jobidentification
from OGRgeoConverter.jobs import jobprocessing
#
from OGRgeoConverter.models import OgrFormat
from OGRgeoConverter.models import GlobalOgrShellParameter
from OGRgeoConverter.geoconverter.filematching import FileMatcher
#
from OGRgeoConverter.modelhandlers import downloadhandler
from OGRgeoConverter.modelhandlers.jobhandler import JobHandler
from OGRgeoConverter.modelhandlers.downloadhandler import DownloadHandler
from OGRgeoConverter.modelhandlers.loghandler import LogHandler
from OGRgeoConverter.geoconverter import sessionhandler
from OGRgeoConverter.filesystem import filemanager


def redirect_to_main_page(request):
    return HttpResponseRedirect(reverse('OGRgeoConverter.views.show_main_page'))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_language(request):
    language_code = translation.get_language_from_request(request)
    for lang_code, lang_name in LANGUAGES:
        if lang_code == language_code:
            return lang_name
    return 'Unknown'

def get_client_user_agent(request):
    return request.META.get('HTTP_USER_AGENT')
    
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
        export_format_name = POST_dict['export_format'].strip()
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
        client_ip = get_client_ip(request)
        client_language = get_client_language(request)
        client_user_agent = get_client_user_agent(request)
        
        session_key = request.session.session_key
        job_identifier = jobidentification.get_new_job_identifier_by_client_job_token(session_key, client_job_token)
        job_id = job_identifier.job_id
        if job_id == '':
            return HttpResponseServerError('Error: Job Token is not valid.')
        
        job_handler = JobHandler(job_identifier)
        log_handler = LogHandler(job_identifier)
        download_handler = DownloadHandler(job_identifier)
        
        file_matcher = FileMatcher(POST_dict)
        for file_match in file_matcher.get_matches():
            job_handler.add_file_match(job_handler.get_upload_folder_path(), file_match.get_file_dict(), file_match.get_ogr_format_name(), file_match.is_archive(), file_match.is_valid())
        
        format_information = OgrFormat.get_format_information_by_name(export_format_name)
        if format_information != None:
            job_handler.set_export_format_name(format_information.ogr_name)
            for shell_parameter in format_information.additional_parameters:
                job_handler.add_shell_parameter(shell_parameter.prefix, shell_parameter.parameter_name, shell_parameter.parameter_value, shell_parameter.value_quotation_marks)
        
        for global_shell_parameter in GlobalOgrShellParameter.get_active_parameters():
            job_handler.add_shell_parameter_object(global_shell_parameter)
        
        job_handler.set_export_format_name(export_format_name)
        job_handler.set_source_srs(source_srs)
        job_handler.set_target_srs(target_srs)
        job_handler.set_simplify_parameter(simplify_parameter)
        
        #job_id = jobhandler.get_path_code(session_key, client_job_token)
        download_handler.set_download_caption(download_name)
        
        log_handler.set_start_time()
        log_handler.set_client_ip(client_ip)
        log_handler.set_client_language(client_language)
        log_handler.set_client_user_agent(client_user_agent)
        log_handler.set_input_type('files')
        log_handler.set_export_format_name(job_handler.get_export_format_name())
        log_handler.set_source_srs(job_handler.get_source_srs())
        log_handler.set_target_srs(job_handler.get_target_srs())
        log_handler.set_simplify_parameter(job_handler.get_simplify_parameter())
        
        jobprocessing.initialize_conversion_job(job_identifier)
        
        return HttpResponse('success')
    else:
        return redirect_to_main_page(request)
    
@csrf_exempt
def process_upload(request, client_job_token):
    #file_name = request.GET['qqfile']
    file_id = request.GET['qqfileid']
    file_data = SimpleUploadedFile(request.GET['qqfile'], request.body)
    
    job_identifier = jobidentification.get_job_identifier_by_client_job_token(request.session.session_key, client_job_token)
    
    jobprocessing.store_file(job_identifier, file_id, file_data)
    jobprocessing.process_file(job_identifier, file_id)
    
    response_data = {}
    response_data['success'] = True
    
    # mimetype should be "application/json" but than IE offers the response as download...
    return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
def remove_file(request, client_job_token, file_id):
    if request.method == 'POST':
        job_identifier = jobidentification.get_job_identifier_by_client_job_token(request.session.session_key, client_job_token)
        job_handler = JobHandler(job_identifier)
        job_handler.remove_file(file_id)
        return HttpResponse('success')
    else:
        return redirect_to_main_page(request)
        
def finish_conversion_job(request, client_job_token):
    if request.method == 'POST':
        job_identifier = jobidentification.get_job_identifier_by_client_job_token(request.session.session_key, client_job_token)
        
        #jobprocessing.convert_unprocessed_files(session_key, client_job_token)
        
        jobprocessing.create_download_file(job_identifier)
        
        log_handler = LogHandler(job_identifier)
        download_handler = DownloadHandler(job_identifier)
        
        download_handler.add_download_item()
        
        log_handler.set_end_time()
        log_handler.set_download_file_size(download_handler.get_download_file_size()/1024)
        log_handler.set_has_download_file(download_handler.download_file_exists())
        log_handler.set_all_files_converted()
        log_handler.set_has_no_error()
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['job_id'] = job_identifier.job_id
        response_data['successful'] = download_handler.download_file_exists()
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
        # if count files == 0 response job canceled
    return HttpResponse('success')

def download_output_file(request, *job_id_args):
    session_key = request.session.session_key
    job_id = jobidentification.join_job_id(*job_id_args)
    job_identifier = jobidentification.get_job_identifier_by_job_id(session_key, job_id)
    
    download_handler = DownloadHandler(job_identifier)
    log_hander = LogHandler(job_identifier)
    
    download_file_information = download_handler.get_download_file_information()
    
    if download_file_information != None:
        file, file_name, file_size = download_file_information
        
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['Content-Length'] = file_size
        
        download_handler.set_is_downloaded()
        log_hander.set_file_downloaded()
        
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
    
    return HttpResponseServerError('Error removing file')

def convert_webservice(request, client_job_token):
    if request.method == 'POST':
        POST_dict = request.POST.dict()
        webservice_url = POST_dict['webservice_url'].strip()
        export_format_name = POST_dict['export_format'].strip()
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
        
        job_handler = JobHandler(job_identifier)
        log_handler = LogHandler(job_identifier)
        download_handler = DownloadHandler(job_identifier)
        
        format_information = OgrFormat.get_format_information_by_name(export_format_name)
        if format_information != None:
            job_handler.set_export_format_name(format_information.ogr_name)
            for shell_parameter in format_information.additional_parameters:
                job_handler.add_shell_parameter(shell_parameter.prefix, shell_parameter.parameter_name, shell_parameter.parameter_value, shell_parameter.value_quotation_marks)
        
        for global_shell_parameter in GlobalOgrShellParameter.get_active_parameters():
            job_handler.add_shell_parameter_object(global_shell_parameter)
        
        job_handler.add_webservice_url('0', webservice_url)
        job_handler.set_export_format_name(export_format_name)
        job_handler.set_source_srs(source_srs)
        job_handler.set_target_srs(target_srs)
        job_handler.set_simplify_parameter(simplify_parameter)
        
        # Log start
        
        log_handler.set_start_time()
        log_handler.set_input_type('webservice')
        log_handler.set_export_format_name(job_handler.get_export_format_name())
        log_handler.set_source_srs(job_handler.get_source_srs())
        log_handler.set_target_srs(job_handler.get_target_srs())
        log_handler.set_simplify_parameter(job_handler.get_simplify_parameter())
        
        # Conversion start
        jobprocessing.initialize_conversion_job(job_identifier)
        jobprocessing.process_webservice_urls(job_identifier)
        
        jobprocessing.create_download_file(job_identifier)
        
        download_handler.add_download_item()
        download_handler.set_download_caption(download_name)
        
        # Conversion end
        
        log_handler.set_end_time()
        log_handler.set_download_file_size(download_handler.get_download_file_size()/1024)
        log_handler.set_has_download_file(download_handler.download_file_exists())
        log_handler.set_all_files_converted()
        log_handler.set_has_no_error()
        
        # Log end
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['job_id'] = job_id
        response_data['successful'] = download_handler.download_file_exists()
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
    return HttpResponseServerError('Error: Request not valid.')
