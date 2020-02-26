import json

import click

import cooar_plugins
from cooar.file import File
from cooar.plugin import CooarPlugin
from cooar.utilities import echo, types
from cooar.utilities.plugin_discovery import (external_plugins,
                                              plugins_from_namespace)


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


def enum_list_to_string(enu):
    string = ""
    for ei in enu:
        string = string + ei.value + ", "
    return string[:-2]


def enum_to_list(enu):
    return [e.value for e in enu]


def list_to_string(l):
    string = ""
    for li in l:
        string = string + li + ", "
    return string[:-2]


def set_debug(debug_state):
    ctx = click.get_current_context()
    ctx.obj["DEBUG"] = debug_state
    echo.debug_msg("Debug mode is active")


def show_info(plugin):
    echo.key_value_message("Plugin Name", plugin.name)
    echo.key_value_message("Author", plugin.author)
    echo.key_value_message("URL", plugin.url)
    echo.key_value_message("Description", plugin.description)
    echo.key_value_message(
        "Supported auth types", enum_list_to_string(plugin.supported_authtypes)
    )
    echo.key_value_message(
        "Supported media types", enum_list_to_string(plugin.supported_mediatypes)
    )
    echo.key_value_message("Template strings", list_to_string(plugin.template_strings))
    for m in plugin.supported_mediatypes:
        qualities = plugin.supported_qualities.get(m)
        if qualities is not None:
            echo.key_value_message(
                f"{m.value.capitalize()} qualities", list_to_string(qualities)
            )
    echo.key_value_message("Default template string", plugin.default_template)


def current_item_name(file: File):
    if file is not None:
        return file.filename
