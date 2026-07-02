"""Minimal reader for the `.cdc` native source format.

Grammar (from CDC_LANGUAGE.md): a program is a sequence of directives, one
per line. A directive is a keyword followed by positional names and `key=value`
attributes; `#` begins a comment; values may be shell-quoted. `channel` uses
the special `path -> path` form; `expect` keeps its raw predicate tokens.

This reader serves three purposes in the GIST build:

1. parity - load the CDC repository's `bridge64.cdc` and native scenario
   files and check this engine reproduces their declared expectations;
2. contract - load `gist.cdc`, the GIST engine's own native contract, and
   verify every declared witness against a live executable check;
3. discipline - the engine's semantic claims stay expressed in the calculus's
   own source language rather than only in host-language code.

It is a loader/checker in the spirit of `cdc_boot.py`: it never executes
reductions itself.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Directive:
    kind: str
    args: list[str] = field(default_factory=list)
    kwargs: dict[str, str] = field(default_factory=dict)
    line_no: int = 0

    @property
    def key(self) -> str | None:
        return self.args[0] if self.args else None

    def get(self, name: str, default: str | None = None) -> str | None:
        return self.kwargs.get(name, default)

    def get_float(self, name: str, default: float = 0.0) -> float:
        raw = self.kwargs.get(name)
        return default if raw is None else float(raw)

    def get_int(self, name: str, default: int = 0) -> int:
        raw = self.kwargs.get(name)
        return default if raw is None else int(raw)


@dataclass
class Program:
    directives: list[Directive]
    path: str = ""

    def all(self, kind: str) -> list[Directive]:
        return [d for d in self.directives if d.kind == kind]

    def find(self, kind: str, key: str) -> Directive | None:
        for d in self.directives:
            if d.kind == kind and d.key == key:
                return d
        return None

    def expects(self) -> list[list[str]]:
        return [d.args for d in self.directives if d.kind == "expect"]


def parse_line(line: str, line_no: int = 0) -> Directive | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    tokens = shlex.split(stripped, comments=True, posix=True)
    if not tokens:
        return None
    kind = tokens[0]
    if kind == "end":
        return Directive(kind="end", line_no=line_no)
    args: list[str] = []
    kwargs: dict[str, str] = {}
    rest = tokens[1:]
    if kind == "channel":
        # channel <path-a> -> <path-b> key=value...
        if len(rest) >= 3 and rest[1] == "->":
            kwargs["src"] = rest[0]
            kwargs["dst"] = rest[2]
            args = [f"{rest[0]}->{rest[2]}"]
            rest = rest[3:]
        # fall through: remaining tokens parsed as kwargs
    for tok in rest:
        if "=" in tok and not tok.startswith("="):
            k, _, v = tok.partition("=")
            kwargs[k] = v
        else:
            args.append(tok)
    return Directive(kind=kind, args=args, kwargs=kwargs, line_no=line_no)


def parse_text(text: str, path: str = "") -> Program:
    directives: list[Directive] = []
    for i, line in enumerate(text.splitlines(), start=1):
        d = parse_line(line, i)
        if d is not None:
            directives.append(d)
    return Program(directives=directives, path=path)


def parse_file(path: str | Path) -> Program:
    p = Path(path)
    return parse_text(p.read_text(encoding="utf-8"), path=str(p))
