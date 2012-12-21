class DatabaseRouter(object):
    '''
    These functions are always called when Django accesses the database.
    Returns the name of the database to use depending on the app and model.
    Returning None means use default.
    '''
    
    def db_for_read(self, model, **hints):
        return self.__db_for_read_and_write(model, **hints)

    def db_for_write(self, model, **hints):
        return self.__db_for_read_and_write(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        '''
        Makes sure the correct databases are used when "python manage.py syncdb" is called.
        Returning True means "model" should be synchronised with "db".
        '''
        if db == 'default':
            return model._meta.app_label != 'OGRgeoConverter' and model._meta.app_label != 'sessions'
        elif db == 'sessions_db':
            return model._meta.app_label == 'sessions'
        elif db == 'ogrgeoconverter_db':
            return model._meta.app_label == 'OGRgeoConverter' and model._meta.db_table != 'ogrgeoconverter_log'
        elif db == 'ogrgeoconverter_log_db':
            return model._meta.app_label == 'OGRgeoConverter' and model._meta.db_table == 'ogrgeoconverter_log'
            
        return None
    
    def __db_for_read_and_write(self, model, **hints):
        if model._meta.app_label == 'sessions':
            return 'sessions_db'
        elif model._meta.app_label == 'OGRgeoConverter':
            if model._meta.db_table == 'ogrgeoconverter_log':
                return 'ogrgeoconverter_log_db'
            else:
                return 'ogrgeoconverter_db'
                
        return None