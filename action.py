#!/usr/bin/env python3
"""GitHub Actions logic."""

from __future__ import annotations

if __name__ != '__main__':
    m = 'This module is not intended to be imported.'
    raise ImportError(m)

import os
from base64 import b64encode
from itertools import chain

import check_empty.__main__

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable
k, C, E = dict.fromkeys, 0x100000 if os.name == 'nt' else 0x40000, os.environ
B = k(('true', 'True', 'TRUE'), True)
B.update(k(('false', 'False', 'FALSE'), False))


def _(name: str, default: bool = False) -> bool:
    k = E[f'CE_{name.upper()}']
    if k == '<default>':
        return default
    try:
        return B[k]
    except KeyError:
        m = f'''Input does not meet YAML 1.2 "Core Schema" specification: {name}
Supported boolean inputs: "true | True | TRUE | false | False | FALSE"'''
        raise TypeError(m) from None


def g(x: Iterable[str] | None) -> bytes:
    return (
        b'W10='
        if x is None
        else b64encode(b'["%b"]' % b'", "'.join(map(str.encode, x)))
    )


class R(check_empty.reporter.abcdef.ReporterABC):
    if TYPE_CHECKING:
        o: str | None

        def to(self, out: str) -> str | None: ...

    def report(self, *a) -> None:
        o = self.o
        if o is None:
            return
        with open(o, 'ab') as f:
            # fmt: off
            f.write(
b"""z=%b
a=%b
b=%b
e=%b
r=%b
w=%b
x=%d
y=%d
d=%d
p=%d
n=%d
t=%d
l=%d
""" % (
        *map(g, a[:4]),
        b'e30='
        if a[4] is None
        else b64encode(
            b'{%b}'
            % b', '.join(b'"%b": %d' % (k.encode(), v) for k, v in a[4])
        ),
        g(map(str, a[5])),
        *a[6:12],
        bool(a[7] and a[13] and not a[8] and (not a[6] or d['may_not_exist'])),
    )
)


# fmt: on
d, x = {k: _(k) for k in ('clear', 'may_not_exist')}, R()
x.to(E['GITHUB_OUTPUT'])
r = check_empty.check(
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
    **d,
    recurse_into=int(E['CE_RECURSE_INTO'], 0),
    reporter=x,
    verbosity=5,
)
if d['clear']:
    r &= 12
check_empty.__main__._p.exit(r)  # ruff: ignore[private-member-access]
