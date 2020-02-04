import importlib
import inspect
import pkgutil

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
    """
    plugins = []
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
