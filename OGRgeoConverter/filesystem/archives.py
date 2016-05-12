'''
Handles archive files like zip.
Currently zip and tar are supported.
'''

import os
import zipfile
import tarfile


def is_archive_file(file_path):
    if zipfile.is_zipfile(file_path):
        return True
    elif tarfile.is_tarfile(file_path):
        return True

    return False


def is_archive_file_extension(file_extension):
    if file_extension.lower() == 'zip':
        return True
    elif file_extension.lower() == 'tar':
        return True

    return False


def unpack_archive_file(source_file_path, destination_folder_path):
    if zipfile.is_zipfile(source_file_path):
        unpack_zip_archive_file(source_file_path, destination_folder_path)
    elif tarfile.is_tarfile(source_file_path):
        unpack_tar_archive_file(source_file_path, destination_folder_path)


def unpack_zip_archive_file(source_file_path, destination_folder_path):
    source_zip = zipfile.ZipFile(source_file_path, 'r')
    source_zip.extractall(destination_folder_path)


def unpack_tar_archive_file(source_file_path, destination_folder_path):
    source_tar = tarfile.TarFile(source_file_path, 'r')
    source_tar.extractall(destination_folder_path)


def create_zip_archive(folder_path, zip_file_path):
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for folder_name in dirs:
            source_full_path = os.path.join(root, folder_name)
            destination_short_path = source_full_path.replace(
                folder_path,
                '').lstrip('/\\')
            file_list.append((source_full_path, destination_short_path))
        for file_name in files:
            source_full_path = os.path.join(root, file_name)
            destination_short_path = source_full_path.replace(
                folder_path,
                '').lstrip('/\\')
            file_list.append((source_full_path, destination_short_path))

    target_zip = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
    for source, destination in file_list:
        target_zip.write(source, destination)
    target_zip.close()
