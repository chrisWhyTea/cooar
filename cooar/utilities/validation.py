import json

from cooar.plugin import CooarPlugin
from cooar.utilities import cli_utils, echo, types


def auth_validation(plugin: CooarPlugin, username, password, cookies, token):
    if (
        types.AuthType.USERNAME_PASSWORD in plugin.supported_authtypes
        and username is not None
        and password is not None
    ):
        return (types.AuthType.USERNAME_PASSWORD, username, password)
    elif (
        types.AuthType.PASSWORD_ONLY in plugin.supported_authtypes
        and password is not None
    ):
        return (types.AuthType.PASSWORD_ONLY, password)
    elif types.AuthType.COOKIES in plugin.supported_authtypes and cookies is not None:
        return (types.AuthType.COOKIES, json.loads(cookies))
    elif types.AuthType.TOKEN in plugin.supported_authtypes and token is not None:
        return (types.AuthType.TOKEN, token)
    elif (
        types.AuthType.NO_AUTH in plugin.supported_authtypes
        and password is None
        and username is None
        and cookies is None
    ):
        return (types.AuthType.NO_AUTH,)
    else:
        echo.error_msg("Invalid auth")
        exit(1)


def mediatype_validation(plugin: CooarPlugin, mediatypes):
    ml = []
    for mediatype in mediatypes:
        m = types.MediaType(mediatype)
        if m in plugin.supported_mediatypes:
            ml.append(m)
        else:
            echo.error_msg("Unsupported MediaType")
            exit(1)
    # If no mediatype is given, expect to load all supported mediatypes
    if len(ml) == 0:
        ml = plugin.supported_mediatypes
    return tuple(set(ml))


def quality_validation(plugin: CooarPlugin, quality):
    qd = {}

    for q in quality:
        m, qs = q.split(":", 1)
        m = types.MediaType(m)
        qualities = plugin.supported_qualities.get(m)
        if qualities is not None:
            if qs in qualities:
                qd[m] = qs
            else:
                echo.error_msg("Unsupported quality.")
                exit(1)

        else:
            echo.error_msg("Unsupported MediaType for quality.")
            exit(1)

    # Set default for not defined qualities
    for m in plugin.supported_mediatypes:
        if qd.get(m) is None:
            qd[m] = plugin.supported_qualities.get(m)[0]
    return qd

def template_validation(plugin: CooarPlugin, templates):
    td = {}
    overwrite_all = None
    for template in templates:
        m, ts = template.split(":", 1)
        if m == 'all':
            overwrite_all = ts
            break
        m = types.MediaType(m)
        td[m] = ts
    
    # Set default and overwirte
    for mediatype in plugin.supported_mediatypes:
        if overwrite_all is not None:
            td[mediatype] = overwrite_all
        elif td.get(mediatype) is None:
            td[mediatype] = plugin.default_template
        else:
            continue
    return td
        


def validate(**kwargs):
    plugin = cli_utils.get_all_plugins().get(kwargs.get("plugin"))
    auth_package = auth_validation(
        plugin,
        kwargs.get("username"),
        kwargs.get("password"),
        kwargs.get("cookies"),
        kwargs.get("token"),
    )
    mediatypes = mediatype_validation(plugin, kwargs.get("mediatype"))
    qualities = quality_validation(plugin, kwargs.get("quality", []))
    templates = template_validation(plugin, kwargs.get("template", []))
    return_value = {
        "plugin": plugin,
        "auth": auth_package,
        "mediatypes": mediatypes,
        "qualities": qualities,
        "templates": templates
    }
    echo.debug_msg(f"Validated args: {return_value}")
    return return_value
