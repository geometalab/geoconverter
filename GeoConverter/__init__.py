from ._version import get_versions
__version__ = get_versions()['version']
__date__ = get_versions()['date']


def get_metadata():
    return get_versions()

