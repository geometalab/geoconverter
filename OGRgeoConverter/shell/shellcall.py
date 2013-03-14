class ShellCall(object):
    '''
    Can be sent to the Shell to be executed.
    Saves a command and its arguments.
    '''

    def __init__(self):
        self.__arguments = None
    
    def set_command(self, command):
        self.__command = command
        
    def set_arguments(self, arguments):
        self.__arguments = arguments
        
    def get_shell_command(self):
        if self.__arguments == None:
            argument_string = ''
        else:
            argument_string = self.__arguments.get_arguments_string()
        if argument_string != '':
            argument_string = ' ' + argument_string
        return self.__command + argument_string



class ArgumentList(object):
    '''
    Represents a list of arguments for a shell command
    '''

    def __init__(self):
        self.__argument_list = []
        
    def add_argument(self, argument_name, argument_value, prefix='-', value_quotation_marks=True):
        if argument_name == None:
            argument_name = ''
        if argument_value == None:
            argument_value = ''
        if prefix == None:
            prefix = ''
        self.__argument_list.append((prefix, argument_name, argument_value, value_quotation_marks))
    
    def get_arguments_string(self):
        output = ''
        for argument in self.__argument_list:
            prefix = ('' if argument[1] == '' else argument[0])
            argument_name = argument[1]
            value = self.__get_value_string(argument[2], argument[3], prefix=='' and argument_name=='')
            output += ' ' + prefix + argument_name + value
        return output[1:]
    
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