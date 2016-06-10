from OGRgeoConverter.models import ConversionJob
from OGRgeoConverter.models import ConversionJobFolder, ConversionJobFileMatch, ConversionJobFile, ConversionJobFileIdTracker
from OGRgeoConverter.models import ConversionJobUrl
from OGRgeoConverter.models import ConversionJobShellParameter


class JobHandler:

    '''
    Class that manages conversion jobs.
    '''

    def __init__(self, job_identifier):
        if job_identifier is not None:
            self.__job_identifier = job_identifier
        else:
            raise Exception("job_identifier may not be None")

    def __get_conversion_job_query_set(self):
        conversion_jobs = ConversionJob.get_conversion_job(
            self.__job_identifier)

        if len(conversion_jobs) == 0:
            conversion_job = ConversionJob()
            conversion_job.job_identifier = self.__job_identifier
            conversion_job.source_srs = 0
            conversion_job.target_srs = 0
            conversion_job.simplify_parameter = 0
            conversion_job.save()
            conversion_jobs = ConversionJob.get_conversion_job(
                self.__job_identifier)

        if len(conversion_jobs) == 1:
            return conversion_jobs
        else:
            raise Exception("Number of found conversion_jobs must be 1")

    def __get_conversion_job_folder_query_set(self, folder_path):
        conversion_job = self.__get_conversion_job_query_set()[0]
        conversion_job_folders = ConversionJobFolder.get_conversion_job_folder_by_path(
            conversion_job, folder_path)

        if len(conversion_job_folders) == 0:
            conversion_job_folder = ConversionJobFolder()
            conversion_job_folder.conversion_job = conversion_job
            conversion_job_folder.folder_path = folder_path
            conversion_job_folder.save()
            conversion_job_folders = ConversionJobFolder.get_conversion_job_folder_by_path(
                conversion_job, folder_path)

        if len(conversion_job_folders) == 1:
            return conversion_job_folders
        else:
            raise Exception("Number of found conversion_job_folders must be 1")

    def __get_conversion_job_files_query_set(self):
        conversion_job = self.__get_conversion_job_query_set()[0]
        conversion_job_files = ConversionJobFile.get_conversion_job_files_by_conversion_job(
            conversion_job)
        return conversion_job_files

    def __get_conversion_job_files_query_set_from_file_match(self, file_match):
        conversion_job_files = ConversionJobFile.get_conversion_job_files_by_file_match(
            file_match)
        return conversion_job_files

    def __get_conversion_job_urls_query_set(self):
        conversion_job = self.__get_conversion_job_query_set()[0]
        conversion_job_urls = ConversionJobUrl.get_conversion_job_urls(
            conversion_job)
        return conversion_job_urls

    def __get_conversion_job_shell_parameter_query_set(self):
        conversion_job = self.__get_conversion_job_query_set()[0]
        conversion_job_shell_parameters = ConversionJobShellParameter.get_conversion_job_shell_parameters(
            conversion_job)
        return conversion_job_shell_parameters

    def get_job_identifier(self):
        return self.__job_identifier

    def set_export_format_name(self, export_format_name):
        conversion_job = self.__get_conversion_job_query_set()
        conversion_job.update(export_format_name=export_format_name)

    def get_export_format_name(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].export_format_name

    def set_source_srs(self, source_srs):
        if len(source_srs) <= 8 and source_srs.isdigit():
            conversion_job = self.__get_conversion_job_query_set()
            conversion_job.update(source_srs=int(source_srs))

    def get_source_srs(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].source_srs

    def set_target_srs(self, target_srs):
        target_srs_string = str(target_srs)
        if len(target_srs_string) <= 8 and target_srs_string.isdigit():
            conversion_job = self.__get_conversion_job_query_set()
            conversion_job.update(target_srs=int(target_srs_string))

    def get_target_srs(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].target_srs

    def set_simplify_parameter(self, simplify_parameter):
        simplify_parameter_string = str(simplify_parameter)
        try:
            simplify_parameter_float = float(simplify_parameter_string)
        except ValueError:
            simplify_parameter_float = 0
        if simplify_parameter_float < 0:
            simplify_parameter_float = 0
        conversion_job = self.__get_conversion_job_query_set()
        conversion_job.update(simplify_parameter=simplify_parameter_float)

    def get_simplify_parameter(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].simplify_parameter

    def get_original_file_name(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        return file_query_set[0].file_name

    def get_file_name(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        return file_query_set[0].matched_file_name

    def add_file_match(
            self,
            source_path,
            file_dict,
            ogr_format_name,
            is_archive,
            is_valid):
        conversion_job_folder = self.__get_conversion_job_folder_query_set(
            source_path)[0]
        conversion_job_file_match = ConversionJobFileMatch()
        conversion_job_file_match.conversion_job_folder = conversion_job_folder
        conversion_job_file_match.identified_format_name = ogr_format_name
        conversion_job_file_match.is_archive = is_archive
        conversion_job_file_match.is_valid = is_valid
        conversion_job_file_match.save()
        for file_id, file_name in file_dict.items():
            conversion_job_file = ConversionJobFile()
            conversion_job_file.conversion_job = self.__get_conversion_job_query_set()[
                0]
            conversion_job_file.file_match = conversion_job_file_match
            conversion_job_file.file_id = file_id
            conversion_job_file.file_name = file_name
            conversion_job_file.matched_file_name = file_name
            conversion_job_file.save()

    def get_files(self, file_id, include_removed_files=False):
        file_query_set = self.__get_conversion_job_files_query_set()
        file_dict = {}
        for file in file_query_set:
            if not file.is_removed or include_removed_files:
                file_dict[file.file_id] = file.file_name
        return file_dict

    def get_file_count(self):
        file_query_set = self.__get_conversion_job_files_query_set()
        return len(file_query_set)

    def get_free_file_id(self):
        file_id_tracker = ConversionJobFileIdTracker()
        file_id_tracker.conversion_job = self.__get_conversion_job_query_set()[
            0]
        file_id_tracker.save()
        return "id" + str(file_id_tracker.file_id)

    def remove_file(self, file_id):
        conversion_job_file = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        conversion_job_file.update(is_removed=True)

    def file_removed(self, file_id):
        conversion_job_file = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        if not conversion_job_file:
            return True
        return conversion_job_file[0].is_removed

    def set_file_uploaded(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        file_query_set.update(is_uploaded=True)

    def file_ready_for_process(self, file_id):
        matched_files = self.get_matched_files(file_id)
        if len(matched_files) == 0:
            return False

        is_ready = True
        for matched_file in matched_files:
            if not matched_file.is_uploaded:
                is_ready = False
        return is_ready

    def filematch_try_process(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        file_match = file_query_set[0].file_match
        if file_match.in_process_id == '':
            file_match.in_process_id = file_id
            file_match.save(update_fields=('in_process_id',))
            return True
        else:
            return False

    def filematch_in_process(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        return file_query_set[0].file_match.in_process_id != ''

    def filematch_processing_id(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        return file_query_set[0].file_match.in_process_id

    def set_file_processed(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        file_query_set.update(is_processed=True)

    def get_file_processed(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        return file_query_set[0].is_processed

    def get_matched_files(self, file_id):
        file_query_set = self.__get_conversion_job_files_query_set().filter(
            file_id=file_id)
        file_match = file_query_set[0].file_match
        matched_file_query_set = self.__get_conversion_job_files_query_set_from_file_match(
            file_match)

        return list(matched_file_query_set)

    def get_unprocessed_files(self):
        unprocessed_files = []

        for file_id, processed in self.__processed_file_dict.items():
            if not processed:
                unprocessed_files.append(file_id)

        return unprocessed_files

    def add_webservice_url(self, url_id, url):
        conversion_job_url = ConversionJobUrl()
        conversion_job_url.conversion_job = self.__get_conversion_job_query_set()[
            0]
        conversion_job_url.url_id = url_id
        conversion_job_url.url = url
        conversion_job_url.save()

    def get_webservice_url(self, url_id):
        url_query_set = self.__get_conversion_job_urls_query_set().filter(
            url_id=url_id)
        if len(url_query_set) == 1:
            return url_query_set[0].url
        else:
            return ''

    def add_webservice_urls(self, url_dict):
        for url_id, url in url_dict:
            self.add_webservice_url(url_id, url)

    def get_webservice_urls(self):
        url_query_set = self.__get_conversion_job_urls_query_set()
        url_dict = {}
        for webservice_url in url_query_set:
            url_dict[webservice_url.url_id] = webservice_url.url
        return url_dict

    def get_webservice_urls_count(self):
        url_query_set = self.__get_conversion_job_urls_query_set()
        return len(url_query_set)

    def remove_webservice_url(self):
        raise Exception('Not implemented')

    def add_shell_parameter_object(self, shell_parameter):
        self.add_shell_parameter(
            shell_parameter.prefix,
            shell_parameter.parameter_name,
            shell_parameter.parameter_value,
            shell_parameter.value_quotation_marks)

    def add_shell_parameter(
            self,
            prefix,
            parameter_name,
            parameter_value,
            value_quotation_marks):
        shell_parameter = ConversionJobShellParameter()
        shell_parameter.conversion_job = self.__get_conversion_job_query_set()[
            0]
        shell_parameter.prefix = prefix
        shell_parameter.parameter_name = parameter_name
        shell_parameter.parameter_value = parameter_value
        shell_parameter.value_quotation_marks = value_quotation_marks
        shell_parameter.save()

    def get_shell_parameters(self):
        shell_parameters_query_set = self.__get_conversion_job_shell_parameter_query_set()
        shell_parameters_list = []
        for shell_parameter in shell_parameters_query_set:
            shell_parameters_list.append(shell_parameter)
        return shell_parameters_list

    def set_upload_folder_path(self, upload_folder_path):
        conversion_job = self.__get_conversion_job_query_set()
        conversion_job.update(upload_folder_path=upload_folder_path)

    def get_upload_folder_path(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].upload_folder_path

    def set_extract_folder_path(self, extract_folder_path):
        conversion_job = self.__get_conversion_job_query_set()
        conversion_job.update(extract_folder_path=extract_folder_path)

    def get_extract_folder_path(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].extract_folder_path

    def set_output_folder_path(self, output_folder_path):
        conversion_job = self.__get_conversion_job_query_set()
        conversion_job.update(output_folder_path=output_folder_path)

    def get_output_folder_path(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].output_folder_path

    def set_download_folder_path(self, download_folder_path):
        conversion_job = self.__get_conversion_job_query_set()
        conversion_job.update(download_folder_path=download_folder_path)

    def get_download_folder_path(self):
        conversion_job = self.__get_conversion_job_query_set()
        return conversion_job[0].download_folder_path
