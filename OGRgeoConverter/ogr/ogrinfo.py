'''
Interface for the OGR tool "ogrinfo".
Returns supported formats
'''

from OGRgeoConverter.shell.shellcall import ArgumentList
from OGRgeoConverter.shell.shellcall import ShellCall
from OGRgeoConverter.shell import shell
from collections import namedtuple

def get_ogrinfo_shell_call():
    call = ShellCall()
    call.set_command('ogrinfo')
    return call

def get_supported_formats():
    call = get_ogrinfo_shell_call()
    
    arguments = ArgumentList()
    arguments.add_argument('formats', None, '--')
    call.set_arguments(arguments)
    
    result = shell.execute(call)
    
    OgrFormat = namedtuple('OgrFormat', ['name', 'read', 'write'])
    format_list = []
    for line in result.get_text().splitlines():
        if '->' in line:
            name_pos1 = line.find('"') + 1
            name_pos2 = line.find('"', name_pos1)
            name = line[name_pos1:name_pos2]
            if 'readonly' in line:
                read = True
                write = False
            elif 'writeonly' in line:
                # probably not used by OGR
                read = False
                write = True
            elif 'read/write' in line:
                read = True
                write = True
            else:
                # should not be the case
                read = False
                write = False
            format_list.append(OgrFormat(name, read, write))
    
    return format_list