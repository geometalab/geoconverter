from django import forms
from OGRgeoConverter.models import OgrFormat


class GeoConverterFilesForm(forms.Form):
    fileupload = forms.FileField(label='File')
    files_ogrformat = forms.ChoiceField(
        widget=forms.Select,
        label='Export format')

    def __init__(self, post=None, files=None):
        forms.Form.__init__(self, post, files)
        self.fields['files_ogrformat'].choices = [
            ('', '--Choose--')] + [
            (c.name, c.name) for c in OgrFormat.objects.all().order_by('name')
            if c.is_active()]
        self.files = files
        self.post = post


class GeoConverterWebservicesForm(forms.Form):
    urlinput = forms.CharField()
    webservices_ogrformat = forms.ChoiceField(
        widget=forms.Select,
        label='Export format')

    def __init__(self, post=None, url=None):
        forms.Form.__init__(self, post, url)
        self.fields['webservices_ogrformat'].choices = [
            ('', '--Choose--')] + [
            (c.name, c.name) for c in OgrFormat.objects.all().order_by('name')
            if c.is_active()]
        self.urlinput = url
        self.post = post
