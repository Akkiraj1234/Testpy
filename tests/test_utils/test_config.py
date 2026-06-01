from __future__ import annotations
from pathlib import Path

from src.testpy.config import (
    DEFAULT_CONFIG,
    find_config, 
    merge_dicts
)


# In this file we gonna test these 
#
# => merge_dicts
# 1. Does not mutate the original defaults dictionary.
# 2. Merges two dictionaries correctly.
# 3. User values override default values.
# 4. Nested dictionaries are merged recursively.
# 
# => find_config
# 1. Finds a config file in the current directory.
# 2. Finds a config file in a parent directory.
# 3. Stops searching after RECURSIVE_CONFIG_SEARCH levels.
# 4. Creates a default config when none exists.
# 5. Returns merged defaults and user config.
# 6. Adds the root key correctly.
# 7. Handles reaching filesystem root without crashing.


# Merge Dicts

def test_merge_dicts_does_not_mutate_defaults():
    pass


def test_merge_dicts_user_values_override_defaults():
    pass


def test_merge_dicts_merges_nested_dicts():
    pass


def test_user_value_override():
    pass


















def test_merge_dicts_preserves_defaults_when_user_overrides_nested_values() -> None:
    merged = merge_dicts(
        DEFAULT_CONFIG,
        {
            "ui": {"padding": 4},
            "theme": "light",
        },
    )

    assert merged["theme"] == "light"
    assert merged["ui"]["padding"] == 4
    assert merged["ui"]["border"] is True


def test_find_config_reads_nearest_testpy_toml(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    nested = project_root / "apps" / "demo"
    nested.mkdir(parents=True)
    (project_root / "testpy.toml").write_text(
        """
        theme = "light"

        [ui]
        padding = 6
        """.strip()
        + "\n",
        encoding="utf-8",
    )

    config = find_config(nested)

    assert config["theme"] == "light"
    assert config["ui"]["padding"] == 6
    assert config["ui"]["border"] is True
    assert config["root"] == str(project_root.resolve())


def test_find_config_falls_back_to_defaults_when_config_missing(tmp_path: Path) -> None:
    config = find_config(tmp_path)

    assert config["theme"] == DEFAULT_CONFIG["theme"]
    assert config["TEST_DIR"] == DEFAULT_CONFIG["TEST_DIR"]
    assert config["root"] == str(tmp_path.resolve())
