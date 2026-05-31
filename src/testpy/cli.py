from __future__ import annotations

import curses
import locale

from .config import find_config
from .ui import TestpyApp


def main() -> None:
    locale.setlocale(locale.LC_ALL, "")
    config = find_config()
    curses.wrapper(TestpyApp(config).run)
