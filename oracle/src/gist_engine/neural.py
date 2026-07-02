"""GIST-NN: the engine's functional form as an analytically-built neural net.

No training, no dataset, no loss curve: the weights are *derived* from a
CDC field's declared structure, and equivalence tests prove the network
computes the same reduction as the reference engine, state for state. This
is the "essence reduction" - the invariants that make GIST what it is,
carried into tensor form with nothing lost:

  rotation ⟳        SO(2) weight blocks: a channel with weight w and angular
                    bias α is the 2x2 block  w·[[cosα, -sinα],[sinα, cosα]]
                    acting on the cell's (x, y) = (a·cosθ, a·sinθ) state.
                    Complexly: one matrix M with A = M·z. Phase is weight
                    structure, not activation folklore.

  interfere ⊞       summation - the linear layer's own additivity.

  corefold ∂        fixed averaging sub-blocks of M (the pyramid).

  flow ⟶_d          a recurrent cell (one per realization step):
                        A       = M z                    (linear, complex)
                        dθ_i    = ω_i + gain·Im(A_i e^{-iθ_i})   (Kuramoto)
                        θ_i    += step·dθ_i
                        a_i    += step·relax·(|A_i| - a_i)
                        b_m    += step·[π·(mean Re A_m - b_m) - (b_m - b⁰_m)]
                    Im(A e^{-iθ}) = |A|·sin(arg A - θ) exactly - the phase
                    turn is a bilinear form of state and afferent, a bona
                    fide recurrent nonlinearity.

  commit ⟶_β        a quantization head:
                        κ_i  = cosθ_i (0 where a_i = 0)
                        t_i  = sign(κ_i)·1[|κ_i| > δ]        (ternary bottleneck)
                        walk = L·t per module (L = lower-triangular ones)
                        admissible = min(walk) ≥ 0            (the barrier)
                    Hold/accept/latch are gating scalars around this head.

  lattice/ladder    the 64 slots are the vertices of the 6-cube; the ladder
                    is six pooling layers, each contracting one hypercube
                    dimension (documented in NEURAL.md; the recurrent core
                    here is the substrate they pool over).

Scope (stated, not waved): this module covers the recurrent core - flow,
quantization, barrier - with exact equivalence to `field.Field`. Delayed
channels (delay > 0) need recurrent taps and are rejected explicitly;
plastic channels are frozen at their current weight. The commit's
hold/accept control flow and the ledger remain engine-side (they are
control logic, not tensor math); NEURAL.md maps them to gating for an
in-architecture implementation, and `export_weights()` emits everything a
torch/jax port needs.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field as dc_field
from typing import Any

from .field import Field
from .walks import first_violation, is_admissible


@dataclass
class NeuralWeights:
    """The complete analytic parameterization of a field's recurrent core."""

    n_cells: int
    cell_index: list[str]                      # "module:idx" per state row
    modules: list[str]
    module_of: list[int]                       # cell row -> module row
    # sparse complex afferent matrix: A = M z
    entries: list[tuple[int, int, float, float]]   # (dst, src, re, im)
    omega: list[float]
    gain: float
    dt: float
    deadband: float
    amp_relax: float
    belief: list[float]                        # per module
    prior: list[float]
    precision: list[float]

    def to_json(self) -> dict[str, Any]:
        return {
            "n_cells": self.n_cells,
            "cell_index": self.cell_index,
            "modules": self.modules,
            "module_of": self.module_of,
            "entries": [list(e) for e in self.entries],
            "omega": self.omega,
            "gain": self.gain,
            "dt": self.dt,
            "deadband": self.deadband,
            "amp_relax": self.amp_relax,
            "belief": self.belief,
            "prior": self.prior,
            "precision": self.precision,
        }

    @staticmethod
    def from_json(d: dict[str, Any]) -> "NeuralWeights":
        return NeuralWeights(
            n_cells=d["n_cells"],
            cell_index=list(d["cell_index"]),
            modules=list(d["modules"]),
            module_of=list(d["module_of"]),
            entries=[tuple(e) for e in d["entries"]],
            omega=list(d["omega"]),
            gain=d["gain"],
            dt=d["dt"],
            deadband=d["deadband"],
            amp_relax=d["amp_relax"],
            belief=list(d["belief"]),
            prior=list(d["prior"]),
            precision=list(d["precision"]),
        )

    def dense(self) -> tuple[list[list[float]], list[list[float]]]:
        """(W_re, W_im) dense matrices for direct nn.Linear-style loading."""
        w_re = [[0.0] * self.n_cells for _ in range(self.n_cells)]
        w_im = [[0.0] * self.n_cells for _ in range(self.n_cells)]
        for dst, src, re, im in self.entries:
            w_re[dst][src] += re
            w_im[dst][src] += im
        return w_re, w_im


class GistNeural:
    """The recurrent core, executable in pure Python (reference semantics)."""

    def __init__(self, weights: NeuralWeights,
                 theta: list[float], amp: list[float]):
        self.w = weights
        self.theta = list(theta)
        self.amp = list(amp)
        self.belief = list(weights.belief)

    # -- construction --------------------------------------------------------

    @staticmethod
    def from_field(field: Field) -> "GistNeural":
        """Derive the network analytically from a live field. Zero training."""
        cell_index: list[str] = []
        row_of: dict[str, int] = {}
        modules = list(field.modules)
        module_row = {name: i for i, name in enumerate(modules)}
        module_of: list[int] = []
        omega: list[float] = []
        theta: list[float] = []
        amp: list[float] = []
        for name, m in field.modules.items():
            for i, cell in enumerate(m.cells):
                key = f"{name}:{i}"
                row_of[key] = len(cell_index)
                cell_index.append(key)
                module_of.append(module_row[name])
                omega.append(cell.omega)
                theta.append(cell.theta)
                amp.append(cell.amp)

        entries: list[tuple[int, int, float, float]] = []
        for ch in field.channels:
            if ch.delay != 0.0:
                raise ValueError(
                    "GistNeural covers delay=0 channels; delayed channels "
                    "need recurrent taps (see NEURAL.md)"
                )
            rot_re = ch.weight * math.cos(ch.angle)
            rot_im = ch.weight * math.sin(ch.angle)
            # source rows and their linear coefficients
            if ":" in ch.src:
                src_rows = [(row_of[ch.src], 1.0)]
            else:
                m = field.modules[ch.src]
                cone = m.write_cone
                coef = 1.0 / len(cone) if cone else 0.0
                src_rows = [(row_of[f"{ch.src}:{i}"], coef) for i in cone]
            # destination rows
            if ":" in ch.dst:
                dst_rows = [row_of[ch.dst]]
            else:
                m = field.modules[ch.dst]
                targets = ch.lines if ch.lines is not None else m.read_cone
                dst_rows = [row_of[f"{ch.dst}:{i}"] for i in targets]
            for d in dst_rows:
                for s, coef in src_rows:
                    entries.append((d, s, rot_re * coef, rot_im * coef))

        weights = NeuralWeights(
            n_cells=len(cell_index),
            cell_index=cell_index,
            modules=modules,
            module_of=module_of,
            entries=entries,
            omega=omega,
            gain=field.gain,
            dt=field.dt,
            deadband=field.deadband,
            amp_relax=field.amp_relax,
            belief=[field.modules[n].belief for n in modules],
            prior=[field.modules[n].prior for n in modules],
            precision=[field.modules[n].precision for n in modules],
        )
        return GistNeural(weights, theta, amp)

    # -- the recurrent cell ---------------------------------------------------

    def afferents(self) -> tuple[list[float], list[float]]:
        """A = M z in Cartesian components (the linear layer)."""
        n = self.w.n_cells
        ax = [0.0] * n
        ay = [0.0] * n
        zx = [self.amp[i] * math.cos(self.theta[i]) for i in range(n)]
        zy = [self.amp[i] * math.sin(self.theta[i]) for i in range(n)]
        for dst, src, re, im in self.w.entries:
            # complex multiply (re + i·im)·(zx + i·zy)
            ax[dst] += re * zx[src] - im * zy[src]
            ay[dst] += re * zy[src] + im * zx[src]
        return ax, ay

    def flow_step(self, step: float) -> None:
        """One synchronous Euler step - the recurrent cell forward pass.

        Matches field._flow_step exactly: afferents evaluated against the
        pre-step state, then phase turn, amplitude relaxation, and the
        belief gradient step, in that order.
        """
        w = self.w
        ax, ay = self.afferents()
        # per-module mean Re A (linear pooling), computed pre-update
        n_mod = len(w.modules)
        mod_sum = [0.0] * n_mod
        mod_cnt = [0] * n_mod
        for i in range(w.n_cells):
            mod_sum[w.module_of[i]] += ax[i]
            mod_cnt[w.module_of[i]] += 1
        # cells
        for i in range(w.n_cells):
            a_amp = math.hypot(ax[i], ay[i])
            dtheta = w.omega[i]
            if a_amp > 0.0:
                # |A|·sin(arg A − θ) = Im(A·e^{-iθ}) = Ay·cosθ − Ax·sinθ
                dtheta += w.gain * (
                    ay[i] * math.cos(self.theta[i])
                    - ax[i] * math.sin(self.theta[i])
                )
            self.theta[i] = _wrap(self.theta[i] + step * dtheta)
            if w.amp_relax > 0.0 and a_amp > 0.0:
                self.amp[i] += step * w.amp_relax * (a_amp - self.amp[i])
                self.amp[i] = max(0.0, self.amp[i])
        # beliefs (exact gradient of the potential's belief terms)
        for m in range(n_mod):
            if mod_cnt[m]:
                mean_re = mod_sum[m] / mod_cnt[m]
                db = (w.precision[m] * (mean_re - self.belief[m])
                      - (self.belief[m] - w.prior[m]))
                self.belief[m] += step * db

    def flow(self, duration: float) -> None:
        remaining = duration
        while remaining > 1e-12:
            step = min(self.w.dt, remaining)
            self.flow_step(step)
            remaining -= step

    # -- the quantization head -------------------------------------------------

    def quantize(self) -> list[int]:
        """The ternary bottleneck: κ thresholded at the deadband."""
        out = []
        for i in range(self.w.n_cells):
            if self.amp[i] == 0.0:
                out.append(0)
                continue
            k = math.cos(self.theta[i])
            out.append(1 if k > self.w.deadband
                       else (-1 if k < -self.w.deadband else 0))
        return out

    def commit_head(self, module: str) -> dict[str, Any]:
        """Candidate word + barrier for one module (the tensorizable part
        of the commit; hold/accept control flow stays engine-side)."""
        rows = [i for i in range(self.w.n_cells)
                if self.w.modules[self.w.module_of[i]] == module]
        trits = [self.quantize()[i] for i in rows]
        return {
            "module": module,
            "trits": trits,
            "walk": _cumsum(trits),
            "admissible": is_admissible(trits),
            "violation_cell": first_violation(trits),
        }

    # -- persistence -----------------------------------------------------------

    def export_weights(self) -> dict[str, Any]:
        return self.w.to_json()

    def export_state(self) -> dict[str, Any]:
        return {"theta": list(self.theta), "amp": list(self.amp),
                "belief": list(self.belief)}

    @staticmethod
    def load(weights_json: dict[str, Any],
             state_json: dict[str, Any]) -> "GistNeural":
        w = NeuralWeights.from_json(weights_json)
        nn = GistNeural(w, state_json["theta"], state_json["amp"])
        nn.belief = list(state_json["belief"])
        return nn

    @staticmethod
    def loads(payload: str) -> "GistNeural":
        d = json.loads(payload)
        return GistNeural.load(d["weights"], d["state"])

    def dumps(self) -> str:
        return json.dumps(
            {"weights": self.export_weights(), "state": self.export_state()}
        )


def _wrap(a: float) -> float:
    a = math.fmod(a + math.pi, 2.0 * math.pi)
    if a <= 0.0:
        a += 2.0 * math.pi
    return a - math.pi


def _cumsum(xs: list[int]) -> list[int]:
    out = []
    r = 0
    for x in xs:
        r += x
        out.append(r)
    return out
