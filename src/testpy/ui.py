from __future__ import annotations

import curses
import textwrap
from enum import IntEnum
from pathlib import Path
from typing import Any


MIN_WINDOW_HEIGHT = 18
MIN_WINDOW_WIDTH = 72


class Mode(IntEnum):
    NORMAL = 0
    COMMAND = 1


class Color(IntEnum):
    SELECTED = 1
    TITLE = 2
    TEXT = 3
    ERROR = 4
    BORDER = 5


class Key:
    COMMAND = ord(":")
    ESC = 27
    ENTER = (10, 13)
    BACKSPACE = (curses.KEY_BACKSPACE, 127, 8)
    CTRL_Q = 17
    PRINTABLE_START = 32
    PRINTABLE_END = 126


class TestpyWindow:
    def __init__(self, stdscr: curses.window, config: dict[str, Any]) -> None:
        self.stdscr = stdscr
        self.config = config
        self.height = 0
        self.width = 0
        self.mode = Mode.NORMAL
        self.is_small_window = False
        self.command_buffer = ""
        self.command_history: list[str] = []
        self.output_lines = [
            "Welcome to Testpy",
            "Press ':' to enter command mode",
            "Press Ctrl+Q to quit",
        ]
        self.test_dir = Path(config.get("root", ".")) / config.get("TEST_DIR", "./test/")
        self._setup_terminal()
        self._create_windows()
        self.set_layout()

    def _setup_terminal(self) -> None:
        self.stdscr.keypad(True)
        self.stdscr.timeout(16)
        if not curses.has_colors():
            return

        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass

        curses.init_pair(Color.TITLE, curses.COLOR_CYAN, -1)
        curses.init_pair(Color.TEXT, -1, -1)
        curses.init_pair(Color.ERROR, curses.COLOR_RED, -1)
        curses.init_pair(Color.BORDER, curses.COLOR_BLUE, -1)

    def _create_windows(self) -> None:
        self.explore = curses.newwin(1, 1, 0, 0)
        self.output = curses.newwin(1, 1, 0, 0)
        self.command = curses.newwin(1, 1, 0, 0)

    def run(self, stdscr: curses.window) -> None:
        del stdscr
        try:
            curses.curs_set(0)
        except curses.error:
            pass

        while True:
            self.set_layout()
            self.draw()
            curses.doupdate()

            key = self.stdscr.getch()
            if self.handle_input(key):
                break

    def set_layout(self) -> None:
        height, width = self.stdscr.getmaxyx()
        if height == self.height and width == self.width:
            return

        if height < MIN_WINDOW_HEIGHT or width < MIN_WINDOW_WIDTH:
            self.is_small_window = True
            self.height, self.width = height, width
            return

        command_height = 3
        main_height = height - command_height
        explore_width = width // 3
        output_width = width - explore_width

        self.explore.resize(main_height, explore_width)
        self.explore.mvwin(0, 0)
        self.output.resize(main_height, output_width)
        self.output.mvwin(0, explore_width)
        self.command.resize(command_height, width)
        self.command.mvwin(main_height, 0)

        self.is_small_window = False
        self.height, self.width = height, width

    def draw(self) -> None:
        if self.is_small_window:
            self._draw_small_window_message()
            return

        self.explore.erase()
        self.output.erase()
        self.command.erase()

        self._draw_panel(self.explore, " Explore ")
        self._draw_panel(self.output, " Output ")
        self._draw_panel(self.command, " Command ")
        self._draw_explore()
        self._draw_output()
        self._draw_command()

        self.explore.noutrefresh()
        self.output.noutrefresh()
        self.command.noutrefresh()

    def handle_input(self, key: int) -> bool:
        if key == -1:
            return False
        if key == Key.CTRL_Q:
            return True

        if self.mode == Mode.NORMAL:
            self._handle_normal_input(key)
        else:
            self._handle_command_input(key)
        return False

    def _handle_normal_input(self, key: int) -> None:
        if key == Key.COMMAND:
            self.mode = Mode.COMMAND
            self.command_buffer = ""
            try:
                curses.curs_set(1)
            except curses.error:
                pass

    def _handle_command_input(self, key: int) -> None:
        if key in (Key.ESC, Key.COMMAND):
            self.command_buffer = ""
            self.mode = Mode.NORMAL
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return

        if key in Key.ENTER:
            self.execute_command(self.command_buffer)
            self.command_buffer = ""
            self.mode = Mode.NORMAL
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return

        if key in Key.BACKSPACE:
            self.command_buffer = self.command_buffer[:-1]
            return

        if Key.PRINTABLE_START <= key <= Key.PRINTABLE_END:
            self.command_buffer += chr(key)

    def execute_command(self, command: str) -> None:
        command = command.strip()
        if not command:
            return

        self.command_history.append(command)
        lowered = command.lower()

        if lowered in {"q", "quit"}:
            self.output_lines.append("Use Ctrl+Q to quit the app.")
            return

        if lowered in {"h", "help"}:
            self.output_lines.extend(
                [
                    "Available commands:",
                    "  help  Show this help",
                    "  pwd   Show detected test directory",
                    "  clear Clear the output panel",
                ]
            )
            return

        if lowered == "pwd":
            self.output_lines.append(f"Test directory: {self.test_dir}")
            return

        if lowered == "clear":
            self.output_lines.clear()
            return

        self.output_lines.append(f"Unknown command: {command}")

    def _draw_small_window_message(self) -> None:
        self.stdscr.erase()
        message = f"Window is too small. Minimum size is {MIN_WINDOW_WIDTH}x{MIN_WINDOW_HEIGHT}"
        lines = textwrap.wrap(message, width=max(self.width - 4, 1))
        for row, line in enumerate(lines, start=2):
            if row >= self.height - 1:
                break
            self._safe_addstr(self.stdscr, row, 2, line, curses.A_DIM)
        self.stdscr.noutrefresh()

    def _draw_panel(self, window: curses.window, title: str) -> None:
        height, width = window.getmaxyx()
        if height < 2 or width < 2:
            return

        border_style = curses.A_DIM
        title_style = curses.A_DIM | curses.A_BOLD
        if curses.has_colors():
            border_style |= curses.color_pair(Color.BORDER)
            title_style |= curses.color_pair(Color.TITLE)

        self._safe_addstr(window, 0, 0, "╭", border_style)
        self._safe_addstr(window, 0, width - 1, "╮", border_style)
        self._safe_addstr(window, height - 1, 0, "╰", border_style)
        self._safe_addstr(window, height - 1, width - 1, "╯", border_style)

        if width > 2:
            horizontal = "─" * (width - 2)
            self._safe_addstr(window, 0, 1, horizontal, border_style)
            self._safe_addstr(window, height - 1, 1, horizontal, border_style)

        for row in range(1, height - 1):
            self._safe_addstr(window, row, 0, "│", border_style)
            self._safe_addstr(window, row, width - 1, "│", border_style)

        max_title_width = max(width - 4, 0)
        if max_title_width > 0:
            self._safe_addstr(window, 0, 2, title[:max_title_width], title_style)

    def _draw_explore(self) -> None:
        lines = [
            f"Root: {self.config.get('root', '.')}",
            f"Tests: {self.test_dir}",
            "",
            "Normal mode:",
            "  :  enter command mode",
            "  Ctrl+Q  quit",
        ]
        self._draw_lines(self.explore, lines)

    def _draw_output(self) -> None:
        height, width = self.output.getmaxyx()
        usable_height = max(height - 2, 0)
        usable_width = max(width - 4, 0)
        visible_lines = self.output_lines[-usable_height:]
        row = 1
        for line in visible_lines:
            wrapped = textwrap.wrap(line, width=max(usable_width, 1)) or [""]
            for segment in wrapped:
                if row >= height - 1:
                    return
                self._safe_addstr(self.output, row, 2, segment)
                row += 1

    def _draw_command(self) -> None:
        prompt = ":" if self.mode == Mode.COMMAND else ""
        available_width = max(self.command.getmaxyx()[1] - 3, 0)
        if available_width <= 0:
            return
        text = (prompt + self.command_buffer)[-available_width:]
        self._safe_addstr(self.command, 1, 1, text)
        if self.mode == Mode.COMMAND:
            cursor_x = min(1 + len(text), self.command.getmaxyx()[1] - 2)
            try:
                self.command.move(1, cursor_x)
            except curses.error:
                pass

    def _draw_lines(self, window: curses.window, lines: list[str]) -> None:
        height, width = window.getmaxyx()
        usable_width = max(width - 4, 0)
        row = 1
        for line in lines:
            wrapped = textwrap.wrap(line, width=max(usable_width, 1)) or [""]
            for segment in wrapped:
                if row >= height - 1:
                    return
                self._safe_addstr(window, row, 2, segment)
                row += 1

    def _safe_addstr(
        self,
        window: curses.window,
        y: int,
        x: int,
        text: str,
        style: int = 0,
    ) -> None:
        try:
            window.addstr(y, x, text, style)
        except curses.error:
            pass


class TestpyApp:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def run(self, stdscr: curses.window) -> None:
        window = TestpyWindow(stdscr, self.config)
        window.run(stdscr)
