from __future__ import annotations

import curses
import textwrap

from .utils import draw_panel, safe_addstr


OUTPUT_LINES = [
    "Welcome to Testpy",
    "Press Tab to focus the command panel",
    "Press ':' in the command panel to enter command mode",
    "Press Ctrl+X to quit",
]


def append_output(line: str) -> None:
    OUTPUT_LINES.append(line)


def extend_output(lines: list[str]) -> None:
    OUTPUT_LINES.extend(lines)


def clear_output() -> None:
    OUTPUT_LINES.clear()


class Output:
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
        draw_panel(self.window, " Output ")

        height, width = self.window.getmaxyx()
        usable_height = max(height - 2, 0)
        usable_width = max(width - 4, 0)
        visible_lines = OUTPUT_LINES[-usable_height:]
        row = 1

        for line in visible_lines:
            wrapped = textwrap.wrap(line, width=max(usable_width, 1)) or [""]
            for segment in wrapped:
                if row >= height - 1:
                    self.window.noutrefresh()
                    return
                safe_addstr(self.window, row, 2, segment)
                row += 1

        self.window.noutrefresh()
