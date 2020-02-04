import click


def message(msg: str, color: str = "bright_white", bold=False):
    message = click.style(msg, fg=color, bold=bold)
    click.echo(message)


def debug_msg(msg: str):
    debug_color = "bright_black"
    ctx = click.get_current_context()
    if ctx.obj.get("DEBUG"):
        _prefixed_message("DEBUG", msg, debug_color)


def warning_msg(msg: str):
    warning_color = "bright_yellow"
    _prefixed_message("WARNING", msg, warning_color)


def error_msg(msg: str):
    error_color = "bright_red"
    _prefixed_message("ERROR", msg, error_color)


def _prefixed_message(prefix: str, msg: str, color: str, err: bool = False):
    prefix_msg = click.style(prefix + ": ", fg=color, bold=True)
    message = click.style(msg, fg=color, bold=False)
    if err is True:
        click.echo(prefix_msg + message, err=msg)
    else:
        click.echo(prefix_msg + message)


def key_value_message(
    key: str, value: str, key_color: str = "blue", value_color: str = "bright_blue"
):
    key_msg = click.style(key + ": ", fg=key_color)
    value_msg = click.style(value, fg=value_color)
    click.echo(key_msg + value_msg)


def bool_style(value: bool, true_color: str = "green", false_color: str = "red"):
    if value is True:
        return click.style("True", fg=true_color)
    else:
        return click.style("False", fg=false_color)
