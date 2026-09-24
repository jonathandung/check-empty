"""Abstract base classes for reporters."""

from __future__ import annotations

import abc as a

from .exceptions import NoReport

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

__all__ = ('DelayedReporterMixin', 'ReporterABC')


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
