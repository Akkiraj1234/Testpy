from __future__ import annotations
from enum import IntEnum
from typing import Any
import textwrap
import curses



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

MIN_WINDOW_HEIGHT = 18
MIN_WINDOW_WIDTH = 72


class Explore:
    def __init__(self, window: curses.window):
        self.window = window
        
    
    def update(self):
        pass


class Output(curses.window):
    def __init__(self, window: curses.window):
        self.window = window
    
    def update(self):
        pass


class Command(curses.window):
    def __init__(self, window: curses.window):
        self.window = window

    def update(self):
        pass
    
    def resize(self, height:int, width:int, start_x:int, start_y: int):
        pass
    
    def handle_input(self, key:int):
        pass
    

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

def safe_addstr( window: curses.window, y: int, x: int, text: str, style: int = 0 ) -> None:
    try:  window.addstr(y, x, text, style)
    except curses.error: pass



class Tui:
    
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.mode = Mode.NORMAL
        self.is_small_window = False
        self.height = 0
        self.width = 0
        
        # setup terminal
        self._setup_terminal()
        self._create_window()
    
    
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
    
    
    def _create_window(self) -> None:
        self.explore = Explore(self)
        self.output = Output(self)
        self.command = Command(self)
    
    
    def _draw_small_window_message(self) -> None:
        self.stdscr.erase()
        message = f"Window is too small. Minimum size is {MIN_WINDOW_WIDTH}x{MIN_WINDOW_HEIGHT}"
        lines = textwrap.wrap(message, width=max(self.width - 4, 1))
        
        for row, line in enumerate(lines, start=2):
            if row >= self.height - 1:
                break
            safe_addstr(self.stdscr, row, 2, line, curses.A_DIM)
        
        self.stdscr.noutrefresh()

    
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

        self.explore.resize(main_height, explore_width, 0, 0)
        self.output.resize(main_height, output_width, 0, explore_width)
        self.command.resize(command_height, width, main_height, 0)

        self.is_small_window = False
        self.height, self.width = height, width
    
    
    def handle_input(self, key: int) -> bool:
        if key == -1:
            return False
        if key == Key.CTRL_Q:
            return True

        if self.mode == Mode.NORMAL:
            self.explore.handle_input(key)
        else:
            self.command.handle_input(key)
        
        return False
    
    
    def update(self) -> None:
        if self.is_small_window:
            self._draw_small_window_message()
            return

        self.explore.update()
        self.output.update()
        self.command.update()
    
    
    def run(self, stdscr: curses.window) -> None:
            
        while True:
            self.set_layout()
            self.update()
            curses.doupdate()

            key = self.stdscr.getch()
            if self.handle_input(key):
                break

    
    def run(self):
        pass
    
