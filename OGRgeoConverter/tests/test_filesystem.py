import re
from django.test import TestCase
from OGRgeoConverter.filesystem import filemanager
from OGRgeoConverter.filesystem import pathcode

class FileManagerTest(TestCase):
    '''
    Tests module filemanager
    '''

    def test_filemanager_returns_folder_path_for_valid_pathcode(self):
        path_code = pathcode.get_random_pathcode()
        path = filemanager.get_folder_path(path_code)
        
        self.assertTrue(path != '')
        
    def test_filemanager_returns_output_folder_path_for_valid_pathcode(self):
        path_code = pathcode.get_random_pathcode()
        path = filemanager.get_output_folder_path(path_code)
        
        self.assertTrue(path != '')
        
    def test_filemanager_returns_download_file_path_for_valid_pathcode(self):
        path_code = pathcode.get_random_pathcode()
        path = filemanager.get_download_file_path(path_code)
        
        self.assertTrue(path != '')
    
    
class PathCodeTest(TestCase):
    '''
    Tests module pathcode
    '''

    def test_random_pathcode_not_empty(self):
        path_code = pathcode.get_random_pathcode()
        self.assertTrue(path_code != '')
        
    def test_random_pathcode_is_valid(self):
        path_code = pathcode.get_random_pathcode()
        self.assertTrue(pathcode.is_pathcode(path_code))
        
    def test_valid_pathcode_regex_is_returned(self):
        regex = pathcode.get_pathcode_regex()
        
        self.assertTrue(regex != '')
        
        # Throws error if regex not valid
        re.compile(regex)
        
    def test_valid_bounded_pathcode_regex_is_returned(self):
        regex = pathcode.get_bounded_pathcode_regex()
        
        self.assertTrue(regex != '')
        
        # Throws error if regex not valid
        re.compile(regex)
        
    def test_pathcode_gets_splitted(self):
        path_code = pathcode.get_random_pathcode()
        splitted_path_code = pathcode.split_pathcode(path_code)
        
        self.assertTrue(isinstance(splitted_path_code, list))
        self.assertTrue(len(splitted_path_code) > 1)
        
    def test_splitting_and_joining_pathcode_does_not_change_it(self):
        path_code = pathcode.get_random_pathcode()
        splitted_path_code = pathcode.split_pathcode(path_code)
        joined_path_code = pathcode.join_pathcode(*splitted_path_code)
        
        self.assertTrue(path_code == joined_path_code)
        
    def test_invalid_pathcode_ist_detected(self):
        invalid_path_code = '<invalid_path_code>'
        
        self.assertFalse(pathcode.is_pathcode(invalid_path_code))