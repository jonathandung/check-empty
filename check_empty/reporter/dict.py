"""Defines reporters that output into mutable mappings."""

from __future__ import annotations

import itertools as i

from . import exceptions as _
from .abc import ReporterABC

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable, MutableMapping
    from typing import Any, Final

__all__ = ('DictReporter', 'SelfReporter')


class DictReporter(ReporterABC):
    """Dump the metrics into a dictionary-like object."""

    keys: tuple[
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
    ] = (
        'not_found',
        'io_errors',
        'recursed_into',
        'empty_files',
        'non_empty_files',
        'num_not_found',
        'num_non_empty',
        'num_io_errors',
        'num_empty',
        'num_files',
        'total_size',
        'verbosity',
        'cleared',
    )
    KEYNAME_LENGTH: Final = len(keys)
    """The expected length of the ``keys`` tuple, which is 13."""

    if TYPE_CHECKING:
        o: MutableMapping[str, Any] | None

        def to(self, out: MutableMapping[str, Any]) -> MutableMapping[str, Any] | None:
            """Redirect the output of the reporter for the next check.

            Args:
                out: the output mapping to redirect to.

            Returns:
                The previous output mapping, or ``None`` if no redirection is in effect.
            """

    def __init__(self, keys: Iterable[str | None] | None = None) -> None:
        """Initialize the reporter.

        Args:
            keys: a 13-tuple of strings or ``None`` to use as the keys in the
              output mapping. The order corresponds to the arguments of :meth:`report`.

        Raises:
            IncorrectKeynamesLength: if ``keys`` is not of length 13.
            IncorrectKeynamesType: if ``keys`` is not iterable, or any of its
              elements is not a string or ``None``.
        """
        if keys is None:
            return
        if not isinstance(keys, tuple):
            keys = self._(keys)  # ty: ignore[unsound-assignment]
        if len(keys) != self.KEYNAME_LENGTH:
            raise _.IncorrectKeynamesLength(self)
        if not all(i is None or isinstance(i, str) for i in keys):
            raise _.IncorrectKeynamesType(self)
        self.keys = keys

    def _(
        self,
        k: Iterable[Any],
        # ruff: ignore[missing-type-function-argument, function-call-in-default-argument]
        s=__import__('contextlib').suppress(StopIteration),
    ) -> tuple[Any, ...]:
        try:
            x = i.islice(k, self.KEYNAME_LENGTH)
        except TypeError as e:
            raise _.IncorrectKeynamesType(self) from e
        k = tuple(x)
        with s:
            next(x)
            raise _.IncorrectKeynamesLength(self)
        return k

    def out_fallback(self) -> MutableMapping[str, Any]:
        """Return the output mapping to use if none is set.

        Raises:
            NoOutputMapping: if the default implementation is used.
        """
        raise _.NoOutputMapping(self)

    def report(self, *a: Any) -> None:  # ruff: ignore[any-type]
        """Report the results of the check."""
        o, n = self.o, self.keys
        if o is None:
            o = self.out_fallback()
        k = n[4]
        if k is not None:
            o[k] = dict(a[4])
        for k, v in i.chain(
            zip(n[:4], a[:4], strict=True), zip(n[5:], a[5:], strict=True)
        ):
            if k is not None:
                o[k] = v


class SelfReporter(DictReporter):
    """Assigns check data to the attributes of the reporter itself."""

    def out_fallback(self) -> MutableMapping[str, Any]:
        """Return the instance dictionary."""
        return self.__dict__

    if TYPE_CHECKING:

        def __getattr__(self, name: str) -> Any:  # ruff: ignore[any-type]
            """Does not exist at runtime.

            This is only implemented at type-check time because the exact attributes
            and their types are not statically known.
            """
