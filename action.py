#!/usr/bin/env python3
"""GitHub Action logic."""

from __future__ import annotations

from os import environ

import check_empty.__main__ as c

if __name__ != '__main__':
    m = 'This module is not intended to be imported.'
    raise ImportError(m)
bools: dict[str, bool] = dict.fromkeys(('true', 'True', 'TRUE'), True)
bools.update(dict.fromkeys(('false', 'False', 'FALSE'), False))


def get_boolean_input(name: str) -> bool:
    """Return the boolean value an environment variable corresponds to.

    This behaves as if the name was parsed in a YAML 1.2 file using the ${{ }} syntax.

    Args:
        name: The name of the environment variable to get.

    Returns:
        The boolean value of the environment variable.

    Raises:
        KeyError: If a required input is not passed.

        TypeError: If the input is not a valid boolean value. This mirrors the behaviour
        of @actions/core.getBooleanInput().

    """
    k = environ[name]
    try:
        return bools[k]
    except KeyError:
        m = (
            f'Input does not meet YAML 1.2 "Core Schema" specification: {name}\n'
            'Supported boolean inputs: "true | True | TRUE | false | False | FALSE"'
        )
        raise TypeError(m) from None


a = []
f = a.append
if get_boolean_input('CE_MUST_EXIST'):
    f('-m')
if get_boolean_input('CE_QUIET'):
    f('-q')
a.extend(environ['CE_FILENAMES'].split('\n'))
c.parser.exit(c.main(a))
