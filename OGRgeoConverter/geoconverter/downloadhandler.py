import os
from django.core.servers.basehttp import FileWrapper
from OGRgeoConverter.filesystem import filemanager
#from OGRgeoConverter.jobs import jobidentification
#from OGRgeoConverter.geoconverter import datetimehandler
from OGRgeoConverter.models import DownloadItem


def get_download_items(session_key):
    download_items = DownloadItem.get_download_items(session_key)
    
    download_item_list = []
    for download_item in download_items:
        job_identifier = download_item.job_identifier
        job_id = job_identifier.job_id
        download_caption = download_item.download_caption
        exists = filemanager.download_file_exists(job_identifier.job_id)
        is_downloaded = download_item.is_downloaded
        download_item_list.append((job_id, download_caption, exists, is_downloaded))
        
    return download_item_list


class DownloadHandler:
    '''
    Class handling download items
    '''
    
    def __init__(self, job_identifier):
        if job_identifier != None:
            self.__job_identifier = job_identifier
        else:
            raise Exception("job_identifier may not be None")
        
    def __get_download_item_query_set(self):
        download_items = DownloadItem.get_download_item(self.__job_identifier)
        if len(download_items) == 0:
            # Creat download item if it doesen't exist yet
            download_item = DownloadItem()
            download_item.job_identifier = self.__job_identifier
            download_item.download_caption = ''
            download_item.is_downloaded = False
            download_item.save()
            
            download_items = DownloadItem.get_download_item(self.__job_identifier)
        
        return download_items
    
    def add_download_item(self):
        download_item = self.__get_download_item_query_set()
        return download_item
        
    def set_download_caption(self, download_caption):
        download_item = self.__get_download_item_query_set()
        download_item.update(download_caption=download_caption)
        
    def get_download_caption(self):
        download_item = self.__get_download_item_query_set()
        return download_item[0].download_caption
    
    def set_is_downloaded(self):
        download_item = self.__get_download_item_query_set()
        download_item.update(is_downloaded=True)
    
    def get_is_downloaded(self):
        download_item = self.__get_download_item_query_set()
        return download_item[0].is_downloaded
    
    def remove_download_item(self):
        download_item = self.__get_download_item_query_set()
        download_item.delete()
    
    def get_download_file_information(self):
        '''
        Returns a download file in a wrapper and its name and size
        '''
        
        file_path = filemanager.get_download_file_path(self.__job_identifier.job_id)
        
        if self.download_file_exists():
            wrapper = FileWrapper(open(file_path, 'rb'))
            file_name = os.path.split(file_path)[1]
            file_size = os.path.getsize(file_path)
            return wrapper, file_name, file_size
        else:
            return None
        
    def get_download_file_size(self):
        file_path = filemanager.get_download_file_path(self.__job_identifier.job_id)
        
        if self.download_file_exists():
            return os.path.getsize(file_path)
        else:
            return -1
        
    def download_file_exists(self):
        return filemanager.download_file_exists(self.__job_identifier.job_id)