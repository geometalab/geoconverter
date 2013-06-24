import os, shutil

print('Warning: All data will be lost!')
answer = input('Do you want to continue? (yes/no): ')
if answer == 'yes':
    print('')
    
    print('Removing old conversion files ...')
    folder_path = './OGRgeoConverter/ConversionJobFiles'
    for folder in os.listdir(folder_path):
        full_path = os.path.join(folder_path, folder)
        shutil.rmtree(full_path)
    
    print('Removing database.sqlite ...')
    if os.path.exists('default.sqlite'):
        os.remove('default.sqlite')
        
    print('Removing sessions.sqlite ...')
    if os.path.exists('sessions.sqlite'):
        os.remove('sessions.sqlite')
        
    print('Removing ogrgeoconverter.sqlite ...')
    if os.path.exists('./OGRgeoConverter/ogrgeoconverter.sqlite'):
        os.remove('./OGRgeoConverter/ogrgeoconverter.sqlite')
        
    print('Removing log.sqlite ...')
    if os.path.exists('./OGRgeoConverter/log.sqlite'):
        os.remove('./OGRgeoConverter/log.sqlite')
    
    print('Removing conversionjobs.sqlite ...')
    if os.path.exists('./OGRgeoConverter/conversionjobs.sqlite'):
        os.remove('./OGRgeoConverter/conversionjobs.sqlite')
            
    print('Creating default.sqlite ...')
    os.system('python manage.py syncdb')

    print('Creating sessions.sqlite ...')
    os.system('python manage.py syncdb --database=sessions_db')
    
    print('Creating ogrgeoconverter.sqlite ...')
    os.system('python manage.py syncdb --database=ogrgeoconverter_db')
    
    print('Creating log.sqlite ...')
    os.system('python manage.py syncdb --database=ogrgeoconverter_log_db')
    
    print('Creating conversionjobs.sqlite ...')
    os.system('python manage.py syncdb --database=ogrgeoconverter_conversion_jobs_db')
    
    print('Loading fixture ogr_formats.json ...')
    os.system('python manage.py loaddata ogr_formats.json --database=ogrgeoconverter_db')

    print('Loading fixture global_shell_parameters.json ...')
    os.system('python manage.py loaddata global_shell_parameters.json --database=ogrgeoconverter_db')
else:
    print('Action canceled')
