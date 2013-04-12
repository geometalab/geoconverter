'''
Stores and returns download items
'''

import os
from django.core.servers.basehttp import FileWrapper
from OGRgeoConverter.filesystem import filemanager
from OGRgeoConverter.jobs import jobidentification
from OGRgeoConverter.geoconverter import datetimehandler
from OGRgeoConverter.models import DownloadItem

def _get_download_item_query_set(job_identifier):
    download_items = DownloadItem.get_download_item(job_identifier)
    if len(download_items) == 0:
        # Creat download item if it doesen't exist yet
        download_item = DownloadItem()
        download_item.job_identifier = job_identifier
        download_item.download_caption = ''
        download_item.is_downloaded = False
        download_item.save()
        
        download_items = DownloadItem.get_download_item(job_identifier)
    
    return download_items

def get_download_items(session_key):
    download_items = DownloadItem.get_download_items(session_key)
        
    download_item_list = []
    for download_item in download_items:
        job_identifier = download_item.job_identifier
        job_id = job_identifier.job_id
        download_caption = download_item.download_caption
        exists = download_file_exists(job_identifier)
        is_downloaded = download_item.is_downloaded
        download_item_list.append((job_id, download_caption, exists, is_downloaded))
        
    return download_item_list

def add_download_item(job_identifier):
    download_item = _get_download_item_query_set(job_identifier)
    return download_item
    
def set_download_caption(job_identifier, download_caption):
    download_item = _get_download_item_query_set(job_identifier)
    download_item.update(download_caption=download_caption)
    
def get_download_caption(job_identifier):
    download_item = _get_download_item_query_set(job_identifier)
    return download_item[0].download_caption

def set_is_downloaded(job_identifier):
    download_item = _get_download_item_query_set(job_identifier)
    download_item.update(is_downloaded=True)

def get_is_downloaded(job_identifier):
    download_item = _get_download_item_query_set(job_identifier)
    return download_item[0].is_downloaded

def remove_download_item(job_identifier):
    download_item = _get_download_item_query_set(job_identifier)
    download_item.delete()

def get_download_file_information(job_identifier):
    '''
    Returns a download file in a wrapper and its name and size
    '''
    
    file_path = filemanager.get_download_file_path(job_identifier.job_id)
    
    if filemanager.download_file_exists(job_identifier.job_id):
        wrapper = FileWrapper(file(file_path, 'rb'))
        file_name = os.path.split(file_path)[1]
        file_size = os.path.getsize(file_path)
        return wrapper, file_name, file_size
    else:
        return None
    
def get_download_file_size(job_identifier):
    file_path = filemanager.get_download_file_path(job_identifier.job_id)
    
    if filemanager.download_file_exists(job_identifier.job_id):
        return os.path.getsize(file_path)
    else:
        return -1
    
def download_file_exists(job_identifier):
    return filemanager.download_file_exists(job_identifier.job_id)