"""The reporter API for :func:`~check_empty.check`."""

from __future__ import annotations

import abc as a
import itertools as i
import sys as s
from contextlib import suppress

from .constants import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, MutableMapping
    from typing import IO, Any, ClassVar, Final

__all__ = (
    'DelayedReporter',
    'DelayedReporterMixin',
    'DictReporter',
    'IncorrectKeynames',
    'IncorrectKeynamesLength',
    'IncorrectKeynamesType',
    'NoOutputMapping',
    'NoReport',
    'Reporter',
    'ReporterABC',
    'ReporterError',
    'SelfReporter',
)


class ReporterError(Exception):
    """Base class for all exceptions raised by reporters."""

    reporter: ReporterABC
    """The reporter concerned."""
    message: ClassVar[str]
    """The message of the exception."""

    def __init__(self, reporter: ReporterABC) -> None:
        """Initialize the exception.

        Args:
            reporter: the reporter in question.
        """
        super().__init__(self.message)
        self.reporter = reporter


class NoReport(ReporterError):
    """Raised when a delayed reporter is asked to report but has nothing to report."""

    reporter: DelayedReporterMixin
    """The reporter concerned."""
    message = 'nothing to report'


class IncorrectKeynames(ReporterError):
    """Base class for errors when :class:`DictReporter` gets invalid ``keynames``."""

    reporter: DictReporter
    """The reporter concerned."""


class IncorrectKeynamesLength(IncorrectKeynames):
    """Raised when the length of ``keynames`` is not 13."""

    message = 'keynames must have length 13'


class IncorrectKeynamesType(IncorrectKeynames):
    """Raised when ``keynames`` or anything within is of the wrong type."""

    message = 'keynames must either be None, or an iterable giving strings or None'


class NoOutputMapping(ReporterError):
    """Raised when a :class:`DictReporter` has no output mapping to write to."""

    message = 'no mapping to output to'


class ReporterABC(metaclass=a.ABCMeta):
    """Abstract base class for all reporters accepted by :func:`~check_empty.check`."""

    o: Any | None = None
    """The attribute that stores the output stream."""

    @a.abstractmethod
    def report(  # ruff: ignore[too-many-arguments, too-many-positional-arguments]
        self,
        z: list[str] | None,
        w: list[str] | None,
        a: list[str] | None,
        b: list[str] | None,
        r: list[tuple[str, int]] | None,
        x: int,
        y: int,
        d: int,
        p: int,
        n: int,
        t: int,
        v: int,
        c: bool,
        /,
    ) -> None:
        """Report the results of the check.

        Args:
            z: list of paths to files that were not found.
            w: list of error messages for files that could not be processed.
            a: list of directories that were recursed into.
            b: list of empty file paths.
            r: list of 2-tuples representing non-empty files and their sizes.
            x: number of files that were not found.
            y: number of non-empty files.
            d: number of I/O errors encountered.
            p: number of empty files.
            n: number of files checked.
            t: total size of non-empty files in bytes.
            v: the integer value of ``verbosity`` as passed to
              :func:`~check_empty.check`.
            c: the value of ``clear`` as passed to :func:`~check_empty.check`.

        All arguments are to be treated as positional-only. Besides, implementations
        should not mutate the lists or compute the return value from these parameters.
        """

    @staticmethod
    def calculate_result(y: bool, x: bool, d: bool, /) -> int:
        """Return the exit code of the check according to the parameters.

        The default implementation packs ``y``, ``x``, ``d`` into the first, third and
        fourth bits respectively, such that 0 is correctly the only return value that
        represents success. The second bit is skipped since 2 is the exit code of
        :class:`argparse.ArgumentParser` when it encounters invalid arguments.

        Args:
            y: whether any files were not empty.
            x: whether any files or directories were absent and
              :ref:`-m <check-empty--m>` /
              :ref:`--may-not-exist <check-empty---may-not-exist>` was omitted
            d: whether any :exc:`OSError` was caught while processing files.

        Returns:
            An integer derived from the arguments, which will be returned by
            :func:`~check_empty.check` and act as the exit code if
            :func:`~check_empty.__main__.main` instrumented the check.
        """
        return y | x << 2 | d << 3

    def to(self, out: Any) -> Any | None:  # ruff: ignore[any-type]
        """Redirect the output of the reporter for the next check.

        This may be, for instance, a file on disk, an in-memory object, or a socket.

        Returns:
            The previous output stream, or ``None`` if no redirection is in effect.
        """
        self.o, o = out, self.o
        return o

    def reset_out(self) -> None:
        """Undo the output redirection initiated by :meth:`to`, if any.

        This is called by :func:`~check_empty.check`. It is expected to perform cleanup
        accordingly.
        """
        self.o = None


class Reporter(ReporterABC):
    """Concrete and default reporter implementation that prints output to a stream."""

    if TYPE_CHECKING:
        o: IO[str] | None

        def to(self, out: IO[str] | None = None) -> IO[str] | None:
            """Temporarily redirect the output of the reporter for one check.

            Args:
                out: the output stream to redirect to. If ``None``, the reporter will
                  write to :data:`sys.stdout`.

            Returns:
                The previous output stream, or ``None`` if no redirection is in effect.

            """

    def report(  # ruff: ignore[too-many-arguments, too-many-positional-arguments]
        self,
        z: list[str] | None,
        w: list[str] | None,
        a: list[str] | None,
        b: list[str] | None,
        r: list[tuple[str, int]] | None,
        x: int,
        y: int,
        d: int,
        p: int,
        n: int,
        t: int,
        v: int,
        c: bool,
        /,
    ) -> None:
        """Report the results of the check.

        For this implementation, ``v > 5`` is equivalent to ``v == 5``, and a
        non-positive value of ``v`` makes the report return fast, giving no output.
        """
        if v <= 0:
            return
        q = self.o
        q = (s.stdout if q is None else q).write
        if a is not None:
            q('\nRecursing into directory: '.join(a))
        if z is not None:
            q('\nNot found: '.join(z))
        q(
            f'\n{x} file{"s" if x > 1 else ""} not found'
            if x
            else '\nAll files were found'
        )
        if w is not None:
            q('\nError: '.join(w))
        if d:
            q(f'\n{d} I/O error{"s" if d > 1 else ""} encountered')
        if b is not None:
            q('\nEmpty: '.join(b))
        if v > 2:  # ruff: ignore[magic-value-comparison]
            q(f'\n{p or "No"} empty file{"" if p == 1 else "s"}')
        if y:
            if r is not None:
                q(
                    ('\nCleared: ' if c else '\nNot empty: ').join(
                        i.chain(('',), map('%s (%d bytes)'.__mod__, r))
                    )
                )
            q(f'\n{y} offending file{"s" if y > 1 else ""}\nTotal size: {t} bytes\n')
        elif n > x:
            q('\nAll found files were empty\n')

    def reset_out(self) -> None:
        """Unset the output stream of the reporter and close it if appropriate."""
        q, self.o = self.o, None
        if q not in {None, s.stdout, s.stderr, s.__stdout__, s.__stderr__}:
            q.close()


class DictReporter(ReporterABC):
    """Dump the metrics into a dictionary-like object."""

    keynames: tuple[
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
    KEYNAME_LENGTH: Final = len(keynames)
    """The expected length of the ``keynames`` tuple, which is 13."""

    if TYPE_CHECKING:
        o: MutableMapping[str, Any] | None

        def to(self, out: MutableMapping[str, Any]) -> MutableMapping[str, Any] | None:
            """Redirect the output of the reporter for the next check.

            Args:
                out: the output mapping to redirect to.

            Returns:
                The previous output mapping, or ``None`` if no redirection is in effect.
            """

    def __init__(self, keynames: Iterable[str | None] | None = None) -> None:
        """Initialize the reporter.

        Args:
            keynames: a 13-tuple of strings or ``None`` to use as the keys in the
              output mapping. The order corresponds to the arguments of :meth:`report`.

        Raises:
            IncorrectKeynamesLength: if ``keynames`` is not of length 13.
            IncorrectKeynamesType: if ``keynames`` is not iterable, or any of its
              elements is not a string or ``None``.
        """
        if keynames is None:
            return
        if not isinstance(keynames, tuple):
            keynames = self._(keynames)  # ty: ignore[unsound-assignment]
        if len(keynames) != self.KEYNAME_LENGTH:
            raise IncorrectKeynamesLength(self)
        if not all(i is None or isinstance(i, str) for i in keynames):
            raise IncorrectKeynamesType(self)
        self.keynames = keynames

    def _(self, k: Iterable[Any]) -> tuple[Any, ...]:
        try:
            x = i.islice(k, self.KEYNAME_LENGTH)
        except TypeError as e:
            raise IncorrectKeynamesType(self) from e
        k = tuple(x)
        with suppress(StopIteration):
            next(x)
            raise IncorrectKeynamesLength(self)
        return k

    def out_fallback(self) -> MutableMapping[str, Any]:
        """Return the output mapping to use if none is set.

        Raises:
            NoOutputMapping: if the default implementation is used.
        """
        raise NoOutputMapping(self)

    def report(self, *a: Any) -> None:  # ruff: ignore[any-type]
        """Report the results of the check."""
        o, n = self.o, self.keynames
        if o is None:
            o = self.out_fallback()
        k = n[4]
        if k is not None:
            o[k] = dict(a[4])
        for k, v in i.chain(zip(n[:4], a[:4]), zip(n[5:], a[5:])):
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


class DelayedReporterMixin(ReporterABC):
    """Reporter mixin to report results on demand.

    Stores the arguments passed to the most recent :meth:`report` call as :attr:`a`,
    such that the actual report may be done much later, even repeatedly, unless another
    check uses the same reporter before then. Use with care.
    """

    a: tuple[Any, ...] | None = None
    """The aforementioned arguments as a :class:`tuple`."""

    def report(self, *a: Any) -> None:  # ruff: ignore[any-type]
        """Store the report arguments for later use."""
        self.a = a

    def do_report(self) -> None:
        """Conduct the report for the most recent check using this reporter.

        Raises:
            NoReport: if no report has been stored yet.
        """
        a = self.a
        if a is None:
            raise NoReport(self)
        super().report(*a)


class DelayedReporter(DelayedReporterMixin, Reporter):
    """The delayed version of the default reporter."""
