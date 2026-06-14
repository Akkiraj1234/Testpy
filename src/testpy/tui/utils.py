from __future__ import annotations
from enum import IntEnum
import curses
import os
import sys


class MatchGroup:
    __slots__ = ("codes",)
    
    def __init__(self, *codes):
        self.codes = codes

    def __eq__(self, other):
        return other in self.codes

    def __repr__(self):
        return f"KeyCode{self.codes}"


class Color(IntEnum):
    """
    Requires curses color system to be initialized.
    """

    # Core UI
    BORDER = 1
    TITLE = 2
    TEXT = 3
    LINK = 4

    # Status
    ERROR = 5
    WARNING = 6
    SUCCESS = 7

    # Theme / custom colors
    ACCENT_1 = 8
    ACCENT_2 = 9
    ACCENT_3 = 10
    ACCENT_4 = 11
    ACCENT_5 = 12
    ACCENT_6 = 13

    @property
    def attr(self) -> int:
        return curses.color_pair(self)
    
    def __or__(self, attr: int) -> int:
        return self.attr | attr


class State:
    """
    Curses attribute modifiers.

    Combine with Color using the bitwise OR operator.

    Examples:
        Color.PANEL | State.ACTIVE
        Color.TITLE | State.FOCUSED
        Color.ERROR | State.UNDERLINE
    """
    ACTIVE = curses.A_BOLD
    INACTIVE = curses.A_DIM
    FOCUSED = curses.A_REVERSE
    
    UNDERLINE = curses.A_UNDERLINE
    BOLD = curses.A_BOLD
    ITALIC = ITALIC = getattr(curses, "A_ITALIC", 0)


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


def set_color(cls):
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    
    curses.init_pair(Color.BORDER,  curses.COLOR_BLUE,    -1)
    curses.init_pair(Color.TITLE,   curses.COLOR_CYAN,    -1)
    curses.init_pair(Color.TEXT,    curses.COLOR_CYAN,    -1)
    curses.init_pair(Color.LINK,    curses.COLOR_MAGENTA, -1)

    curses.init_pair(Color.ERROR,   curses.COLOR_RED,     -1)
    curses.init_pair(Color.WARNING, curses.COLOR_YELLOW,  -1)
    curses.init_pair(Color.SUCCESS, curses.COLOR_GREEN,   -1)

    curses.init_pair(Color.ACCENT_1, curses.COLOR_BLUE,    -1)
    curses.init_pair(Color.ACCENT_2, curses.COLOR_CYAN,    -1)
    curses.init_pair(Color.ACCENT_3, curses.COLOR_GREEN,   -1)
    curses.init_pair(Color.ACCENT_4, curses.COLOR_YELLOW,  -1)
    curses.init_pair(Color.ACCENT_5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(Color.ACCENT_6, curses.COLOR_RED,     -1)
    


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
    
def draw_panel(
    window: curses.window,
    title: str,
    active: bool = False,
    has_color: bool = False,
) -> None:
    """
    Draw a bordered panel with a title.
    """
    height, width = window.getmaxyx()

    if height < 2 or width < 2:
        return

    state = (
        State.ACTIVE
        if active
        else State.INACTIVE
    )

    border_style = state
    title_style = state

    if has_color:
        border_style = Color.BORDER | state
        title_style = Color.TITLE | state

    last_row = height - 1
    last_col = width - 1

    # Corners
    safe_addstr(window, 0, 0, "╭", border_style)
    safe_addstr(window, 0, last_col, "╮", border_style)
    safe_addstr(window, last_row, 0, "╰", border_style)
    safe_addstr(window, last_row, last_col, "╯", border_style)

    # Top / Bottom borders
    if width > 2:
        horizontal = "─" * (width - 2)

        safe_addstr(window, 0, 1, horizontal, border_style)
        safe_addstr(window, last_row, 1, horizontal, border_style)

    # Side borders
    for row in range(1, last_row):
        safe_addstr(window, row, 0, "│", border_style)
        safe_addstr(window, row, last_col, "│", border_style)

    # Title
    if width > 4:
        safe_addstr(
            window,
            0,
            2,
            title[: width - 4],
            title_style,
        )
    

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