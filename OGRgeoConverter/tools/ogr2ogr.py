import os
from OGRgeoConverter.tools.shell import ShellCommand


class Ogr2ogr:

    '''
    Class to convert files and WMS.
    Interface for the OGR tool "ogr2ogr".
    '''

    def __init__(self):
        self.__input_file_path = ''
        self.__webservice_url = ''
        self.__output_file_path = ''
        self.__ogr_output_format = ''
        self.__source_srs = 0
        self.__target_srs = 0
        self.__simplify_parameter = 0
        self.__additional_shell_parameters = []
        self.__last_command = ''
        self.__last_output = ''
        self.__last_error = ''
        self.__last_successful = False

    def set_input_file_path(self, input_file_path):
        self.__input_file_path = input_file_path

    def get_input_file_path(self):
        return self.__input_file_path

    def set_webservice_url(self, webservice_url):
        self.__webservice_url = webservice_url

    def get_webservice_url(self):
        return self.__webservice_url

    def set_output_file_path(self, output_file_path):
        self.__output_file_path = output_file_path

    def get_output_file_path(self):
        return self.__output_file_path

    def set_ogr_output_format(self, ogr_output_format):
        self.__ogr_output_format = ogr_output_format

    def get_ogr_output_format(self):
        return self.__ogr_output_format

    def set_source_srs(self, source_srs):
        self.__source_srs = source_srs

    def get_source_srs(self):
        return self.__source_srs

    def set_target_srs(self, target_srs):
        self.__target_srs = target_srs

    def get_target_srs(self):
        return self.__target_srs

    def set_simplify_parameter(self, simplify_parameter):
        self.__simplify_parameter = simplify_parameter

    def get_simplify_parameter(self):
        return self.__simplify_parameter

    def add_shell_parameter(self, shell_parameter):
        self.__additional_shell_parameters.append(shell_parameter)

    def get_additional_shell_parameters(self):
        return self.__additional_shell_parameters

    def get_last_output(self):
        return self.__last_error if self.__last_error != '' else self.__last_output

    def __get_base_shell_command(self):
        shell_command = ShellCommand()
        shell_command.set_command('ogr2ogr')

        # Sets EPGS numbers
        if self.__source_srs != 0:
            shell_command.add_parameter(
                's_srs', 'EPSG:' + str(self.__source_srs),
                '-', False)
        if self.__target_srs != 0:
            shell_command.add_parameter(
                't_srs', 'EPSG:' + str(self.__target_srs),
                '-', False)

        # Sets Simplify parameter
        if self.__simplify_parameter > 0:
            shell_command.add_parameter(
                'simplify',
                self.__simplify_parameter,
                '-',
                False)

        # Sets additional parameters
        for shell_parameter in self.__additional_shell_parameters:
            shell_command.add_parameter_object(shell_parameter)

        # Sets the output format
        shell_command.add_parameter('f', self.__ogr_output_format)

        # Sets the output file
        shell_command.add_parameter(None, self.__output_file_path)

        return shell_command

    def __get_file_conversion_command(self):
        shell_command = self.__get_base_shell_command()
        # Sets the input file
        shell_command.add_parameter(None, self.__input_file_path)
        return shell_command

    def __get_webservice_conversion_command(self):
        shell_command = self.__get_base_shell_command()
        # Sets the WMS url
        shell_command.add_parameter(None, 'WFS:' + self.__webservice_url)
        return shell_command

    def get_file_conversion_command(self):
        shell_command = self.__get_file_conversion_command()
        return shell_command.get_full_command_string()

    def get_webservice_conversion_command(self):
        shell_command = self.__get_webservice_conversion_command()
        return shell_command.get_full_command_string()

    def get_last_command(self):
        return self.__last_command

    def get_last_successful(self):
        return self.__last_successful

    def convert_file(self):
        shell_command = self.__get_file_conversion_command()
        self.__last_command = shell_command.get_full_command_string()
        shell_command.execute()
        # Fehlermeldungen analysieren => ogr2ogr result!
        self.__last_output = shell_command.get_result_output()
        self.__last_error = shell_command.get_result_error()
        self.__last_successful = os.path.exists(self.__output_file_path)

    def convert_wfs(self):
        shell_command = self.__get_webservice_conversion_command()
        self.__last_command = shell_command.get_full_command_string()
        shell_command.execute()
        self.__last_output = shell_command.get_result_output()
        self.__last_error = shell_command.get_result_error()
        self.__last_successful = os.path.isfile(self.__output_file_path)
