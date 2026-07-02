"""GistSSM: the GIST-native neural architecture, trainable on cdcgrad.

The isomorphism, made literal:

  selective nonlinear state space   the CDC flow is a recurrence whose
                                    coupling is state-dependent (the
                                    Kuramoto turn |A|sin(argA − θ) - the
                                    Mamba-style selectivity is the phase
                                    geometry itself);
  convolutional filtration          the corefold pyramid (and, at lattice
                                    scale, Hamming-1 mixing + ladder
                                    pooling on the 6-cube) is a fixed-
                                    topology graph convolution whose
                                    weights are learnable SO(2) rotations;
  ternary bottleneck                the commit is a balanced-ternary
                                    quantization with a straight-through
                                    gradient (the BitNet-style ternary
                                    direction, with the deadband as a
                                    *semantic* quantizer);
  Sierpinski/64 bijection           slot addressing and pooling structure
                                    inherit bridge64 (multi-slot form).

Initialize-at-the-calculus: `GistSSM.init_calculus()` sets the mixing
edges to the exact corefold pyramid (w = 1/2, α = 0) and the dynamics
gains to the engine's - the provably-equivalent point from GIST-NN - and
training then learns to *anticipate* the full reduction from fewer
recurrent steps (the model learns what the gate will accept). Training
data comes from the mechanism itself: the reference engine labels every
sample exactly (the flywheel - the oracle generates verified supervision).

This module ships the single-slot cell (6 cells, K recurrent steps,
ternary features, linear readout) - the unit the multi-slot lattice form
tiles by bridge64 addressing. Pure Python on cdcgrad; export/port to
torch via the same op graph.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass

from . import cdcgrad as G
from .field import Cell, Channel, Field, Module

# the corefold pyramid topology (read 0,1,2 -> dyads 3,5 -> singular 4)
PYRAMID_EDGES: tuple[tuple[int, int], ...] = (
    (0, 3), (1, 3), (1, 5), (2, 5), (3, 4), (5, 4),
)
N_CELLS = 6
CLASSES = (-1, 0, 1)          # singular trit -> class index = trit + 1


def _rng(seed: int):
    n = [0]

    def draw() -> float:
        n[0] += 1
        d = hashlib.sha256(f"gistnet:{seed}:{n[0]}".encode()).digest()
        return int.from_bytes(d[:8], "big") / 2**64

    return draw


# ---------------------------------------------------------------------------
# dataset: the mechanism labels its own training data (the flywheel)
# ---------------------------------------------------------------------------


def _cluster_read_cone(atoms: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """The engine's dialectic absorb rule, standalone: cluster atoms
    (theta, amplitude) into <= 3 read cells; fill order ends, then middle."""
    cells: list[complex] = [0j, 0j, 0j]
    order = [0, 2, 1]
    for theta, amp in atoms:
        v = complex(amp * math.cos(theta), amp * math.sin(theta))
        best, best_d = None, None
        empty = None
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
    return [(abs(c), math.atan2(c.imag, c.real) if abs(c) > 0 else math.pi / 2)
            for c in cells]


def _wrap(a: float) -> float:
    a = math.fmod(a + math.pi, 2 * math.pi)
    if a <= 0:
        a += 2 * math.pi
    return a - math.pi


def _committed_singular(read: list[tuple[float, float]]) -> int:
    f = Field(name="label", deadband=0.5, amp_relax=0.8)
    cells = [Cell(theta=t, amp=a) for a, t in read]
    cells += [Cell(theta=math.pi / 2, amp=0.0) for _ in range(3)]
    f.add_module(Module(name="s", cells=cells))
    for src, dst in ((0, 3), (1, 3), (1, 5), (2, 5)):
        f.add_channel(Channel(src=f"s:{src}", dst=f"s:{dst}", weight=0.5))
    for src in (3, 5):
        f.add_channel(Channel(src=f"s:{src}", dst="s:4", weight=0.5))
    f.flow(12.0)  # converge the pyramid fully: the oracle is the fixpoint
    f.commit("s")
    return f.modules["s"].latched_word()[4]


def _reference_label(read: list[tuple[float, float]]) -> int:
    """The oracle: the verdict semantics of the calculus.

    The commit barrier is assertion-leading, so a decisively negative word
    holds rather than latching; the honest label follows the same mirror
    rule the verdict bridge uses - a -1 label is the mirrored geometry
    (θ -> π−θ) latching +1. The network therefore learns the full ternary
    verdict discipline, mirror included.
    """
    t = _committed_singular(read)
    if t != 0:
        return t
    mirrored = [(a, math.pi - th) for a, th in read]
    return -_committed_singular(mirrored)


@dataclass
class Sample:
    theta: list[float]      # 6 initial cell phases
    amp: list[float]        # 6 initial cell amplitudes
    label: int              # singular trit in {-1, 0, +1}


def make_dataset(n: int, seed: int) -> list[Sample]:
    """Engine-labeled samples: random evidence -> clustered read cone ->
    oracle label. Deterministic in (n, seed)."""
    draw = _rng(seed)
    out: list[Sample] = []
    for _ in range(n):
        k = 2 + int(draw() * 5)
        mode = draw()
        sample_sign = 1.0 if draw() > 0.5 else -1.0
        atoms = []
        for j in range(k):
            if mode < 0.4:
                # consensus scenario: one shared stance, occasional dissent
                sign = -sample_sign if (j == k - 1 and draw() < 0.3) \
                    else sample_sign
                polarity = sign * (0.55 + 0.4 * draw())
            elif mode < 0.6:
                # contested scenario: strong opposing stances
                polarity = (1.0 if j % 2 == 0 else -1.0) * (0.6 + 0.35 * draw())
            else:
                polarity = 2.0 * draw() - 1.0
            salience = 0.5 + 0.5 * draw()
            atoms.append((math.acos(max(-1.0, min(1.0, polarity))), salience))
        read = _cluster_read_cone(atoms)
        theta = [t for _a, t in read] + [math.pi / 2] * 3
        amp = [a for a, _t in read] + [0.0] * 3
        out.append(Sample(theta=theta, amp=amp,
                          label=_reference_label(read)))
    return out


# ---------------------------------------------------------------------------
# the model
# ---------------------------------------------------------------------------


class GistSSM:
    """One slot-cell of the GIST-native SSM (see module docstring).

    forward: K recurrent CDC steps with learnable SO(2) edge rotations,
    then the ternary commit bottleneck (STE), then a linear readout over
    [zx, zy, trits] predicting the oracle's singular trit.
    """

    def __init__(self, steps: int = 4, step_size: float = 1.0):
        self.steps = steps
        self.step_size = step_size
        e = len(PYRAMID_EDGES)
        self.w = G.tensor([0.0] * e, requires_grad=True)       # edge weights
        self.alpha = G.tensor([0.0] * e, requires_grad=True)   # edge angles
        self.gain = G.tensor([1.0], requires_grad=True)
        self.relax = G.tensor([0.8], requires_grad=True)
        n_feat = 3 * N_CELLS
        self.w_out = G.tensor([0.0] * (n_feat * 3), requires_grad=True)
        self.b_out = G.tensor([0.0] * 3, requires_grad=True)

    # -- initializations ------------------------------------------------------

    def init_calculus(self) -> "GistSSM":
        """The GIST-NN point: exact pyramid weights, neutral angles."""
        self.w.data = [0.5] * len(PYRAMID_EDGES)
        self.alpha.data = [0.0] * len(PYRAMID_EDGES)
        self.gain.data = [1.0]
        self.relax.data = [0.8]
        # readout initialized to read the singular trit directly:
        # feature layout [zx(6), zy(6), trits(6)]; singular trit at 12 + 4
        w = [0.0] * (18 * 3)
        for cls in range(3):
            w[cls * 18 + 12 + 4] = 2.0 * (cls - 1)   # -2, 0, +2 vs trit
        self.w_out.data = w
        self.b_out.data = [0.0, 0.5, 0.0]            # mild prior toward 0
        return self

    def init_random(self, seed: int) -> "GistSSM":
        draw = _rng(seed * 31 + 7)
        self.w.data = [draw() - 0.5 for _ in PYRAMID_EDGES]
        self.alpha.data = [2.0 * (draw() - 0.5) for _ in PYRAMID_EDGES]
        self.gain.data = [0.5 + draw()]
        self.relax.data = [draw()]
        self.w_out.data = [0.6 * (draw() - 0.5) for _ in range(18 * 3)]
        self.b_out.data = [0.0, 0.0, 0.0]
        return self

    def params(self) -> list[G.Tensor]:
        return [self.w, self.alpha, self.gain, self.relax,
                self.w_out, self.b_out]

    def n_params(self) -> int:
        return sum(len(p) for p in self.params())

    # -- forward ---------------------------------------------------------------

    def forward(self, sample: Sample) -> G.Tensor:
        src = [s for s, _ in PYRAMID_EDGES]
        dst = [d for _, d in PYRAMID_EDGES]
        theta = G.tensor(sample.theta)
        amp = G.tensor(sample.amp)
        gain6 = G.concat([self.gain] * N_CELLS)
        relax6 = G.concat([self.relax] * N_CELLS)
        re_w = G.mul(self.w, G.cos(self.alpha))
        im_w = G.mul(self.w, G.sin(self.alpha))

        for _ in range(self.steps):
            zx = G.mul(amp, G.cos(theta))
            zy = G.mul(amp, G.sin(theta))
            ax, ay = G.complex_mix(re_w, im_w, src, dst, zx, zy, N_CELLS)
            # Kuramoto turn: dθ = gain · (Ay cosθ − Ax sinθ)
            turn = G.sub(G.mul(ay, G.cos(theta)), G.mul(ax, G.sin(theta)))
            theta = G.add(theta, G.scale(G.mul(gain6, turn), self.step_size))
            # amplitude relaxation toward |A| where afferents exist
            a_amp = G.sqrt(G.add(G.mul(ax, ax), G.mul(ay, ay)))
            gate = [1.0 if v > 1e-12 else 0.0 for v in a_amp.data]
            delta = G.mask(G.mul(relax6, G.sub(a_amp, amp)), gate)
            amp = G.add(amp, G.scale(delta, self.step_size))

        zx = G.mul(amp, G.cos(theta))
        zy = G.mul(amp, G.sin(theta))
        # the commit bottleneck: κ = cosθ gated by amplitude presence
        amp_gate = [1.0 if v > 1e-9 else 0.0 for v in amp.data]
        kappa = G.mask(G.cos(theta), amp_gate)
        trits = G.ste_trit(kappa, deadband=0.5)

        feats = G.concat([zx, zy, trits])
        logits = []
        for cls in range(3):
            row = G.gather(self.w_out, list(range(cls * 18, cls * 18 + 18)))
            logits.append(G.add(G.total(G.mul(row, feats)),
                                G.gather(self.b_out, [cls])))
        return G.concat(logits)

    def predict(self, sample: Sample) -> int:
        logits = self.forward(sample).data
        return logits.index(max(logits)) - 1

    # -- training ---------------------------------------------------------------

    def loss(self, sample: Sample) -> G.Tensor:
        return G.cross_entropy(self.forward(sample), sample.label + 1)

    def fit(self, data: list[Sample], epochs: int = 10,
            lr: float = 0.05) -> list[float]:
        """Plain SGD; returns per-epoch mean losses."""
        history = []
        for _ in range(epochs):
            total_loss = 0.0
            for sample in data:
                loss = self.loss(sample)
                loss.backward()
                G.sgd_step(self.params(), lr)
                total_loss += loss.data[0]
            history.append(total_loss / max(1, len(data)))
        return history

    def accuracy(self, data: list[Sample]) -> float:
        if not data:
            return 0.0
        hits = sum(1 for s in data if self.predict(s) == s.label)
        return hits / len(data)

    # -- export -------------------------------------------------------------------

    def export_weights(self) -> dict:
        return {
            "architecture": "GistSSM/slot-cell",
            "steps": self.steps,
            "step_size": self.step_size,
            "edges": [list(e) for e in PYRAMID_EDGES],
            "w": list(self.w.data),
            "alpha": list(self.alpha.data),
            "gain": self.gain.data[0],
            "relax": self.relax.data[0],
            "w_out": list(self.w_out.data),
            "b_out": list(self.b_out.data),
        }
