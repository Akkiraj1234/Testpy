from __future__ import annotations
from .utils import (
    Key, 
    draw_panel, 
    safe_addstr
)

import curses


class Command:
    
    def __init__(self, window: curses.window | None) -> None:
        self.window = window
        self.active = False
        self.command_buffer = ""
        self.command_history: list[str] = []

    def resize(self, height: int, width: int, start_y: int, start_x: int) -> None:
        if self.window is None:
            self.window = curses.newwin(height, width, start_y, start_x)
            return

        self.window.resize(height, width)
        self.window.mvwin(start_y, start_x)

    def handle_input(self, key: int) -> None:
        if not self.active:
            if key == ord(":"):
                self.active = True
                self.command_buffer = ""
                try:
                    curses.curs_set(1)
                except curses.error:
                    pass
            return

        if key in (Key.ESC, ord(":")):
            self.command_buffer = ""
            self.active = False
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return

        if key in Key.ENTER:
            self.execute_command(self.command_buffer)
            self.command_buffer = ""
            self.active = False
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return

        if key in Key.BACKSPACE:
            self.command_buffer = self.command_buffer[:-1]
            return

        if Key.is_printable(key):
            self.command_buffer += chr(key)

    def update(self) -> None:
        if self.window is None:
            return

        self.window.erase()
        draw_panel(self.window, " Command ")

        prompt = ":" if self.active else ""
        available_width = max(self.window.getmaxyx()[1] - 3, 0)
        if available_width <= 0:
            self.window.noutrefresh()
            return

        text = (prompt + self.command_buffer)[-available_width:]
        safe_addstr(self.window, 1, 1, text)

        if self.active:
            cursor_x = min(1 + len(text), self.window.getmaxyx()[1] - 2)
            try:
                self.window.move(1, cursor_x)
            except curses.error:
                pass

        self.window.noutrefresh()

    def execute_command(self, command: str) -> None:
        command = command.strip()
        if not command:
            return

        self.command_history.append(command)
        lowered = command.lower()

        if lowered in {"q", "quit"}:
            append_output("Use Ctrl+X to quit the app.")
            return

        if lowered in {"h", "help"}:
            extend_output(
                [
                    "Available commands:",
                    "  help  Show this help",
                    "  pwd   Show detected test directory",
                    "  clear Clear the output panel",
                ]
            )
            return

        if lowered == "pwd":
            append_output(f"Test directory: {get_test_dir()}")
            return

        if lowered == "clear":
            clear_output()
            return

        append_output(f"Unknown command: {command}")
