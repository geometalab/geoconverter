'''
Functions returning absolute paths to important files and folders.
For example: app root path, database file, conversion jobs folder
'''

import os


def application_root():
    # /OGRgeoConverter/
    return os.path.dirname(os.path.realpath(__file__))


def default_database_path():
    # /OGRgeoConverter/ogrgeoconverter.sqlite
    return os.path.join(application_root(), 'ogrgeoconverter.sqlite')


def log_database_path():
    # /OGRgeoConverter/log.sqlite
    return os.path.join(application_root(), 'log.sqlite')


def conversion_jobs_database_path():
    # /OGRgeoConverter/conversionjobs.sqlite
    return os.path.join(application_root(), 'conversionjobs.sqlite')


def conversion_job_path():
    # /OGRgeoConverter/ConversionJobs/
    return os.path.join(application_root(), 'ConversionJobFiles')
