# Copyright © 2026 Jonathan Dung. All rights reserved.
# SPDX-License-Identifier: MIT
"""Utility to check the emptiness of files.

Pre-commit hook, command-line tool and GitHub Action all-in-one.
"""

from __future__ import annotations

import os

from . import constants, reporter, util

if constants.TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import SupportsIndex

    from _typeshed import FileDescriptorOrPath

__all__ = ('check', 'default_reporter')
__version__ = '2.0.0'
"""The version of the package."""
default_reporter: reporter.Reporter = reporter.Reporter()
"""The default reporter used by :func:`check`."""


def check(
    files: Iterable[FileDescriptorOrPath],
    *,
    clear: bool = False,
    may_not_exist: bool = False,
    verbosity: SupportsIndex = 2,
    recurse_into: SupportsIndex = constants.RecurseInto.NONE,
    reporter: reporter.ReporterABC = default_reporter,
) -> int:
    # ruff: ignore[docstring-missing-exception]
    r"""Check the emptiness of files, recursing into directories if passed.

    If using a custom reporter and you want to use all the information that can be
    gathered during the check, remember to pass a ``verbosity`` greater than or equal
    to 5, since some parameters to :meth:`~check_empty.reporter.Reporter.report` will
    take values of ``None`` otherwise.

    Args:
        files: an iterable of file descriptors or paths representing the files and
          directories to check; directory descriptors (\*nix) are not supported.
        clear: if ``True``, clear the contents of non-empty files; directories, notably,
          are not purged, but all files within should become empty.
        may_not_exist: if ``True``, do not treat absent files or directories as errors.
        verbosity: how much detail the program should print to stdout.
        recurse_into: a bitwise or of flags indicating which types of archives to
          recurse into; by default, all archives are treated as regular files.
        reporter: The reporter to use for reporting the results. All output of this
          function is produced by the reporter.

    Returns:
        The integer exit code calculated by the reporter.

    """
    files = list(files)
    if not files:
        return 0
    k, j, t, n, o = [0] * 5, [], 0, len(files), files.pop
    u, e, _ = j.extend, j.pop, lambda v: lambda _, k=k: k.__setitem__(v, k[v] + 1)
    verbosity, recurse_into = (type(x).__index__(x) for x in (verbosity, recurse_into))
    # ruff: disable[magic-value-comparison]
    if verbosity > 4:
        b = ['']
        f = b.append
    else:
        b, f = None, _(0)
    if verbosity > 3:
        v, ra = [''], ['']
        x, aa = v.append, ra.append
    else:
        v = ra = None
        x = aa = lambda _: None
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
    # ruff: enable[magic-value-comparison]
    zp, tr, rr, z7, lh = map(
        recurse_into.__and__,
        filter(lambda x: x > 0 == x & (x - 1), constants.RecurseInto),
    )
    an = bool(recurse_into)
    if an:
        from . import archives as ar
    md = 'a' if clear else 'r'
    if constants.TYPE_CHECKING:
        import tarfile as tr
        import zipfile as zp

        import lhafile as lh
        import py7zr as z7
        import rarfile as rr
    else:
        if tr:
            import tarfile as tr
        if zp:
            import zipfile as zp
        if lh:
            import lhafile as lh
        if z7:
            import py7zr as z7
        if rr:
            import rarfile as rr

    def ha(a: str) -> bool:
        if not an:
            return False

        def c() -> None:
            nonlocal t
            g(q)
            t += s

        def e() -> None:
            c() if s else f(a)

        def w() -> None:
            if s:
                if clear:
                    raise NotImplementedError(m)
                c()
            else:
                f(a)

        y = []
        if tr and util.try_tar(a, y.append):
            d = y.pop()
            aa(a)
            for r in d.getmembers():
                a, s = q = r.name, r.size
                e()
            if clear:
                ar.purge_tar(d)
        elif zp and zp.is_zipfile(a):
            with zp.ZipFile(a, md) as d:
                aa(a)
                for r in d.infolist():
                    a, s = q = r.filename, r.file_size
                    if s:
                        c()
                        if clear:
                            ar.clear_file_in_zip(d, r)
                    else:
                        f(a)
        elif z7 and z7.is_7zfile(a):
            with z7.SevenZipFile(a) as d:
                aa(a)
                for r in d.files:
                    a, s = q = r.filename, r.origin.stat().st_size
                    e()
                if clear:
                    ar.purge_7z(d)
        elif rr and rr.is_rarfile(a):
            m = 'Cannot clear files in RAR archives'
            with rr.RarFile(a) as d:
                aa(a)
                for r in d.infolist():
                    a, s = q = r.filename, r.file_size
                    w()
        else:
            try:
                d = lh.LhaFile(a)
            except (RuntimeError, lh.BadLhafile):
                return False
            m = 'Cannot clear files in LHA archives'
            aa(a)
            for r in d.filelist:
                a, s = q = r.filename, r.file_size
                w()
        return True

    def hb(a: str) -> bool:
        try:
            return ha(a)
        except Exception as e:  # ruff: ignore[blind-except]
            i[1](str(e))
            return True

    while files:
        a, q = o(), None
        m = isinstance(a, int)
        if not m:
            a = os.fsdecode(a)
            if hb(a):
                continue
        with util.Handler(*i, a) as h:
            q = os.stat(a)  # ruff: ignore[os-stat]
        if q is None:
            continue
        c = h.e
        if q.st_mode & constants.TYPE_MASK == constants.S_IFDIR:
            if m:
                raise constants.DIRFD_UNSUPPORTED
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
        if hb(a):
            continue
        n += 1
        s = m.stat().st_size
        if not s:
            f(a)
            continue
        g((a, s))
        t += s
        if clear:
            util.Handler(*i, a).o()
    del j
    x, d = k[1] if z is None else len(z) - 1, k[2] if w is None else len(w) - 1
    y, p = k[3] if r is None else len(r), k[0] if b is None else len(b) - 1
    reporter.report(z, w, v, b, r, x, y, d, p, n, t, verbosity, clear)
    reporter.reset_out()
    return reporter.calculate_result(*map(bool, (y, x and not may_not_exist, d)))
