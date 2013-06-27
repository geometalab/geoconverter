'''
Functions to convert geo data
'''

import os
from OGRgeoConverter.tools.ogr2ogr import Ogr2ogr
from OGRgeoConverter.modelhandlers.loghandler import LogHandler
from OGRgeoConverter.modelhandlers.jobhandler import JobHandler
from OGRgeoConverter.models import OgrFormat

def convert_files(job_identifier, source_path, matched_files, destination_path, output_format_name, source_srs, target_srs, simplify_parameter, additional_arguments):
    '''
    Prepares a conversion of files and calls ogr2ogr
    '''
    
    input_files = []
    for matched_file in matched_files:
        input_files.append(os.path.join(source_path, matched_file.file_name))

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    if len(input_files) > 0:
        input_format_name = matched_files[0].file_match.identified_format_name
        input_format_info = OgrFormat.get_format_information_by_name(input_format_name)
        output_format_info = OgrFormat.get_format_information_by_name(output_format_name)
    
        if input_format_info != None:
            ogr_input_format = input_format_info.ogr_name
            input_format_extension = input_format_info.extension.lower()
            for shell_parameter in input_format_info.additional_parameters:
                if shell_parameter.use_for_reading:
                    additional_arguments.append(shell_parameter)
        else:
            ogr_input_format = ''
            input_format_extension = os.path.splitext(os.path.basename(input_files[0]))[0].lower()
            
        ogr_output_format = output_format_info.ogr_name
        
        base_name = os.path.splitext(os.path.basename(input_files[0]))[0]
        output_file_path = _get_extended_output_file_path(destination_path, base_name, output_format_info)
              
        if input_format_info != None and input_format_info.state_all_files:
            input_file_path = ','.join(input_files)
        else:
            input_file_path = ''
            for input_file in input_files:
                if os.path.splitext(os.path.basename(input_file))[1].lower() == '.' + input_format_extension:
                    input_file_path = input_file
            if input_file_path == '': input_file_path = input_files[0]
        
        ogr2ogr_converter = Ogr2ogr()
        ogr2ogr_converter.set_input_file_path(input_file_path)
        ogr2ogr_converter.set_output_file_path(output_file_path)
        ogr2ogr_converter.set_ogr_output_format(ogr_output_format)
        ogr2ogr_converter.set_source_srs(source_srs)
        ogr2ogr_converter.set_target_srs(target_srs)
        ogr2ogr_converter.set_target_srs(target_srs)
        for shell_parameter in additional_arguments:
            ogr2ogr_converter.add_shell_parameter(shell_parameter)
        ogr2ogr_converter.convert_file()
        
        input_file_names = []
        for matched_file in matched_files:
            input_file_names.append(matched_file.file_name)
        file_list = ', '.join(input_file_names)
        _add_ogr_log_entry(job_identifier, file_list, destination_path, ogr2ogr_converter.get_last_command(), ogr2ogr_converter.get_last_output(), ogr2ogr_converter.get_last_successful())
    else:
        pass
        # Error !!!!!!!!!!!!!!!!!!!
        
def convert_webservice(job_identifier, webservice_url, destination_path, base_name, output_format_name, source_srs, target_srs, simplify_parameter, additional_arguments):
    '''
    Prepares a conversion of a webservice and calls ogr2ogr
    '''
    
    output_format_info = OgrFormat.get_format_information_by_name(output_format_name)
    ogr_output_format = output_format_info.ogr_name
    
    output_file_path = _get_extended_output_file_path(destination_path, base_name, output_format_info)
    
    ogr2ogr_converter = Ogr2ogr()
    ogr2ogr_converter.set_webservice_url(webservice_url)
    ogr2ogr_converter.set_output_file_path(output_file_path)
    ogr2ogr_converter.set_ogr_output_format(ogr_output_format)
    ogr2ogr_converter.set_source_srs(source_srs)
    ogr2ogr_converter.set_target_srs(target_srs)
    ogr2ogr_converter.set_target_srs(target_srs)
    for shell_parameter in additional_arguments:
        ogr2ogr_converter.add_shell_parameter(shell_parameter)
    ogr2ogr_converter.convert_wfs()
    
    _add_ogr_log_entry(job_identifier, webservice_url, destination_path, ogr2ogr_converter.get_last_command(), ogr2ogr_converter.get_last_output(), ogr2ogr_converter.get_last_successful())
    
    
def _get_extended_output_file_path(output_path, base_name, format_info):
    '''
    Returns the output path.
    For folders: name of the input file.
    For files: name of the input file and export file extension.
    '''
    
    output_name = os.path.join(output_path, base_name)
    
    extension = ''
    is_folder = False
    if format_info != None:
        extension = format_info.extension
        is_folder = format_info.is_folder
    
    if not is_folder:
        output_name = output_name + '.' + extension
        
    return output_name


def _add_ogr_log_entry(job_identifier, input_string, full_path, ogr_command, ogr_error_message, is_successful):
    log_handler = LogHandler(job_identifier)
    job_handler = JobHandler(job_identifier)
    sub_path = full_path.replace(job_handler.get_output_folder_path(), '').lstrip('/\\')
    if sub_path == '':
        sub_path = '-'
    else:
        sub_path = os.path.join('.', sub_path)
    log_handler.add_ogr_log_entry(sub_path, input_string, ogr_command, ogr_error_message, is_successful)
    