# Copyright © 2026 Jonathan Dung. All rights reserved.
# SPDX-License-Identifier: MIT
"""Utility to check the emptiness of files and directories.

Pre-commit hook, command-line tool and GitHub Action all-in-one.
"""

from __future__ import annotations

import os

__all__ = ('check',)
__version__ = '1.1.0'

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import IO

    from _typeshed import FileDescriptorOrPath
    from typing_extensions import Literal, SupportsIndex, TypeAlias

    ExitCode: TypeAlias = Literal[0, 1, 4, 5, 8, 9, 12, 13]
else:
    ExitCode = int
DIRECTORY_DESCRIPTOR_UNSUPPORTED: BaseException = (
    SystemError('somehow got directory descriptor on Windows')
    if os.name == 'nt'
    else NotImplementedError('directory descriptors are not supported')
)

TYPE_MASK: int = 0xF000
S_IFDIR: int = 0x4000


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


def check(  # ruff: ignore[too-many-branches, too-many-locals, too-many-statements]
    files: Iterable[FileDescriptorOrPath],
    *,
    clear: bool = False,
    may_not_exist: bool = False,
    verbosity: SupportsIndex = 2,
    out: IO[str] | None = None,
) -> ExitCode:
    """Check the emptiness of files, recursing into directories if passed.

    Args:
        files: an iterable of file descriptors or paths representing the files and
        directories to check; directory descriptors (Unix) are not supported.
        clear: if True, clear the contents of non-empty files; directories, notably,
        are not purged, but all files within should become empty.
        may_not_exist: if True, do not treat absent files or directories as errors.
        verbosity: how much detail the program should print to stdout; if 0, print
        nothing; verbosity > 5 is equivalent to verbosity = 5.
        out: The file to which output is printed; default `sys.stdout`.

    Returns:
        The integer exit code. A bitwise or of 1 (some files were not empty), 4 (some
        files or directories were absent and `-m`/`--may-not-exist` was omitted) and 8
        (caught OSError while processing some files), such that 0 is correctly the only
        return value that represents success. The 2 bit is skipped since 2 is the exit
        code of `argparse.ArgumentParser` when it encounters invalid arguments.

    """
    files = list(files)
    if not files:
        return 0
    k, j, t, n, o = [0] * 4, [], 0, len(files), files.pop
    u, e, _ = j.extend, j.pop, lambda v: lambda _, k=k: k.__setitem__(v, k[v] + 1)

    verbosity = type(verbosity).__index__(verbosity)
    if verbosity > 4:
        b = ['']
        f = b.append
    else:
        b, f = None, _(0)
    if verbosity > 3:
        rc = ['']
        ra = rc.append
    else:
        rc, ra = None, lambda _: None
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
        if q.st_mode & TYPE_MASK == S_IFDIR:
            if isinstance(a, int):
                raise DIRECTORY_DESCRIPTOR_UNSUPPORTED
            ra(c)
            u(os.scandir(c))
            continue
        s = q.st_size
        if not s:
            f(c)
            continue
        g(f'{c} ({s} bytes)')
        t += s
        if clear:
            h.o()
    del o, files
    while j:
        m = e()
        a = m.path
        if m.is_dir():
            ra(a)
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
            _Handler(*i, a).o()
    x = k[1] if z is None else len(z) - 1
    y = k[3] if r is None else len(r) - 1
    d = k[2] if w is None else len(w) - 1
    v = bool(y) | (bool(x) and not may_not_exist) << 2 | bool(d) << 3
    if verbosity <= 0:
        return v  # ty: ignore[invalid-return-type]
    q = (__import__('sys').stdout if out is None else out).write
    if rc is not None:
        q('\nRecursing into directory: '.join(rc))
        q('\n\n')
    if z is not None:
        q('\nNot found: '.join(z))
        q('\n')
    q(f'{x} file{"s" if x > 1 else ""} not found\n' if x else 'All files were found\n')
    if w is not None:
        q('\nError: '.join(w))
        q('\n')
    if d:
        q(f'{d} I/O error{"s" if d > 1 else ""} encountered\n')
    if b is not None:
        q('\nEmpty: '.join(b))
        q('\n')
    if verbosity > 2:
        p = k[0] if b is None else len(b) - 1
        q(f'{p} empty file{"" if p == 1 else "s"}\n' if p else 'No empty files\n')
    if y:
        if r is not None:
            q(('\nCleared: ' if clear else '\nNot empty: ').join(r))
            q('\n\n')
        q(f'{y} offending file{"s" if y > 1 else ""}\nTotal size: {t} bytes\n')
    elif n > x:
        q('All found files were empty\n')
    return v  # ty: ignore[invalid-return-type]
