from OGRgeoConverter.models import LogEntry
from OGRgeoConverter.models import OGRlogEntry
from OGRgeoConverter.geoconverter import datetimehandler


class LogHandler:

    '''
    Class to read and write log entries.
    '''

    def __init__(self, job_identifier):
        if job_identifier is not None:
            self.__job_identifier = job_identifier
        else:
            raise Exception("job_identifier may not be None")

    def __get_log_entry_query_set(self):
        log_entries = LogEntry.get_log_entry(
            self.__job_identifier.session_key,
            self.__job_identifier.job_id)

        if len(log_entries) == 0:
            # Creat log entry if it doesen't exist yet
            log_entry = LogEntry()
            log_entry.session_key = self.__job_identifier.session_key
            log_entry.job_id = self.__job_identifier.job_id
            log_entry.client_job_token = self.__job_identifier.client_job_token
            log_entry.start_time = datetimehandler.get_default_datetime()
            log_entry.end_time = datetimehandler.get_default_datetime()
            log_entry.download_file_size = -1
            log_entry.save()
            log_entries = LogEntry.get_log_entry(
                self.__job_identifier.session_key,
                self.__job_identifier.job_id)

        if len(log_entries) == 1:
            return log_entries
        else:
            raise Exception("Number of found log_entries must be 1")

    def __get_ogr_log_entry_query_set(self):
        return OGRlogEntry.get_ogr_log_entry(
            self.__get_log_entry_query_set()[0])

    def get_job_identifier(self):
        return self.__job_identifier

    def set_client_ip(self, client_ip):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(client_ip=client_ip)

    def get_client_ip(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].client_ip

    def set_client_language(self, client_language):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(client_language=client_language)

    def get_client_language(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].client_language

    def set_client_user_agent(self, client_user_agent):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(client_user_agent=client_user_agent)

    def get_client_user_agent(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].client_user_agent

    def set_input_type(self, input_type):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(input_type=input_type)

    def get_input_type(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].input_type

    def set_start_time(self):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(start_time=datetimehandler.get_now())

    def get_start_time(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].start_time

    def set_end_time(self):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(end_time=datetimehandler.get_now())

    def get_end_time(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].end_time

    def set_export_format_name(self, export_format):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(export_format=export_format)

    def get_export_format_name(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].export_format

    def set_source_srs(self, source_srs):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(source_srs=source_srs)

    def get_source_srs(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].source_srs

    def set_target_srs(self, target_srs):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(target_srs=target_srs)

    def get_target_srs(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].target_srs

    def set_simplify_parameter(self, simplify_parameter):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(simplify_parameter=simplify_parameter)

    def get_simplify_parameter(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].simplify_parameter

    def set_download_file_size(self, file_size):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(download_file_size=file_size)

    def get_download_file_size(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].download_file_size

    def set_file_downloaded(self):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(file_downloaded=True)

    def get_file_downloaded(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].file_downloaded

    def set_has_download_file(self, has_download_file):
        log_entry = self.__get_log_entry_query_set()
        log_entry.update(has_download_file=has_download_file)

    def get_has_download_file(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].has_download_file

    def set_all_files_converted(self):
        all_files_converted = True
        for ogr_log_entry in self.__get_ogr_log_entry_query_set():
            if not ogr_log_entry.has_output_file:
                all_files_converted = False
                break
        all_files_converted = all_files_converted and len(
            self.__get_ogr_log_entry_query_set()) > 0

        log_entry = self.__get_log_entry_query_set()
        log_entry.update(all_files_converted=all_files_converted)

    def get_all_files_converted(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].all_files_converted

    def set_has_no_error(self):
        has_no_error = True
        for ogr_log_entry in self.__get_ogr_log_entry_query_set():
            if ogr_log_entry.error_message != '':
                has_no_error = False
                break
        has_no_error = has_no_error and len(
            self.__get_ogr_log_entry_query_set()) > 0

        log_entry = self.__get_log_entry_query_set()
        log_entry.update(has_no_error=has_no_error)

    def get_has_no_error(self):
        log_entry = self.__get_log_entry_query_set()
        return log_entry[0].has_no_error

    def add_ogr_log_entry(
            self,
            sub_path,
            input_string,
            ogr_command,
            ogr_error_message,
            has_output_file):
        command_max_length = OGRlogEntry._meta.get_field('command').max_length
        if len(ogr_command) > command_max_length:
            ogr_command = ogr_command[0:command_max_length - 7] + ' [...]'

        error_message_max_length = OGRlogEntry._meta.get_field(
            'error_message').max_length
        if len(ogr_error_message) > error_message_max_length:
            split_position1 = error_message_max_length // 3 * 2 - 10
            split_position2 = error_message_max_length - split_position1 - 20
            ogr_error_message = ogr_error_message[
                0:split_position1] + '...\n\n[...]\n\n...' + ogr_error_message[-split_position2:]

        log_entry = self.__get_log_entry_query_set()[0]

        ogr_log_entry = OGRlogEntry()
        ogr_log_entry.log_entry = log_entry
        ogr_log_entry.sub_path = sub_path
        ogr_log_entry.input = input_string
        ogr_log_entry.command = ogr_command
        ogr_log_entry.error_message = ogr_error_message
        ogr_log_entry.has_output_file = has_output_file
        ogr_log_entry.save()

    def get_ogr_log_entries(self):
        return self.__get_ogr_log_entry_query_set()
