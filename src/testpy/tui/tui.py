from __future__ import annotations
from typing import Dict
from queue import Queue

from .utils import (
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    safe_addstr,
    set_color,
    Key
)
import curses
import textwrap

# importing windows
from .command import Command
from .explore import Explore
from .output import Output



class FocusManager:
    """
    Manages focus ownership between interactive windows.
    """

    def __init__(
        self,
        focus_windows: Dict[str, object],
        current_focus_index: int = 0,
    ) -> None:
        if not focus_windows:
            raise ValueError("focus_windows cannot be empty")

        self.focus_windows = focus_windows
        self.current_focus_index = current_focus_index

        self._focus_windows_list = list(focus_windows.keys())
        self._focus_window_index = {
            name: idx
            for idx, name in enumerate(self._focus_windows_list)
        }

    
    @property
    def current(self) -> object:
        """
        Return the currently focused window.
        """
        name = self._focus_windows_list[self.current_focus_index]
        return self.focus_windows[name]

    
    def next_focus(self) -> None:
        """
        Move focus to the next window.
        """
        self.current_focus_index = (
            self.current_focus_index + 1
        ) % len(self._focus_windows_list)

    
    def previous_focus(self) -> None:
        """
        Move focus to the previous window.
        """
        self.current_focus_index = (
            self.current_focus_index - 1
        ) % len(self._focus_windows_list)

    
    def focus(self, window_name: str) -> bool:
        """
        Set focus to a window by name.
        """
        idx = self._focus_window_index.get(window_name)

        if idx is None:
            return False

        self.current_focus_index = idx
        return True

    
    def handle_key(self, key: int) -> None:
        """
        Forward input to the focused window.
        """
        return self.current.handle_input(key)



class Tui:
    """
    Main application controller.

    Responsible for terminal initialization, layout
    management, rendering, focus coordination, and input
    processing.
    """

    def __init__(
        self, 
        event_bus: Queue,
        stdscr: curses.window
    ) -> None:
        self.event_bus = event_bus
        self.stdscr = stdscr
        self.height = 0
        self.width = 0
        self.is_small_window = False

        self._setup_terminal()
        self._setup_tui_app()

    
    def _setup_terminal(self) -> None:
        """
        Configure curses and initialize color pairs.
        """

        self.stdscr.keypad(True)
        self.stdscr.timeout(16)

        if not curses.has_colors():
            self.has_colors = False
            return

        set_color(None)

    
    def _setup_tui_app(self) -> None:
        """
        Create application panels and focus management.
        """
        
        self.explore = Explore(None)
        self.output = Output(None)
        self.command = Command(None)

        self.focus_manager = FocusManager(
            {
                "explore": self.explore,
                "output": self.output,
                "command": self.command,
            }
        )

    
    def _draw_small_window_message(self) -> None:
        """
        Display a warning when the terminal is too small.
        """

        self.stdscr.erase()

        message = (
            f"Window is too small. Minimum size is "
            f"{MIN_WINDOW_WIDTH}x{MIN_WINDOW_HEIGHT}"
        )

        lines = textwrap.wrap(
            message,
            width=max(self.width - 4, 1),
        )

        for row, line in enumerate(lines, start=2):
            if row >= self.height - 1:
                break
            
            safe_addstr(self.stdscr, row, 2, line, curses.A_DIM)

        self.stdscr.noutrefresh()
    
    
    def update_layout(self) -> None:
        """
        Update window layout after a terminal resize.
        """
        height, width = self.stdscr.getmaxyx()

        if (height, width) == (self.height, self.width):
            return

        self.height, self.width = height, width

        if (
            height < MIN_WINDOW_HEIGHT
            or width < MIN_WINDOW_WIDTH
        ):
            self.is_small_window = True
            return

        self.is_small_window = False
        command_height = 3
        main_height = height - command_height
        explore_width = width // 3

        self.explore.resize(main_height, explore_width, 0, 0)
        self.output.resize(main_height, width - explore_width, 0, explore_width)
        self.command.resize(command_height, width, main_height, 0)
    
    
    def handle_input(self, key: int) -> bool:
        """
        Process a single keyboard event.

        Returns:
            True if the application should exit.
        """

        if key == -1:
            return False

        if key == Key.CTRL_X:
            return True

        if key == Key.TAB:
            self.focus_manager.next_focus()
            return False

        if key == Key.SHIFT_TAB:
            self.focus_manager.previous_focus()
            return False

        self.focus_manager.handle_key(key)
        return False
    
    
    def update(self) -> None:
        """
        Render the current application state.
        
        Displays a warning when the terminal is too small,
        otherwise updates all visible panels.
        """

        if self.is_small_window:
            self._draw_small_window_message()
            return

        self.explore.update()
        self.output.update()
        self.command.update()
        
        
    def run(self) -> None:
        """
        Start the main application event loop.
        
        Continuously updates the layout, renders the UI,
        processes user input, and exits when requested.
        """

        while True:
            self.update_layout()
            self.update()
            curses.doupdate()

            key = self.stdscr.getch()
            
            if self.handle_input(key):
                break