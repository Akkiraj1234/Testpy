from __future__ import annotations

from typing import Dict, Iterable, Tuple, overload
import curses

RGB = Tuple[int, int, int]

_THEME_KEYS = (
    "Text",
    "Text_Active",
    "Text_Inactive",
    "Border",
    "Border_Active",
    "Border_Inactive",
    "Main_Border",
    "Main_Border_Active",
    "Main_Border_Inactive",
    "H1",
    "H1_Active",
    "H1_Inactive",
    "H2",
    "H2_Active",
    "H2_Inactive",
    "Command",
    "Command_Active",
    "Command_Inactive",
    "Suggestion",
    "Suggestion_Active",
    "Suggestion_Inactive",
    "Error",
    "Error_Active",
    "Error_Inactive",
    "Warning",
    "Warning_Active",
    "Warning_Inactive",
    "Success",
    "Success_Active",
    "Success_Inactive",
    "Selected",
    "Focused",
    "Disabled",
)

_BASE_CURSES_COLORS: Dict[int, RGB] = {
    curses.COLOR_BLACK: (0, 0, 0),
    curses.COLOR_RED: (255, 0, 0),
    curses.COLOR_GREEN: (0, 255, 0),
    curses.COLOR_YELLOW: (255, 255, 0),
    curses.COLOR_BLUE: (0, 0, 255),
    curses.COLOR_MAGENTA: (255, 0, 255),
    curses.COLOR_CYAN: (0, 255, 255),
    curses.COLOR_WHITE: (255, 255, 255),
}

_BUILTIN_THEMES: Dict[str, Dict[str, object]] = {
    "tokyo-night": {
        "Text": {"fg": (192, 202, 245)},
        "Text_Active": {"fg": (214, 222, 255), "bold": True},
        "Text_Inactive": {"fg": (128, 136, 176), "dim": True},
        "Border": {"fg": (86, 95, 137)},
        "Border_Active": {"fg": (122, 162, 247), "bold": True},
        "Border_Inactive": {"fg": (65, 72, 104)},
        "Main_Border": {"fg": (122, 162, 247)},
        "Main_Border_Active": {"fg": (125, 207, 255), "bold": True},
        "Main_Border_Inactive": {"fg": (65, 72, 104)},
        "H1": {"fg": (187, 154, 247), "bold": True},
        "H1_Active": {"fg": (224, 175, 104), "bold": True},
        "H1_Inactive": {"fg": (122, 134, 187)},
        "H2": {"fg": (125, 207, 255), "bold": True},
        "H2_Active": {"fg": (158, 206, 106), "bold": True},
        "H2_Inactive": {"fg": (122, 134, 187)},
        "Command": {"fg": (158, 206, 106)},
        "Command_Active": {"fg": (158, 206, 106), "bold": True},
        "Command_Inactive": {"fg": (109, 117, 141)},
        "Suggestion": {"fg": (122, 162, 247)},
        "Suggestion_Active": {"fg": (125, 207, 255), "underline": True},
        "Suggestion_Inactive": {"fg": (109, 117, 141)},
        "Error": {"fg": (247, 118, 142), "bold": True},
        "Error_Active": {"fg": (255, 158, 180), "bold": True},
        "Error_Inactive": {"fg": (168, 88, 108)},
        "Warning": {"fg": (224, 175, 104), "bold": True},
        "Warning_Active": {"fg": (255, 203, 139), "bold": True},
        "Warning_Inactive": {"fg": (163, 128, 82)},
        "Success": {"fg": (158, 206, 106), "bold": True},
        "Success_Active": {"fg": (193, 255, 134), "bold": True},
        "Success_Inactive": {"fg": (105, 137, 70)},
        "Selected": {"fg": (26, 27, 38), "bg": (122, 162, 247), "bold": True},
        "Focused": {"fg": (214, 222, 255), "bg": (65, 72, 104), "reverse": True},
        "Disabled": {"fg": (86, 95, 137), "dim": True},
    },
    "dark": {
        "Text": {"fg": (230, 230, 230)},
        "Text_Active": {"fg": (255, 255, 255), "bold": True},
        "Text_Inactive": {"fg": (140, 140, 140), "dim": True},
        "Border": {"fg": (120, 120, 120)},
        "Border_Active": {"fg": (90, 170, 255), "bold": True},
        "Border_Inactive": {"fg": (80, 80, 80)},
        "Main_Border": {"fg": (90, 170, 255)},
        "Main_Border_Active": {"fg": (120, 200, 255), "bold": True},
        "Main_Border_Inactive": {"fg": (80, 80, 80)},
        "H1": {"fg": (255, 210, 120), "bold": True},
        "H1_Active": {"fg": (255, 230, 160), "bold": True},
        "H1_Inactive": {"fg": (160, 140, 90)},
        "H2": {"fg": (170, 200, 255), "bold": True},
        "H2_Active": {"fg": (200, 220, 255), "bold": True},
        "H2_Inactive": {"fg": (110, 130, 160)},
        "Command": {"fg": (170, 255, 170)},
        "Command_Active": {"fg": (200, 255, 200), "bold": True},
        "Command_Inactive": {"fg": (110, 150, 110)},
        "Suggestion": {"fg": (170, 200, 255)},
        "Suggestion_Active": {"fg": (200, 220, 255), "underline": True},
        "Suggestion_Inactive": {"fg": (110, 130, 160)},
        "Error": {"fg": (255, 110, 110), "bold": True},
        "Error_Active": {"fg": (255, 150, 150), "bold": True},
        "Error_Inactive": {"fg": (140, 80, 80)},
        "Warning": {"fg": (255, 210, 100), "bold": True},
        "Warning_Active": {"fg": (255, 230, 150), "bold": True},
        "Warning_Inactive": {"fg": (150, 120, 70)},
        "Success": {"fg": (120, 220, 120), "bold": True},
        "Success_Active": {"fg": (160, 255, 160), "bold": True},
        "Success_Inactive": {"fg": (90, 130, 90)},
        "Selected": {"fg": (0, 0, 0), "bg": (170, 200, 255), "bold": True},
        "Focused": {"fg": (255, 255, 255), "bg": (70, 70, 70)},
        "Disabled": {"fg": (100, 100, 100), "dim": True},
    },
}

SUPPORT_RGB = False
CURSES_COLORS = 0
CURSES_COLOR_PAIRS = 0
NEXT_PAIR = 1

_PAIR_CACHE: Dict[tuple[object, object], int] = {}
_RGB_COLOR_CACHE: Dict[RGB, int] = {}
_NEXT_COLOR_ID: int | None = None


class Theme:
    pass


for _theme_key in _THEME_KEYS:
    setattr(Theme, _theme_key, 0)


@overload
def style(
    *,
    fg: RGB,
    bg: RGB | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    dim: bool = False,
    reverse: bool = False,
) -> int: ...


@overload
def style(
    *,
    mask: int,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    dim: bool = False,
    reverse: bool = False,
) -> int: ...


def _clamp_rgb(rgb: Iterable[int]) -> RGB:
    values = tuple(int(channel) for channel in rgb)
    if len(values) != 3:
        raise ValueError("RGB colors must contain exactly three channels")
    return tuple(max(0, min(255, channel)) for channel in values)  # type: ignore[return-value]


def _to_curses_channel(value: int) -> int:
    return round((value / 255) * 1000)


def _normalize_theme_value(value: object) -> dict[str, object]:
    if value is None or value == "None":
        return {}

    if isinstance(value, int):
        return {"mask": value}

    if isinstance(value, dict):
        normalized = dict(value)
        if "fg" in normalized and normalized["fg"] is not None:
            normalized["fg"] = _clamp_rgb(normalized["fg"])  # type: ignore[arg-type]
        if "bg" in normalized and normalized["bg"] is not None:
            normalized["bg"] = _clamp_rgb(normalized["bg"])  # type: ignore[arg-type]
        return normalized

    if isinstance(value, (list, tuple)):
        return {"fg": _clamp_rgb(value)}

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return {}
        if text.startswith("#") and len(text) == 7:
            return {
                "fg": (
                    int(text[1:3], 16),
                    int(text[3:5], 16),
                    int(text[5:7], 16),
                )
            }

    raise ValueError(f"Unsupported theme entry: {value!r}")


def _config_theme_name(config: Dict[str, object] | None) -> str:
    if not config:
        return "tokyo-night"

    for key in ("theme", "Theme"):
        theme_name = config.get(key)
        if isinstance(theme_name, str) and theme_name:
            return theme_name

    style_config = config.get("style")
    if isinstance(style_config, dict):
        theme_name = style_config.get("theme")
        if isinstance(theme_name, str) and theme_name:
            return theme_name

    return "tokyo-night"


def _custom_theme_config(config: Dict[str, object] | None, theme_name: str) -> Dict[str, object] | None:
    if not config:
        return None

    custom = config.get("custom")
    if not isinstance(custom, dict):
        return None

    theme_group = custom.get("Theme")
    if isinstance(theme_group, dict):
        theme_values = theme_group.get(theme_name)
        if isinstance(theme_values, dict):
            return theme_values

    direct_theme = custom.get(theme_name)
    if isinstance(direct_theme, dict):
        return direct_theme

    return None


def closest_color(rgb: RGB) -> int:
    r, g, b = _clamp_rgb(rgb)
    best = curses.COLOR_WHITE
    best_dist = float("inf")

    for color_id, (cr, cg, cb) in _BASE_CURSES_COLORS.items():
        dist = ((r - cr) ** 2) + ((g - cg) ** 2) + ((b - cb) ** 2)
        if dist < best_dist:
            best = color_id
            best_dist = dist

    return best


def rgb_to_curses(rgb: RGB) -> RGB | int:
    normalized = _clamp_rgb(rgb)
    if SUPPORT_RGB:
        return normalized
    return closest_color(normalized)


def _resolve_color(color: RGB | None) -> int:
    global _NEXT_COLOR_ID

    if color is None:
        return -1

    converted = rgb_to_curses(color)
    if isinstance(converted, int):
        return converted

    cached = _RGB_COLOR_CACHE.get(converted)
    if cached is not None:
        return cached

    if _NEXT_COLOR_ID is None or _NEXT_COLOR_ID >= CURSES_COLORS:
        return closest_color(converted)

    color_id = _NEXT_COLOR_ID
    curses.init_color(
        color_id,
        _to_curses_channel(converted[0]),
        _to_curses_channel(converted[1]),
        _to_curses_channel(converted[2]),
    )
    _RGB_COLOR_CACHE[converted] = color_id
    _NEXT_COLOR_ID += 1
    return color_id


def _get_pair(fg: RGB, bg: RGB | None) -> int:
    global NEXT_PAIR

    resolved_fg = _resolve_color(fg)
    resolved_bg = _resolve_color(bg)
    cache_key = (resolved_fg, resolved_bg)

    pair_number = _PAIR_CACHE.get(cache_key)
    if pair_number is not None:
        return pair_number

    if NEXT_PAIR >= CURSES_COLOR_PAIRS:
        return 0

    pair_number = NEXT_PAIR
    curses.init_pair(pair_number, resolved_fg, resolved_bg)
    _PAIR_CACHE[cache_key] = pair_number
    NEXT_PAIR += 1
    return pair_number


def _apply_flags(
    base_mask: int,
    *,
    bold: bool,
    italic: bool,
    underline: bool,
    dim: bool,
    reverse: bool,
) -> int:
    mask = base_mask

    if bold:
        mask |= curses.A_BOLD
    if italic:
        mask |= getattr(curses, "A_ITALIC", 0)
    if underline:
        mask |= curses.A_UNDERLINE
    if dim:
        mask |= curses.A_DIM
    if reverse:
        mask |= curses.A_REVERSE

    return mask


def style(
    *,
    mask: int | None = None,
    fg: RGB | None = None,
    bg: RGB | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    dim: bool = False,
    reverse: bool = False,
) -> int:
    if mask is None and fg is None:
        raise ValueError("must provide either mask or fg")

    if fg is not None:
        pair_number = _get_pair(_clamp_rgb(fg), None if bg is None else _clamp_rgb(bg))
        mask = curses.color_pair(pair_number)
    elif mask is None:
        mask = 0

    return _apply_flags(
        mask,
        bold=bold,
        italic=italic,
        underline=underline,
        dim=dim,
        reverse=reverse,
    )


def _load_theme(config: Dict[str, object] | None) -> Dict[str, object]:
    theme_name = _config_theme_name(config)
    if theme_name in _BUILTIN_THEMES:
        return _BUILTIN_THEMES[theme_name]

    custom_theme = _custom_theme_config(config, theme_name)
    if custom_theme is not None:
        return custom_theme

    return _BUILTIN_THEMES["tokyo-night"]


def start_color(config: Dict[str, object] | None = None) -> None:
    global SUPPORT_RGB, CURSES_COLORS, CURSES_COLOR_PAIRS, NEXT_PAIR, _NEXT_COLOR_ID

    if not curses.has_colors():
        return

    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass

    CURSES_COLORS = getattr(curses, "COLORS", 0)
    CURSES_COLOR_PAIRS = getattr(curses, "COLOR_PAIRS", 0)
    SUPPORT_RGB = bool(getattr(curses, "can_change_color", lambda: False)()) and CURSES_COLORS > 16

    NEXT_PAIR = 1
    _PAIR_CACHE.clear()
    _RGB_COLOR_CACHE.clear()
    _NEXT_COLOR_ID = len(_BASE_CURSES_COLORS) if SUPPORT_RGB else None

    theme_config = _load_theme(config)
    for key in _THEME_KEYS:
        entry = _normalize_theme_value(theme_config.get(key))
        setattr(Theme, key, style(**entry) if entry else 0)
