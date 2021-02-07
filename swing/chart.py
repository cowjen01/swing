import os
import zipfile
from io import BytesIO

import click


class Chart:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, json):
        name = json.get('name')
        description = json.get('description')
        return cls(name, description)


class Release:
    def __init__(self, version, release_date, archive_url, notes):
        self.version = version
        self.release_date = release_date
        self.archive_url = archive_url
        self.notes = notes

    @classmethod
    def from_dict(cls, json):
        version = json.get('version')
        release_date = json.get('releaseDate')
        archive_url = json.get('archiveUrl')
        notes = json.get('notes')
        return cls(version, release_date, archive_url, notes)


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

                click.echo(f'Packing file: {arcname}')

                zip_archive.write(filename, arcname=arcname)

    return archive
