'''
Stores and returns download items
'''

import os
from django.core.servers.basehttp import FileWrapper
from OGRgeoConverter.filesystem import filemanager, pathcode
from OGRgeoConverter.geoconverter import sessionhandler

def store_download_item(session_key, path_code):
    session = sessionhandler.get_session(session_key)
    if not 'download_items' in session:
        session['download_items'] = []
    session['download_items'].insert(0, path_code)
    session.save()
    
def set_download_name(session_key, path_code, download_name):
    session = sessionhandler.get_session(session_key)
    if not 'download_names' in session:
        session['download_names'] = {}
    session['download_names'][path_code] = download_name
    session.save()
    
def get_download_name(session_key, path_code):
    session = sessionhandler.get_session(session_key)
    if not 'download_names' in session:
        session['download_names'] = {}
    if path_code in session['download_names']:
        return session['download_names'][path_code]
    else:
        return ''

def remove_download_item(session_key, path_code):
    session = sessionhandler.get_session(session_key)
    if not 'download_items' in session:
        session['download_items'] = []
    if path_code in session['download_items']:
        session['download_items'].remove(path_code)
    session.save()

def get_download_items(session_key):
    session = sessionhandler.get_session(session_key)
    if not 'download_items' in session:
        session['download_items'] = []
        
    download_items = []
    for download_item in session['download_items']:
        download_items.append((download_item, get_download_name(session_key, download_item)))
        
    return download_items

def get_download_file_information(*path_code_args):
    '''
    Returns a download file in a wrapper and its name and size
    '''
    path_code = pathcode.join_pathcode(*path_code_args)
    file_path = filemanager.get_download_file_path(path_code)
    
    if file_path != '':
        wrapper = FileWrapper(file(file_path, 'rb'))
        file_name = os.path.split(file_path)[1]
        file_size = os.path.getsize(file_path)
        return wrapper, file_name, file_size
    else:
        return None
    
def get_download_file_size(path_code):
    file_path = filemanager.get_download_file_path(path_code)
    
    if file_path != '':
        return os.path.getsize(file_path)
    else:
        return -1