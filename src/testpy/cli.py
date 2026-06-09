from __future__ import annotations

import curses
import locale
import sys

from .app import TestpyApp
from .args import parse_args
from .config import find_config
from .headless import headless


def run() -> int:
    # Setup locale support for terminal rendering
    locale.setlocale(locale.LC_ALL, "")

    # Parse command-line arguments
    args = parse_args()

    # Find and load testpy.toml
    # If not found, create a default config in the current directory.
    config = find_config()

    
    app = TestpyApp(config, args)
    
    if args.no_cli:
        headless.wrapper(app.run)
    else:
        curses.wrapper(app.run)
    
    return 0


def main() -> int:
    try:
        sys.exit(run())

    except KeyboardInterrupt:
        sys.exit(130)
    
    # except TestpyError as exc: will use
    except Exception as exc:
        print(f"testpy: {exc}", file=sys.stderr)
        sys.exit(1)