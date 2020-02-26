from pathlib import Path
from time import sleep

import click

from cooar.plugin import CooarPlugin
from cooar.utilities import cli_utils, echo, types, validation


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


@cli.command()
@click.argument(
    "plugin",
    metavar="plugin",
    envvar="COOAR_PLUGIN",
    type=click.Choice(cli_utils.get_all_plugin_names()),
)
@click.option("--username", "-u", type=click.STRING)
@click.option("--password", "-p", type=click.STRING)
@click.option("--cookies", "-c", type=click.STRING)
@click.option("--authtoken", "-t", type=click.STRING)
@click.option(
    "--mediatype",
    "-m",
    type=click.Choice(cli_utils.enum_to_list(types.MediaType)),
    multiple=True,
)
@click.option("--part_id", "-P", type=click.STRING)
@click.option("--quality", "-q", type=click.STRING, multiple=True)
@click.option("--template", "-T", type=click.STRING, multiple=True)
@click.option("--replace/--no-replace", default=False)
@click.option(
    "--download_path",
    "-d",
    default=Path("."),
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
)
@click.pass_context
def download(ctx, **kwargs):
    package = validation.validate(**kwargs)

    plugin = package["plugin"]()

    plugin.prepare(**package)

    files = plugin.collect(part_id=kwargs.get("part_id"))

    with click.progressbar(
        files,
        length=len(files),
        label="Downloaded files",
        show_pos=True,
        item_show_func=cli_utils.current_item_name,
    ) as files_progress:
        for f in files_progress:
            if not ctx.obj.get("SIMULATION"):
                f.prepare_file_path(kwargs.get("download_path"))
                if not kwargs.get("replace"):
                    if f.absolute_file_path.exists():
                        echo.debug_msg("Skip existing file")
                        continue
                plugin.download(f)
            else:
                sleep(0.5)
                continue
                # SIMULATE DOWNLOAD
    echo.debug_msg("Download complete")


@cli.command()
@click.argument(
    "plugin",
    metavar="plugin",
    envvar="COOAR_PLUGIN",
    type=click.Choice(cli_utils.get_all_plugin_names()),
)
@click.option("--username", "-u", type=click.STRING)
@click.option("--password", "-p", type=click.STRING)
@click.option("--cookies", "-c", type=click.STRING)
@click.option("--authtoken", "-t", type=click.STRING)
@click.option(
    "--mediatype",
    "-m",
    type=click.Choice(cli_utils.enum_to_list(types.MediaType)),
    multiple=True,
)
@click.option("--part_id", "-P", type=click.STRING)
@click.option("--quality", "-q", type=click.STRING, multiple=True)
@click.option("--template", "-T", type=click.STRING, multiple=True)
@click.option("--replace/--no-replace", default=False)
@click.option(
    "--download_path",
    "-d",
    default=Path("."),
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
)
@click.pass_context
def simulate(ctx, plugin, **kwargs):
    ctx.obj["SIMULATION"] = True
    ctx.forward(download)
