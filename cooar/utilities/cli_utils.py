from cooar.utilities.plugin_discovery import plugins_from_namespace, external_plugins
import cooar_plugins


def get_all_plugins():
    plugin_dict = {}
    plugins = plugins_from_namespace(cooar_plugins)
    for plugin in plugins:
        plugin_dict[plugin.name] = plugin
    return plugin_dict


def get_all_plugin_names():
    names = []
    for k, _ in get_all_plugins().items():
        names.append(k)
    return names
