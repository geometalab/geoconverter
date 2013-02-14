'''
Functions to process conversion jobs.
'''

import os
from OGRgeoConverter.filesystem import filemanager, archives
from OGRgeoConverter.geoconverter import sessionhandler, conversion
from OGRgeoConverter.geoconverter.filematching import FileMatcher

def _initialize_job(session_key, job_id):
    session = sessionhandler.get_session(session_key)
    if not 'jobs' in session:
        session['jobs'] = {}
    if not job_id in session['jobs']:
        session['jobs'][job_id] = ConversionJob(job_id)
    session.save()
    
def add_file_names(session_key, job_id, file_dict):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    session['jobs'][job_id].add_file_names(file_dict)
    session.save()
    
def add_webservice_url(session_key, job_id, webservice_url):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    session['jobs'][job_id].add_webservice_url(webservice_url)
    session.save()
    
def set_export_format(session_key, job_id, export_format_name):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    
    session['jobs'][job_id].set_export_format_name(export_format_name)
    
    from OGRgeoConverter.models import OgrFormat
    format_information = OgrFormat.get_format_information_by_name(export_format_name)
    
    if format_information != None:
        session['jobs'][job_id].set_export_format(format_information.ogr_name)
        session['jobs'][job_id].set_additional_arguments(format_information.additional_arguments)
            
    session.save()
    
def set_srs(session_key, job_id, source_srs, target_srs):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    session['jobs'][job_id].set_source_srs(source_srs)
    session['jobs'][job_id].set_target_srs(target_srs)
    session.save()
        
def remove_file(session_key, job_id, file_id):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    session['jobs'][job_id].remove_file(file_id)
    session.save()
    
def store_file(session_key, job_id, file_id, file_data):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    conversion_job = session['jobs'][job_id]
    # TODO: check if file was removed
    file_name = conversion_job.get_file_name(file_id)
    path_code = conversion_job.get_path_code()
    filemanager.store_uploaded_file(path_code, file_data, file_name)
    
    # reload session to reduce race conditions
    session = sessionhandler.get_session(session_key)
    session['jobs'][job_id].set_file_uploaded(file_id)
    session.save()
    
def process_file(session_key, job_id, file_id):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    conversion_job = session['jobs'][job_id]
    if conversion_job.file_ready_for_process(file_id):
        matched_files = conversion_job.get_matched_files(file_id)
        for matched_file_id in matched_files.get_file_dict().keys():
            conversion_job.set_file_processed(matched_file_id)
        session.save()
        
        source_path = conversion_job.get_upload_folder_path()
        destination_path = conversion_job.get_output_folder_path()
        export_format_name = conversion_job.get_export_format_name()
        export_format = conversion_job.get_export_format()
        source_srs = conversion_job.get_source_srs()
        target_srs = conversion_job.get_target_srs()
        additional_arguments = conversion_job.get_additional_arguments()
        if matched_files.is_archive():
            extract_path = conversion_job.get_extract_folder_path()
            file_name = matched_files.get_files()[0]
            if conversion_job.get_file_count() > 1:
                # Creates a sub folder in the extract folder
                extract_path = os.path.join(extract_path, os.path.splitext(file_name)[0])
            process_archive(os.path.join(source_path, file_name), extract_path, destination_path, export_format_name, export_format, source_srs, target_srs, additional_arguments)
        else:
            conversion.convert_files(source_path, matched_files, destination_path, export_format_name, export_format, source_srs, target_srs, additional_arguments)

def process_archive(archive_path, unpack_path, output_path, export_format_name, export_format, source_srs, target_srs, additional_arguments):
    archives.unpack_archive_file(archive_path, unpack_path)
    
    folder_files_list = [(root, files) for root, dirs, files in os.walk(unpack_path)]
    
    file_matches = []
    
    for folder_files in folder_files_list:
        print '++++++++++++++++++++'
        print folder_files
        
        source_path = folder_files[0]
        
        file_dict = {}
        file_id_counter = 0
        for file_name in folder_files[1]:
            file_dict[file_id_counter] = file_name
            file_id_counter += 1
            
        sub_path = source_path.replace(unpack_path, '').lstrip('/\\')
        destination_path = os.path.join(output_path, sub_path)
        
        process_folder(source_path, file_dict, destination_path, export_format_name, export_format, source_srs, target_srs, additional_arguments)

def process_folder(source_path, file_dict, destination_path, export_format_name, export_format, source_srs, target_srs, additional_arguments):
    file_matcher = FileMatcher(file_dict)
    
    for file_match in file_matcher.get_matches():
        if file_match.is_archive():
            print 'Nested archive!!!!!'
            #extract_path = conversion_job.get_extract_folder_path()
            #process_archive(os.path.join(source_path, file_match.get_file[0]), extract_path)
        else:
            '''
            x y
            x y
            x y
            File match: Original Names + Destination Names
            x y
            x y
            x y
            '''
            conversion.convert_files(source_path, file_match, destination_path, export_format_name, export_format, source_srs, target_srs, additional_arguments)

def process_webservice_urls(session_key, job_id):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    conversion_job = session['jobs'][job_id]
    
    webservice_urls = conversion_job.get_webservice_urls()
    destination_path = conversion_job.get_output_folder_path()
    export_format_name = conversion_job.get_export_format_name()
    export_format = conversion_job.get_export_format()
    source_srs = conversion_job.get_source_srs()
    target_srs = conversion_job.get_target_srs()
    additional_arguments = conversion_job.get_additional_arguments()
    
    base_name = 'webservice'
    if len(webservice_urls) == 1:
        conversion.convert_webservice(webservice_urls[0], destination_path, base_name, export_format_name, export_format, source_srs, target_srs, additional_arguments)
    else:
        counter = 1
        for webservice_url in webservice_urls:
            conversion.convert_webservice(webservice_url, destination_path, base_name + str(counter), export_format_name, export_format, source_srs, target_srs, additional_arguments)
            counter += 1

def create_download_file(session_key, job_id):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    path_code = session['jobs'][job_id].get_path_code()
    output_folder = filemanager.get_output_folder_path(path_code)
    zip_file_path = filemanager.get_download_file_path(path_code)
    archives.create_zip_archive(output_folder, zip_file_path)
            
def is_canceled(session_key, job_id):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    return session['jobs'][job_id].get_file_count() == 0

def get_path_code(session_key, job_id):
    _initialize_job(session_key, job_id)
    session = sessionhandler.get_session(session_key)
    return session['jobs'][job_id].get_path_code()


class ConversionJob:
    '''
    Class storing information of a conversion job.
    '''
    
    def __init__(self, job_id):
        self.__job_id = job_id
        self.__export_format = ''
        self.__export_format_name = ''
        self.__source_srs = 0
        self.__target_srs = 0
        self.__additional_arguments = []
        
        self.__file_dict = {}
        self.__uploaded_file_dict = {}
        self.__processed_file_dict = {}
        self.__matched_files = FileMatcher({})
        
        self.__webservice_urls = []
        
        self.__path_code = filemanager.get_empty_job_folder()
        self.__upload_path = filemanager.get_upload_folder_path(self.__path_code)
        self.__extract_path = filemanager.get_extract_folder_path(self.__path_code)
        self.__output_path = filemanager.get_output_folder_path(self.__path_code)
        self.__download_path = filemanager.get_download_folder_path(self.__path_code)
        
    def get_path_code(self):
        return self.__path_code
    
    def add_file_names(self, file_dict):
        self.__file_dict.update(file_dict)
        self.__matched_files = FileMatcher(self.__file_dict)
        
        for key, value in self.__file_dict.items():
            if not key in self.__uploaded_file_dict:
                self.__uploaded_file_dict[key] = False
                self.__processed_file_dict[key] = False
                
    def add_webservice_url(self, webservice_url):
        self.__webservice_urls.append(webservice_url)
        
    def get_webservice_urls(self):
        return self.__webservice_urls
        
    def set_export_format(self, export_format):
        self.__export_format = export_format
        
    def get_export_format(self):
        return self.__export_format
    
    def set_export_format_name(self, export_format_name):
        self.__export_format_name = export_format_name
        
    def get_export_format_name(self):
        return self.__export_format_name
    
    def set_source_srs(self, source_srs):
        if len(source_srs) <= 8 and source_srs.isdigit():
            self.__source_srs = int(source_srs)
        
    def get_source_srs(self):
        return self.__source_srs
    
    def set_target_srs(self, target_srs):
        if len(target_srs) <= 8 and target_srs.isdigit():
            self.__target_srs = int(target_srs)
        
    def get_target_srs(self):
        return self.__target_srs
    
    def set_additional_arguments(self, additional_arguments):
        self.__additional_arguments = additional_arguments
            
    def get_additional_arguments(self):
        return self.__additional_arguments
    
    def get_file_count(self):
        return len(self.__file_dict)
    
    def get_file_name(self, file_id):
        return self.__matched_files.get_file_name(file_id)
    
    def set_file_uploaded(self, file_id):
        self.__uploaded_file_dict[file_id] = True
        
    def remove_file(self, file_id):
        if file_id in self.__file_dict:
            del self.__file_dict[file_id]
        self.__matched_files = FileMatcher(self.__file_dict)
            
    def file_ready_for_process(self, file_id):
        matched_files = self.get_matched_files(file_id)
        if matched_files == None:
            return False
        
        is_ready = True
        for matched_file_id in matched_files.get_file_dict().keys():
            if not self.__uploaded_file_dict[matched_file_id]:
                is_ready = False
        return is_ready
    
    def set_file_processed(self, file_id):
        self.__processed_file_dict[file_id] = True
        
    def get_matched_files(self, file_id):
        return self.__matched_files.get_match(file_id)
    
    
    def get_upload_folder_path(self):
        return self.__upload_path

    def get_extract_folder_path(self):
        return self.__extract_path
    
    def get_output_folder_path(self):
        return self.__output_path
    
    def get_download_folder_path(self):
        return self.__download_path
