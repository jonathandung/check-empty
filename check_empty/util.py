"""Utility functions for :mod:`check_empty`."""

from __future__ import annotations

from contextlib import suppress

from .constants import ENOENT, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from tarfile import TarFile
    from types import TracebackType
    from typing import Any

    from typing_extensions import Self
__all__ = ('try_tar',)


def try_tar(a: str, f: Callable[[TarFile], Any]) -> bool:
    """Open a file as a .tar archive and return success.

    Since :func:`tarfile.is_tarfile` calls :func:`tarfile.open` internally and
    discards the result, using the LBYL approach ends up opening the file twice,
    incurring twice the I/O cost.
    Thus, the resultant tarfile is recorded by the callback ``f`` via which the user
    may retrieve it later. The tarfile is not returned directly because the boolean
    return value allows this function to be used as a condition in an if-elif-else
    block, which is integral to the handling of multiple archive formats.

    Args:
        a: the string path to the file
        f: the callback

    Returns:
        Whether the archive was opened and appended to ``e`` with no errors.
    """
    import tarfile as m

    with suppress(m.TarError):
        f(m.open(a))  # ruff: ignore[open-file-with-context-handler]
        return True
    return False


class Handler:
    __slots__ = 'a', 'c', 'f', 'j', 'v'
    a: int | str
    c: bool
    f: Callable[[str], None]
    j: Callable[[str], None]
    v: str | None

    def __init__(self, *a: Any) -> None:  # ruff: ignore[any-type]
        self.j, self.f, self.a = a
        self.v = None

    def __enter__(self) -> Self:
        self.c = False
        return self

    def o(self) -> None:
        with self, open(self.a, 'wb'):
            ...

    @property
    def e(self, s: str = 'invalid fd (negative): %d', t: str = 'fd: %d') -> str:  # ruff: ignore[property-with-parameters]
        r = self.v
        if r is None:
            a = self.a
            self.v = r = (t, s)[a < 0] % a if isinstance(a, int) else a
        return r

    def __exit__(
        self,
        t: type[BaseException] | None,
        v: BaseException | None,
        _: TracebackType | None,
    ) -> bool:
        if t is None or not isinstance(v, OSError):
            return False
        self.j(self.e) if v.errno == ENOENT else self.f(str(v))
        self.c = True
        return True


del TYPE_CHECKING
