# Copyright © 2026 Jonathan Dung. All rights reserved.
# SPDX-License-Identifier: MIT
"""Utility to check the emptiness of files.

Pre-commit hook, command-line tool and GitHub Action all-in-one.
"""

__all__ = ('main',)
from check_empty.__main__ import __version__ as __version__, main
