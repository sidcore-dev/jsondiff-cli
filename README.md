# jsondiff-cli

A small, dependency-free command-line tool that compares two JSON files and
prints a clear, path-based diff — so you can see exactly which keys were
added, removed, or changed, and where.

## Why

`diff` on two JSON files is nearly useless once formatting or key order
differs. `jsondiff-cli` parses both files as JSON first, so it only reports
*semantic* differences, addressed by path (e.g. `root.users[2].email`).

## Install

```bash
pip install .
```

This installs a `jsondiff-cli` command on your PATH.

## Usage

```bash
jsondiff-cli old.json new.json
```

Example output:

```
- root.users[2].beta_tester = true
~ root.version: 1.2.0 -> 1.3.0
+ root.users[3] = {'id': 4, 'name': 'New User'}
```

- `+` additions, `-` removals, `~` changes (shown in color on a TTY).

### Options

| Flag         | Description                                      |
|--------------|---------------------------------------------------|
| `--no-color` | Disable colorized output                          |
| `--json`     | Emit machine-readable JSON instead of text         |
| `--quiet`    | Suppress output; rely on the exit code only        |

### Exit codes

- `0` — no differences found
- `1` — differences found
- `2` — one of the files could not be read or parsed

This makes it easy to use in CI:

```bash
jsondiff-cli --quiet expected.json actual.json || echo "config drifted!"
```

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
