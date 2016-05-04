# -*- coding: utf-8 -*-
from collections import namedtuple
from django.db import models
from OGRgeoConverter.tools import ogrinfo


#################################################
# Abstract Models                               #
#################################################

class ShellParameter(models.Model):
    prefix = models.CharField(
        max_length=10,
        verbose_name='Parameter prefix',
        default='-',
        blank=True)
    parameter_name = models.CharField(max_length=100, blank=True)
    parameter_value = models.CharField(max_length=100, blank=True)
    value_quotation_marks = models.BooleanField(
        verbose_name='Value in quotation marks')

    class Meta:
        abstract = True


#################################################
# Database: ogrgeoconverter_conversion_jobs_db  #
#################################################

class JobIdentifier(models.Model):
    session_key = models.CharField(max_length=50, blank=False)
    client_job_token = models.CharField(max_length=50, blank=False)
    job_id = models.CharField(max_length=50, unique=True, blank=False)
    creation_time = models.DateTimeField()

    def __unicode__(self):
        return self.job_id

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_identification'
        unique_together = (('session_key', 'client_job_token'),)

    @staticmethod
    def get_job_identifier_by_client_job_token(session_key, client_job_token):
        return JobIdentifier.objects.filter(
            session_key=session_key,
            client_job_token=client_job_token)

    @staticmethod
    def get_job_identifier_by_job_id(session_key, job_id):
        return JobIdentifier.objects.filter(
            session_key=session_key,
            job_id=job_id)

    @staticmethod
    def cleanup_by_date(date_limit):
        JobIdentifier.objects.filter(creation_time__lt=date_limit).delete()


class ConversionJob(models.Model):
    job_identifier = models.ForeignKey(JobIdentifier)

    #export_format = models.CharField(max_length=20)
    export_format_name = models.CharField(max_length=50)
    source_srs = models.IntegerField()
    target_srs = models.IntegerField()
    simplify_parameter = models.DecimalField(max_digits=16, decimal_places=10)

    upload_folder_path = models.CharField(max_length=128)
    extract_folder_path = models.CharField(max_length=128)
    output_folder_path = models.CharField(max_length=128)
    download_folder_path = models.CharField(max_length=128)

    class Meta:
        db_table = 'ogrgeoconverter_conversion_jobs'

    @staticmethod
    def get_conversion_job(job_identifier):
        return ConversionJob.objects.filter(job_identifier=job_identifier)


class ConversionJobFolder(models.Model):
    conversion_job = models.ForeignKey(ConversionJob)

    folder_path = models.CharField(max_length=1024)

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_folders'
        unique_together = (('conversion_job', 'folder_path'),)

    @staticmethod
    def get_conversion_job_folders(conversion_job):
        return ConversionJobFolder.objects.filter(
            conversion_job=conversion_job)

    @staticmethod
    def get_conversion_job_folder_by_path(conversion_job, folder_path):
        return ConversionJobFolder.objects.filter(
            conversion_job=conversion_job,
            folder_path=folder_path)


class ConversionJobFileMatch(models.Model):
    conversion_job_folder = models.ForeignKey(ConversionJobFolder)

    identified_format_name = models.CharField(max_length=50)
    is_archive = models.BooleanField()
    is_valid = models.BooleanField()
    in_process_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_file_matches'


class ConversionJobFile(models.Model):
    conversion_job = models.ForeignKey(ConversionJob)
    file_match = models.ForeignKey(ConversionJobFileMatch)

    file_id = models.CharField(max_length=50)
    file_name = models.CharField(max_length=1024)
    matched_file_name = models.CharField(max_length=1024)
    is_uploaded = models.BooleanField()
    is_processed = models.BooleanField()
    is_removed = models.BooleanField()

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_files'
        unique_together = (('conversion_job', 'file_id'),)

    @staticmethod
    def get_conversion_job_files_by_conversion_job(conversion_job):
        return ConversionJobFile.objects.filter(conversion_job=conversion_job)

    @staticmethod
    def get_conversion_job_files_by_file_match(file_match):
        return ConversionJobFile.objects.filter(file_match=file_match)


class ConversionJobFileIdTracker(models.Model):
    conversion_job = models.ForeignKey(ConversionJob)
    file_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_file_id_tracking'


class ConversionJobUrl(models.Model):
    conversion_job = models.ForeignKey(ConversionJob)

    url_id = models.CharField(max_length=50)
    url = models.CharField(max_length=2048)
    is_processed = models.BooleanField()
    is_removed = models.BooleanField()

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_urls'

    @staticmethod
    def get_conversion_job_urls(conversion_job):
        return ConversionJobUrl.objects.filter(conversion_job=conversion_job)


class ConversionJobShellParameter(ShellParameter):
    conversion_job = models.ForeignKey(ConversionJob)

    class Meta(ShellParameter.Meta):
        db_table = 'ogrgeoconverter_conversion_job_shell_parameters'
        unique_together = (
            ('conversion_job',
             'parameter_name',
             'parameter_value'),
        )

    @staticmethod
    def get_conversion_job_shell_parameters(conversion_job):
        return ConversionJobShellParameter.objects.filter(
            conversion_job=conversion_job)


#################################################
# Database: ogrgeoconverter_db                  #
#################################################

OgrFormatInformation = namedtuple(
    'OgrFormatInformation',
    ['name', 'ogr_name', 'extension', 'is_folder', 'state_all_files',
     'additional_files', 'additional_parameters'])
AdditionalOgrFormatInformation = namedtuple(
    'AdditionalOgrFormatInformation',
    ['file_extension', 'is_required', 'is_multiple'])
AdditionalShellParameterInformation = namedtuple(
    'AdditionalShellParameterInformation',
    ['prefix', 'parameter_name', 'parameter_value', 'value_quotation_marks',
     'use_for_reading', 'use_for_writing'])


def get_ogr_formats_tuple():
    supported_formats = ogrinfo.get_supported_formats()
    format_list = []

    for ogr_format in supported_formats:
        name = ogr_format.name
        if ogr_format.write == False:
            name += ' (readonly)'
        format_list.append((ogr_format.name, name))

    return format_list


class OgrFormat(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Name des Formats, wie er auf der Webseite angezeigt werden soll.')
    ogr_name = models.CharField(
        max_length=100,
        verbose_name='OGR name',
        help_text='Der von OGR verwendete Name.',
        choices=get_ogr_formats_tuple())
    file_extension = models.CharField(
        max_length=100,
        help_text='Die Dateiendung des Formats. Beispiel: gpx (ohne Punkt am Anfang!)')
    output_type = models.CharField(
        max_length=100,
        help_text='Ausgabe dieses OGR-Formats in eine Datei (meistens) oder Ordner (z.B. bei ESRI Shapefile).',
        choices=(('file', 'File'),
                 ('folder', 'Folder')),
        default='file')
    state_all_files = models.BooleanField(
        verbose_name='List all files, separated by commas.',
        help_text='Hat einen Einfluss auf den im Terminal ausgeführten Befehl. Ist die Option aktiviert, sieht der Befehl z.B. so aus: ogr2ogr ... "input.itf,model.ili".')
    is_export_format = models.BooleanField(
        verbose_name='Show as export format.',
        help_text='Bestimmt, ob dieses Format auf der Webseite für Besucher als Exportformat sichtbar ist.')

    def __unicode__(self):
        return self.name

    def is_active(self):
        return self.is_export_format and self.is_writeable()
    is_active.boolean = True

    def is_readable(self):
        supported_formats = ogrinfo.get_supported_formats()

        for ogr_format in supported_formats:
            if ogr_format.name == self.ogr_name and ogr_format.read:
                return True

        return False
    is_readable.boolean = True

    def is_writeable(self):
        supported_formats = ogrinfo.get_supported_formats()

        for ogr_format in supported_formats:
            if ogr_format.name == self.ogr_name and ogr_format.write:
                return True

        return False
    is_writeable.boolean = True

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
            formats_information[name] = OgrFormatInformation(
                name,
                ogr_name,
                extension,
                is_folder,
                state_all_files,
                [],
                [])

        for additional_ogr_format in AdditionalOgrFormat.objects.all():
            file_extension = additional_ogr_format.file_extension
            is_required = additional_ogr_format.required
            is_multiple = additional_ogr_format.multiple
            formats_information[
                additional_ogr_format.ogr_format.name].additional_files.append(
                AdditionalOgrFormatInformation(
                    file_extension,
                    is_required,
                    is_multiple))

        for additional_shell_parameter in OgrFormatShellParameter.objects.all():
            prefix = additional_shell_parameter.prefix
            parameter_name = additional_shell_parameter.parameter_name
            parameter_value = additional_shell_parameter.parameter_value
            value_quotation_marks = additional_shell_parameter.value_quotation_marks
            use_for_reading = additional_shell_parameter.use_for_reading
            use_for_writing = additional_shell_parameter.use_for_writing
            formats_information[
                additional_shell_parameter.ogr_format.name].additional_parameters.append(
                AdditionalShellParameterInformation(
                    prefix,
                    parameter_name,
                    parameter_value,
                    value_quotation_marks,
                    use_for_reading,
                    use_for_writing))

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

    file_extension = models.CharField(max_length=100)
    required = models.BooleanField()
    multiple = models.BooleanField(verbose_name='Allow various files')

    order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.file_extension

    class Meta:
        ordering = ('order',)
        unique_together = (('ogr_format', 'file_extension'),)
        verbose_name = 'Additional file'
        verbose_name_plural = 'Additional files'

    @staticmethod
    def contains_extension(extension_name):
        contained = False
        for additional_ogr_format in AdditionalOgrFormat.objects.all():
            if additional_ogr_format.file_extension.lower(
            ) == extension_name.lower():
                contained = True
        return contained


class OgrFormatShellParameter(ShellParameter):
    ogr_format = models.ForeignKey(OgrFormat)
    use_for_reading = models.BooleanField()
    use_for_writing = models.BooleanField(default=True)

    order = models.IntegerField(blank=True, null=True)

    class Meta(ShellParameter.Meta):
        verbose_name = 'Shell parameter'
        verbose_name_plural = 'Shell parameters'
        unique_together = (
            ('ogr_format',
             'parameter_name',
             'parameter_value'),
        )
        ordering = ('order',)


class GlobalOgrShellParameter(ShellParameter):
    is_active = models.BooleanField(default=True)

    def parameter_string(self):
        prefix = ('' if self.parameter_name == '' else self.prefix)
        value = self.__get_value_string(
            self.parameter_value,
            self.value_quotation_marks,
            self.parameter_name == '')
        parameter = prefix + self.parameter_name + value
        return parameter

    def __get_value_string(self, value, quotation_marks, value_only):
        if value == '':
            newvalue = ''
        else:
            if quotation_marks:
                newvalue = '"' + value + '"'
            else:
                newvalue = str(value)
            if not value_only:
                newvalue = ' ' + newvalue
        return newvalue

    class Meta(ShellParameter.Meta):
        verbose_name = 'Global shell parameter'
        verbose_name_plural = 'Global shell parameters'
        unique_together = (('parameter_name', 'parameter_value'),)

    @staticmethod
    def get_all_parameters():
        return GlobalOgrShellParameter.objects.all()

    @staticmethod
    def get_active_parameters():
        return GlobalOgrShellParameter.objects.filter(is_active=True)


class DownloadItem(models.Model):
    job_identifier = models.ForeignKey(JobIdentifier)

    download_caption = models.CharField(max_length=100)
    is_downloaded = models.BooleanField()

    class Meta:
        db_table = 'ogrgeoconverter_conversion_job_download_items'

    @staticmethod
    def get_download_item(job_identifier):
        return DownloadItem.objects.filter(job_identifier=job_identifier)

    @staticmethod
    def get_download_items(session_key):
        return DownloadItem.objects.filter(
            job_identifier__session_key=session_key).order_by(
            'job_identifier__creation_time').reverse()


#################################################
# Database: ogrgeoconverter_log_db              #
#################################################

class LogEntry(models.Model):
    session_key = models.CharField(max_length=50)
    job_id = models.CharField(max_length=50)

    client_job_token = models.CharField(max_length=50)
    client_ip = models.CharField(max_length=50)
    client_language = models.CharField(max_length=50)
    client_user_agent = models.CharField(max_length=256)

    input_type = models.CharField(
        max_length=50, choices=(
            ('files', 'Files'), ('webservice', 'Webservice')))
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    export_format = models.CharField(max_length=100)
    source_srs = models.CharField(max_length=100)
    target_srs = models.CharField(max_length=100)
    simplify_parameter = models.CharField(max_length=100)
    download_file_size = models.IntegerField(
        verbose_name='Download file size (KB)')

    file_downloaded = models.BooleanField()
    has_download_file = models.BooleanField()
    all_files_converted = models.BooleanField()
    has_no_error = models.BooleanField()

    def __unicode__(self):
        return str(self.start_time)

    def duration(self):
        difference = self.end_time - self.start_time
        return str(difference)

    class Meta:
        verbose_name_plural = "Log entries"
        db_table = 'ogrgeoconverter_log_entries'

    @staticmethod
    def get_log_entry(session_key, job_id):
        return LogEntry.objects.filter(session_key=session_key, job_id=job_id)


class OGRlogEntry(models.Model):
    log_entry = models.ForeignKey(LogEntry)

    sub_path = models.CharField(max_length=1000)
    input = models.CharField(max_length=5000)
    command = models.CharField(max_length=1000)
    error_message = models.CharField(max_length=10000)
    has_output_file = models.BooleanField()

    class Meta:
        verbose_name = "OGR Log entry"
        verbose_name_plural = "OGR Log entries"
        db_table = 'ogrgeoconverter_ogr_log_entries'

    @staticmethod
    def get_ogr_log_entry(log_entry):
        return OGRlogEntry.objects.filter(log_entry=log_entry)

    @staticmethod
    def cleanup_by_date(date_limit):
        OGRlogEntry.objects.filter(
            log_entry__start_time__lt=date_limit).delete()
