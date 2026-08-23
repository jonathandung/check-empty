#!/usr/bin/env python3
"""GitHub Action logic as an unimportable script."""

from __future__ import annotations

if __name__ != '__main__':
    m = 'This module is not intended to be imported.'
    raise ImportError(m)

import sys
from itertools import chain
from os import environ, name

from check_empty import check
from check_empty.__main__ import parser

B = dict.fromkeys(('true', 'True', 'TRUE'), True)
B.update(dict.fromkeys(('false', 'False', 'FALSE'), False))
C = 0x100000 if name == 'nt' else 0x40000


def get_boolean_input(name: str, default: bool = False) -> bool:
    """Return the boolean value of the input name based on an environment variable.

    This behaves as if the name was parsed in a YAML 1.2 file using the ${{ }} syntax,
    combined with the default value behaviour.

    Args:
        name: The name of the environment variable to get.
        default: The default value to return if the environment variable is an empty
        string, indicating an omission to provide the input.

    Returns:
        The boolean value of the environment variable.

    Raises:
        KeyError: If a required input is not passed.

        TypeError: If the input is not a valid boolean value. This mirrors the behaviour
        of @actions/core.getBooleanInput() in the toolkit.

    """
    k = environ[f'CE_{name.upper()}']
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


k = {k: get_boolean_input(k) for k in ('clear', 'may_not_exist')}
s = __import__('io').StringIO()
r = check(
    chain(
        environ['CE_FILENAMES'].split('\n'),
        chain.from_iterable(
            map(
                __import__('functools').partial(
                    __import__('glob').iglob, recursive=True
                ),
                environ['CE_GLOBS'].split('\n'),
            )
        ),
    ),
    **k,
    verbosity=int(environ['CE_VERBOSITY'], 0),
    out=s,
)
s.seek(0)
f, g = s.read, (sys.stderr if r else sys.stdout).write
c = f(C)
while c:
    g(c)
    c = f(C)

parser.exit(r & 12 if k['clear'] else r)
