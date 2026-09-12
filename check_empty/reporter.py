"""The reporter API for :func:`~check_empty.check`."""

from __future__ import annotations

import sys as s

from .constants import TYPE_CHECKING

if TYPE_CHECKING:
    import typing

__all__ = ('DelayedReporter', 'Reporter')


class Reporter:
    """Type of all reporters accepted by :func:`check` for the ``reporter`` argument."""

    __slots__ = ('o',)
    o: typing.IO[str] | None

    def __init__(self) -> None:
        """Initialize the reporter."""
        self.o = None

    def to(self, out: typing.IO[str] | None = None) -> typing.IO[str] | None:
        """Temporarily redirect the output of the reporter for one check.

        Args:
            out: The output stream to redirect to. If ``None``, the reporter will write
              to :data:`sys.stdout`.

        Returns:
            The previous output stream, or ``None`` if no redirection is in effect.

        """
        self.o, o = out, self.o
        return o

    @staticmethod
    def calculate_result(y: bool, x: bool, d: bool) -> int:
        """Set the result of the check as :attr:`r`.

        Returns:
            The exit code of the check. For the default implementation, this is a
            bitwise or of 1 (some files were not empty), 4 (some files or directories
            were absent and :ref:`-m <check-empty--m>` /
            :ref:`--may-not-exist <check-empty---may-not-exist>` was omitted) and 8
            (caught :exc:`OSError` while processing some files), such that 0 is
            correctly the only return value that represents success. The 2 bit is
            skipped since 2 is the exit code of :class:`argparse.ArgumentParser` when
            it encounters invalid arguments.
        """
        return y | x << 2 | d << 3

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
        t: int,
        n: int,
        v: int,
        c: bool,
    ) -> None:
        """Report the results of the check.

        Args:
            z: List of paths to files that were not found.
            w: List of error messages for files that could not be processed.
            a: List of directories that were recursed into.
            b: List of empty file paths.
            r: List of 2-tuples representing non-empty files and their sizes.
            x: Number of files that were not found.
            y: Number of non-empty files.
            d: Number of I/O errors encountered.
            p: Number of empty files.
            t: Total size of non-empty files in bytes.
            n: Total number of files checked.
            v: The integer value of ``verbosity`` as passed to :func:`check`. For the
              default implementation, verbosity > 5 is equivalent to verbosity = 5, and
              a non-positive verbosity gives no output.
            c: The value of ``clear`` as passed to :func:`check`.
        """
        if v <= 0:
            return
        q = self.o
        q = (s.stdout if q is None else q).write
        if a is not None:
            q('\nRecursing into directory: '.join(a))
            q('\n')
        if z is not None:
            q('\nNot found: '.join(z))
        q(
            f'{x} file{"s" if x > 1 else ""} not found\n'
            if x
            else 'All files were found\n'
        )
        if w is not None:
            q('\nError: '.join(w))
        if d:
            q(f'{d} I/O error{"s" if d > 1 else ""} encountered\n')
        if b is not None:
            q('\nEmpty: '.join(b))
        if v > 2:  # ruff: ignore[magic-value-comparison]
            q(f'\n{p or "No"} empty file{"" if p == 1 else "s"}\n')
        if y:
            if r is not None:
                q(
                    ('\nCleared: ' if c else '\nNot empty: ').join(
                        __import__('itertools').chain(
                            ('',), map('%s (%d bytes)'.__mod__, r)
                        )
                    )
                )
                q('\n')
            q(f'{y} offending file{"s" if y > 1 else ""}\nTotal size: {t} bytes\n')
        elif n > x:
            q('All found files were empty\n')

    def reset_stream(self) -> None:
        """Reset the reporter, closing the output stream if appropriate."""
        q, self.o = self.o, None
        if q not in {None, s.stdout, s.stderr, s.__stdout__, s.__stderr__}:
            q.close()


class DelayedReporter(Reporter):
    """Only report the results only when :meth:`do_report` is called."""

    __slots__ = ('a',)

    def report(self, *a: typing.Any) -> None:  # ruff: ignore[any-type] # ty: ignore[invalid-method-override]
        """Store the report arguments for later use."""
        self.a = a

    def do_report(self) -> None:
        """Conduct the report for the most recent check using this reporter."""
        super().report(*self.a)
