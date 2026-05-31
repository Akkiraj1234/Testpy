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

pip install -e .
testpy
```

## Documentation

* docs/configuration.md
* docs/commands.md
* docs/frameworks.md
* CONTRIBUTING.md

## Status

Testpy is currently under active development and APIs may change between releases.

## License

Apache License 2.0
