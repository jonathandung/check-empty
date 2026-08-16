"""Implementation of the main routine. Also exports the argument parser."""

from __future__ import annotations

import check_empty as c

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable

    from typing_extensions import Literal
__all__ = 'main', 'parser'
parser = __import__('argparse').ArgumentParser(
    'check-empty',
    description='Assert or enforce that some files, or even directories, are empty. '
    'Makes some reasonable assumptions, such as the absence of another process '
    'modifying a file or directory involved, while running.',
    epilog='It is preferred that you use this as a pre-commit/prek hook or GitHub '
    'Action for most cases which are not one-off.',
)
f = parser.add_argument
f('filenames', nargs='+', help='the files that should be empty')
f('-v', '--version', action='version', version='check-empty v' + c.__version__)
f('-c', '--clear', action='store_true', help='clear files that are not empty')
f(
    '-m',
    '--may-not-exist',
    action='store_true',
    help='do not fail solely because some files are not present',
)
f('-Q', '--quiet', action='count', default=0, help='decrease output verbosity')
f('-V', '--verbose', action='count', default=0, help='increase output verbosity')
f('-o', '--out', help='write output to this file instead of stdout')


def main(argv: Iterable[str] | None = None) -> c.ExitCode | Literal[2]:
    """Run the hook/CLI on the files in the command-line arguments passed.

    Args:
        argv: a list of arguments; default `sys.argv[1:]`.

    Returns:
        The exit code. See `check` for details.

    """
    try:
        n = parser.parse_args(argv)
    except SystemExit as e:
        return e.code  # ty: ignore[invalid-return-type]
    o = n.out
    if o is not None:
        # ruff: ignore[open-file-with-context-handler]
        o = open(o, 'w', encoding='utf-8')
    try:
        return c.check(
            n.filenames,
            clear=n.clear,
            may_not_exist=n.may_not_exist,
            verbosity=2 + n.verbose - n.quiet,
            out=o,
        )
    finally:
        if o is not None:
            o.close()


del f, TYPE_CHECKING
if __name__ == '__main__':
    parser.exit(main())
