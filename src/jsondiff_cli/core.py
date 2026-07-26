"""Core diff engine for jsondiff-cli.

Produces a flat list of DiffEntry objects describing every difference
between two JSON-compatible Python values, addressed by JSONPath-like
string paths (e.g. "root.users[2].name").
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, List


@dataclass(frozen=True)
class DiffEntry:
    path: str
    kind: str  # "added" | "removed" | "changed" | "type_changed"
    old: Any = None
    new: Any = None

    def describe(self) -> str:
        if self.kind == "added":
            return f"+ {self.path} = {self.new!r}"
        if self.kind == "removed":
            return f"- {self.path} = {self.old!r}"
        if self.kind == "type_changed":
            return (
                f"~ {self.path}: type {type(self.old).__name__} -> "
                f"{type(self.new).__name__} ({self.old!r} -> {self.new!r})"
            )
        return f"~ {self.path}: {self.old!r} -> {self.new!r}"


def diff(old: Any, new: Any, path: str = "root") -> List[DiffEntry]:
    """Return a list of DiffEntry describing differences from old to new."""
    entries: List[DiffEntry] = []
    _diff_into(old, new, path, entries)
    return entries


def _diff_into(old: Any, new: Any, path: str, out: List[DiffEntry]) -> None:
    if type(old) is not type(new) and not _numeric_pair(old, new):
        out.append(DiffEntry(path, "type_changed", old, new))
        return

    if isinstance(old, dict):
        _diff_dict(old, new, path, out)
    elif isinstance(old, list):
        _diff_list(old, new, path, out)
    else:
        if old != new:
            out.append(DiffEntry(path, "changed", old, new))


def _numeric_pair(a: Any, b: Any) -> bool:
    numeric = (int, float)
    return (
        isinstance(a, numeric)
        and isinstance(b, numeric)
        and not isinstance(a, bool)
        and not isinstance(b, bool)
    )


def _diff_dict(old: dict, new: dict, path: str, out: List[DiffEntry]) -> None:
    old_keys = set(old.keys())
    new_keys = set(new.keys())
    for key in sorted(old_keys - new_keys):
        out.append(DiffEntry(f"{path}.{key}", "removed", old=old[key]))
    for key in sorted(new_keys - old_keys):
        out.append(DiffEntry(f"{path}.{key}", "added", new=new[key]))
    for key in sorted(old_keys & new_keys):
        _diff_into(old[key], new[key], f"{path}.{key}", out)


def _diff_list(old: list, new: list, path: str, out: List[DiffEntry]) -> None:
    common = min(len(old), len(new))
    for i in range(common):
        _diff_into(old[i], new[i], f"{path}[{i}]", out)
    for i in range(common, len(old)):
        out.append(DiffEntry(f"{path}[{i}]", "removed", old=old[i]))
    for i in range(common, len(new)):
        out.append(DiffEntry(f"{path}[{i}]", "added", new=new[i]))


def iter_paths(entries: List[DiffEntry]) -> Iterator[str]:
    for entry in entries:
        yield entry.path
