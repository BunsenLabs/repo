#!/usr/bin/env python3

# apt-sourcemgr - CLI around python-apt for simple APT sources.list entry management
# Copyright (C) 2018 Jens John <dev ! 2ion ! de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from apt.sourcemgr import options
from aptsources import sourceslist, distinfo
from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter, ArgumentError)
import apt_pkg
import os
import re
import sys

EXIT_SUCCESS, EXIT_FAILURE, EXIT_NOMATCH = 0, 1, 2
APT_SOURCE_PARTSDIR = apt_pkg.config.find_dir("Dir::Etc::sourceparts")

def find_entries(entries, opts):
    """Find source entries matching the specification"""

    def cmp_list(x, y):
        if y is None:
            return True

        if opts.fuzzy:
            if opts.regex:
                return any(map(lambda xx: not not re.search(y, xx, flags=re.IGNORECASE)))
            return any([ x.count(yy) > 0 for yy in y ])

        return set(x) == set(y)

    def cmp_regex(x, y):
        if y is None:
            return True

        if opts.regex:
            return not not re.search(y, x, flags=re.IGNORECASE)

        return x == y

    def cmp_other(x, y):
        if y is None:
            return True
        return x == y

    def _filter(e):
        return (cmp_list(e.architectures, opts.architecture) and
                cmp_list(e.comps, opts.component) and
                cmp_regex(e.uri, opts.uri) and
                cmp_regex(e.dist, opts.distribution) and
                cmp_other(not e.disabled, opts.enabled) and
                cmp_other(e.disabled, opts.disabled) and
                cmp_other(e.invalid, opts.invalid) and
                cmp_other(e.type, opts.type))

    return filter(_filter, entries)

def main():
    opts = options.get()

    if opts.verb != "find" and (not opts.simulate and os.geteuid() > 0):
        print("Error: The given action requires root privileges.",
                file=sys.stderr)
        return EXIT_FAILURE

    if (opts.verb == "apply-template" and (opts.template is None or
        opts.distribution is None)):
        print("Error: `apply-template` requires non-empty --template and --distribution paramters.",
                file=sys.stderr)
        return EXIT_FAILURE

    try:
        deletion_queue = []
        src = sourceslist.SourcesList()

        if opts.verb == "add":
            kwargs = dict()
            if opts.file is not None:
                kwargs["file"] = opts.file
            if not all([opts.type, opts.uri, opts.distribution,
                opts.component]):
                raise BaseException("Not enough arguments: add")
            print(src.add(opts.type, opts.uri, opts.distribution, opts.component, **kwargs))

        elif opts.verb == "apply-template":
            def match_distro(v):
                if opts.regex:
                    return not not re.search(opts.distribution, v, flags=re.IGNORECASE)
                else:
                    return v == opts.distribution
            di = distinfo.DistInfo(dist=opts.template)
            # TODO: Implement mirror selection.
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
        else:
            entries = list(find_entries(src.list, opts))
            if len(entries) == 0:
                return EXIT_NOMATCH

            if opts.verb == "find":
                for e in entries:
                    print(e)

            elif opts.verb == "remove":
                for e in entries:
                    if all([ x is not e and x.file != e.file for x in src.list ]):
                        deletion_queue.append(e.file)
                        src.remove(e)
                    else:
                        print("Entry has other neighbours, disabling instead of removing: <{}>".format(e),
                                file=sys.stderr)
                        e.set_enabled(False)

            elif opts.verb == "enable":
                for e in entries:
                    e.set_enabled(True)

            elif opts.verb == "disable":
                for e in entries:
                    e.set_enabled(False)

        if not opts.simulate and opts.verb != "find":
            src.save()
            for path in deletion_queue:
                os.remove(path)
    except BaseException as e:
        print("ERROR, will not save any change(s):", e, file=sys.stderr)
        return EXIT_FAILURE

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
