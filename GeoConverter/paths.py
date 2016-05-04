'''
Functions returning absolute paths to important files and folders.
For example: root path, database file, template folder
'''

import os
from OGRgeoConverter import paths as ogrgeoconverter_paths


def site_root():
    # /
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def manage_py_paht():
    # /manage.py
    return os.path.join(site_root(), 'manage.py')


def template_path():
    # /templates/
    return os.path.join(site_root(), 'templates')


def default_database_path():
    # /default.sqlite
    return os.path.join(site_root(), 'default.sqlite')


def sessions_database_path():
    # /sessions.sqlite
    return os.path.join(site_root(), 'sessions.sqlite')


def ogrgeoconverter_database_path():
    # /OGRgeoConverter/ogrgeoconverter.sqlite
    return ogrgeoconverter_paths.default_database_path()


def ogrgeoconverter_log_database_path():
    # /OGRgeoConverter/log.sqlite
    return ogrgeoconverter_paths.log_database_path()


def ogrgeoconverter_conversion_jobs_database_path():
    # /OGRgeoConverter/conversion_jobs.sqlite
    return ogrgeoconverter_paths.conversion_jobs_database_path()


def static_files_path():
    # /static/
    return os.path.join(site_root(), 'static')


def django_root():
    # Path to Django installation/ libraries
    # In Windows for example: C:\Python27\Lib\site-packages\django\
    import django
    return os.path.dirname(django.__file__)


def static_admin_files_path():
    # Path to static files needed for Django admin site
    # In Windows for example:
    # C:\Python27\Lib\site-packages\django\contrib\admin\static\admin
    return os.path.join(django_root(), 'contrib/admin/static/admin')
