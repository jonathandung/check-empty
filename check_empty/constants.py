"""Defines constants used by :mod:`check_empty`."""

from __future__ import annotations

import os

__all__ = (
    'ARCHIVE_FORMATS',
    'DIRFD_UNSUPPORTED',
    'ENOENT',
    'S_IFDIR',
    'TYPE_MASK',
    'RecurseInto',
)
TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Final
TYPE_MASK: Final = 0xF000
"""The mask that extracts the type of a file from its mode bits using bitwise and."""
S_IFDIR: Final = 0x4000
"""Equal to :data:`stat.S_IFDIR`."""
ENOENT: Final = 2
"""Equal to :data:`errno.ENOENT`."""
DIRFD_UNSUPPORTED: Final = (
    SystemError('got directory descriptor on Windows')
    if os.name == 'nt'
    else NotImplementedError('directory descriptors are not supported')
)
"""The error raised when :func:`~check_empty.check` gets a directory descriptor."""


class RecurseInto(__import__('enum').IntFlag):
    """Flags for the ``recurse_into`` argument of :func:`~check_empty.check`."""

    NONE = 0
    """Don't recurse into any archives; the default behaviour."""
    ZIP = 1
    """Recurse into .zip archives."""
    TAR = 2
    """Recurse into .tar archives."""
    RAR = 4
    """Recurse into .rar archives; requires :mod:`rarfile`."""
    Z7 = 8
    """Recurse into .7z archives; requires :mod:`py7zr`.

    The unfortunate name of this member is due to the fact that Python identifiers
    cannot start with a digit.
    """
    TYPICAL = 15
    """Recurse into the most common archive types, namely .zip, .tar, .7z, and .rar."""
    AR = 16
    """Recurse into .a, .ar and .lib archives; requires `arpy <https://github.com/onekey-sec/arpy>`__."""
    LZH = 32
    """Recurse into .lzh and .lha archives; requires `lhafile <https://github.com/FrodeSolheim/python-lhafile>`__."""
    ACE = 64
    """Recurse into .ace archives; requires `acefile <https://apidoc.roe.ch/acefile/latest>`__."""
    ALL = 127
    """Recurse into all supported archive types."""


ARCHIVE_FORMATS: Final = tuple(RecurseInto)
"""A tuple of the flags corresponding to each supported archive type ordered by bit."""
del os, TYPE_CHECKING
