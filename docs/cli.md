# Command Line Interface

## Current arguments

### General
```bash
testpy --help
testpy --version
```

### Execution
```bash
testpy --run-all
```
Run all discovered tests and skip the TUI.

### Interface
```bash
testpy --no-cli
```
Run without the curses UI.

### Configuration
```bash
testpy --config path/to/testpy.toml
```
Use a specific configuration file.

## Behavior

- `--help` and `--version` should exit immediately.
- `--run-all` should run tests without starting the interactive UI.
- `--no-cli` should use the headless wrapper path.
- CLI parsing should happen before config loading and app startup.

## Future CLI arguments

- `--discover`
- `--run-failed`
- `--framework pytest`
- `--framework criterion`
- `--framework jest`
