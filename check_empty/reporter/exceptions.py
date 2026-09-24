"""Declares exceptions raised by reporters."""

from __future__ import annotations

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import ClassVar

    from .abc import DelayedReporterMixin, ReporterABC
    from .dict import DictReporter

__all__ = (
    'IncorrectKeynames',
    'IncorrectKeynamesLength',
    'IncorrectKeynamesType',
    'NoOutputMapping',
    'NoReport',
    'ReporterError',
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
    """A delayed reporter was asked to report but had nothing to report."""

    reporter: DelayedReporterMixin
    """The reporter concerned."""
    message = 'nothing to report'


class IncorrectKeynames(ReporterError):
    """A :class:`check_empty.reporter.dict.DictReporter` got invalid ``keys``."""

    reporter: DictReporter
    """The reporter concerned."""


class IncorrectKeynamesLength(IncorrectKeynames):
    """The length of ``keys`` was not 13."""

    message = 'keys must have length 13'


class IncorrectKeynamesType(IncorrectKeynames):
    """``keys`` or anything within was of the wrong type."""

    message = 'keys must either be None, or an iterable giving strings or None'


class NoOutputMapping(ReporterError):
    """A :class:`check_empty.reporter.dict.DictReporter` had no output mapping."""

    message = 'no mapping to output to'
