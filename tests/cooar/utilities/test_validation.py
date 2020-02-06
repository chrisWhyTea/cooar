import pytest
from cooar.plugin import CooarPlugin
from cooar.utilities import types, validation


class TestValidation:
    @pytest.fixture
    def plugin(self):
        class Plugin(CooarPlugin):
            name = "plugin"
            description = "a test plugin"
            url = ""
            author = ""
            supported_mediatypes = (types.MediaType.VIDEO, types.MediaType.ARCHIVE)
            supported_authtypes = (types.AuthType.NO_AUTH,)
            supported_qualities = {types.MediaType.VIDEO: ("SD", "HD", "FullHD"),
            types.MediaType.ARCHIVE: ("SD", "HD")}
            template_strings = ("name", "lenght", "site")
            default_template = "default"

            def prepare(self, **kwargs):
                raise NotImplementedError()

            def collect(self, part_id=None, **kwargs):
                raise NotImplementedError()

            def download(self, file, **kwargs):
                raise NotImplementedError()

        return Plugin

    @pytest.mark.parametrize("mt", ["all", "video", "image", None])
    def test_template_validation(self, plugin, mt):
        if mt is not None:
            templates = {f"{mt}:{mt}"}
        else:
            templates = []
        values = validation.template_validation(plugin, templates)
        print(values)
        if mt == "all":
            assert values[types.MediaType.VIDEO] == "all"
            assert values[types.MediaType.ARCHIVE] == "all"
        elif mt == "video":
            assert values[types.MediaType.VIDEO] == "video"
            assert values[types.MediaType.ARCHIVE] == "default"
        elif mt == None:
            assert values[types.MediaType.VIDEO] == "default"
            assert values[types.MediaType.ARCHIVE] == "default"
        elif mt == "image":
            assert values[types.MediaType.VIDEO] == "default"
            assert values[types.MediaType.ARCHIVE] == "default"

    @pytest.mark.parametrize("mediatype_list", [[],[types.MediaType.VIDEO],[types.MediaType.IMAGE]])
    def test_mediatype_validation(self, plugin,mediatype_list):
        if mediatype_list == [types.MediaType.IMAGE]:
            with pytest.raises(SystemExit):
                validation.mediatype_validation(plugin, mediatype_list)
        else:
            values = validation.mediatype_validation(plugin, mediatype_list)

            if mediatype_list == []:
                assert len(values) == 2
            elif mediatype_list == [types.MediaType.VIDEO]:
                assert len(values) == 1
                assert values[0] == types.MediaType.VIDEO
    
    @pytest.mark.parametrize("qualities", [['video:HD'],['video:UHD'],[], ['image:HD']])
    def test_quality_validation(self,plugin,qualities):
        if qualities in (['image:HD'],['video:UHD']):
            with pytest.raises(SystemExit):
                validation.quality_validation(plugin, qualities)
        else:
            values = validation.quality_validation(plugin, qualities)
            if qualities == ['video:HD']:
                assert values.get(types.MediaType.VIDEO) == 'HD'
                assert values.get(types.MediaType.ARCHIVE) == 'SD'
            elif qualities == []:
                assert values.get(types.MediaType.VIDEO) == 'SD'
                assert values.get(types.MediaType.ARCHIVE) == 'SD'
            else:
                assert False
