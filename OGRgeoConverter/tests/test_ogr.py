from django.test import TestCase
from OGRgeoConverter.ogr import ogrinfo
from OGRgeoConverter.shell.shellcall import ArgumentList
from OGRgeoConverter.shell import shell


class OgrInfoTest(TestCase):
    '''
    Tests module ogrinfo
    '''

    def test_ogrinfo_returns_shell_call_object_and_works_with_test_command(self):  
        call = ogrinfo.get_ogrinfo_shell_call()  
        arguments = ArgumentList()
        arguments.add_argument("version", None, "--")
        call.set_arguments(arguments)
        result = shell.execute(call)
        self.assertTrue(result.get_text() != "" and result.get_error() == "")

    def test_ogrinfo_returns_format_list(self):
        formats = ogrinfo.get_supported_formats()

        self.assertTrue(isinstance(formats, list))
        self.assertTrue(len(formats) > 0)
        
        
class Ogr2ogrTest(TestCase):
    '''
    Tests module ogr2ogr
    '''

    def test_x(self):
        pass