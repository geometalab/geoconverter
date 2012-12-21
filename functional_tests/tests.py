from django.test import TestCase
from OGRgeoConverter.ogr import ogrinfo

class OGRgeoConverterTest(TestCase):
    
    def test_ogr_supports_interlis(self):
        formats = ogrinfo.get_supported_formats()
        
        containsInterlis1 = False
        containsInterlis2 = False
        
        for ogrformat in formats:
            if ogrformat.name.lower() == "interlis 1":
                containsInterlis1 = True
            if ogrformat.name.lower() == "interlis 2":
                containsInterlis2 = True
        
        self.assertTrue(containsInterlis1)
        self.assertTrue(containsInterlis2)