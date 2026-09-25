"""The reporter API for :func:`~check_empty.check`."""

from __future__ import annotations

import itertools as i
import sys as s

from check_empty.reporter import abcdef, dct as dct

__all__ = ('DelayedReporter', 'Reporter')
TYPE_CHECKING = False


class Reporter(abcdef.ReporterABC):
    """Concrete and default reporter implementation that prints output to a stream."""

    if TYPE_CHECKING:
        from typing import IO

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
        w: list[OSError] | None,
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
            q('\nError: '.join(i.chain(('',), map(str, w))))
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


class DelayedReporter(abcdef.DelayedReporterMixin, Reporter):
    """The delayed version of the default reporter."""


del TYPE_CHECKING
