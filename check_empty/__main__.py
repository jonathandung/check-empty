"""Implementation of the main routine."""

from __future__ import annotations

import check_empty as c

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable
__all__ = ('main',)
_p = __import__('argparse').ArgumentParser(
    'check-empty',
    description='Assert or enforce that some files, or even directories, are empty. '
    'Makes some reasonable assumptions, such as the absence of another process '
    'modifying a file or directory involved while running, which is the responsibility'
    ' of the user to ensure.',
    epilog='It is preferred that you use this as a pre-commit or prek hook, or a step '
    'in a GitHub Actions workflow, for most cases.',
    fromfile_prefix_chars='@',
    add_help=False,
)
f = _p.add_argument
f('filenames', nargs='+', help='the files that should be empty')
f('-?', '-h', '--help', action='help', help='show this help message and exit')
f('-v', '--version', action='version', version='check-empty v' + c.__version__)
f('-c', '--clear', action='store_true', help='clear files that are not empty')
f(
    '-m',
    '--may-not-exist',
    action='store_true',
    help='succeed even if some files are not present',
)
f('-Q', '--quiet', action='count', default=0, help='decrease output verbosity')
f('-V', '--verbose', action='count', default=0, help='increase output verbosity')
f('-o', '--out', help='write output to this file instead of stdout')


def _r():
    return _p


def main(argv: Iterable[str] | None = None) -> int:
    """Run the hook/CLI on the files in the command-line arguments passed.

    Args:
        argv: a list of arguments; default ``sys.argv[1:]``.

    Returns:
        The exit code. See :func:`~check_empty.check` for details.

    """
    try:
        n = _p.parse_args(argv)
    except SystemExit as e:
        return e.code  # ty: ignore[invalid-return-type]
    o = n.out
    if o is not None:
        # ruff: ignore[open-file-with-context-handler]
        c.default_reporter.to(open(o, 'w', encoding='utf-8'))
    return c.check(
        n.filenames,
        clear=n.clear,
        may_not_exist=n.may_not_exist,
        verbosity=2 + n.verbose - n.quiet,
    )


del f, TYPE_CHECKING
if __name__ == '__main__':
    _p.exit(main())
