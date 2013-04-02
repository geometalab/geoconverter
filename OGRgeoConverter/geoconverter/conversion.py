'''
Functions to convert geo data
'''

import os
from OGRgeoConverter.ogr import ogr2ogr
from OGRgeoConverter.models import OgrFormat

def convert_files(source_path, matched_files, destination_path, output_format_name, ogr_output_format, source_srs, target_srs, simplify_parameter, additional_arguments):
    '''
    Prepares a conversion of files and calls ogr2ogr
    '''
    
    print 'Converting files...'
    
    input_files = []
    for file_name in matched_files.get_files():
        input_files.append(os.path.join(source_path, file_name))

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    format_info = OgrFormat.get_format_information_by_name(output_format_name)
    
    if len(input_files) > 0:
        base_name = os.path.splitext(os.path.basename(input_files[0]))[0]
        output_file_path = _get_extended_output_file_path(destination_path, base_name, format_info)
        
        ogr_input_format = matched_files.get_ogr_format()
        
        if format_info != None and format_info.state_all_files:
            input_file_path = ','.join(input_files)
        else:
            input_file_path = ''
            for input_file in input_files:
                if os.path.splitext(os.path.basename(input_file))[1].lower() == '.' + format_info.extension.lower():
                    input_file_path = input_file
            if input_file_path == '': input_file_path = input_files[0]
        
        argument_list = _get_argument_list(additional_arguments)
        
        ogr2ogr.convert_file(input_file_path, output_file_path, ogr_input_format, ogr_output_format, source_srs, target_srs, simplify_parameter, argument_list)

def convert_webservice(webservice_url, destination_path, base_name, output_format_name, ogr_output_format, source_srs, target_srs, simplify_parameter, additional_arguments):
    '''
    Prepares a conversion of a webservice and calls ogr2ogr
    '''
    
    format_info = OgrFormat.get_format_information_by_name(output_format_name)
    
    output_file_path = _get_extended_output_file_path(destination_path, base_name, format_info)
    argument_list = _get_argument_list(additional_arguments)
        
    ogr2ogr.convert_wfs(webservice_url, output_file_path, ogr_output_format, source_srs, target_srs, simplify_parameter, argument_list)

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

def _get_argument_list(additional_arguments):
    '''
    Returns a list of arguments used for the conversion by ogr2ogr
    '''
    
    argument_list = []
    if len(additional_arguments) > 0:
        for additional_argument in additional_arguments:
            name = additional_argument.argument_name
            value = additional_argument.argument_value
            prefix = additional_argument.prefix
            quotation_marks = additional_argument.value_quotation_marks
            argument_list.append((name, value, prefix, quotation_marks))
        
    return argument_list