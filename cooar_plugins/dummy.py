from cooar.file import File
from cooar.plugin import CooarPlugin
from cooar.utilities import echo, types


class DummyPlugin(CooarPlugin):
    name = "dummy"
    description = "a dummy plugin"
    url = ""
    author = "Christopher Schmitt <cooar@chris.yt>"
    supported_mediatypes = (types.MediaType.VIDEO,)
    supported_authtypes = (types.AuthType.NO_AUTH,)
    supported_qualities = {types.MediaType.VIDEO: ("SD", "HD", "FullHD")}
    template_strings = ("name", "lenght", "site")
    default_template = ""

    def prepare(self, **kwargs):
        pass

    def collect(self, part_id=None, **kwargs):
        # The dummy always generates as many files provided by the part_id says,
        # normaly the part_id would be used to filter for a specific part of a website
        # but in this case it provides the amount of Files. Obviously this will fail in
        # case a non int castable string is given
        try:
            amount = int(part_id) if part_id is not None else 100
        except ValueError:
            echo.error_msg("Invalid part_id, must be a integer")
            exit(1)
        file_counter = 0
        files = []
        while file_counter != amount:
            files.append(File(f"/files/file_{file_counter}.txt"))
            file_counter += 1
        return files

    def download(self, file, **kwargs):
        pass
