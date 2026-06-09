import testpy.cli
import pytest


def test_run_uses_curses_wrapper(monkeypatch):
    called = {}
    
    class FakeArgs:
        no_cli = False
        
    class FakeApp:
        def __init__(self, config, args):
            pass
        
        def run(self, stdscr):
            pass
        
    monkeypatch.setattr(
        testpy.cli,
        "parse_args",
        lambda: FakeArgs()
    )
    
    monkeypatch.setattr(
        testpy.cli,
        "find_config",
        lambda: {}
    )
    
    monkeypatch.setattr(
        testpy.cli,
        "TestpyApp",
        FakeApp
    )
    
    monkeypatch.setattr(
        testpy.cli.curses,
        "wrapper",
        lambda fn: called.setdefault("wrapper", fn)
    )
    
    result = testpy.cli.run()
    assert "wrapper" in called
    assert result == 0


def test_run_uses_curses_wrapper(monkeypatch):
    called = {}
    
    class FakeArgs:
        no_cli = True
        
    class FakeApp:
        def __init__(self, config, args):
            pass
        
        def run(self, stdscr):
            pass
        
    monkeypatch.setattr(
        testpy.cli,
        "parse_args",
        lambda: FakeArgs()
    )
    
    monkeypatch.setattr(
        testpy.cli,
        "find_config",
        lambda: {}
    )
    
    monkeypatch.setattr(
        testpy.cli,
        "TestpyApp",
        FakeApp
    )
    
    monkeypatch.setattr(
        testpy.cli.headless,
        "wrapper",
        lambda fn: called.setdefault("wrapper", fn)
    )
    
    result = testpy.cli.run()
    assert "wrapper" in called
    assert result == 0
    
    
def test_main_keyboard_interrupt(monkeypatch):
    
    def fake_run():
        raise KeyboardInterrupt
    
    monkeypatch.setattr(
        testpy.cli,
        "run",
        fake_run
    )
    
    with pytest.raises(SystemExit) as exc:
        testpy.cli.main()
        
    assert exc.value.code == 130


def test_main_keyboard_interrupt(monkeypatch):
    
    def fake_run():
        raise RuntimeError("why 2+2 not 5 error boom")
    
    monkeypatch.setattr(
        testpy.cli,
        "run",
        fake_run
    )
    
    with pytest.raises(SystemExit) as exc:
        testpy.cli.main()
        
    assert exc.value.code == 1
    

def test_main_success(monkeypatch):
    monkeypatch.setattr(
        testpy.cli,
        "run",
        lambda: 0
    )

    with pytest.raises(SystemExit) as exc:
        testpy.cli.main()

    assert exc.value.code == 0