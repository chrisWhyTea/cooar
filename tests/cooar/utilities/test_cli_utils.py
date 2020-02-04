from cooar.utilities.cli_utils import get_all_plugin_names


class TestCliUtils:
    def test_get_all_plugin_names(self):
        n = get_all_plugin_names()
        assert len(n) == 1
