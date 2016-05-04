import shlex
import locale
from subprocess import Popen, PIPE


class ShellCommand:

    '''
    Class to build and execute Shell Commands
    '''

    def __init__(self):
        self.__command = ''
        self.__parameter_list = ShellParameterList()
        self.__result_output = ''
        self.__result_error = ''
        self.__commandtimeoutsecs = 600

    def set_command(self, command):
        self.__command = command

    def set_timeout(self, timeout=None):
        self.__commandtimeoutsecs = timeout

    def get_command(self):
        return self.__command

    def get_full_command_string(self):
        parameter_string = self.__parameter_list.get_parameters_string()
        if parameter_string != '':
            argument_string = ' ' + parameter_string
        return self.__command + argument_string

    def add_parameter(
            self,
            parameter_name,
            parameter_value,
            prefix='-',
            value_quotation_marks=True):
        self.__parameter_list.add_parameter(
            parameter_name,
            parameter_value,
            prefix,
            value_quotation_marks)

    def add_parameter_object(self, shell_parameter):
        self.__parameter_list.add_parameter(
            shell_parameter.parameter_name,
            shell_parameter.parameter_value,
            shell_parameter.prefix,
            shell_parameter.value_quotation_marks)

    def execute(self):
        command = self.get_full_command_string()
        try:
            args = shlex.split(command)
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate(timeout=self.__commandtimeoutsecs)
        except subprocess.TimeoutExpired as e:
            # The child process is not killed if the timeout expires
            p.kill()
            stdout, stderr = p.communicate()
            if not stderr:
                stderr = e
        except Exception as e:
            stdout = ''
            stderr = e

        encoding = locale.getdefaultlocale()[1]
        if encoding is None:
            encoding = 'utf-8'
        if stdout is not None:
            self.__result_output = stdout.decode(encoding)
        if stderr is not None:
            self.__result_error = stderr.decode(encoding)

    def get_result_output(self):
        return self.__result_output

    def get_result_error(self):
        return self.__result_error

    def has_error(self):
        return self.__result_error != ''


class ShellParameterList(object):

    '''
    Represents a list of parameters to be used in a shell command
    '''

    def __init__(self):
        self.__parameter_list = []

    def add_parameter(
            self,
            parameter_name,
            parameter_value,
            prefix='-',
            value_quotation_marks=True):
        if parameter_name is None:
            parameter_name = ''
        if parameter_value is None:
            parameter_value = ''
        if prefix is None:
            prefix = ''
        self.__parameter_list.append(
            (prefix,
             parameter_name,
             parameter_value,
             value_quotation_marks))

    def get_parameters_string(self):
        output = ''
        for parameter in self.__parameter_list:
            prefix = ('' if parameter[1] == '' else parameter[0])
            parameter_name = parameter[1]
            value = self.__get_value_string(
                parameter[2],
                parameter[3],
                parameter_name == '')
            output += ' ' + prefix + parameter_name + value
        return output[1:]  # cuts ' ' at beginning

    def __get_value_string(self, value, quotation_marks, value_only):
        if value == '':
            newvalue = ''
        else:
            if quotation_marks:
                newvalue = '"' + value + '"'
            else:
                newvalue = str(value)
            if not value_only:
                newvalue = ' ' + newvalue
        return newvalue
