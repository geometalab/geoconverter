'''
Stores and returns download items
'''

import os
from django.core.servers.basehttp import FileWrapper
from OGRgeoConverter.filesystem import filemanager, pathcode
from OGRgeoConverter.geoconverter import datetimehandler
from OGRgeoConverter.models import DownloadItem

def _get_download_item_query_set(session_key, job_id):
    download_items = DownloadItem.get_download_item(session_key, job_id)
    if len(download_items) == 0:
        # Creat download item if it doesen't exist yet
        download_item = DownloadItem()
        download_item.session_key = session_key
        download_item.job_id = job_id
        download_item.creation_time = datetimehandler.get_default_datetime()
        download_item.save()
        download_items = DownloadItem.get_download_item(session_key, job_id)
    
    return download_items

def get_download_items(session_key):
    download_items = DownloadItem.get_download_items(session_key)
        
    download_item_list = []
    for download_item in download_items:
        job_id = download_item.job_id
        download_caption = get_download_caption(session_key, download_item.job_id)
        exists = filemanager.download_file_exists(job_id)
        download_item_list.append((job_id, download_caption, exists))
        
    return download_item_list

def add_download_item(session_key, job_id):
    download_item = _get_download_item_query_set(session_key, job_id)
    download_item.update(creation_time=datetimehandler.get_now())
    
def set_download_caption(session_key, job_id, download_caption):
    download_item = _get_download_item_query_set(session_key, job_id)
    download_item.update(download_caption=download_caption)
    
def get_download_caption(session_key, job_id):
    download_item = _get_download_item_query_set(session_key, job_id)
    return download_item[0].download_caption

def remove_download_item(session_key, job_id):
    download_item = _get_download_item_query_set(session_key, job_id)
    download_item.delete()

def get_download_file_information(*path_code_args):
    '''
    Returns a download file in a wrapper and its name and size
    '''
    path_code = pathcode.join_pathcode(*path_code_args)
    file_path = filemanager.get_download_file_path(path_code)
    
    if filemanager.download_file_exists(path_code):
        wrapper = FileWrapper(file(file_path, 'rb'))
        file_name = os.path.split(file_path)[1]
        file_size = os.path.getsize(file_path)
        return wrapper, file_name, file_size
    else:
        return None
    
def get_download_file_size(job_id):
    file_path = filemanager.get_download_file_path(job_id)
    
    if filemanager.download_file_exists(job_id):
        return os.path.getsize(file_path)
    else:
        return -1
    
def download_file_exists(job_id):
    return filemanager.download_file_exists(job_id)