'''
Functions to process conversion jobs.
'''

import os
from OGRgeoConverter.filesystem import filemanager, archives
from OGRgeoConverter.geoconverter import conversion
from OGRgeoConverter.geoconverter.filematching import FileMatcher
from OGRgeoConverter.modelhandlers.jobhandler import JobHandler

def initialize_conversion_job(job_identifier):
    filemanager.create_job_folders(job_identifier.job_id)
    upload_folder_path = filemanager.get_upload_folder_path(job_identifier.job_id)
    extract_folder_path = filemanager.get_extract_folder_path(job_identifier.job_id)
    output_folder_path = filemanager.get_output_folder_path(job_identifier.job_id)
    download_folder_path = filemanager.get_download_folder_path(job_identifier.job_id)
    
    job_handler = JobHandler(job_identifier)
    job_handler.set_upload_folder_path(upload_folder_path)
    job_handler.set_extract_folder_path(extract_folder_path)
    job_handler.set_output_folder_path(output_folder_path)
    job_handler.set_download_folder_path(download_folder_path)
    
def store_file(job_identifier, file_id, file_data):
    job_handler = JobHandler(job_identifier)
    if not job_handler.file_removed(file_id):
        file_name = job_handler.get_file_name(file_id)
        filemanager.store_uploaded_file(job_identifier.job_id, file_data, file_name)
        job_handler.set_file_uploaded(file_id)
    
def remove_file(job_identifier, job_id, file_id):
    job_handler = JobHandler(job_identifier)
    job_handler.remove_file(file_id)
    #...
        
def process_file(job_identifier, file_id):
    job_handler = JobHandler(job_identifier)
    if job_handler.file_ready_for_process(file_id) and job_handler.filematch_try_process(file_id):
        time.sleep(0.001)
        if job_handler.filematch_processing_id(file_id) != file_id:
            return # In this case two threads are processing the same file match => Race Condition!
        matched_files = job_handler.get_matched_files(file_id)
        for matched_file in matched_files:
            job_handler.set_file_processed(matched_file.file_id)
        
        source_path = job_handler.get_upload_folder_path()
        destination_path = job_handler.get_output_folder_path()
        export_format_name = job_handler.get_export_format_name()
        source_srs = job_handler.get_source_srs()
        target_srs = job_handler.get_target_srs()
        simplify_parameter = job_handler.get_simplify_parameter()
        additional_arguments = job_handler.get_shell_parameters()
        extract_base_path = job_handler.get_extract_folder_path()
        if matched_files[0].file_match.is_archive:
            file_name = matched_files[0].matched_file_name
            if job_handler.get_file_count() > 1:
                # Creates a sub folder in the extract folder
                extract_path = os.path.join(extract_base_path, os.path.splitext(file_name)[0])
            else:
                extract_path = extract_base_path
            process_archive(job_identifier, os.path.join(source_path, file_name), extract_base_path, extract_path, destination_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments, 1)
        else:
            conversion.convert_files(job_identifier, source_path, matched_files, destination_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments)
        
def process_archive(job_identifier, archive_path, unpack_base_path, unpack_path, output_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments, archive_depth=1):
    job_handler = JobHandler(job_identifier)
    
    # Allowed depth of nested archives
    if archive_depth > 6:
        return
    
    archives.unpack_archive_file(archive_path, unpack_path)
    
    folder_files_list = [(root, files) for root, dirs, files in os.walk(unpack_path)]
    
    #file_matches = []
    
    for folder_files in folder_files_list:
        source_path = folder_files[0]
        
        file_dict = {}
        
        #print '$$$$$$$$$$$$$$$$$'
        #print 'Source path: ' + source_path
        #print 'Number of files: ' + str(len(folder_files[1]))

        for file_name in folder_files[1]:
            file_dict[job_handler.get_free_file_id()] = file_name
        sub_path = source_path.replace(unpack_base_path, '').lstrip('/\\')
        destination_path = os.path.join(output_path, sub_path)
        
        #
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        #
        
        process_folder(job_identifier, source_path, file_dict, destination_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments, archive_depth)

def process_folder(job_identifier, source_path, file_dict, destination_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments, archive_depth=1):
    job_handler = JobHandler(job_identifier)
    file_matcher = FileMatcher(file_dict)
    
    for file_match in file_matcher.get_matches():
        # Rename files
        for file_id, new_file_name in file_match.get_file_dict().items():
            original_file_name = file_matcher.get_original_file_name(file_id)
            if original_file_name != new_file_name:
                filemanager.rename_file(source_path, original_file_name, new_file_name)
          
    for file_match in file_matcher.get_matches():
        job_handler.add_file_match(source_path, file_match.get_file_dict(), file_match.get_ogr_format_name(), file_match.is_archive(), file_match.is_valid())
        
    for file_match in file_matcher.get_matches(): 
        file_id = list(file_match.get_file_dict().keys())[0]         
        if not job_handler.get_file_processed(file_id):
            matched_files = job_handler.get_matched_files(file_id)
            for matched_file in matched_files:
                job_handler.set_file_processed(matched_file.file_id)
    
        if matched_files[0].file_match.is_archive:
            # Process nested archive
            archive_file_name_without_extension = os.path.splitext(matched_files[0].file_name)[0]
            archive_path = os.path.join(source_path, matched_files[0].file_name)
            unpack_path = os.path.join(source_path, archive_file_name_without_extension)
            output_path = os.path.join(destination_path, archive_file_name_without_extension)
            #process_archive(archive_path, unpack_base_path, unpack_path, output_path, export_format_name, export_format, source_srs, target_srs, additional_arguments, archive_depth+1)
            process_archive(job_identifier, archive_path, unpack_path, unpack_path, output_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments, archive_depth+1)
        else:
            # Convert files        
            conversion.convert_files(job_identifier, source_path, matched_files, destination_path, export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments)
    
def process_webservice_urls(job_identifier):
    job_handler = JobHandler(job_identifier)
    
    webservice_urls = job_handler.get_webservice_urls()
    destination_path = job_handler.get_output_folder_path()
    export_format_name = job_handler.get_export_format_name()
    source_srs = job_handler.get_source_srs()
    target_srs = job_handler.get_target_srs()
    simplify_parameter = job_handler.get_simplify_parameter()
    additional_arguments = job_handler.get_shell_parameters()
    
    base_name = 'webservice'
    counter = 1
    for webservice_url in webservice_urls.values():
        conversion.convert_webservice(job_identifier, webservice_url, destination_path, base_name + (str(counter) if counter > 1 else ''), export_format_name, source_srs, target_srs, simplify_parameter, additional_arguments)
        counter += 1

def create_download_file(job_identifier):
    job_id = job_identifier.job_id
    output_folder = filemanager.get_output_folder_path(job_id)
    zip_file_path = filemanager.get_download_file_path(job_id)
    if filemanager.get_file_count(output_folder) > 0:
        archives.create_zip_archive(output_folder, zip_file_path)

import time
from threading import Thread
from datetime import datetime, timedelta
from django.utils.timezone import utc
from OGRgeoConverter.models import JobIdentifier, OGRlogEntry
    
def cleanup():
    thread = Thread(target=cleanup_thread)
    thread.start()

def cleanup_thread():
    filemanager.remove_old_folders()
    
    job_identifiers_date_limit = (datetime.now() - timedelta(days=5)).replace(tzinfo=utc)
    JobIdentifier.cleanup_by_date(job_identifiers_date_limit)
    
    ogr_log_entry_date_limit = (datetime.now() - timedelta(weeks=18)).replace(tzinfo=utc)
    OGRlogEntry.cleanup_by_date(ogr_log_entry_date_limit)
    