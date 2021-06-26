import logging

import click
import click_log
click_log.basic_config()

from .manager import SourceManager, parse_printable_format, PrintableFormat
from .privdrop import privdrop

logger = logging.getLogger(__name__)
fmt = PrintableFormat.TEXT
flag_backup = False
flag_save = True

@click.command("ls")
@click.option("--all/--no-all", default=False, help="Also list disabled (commented) entries")
def ls(all) -> int:
    """ List enabled sources.list entries. """
    assert privdrop() == True
    with SourceManager(save=False, backup=False) as mgr:
        entries = mgr.entries(include_disabled=all)
        print(mgr.printable(entries, fmt=fmt))
    return 0

@click.command("add")
@click.option("-t", "--type", default="deb")
@click.option("-u", "--uri", required=True)
@click.option("-a", "--arch", multiple=True)
@click.option("-c", "--component", multiple=True, default=list(), required=True)
@click.option("-d", "--distribution", required=True)
def add(type, uri, arch, component, distribution):
    """ Ensure a specific entry exists in sources.list, and is enabled. """
    with SourceManager(save=flag_save, backup=flag_backup) as mgr:
        if entry := mgr.add(type, uri, distribution, component, architectures=arch):
            print(mgr.printable([entry], fmt=fmt))
            return 0
    return 1

@click.command("insert")
@click.argument("source-entry", nargs=-1)
def insert(source_entry):
    """ Add multiple entry lines to sources.list. """
    with SourceManager(save=flag_save, backup=flag_backup) as mgr:
        for line in source_entry:
            if entry := mgr.add_from_line(line):
                print(mgr.printable([entry], fmt=fmt))
    return 0

@click.command("enable")
def enable():
    """ Enable all matching entries. """
    return 0

@click.command("disable")
def disable():
    """ Disable all matching entries. """
    return 0

@click.command("rm")
def rm():
    """ Remove all matching entries. """
    return 0

@click.command("test")
def test():
    """ Test if a matching entry exists in sources.list. Useful in scripting. """
    assert privdrop() == True
    return 0

@click.group()
@click.option("-f", "--format", type=click.Choice(["text", "json"]), default="text", help="Change sources.list entry presentation format")
@click.option("--backup/--no-backup", default=False, help="For actions modifying the sources.list, always create a backup before applying changes")
@click.option("--save/--no-save", default=True, help="Optionally disable saving of any changes applied to sources.list. Usefull only for debugging")
@click_log.simple_verbosity_option()
def entrypoint(format: str, backup: bool, save: bool):
    """ Simple APT sources.list management tool """
    global fmt
    global flag_save
    global flag_backup
    fmt = parse_printable_format(format) 
    flag_backup = backup
    flag_save = save

entrypoint.add_command(add)
entrypoint.add_command(disable)
entrypoint.add_command(enable)
entrypoint.add_command(insert)
entrypoint.add_command(ls)
entrypoint.add_command(rm)
