# Contributing

Thank you for your interest in contributing to Testpy.

## Reporting Issues

When reporting a bug, please include:

* Operating system
* Python version
* Testpy version
* Steps to reproduce
* Expected behavior
* Actual behavior

## Development Setup

```bash
git clone https://github.com/<username>/Testpy.git
cd Testpy

poetry install
```

Run:

```bash
poetry run pytest
poetry run testpy
```

If you want the wrapper commands used in automation, you can also run:

```bash
make test
make build
```

## Pull Requests

Before opening a pull request:

* Keep changes focused and small.
* Add documentation when needed.
* Follow existing code style.
* Test changes locally.

## Philosophy

Testpy aims to provide a simple and fast terminal interface for test execution.

Features should prioritize:

* Simplicity
* Performance
* Predictability
* Keyboard-driven workflows
