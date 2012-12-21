'''
Functions being called when the user enters a specific URL.
URL-Function mapping is defined in urls.py.
'''

import json
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
from OGRgeoConverter.geoconverter import sessionhandler
from OGRgeoConverter.filesystem import filemanager


def redirect_to_main_page(request):
    return HttpResponseRedirect(reverse('OGRgeoConverter.views.show_main_page'))

def show_main_page(request):
    if not sessionhandler.is_valid_key(request.session.session_key):
        request.session.flush()
    
    #s = SessionStore(session_key=request.session.session_key)
    #s.save()
    #if s.session_key != request.session.session_key:
    #    request.session.flush()
    
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
        
        jobhandler.add_file_names(request.session.session_key, job_id, POST_dict)
        jobhandler.set_export_format(request.session.session_key, job_id, export_format)
        jobhandler.set_srs(request.session.session_key, job_id, source_srs, target_srs)
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
    
    # mimetype should be "application/json" but than IE offers the response as dwonload...
    return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
def remove_file(request, job_id, file_id):
    if request.method == 'POST':
        jobhandler.remove_file(request.session.session_key, job_id, file_id)
        return HttpResponse('success')
    else:
        return redirect_to_main_page(request)
        
def finish_conversion_job(request, job_id):
    if request.method == 'POST':
        jobhandler.create_download_file(request.session.session_key, job_id)
        
        path_code = jobhandler.get_path_code(request.session.session_key, job_id)
        
        downloadhandler.store_download_item(request.session.session_key, path_code)
        
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
    #path_code = pathcode.join_pathcode(*path_code_args)
    
    #if path_code != '':
    #    # http://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary
    #    del request.session['download_list'][path_code]
    #    request.session.modified = True
    #    return HttpResponse('success')
    
    #return HttpResponse('fail')

def convert_webservice(request, job_id):
    if request.method == 'POST':
        POST_dict = request.POST.dict()
        webservice_url = POST_dict['webservice_url'].strip()
        export_format = POST_dict['export_format'].strip()
        source_srs = POST_dict['source_srs'].strip()
        target_srs = POST_dict['target_srs'].strip()

        jobhandler.add_webservice_url(request.session.session_key, job_id, webservice_url)
        jobhandler.set_export_format(request.session.session_key, job_id, export_format)
        jobhandler.set_srs(request.session.session_key, job_id, source_srs, target_srs)
        
        jobhandler.process_webservice_urls(request.session.session_key, job_id)
        
        jobhandler.create_download_file(request.session.session_key, job_id)
        
        path_code = jobhandler.get_path_code(request.session.session_key, job_id)
        
        downloadhandler.store_download_item(request.session.session_key, path_code)
        
        filemanager.remove_old_folders()
        
        response_data = {}
        response_data['path_code'] = path_code
        return HttpResponse(json.dumps(response_data), mimetype="text/plain")
    
    return HttpResponse('fail')

"""
def process_form_submit(request):
    if request.method == 'POST':
        _initialize_session(request)
        files_form = GeoConverterFilesForm(request.POST, request.FILES)
        
        if 'urlinput' in request.POST:
            webservices_form = GeoConverterWebservicesForm(request.POST, request.POST['urlinput'])
        else:
            webservices_form = GeoConverterWebservicesForm()
        
        if files_form.is_valid():
            uploaded_file = request.FILES['fileupload']
            ogr_format_name = request.POST['ogrformat']
            
            path_code = geoconverter.process_convert_request(uploaded_file, ogr_format_name)

            # Reload session. Otherwise parallel requests will be lost!
            # This part is still not thread safe (parallel user requests) but erorrs are rare
            reloaded_session = SessionStore(session_key=request.session.session_key)
            reloaded_session['download_list'][path_code] = reverse('OGRgeoConverter.views.download_output_file', args=pathcode.split_pathcode(path_code))
            reloaded_session.save()
         
            response_data = {}
            response_data['path_code'] = path_code
            response_data['download_url'] = reverse('OGRgeoConverter.views.download_output_file', args=pathcode.split_pathcode(path_code))
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
            
        if webservices_form.is_valid():
            pass

    return HttpResponse('invalid')
"""
