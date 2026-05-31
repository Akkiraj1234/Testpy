from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any
import tomllib

RECURSIVE_CONFIG_SEARCH = 5
CONFIG_FILE_NAME = "testpy.toml"

DEFAULT_CONFIG: dict[str, Any] = {
    "theme": "dark",
    "refresh_rate": 60,
    "ui": {
        "border": True,
        "padding": 2,
        "window_margin_y": 1,
        "window_margin_x": 3,
    },
    "TEST_DIR": "./test/",
}


def merge_dicts(defaults: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(defaults)

    def merge_into(target: dict[str, Any], incoming: dict[str, Any]) -> None:
        for key, value in incoming.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                merge_into(target[key], value)
            else:
                target[key] = value

    merge_into(merged, user)
    return merged


def find_config(start: Path | None = None) -> dict[str, Any]:
    current = (start or Path.cwd()).resolve()

    for _ in range(RECURSIVE_CONFIG_SEARCH):
        config_path = current / CONFIG_FILE_NAME
        if config_path.exists():
            with config_path.open("rb") as file:
                config = tomllib.load(file)
            return merge_dicts(DEFAULT_CONFIG, {**config, "root": str(current)})

        if current == current.parent:
            break

        current = current.parent

    return merge_dicts(DEFAULT_CONFIG, {"root": str((start or Path.cwd()).resolve())})
