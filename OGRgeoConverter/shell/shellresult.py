class ShellResult(object):
    '''
    Is returned by the Shell.
    Saves output text and error messages.
    '''

    def __init__(self, text, error):
        if text != None:
            self.__shell_text = str(text)
        else:
            self.__shell_text = ''
        if error != None:
            self.__error_text = str(error)
        else:
            self.__error_text = ''
        
    def get_text(self):
        return self.__shell_text
    
    def get_error(self):
        return self.__error_text
    
    def has_error(self):
        return self.__error_text != ''