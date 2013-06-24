'''
Interface for the OGR tool "ogrinfo".
Returns supported formats
'''

from OGRgeoConverter.tools.shell import ShellCommand
from collections import namedtuple


def get_supported_formats():
    shell_command = ShellCommand()
    shell_command.set_command('ogrinfo')
    
    shell_command.add_parameter('formats', None, '--')
    
    shell_command.execute()
    
    OgrFormat = namedtuple('OgrFormat', ['name', 'read', 'write'])
    format_list = []
    for line in shell_command.get_result_output().splitlines():
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