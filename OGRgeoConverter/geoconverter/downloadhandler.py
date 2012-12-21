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
    session['download_items'].append(path_code)
    session.save()

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
    return session['download_items']

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