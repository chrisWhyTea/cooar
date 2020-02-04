import click

from cooar.plugin import CooarPlugin
from cooar.utilities import cli_utils, echo


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
    cli_utils.set_debug(debug)

    if info is not None:
        cli_utils.show_info(cli_utils.get_all_plugins().get(info))
