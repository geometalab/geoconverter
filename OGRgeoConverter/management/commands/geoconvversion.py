from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from GeoConverter import settings


class Command(BaseCommand):
    help = 'Get version information'
    option_list = BaseCommand.option_list + (
        make_option(
            '--short',
            action='store_true',
            dest='short',
            default=False,
            help='Print only the numbers and nothing more'),
    )

    def handle(self, *args, **options):
        v_infostring = '{version}'
        if options['short'] is False:
            v_infostring = 'Version: {version}, Date: {date}'
        self.stdout.write(v_infostring.format(**settings.METADATA))
