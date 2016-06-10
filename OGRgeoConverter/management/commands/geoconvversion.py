from django.core.management.base import BaseCommand
from optparse import make_option
from GeoConverter import settings
import re

class Command(BaseCommand):
    help = 'Get version information'
    option_list = BaseCommand.option_list + (
        make_option(
            '--short',
            action='store_true',
            dest='short',
            default=False,
            help='Print only the numbers and nothing more'),
        make_option(
            '--dockertag',
            action='store_true',
            dest='dockertag',
            default=False,
            help='Print only the numbers following docker tag convention and nothing more'),
    )

    def handle(self, *args, **options):
        v_infostring = 'Version: {version}, Date: {date}'
        _version = settings.METADATA.get('version', '0.0.0')
        # pep440 formatted strings are not suitable as docker image tags, replace illegal chars
        _version = re.sub('^([^+]+)(.*)$', lambda mo: mo.group(1)+mo.group(2).replace('+','-').replace('.', '-'), _version)
        if options['short']:
            v_infostring = '{version}'
        elif options['dockertag']:
            v_infostring = '{_version}'
        self.stdout.write(v_infostring.format(_version=_version, **settings.METADATA))
