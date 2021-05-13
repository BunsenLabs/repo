from aptsources.distinfo import DistInfo, Template
from aptsources.distro import Distribution, DebianDistribution
from aptsources.sourceslist import SourcesList

class Model:
    def __init__(self):
        self.__sources = SourcesList()

    def save(self):
        self.__sources.save()

    def load(self):
        self.__sources.refresh()

    def entries(self, include_disabled: bool = False):
        if include_disabled:
            return list(self.__valid_entries())
        else:
            return [ e for e in self.__valid_entries() if not e.disabled ]

    def __valid_entries(self):
        yield from (e for e in self.__sources.list if not e.invalid)
