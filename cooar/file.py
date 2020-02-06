from pathlib import Path


class File:
    _filename = None
    _path = None
    _file_path_string = None
    url = None
    absolute_file_path = None

    def __init__(self, file_path_string=None, url=None):
        self.file_path_string = file_path_string
        self.url = url

    @property
    def filename(self):
        return self._filename

    @property
    def path(self):
        return self._path

    @property
    def file_path_string(self):
        return self._file_path_string

    @file_path_string.setter
    def file_path_string(self, file_path_string):
        ep, fn = file_path_string.rsplit("/", 1)
        self._filename = fn
        self._path = ep
        self._file_path_string = file_path_string

    def prepare_file_path(self, download_path):
        p = Path(download_path) / self.path
        p.mkdir(parents=True, exist_ok=True)
        self.absolute_file_path = p / self.filename
