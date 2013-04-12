'''
Functions to read and write log entries.
'''

from OGRgeoConverter.models import LogEntry
from OGRgeoConverter.geoconverter import datetimehandler

def _get_log_entry_query_set(session_key, job_id):
    log_entries = LogEntry.get_log_entry(session_key, job_id)
    if len(log_entries) == 0:
        # Creat log entry if it doesen't exist yet
        log_entry = LogEntry()
        log_entry.session_key = session_key
        log_entry.job_id = job_id
        log_entry.start_time = datetimehandler.get_default_datetime();
        log_entry.end_time = datetimehandler.get_default_datetime();
        log_entry.download_file_size = -1
        log_entry.save()
        log_entries = LogEntry.get_log_entry(session_key, job_id)
    
    return log_entries

def set_input_type(session_key, job_id, input_type):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(input_type=input_type)
    
def set_start_time(session_key, job_id):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(start_time=datetimehandler.get_now())
    
def set_end_time(session_key, job_id):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(end_time=datetimehandler.get_now())
    
def set_export_format(session_key, job_id, export_format):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(export_format=export_format)

def set_srs(session_key, job_id, source_srs, target_srs):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(source_srs=source_srs)
    log_entry.update(target_srs=target_srs)
    
def set_download_file_size(session_key, job_id, file_size):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(download_file_size=file_size)
    
def set_simplify_parameter(session_key, job_id, simplify_parameter):
    log_entry = _get_log_entry_query_set(session_key, job_id)
    log_entry.update(simplify_parameter=simplify_parameter)

def add_ogr_command(session_key, job_id, ogr_command):
    pass
    #log_entry = _get_log_entry_query_set(session_key, job_id)
    #max_length = LogEntry.ogr_command_max_length()
    #if len(ogr_command) > max_length:
    #    ogr_command = ogr_command[0:max_length-6] + ' [...]'
    #log_entry.update(ogr_command=ogr_command)
    
def add_ogr_error_message(session_key, job_id, ogr_error_message):
    pass
    #log_entry = _get_log_entry_query_set(session_key, job_id)
    #max_length = LogEntry.ogr_error_message_max_length()
    #if len(ogr_error_message) > max_length:
    #    ogr_error_message = ogr_error_message[0:max_length-6] + ' [...]'
    #log_entry.update(ogr_error_message=ogr_error_message)