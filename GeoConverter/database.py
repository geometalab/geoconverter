class DatabaseRouter(object):

    '''
    These functions are called when Django accesses the database.
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
        allow = False
        if db == 'default':
            allow = model._meta.app_label != 'OGRgeoConverter'
            allow = allow and model._meta.app_label != 'sessions'
        elif db == 'sessions_db':
            allow = model._meta.app_label == 'sessions'
        elif db == 'ogrgeoconverter_db':
            allow = model._meta.db_table != 'ogrgeoconverter_log_entries'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_ogr_log_entries'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_jobs'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_folders'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_file_matches'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_files'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_file_id_tracking'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_urls'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_shell_parameters'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_download_items'
            allow = allow and model._meta.db_table != 'ogrgeoconverter_conversion_job_identification'
            allow = allow and model._meta.app_label == 'OGRgeoConverter'
        elif db == 'ogrgeoconverter_conversion_jobs_db':
            allow = model._meta.db_table == 'ogrgeoconverter_conversion_jobs'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_folders'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_file_matches'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_files'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_file_id_tracking'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_urls'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_shell_parameters'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_download_items'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_conversion_job_identification'
            allow = allow and model._meta.app_label == 'OGRgeoConverter'
        elif db == 'ogrgeoconverter_log_db':
            allow = model._meta.db_table == 'ogrgeoconverter_log_entries'
            allow = allow or model._meta.db_table == 'ogrgeoconverter_ogr_log_entries'
            allow = allow and model._meta.app_label == 'OGRgeoConverter'
        else:
            allow = None

        return allow

    def __db_for_read_and_write(self, model, **hints):
        if model._meta.app_label == 'sessions':
            return 'sessions_db'
        elif model._meta.app_label == 'OGRgeoConverter':
            if model._meta.db_table == 'ogrgeoconverter_log_entries' \
                    or model._meta.db_table == 'ogrgeoconverter_ogr_log_entries':
                return 'ogrgeoconverter_log_db'
            elif model._meta.db_table == 'ogrgeoconverter_conversion_jobs' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_folders' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_file_matches' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_files' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_file_id_tracking' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_urls' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_shell_parameters' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_download_items' \
                    or model._meta.db_table == 'ogrgeoconverter_conversion_job_identification':
                return 'ogrgeoconverter_conversion_jobs_db'
            else:
                return 'ogrgeoconverter_db'

        return None
