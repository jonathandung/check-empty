"""Defines constants used by :mod:`check_empty`."""

from __future__ import annotations

import os

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Final
__all__ = (
    'DIRFD_UNSUPPORTED',
    'ENOENT',
    'S_IFDIR',
    'TYPE_CHECKING',
    'TYPE_MASK',
    'RecurseInto',
)
TYPE_MASK: Final = 0xF000
"""This mask extracts the type of a file from its mode bits from :func:`os.stat`."""
S_IFDIR: Final = 0x4000
"""Equal to :data:`stat.S_IFDIR`."""
ENOENT: Final = 2
"""Equal to :data:`errno.ENOENT`."""
DIRFD_UNSUPPORTED: Final[BaseException] = (
    SystemError('got directory descriptor on Windows')
    if os.name == 'nt'
    else NotImplementedError('directory descriptors are not supported')
)
"""Error raised when a directory descriptor is passed to :func:`~check_empty.check`."""


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
    """Recurse into .a, .ar and .lib archives; requires :mod:`!arpy`."""
    LZH = 32
    """Recurse into .lzh and .lha archives; requires :mod:`!lhafile`."""
    ACE = 64
    """Recurse into .ace archives; requires :mod:`!acefile`."""
    ALL = 127
    """Recurse into all archive types."""


ARCHIVE_FORMATS: Final = tuple(
    filter(lambda x: x > 0 == x & (x - 1), RecurseInto)
    if __import__('sys').version_info < (3, 11)
    else RecurseInto
)
del os, TYPE_CHECKING
