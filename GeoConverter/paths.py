'''
Functions returning absolute paths to important files and folders.
For example: root path, database file, template folder
'''

import os
from OGRgeoConverter import paths as ogrgeoconverter_paths

def site_root():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def manage_py_paht():
    return os.path.join(site_root(), 'manage.py') 

def template_path():
    return os.path.join(site_root(), 'templates')

def default_database_path():
    return os.path.join(site_root(), 'default.sqlite')

def sessions_database_path():
    return os.path.join(site_root(), 'sessions.sqlite')

def ogrgeoconverter_database_path():
    return os.path.join(ogrgeoconverter_paths.application_root(), 'ogrgeoconverter.sqlite')

def ogrgeoconverter_log_database_path():
    return os.path.join(ogrgeoconverter_paths.application_root(), 'log.sqlite')

def static_files_path():
    return os.path.join(site_root(), 'static')

def django_root():
    import django
    return os.path.dirname(django.__file__)

def static_admin_files_path():
    return os.path.join(django_root(), 'contrib/admin/static/admin')