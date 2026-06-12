from __future__ import annotations

from pathlib import Path
import curses
import textwrap

from testpy.config import find_config

from .utils import draw_panel, safe_addstr


_CONFIG = find_config()
_TEST_DIR = Path(_CONFIG.get("root", ".")) / _CONFIG.get("TEST_DIR", "./test/")


def get_test_dir() -> Path:
    return _TEST_DIR


def get_root() -> str:
    return str(_CONFIG.get("root", "."))


class Explore:
    def __init__(self, window: curses.window | None) -> None:
        self.window = window

    def resize(self, height: int, width: int, start_y: int, start_x: int) -> None:
        if self.window is None:
            self.window = curses.newwin(height, width, start_y, start_x)
            return

        self.window.resize(height, width)
        self.window.mvwin(start_y, start_x)

    def handle_input(self, key: int) -> None:
        del key

    def update(self) -> None:
        if self.window is None:
            return

        self.window.erase()
        draw_panel(self.window, " Explore ")
        self._draw_lines(
            [
                f"Root: {get_root()}",
                f"Tests: {get_test_dir()}",
                "",
                "Normal mode:",
                "  Tab  move focus",
                "  :    command mode when command panel is focused",
                "  Ctrl+X  quit",
            ]
        )
        self.window.noutrefresh()

    def _draw_lines(self, lines: list[str]) -> None:
        if self.window is None:
            return

        height, width = self.window.getmaxyx()
        usable_width = max(width - 4, 0)
        row = 1

        for line in lines:
            wrapped = textwrap.wrap(line, width=max(usable_width, 1)) or [""]
            for segment in wrapped:
                if row >= height - 1:
                    return
                safe_addstr(self.window, row, 2, segment)
                row += 1
