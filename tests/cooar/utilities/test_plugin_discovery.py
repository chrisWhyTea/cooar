import pytest

import tests
from cooar.utilities.plugin_discovery import external_plugins, plugins_from_namespace


class TestPluginDiscovery:
    def test_plugins_from_namespace(self):
        plugins = plugins_from_namespace(tests)
        assert len(plugins) == 1
        assert plugins[0].__name__ == "TestingPlugin"
