"""The append-only ledger: GIST's trace/window layer.

The ledger is the CDC observer layer made operational:

  - it is append-only and hash-chained (each entry links to the previous
    entry's hash over its *payload*; wall-clock metadata rides outside the
    hash so replay determinism is semantic, not temporal);
  - reading it is passive observation: projections (`TraceWindow`) never
    mutate engine state;
  - trace order is local (T6): the ledger's sequence is the order of ledger
    events, and any bounded window over it carries its own local counter -
    no global tick is assumed by the engine's reactors;
  - the whole engine state is a pure fold over ledger payloads, so any third
    party can replay and re-derive the state, the Merkle roots, and the
    decision stamp.

Reactors (human, LLM, code) coordinate *through* this ledger - GIST's
"no orchestrator" principle: agents react to entries and append entries.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from .crypto import GENESIS, chain_hash


@dataclass
class Entry:
    seq: int
    kind: str
    payload: dict[str, Any]
    prev_hash: str
    hash: str
    meta: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "seq": self.seq,
            "kind": self.kind,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
            "meta": self.meta,
        }

    @staticmethod
    def from_json(obj: dict[str, Any]) -> "Entry":
        return Entry(
            seq=obj["seq"],
            kind=obj["kind"],
            payload=obj["payload"],
            prev_hash=obj["prev_hash"],
            hash=obj["hash"],
            meta=obj.get("meta", {}),
        )


class LedgerError(Exception):
    pass


class Ledger:
    """Append-only, hash-chained event log with optional JSONL persistence."""

    def __init__(self, path: str | Path | None = None, clock: Callable[[], float] | None = None):
        self.path = Path(path) if path is not None else None
        self.entries: list[Entry] = []
        self._clock = clock or time.time
        if self.path is not None and self.path.exists():
            self._load()

    # -- write ---------------------------------------------------------------

    def append(self, kind: str, payload: dict[str, Any]) -> Entry:
        prev = self.entries[-1].hash if self.entries else GENESIS
        body = {"seq": len(self.entries), "kind": kind, "payload": payload}
        entry = Entry(
            seq=len(self.entries),
            kind=kind,
            payload=payload,
            prev_hash=prev,
            hash=chain_hash(prev, body),
            meta={"ts": self._clock()},
        )
        self.entries.append(entry)
        if self.path is not None:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry.to_json(), ensure_ascii=False) + "\n")
        return entry

    # -- read (passive) --------------------------------------------------------

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self) -> Iterator[Entry]:
        return iter(self.entries)

    @property
    def head_hash(self) -> str:
        return self.entries[-1].hash if self.entries else GENESIS

    def of_kind(self, *kinds: str) -> list[Entry]:
        want = set(kinds)
        return [e for e in self.entries if e.kind in want]

    def last_of_kind(self, kind: str) -> Entry | None:
        for e in reversed(self.entries):
            if e.kind == kind:
                return e
        return None

    # -- verification -----------------------------------------------------------

    def verify_chain(self) -> bool:
        """Recompute the whole hash chain; True iff untampered."""
        prev = GENESIS
        for i, e in enumerate(self.entries):
            body = {"seq": e.seq, "kind": e.kind, "payload": e.payload}
            if e.seq != i or e.prev_hash != prev or e.hash != chain_hash(prev, body):
                return False
            prev = e.hash
        return True

    # -- persistence -----------------------------------------------------------

    def _load(self) -> None:
        assert self.path is not None
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    self.entries.append(Entry.from_json(json.loads(line)))
        if not self.verify_chain():
            raise LedgerError(f"ledger chain verification failed: {self.path}")

    @staticmethod
    def load(path: str | Path) -> "Ledger":
        return Ledger(path=path)


@dataclass
class TraceWindow:
    """A bounded, passive projection over the ledger (a CDC window).

    scope filters by payload 'slot' membership (None = whole field); kinds
    filters event kinds; [seq0, seq1) bounds the span. The window carries a
    local event counter - windows over the same ledger can legitimately see
    different event densities (trace-order locality).
    """

    name: str
    kinds: tuple[str, ...] | None = None
    scope_slots: tuple[int, ...] | None = None
    seq0: int = 0
    seq1: int | None = None

    def project(self, ledger: Ledger) -> list[Entry]:
        out = []
        for e in ledger:
            if e.seq < self.seq0:
                continue
            if self.seq1 is not None and e.seq >= self.seq1:
                continue  # causal: windows never read past their bound
            if self.kinds is not None and e.kind not in self.kinds:
                continue
            if self.scope_slots is not None:
                slot = e.payload.get("slot")
                if slot is None or slot not in self.scope_slots:
                    continue
            out.append(e)
        return out

    def local_counter(self, ledger: Ledger) -> int:
        return len(self.project(ledger))


def replay_payloads(ledger: Iterable[Entry]) -> Iterator[tuple[str, dict[str, Any]]]:
    """The pure event stream (kind, payload) a fold reconstructs state from."""
    for e in ledger:
        yield e.kind, e.payload
