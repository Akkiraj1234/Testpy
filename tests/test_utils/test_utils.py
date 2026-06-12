from __future__ import annotations
from importlib.metadata import PackageNotFoundError
import importlib
import sys


def test_version_exists():
    from testpy.__version__ import VERSION
    assert isinstance(VERSION, str)
    
    
def test_init_version_import():
    from testpy import VERSION
    assert isinstance(VERSION, str)
    

def test_error_handling_for_version(monkeypatch):
    def fake_version(name: str):
        raise PackageNotFoundError

    monkeypatch.setattr("importlib.metadata.version", fake_version)
    sys.modules.pop("testpy.__version__", None)

    version_module = importlib.import_module("testpy.__version__")

    assert version_module.VERSION == "0.0.0"
