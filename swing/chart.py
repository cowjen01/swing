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
    def __init__(self, version, release_date, archive_url):
        self.version = version
        self.release_date = release_date
        self.archive_url = archive_url

    @classmethod
    def from_dict(cls, json):
        version = json.get('version')
        release_date = json.get('releaseDate')
        archive_url = json.get('archiveUrl')
        return cls(version, release_date, archive_url)
