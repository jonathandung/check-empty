# Copyright © 2026 Jonathan Dung. All rights reserved.
# SPDX-License-Identifier: MIT
"""Utility to check the emptiness of files and directories.

Pre-commit hook, command-line tool and GitHub Action all-in-one.
"""

from __future__ import annotations

import os
import sys
from itertools import chain

__all__ = ('DelayedReporter', 'Reporter', 'check', 'default_reporter')
__version__ = '1.2.3'

TYPE_CHECKING = False
if TYPE_CHECKING:
    import typing
    from collections.abc import Iterable

    from _typeshed import FileDescriptorOrPath
_DIRECTORY_DESCRIPTOR_UNSUPPORTED: BaseException = (
    SystemError('got directory descriptor on Windows')
    if os.name == 'nt'
    else NotImplementedError('directory descriptors are not supported')
)
_TYPE_MASK: int = 0xF000
_S_IFDIR: int = 0x4000


class _Handler:
    __slots__ = 'a', 'c', 'f', 'j', 'v'

    def __init__(self, *a):
        self.j, self.f, self.a = a
        self.v = None

    def __enter__(self):
        self.c = False
        return self

    def o(self):
        with self, open(self.a, 'wb'):
            ...

    @property
    def e(self, s='invalid fd (negative): %d', t='fd: %d'):  # ruff: ignore[property-with-parameters]
        r = self.v
        if r is None:
            a = self.a
            self.v = r = (t, s)[a < 0] % a if isinstance(a, int) else os.fsdecode(a)
        return r

    def __exit__(self, t, v, _):
        if t is None or not issubclass(t, OSError):
            return False
        self.j(self.e) if v.errno == 2 else self.f(str(v))
        self.c = True
        return True


class Reporter:
    """Type of all reporters that :func:`check` accepts as the ``reporter`` argument."""
    __slots__ = 'o',
    o: typing.IO[str] | None

    def __init__(self):
        """Initialize the reporter."""
        self.o = None

    def to(self, out: typing.IO[str] | None = None) -> typing.IO[str] | None:
        """Temporarily redirect the output of the reporter for one check.

        Args:
            out: The output stream to redirect to. If ``None``, the reporter will write
              to :data:`sys.stdout`.

        Returns:
            The previous output stream.

        """
        self.o, o = out, self.o
        return o

    @staticmethod
    def calculate_result(y: bool, x: bool, d: bool) -> int:
        """Set the result of the check as :attr:`r`.

        Returns:
            The exit code of the check. For the default implementation, this is a
            bitwise or of 1 (some files were not empty), 4 (some files or directories
            were absent and :ref:`-m <check-empty--m>` / :ref:`--may-not-exist
            <check-empty---may-not-exist>` was omitted) and 8 (caught :exc:`OSError`
            while processing some files), such that 0 is correctly the only return
            value that represents success. The 2 bit is skipped since 2 is the exit
            code of :class:`argparse.ArgumentParser` when it encounters invalid
            arguments.
        """
        return y | x << 2 | d << 3

    def report(self, z, w, r, x, y, d, p, a, b, t, n, v, c):  # ruff: ignore[too-many-arguments, too-many-positional-arguments]
        """Report the results of the check.

        Args:
            z: List of files that were not found.
            w: List of error messages for files that could not be processed.
            r: List of 2-tuples representing non-empty files and their sizes.
            x: Number of files that were not found.
            y: Number of non-empty files.
            d: Number of I/O errors encountered.
            p: Number of empty files.
            a: List of directories that were recursed into.
            b: List of empty file paths.
            t: Total size of non-empty files in bytes.
            n: Total number of files checked.
            v: The value of ``verbosity`` as passed to :func:`check`. For the default
              implementation, verbosity > 5 is equivalent to verbosity = 5, and a
              non-positive verbosity gives no output.
            c: The value of ``clear`` as passed to :func:`check`.
        """
        q = self.o
        q = (sys.stdout if q is None else q).write
        if a is not None:
            q('\nRecursing into directory: '.join(a))
            q('\n')
        if z is not None:
            q('\nNot found: '.join(z))
        q(
            f'{x} file{"s" if x > 1 else ""} not found\n'
            if x
            else 'All files were found\n'
        )
        if w is not None:
            q('\nError: '.join(w))
        if d:
            q(f'{d} I/O error{"s" if d > 1 else ""} encountered\n')
        if b is not None:
            q('\nEmpty: '.join(b))
        if v > 2:
            q(f'\n{p or "No"} empty file{"" if p == 1 else "s"}\n')
        if y:
            if r is not None:
                q(
                    ('\nCleared: ' if c else '\nNot empty: ').join(
                        chain(('',), map('%s (%d bytes)'.__mod__, r))
                    )
                )
                q('\n')
            q(f'{y} offending file{"s" if y > 1 else ""}\nTotal size: {t} bytes\n')
        elif n > x:
            q('All found files were empty\n')

    def reset_stream(self) -> None:
        """Reset the reporter, closing the output stream if appropriate."""
        q, self.o = self.o, None
        if q not in {None, sys.stdout, sys.stderr, sys.__stdout__, sys.__stderr__}:
            q.close()


class DelayedReporter(Reporter):
    """Only report the results only when :meth:`do_report` is called."""
    __slots__ = ('a',)

    def report(self, *a):  # ty: ignore[invalid-method-override]
        """Store the report arguments for later use."""
        self.a = a

    def do_report(self) -> None:
        """Conduct the report for the most recent check using this reporter."""
        super().report(*self.a)


default_reporter: Reporter = Reporter()
"""The default reporter used by :func:`check`."""


def check(
    files: Iterable[FileDescriptorOrPath],
    *,
    clear: bool = False,
    may_not_exist: bool = False,
    verbosity: typing.SupportsIndex = 2,
    reporter: Reporter = default_reporter,
) -> int:
    """Check the emptiness of files, recursing into directories if passed.

    Args:
        files: an iterable of file descriptors or paths representing the files and
          directories to check; directory descriptors (*nix) are not supported.
        clear: if ``True``, clear the contents of non-empty files; directories, notably,
          are not purged, but all files within should become empty.
        may_not_exist: if ``True``, do not treat absent files or directories as errors.
        verbosity: how much detail the program should print to stdout.
        reporter: The reporter to use for reporting the results. All output of this
          function is produced by the reporter.

    Returns:
        The integer exit code calculated by the reporter.
    """
    files = list(files)
    if not files:
        return 0
    k, j, t, n, o = [0] * 4, [], 0, len(files), files.pop
    u, e, _ = j.extend, j.pop, lambda v: lambda _, k=k: k.__setitem__(v, k[v] + 1)
    verbosity = max(0, type(verbosity).__index__(verbosity))
    if verbosity > 4:
        b = ['']
        f = b.append
    else:
        b, f = None, _(0)
    if verbosity > 3:
        v = ['']
        x = v.append
    else:
        v, x = None, lambda _: None
    if verbosity > 2:
        z, w = [''], ['']
        i = z.append, w.append
    else:
        z = w = None
        i = _(1), _(2)
    if verbosity > 1:
        r = []
        g = r.append
    else:
        r, g = None, _(3)
    while files:
        a = o()
        with _Handler(*i, a) as h:
            q = os.stat(a)
        if h.c:
            continue
        c = h.e
        if q.st_mode & _TYPE_MASK == _S_IFDIR:
            if isinstance(a, int):
                raise _DIRECTORY_DESCRIPTOR_UNSUPPORTED
            x(c)
            u(os.scandir(c))
            continue
        s = q.st_size
        if not s:
            f(c)
            continue
        g((c, s))
        t += s
        if clear:
            h.o()
    del o, files
    while j:
        m = e()
        a = m.path
        if m.is_dir():
            x(a)
            u(os.scandir(a))
            continue
        n += 1
        s = m.stat().st_size
        if not s:
            f(a)
            continue
        g((a, s))
        t += s
        if clear:
            _Handler(*i, a).o()
    x = k[1] if z is None else len(z) - 1
    d = k[2] if w is None else len(w) - 1
    y = k[3] if r is None else len(r)
    if verbosity:
        p = k[0] if b is None else len(b) - 1
        reporter.report(z, w, r, x, y, d, p, v, b, t, n, verbosity, clear)
    reporter.reset_stream()
    return reporter.calculate_result(*map(bool, (y, x and not may_not_exist, d)))


del TYPE_CHECKING
