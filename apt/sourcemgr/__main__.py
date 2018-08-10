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
from apt.sourcemgr import EXIT_SUCCESS, EXIT_FAILURE
from apt.sourcemgr.actions import FUNCTION_TABLE
from aptsources import sourceslist, distinfo
import os
import re
import sys


def main() -> int:
    opts = options.get()
    ret = EXIT_SUCCESS

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
        ret = FUNCTION_TABLE[opts.verb](src, opts, deletion_queue)
        if not opts.simulate and opts.verb != "find":
            for path in deletion_queue:
                if os.access(path, os.F_OK | os.W_OK):
                    os.remove(path)
            src.save()
    except BaseException as e:
        print("ERROR, will not save any change(s):", e, file=sys.stderr)
        return EXIT_FAILURE

    return ret

if __name__ == "__main__":
    sys.exit(main())
