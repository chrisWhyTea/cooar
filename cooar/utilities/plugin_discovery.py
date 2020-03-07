import importlib
import inspect
import os
import pkgutil
import sys
from pathlib import Path

from click import get_current_context

from cooar.plugin import CooarPlugin


def iter_namespace(ns_pkg):
    """
    iterates over the namespace modules,
    """
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def external_plugins():
    """
    Get all external plugins installed in the current environment 
    where the module name is starting with 'cooar_'

    To use this the corresponding module needs a __init__.py that contains or imports the acctual plugin file.

    To provide support for private plugins that are not shared via pypi you can put the plugin module into a '.cooarplugins' folder in your homedir
    """
    plugins = []

    # external plugins will not be used when cooar is doing unit tests
    if os.getenv("COOAR_IN_TEST_MODE"):
        return plugins
    private_plugins = Path.home() / ".cooarplugins"
    if private_plugins.exists() and str(private_plugins) not in sys.path:
        sys.path.append(str(private_plugins))

    for _, name, _ in pkgutil.iter_modules():
        if name.startswith("cooar_"):
            plugins.extend(_get_plugins_from_module(name))
    return plugins


def plugins_from_namespace(namespace):
    """
    Get all plugins present in the given namespace
    """
    plugins = []
    for _, name, _ in iter_namespace(namespace):
        plugins.extend(_get_plugins_from_module(name))
    return plugins


def _get_plugins_from_module(module_name):
    plugins = []
    for _, obj in inspect.getmembers(importlib.import_module(module_name)):
        if not inspect.isclass(obj):
            continue
        if not issubclass(obj, CooarPlugin):
            continue
        if obj.__name__ == CooarPlugin.__name__:
            continue
        plugins.append(obj)
    return plugins
