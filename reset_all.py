import os

print 'Warning: All data will be lost!'
answer = raw_input('Do you want to continue? (yes/no): ')
if answer == 'yes':
    print ''
    print 'Removing database.sqlite ...'
    if os.path.exists('default.sqlite'):
        os.remove('default.sqlite')
        
    print 'Removing sessions.sqlite ...'
    if os.path.exists('sessions.sqlite'):
        os.remove('sessions.sqlite')
        
    print 'Removing ogrgeoconverter.sqlite ...'
    if os.path.exists('./OGRgeoConverter/ogrgeoconverter.sqlite'):
        os.remove('./OGRgeoConverter/ogrgeoconverter.sqlite')
        
    print 'Removing log.sqlite ...'
    if os.path.exists('./OGRgeoConverter/log.sqlite'):
        os.remove('./OGRgeoConverter/log.sqlite')
    
    print 'Removing conversion_jobs.sqlite ...'
    if os.path.exists('./OGRgeoConverter/conversion_jobs.sqlite'):
        os.remove('./OGRgeoConverter/conversion_jobs.sqlite')
            
    print 'Creating default.sqlite ...'
    os.system('python manage.py syncdb')

    print 'Creating sessions.sqlite ...'
    os.system('python manage.py syncdb --database=sessions_db')
    
    print 'Creating ogrgeoconverter.sqlite ...'
    os.system('python manage.py syncdb --database=ogrgeoconverter_db')
    
    print 'Creating log.sqlite ...'
    os.system('python manage.py syncdb --database=ogrgeoconverter_log_db')
    
    print 'Creating conversion_jobs.sqlite ...'
    os.system('python manage.py syncdb --database=ogrgeoconverter_conversion_jobs_db')
    
    print 'Loading fixture ogr_formats.json ...'
    os.system('python manage.py loaddata ogr_formats.json --database=ogrgeoconverter_db')
