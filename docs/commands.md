# Commands

Commands are typed after `:` in the command bar.

## Core commands for V1

| Command | What it does |
| --- | --- |
| `:help` | Open the help window |
| `:quit` | Exit the application |
| `:reload` | Reload configuration and refresh the UI |
| `:tree` | Show the current tree / explorer state |
| `:stats` | Show summary statistics |
| `:run` | Run selected tests |
| `:run-current` | Run the currently focused item |
| `:run-all` | Run all discovered tests |
| `:run-failed` | Run failed tests |
| `:save-log <file>` | Save the current output to a file |
| `:search <query>` | Search tests or output |

## Command mode behavior

- `:` opens command mode.
- `Esc` cancels the current command.
- `Backspace` deletes the last character.
- `Enter` submits the command.
- Unknown commands should show a safe error in the output panel.

## Planned later commands

- `:filter <query>`
- `:framework pytest`
- `:framework criterion`
- `:framework jest`

Those are not required for V1.
