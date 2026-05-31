# Keybindings

Testpy supports a Vim-like workflow for the TUI.

## Navigation

| Key | Action |
| --- | --- |
| `j` / `↓` | Move down |
| `k` / `↑` | Move up |
| `g` | Jump to top |
| `G` | Jump to bottom |

## Selection

| Key | Action |
| --- | --- |
| `Enter` | Toggle selection |
| `a` | Select all in current view |
| `d` | Deselect all in current view |
| `i` | Invert selection |

## Execution

| Key | Action |
| --- | --- |
| `r` | Run current item |
| `R` | Run failed tests |
| `Ctrl+Enter` | Run selected tests |

## Search

| Key | Action |
| --- | --- |
| `/` | Search |
| `n` | Next match |
| `N` | Previous match |

## UI / Utility

| Key | Action |
| --- | --- |
| `:` | Open command mode |
| `Esc` | Exit current mode |
| `h` | Open help screen |
| `Ctrl+L` | Clear output |
| `Ctrl+Q` | Quit |

## Notes

- In command mode, the input line stays active until `Enter` submits or `Esc` cancels.
- `h` is reserved for help in V1.
- The explorer uses movement keys; command mode is separate from the tree.
