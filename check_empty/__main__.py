#!usr/bin/env python3
"""Implementation of the main routine."""

from __future__ import annotations

from os.path import getsize

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Literal, Sequence

__version__ = '0.1'
parser = __import__('argparse').ArgumentParser(
    'check-empty',
    description='Assert or enforce that some files are empty.',
    epilog='It is preferred that you use this as a pre-commit/prek hook or GitHub '
    'Action for most cases which are not one-off.',
)
f = parser.add_argument
f('filenames', nargs='+', help='the files that should be empty')
f('-v', '--version', action='version', version='check-empty v' + __version__)
f('-c', '--clear', action='store_true', help='clear files that are not empty')
f('-m', '--must-exist', action='store_true', help='fail if any file is absent')
f('-q', '--quiet', action='store_true', help='suppress output')


def main(argv: Sequence[str] | None = None) -> Literal[0, 1, 2, 3]:
    """Run the hook on the files in the (command-line) arguments passed.

    Args:
        argv: A list of arguments excluding the executable name, default sys.argv[1:].

    Returns:
        The exit code. A bitwise or of 1 (some files were not empty) and 2 (some files
        were absent and -m/--must-exist was specified), such that 0 is the only return
        value that represents success as expected.

    """
    r, z, n = [''], [''], parser.parse_args(argv)
    g, j, c, t, i = r.append, z.append, n.clear, 0, n.filenames
    if c:
        for a in i:
            try:
                s = getsize(a)
            except FileNotFoundError:
                j(a)
                continue
            if not s:
                continue
            g(f'{a} ({s} bytes)')
            t += s
            with open(a, 'wb'):
                ...
    else:
        for a in i:
            try:
                s = getsize(a)
            except FileNotFoundError:
                j(a)
                continue
            if not s:
                continue
            g(f'{a} ({s} bytes)')
            t += s
    p, x, y = not n.quiet, len(z) - 1, len(r) - 1
    v = n.must_exist << 1 if x else 0
    if p:
        print(*z, sep='\nNot found: ')
        print(f'{x} files not found' if x else 'All files were found')
    if y:
        if p:
            print(*r, sep='\nCleared: ' if c else '\nNot empty: ', end='\n\n')
            print(y, 'offending files' if y > 1 else 'offending file')
            print(f'Total size: {t} bytes')
        return v | 1
    if p:
        print('All found files were empty')
    return v


if __name__ == '__main__':
    parser.exit(main())
del f, TYPE_CHECKING
