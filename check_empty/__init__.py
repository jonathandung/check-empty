# Copyright © 2026 Jonathan Dung. All rights reserved.
# SPDX-License-Identifier: MIT
"""Utility to check the emptiness of files and directories.

Pre-commit hook, command-line tool and GitHub Action all-in-one.
"""

from __future__ import annotations

import os

__all__ = ('check',)
__version__ = '0.6.0'

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable

    from _typeshed import FileDescriptorOrPath
    from typing_extensions import Literal, SupportsIndex

DIRECTORY_DESCRIPTOR_UNSUPPORTED: BaseException = (
    SystemError('got directory descriptor on Windows??')
    if os.name == 'nt'
    else NotImplementedError('directory descriptors are not supported')
)


class _Handler:
    __slots__ = 'a', 'c', 'f', 'j', 'v'

    def __init__(self, *a):
        self.j, self.f, self.a = a
        self.v = None

    def __enter__(self):
        self.c = False
        return self

    @property
    def e(self, s='invalid fd (negative): %d', t='fd: %d'):  # ruff: ignore[property-with-parameters]
        r = self.v
        if r is not None:
            return r
        a = self.a
        self.v = r = (s if a < 0 else t) % a if isinstance(a, int) else os.fsdecode(a)
        return r

    def _x(self, v):
        self.j(self.e) if v.errno == 2 else self.f(str(v))

    def __exit__(self, t, v, _):
        if t is None or not issubclass(t, OSError):
            return False
        self._x(v)
        self.c = True
        return True


def check(  # ruff: ignore[too-many-branches, too-many-locals, too-many-statements]
    files: Iterable[FileDescriptorOrPath],
    *,
    clear: bool = False,
    may_not_exist: bool = False,
    verbosity: SupportsIndex = 2,
) -> Literal[0, 1, 4, 5, 8, 9, 12, 13]:
    """Check the emptiness of files and directories.

    Args:
        files: an iterable of file descriptors or paths representing the files and
        directories to check; directory descriptors (Unix) are not supported.
        clear: if True, clear the contents of non-empty files; directories, notably,
        are not purged, but all files within should become empty.
        may_not_exist: if True, do not treat absent files or directories as errors.
        verbosity: how much detail the program should print to stdout; if 0, print
        nothing; verbosity > 5 is equivalent to verbosity = 5.

    Returns:
        The integer exit code. A bitwise or of 1 (some files were not empty), 4 (some
        files or directories were absent and `-m`/`--may-not-exist` was not specified)
        and 8 (caught OSError while processing some files), such that 0 is the only
        return value that represents success as expected. The 2 bit is skipped since it
        conflicts with the exit code of `argparse.ArgumentParser` when it encounters
        invalid arguments.

    """
    files = list(files)
    if not files:
        return 0
    k, j, t, n, o = [0] * 4, [], 0, len(files), files.pop
    u, e = j.extend, j.pop

    def _(v, k=k):
        def f(_):
            k[v] += 1

        return f

    verbosity = type(verbosity).__index__(verbosity)
    if verbosity > 4:
        b = ['']
        f = b.append
    else:
        b, f = None, _(0)
    if verbosity > 2:
        z, w = [''], ['']
        i = z.append, w.append
    else:
        z = w = None
        i = _(1), _(2)
    if verbosity > 1:
        r = ['']
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
        if (q.st_mode >> 12) & 15 == 4:
            if isinstance(a, int):
                raise DIRECTORY_DESCRIPTOR_UNSUPPORTED
            if verbosity > 3:
                print('Recursing into directory:', c)
            u(os.scandir(c))
            continue
        s = q.st_size
        if not s:
            f(c)
            continue
        g(f'{c} ({s} bytes)')
        t += s
        if clear:
            with h, open(a, 'wb'):
                ...
    del o, files
    while j:
        m = e()
        a = m.path
        if m.is_dir():
            if verbosity > 3:
                print('Recursing into directory:', a)
            u(os.scandir(a))
            continue
        n += 1
        s = m.stat().st_size
        if not s:
            f(a)
            continue
        g(f'{a} ({s} bytes)')
        t += s
        if clear:
            with _Handler(*i, a), open(a, 'wb'):
                ...
    x = k[1] if z is None else len(z) - 1
    y = k[3] if r is None else len(r) - 1
    d = k[2] if w is None else len(w) - 1
    v = bool(y) | (bool(x) and not may_not_exist) << 2 | bool(d) << 3
    if verbosity <= 0:
        return v  # ty: ignore[invalid-return-type]
    if verbosity > 2:
        print(*z, sep='\nNot found: ')
    print(f'{x} file{"" if x == 1 else "s"} not found' if x else 'All files were found')
    if verbosity > 2:
        print(*w, sep='\nError: ')
    if d:
        print(f'{d} I/O error{"s" if d > 1 else ""} encountered')
    if verbosity > 4:
        print(*b, sep='\nEmpty: ')
    if verbosity > 2:
        p = k[0] if b is None else len(b) - 1
        print(f'{p} empty file{"" if p == 1 else "s"}' if p else 'No empty files')
    if y:
        if verbosity > 1:
            print(*r, sep='\nCleared: ' if clear else '\nNot empty: ', end='')
            print(end='\n\n')
        print(y, 'offending files' if y > 1 else 'offending file')
        print(f'Total size: {t} bytes')
    elif n > x:
        print('All found files were empty')
    return v  # ty: ignore[invalid-return-type]
