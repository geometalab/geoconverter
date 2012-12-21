'''
Handles files, folders and paths.
'''

import os
import shutil
from datetime import datetime
from datetime import date
from OGRgeoConverter import paths
from OGRgeoConverter.filesystem import pathcode

def store_uploaded_file(path_code, file_data, file_name):
    '''
    Takes file data as argument and stores it in the path specified by path_code and file_name
    '''
    upload_folder_path = get_upload_folder_path(path_code)
    upload_file_path = os.path.join(upload_folder_path, file_name)
    
    with open(upload_file_path, 'wb+') as destination:
        for chunk in file_data.chunks():
            destination.write(chunk)

def get_empty_job_folder():
    '''
    Returns a unique random pathcode and creates folders belonging to the pathocde.
    '''
    i = 0
    while i < 100:
        path_code = pathcode.get_random_pathcode()
        full_path = get_folder_path(path_code)
        i += 1
        if not os.path.exists(get_folder_path(path_code)):
            os.makedirs(full_path)
            break
    
    os.makedirs(get_upload_folder_path(path_code))
    os.makedirs(get_extract_folder_path(path_code))
    os.makedirs(get_output_folder_path(path_code))
    os.makedirs(get_download_folder_path(path_code))

    return path_code

def remove_old_folders():
    folder_path = get_conversion_job_folder()
    
    today = datetime.now().date()
    
    for folder in os.listdir(folder_path):
        parts = folder.split('_')
        if len(parts) == 3:
            folder_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
            difference = today - folder_date
            if difference.days > 5:
                full_path = os.path.join(folder_path, folder)
                shutil.rmtree(full_path)
                

def get_conversion_job_folder():
    return paths.conversion_job_path()

def get_folder_path(path_code):
    '''
    Returns the root job folder belonging to a pathcode
    '''
    year, month, day, hour, minute, second, code = pathcode.split_pathcode(path_code)
    
    folder_path = get_conversion_job_folder()
    folder_path = os.path.join(folder_path, year + '_' + month + '_' + day)
    folder_path = os.path.join(folder_path, hour + '_' + minute + '_' + code)
    
    return folder_path
    
def get_upload_folder_path(path_code):
    '''
    Returns the folder where uploads are stored (depending on pathcode)
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '1_upload')
    return folder_path

def get_extract_folder_path(path_code):
    '''
    Returns the folder where files from archives are extracted to (depending on pathcode)
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '2_extract')
    return folder_path

def get_output_folder_path(path_code):
    '''
    Returns the folder where converted files are stored (depending on pathcode)
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '3_output')
    return folder_path

def get_download_folder_path(path_code):
    '''
    Returns the folder where the download file is stored (depending on pathcode)
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '4_download')
    return folder_path
    
def get_download_file_path(path_code):
    '''
    Returns the file path of the final archive with the converted files (depending on pathcode)
    '''
    year, month, day, hour, minute, second, code = pathcode.split_pathcode(path_code)
    
    file_path = get_download_folder_path(path_code)
    file_path = os.path.join(file_path, year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second + '-geoconverter-ch.zip')
    return file_path
        