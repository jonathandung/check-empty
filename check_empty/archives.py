"""Functions used to clear files in archives."""

from __future__ import annotations

import os
from itertools import filterfalse
from operator import attrgetter
from tempfile import NamedTemporaryFile

__all__ = (
    'AR_FS',
    'AR_MAG',
    'AR_NAME_SIZE',
    'clear_file_in_zip',
    'purge_7z',
    'purge_ar',
    'purge_tar',
)
_ = __import__('io').BytesIO()
AR_FS: Final = b'%-16b0           0     0     100644  %-10d`\n%b'
AR_MAG: Final = b'!<arch>\n'
AR_NAME_SIZE: Final = 16
AR_SKIP: Final[
    frozenset[
        Literal[b'/', b'//', b'/SYM64/', b'__.SYMDEF', b'__.SYMDEF SORTED'] | None
    ]
] = frozenset((b'/', b'//', b'/SYM64/', b'__.SYMDEF', b'__.SYMDEF SORTED', None))
TYPE_CHECKING = False
if TYPE_CHECKING:
    import tarfile
    import zipfile
    from collections.abc import Callable, Iterable
    from typing import Final, Literal

    import py7zr
    from arpy import Archive


def clear_file_in_zip(z: zipfile.ZipFile, i: zipfile.ZipInfo) -> None:
    """Clear the contents of a file in a .zip archive."""
    z.writestr(i, b'')


def purge_7z(z: py7zr.SevenZipFile) -> None:
    """Clear the contents of each file in a .7z archive."""
    x = z.filename
    if x is None:
        raise NotImplementedError
    y = z.namelist()
    with __import__('py7zr').SevenZipFile(x, 'w') as a:
        for n in y:
            a.writef(_, n)


def purge_tar(t: tarfile.TarFile) -> None:
    """Clear the contents of each file in a .tar archive."""
    x = t.name
    if x is None:
        raise NotImplementedError
    n = t.getmembers()
    t.close()
    import tarfile as z

    with (
        NamedTemporaryFile(suffix='.tar.gz', delete=False) as p,
        z.open(fileobj=p, mode='w:gz') as f,
    ):
        a = f.addfile
        for m in n:
            a(z.TarInfo(m.name))
    os.replace(p.name, x)


def purge_ar(a: Archive, g: int) -> None:
    """Clear the contents of each file in a .a, .ar or .lib archive."""
    a.read_all_headers()
    i, n = a.headers, a.file.name
    a.close()
    if not i:
        os.truncate(n, 8)
        return

    with NamedTemporaryFile(suffix='.a', delete=False) as f:
        w = f.write
        w(AR_MAG)
        q = filterfalse(AR_SKIP.__contains__, map(attrgetter('name'), i))
        _purge_ar_gnu(tuple(q), w) if i[0].type == g else _purge_ar_bsd(q, w)
    os.replace(f.name, n)


def _purge_ar_bsd(q: Iterable[bytes], w: Callable[[bytes], int]) -> None:
    """Clear the contents of each file in a BSD .a, .ar or .lib archive."""
    for m in q:
        x = len(m)
        b = b' ' in m or x > AR_NAME_SIZE
        w(AR_FS % (b'#1/%d' % x if b else m, x, m if b else b''))


def _purge_ar_gnu(q: tuple[bytes, ...], w: Callable[[bytes], int]) -> None:
    """Clear the contents of each file in a GNU .a, .ar or .lib archive."""
    c, d = 0, {}
    for m in q:
        x = len(m)
        if b' ' in m or x >= AR_NAME_SIZE:
            d[m] = c
            c += x + 1
    if d:
        t = bytearray(1).join(d)
        t.append(0)
        x = len(t)
        w(AR_FS % (b'//', x, t))
        if x & 1:
            w(b'\n')
    for m in q:
        z = d.get(m)
        m += b'/' if z is None else b'/%d' % z  # ruff: ignore[redefined-loop-name]
        w(AR_FS % (m, len(m), b''))


del TYPE_CHECKING
