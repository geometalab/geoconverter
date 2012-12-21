from django.contrib import admin
from OGRgeoConverter.models import OgrFormat
from OGRgeoConverter.models import AdditionalOgrFormat
from OGRgeoConverter.models import AdditionalShellParameter
from OGRgeoConverter.models import LogEntry

class AdditionalOgrFormatInline(admin.StackedInline):
    model = AdditionalOgrFormat
    extra = 0

class AdditionalShellArgumentInline(admin.StackedInline):
    model = AdditionalShellParameter
    extra = 0

class OgrFormatAdmin(admin.ModelAdmin):
    model = OgrFormat
    inlines = [AdditionalOgrFormatInline, AdditionalShellArgumentInline]
    list_display = ('name', 'is_readable', 'is_writeable')
    
    class Media:
        js = (
            '/static/jquery/js/jquery-1.8.2.min.js',
            '/static/jquery/js/jquery-ui-1.9.1.custom.min.js',
            '/static/django/js/geofiles-sort.js',
        )
    
admin.site.register(OgrFormat, OgrFormatAdmin)
admin.site.register(LogEntry)