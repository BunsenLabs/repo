""" This module implements functionality for managing representations of
pointers on the system. It does so by editing APT's sources.list
configuration files. """

from contextlib import AbstractContextManager
from enum import Enum
from typing import List, Optional, Callable
import json
import logging
import re
import shlex
import shutil

from aptsources.sourceslist import SourcesList, SourceEntry

from repo.privdrop import privdrop, privhave

logger = logging.getLogger(__name__)

PrintableFormat = Enum("PrintableFormat", "TEXT JSON SHELL")
SourceFilterExprOp = Enum("SourceFilterExprOp", "EQ NE REGEX NREGEX")

def parse_printable_format(key: str) -> PrintableFormat:
    """ For a given string key, return a matching PrintableFormat if it exists. """
    _key = key.upper()
    for pf in PrintableFormat:
        if pf.name == _key:
            return PrintableFormat(pf.value)
    raise ValueError(f"String {key} is not an index to PrintableFormat enum")

class SourceEntryFilter:
    """ A user-exposable filter engine operating on lists of
    SourceEntry. """

    OPERATORS = {
        # ours := source entry field value
        # theirs := user input
        "=": lambda ours, theirs: ours == theirs,
        "!": lambda ours, theirs: ours != theirs,
        "~": lambda ours, theirs: re.search(theirs, ours, flags=re.IGNORECASE) is not None,
        "^": lambda ours, theirs: re.search(theirs, ours, flags=re.IGNORECASE) is None,
    }
    # Because SourceEntry has some ugly field names as an implementation
    # detail, we perform alias translation for the SourceEntry fields we
    # commonly expose in the CLI.
    ALIAS = {
        "arch"         : "architectures",
        "architecture" : "architectures",
        "component"    : "comps",
        "components"   : "comps",
        "distribution" : "dist",
    }

    def __init__(self, expressions: List[str]):
        self.__expressions = expressions
        self.__parse()

    def __parse(self):
        composite = []
        for e in self.__expressions:
            composite.append(self.__parsexpr(e))
        self.__filter = lambda e: (
            all([ func(e) for func in composite ])
        )

    def filter(self, entries: List[SourceEntry]) -> List[SourceEntry]:
        return list(filter(self.__filter, entries))

    def __parsexpr(self, s: str) -> Callable[[SourceEntry], bool]:
        if m := re.match(r"^(?P<field>\w+)(?P<op>[=!~^])(?P<oparg>.+)$", s):
            d = m.groupdict()
            logger.debug("SourceEntryFilter: parse %s", d)
            field, op, oparg = d["field"], d["op"], d["oparg"]
            if alias := SourceEntryFilter.ALIAS.get(field, None):
                logger.debug("SourceEntryFilter: alias %s -> %s", field, alias)
                field = alias
            def func(e: SourceEntry) -> bool:
                try:
                    v = getattr(e, field)
                except AttributeError:
                    return False
                _oparg = oparg.lower()
                if isinstance(v, (str, int, float, bool,)):
                    return SourceEntryFilter.OPERATORS[op](str(v).lower(), oparg.lower())
                elif isinstance(v, list):
                    return any([
                        SourceEntryFilter.OPERATORS[op](str(vv).lower(), oparg.lower())
                        for vv in v
                    ])
                else:
                    return False
            return func
        else:
            raise ValueError(f"invalid filter expression: <{s}>")

class ExtSourcesList(SourcesList):
    """ Extensions to python-apt's aptsources.sourceslist.SourcesList class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def entries(self, include_disabled: bool = False):
        """ Returns matching instances of SourceEntry contained in this list. """
        if include_disabled:
            return list(self.__valid_entries())
        else:
            return [ e for e in self.__valid_entries() if not e.disabled ]

    def add_from_line(self, line: str) -> SourceEntry:
        """ Given a sources.list line, parse the lines and add them to
        the source. """
        entry = SourceEntry(line)
        if entry.invalid:
            raise ValueError(f"Could not parse line: {line}")
        return self.add(
            entry.type,
            entry.uri,
            entry.dist,
            entry.comps,
            entry.comment,
            architectures=entry.architectures,
        )

    def printable(self, entries: List[SourceEntry], fmt: PrintableFormat = PrintableFormat.TEXT) -> str:
        """ Given a list of SourceEntry, format them into a printable representation and return that
        string. """

        if fmt == PrintableFormat.TEXT:
            return "\n".join(str(e) for e in entries)

        elif fmt == PrintableFormat.SHELL:
            txt = """declare -A REPO_RESULTS=(\n"""
            for e in entries:
                for c in e.comps:
                    txt += "[{}]={}\n".format(
                        shlex.quote("{}/{}/{}".format(e.type, e.dist, c)),
                        shlex.quote(str(e)),
                    )
            txt += ")"
            return txt

        elif fmt == PrintableFormat.JSON:
            return json.dumps({
                "entries": [
                    {
                        "invalid": e.invalid,
                        "disabled": e.disabled,
                        "type": e.type,
                        "architectures": e.architectures,
                        "trusted": e.trusted,
                        "uri": e.uri,
                        "dist": e.dist,
                        "components": e.comps,
                        "comment": e.comment,
                        "line": str(e),
                        "file": e.file,
                    }
                    for e in entries
                ]
            }, indent=2, sort_keys=True)

    def __valid_entries(self):
        yield from (e for e in self.list if not e.invalid)

class SourceManager(AbstractContextManager):
    """ Allows ExtSourcesList to be used as a convenient context. """

    def __init__(self, save: bool = False, backup: bool = False):
        self.__save = save
        self.__backup = backup

    def __enter__(self) -> ExtSourcesList:
        self.__sourceslist = ExtSourcesList()
        if not (self.__save or self.__backup):
            # For any instances that do not require to do any writing
            # actions to the file system, we privdrop.
            logger.debug("Dropping privileges for non-write instance of SourceManager")
            assert privdrop() == True, "Failed to drop privileges for non-write instance of SourceManager"
        else:
            assert privhave() == True, "Requiring root privileges."
        if self.__backup:
            extension = self.__sourceslist.backup()
            logger.debug("Created sources.list backup with extension: %s", extension)
        return self.__sourceslist

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            if self.__save:
                self.__sourceslist.save()
                logger.debug("Saved sources list upon exit")
            return True
        else:
            if self.__save:
                logger.error("Sources list not saved due to previous error(s)")
            pass # do not suppress exception
