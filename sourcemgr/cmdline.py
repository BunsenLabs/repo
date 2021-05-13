import logging
import os
import re

import click
import click_log

from .model import Model

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.command("ls")
@click.option("--all/--no-all", default=False, help="Also list disabled (commented) entries")
def ls(all) -> int:
    """ List enabled sources.list entries. """
    m = Model()
    print("\n".join(str(e) for e in m.entries(include_disabled=all)))
    return 0

@click.command("add")
@click.option("-t", "--type", default="deb")
@click.option("-u", "--uri", required=True)
@click.option("-a", "--arch", multiple=True)
@click.option("-c", "--component", multiple=True, default=list(), required=True)
@click.option("-d", "--distribution", required=True)
def add(type, uri, arch, component, distribution):
    """ Add a specific entry to sources.list. If an entry matching the parameters already exists in
    disabled state, the existing entry will be enabled instead. """
    return 0

@click.command("insert")
@click.argument("source-entry", nargs=-1)
def insert(source_entry):
    """ Add entries by specifying entries as they should appear in sources.list """
    print(source_entry)
    return 0

@click.command("enable")
def enable():
    """ Based on the given filter options, enable all matching entries in sources.list. """
    return 0

@click.command("disable")
def disable():
    """ Based on the given filter options, disable all matching entries in sources.list. """
    return 0

@click.command("rm")
def rm():
    """ Based on the given filter options, remove all matching entries in sources.list. """
    return 0

@click.group()
@click_log.simple_verbosity_option(logger)
def entrypoint():
    """ Simple APT sources.list management tool """
    pass

entrypoint.add_command(add)
entrypoint.add_command(disable)
entrypoint.add_command(enable)
entrypoint.add_command(insert)
entrypoint.add_command(ls)
entrypoint.add_command(rm)
