# Configuration

Testpy looks for `testpy.toml` starting from the current directory and walks upward through parent directories up to depth 5.

## Example

```toml
theme = "dark"

[ui]
border = true
padding = 2
window_margin_x = 3
window_margin_y = 1

[test]
directory = "./tests"
```

## Options

### theme
Type: string

Controls the color/theme preset used by the UI.

### ui.border
Type: boolean

Enables or disables window borders.

### ui.padding
Type: integer

Controls inner spacing for UI windows.

### ui.window_margin_x
Type: integer

Horizontal outer margin.

### ui.window_margin_y
Type: integer

Vertical outer margin.

### test.directory
Type: string

Directory that Testpy should scan for tests.

## Config behavior

- Missing config should be created in the current working directory.
- Defaults should be merged with user settings.
- Nested tables should merge recursively.
