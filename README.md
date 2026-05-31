# Testpy

Testpy is a terminal-based test workspace for running and managing tests across multiple languages and testing frameworks.

Currently supported:

| Language   | Framework |
| ---------- | --------- |
| Python     | pytest    |
| JavaScript | Jest      |
| C / C++    | Criterion |

## Features

* Terminal user interface (TUI)
* Test discovery
* Test selection
* Unified output view
* Command-driven workflow
* Project configuration through `testpy.toml`

## Installation

```bash
pip install testpy
```

## Development

```bash
git clone https://github.com/<username>/Testpy.git
cd Testpy

poetry install
poetry run pytest
poetry build
poetry run testpy
```

Poetry is the primary development workflow. It handles dependency management, virtual environments, test execution, and package builds directly.

The `Makefile` is kept as a thin automation wrapper for CI/CD or for anyone who prefers shorter commands.

If you need `pip`-style dependency files as well:

```bash
python3 scripts/sync_requirements.py
pip install -r requirements-dev.txt
```

## Common Commands

```bash
poetry install
poetry run pytest
poetry build
poetry run testpy

make install
make test
make build
make run
make requirements
```

## Documentation

* docs/configuration.md
* docs/frameworks.md
* CONTRIBUTING.md

## Status

Testpy is currently under active development and APIs may change between releases.

## License

Apache License 2.0
