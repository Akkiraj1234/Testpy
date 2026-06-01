from __future__ import annotations
from copy import deepcopy
from pathlib import Path

import tomli_w

from testpy.config import (
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG,
    merge_dicts,
    RECURSIVE_CONFIG_SEARCH,
    find_config,
)



# Merge Dicts

# 1. Does not mutate the original defaults dictionary.
# 2. Merges two dictionaries correctly.
# 3. User values override default values.
# 4. Nested dictionaries are merged recursively.

def test_merge_dicts_does_not_mutate_defaults():
    default_config = {
        "default": False,
        "data": ["test1", "test2"]
    }
    
    original = deepcopy(default_config)
    
    merge_dicts(
        default_config,
        {"default": True, "data": []}
    )

    assert default_config == original


def test_merge_dicts_user_values_override_defaults():
    default_config = {
        "default": False,
        "data": ["test1", "test2"]
    }
    
    merged = merge_dicts(
        default_config,
        {"default": True, "data": []}
    )
    
    assert merged["default"] is True
    assert merged["data"] == []


def test_merge_dicts_merges_nested_dicts():
    defaults = {
        "ui": {
            "font": {
                "font_size": 10,
                "font_family": "JetBrains Mono"
            },
            "padding": 2,
            "border": 4
        },
        "padding": 4
    }

    user = {
        "ui": {
            "font": {
                "font_size": 5
            },
            "padding": 8,
            "border": 10
        }
    }
    
    merged = merge_dicts(defaults, user)
    
    assert merged == {
        "ui": {
            "font":{
                "font_size":5,
                "font_family": "JetBrains Mono"
            },
            "padding": 8,
            "border": 10,
        },
        "padding": 4
    }
    
    assert merged["padding"] == 4
    assert merged["ui"]["padding"] == 8
    assert merged["ui"]["border"] == 10
    assert merged["ui"]["font"]["font_size"] == 5
    assert merged["ui"]["font"]["font_family"] == "JetBrains Mono"
    

def test_merge_dicts_adds_new_keys():
    defaults = {
        "theme": "dark"
    }

    user = {
        "refresh_rate": 60
    }

    merged = merge_dicts(defaults, user)

    assert merged == {
        "theme": "dark",
        "refresh_rate": 60,
    }


# find_config

# 1. Finds a config file in the current directory.
# 2. Finds a config file in a parent directory.
# 3. Stops searching after RECURSIVE_CONFIG_SEARCH levels.
# 4. Creates a default config when none exists.
# 5. Returns merged defaults and user config.
# 6. Adds the root key correctly.
# 7. Handles reaching filesystem root without crashing.

def test_find_config_current_directory(tmp_path):
    config_file = tmp_path / CONFIG_FILE_NAME
    
    with config_file.open("wb") as file:
        tomli_w.dump(
            { "theme": "light" },
            file
        )

    config = find_config(tmp_path)
    assert config["theme"] == "light"
    assert config["root"] == str(tmp_path)
    
    
def test_find_config_parent_directory(tmp_path):
    config_file = tmp_path / CONFIG_FILE_NAME
    
    with config_file.open("wb") as file:
        tomli_w.dump(
            { "theme": "light" },
            file
        )
        
    # child dicts
    child = tmp_path / "src" / "tests"
    child.mkdir(parents=True)
    
    config = find_config(child)
    assert config["theme"] == "light"
    assert config["root"] == str(tmp_path)
    

def test_find_config_ignores_configs_beyond_search_limit(tmp_path):
    config_file = tmp_path / CONFIG_FILE_NAME

    with config_file.open("wb") as file:
        tomli_w.dump(
            {"recursive_limit": True},
            file
        )

    current = tmp_path
    for i in range(RECURSIVE_CONFIG_SEARCH + 1):
        current = current / f"dir_{i}"

    current.mkdir(parents=True)
    config = find_config(current)

    assert isinstance(config, dict)
    assert "recursive_limit" not in config
    assert config["root"] == str(Path.cwd().resolve())


def test_create_default_config_when_none_exists(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    config = find_config()

    assert isinstance(config, dict)
    assert (tmp_path / CONFIG_FILE_NAME).exists()
    assert config["root"] == str(tmp_path)
    
    
def test_find_config_returns_merged_defaults_and_user_config(tmp_path):
    config_file = tmp_path / CONFIG_FILE_NAME

    with config_file.open("wb") as file:
        tomli_w.dump(
            {
                "theme": "light"
            },
            file
        )

    config = find_config(tmp_path)

    assert config["theme"] == "light"
    assert config["refresh_rate"] == DEFAULT_CONFIG["refresh_rate"]
    
    
def test_find_config_adds_root_key(tmp_path):
    config_file = tmp_path / CONFIG_FILE_NAME

    with config_file.open("wb") as file:
        tomli_w.dump({}, file)

    config = find_config(tmp_path)

    assert "root" in config
    assert config["root"] == str(tmp_path)
