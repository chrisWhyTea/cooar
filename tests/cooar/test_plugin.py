from cooar.plugin import CooarPlugin
from cooar.utilities.types import AuthType, MediaType


class TestCooarPlugin:
    def test_instantiate_cooar_plugin(self):
        class Plugin(CooarPlugin):
            name = "plugin"
            description = "a test plugin"
            url = ""
            author = "Christopher Schmitt <cooar@chris.yt>"
            supported_mediatypes = (MediaType.VIDEO,)
            supported_authtypes = (AuthType.NO_AUTH,)
            supported_qualities = {MediaType.VIDEO: ("SD", "HD", "FullHD")}
            template_strings = ("name", "lenght", "site")
            default_template = ""

            def prepare(self, **kwargs):
                raise NotImplementedError()

            def collect(self, part_id=None, **kwargs):
                raise NotImplementedError()

            def download(self, file, **kwargs):
                raise NotImplementedError()

        plugin = Plugin()
        assert plugin.supported_qualities[MediaType.VIDEO] == ("SD", "HD", "FullHD")
