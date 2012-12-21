'''
Function to convert files
'''

import os
from OGRgeoConverter.ogr import ogr2ogr
from OGRgeoConverter.models import OgrFormat

def convert_files(source_path, matched_files, destination_path, output_format_name, ogr_output_format, source_srs, target_srs, additional_arguments):
    input_files = []
    for file_name in matched_files.get_files():
        input_files.append(os.path.join(source_path, file_name))

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    if len(input_files) > 0:
        base_name = os.path.splitext(os.path.basename(input_files[0]))[0]
        output_file_path = _get_extended_output_file_path(destination_path, base_name, output_format_name)
        
        ogr_input_format = matched_files.get_ogr_format()
        
        format_info = OgrFormat.get_format_information_by_name(output_format_name)
        if format_info != None and format_info.state_all_files:
            input_file = ','.join(input_files)
        else:
            input_file = input_files[0]
        
        if len(additional_arguments) > 0:
            argument_list = []
            for additional_argument in additional_arguments:
                name = additional_argument.argument_name
                value = additional_argument.argument_value
                prefix = additional_argument.prefix
                quotation_marks = additional_argument.value_quotation_marks
                argument_list.append((name, value, prefix, quotation_marks))
        else:
            argument_list = []
        
        ogr2ogr.convert_file(input_file, output_file_path, ogr_input_format, ogr_output_format, source_srs, target_srs, argument_list)

def convert_webservice(webservice_url, destination_path, output_format_name, ogr_output_format, source_srs, target_srs, additional_arguments):
    base_name = 'webservice'
    output_file_path = _get_extended_output_file_path(destination_path, base_name, output_format_name)
    
    if len(additional_arguments) > 0:
        argument_list = []
        for additional_argument in additional_arguments:
            name = additional_argument.argument_name
            value = additional_argument.argument_value
            prefix = additional_argument.prefix
            quotation_marks = additional_argument.value_quotation_marks
            argument_list.append((name, value, prefix, quotation_marks))
    else:
        argument_list = []
        
    ogr2ogr.convert_wfs(webservice_url, output_file_path, ogr_output_format, source_srs, target_srs, argument_list)

def _get_extended_output_file_path(output_path, base_name, format_name):     
    output_name = os.path.join(output_path, base_name)
    
    extension = ''
    is_folder = False
    for ogr_format in OgrFormat.objects.all():
        if ogr_format.name == format_name:
            extension = ogr_format.file_extension
            is_folder = ogr_format.output_type == 'folder'
    
    if not is_folder:
        output_name = output_name + "." + extension
        
    return output_name