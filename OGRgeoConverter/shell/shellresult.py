class ShellResult:
    '''
    Is returned by the Shell.
    Stores output text and error messages.
    '''

    def __init__(self, text, error):
        if text != None:
            self.__shell_text = text.decode('utf-8')
        else:
            self.__shell_text = ''
        if error != None:
            self.__error_text = error.decode('utf-8')
        else:
            self.__error_text = ''
        
    def get_text(self):
        return self.__shell_text
    
    def get_error(self):
        return self.__error_text
    
    def has_error(self):
        return self.__error_text != ''