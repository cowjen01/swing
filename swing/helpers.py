import os
import re
import zipfile

url_regex = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'


def is_valid_url(url):
    return bool(re.match(url_regex, url))


def is_readable_file(path):
    return path and os.path.isfile(path) and os.access(path, os.R_OK)


def is_readable_dir(path):
    return path and os.path.isdir(path) and os.access(path, os.R_OK)


def get_archive_filename(chart_name, version):
    return f'{chart_name}-{version}.zip'


def get_current_dir():
    return os.getcwd()


def create_directory(path):
    if path and not os.path.exists(path):
        os.makedirs(path)


def get_yaml_filename(directory, name):
    yaml_path = os.path.join(directory, f'{name}.yaml')
    yml_path = os.path.join(directory, f'{name}.yml')

    if is_readable_file(yaml_path):
        return yaml_path
    elif is_readable_file(yml_path):
        return yml_path
    
    return None


def zip_folder(dir_path, dst_path):
    zip_file = zipfile.ZipFile(dst_path, 'w')
    
    for dirname, subdirs, files in os.walk(dir_path):
        zip_file.write(dirname)
        for filename in files:
            zip_file.write(os.path.join(dirname, filename))
    
    zip_file.close()
