"""Scene generation with NATIVE labels: the BiDi C runtime is the labeler.

Every training label is produced by the actual mechanism: scenes compile to
`.cdc` batch files (one module per slot, the corefold pyramid as channels,
twelve converged flow steps, a commit per module), the extended BiDi
`cdc_native_runtime` executes them, and the committed words come back as
supervision. Slot labels follow the verdict rule the mechanism uses
elsewhere (assertion-leading barrier + mirror): a slot's label is

    +1  if the factual field commits an accepted decisive + singular
    -1  if the mirrored field (theta -> pi - theta) does
     0  otherwise (open / contested / held)

and a scene's global label aggregates decisively-supported vs contradicted
slots:  sum >= +2 -> yes(+1), sum <= -2 -> no(-1), else maybe(0).

Datasets are cached as JSON with the generating seed, so every number in
the results is reproducible from the native runtime alone.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import tempfile

import numpy as np

CELLS = 6
SINGULAR = 4
PYRAMID = ((0, 3), (1, 3), (1, 5), (2, 5), (3, 4), (5, 4))
FLOW_STEPS = 12
BATCH_MODULES = 32

_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_runtime():
    """Prefer the repo's vendored (extended) bridge; build it if needed;
    fall back to a sibling BiDi checkout (development layout)."""
    vendored_dir = os.path.normpath(os.path.join(_HERE, "..", "runtime"))
    vendored = os.path.join(vendored_dir, "build", "cdc_native_runtime")
    if os.path.exists(os.path.join(vendored_dir, "cdc_native_runtime.c")):
        if not os.path.exists(vendored):
            os.makedirs(os.path.dirname(vendored), exist_ok=True)
            subprocess.run(
                ["cc", "-O2", "-o", vendored,
                 os.path.join(vendored_dir, "cdc_native_runtime.c"),
                 os.path.join(vendored_dir, "cdc_source.c"), "-lm"],
                check=True)
        return vendored
    return os.path.normpath(os.path.join(
        _HERE, "..", "..", "bidi-coherence-delta-calculus", "build",
        "cdc_native_runtime"))


DEFAULT_RT = _find_runtime()


def _rng_stream(seed: int):
    n = [0]

    def draw() -> float:
        n[0] += 1
        d = hashlib.sha256(f"torchcdc:{seed}:{n[0]}".encode()).digest()
        return int.from_bytes(d[:8], "big") / 2 ** 64

    return draw


def _cluster(atoms):
    """The engine's dialectic absorb rule (ends first, middle last)."""
    cells = [0j, 0j, 0j]
    order = [0, 2, 1]
    for theta, amp in atoms:
        v = complex(amp * math.cos(theta), amp * math.sin(theta))
        best, best_d, empty = None, None, None
        for i in order:
            if abs(cells[i]) <= 1e-12:
                if empty is None:
                    empty = i
                continue
            d = abs(_wrap(math.atan2(cells[i].imag, cells[i].real) - theta))
            if best_d is None or d < best_d:
                best, best_d = i, d
        if best is None or (empty is not None and (best_d or 0.0) > 1.0472):
            target = empty if empty is not None else 0
        else:
            target = best
        cells[target] += v
    return [(abs(c),
             math.atan2(c.imag, c.real) if abs(c) > 0 else math.pi / 2)
            for c in cells]


def _wrap(a):
    a = math.fmod(a + math.pi, 2 * math.pi)
    if a <= 0:
        a += 2 * math.pi
    return a - math.pi


def _slot_evidence(draw):
    """One occupied slot's read cone from a random evidence scenario."""
    k = 2 + int(draw() * 5)
    mode = draw()
    sign = 1.0 if draw() > 0.5 else -1.0
    atoms = []
    for j in range(k):
        if mode < 0.5:
            # consensus scenario: one shared stance, occasional weak dissent
            s = -sign if (j == k - 1 and draw() < 0.3) else sign
            polarity = s * (0.6 + 0.35 * draw())
        elif mode < 0.7:
            # contested scenario: strong opposing stances
            polarity = (1.0 if j % 2 == 0 else -1.0) * (0.6 + 0.35 * draw())
        else:
            polarity = 2.0 * draw() - 1.0
        salience = 0.5 + 0.5 * draw()
        atoms.append((math.acos(max(-1.0, min(1.0, polarity))), salience))
    return _cluster(atoms)


def generate_scenes(n_scenes: int, slots: int, seed: int):
    """Scenes as (theta [n, slots*6], amp [n, slots*6], occupied [n, slots])."""
    draw = _rng_stream(seed)
    theta = np.full((n_scenes, slots * CELLS), math.pi / 2.0)
    amp = np.zeros((n_scenes, slots * CELLS))
    occupied = np.zeros((n_scenes, slots), dtype=bool)
    for i in range(n_scenes):
        occ = [s for s in range(slots) if draw() < 0.55]
        if len(occ) < 2:
            occ = [0, slots - 1]
        for s in occ:
            occupied[i, s] = True
            read = _slot_evidence(draw)
            for c, (a, t) in enumerate(read):
                theta[i, s * CELLS + c] = t
                amp[i, s * CELLS + c] = a
    return theta, amp, occupied


# --------------------------------------------------------------------------- #
# native labeling
# --------------------------------------------------------------------------- #


def _emit_batch_cdc(path, batch, flow_steps=FLOW_STEPS, duration=0.25):
    """batch: list of 3-tuples (amp, theta) triples for read cones.

    Compilation rule (mass-weighted pyramid): the C runtime's flow is
    amplitude-blind (pure phase coupling), so evidence mass is folded into
    the channel weights - w(read->dyad) = 0.5 * mass(read cell), and
    w(dyad->singular) = 0.5 * mass(dyad) with mass(dyad) = 0.5 * (sum of
    its read masses). Zero-mass channels are omitted (an empty crossing
    exerts no pull). This realizes the calculus's |A|-weighted
    superposition exactly within the runtime's own semantics.
    """
    lines = ["# generated slot-label batch (torchcdc -> native runtime)",
             "field label-field dt=0.125 gain=1.0 deadband=0.5", ""]
    for m, read in enumerate(batch):
        lines.append(
            f"module m{m} field=label-field belief=0.0 prior=0.0 "
            f"precision=1.0 action-gain=1.0")
        for c in range(3):
            a, t = read[c]
            lines.append(
                f"cell m{m}.c{c} module=m{m} theta={t:.12f} "
                f"amplitude={a:.12f} omega=0.0")
        for c in range(3, 6):
            lines.append(
                f"cell m{m}.c{c} module=m{m} theta=1.5707963267948966 "
                f"amplitude=1.0 omega=0.0")
    lines.append("module aux field=label-field belief=0.0 prior=0.0 "
                 "precision=1.0 action-gain=1.0 parent=m0")
    lines.append("cell aux.a module=aux theta=0.0 amplitude=1.0 omega=0.0")
    lines.append("")
    for m, read in enumerate(batch):
        mass = [read[c][0] for c in range(3)]
        d_mass = {3: 0.5 * (mass[0] + mass[1]), 5: 0.5 * (mass[1] + mass[2])}
        for a, b in PYRAMID:
            if a < 3:
                w = 0.5 * mass[a]
            else:
                w = 0.5 * d_mass[a]
            if w <= 1e-9:
                continue
            lines.append(
                f"channel m{m}.c{a} -> m{m}.c{b} weight={w:.12f} delay=0.0 "
                f"angle=0.0 lines=1")
    lines.append("")
    for k in range(flow_steps):
        lines.append(f"flow f{k} field=label-field duration={duration}")
    for m in range(len(batch)):
        lines.append(f"commit c{m} module=m{m}")
    lines.append("nest n0 parent=m0 child=aux")
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def _run_batch(rt, batch, workdir):
    path = os.path.join(workdir, "label_batch.cdc")
    _emit_batch_cdc(path, batch)
    out = subprocess.run([rt, "run", path], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"native labeler failed: {out.stderr}")
    words, statuses = {}, {}
    for line in out.stdout.splitlines():
        if line.startswith("commit=c"):
            parts = dict(p.split("=", 1) for p in line.split() if "=" in p)
            m = int(parts["module"][1:])
            words[m] = parts["trits"]
            statuses[m] = parts["status"]
    return words, statuses


def native_slot_labels(reads, rt=DEFAULT_RT, workdir=None):
    """Label a list of read cones through the native runtime (+ mirror rule).

    Returns (labels [-1/0/+1], factual_words, mirror_words).
    """
    own = workdir is None
    if own:
        tmp = tempfile.TemporaryDirectory()
        workdir = tmp.name
    labels, fwords, mwords = [], [], []
    for lo in range(0, len(reads), BATCH_MODULES):
        chunk = reads[lo:lo + BATCH_MODULES]
        mirror = [[(a, math.pi - t) for a, t in read] for read in chunk]
        fw, fs = _run_batch(rt, chunk, workdir)
        mw, ms = _run_batch(rt, mirror, workdir)
        for i in range(len(chunk)):
            f_ok = fs[i] == "accepted" and fw[i][SINGULAR] == "+"
            m_ok = ms[i] == "accepted" and mw[i][SINGULAR] == "+"
            labels.append(1 if f_ok else (-1 if m_ok else 0))
            fwords.append(fw[i])
            mwords.append(mw[i])
    if own:
        tmp.cleanup()
    return labels, fwords, mwords


def build_dataset(n_scenes, slots, seed, rt=DEFAULT_RT, cache_dir=None):
    """Scenes + native labels, cached by (n, slots, seed)."""
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        cache = os.path.join(cache_dir,
                             f"dataset_s{slots}_n{n_scenes}_seed{seed}.json")
        if os.path.exists(cache):
            d = json.load(open(cache))
            return (np.array(d["theta"]), np.array(d["amp"]),
                    np.array(d["occupied"], dtype=bool),
                    np.array(d["slot_labels"]), np.array(d["global_labels"]))
    theta, amp, occupied = generate_scenes(n_scenes, slots, seed)
    reads, index = [], []
    for i in range(n_scenes):
        for s in range(slots):
            if occupied[i, s]:
                base = s * CELLS
                reads.append([(amp[i, base + c], theta[i, base + c])
                              for c in range(3)])
                index.append((i, s))
    labels, _fw, _mw = native_slot_labels(reads, rt=rt)
    slot_labels = np.zeros((n_scenes, slots), dtype=int)
    for (i, s), lab in zip(index, labels):
        slot_labels[i, s] = lab
    # verdict-rule aggregation: unopposed decisive support is a yes, mixed
    # scenes need a strong net (|sum| >= 3), everything else stays open
    sums = slot_labels.sum(axis=1)
    any_pos = (slot_labels == 1).any(axis=1)
    any_neg = (slot_labels == -1).any(axis=1)
    global_labels = np.where(
        (sums >= 1) & ~any_neg, 1,
        np.where((sums <= -1) & ~any_pos, -1,
                 np.where(sums >= 3, 1, np.where(sums <= -3, -1, 0))))
    if cache_dir:
        json.dump({
            "theta": theta.tolist(), "amp": amp.tolist(),
            "occupied": occupied.tolist(),
            "slot_labels": slot_labels.tolist(),
            "global_labels": global_labels.tolist(),
            "seed": seed, "slots": slots, "labeler": "cdc_native_runtime",
        }, open(cache, "w"))
    return theta, amp, occupied, slot_labels, global_labels
