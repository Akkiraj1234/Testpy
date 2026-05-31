<div align="center">

<img src=".github/repo_resource/Testpy_logo.png" width="128" alt="Testpy Logo">

# Testpy

**A terminal workspace for discovering, selecting, and running tests across multiple languages and frameworks.**

<p>
  <img src="https://img.shields.io/badge/status-pre--release-orange" alt="Pre-release">
  <img src="https://img.shields.io/badge/version-v0.1.1-blue" alt="Version">
  <img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License">
</p>

</div>

---

Testpy provides a unified terminal workspace for discovering, selecting, running, and monitoring tests across multiple languages and testing frameworks.

Instead of remembering framework-specific commands, switching terminals, and manually tracking failures, Testpy keeps the entire workflow in one place.

<h2>Framework Support</h2>

<h3>Supported</h3>

<p>
  <img src="https://img.shields.io/badge/Python-pytest-blue">
  <img src="https://img.shields.io/badge/JavaScript-Jest-yellow">
  <img src="https://img.shields.io/badge/C%2FC%2B%2B-Criterion-orange">
</p>

<h3>Planned</h3>

<p>
  <img src="https://img.shields.io/badge/Python-unittest-lightgrey">
  <img src="https://img.shields.io/badge/JavaScript-Vitest-lightgrey">
  <img src="https://img.shields.io/badge/C%2FC%2B%2B-GoogleTest-lightgrey">
  <img src="https://img.shields.io/badge/C%2FC%2B%2B-Catch2-lightgrey">
  <img src="https://img.shields.io/badge/Rust-cargo%20test-lightgrey">
  <img src="https://img.shields.io/badge/Go-go%20test-lightgrey">
</p>

## Features

- Tree-based test discovery
- Multi-selection support
- Unified output view
- Command mode
- Keyboard-driven workflow
- Project configuration via `testpy.toml`
- Terminal User Interface (TUI)
- Headless execution mode

## Workflow

```text
Discover Tests
      │
      ▼
Select Tests
      │
      ▼
Run Tests
      │
      ▼
View Results
      │
      ▼
Run Failed Tests
```

## Installation

```bash
pip install testpy
```

## Development

```bash
poetry install

poetry run pytest
poetry run testpy

poetry build
```

## Documentation

<table width="100%">
<tr>
    <th align="left">Document</th>
    <th align="left">Description</th>
</tr>

<tr>
    <td><a href="docs/configuration.md">Configuration</a></td>
    <td>Configure Testpy</td>
</tr>

<tr>
    <td><a href="docs/keybindings.md">Keybindings</a></td>
    <td>Keyboard shortcuts</td>
</tr>

<tr>
    <td><a href="docs/commands.md">Commands</a></td>
    <td>Command mode reference</td>
</tr>

<tr>
    <td><a href="docs/cli.md">CLI</a></td>
    <td>Command-line arguments</td>
</tr>

<tr>
    <td><a href="docs/frameworks.md">Framework Support</a></td>
    <td>Supported frameworks</td>
</tr>

<tr>
    <td><a href="docs/roadmap.md">Roadmap</a></td>
    <td>Development roadmap</td>
</tr>

<tr>
    <td><a href="docs/future.md">Future Ideas</a></td>
    <td>Post-v1 ideas</td>
</tr>

<tr>
    <td><a href="CONTRIBUTING.md">Contributing</a></td>
    <td>Contribution guide</td>
</tr>
</table>

## License

Apache License 2.0 [read here](./LICENSE)
