#!/usr/bin/env python3
"""GitHub Action logic as an unimportable script."""

from __future__ import annotations

if __name__ != '__main__':
    m = 'This module is not intended to be imported.'
    raise ImportError(m)

import os
import sys
from itertools import chain

from check_empty import check
from check_empty.__main__ import parser

B = dict.fromkeys(('true', 'True', 'TRUE'), True)
B.update(dict.fromkeys(('false', 'False', 'FALSE'), False))
C, E = 0x100000 if os.name == 'nt' else 0x40000, os.environ


def _get_boolean_input(name: str, default: bool = False) -> bool:
    k = E[f'CE_{name.upper()}']
    if k == '<default>':
        return default
    try:
        return B[k]
    except KeyError:
        m = (
            f'Input does not meet YAML 1.2 "Core Schema" specification: {name}\n'
            'Supported boolean inputs: "true | True | TRUE | false | False | FALSE"'
        )
        raise TypeError(m) from None


k = {k: _get_boolean_input(k) for k in ('clear', 'may_not_exist')}
s = __import__('io').StringIO()
r = check(
    chain(
        E['CE_FILENAMES'].split('\n'),
        chain.from_iterable(
            map(
                __import__('functools').partial(
                    __import__('glob').iglob, recursive=True
                ),
                E['CE_GLOBS'].split('\n'),
            )
        ),
    ),
    **k,
    verbosity=int(E['CE_VERBOSITY'], 0),
    out=s,
)
s.seek(0)
f, g = s.read, (sys.stderr if r else sys.stdout).write
c = f(C)
while c:
    g(c)
    c = f(C)

parser.exit(r & 12 if k['clear'] else r)
