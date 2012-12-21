import os

print 'Warning: The OGR formats configuration will be lost!'
answer = raw_input('Do you want to continue? (yes/no): ')
if answer == 'yes':
    print ''
    print 'Removing ogrgeoconverter.sqlite ...'
    if os.path.exists('./OGRgeoConverter/ogrgeoconverter.sqlite'):
        os.remove('./OGRgeoConverter/ogrgeoconverter.sqlite')
    
    print 'Creating ogrgeoconverter.sqlite ...'
    os.system('python manage.py syncdb --database=ogrgeoconverter_db')
    
    print 'Loading fixture ogr_formats.json ...'
    os.system('python manage.py loaddata ogr_formats.json --database=ogrgeoconverter_db')
