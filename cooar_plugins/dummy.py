from cooar.plugin import CooarPlugin
from cooar.utilities.types import AuthType, MediaType


class DummyPlugin(CooarPlugin):
    name = "dummy"
    description = "a dummy plugin"
    url = ""
    author = "Christopher Schmitt <cooar@chris.yt>"
    supported_mediatypes = (MediaType.VIDEO,)
    supported_authtypes = (AuthType.NO_AUTH,)
    supported_qualities = {MediaType.VIDEO: ("SD", "HD", "FullHD")}
    template_strings = ("name", "lenght", "site")
    default_template = ""

    def prepare(self, **kwargs):
        pass

    def collect(self, part_id=None, **kwargs):
        return []

    def download(self, file, **kwargs):
        pass
