from contextlib import AbstractContextManager
from enum import Enum
from typing import List, Optional
import json
import logging

from aptsources.sourceslist import SourcesList, SourceEntry

from repomgr.privdrop import privdrop

logger = logging.getLogger(__name__)

PrintableFormat = Enum("PrintableFormat", "TEXT JSON")

def parse_printable_format(key: str) -> PrintableFormat:
    """ For a given string key, return a matching PrintableFormat if it exists. """
    _key = key.upper()
    for pf in PrintableFormat:
        if pf.name == _key:
            return PrintableFormat(pf.value)
    raise ValueError(f"String {key} is not an index to PrintableFormat enum")

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
        if not (self.__save and self.__backup):
            # For any instances that do not require to do any writing
            # actions to the file system, we privdrop.
            logger.debug("Dropping privileges for non-write instance of SourceManager")
            assert privdrop() == True, "Failed to drop privileges for non-write instance of SourceManager"
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
            logger.error("Sources list not saved due to previous error(s)")
            pass # do not suppress exception
