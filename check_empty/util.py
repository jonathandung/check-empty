"""Utility functions for :mod:`check_empty`."""

from __future__ import annotations

from contextlib import suppress

from .constants import ENOENT, TYPE_CHECKING

if TYPE_CHECKING:
    import tarfile
    from collections.abc import Callable
    from types import TracebackType
    from typing import Any

    from typing_extensions import Self
__all__ = ('Handler', 'try_tar')


def try_tar(a: str, f: Callable[[tarfile.TarFile], Any]) -> bool:
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
    """Used to handle errors when opening a file."""

    __slots__ = 'a', 'c', 'f', 'j', 'v'
    a: int | str
    """The file descriptor or string path to the file being handled."""
    c: bool
    """Whether an I/O error was handled."""
    f: Callable[[str], None]
    """The function to call when handling an I/O error.

    Should take a string representing the error message as the only argument and
    preferably return ``None``.
    """
    j: Callable[[str], None]
    """The function to call when handling the case where the file is missing.

    Should take the path to the file or a string encapsulating the validity of the file
    descriptor as the only argument and preferably return ``None``.
    """
    v: str | None
    """The cached value of :attr:`e`."""

    def __init__(self, *a: Any) -> None:  # ruff: ignore[any-type]
        """Initialize the handler."""
        self.j, self.f, self.a = a
        self.v = None

    def __enter__(self) -> Self:
        """Enter the handler context.

        Returns:
            The handler itself.
        """
        self.c = False
        return self

    def o(self) -> None:
        """Clear the file immediately."""
        with self, open(self.a, 'wb'):
            ...

    @property
    def e(self, s: str = 'invalid fd (negative): %d', t: str = 'fd: %d') -> str:  # ruff: ignore[property-with-parameters]
        """The file path itself, or the file descriptor coerced to a string."""
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
        """Exit the handler context.

        Returns:
            Whether there was an exception that is to be suppressed.
        """
        if t is None or not isinstance(v, OSError):
            return False
        self.j(self.e) if v.errno == ENOENT else self.f(str(v))
        self.c = True
        return True


del TYPE_CHECKING
