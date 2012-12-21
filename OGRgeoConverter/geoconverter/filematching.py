'''
Matches files belonging together.
Example match for shapefile: file1.shp, file1.shx, file1.dbf
'''

import os
from collections import namedtuple
from OGRgeoConverter.models import OgrFormat, AdditionalOgrFormat
from OGRgeoConverter.filesystem import archives

class FileMatcher:
    '''
    Saves a list of files by an ID and returns files being matched
    '''
    
    def __init__(self, file_dict):
        self.__file_dict = file_dict
        self.__file_matches = _get_matches_from_file_list(self.__file_dict)
        
    def get_file_name(self, file_id):
        file_match = self.get_match(file_id)
        if file_match != None:
            return file_match.get_file_dict()[file_id]
        else:
            return self.__file_dict[file_id]
    
    def get_match(self, file_id):
        for file_match in self.__file_matches:
            if file_id in file_match.get_file_dict():
                return file_match
        return None
    
    def get_matches(self):
        return self.__file_matches


class FileMatch:
    '''
    Represents a single match of files belonging together
    '''
    
    def __init__(self, file_dict, file_list, ogr_format, is_archive, is_valid):
        self.__file_dict = file_dict
        self.__matched_file_list = file_list
        self.__ogr_format = ogr_format
        self.__is_archive = is_archive
        self.__is_valid = is_valid
        print 'Match: ' + ', '.join(file_list)

    def get_file_dict(self):
        return self.__file_dict
    
    def get_files(self):
        return self.__matched_file_list
    
    def get_ogr_format(self):
        return self.__ogr_format
    
    def is_archive(self):
        return self.__is_archive
    
    def is_valid(self):
        return self.__is_valid
    

def _get_matches_from_file_list(file_dict):
    '''
    Does the actual file matching based on the format information set in the Django admin.
    Takes a file dictionary as argument and returns a list of FileMatch objects.
    '''
    if len(file_dict) == 0:
        return []
    else:
        formats = OgrFormat.get_formats_information_dictionary()
        matches = []
        
        ogr_format_files, additional_format_files, archive_formats, unknown_format_files = _get_extended_file_lists(file_dict)

        for file_info in ogr_format_files:
            is_valid = True
            matched_files_dict = {file_info.file_id: file_info.full_name}
            matched_files_list = [file_info.full_name]
            for additional_format in formats[file_info.format_name].additional_files:
                limit_reached = False
                for additional_file_info in additional_format_files:
                    if not limit_reached and additional_file_info.file_extension.lower() == additional_format.file_extension.lower() and additional_file_info.file_name == file_info.file_name:
                        matched_files_dict[additional_file_info.file_id] = additional_file_info.full_name
                        
                        matched_files_list.append(additional_file_info.full_name)
                        if not additional_format.is_multiple:
                            limit_reached = True
                            
            matches.append(FileMatch(matched_files_dict, matched_files_list, file_info.format_name, False, is_valid))
            
        for file_info in archive_formats:
            matches.append(FileMatch({file_info.file_id: file_info.full_name}, [file_info.full_name], file_info.format_name, True, True))
            
        for file_info in unknown_format_files:
            matches.append(FileMatch({file_info.file_id: file_info.full_name}, [file_info.full_name], file_info.format_name, False, False))
        
        return matches
    

ExtendedFileList = namedtuple('ExtendedFileList', ['file_id', 'full_name', 'file_name', 'file_extension', 'is_archive', 'format_name'])

def _get_extended_file_lists(file_dict):
    '''
    Adds additional information to a file dictionary like the format name and OGR or wheter it is an archive file
    '''
    
    ogr_format_files = []
    additional_format_files = []
    archive_formats = []
    unknown_format_files = []
    
    for file_id, full_name in file_dict.items():
        file_name = os.path.splitext(full_name)[0]
        file_extension = os.path.splitext(full_name)[1].lstrip(os.path.extsep)
        
        format_name = OgrFormat.get_ogr_name_by_file_extension(file_extension)
        is_archive = archives.is_archive_file_extension(file_extension)
        extended_list = ExtendedFileList(file_id, full_name, file_name, file_extension, is_archive, format_name)
        
        if OgrFormat.contains_extension(file_extension):
            ogr_format_files.append(extended_list)
        elif AdditionalOgrFormat.contains_extension(file_extension):
            additional_format_files.append(extended_list)
        elif archives.is_archive_file_extension(file_extension):
            archive_formats.append(extended_list)
        else:
            unknown_format_files.append(extended_list)

    return ogr_format_files, additional_format_files, archive_formats, unknown_format_files


