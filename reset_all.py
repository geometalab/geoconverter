#!/usr/bin/env python

import os, sys, shutil

dbname_option_tuples = [
    ('default.sqlite', ''),
    ('sessions.sqlite', '--database=sessions_db'),
    ('OGRgeoConverter/ogrgeoconverter.sqlite', '--database=ogrgeoconverter_db'),
    ('OGRgeoConverter/log.sqlite', '--database=ogrgeoconverter_log_db'),
    ('OGRgeoConverter/conversionjobs.sqlite', '--database=ogrgeoconverter_conversion_jobs_db'),
]

print('Warning: All data will be lost!')
answer = input('Do you want to continue with cleanup? (yes/no): ')
if answer == 'yes':
    print('\nRemoving old conversion files ...')
    try:
        folder_path = './OGRgeoConverter/ConversionJobFiles'
        for folder in os.listdir(folder_path):
            full_path = os.path.join(folder_path, folder)
            shutil.rmtree(full_path)
    except: pass

    for dbname,option in dbname_option_tuples:
        print('Removing', dbname, '...')
        if os.path.exists(dbname):
            os.remove(dbname)
 
print('\nSetup new environment:')
answer = input('Do you want to setup now? (yes/no): ')
if answer == 'yes':
    print('\n')
    for dbname,option in dbname_option_tuples:
        print('Creating', dbname, '...')
        os.system(' '.join(['python manage.py syncdb',option]))
 
    print('Loading fixture ogr_formats.json ...')
    os.system('python manage.py loaddata ogr_formats.json --database=ogrgeoconverter_db')

    print('Loading fixture global_shell_parameters.json ...')
    os.system('python manage.py loaddata global_shell_parameters.json --database=ogrgeoconverter_db')
else:
    print('Action canceled')
