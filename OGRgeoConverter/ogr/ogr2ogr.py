'''
Interface for the OGR tool "ogr2ogr".
Converts files.
'''

from OGRgeoConverter.shell.shellcall import ArgumentList
from OGRgeoConverter.shell.shellcall import ShellCall
from OGRgeoConverter.shell import shell

def get_ogr2ogr_shell_call():
    call = ShellCall()
    call.set_command('ogr2ogr')
    return call

def convert_file(input_file_path, output_file_path, ogr_input_format, ogr_output_format, source_srs = 0, target_srs = 0, additional_arguments = []):
    arguments = ArgumentList()
    
    # Sets the output format
    arguments.add_argument('f', ogr_output_format)
    
    # Sets the output file
    arguments.add_argument(None, output_file_path)
    
    # Sets the input file
    arguments.add_argument(None, input_file_path)
    
    # Sets EPGS Number
    if source_srs != 0:
        arguments.add_argument('s_srs', 'EPSG:'  + str(source_srs), '-', False)
    if target_srs != 0:
        arguments.add_argument('t_srs', 'EPSG:'  + str(target_srs), '-', False)
    
    # Sets optional arguments
    for additional_argument in additional_arguments:
        arguments.add_argument(additional_argument[0], additional_argument[1], additional_argument[2], additional_argument[3])
    
    call = get_ogr2ogr_shell_call()
    call.set_arguments(arguments)
    
    print '________________'
    print call.get_shell_command()
    print ''
    
    result = shell.execute(call)
    
    # !!! Fehlermeldungen umwandeln => ogr2ogr result !!!
    return result

def convert_wfs(webservice_url, output_file_path, ogr_output_format, source_srs, target_srs, additional_arguments = []):
    arguments = ArgumentList()
    
    # Sets the output format
    arguments.add_argument('f', ogr_output_format)
    
    # Sets the output file
    arguments.add_argument(None, output_file_path)
    
    # Sets the input file
    arguments.add_argument(None, 'WFS:' + webservice_url)
    
    # Sets EPGS Number
    if source_srs != 0:
        arguments.add_argument('s_srs', 'EPSG:'  + str(source_srs), '-', False)
    if target_srs != 0:
        arguments.add_argument('t_srs', 'EPSG:'  + str(target_srs), '-', False)
    
    # Sets optional arguments
    for additional_argument in additional_arguments:
        arguments.add_argument(additional_argument[0], additional_argument[1], additional_argument[2], additional_argument[3])
    
    call = get_ogr2ogr_shell_call()
    call.set_arguments(arguments)
    
    print '________________'
    print call.get_shell_command()
    print ''
    
    result = shell.execute(call)
    
    return result

def _is_valid_wfs():
    return True
# ogrinfo -ro -al "WFS:http://openpoimap.ch:80/featureserver/workspace.cgi?key=VajtE4Wk9dX3acyFx8sWNX" WFSLayerMetadata

#INFO: Open of `WFS:http://openpoimap.ch:80/featureserver/workspace.cgi?key=VajtE
#4Wk9dX3acyFx8sWNX'
#      using driver `WFS' successful.
#...