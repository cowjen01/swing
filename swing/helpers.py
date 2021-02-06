import os
import re
from datetime import datetime

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


def get_yaml_filename(directory, name):
    yaml_path = os.path.join(directory, f'{name}.yaml')
    yml_path = os.path.join(directory, f'{name}.yml')

    if is_readable_file(yaml_path):
        return yaml_path
    elif is_readable_file(yml_path):
        return yml_path

    return None


def format_date(date_string):
    fmt = '%a, %d %b %Y %H:%M:%S %Z'
    date = datetime.strptime(date_string, fmt)
    return date.strftime('%m/%d/%y')
