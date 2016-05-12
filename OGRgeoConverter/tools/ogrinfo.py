'''
Interface for the OGR tool "ogrinfo".
Returns supported formats
'''

from OGRgeoConverter.tools.shell import ShellCommand
from collections import namedtuple
import re


def get_version_based_format_re():
    """Retrieve regex to match version specific --formats output
    Example output of version 1.x of ogr2ogr:
      -> "ESRI Shapefile" (read/write)
      -> "UK .NTF" (readonly)
    Example output of version 2.x of ogr2ogr:
      ESRI Shapefile -vector- (rw+v): ESRI Shapefile
      UK .NTF -vector- (ro): UK .NTF
    """
    shell_command = ShellCommand()
    shell_command.set_command('ogrinfo')
    shell_command.add_parameter('version', None, '--')
    shell_command.execute()
    version_pattern = re.compile(
        r'^GDAL\s+(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+[^,]*),.*$', re.M)
    re_match = version_pattern.match(shell_command.get_result_output())
    if re_match is not None:
        if re_match.group('major') == '2':
            return re.compile(
                r'^\s+(?P<name>.*) -[^(]+\(((?P<rw>rw)|(?P<r>ro)|(?P<w>w))(?P<otherflags>[^)]*)\):.*$')
    return re.compile(
        r'^\s+->[^"]*"(?P<name>[^"]+)"[^(]+\(((?P<rw>read/write)|(?P<r>readonly)|(?P<w>writeonly))\).*$')


def get_supported_formats():
    format_re = get_version_based_format_re()
    shell_command = ShellCommand()
    shell_command.set_command('ogrinfo')
    shell_command.add_parameter('formats', None, '--')
    shell_command.execute()

    OgrFormat = namedtuple('OgrFormat', ['name', 'read', 'write'])
    format_list = []
    for line in shell_command.get_result_output().splitlines():
        re_match = format_re.match(line)
        if re_match is not None:
            read = False
            write = False
            if re_match.group('r') is not None:
                read = True
            elif re_match.group('w') is not None:
                write = True
            elif re_match.group('rw') is not None:
                read = True
                write = True
            format_list.append(OgrFormat(re_match.group('name'), read, write))

    return format_list

blub = get_supported_formats()
