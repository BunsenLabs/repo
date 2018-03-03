from apt.sourcemgr import EXIT_FAILURE, EXIT_NOMATCH, EXIT_SUCCESS
from apt.sourcemgr.match import find_entries
from aptsources.sourceslist import SourcesList
from argparse import Namespace
from typing import List
import re
import sys

#######################################################################

FUNCTION_TABLE = dict()

def register(key):
    def __register(func):
        FUNCTION_TABLE[key] = func
        return func
    return __register

#######################################################################

@register('add')
def add(src: SourcesList, opts: Namespace, deletion_queue: List[str]) -> int:
    kwargs = dict()

    if opts.file is not None:
        kwargs["file"] = opts.file

    if not all([opts.type, opts.uri, opts.distribution,
        opts.component]):
        raise BaseException("Not enough arguments: add")

    print(src.add(opts.type, opts.uri, opts.distribution, opts.component, **kwargs))
    return EXIT_SUCCESS

@register('apply_template')
def apply_template(src: SourcesList, opts: Namespace, deletion_queue: List[str]) -> int:
    def match_distro(v):
        if opts.regex:
            return not not re.search(opts.distribution, v, flags=re.IGNORECASE)
        else:
            return v == opts.distribution
    di = distinfo.DistInfo(dist=opts.template)
    for t in filter(lambda t: match_distro(t.name), di.templates):
        base_uri = t.base_uri if t.base_uri is not None else t.parents[0].base_uri
        base_components = [ c.name for c in (t.components if
            len(t.components)>0 else t.parents[0].components) ]
        target_file = opts.file or "{}/{}.list".format(APT_SOURCE_PARTSDIR,
                opts.template.lower())
        if opts.component is not None:
            if opts.regex:
                r = re.compile(opts.component[0], flags=re.IGNORECASE)
                base_components = list(filter(r.search, base_components))
            else:
                base_components = list(filter(lambda c: c in opts.component,
                    base_components))
            if len(base_components) == 0:
                print("Error: No components left for template after filtering.", file=sys.stderr)
                return EXIT_NOMATCH
        print(src.add(t.type, base_uri, t.name, base_components, file=target_file))
        return EXIT_SUCCESS

@register('find')
def find(src: SourcesList, opts: Namespace, deletion_queue: List[str]) -> int:
    entries = find_entries(src.list, opts)
    if len(entries) == 0:
        return EXIT_NOMATCH
    for e in entries:
        print(e)
    return EXIT_SUCCESS

@register('remove')
def remove(src: SourcesList, opts: Namespace, deletion_queue: List[str]) -> int:
    entries = find_entries(src.list, opts)
    if len(entries) == 0:
        return EXIT_NOMATCH
    for e in entries:
        if all([ x is not e and x.file != e.file for x in src.list ]):
            deletion_queue.append(e.file)
            src.remove(e)
        else:
            print("Entry has other neighbours, disabling instead of removing: <{}>".format(e),
                    file=sys.stderr)
            e.set_enabled(False)
    return EXIT_SUCCESS

@register('enable')
def enable(src: SourcesList, opts: Namespace, deletion_queue: List[str]) -> int:
    entries = find_entries(src.list, opts)
    if len(entries) == 0:
        return EXIT_NOMATCH
    for e in entries:
        e.set_enabled(True)
    return EXIT_SUCCESS

@register('disable')
def disable(src: SourcesList, opts: Namespace, deletion_queue: List[str]) -> int:
    entries = find_entries(src.list, opts)
    if len(entries) == 0:
        return EXIT_NOMATCH
    for e in entries:
        e.set_enabled(False)
    return EXIT_SUCCESS
