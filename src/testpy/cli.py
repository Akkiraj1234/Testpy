from __future__ import annotations

from queue import Queue
import threading
import curses
import locale
import sys

from .error import TestpyError
from .config import find_config
from .args import parse_args
from .headless import Headless
from .tui import Tui, can_run_tui
from .app import TestpyApp


def run() -> int:
    """
    Initialize and start Testpy.
    """
    # Setup locale support for terminal rendering
    locale.setlocale(locale.LC_ALL, "")
    
    # Parse command-line arguments
    args = parse_args()

    # Find and load testpy.toml
    # If not found, create a default config in the current directory.
    config = find_config()
    event_bus = Queue()
    
    # app will run in thread
    app = TestpyApp(
        config = config,
        args = args,
        event_bus = event_bus,
    )
    
    worker = threading.Thread(
        target = app.run,
        name = "testpy-backend",
        daemon = False
    )
    worker.start()
    
    try: 
        if args.no_cli or not can_run_tui():
            Headless(event_bus).run()
        
        else:
            curses.wrapper(
                lambda stdscr: Tui(event_bus, stdscr).run()
            )
    finally:
        app.stop()
        worker.join(timeout=5)
    
    return 0


def main() -> None:
    try:
        sys.exit(run())

    except KeyboardInterrupt:
        raise SystemExit(130)
    
    except TestpyError as exc:
        print(f"testpy: {exc}", file=sys.stderr)
        raise SystemExit(1)
    
    except Exception as exc:
        print(f"testpy: {exc}", file=sys.stderr)
        raise SystemExit(1)