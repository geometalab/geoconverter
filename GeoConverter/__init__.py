import codecs
import re

__version__ = '1.0.0.dev'
__date__ = 'May 11, 2016'


def get_metadata(filepath=__file__):
    with codecs.open(filepath, encoding='utf8') as version_file:
        return dict(
            re.findall(
                r"""__([a-z]+)__\s*=\s*["']([^"']+)""",
                version_file.read()))
