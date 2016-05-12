from django.contrib import admin
from OGRgeoConverter.models import OgrFormat
from OGRgeoConverter.models import AdditionalOgrFormat
from OGRgeoConverter.models import OgrFormatShellParameter
from OGRgeoConverter.models import GlobalOgrShellParameter
from OGRgeoConverter.models import LogEntry
from OGRgeoConverter.models import OGRlogEntry
from OGRgeoConverter.models import JobIdentifier
from OGRgeoConverter.models import ConversionJob
from OGRgeoConverter.models import ConversionJobFolder
from OGRgeoConverter.models import ConversionJobUrl
from OGRgeoConverter.models import ConversionJobShellParameter
from OGRgeoConverter.models import DownloadItem


class AdditionalOgrFormatInline(admin.StackedInline):
    model = AdditionalOgrFormat
    extra = 0


class AdditionalShellArgumentInline(admin.StackedInline):
    model = OgrFormatShellParameter
    extra = 0


class OgrFormatAdmin(admin.ModelAdmin):
    model = OgrFormat
    inlines = [AdditionalOgrFormatInline, AdditionalShellArgumentInline]
    list_display = (
        'name',
        'is_active',
        'is_readable',
        'is_writeable',
        'file_extension',
        'output_type')

    class Media:
        js = (
            '/static/jquery/js/jquery-1.8.2.min.js',
            '/static/jquery/js/jquery-ui-1.9.1.custom.min.js',
            '/static/django/js/admin-sort.js',
        )


class GlobalOgrShellParameterAdmin(admin.ModelAdmin):
    model = GlobalOgrShellParameter
    list_display = ('parameter_string', 'is_active')


class OGRlogEntryInline(admin.StackedInline):
    model = OGRlogEntry
    extra = 0
    readonly_fields = (
        'sub_path',
        'input',
        'command',
        'error_message',
        'has_output_file')


class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    inlines = [OGRlogEntryInline]
    readonly_fields = (
        'session_key',
        'job_id',
        'client_job_token',
        'client_ip',
        'client_language',
        'client_user_agent',
        'input_type',
        'start_time',
        'end_time',
        'export_format',
        'source_srs',
        'target_srs',
        'simplify_parameter',
        'download_file_size',
        'file_downloaded',
        'has_download_file',
        'all_files_converted',
        'has_no_error')
    list_display = (
        'start_time',
        'duration',
        'input_type',
        'export_format',
        'source_srs',
        'target_srs',
        'simplify_parameter',
        'download_file_size',
        'file_downloaded',
        'has_download_file',
        'all_files_converted',
        'has_no_error')
    list_filter = (
        'start_time',
        'input_type',
        'export_format',
        'file_downloaded',
        'has_download_file',
        'all_files_converted',
        'has_no_error')

admin.site.register(OgrFormat, OgrFormatAdmin)
admin.site.register(GlobalOgrShellParameter, GlobalOgrShellParameterAdmin)
admin.site.register(LogEntry, LogEntryAdmin)


# Temporary !!!!!
class ConversionJobFolderInline(admin.StackedInline):
    model = ConversionJobFolder
    extra = 0


class ConversionJobUrlInline(admin.StackedInline):
    model = ConversionJobUrl
    extra = 0


class ConversionJobShellParameterInline(admin.StackedInline):
    model = ConversionJobShellParameter
    extra = 0


class ConversionJobAdmin(admin.ModelAdmin):
    model = ConversionJob
    inlines = [
        ConversionJobFolderInline,
        ConversionJobUrlInline,
        ConversionJobShellParameterInline]


class DownloadItemAdmin(admin.ModelAdmin):
    model = DownloadItem
    list_display = ('job_identifier', 'download_caption', 'is_downloaded')


class ConversionJobInline(admin.StackedInline):
    model = ConversionJob
    extra = 0


class DownloadItemInline(admin.StackedInline):
    model = DownloadItem
    extra = 0


class JobIdentifierAdmin(admin.ModelAdmin):
    model = JobIdentifier
    inlines = [ConversionJobInline, DownloadItemInline]
