# Testpy Roadmap

Testpy is a terminal-based test workspace for discovering, selecting, running, and monitoring tests across multiple languages and frameworks.

Initial supported frameworks:
- pytest (Python)
- Criterion (C/C++)
- Jest (JavaScript)

## V0.1 — Foundation
Goal: make the application start reliably and keep the core logic testable.

### Must finish first
- [x] App starts without crashing
- [x] `main()` / `run()` exit cleanly
- [x] KeyboardInterrupt is handled at the top level
- [ ] Config loading works
- [ ] Config creation works when no config exists
- [ ] Config merge behavior is tested
- [ ] CLI arguments are parsed
- [ ] Version flag works

### Tests
- [ ] `merge_dicts()` merges nested dictionaries correctly
- [ ] `find_config()` finds config in the current directory
- [ ] `find_config()` walks upward correctly
- [ ] `find_config()` stops after the maximum search depth
- [ ] `find_config()` creates a default config when missing
- [ ] CLI argument parsing is correct
- [ ] CLI error handling returns safe exit codes

### CI / packaging
- [ ] Poetry build works
- [ ] Wheel build works
- [ ] GitHub Actions runs tests
- [ ] GitHub Actions builds the package

Release target:
- The app starts, tests pass, and the build succeeds.

## V0.2 — Command mode and shell
Goal: keyboard-driven control before full test discovery.

### Must have
- [ ] `:` opens command mode
- [ ] `Esc` exits command mode
- [ ] command buffer editing
- [ ] command history
- [ ] help screen
- [ ] reload config/project
- [ ] quit command

### Commands in V0.2
- `:help`
- `:quit`
- `:reload`
- `:stats` (basic placeholder is okay)

Release target:
- command mode works and the app is still stable.

## V0.3 — TUI skeleton
Goal: the three-panel layout works.

### Must have
- [ ] Explorer window
- [ ] Output window
- [ ] Command window
- [ ] Resize handling
- [ ] Minimum terminal size handling
- [ ] Cursor movement in the explorer
- [ ] selection state
- [ ] help overlay or help window

Release target:
- user can move around and select items.

## V0.4 — Test discovery
Goal: show tests in the explorer.

### Must have
- [ ] pytest discovery
- [ ] Criterion discovery
- [ ] Jest discovery
- [ ] directories shown in tree
- [ ] tests shown under their framework/project node

Release target:
- tests appear in the UI tree.

## V0.5 — Test execution
Goal: run selected tests and view output.

### Must have
- [ ] run selected tests
- [ ] run current item
- [ ] run all tests
- [ ] run failed tests
- [ ] live output
- [ ] exit code handling
- [ ] error reporting
- [ ] save log

Release target:
- tests can be executed from the UI.

## V1.0 — Stable multi-language workflow
Goal: a usable multi-language test workspace.

### Required
- [ ] discovery
- [ ] selection
- [ ] execution
- [ ] search
- [ ] logging
- [ ] statistics
- [ ] CLI mode
- [ ] TUI mode
- [ ] configuration support
- [ ] working docs for commands and bindings

Success criteria:
- a developer can install Testpy and manage Python, C/C++, and JavaScript tests from one interface.
