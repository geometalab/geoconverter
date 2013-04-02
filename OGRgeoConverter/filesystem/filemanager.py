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

def rename_file(folder_path, old_file_name, new_file_name):
    old_file_path = os.path.join(folder_path, old_file_name)
    new_file_path = os.path.join(folder_path, new_file_name)
    os.rename(old_file_path, new_file_path)

def get_empty_job_folder():
    '''
    Returns a unique random pathcode and creates the folders belonging to the pathocde.
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
    '''
    Cleans up conversion folders older than 5 days
    '''
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
                
def get_file_count(folder_path):
    file_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
    
    print 'File count: ' + str(file_count)
    return file_count

def get_conversion_job_folder():
    '''
    Returns the folder containing the job folders
    /OGRgeoConverter/ConversionJobs/
    '''
    return paths.conversion_job_path()

def get_folder_path(path_code):
    '''
    Returns the root job folder belonging to a pathcode
    e.g. /OGRgeoConverter/ConversionJobs/2012_12_12/
    '''
    year, month, day, hour, minute, second, code = pathcode.split_pathcode(path_code)
    
    folder_path = get_conversion_job_folder()
    folder_path = os.path.join(folder_path, year + '_' + month + '_' + day)
    folder_path = os.path.join(folder_path, hour + '_' + minute + '_' + code)
    
    return folder_path
    
def get_upload_folder_path(path_code):
    '''
    Returns the folder where uploads are stored (depending on pathcode)
    e.g. /OGRgeoConverter/ConversionJobs/2012_12_12/1_upload/
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '1_upload')
    return folder_path

def get_extract_folder_path(path_code):
    '''
    Returns the folder where files from archives are extracted to (depending on pathcode)
    e.g. /OGRgeoConverter/ConversionJobs/2012_12_12/2_extract/
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '2_extract')
    return folder_path

def get_output_folder_path(path_code):
    '''
    Returns the folder where converted files are stored (depending on pathcode)
    e.g. /OGRgeoConverter/ConversionJobs/2012_12_12/3_output/
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '3_output')
    return folder_path

def get_download_folder_path(path_code):
    '''
    Returns the folder where the download file is stored (depending on pathcode)
    e.g. /OGRgeoConverter/ConversionJobs/2012_12_12/4_download/
    '''
    folder_path = get_folder_path(path_code)
    folder_path = os.path.join(folder_path, '4_download')
    return folder_path
    
def get_download_file_path(path_code):
    '''
    Returns the file path of the final archive with the converted files (depending on pathcode)
    e.g. /OGRgeoConverter/ConversionJobs/2012_12_12/4_download/geoconverter_20121212_151500.zip
    '''
    year, month, day, hour, minute, second, code = pathcode.split_pathcode(path_code)
    
    file_path = get_download_folder_path(path_code)
    file_path = os.path.join(file_path, 'geoconverter' + '_' + year  + month + day + '_' + hour + minute + second + '.zip')
    return file_path

def download_file_exists(path_code):
    download_file_path = get_download_file_path(path_code)
    return os.path.exists(download_file_path)