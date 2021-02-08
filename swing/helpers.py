import os
import re
import shutil
import zipfile
from datetime import datetime
from io import BytesIO

url_regex = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'


def is_valid_url(url):
    return bool(re.match(url_regex, url))


def is_readable_file(path):
    return path and os.path.isfile(path) and os.access(path, os.R_OK)


def is_readable_dir(path):
    return path and os.path.isdir(path) and os.access(path, os.R_OK)


def get_current_dir():
    return os.getcwd()


def create_directory(path):
    if path and not os.path.exists(path):
        os.makedirs(path)


def remove_directory(path):
    if path and os.path.exists(path):
        shutil.rmtree(path)


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def get_yaml_filename(directory, name):
    yaml_path = os.path.join(directory, f'{name}.yaml')
    yml_path = os.path.join(directory, f'{name}.yml')

    if is_readable_file(yaml_path):
        return f'{name}.yaml'
    elif is_readable_file(yml_path):
        return f'{name}.yml'

    return None


def format_date(date_string):
    fmt = '%a, %d %b %Y %H:%M:%S %Z'
    date = datetime.strptime(date_string, fmt)
    return date.strftime('%m/%d/%y')


def get_archive_filename(chart_name, version):
    return f'{chart_name}-{version}.zip'


def zip_chart_folder(dir_path):
    archive = BytesIO()

    with zipfile.ZipFile(archive, 'w') as zip_archive:
        relroot = os.path.abspath(os.path.join(dir_path))
        for dirname, subdirs, files in os.walk(dir_path):
            for file in files:
                filename = os.path.join(dirname, file)
                arcname = os.path.join(os.path.relpath(dirname, relroot), file)

                zip_archive.write(filename, arcname=arcname)

    return archive
