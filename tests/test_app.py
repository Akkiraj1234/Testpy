import testpy.cli
import pytest


def test_run_uses_curses_wrapper(monkeypatch):
    called = {}

    class FakeArgs:
        no_cli = False

    class FakeApp:
        def __init__(
            self,
            config,
            args,
            event_bus,
        ):
            pass

        def run(self):
            pass

        def stop(self):
            pass

    class FakeThread:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            called["thread_started"] = True

        def join(self, timeout=None):
            called["thread_joined"] = True

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
        "can_run_tui",
        lambda: True
    )

    monkeypatch.setattr(
        testpy.cli,
        "TestpyApp",
        FakeApp
    )

    monkeypatch.setattr(
        testpy.cli.threading,
        "Thread",
        FakeThread
    )

    monkeypatch.setattr(
        testpy.cli.curses,
        "wrapper",
        lambda fn: called.setdefault(
            "wrapper_called",
            True
        )
    )

    result = testpy.cli.run()

    assert result == 0
    assert called["wrapper_called"]
    assert called["thread_started"]
    assert called["thread_joined"]


def test_run_uses_headless(monkeypatch):
    called = {}

    class FakeArgs:
        no_cli = True

    class FakeApp:
        def __init__(
            self,
            config,
            args,
            event_bus,
        ):
            pass

        def run(self):
            pass

        def stop(self):
            pass

    class FakeHeadless:
        def __init__(self, event_bus):
            pass

        def run(self):
            called["headless_called"] = True

    class FakeThread:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            called["thread_started"] = True

        def join(self, timeout=None):
            called["thread_joined"] = True

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
        testpy.cli,
        "Headless",
        FakeHeadless
    )

    monkeypatch.setattr(
        testpy.cli.threading,
        "Thread",
        FakeThread
    )

    result = testpy.cli.run()

    assert result == 0
    assert called["headless_called"]
    assert called["thread_started"]
    assert called["thread_joined"]
    
    
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