from __future__ import annotations
from enum import IntEnum
import curses
import os
import sys


class MatchGroup:
    def __init__(self, *codes):
        self.codes = codes

    def __eq__(self, other):
        return other in self.codes

    def __repr__(self):
        return f"KeyCode{self.codes}"
    

class Color(IntEnum):
    """
    Curses color pair identifiers.
    """
    SELECTED = 1
    TITLE = 2
    TEXT = 3
    ERROR = 4
    BORDER = 5


class Key:
    """
    Collection of keyboard constants and key groups used
    throughout the TUI application.
    """

    # General
    ESC = 27
    TAB = 9
    SHIFT_TAB = curses.KEY_BTAB
    SPACE = ord(" ")

    ENTER = MatchGroup(
        curses.KEY_ENTER,
        10,  # LF
        13,  # CR
    )

    BACKSPACE = MatchGroup(
        curses.KEY_BACKSPACE,
        127,
        8,
    )

    # Arrows
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT

    # Navigation
    HOME = curses.KEY_HOME
    END = curses.KEY_END
    PAGE_UP = curses.KEY_PPAGE
    PAGE_DOWN = curses.KEY_NPAGE

    # Delete
    DELETE = curses.KEY_DC
    INSERT = curses.KEY_IC

    # Function keys
    F1 = curses.KEY_F1
    F2 = curses.KEY_F2
    F3 = curses.KEY_F3
    F4 = curses.KEY_F4

    # Ctrl
    CTRL_A = 1
    CTRL_B = 2
    CTRL_C = 3
    CTRL_D = 4
    CTRL_E = 5
    CTRL_F = 6
    CTRL_G = 7
    CTRL_H = 8
    CTRL_I = 9
    CTRL_J = 10
    CTRL_K = 11
    CTRL_L = 12
    CTRL_M = 13
    CTRL_N = 14
    CTRL_O = 15
    CTRL_P = 16
    CTRL_Q = 17
    CTRL_R = 18
    CTRL_S = 19
    CTRL_T = 20
    CTRL_U = 21
    CTRL_V = 22
    CTRL_W = 23
    CTRL_X = 24
    CTRL_Y = 25
    CTRL_Z = 26

    PRINTABLE_START = 32
    PRINTABLE_END = 126

    @classmethod
    def is_printable(cls, key: int) -> bool:
        """
        Return True if the key represents a printable ASCII character.
        """
        return cls.PRINTABLE_START <= key <= cls.PRINTABLE_END
    

MIN_WINDOW_HEIGHT = 18
MIN_WINDOW_WIDTH = 72


def safe_addstr(
    window: curses.window,
    y: int,
    x: int,
    text: str,
    style: int = 0,
) -> None:
    """
    Safely write text to a curses window.

    Drawing errors are ignored to avoid crashes caused by
    terminal resizing or out-of-bounds writes.
    """
    try:
        window.addstr(y, x, text, style)
    except curses.error:
        pass
    
    
def draw_panel(window: curses.window, title: str) -> None:
    """Draw a bordered panel with a title."""

    height, width = window.getmaxyx()

    if height < 2 or width < 2:
        return

    border_style = curses.A_DIM
    title_style = curses.A_DIM | curses.A_BOLD

    if curses.has_colors():
        border_style |= curses.color_pair(Color.BORDER)
        title_style |= curses.color_pair(Color.TITLE)

    safe_addstr(window, 0, 0, "╭", border_style)
    safe_addstr(window, 0, width - 1, "╮", border_style)
    safe_addstr(window, height - 1, 0, "╰", border_style)
    safe_addstr(window, height - 1, width - 1, "╯", border_style)

    if width > 2:
        horizontal = "─" * (width - 2)
        safe_addstr(window, 0, 1, horizontal, border_style)
        safe_addstr(window, height - 1, 1, horizontal, border_style)

    for row in range(1, height - 1):
        safe_addstr(window, row, 0, "│", border_style)
        safe_addstr(window, row, width - 1, "│", border_style)

    safe_addstr(window, 0, 2, title[: max(width - 4, 0)], title_style)
    

def can_run_tui() -> bool:
    """
    Return True if curses can be safely initialized.
    """

    if not sys.stdin.isatty():
        return False

    if not sys.stdout.isatty():
        return False

    term = os.environ.get("TERM")

    if not term or term == "dumb":
        return False

    try:
        curses.setupterm()
    except Exception:
        return False

    return True