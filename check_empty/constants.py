"""Defines constants used by :mod:`check_empty`."""

from __future__ import annotations

import os

TYPE_CHECKING: bool = False
if TYPE_CHECKING:
    import typing
__all__ = ('DIRFD_UNSUPPORTED', 'ENOENT', 'S_IFDIR', 'TYPE_MASK', 'RecurseInto')
TYPE_MASK: typing.Final = 0xF000
"""This mask extracts the type of a file from its mode bits from :func:`os.stat`."""
S_IFDIR: typing.Final = 0x4000
"""Equal to :const:`stat.S_IFDIR`."""
ENOENT: typing.Final = 2
"""Equal to :const:`errno.ENOENT`."""
DIRFD_UNSUPPORTED: typing.Final[BaseException] = (
    SystemError('got directory descriptor on Windows')
    if os.name == 'nt'
    else NotImplementedError('directory descriptors are not supported')
)
"""The exception raised when a directory descriptor is passed to :func:`check`."""


class RecurseInto(__import__('enum').IntFlag):
    """Flags for the ``recurse_into`` argument of :func:`check_empty.check`."""

    NONE = 0
    """Don't recurse into any archives; the default behaviour."""
    ZIP = 1
    """Recurse into .zip archives."""
    TAR = 2
    """Recurse into .tar archives."""
    RAR = 4
    """Recurse into .rar archives; requires :mod:`!rarfile`."""
    _7Z = 8
    """Recurse into .7z archives; requires :mod:`!py7zr`."""
    LZH = 16
    """Recurse into .lzh and .lha archives; requires :mod:`!lhafile`."""
    ALL = 31
    """Recurse into all archive types."""


del os
