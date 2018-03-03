from aptsources.sourceslist import SourceEntry
from argparse import Namespace
from typing import List, Generator, Union
import re

def find_entries(entries: List[SourceEntry], opts: Namespace) -> List[SourceEntry]:
    """Find source entries matching the specification"""

    def cmp_list(x: List[str], y: List[str]) -> bool:
        if y is None:
            return True

        if opts.fuzzy:
            if opts.regex:
                return any(map(lambda xx: not not re.search(y, xx, flags=re.IGNORECASE)))
            return any([ x.count(yy) > 0 for yy in y ])

        return set(x) == set(y)

    def cmp_regex(x: str, y: str) -> bool:
        if y is None:
            return True

        if opts.regex:
            return not not re.search(y, x, flags=re.IGNORECASE)

        return x == y

    def cmp_other(x: str, y: Union[None, str]) -> bool:
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

    return list(filter(_filter, entries))
