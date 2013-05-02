from OGRgeoConverter.models import LogEntry
from OGRgeoConverter.models import OGRlogEntry
from OGRgeoConverter.geoconverter import datetimehandler


class LogHandler:
    '''
    Class to read and write log entries.
    '''

    def __init__(self, job_identifier):
        if job_identifier != None:
            self.__job_identifier = job_identifier
        else:
            raise Exception("job_identifier may not be None")
    
    def __get_log_entry_query_set(self):
        log_entries = LogEntry.get_log_entry(self.__job_identifier)
        
        if len(log_entries) == 0:
            # Creat log entry if it doesen't exist yet
            log_entry = LogEntry()
            log_entry.job_identifier = self.__job_identifier
            log_entry.start_time = datetimehandler.get_default_datetime();
            log_entry.end_time = datetimehandler.get_default_datetime();
            log_entry.download_file_size = -1
            log_entry.save()
            log_entries = LogEntry.get_log_entry(self.__job_identifier)
        
        if len(log_entries) == 1:
            return log_entries
        else:
            raise Exception("Number of found log_entries must be 1")
    
    def set_input_type(self, input_type):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(input_type=input_type)
        
    def get_input_type(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].input_type
            
    def set_start_time(self):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(start_time=datetimehandler.get_now())
        
    def get_start_time(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].start_time
    
    def set_end_time(self):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(end_time=datetimehandler.get_now())
    
    def get_end_time(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].end_time
    
    def set_export_format(self, export_format):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(export_format=export_format)
    
    def get_export_format(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].export_format
    
    def set_source_srs(self, source_srs):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(source_srs=source_srs)
    
    def get_source_srs(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].source_srs
    
    def set_target_srs(self, target_srs):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(target_srs=target_srs)
    
    def get_target_srs(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].target_srs
    
    def set_simplify_parameter(self, simplify_parameter):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(simplify_parameter=simplify_parameter)
        
    def get_simplify_parameter(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].simplify_parameter
    
    def set_download_file_size(self, file_size):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(download_file_size=file_size)
    
    def get_download_file_size(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].download_file_size
    
    def add_ogr_log_entry(self, ogr_command, ogr_error_message, is_successful):
        command_max_length = OGRlogEntry._meta.get_field('ogr_command').max_length
        if len(ogr_command) > command_max_length:
            ogr_command = ogr_command[0:command_max_length-7] + ' [...]'
        
        error_message_max_length = OGRlogEntry._meta.get_field('ogr_error_message').max_length
        if len(ogr_error_message) > error_message_max_length:
            ogr_error_message = ogr_error_message[0:error_message_max_length-7] + ' [...]'
        
        log_entry = self.__get_log_entry_query_set(session_key, job_id)
        
        ogr_log_entry = OGRlogEntry()
        ogr_log_entry.log_entry = log_entry
        ogr_log_entry.command = ogr_command
        ogr_log_entry.error_message = ogr_error_message
        ogr_log_entry.is_successful = is_successful
        ogr_log_entry.save()
        
    def get_ogr_log_entries(self):
        raise Exception("Function not implemented")