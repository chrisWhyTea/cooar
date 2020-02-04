import click

from cooar.utilities import echo
from cooar.utilities import cli_utils


@click.group(invoke_without_command=True)
@click.option("--debug/--no-debug", default=False, envvar="COOAR_DEBUG")
@click.option(
    "--info",
    type=click.Choice(cli_utils.get_all_plugin_names()),
    default=None,
    help="Show infos about the plugin.",
)
@click.pass_context
def cli(ctx, debug, info):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    echo.debug_msg("Debug mode is active")
    if info is not None:
        echo.debug_msg(f"Show info for {info}")
