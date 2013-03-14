'''
Functions to read and write log entries.
'''

from OGRgeoConverter.models import LogEntry
from OGRgeoConverter.geoconverter import sessionhandler

def create_log_entry(session_key, path_code):
    session = sessionhandler.get_session(session_key)
    if not 'log_entries' in session:
        session['log_entries'] = {}
    if not path_code in session['log_entries']:
        log_entry = LogEntry()
        log_entry.start_time = '2000-01-01 00:00:00'
        log_entry.end_time = '2000-01-01 00:00:00'
        log_entry.download_file_size = -1
        log_entry.save()
        session['log_entries'][path_code] = log_entry
    else:
        log_entry = session['log_entries'][path_code]
    session.save()
    
    return log_entry

def get_log_entry(session_key, path_code):
    return create_log_entry(session_key, path_code)
    
def store_log_entry(session_key, path_code, log_entry):
    log_entry.save()
    session = sessionhandler.get_session(session_key)
    if not 'log_entries' in session:
        session['log_entries'] = {}
    session['log_entries'][path_code] = log_entry
    session.save()

def set_input_type(session_key, path_code, input_type):
    log_entry = get_log_entry(session_key, path_code)
    log_entry.input_type = input_type
    store_log_entry(session_key, path_code, log_entry)
    
def set_start_time(session_key, path_code, start_time):
    log_entry = get_log_entry(session_key, path_code)
    log_entry.start_time = start_time
    store_log_entry(session_key, path_code, log_entry)
    
def set_end_time(session_key, path_code, end_time):
    log_entry = get_log_entry(session_key, path_code)
    log_entry.end_time = end_time
    store_log_entry(session_key, path_code, log_entry)
    
def set_export_format(session_key, path_code, export_format):
    log_entry = get_log_entry(session_key, path_code)
    log_entry.export_format = export_format
    store_log_entry(session_key, path_code, log_entry)

def set_srs(session_key, path_code, source_srs, target_srs):
    log_entry = get_log_entry(session_key, path_code)
    log_entry.source_srs = source_srs
    log_entry.target_srs = target_srs
    store_log_entry(session_key, path_code, log_entry)
    
def set_download_file_size(session_key, path_code, file_size):
    log_entry = get_log_entry(session_key, path_code)
    log_entry.download_file_size = file_size
    store_log_entry(session_key, path_code, log_entry)
