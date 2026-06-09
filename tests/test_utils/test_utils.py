from __future__ import annotations


def test_version_exists():
    from testpy.__version__ import VERSION
    assert isinstance(VERSION, str)
    
    
def test_init_version_import():
    from testpy import VERSION
    assert isinstance(VERSION, str)
    
