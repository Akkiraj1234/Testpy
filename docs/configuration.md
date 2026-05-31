# Configuration

Testpy searches for a `testpy.toml` file starting from the current working directory and walking upward through parent directories up to level 5.

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

```toml
theme = "dark"
```

### ui.border

Type: boolean

```toml
[ui]
border = true
```

### ui.padding

Type: integer

```toml
[ui]
padding = 2
```

### ui.window_margin_x

Type: integer

```toml
[ui]
window_margin_x = 3
```

### ui.window_margin_y

Type: integer

```toml
[ui]
window_margin_y = 1
```

### test.directory

Type: string

```toml
[test]
directory = "./tests"
```
