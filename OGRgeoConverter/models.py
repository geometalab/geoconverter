# -*- coding: utf-8 -*-
import time
from collections import namedtuple
from django.db import models
from OGRgeoConverter.ogr import ogrinfo

def get_ogr_formats_tuple():
    supported_formats = ogrinfo.get_supported_formats()
    format_list = []
    
    for ogr_format in supported_formats:
        name = ogr_format.name
        if ogr_format.write == False:
            name += ' (readonly)'
        format_list.append((ogr_format.name, name))
        
    return format_list


OgrFormatInformation = namedtuple('OgrFormatInformation', ['name', 'ogr_name', 'extension', 'is_folder', 'state_all_files', 'additional_files', 'additional_arguments'])
AdditionalOgrFormatInformation = namedtuple('AdditionalOgrFormatInformation', ['file_extension', 'is_required', 'is_multiple'])
AdditionalShellParameterInformation = namedtuple('AdditionalShellParameterInformation', ['prefix', 'argument_name', 'argument_value', 'value_quotation_marks'])

class OgrFormat(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Name', help_text='Name des Formats, wie er auf der Webseite angezeigt werden soll.')
    ogr_name = models.CharField(max_length=100, verbose_name='OGR-Name', help_text='Der von OGR verwendete Name.', choices=get_ogr_formats_tuple())
    file_extension = models.CharField(max_length=100, unique=True, verbose_name='Dateiendung', help_text='Die Dateiendung des Formats. Beispiel: gpx (ohne Punkt am Anfang!)')
    output_type = models.CharField(max_length = 100, verbose_name='Ausgabetyp', help_text='Ausgabe dieses OGR-Formats in eine Datei (meistens) oder Ordner (z.B. bei ESRI Shapefile).', choices=(('file','Datei'),('folder','Ordner')), default='file')
    state_all_files = models.BooleanField(verbose_name='Zusätzliche Dateien mit Komma getrennt angeben', help_text='Hat einen Einfluss auf Befehl im Terminal. Ist die Option aktiviert, sieht der Befehl z.B. so aus: ogr2ogr ... "input.itf,model.ili".')
    
    def __unicode__(self):
        return self.name
    
    def is_readable(self):
        supported_formats = ogrinfo.get_supported_formats()

        for ogr_format in supported_formats:
            if ogr_format.name == self.ogr_name and ogr_format.read:
                return True
        
        return False
    
    def is_writeable(self):
        supported_formats = ogrinfo.get_supported_formats()

        for ogr_format in supported_formats:
            if ogr_format.name == self.ogr_name and ogr_format.write:
                return True
        
        return False
    
    class Meta:
        verbose_name = 'OGR format'
        verbose_name_plural = 'OGR formats'

    @staticmethod
    def get_formats_information_dictionary():
        formats_information = {}
        
        for ogr_format in OgrFormat.objects.all():
            name = ogr_format.name
            ogr_name = ogr_format.ogr_name
            extension = ogr_format.file_extension
            is_folder = ogr_format.output_type == 'folder'
            state_all_files = ogr_format.state_all_files
            formats_information[name] = OgrFormatInformation(name, ogr_name, extension, is_folder, state_all_files, [], [])
    
        for additional_ogr_format in AdditionalOgrFormat.objects.all():
            file_extension = additional_ogr_format.file_extension
            is_required = additional_ogr_format.required
            is_multiple = additional_ogr_format.multiple
            formats_information[additional_ogr_format.ogr_format.name].additional_files.append(AdditionalOgrFormatInformation(file_extension, is_required, is_multiple))
    
        for additional_shell_parameter in AdditionalShellParameter.objects.all():
            prefix = additional_shell_parameter.prefix
            argument_name = additional_shell_parameter.argument_name
            argument_value = additional_shell_parameter.argument_value
            value_quotation_marks = additional_shell_parameter.value_quotation_marks
            formats_information[additional_shell_parameter.ogr_format.name].additional_arguments.append(AdditionalShellParameterInformation(prefix, argument_name, argument_value, value_quotation_marks))
        
        return formats_information
    
    @staticmethod
    def get_format_information_by_name(ogr_format):
        format_dictionary = OgrFormat.get_formats_information_dictionary()
        if ogr_format in format_dictionary:
            return format_dictionary[ogr_format]
        else:
            return None
    
    @staticmethod
    def get_ogr_name_by_file_extension(file_extension):
        for ogr_format in OgrFormat.objects.all():
            if ogr_format.file_extension.lower() == file_extension.lower():
                return ogr_format.name
        return ''

    @staticmethod
    def contains_extension(file_extension):
        return OgrFormat.get_ogr_name_by_file_extension(file_extension) != ''
    

class AdditionalOgrFormat(models.Model):
    ogr_format = models.ForeignKey(OgrFormat)
    
    file_extension = models.CharField(max_length=100, verbose_name='Dateiendung')
    required = models.BooleanField(verbose_name='Benötigt')
    multiple = models.BooleanField(verbose_name='Mehrere Dateien möglich')
    
    order = models.IntegerField(blank = True, null = True)
    
    def __unicode__(self):
        return self.file_extension
    
    class Meta:
        ordering = ('order',)
        verbose_name = 'Additional file'
        verbose_name_plural = 'Additional files'
        
    @staticmethod
    def contains_extension(extension_name):
        contained = False
        for additional_ogr_format in AdditionalOgrFormat.objects.all():
            if additional_ogr_format.file_extension.lower() == extension_name.lower():
                contained = True
        return contained


class AdditionalShellParameter(models.Model):
    ogr_format = models.ForeignKey(OgrFormat)        

    prefix = models.CharField(max_length=10, verbose_name='Argument-Präfix', default="-")
    argument_name = models.CharField(max_length=100, verbose_name='Argument-Name')
    argument_value = models.CharField(max_length=100, verbose_name='Argument-Wert')
    value_quotation_marks = models.BooleanField(verbose_name='Anführungszeichen für Wert', default=True)

class ConversionResult(models.Model):
    pass


class LogEntry(models.Model):
    input_type = models.CharField(max_length=50, verbose_name='Eingabetyp', choices=(('files','Dateien'),('webservice','Webservice')))
    start_time = models.DateTimeField(verbose_name='Startzeit')
    end_time = models.DateTimeField(verbose_name='Endzeit')
    export_format = models.CharField(max_length=100)
    source_srs = models.CharField(max_length=100)
    target_srs = models.CharField(max_length=100)
    simplify_parameter = models.CharField(max_length=100)
    download_file_size = models.IntegerField(verbose_name='Downloadgrösse (KB)')
    
    def __unicode__(self):
        return str(self.start_time)
    
    def duration(self):
        difference = self.end_time - self.start_time
        return str(difference)
        
    class Meta:
        db_table = 'ogrgeoconverter_log'