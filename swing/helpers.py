import os
import re

url_regex = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'


def is_valid_url(url):
    return bool(re.match(url_regex, url))


def is_valid_path(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def get_archive_filename(chart_name, version):
    return f'{chart_name}-{version}.zip'
