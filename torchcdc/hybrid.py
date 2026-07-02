"""GistHybrid: the full-term GIST neural architecture.

The hybrid, in correct terminology, exactly as laid out:

  recurrent nonlinear STATE-SPACE core   K shared-weight recurrent steps of
      the Kuramoto phase turn dtheta = gain * Im(A e^{-i theta}) - a
      selective (state-dependent) nonlinear SSM over cell phases and
      amplitudes;

  CONVOLUTIONAL filtration               two weight-shared graph
      convolutions: (i) the corefold pyramid inside every slot (6 edge
      types shared across all slots - the intra-slot filter bank), and
      (ii) the Hamming-1 lattice convolution on the B-cube (one shared
      SO(2) weight per cube direction, coupling neighbor slots' singular
      cells) - the Sierpinski/bridge64 addressing IS the convolution
      topology;

  GATING                                 learnable openness gates: each
      cell's outbound influence is scaled by sigmoid(beta * (|kappa| -
      delta)) - the calculus's boundary-openness made a trainable gate
      (decisive cells transmit, crossing cells attenuate);

  balanced-TERNARY bottleneck            the commit quantizer with a
      straight-through gradient at readout - activations end as {-,0,+}
      words behind the same deadband the mechanism uses;

  LADDER pooling                         B hypercube contractions with a
      shared alignment rotation per round pool the 2^B slot singulars to
      one global state (the meta-gate ladder as a pooling stack).

Initialization at the calculus (init_calculus) sets the pyramid to the
exact corefold weights, neutral angles, unit gain - the provably-equivalent
GIST-NN point - and training then learns to ANTICIPATE the converged native
reduction from K partial steps.
"""

from __future__ import annotations

import json
import math

import numpy as np

try:
    from . import tensorcdc as tc
except ImportError:  # direct script use
    import tensorcdc as tc

PYRAMID_EDGES = ((0, 3), (1, 3), (1, 5), (2, 5), (3, 4), (5, 4))
CELLS = 6
SINGULAR = 4
DEADBAND = 0.5


class GistHybrid:
    """Batch model over an S-slot lattice scene (S = 2**bits)."""

    def __init__(self, bits: int = 3, steps: int = 4, step_size: float = 1.0,
                 lattice: bool = True, gating: bool = True,
                 bottleneck: bool = True, deploy: bool = False, seed: int = 0):
        self.bits = bits
        self.slots = 2 ** bits
        self.n = self.slots * CELLS
        self.steps = steps
        self.step_size = step_size
        self.use_lattice = lattice and bits > 0
        self.use_gating = gating and not deploy
        self.use_bottleneck = bottleneck
        # deploy mode: exact C-runtime parity - amplitude-blind dynamics
        # (relax pinned to 0, no gating), so the exported .cdc computes the
        # identical forward pass under `cdc_native_runtime infer`
        self.deploy = deploy

        # --- convolution kernels (weight-shared) ---
        e = len(PYRAMID_EDGES)
        self.pyr_w = tc.param(np.zeros(e))          # pyramid filter weights
        self.pyr_a = tc.param(np.zeros(e))          # pyramid filter angles
        self.lat_w = tc.param(np.zeros(bits))       # cube-direction weights
        self.lat_a = tc.param(np.zeros(bits))       # cube-direction angles
        # --- SSM dynamics ---
        self.gain = tc.param(np.array([1.0]))
        self.relax = tc.param(np.array([0.8]))
        # --- gating (openness) ---
        self.gate_beta = tc.param(np.array([4.0]))
        self.gate_delta = tc.param(np.array([DEADBAND]))
        # --- ladder pooling alignment (one rotation per round) ---
        self.ladder_a = tc.param(np.zeros(bits))
        # --- heads ---
        feat = 3 * CELLS                             # [zx, zy, trits] per slot
        self.w_slot = tc.param(np.zeros((feat, 3)))
        self.b_slot = tc.param(np.zeros(3))
        gfeat = 5                                    # ladder-root features
        self.w_glob = tc.param(np.zeros((gfeat, 3)))
        self.b_glob = tc.param(np.zeros(3))

        # static index plumbing
        src, dst = [], []
        for s in range(self.slots):
            base = s * CELLS
            for a, b in PYRAMID_EDGES:
                src.append(base + a)
                dst.append(base + b)
        self.pyr_src = np.array(src)
        self.pyr_dst = np.array(dst)
        self.pyr_type = np.tile(np.arange(e), self.slots)
        lsrc, ldst, ltype = [], [], []
        for s in range(self.slots):
            for b in range(bits):
                t = s ^ (1 << b)
                lsrc.append(s * CELLS + SINGULAR)
                ldst.append(t * CELLS + SINGULAR)
                ltype.append(b)
        self.lat_src = np.array(lsrc)
        self.lat_dst = np.array(ldst)
        self.lat_type = np.array(ltype)

        self._rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------ #

    def params(self):
        ps = [self.pyr_w, self.pyr_a, self.gain,
              self.w_slot, self.b_slot, self.w_glob, self.b_glob]
        if not self.deploy:
            ps.append(self.relax)
        if self.use_lattice:
            ps.append(self.ladder_a)
        if self.use_lattice:
            ps += [self.lat_w, self.lat_a]
        if self.use_gating:
            ps += [self.gate_beta, self.gate_delta]
        return ps

    def n_params(self):
        return sum(p.v.size for p in self.params())

    def init_calculus(self):
        """The GIST-NN point: exact corefold pyramid, neutral everything."""
        self.pyr_w.v[:] = 0.5
        self.pyr_a.v[:] = 0.0
        self.lat_w.v[:] = 0.05
        self.lat_a.v[:] = 0.0
        self.gain.v[:] = 1.0
        self.relax.v[:] = 0.0 if self.deploy else 0.8
        self.gate_beta.v[:] = 4.0
        self.gate_delta.v[:] = DEADBAND
        self.ladder_a.v[:] = 0.0
        self.w_slot.v[:] = 0.0
        # read the singular trit feature directly (feature block 2, cell 4)
        for cls in range(3):
            self.w_slot.v[2 * CELLS + SINGULAR, cls] = 2.0 * (cls - 1)
        self.b_slot.v[:] = np.array([0.0, 0.5, 0.0])
        self.w_glob.v[:] = 0.0
        self.w_glob.v[0, 0] = -2.0   # root kappa -> no
        self.w_glob.v[0, 2] = 2.0    # root kappa -> yes
        self.b_glob.v[:] = np.array([0.0, 0.5, 0.0])
        return self

    def init_random(self, seed: int):
        rng = np.random.default_rng(seed)
        for p, scale_ in ((self.pyr_w, 0.6), (self.pyr_a, 1.0),
                          (self.lat_w, 0.2), (self.lat_a, 1.0),
                          (self.ladder_a, 1.0),
                          (self.w_slot, 0.3), (self.w_glob, 0.3)):
            p.v[:] = rng.uniform(-scale_, scale_, size=p.v.shape)
        self.gain.v[:] = rng.uniform(0.5, 1.5)
        self.relax.v[:] = 0.0 if self.deploy else rng.uniform(0.2, 1.0)
        self.gate_beta.v[:] = rng.uniform(1.0, 6.0)
        self.gate_delta.v[:] = rng.uniform(0.2, 0.8)
        self.b_slot.v[:] = 0.0
        self.b_glob.v[:] = 0.0
        return self

    # ------------------------------------------------------------------ #

    def forward(self, theta0: np.ndarray, amp0: np.ndarray):
        """theta0, amp0: [batch, slots*6]. Returns (slot_logits [batch,
        slots, 3], global_logits [batch, 3], words [batch, slots*6])."""
        theta = tc.const(theta0)
        amp = tc.const(amp0)

        edge_w = tc.gather(self.pyr_w, self.pyr_type)
        edge_a = tc.gather(self.pyr_a, self.pyr_type)
        re_p = tc.mul(edge_w, tc.cos(edge_a))
        im_p = tc.mul(edge_w, tc.sin(edge_a))
        if self.use_lattice:
            lw = tc.gather(self.lat_w, self.lat_type)
            la = tc.gather(self.lat_a, self.lat_type)
            re_l = tc.mul(lw, tc.cos(la))
            im_l = tc.mul(lw, tc.sin(la))

        for _ in range(self.steps):
            zx = tc.mul(amp, tc.cos(theta))
            zy = tc.mul(amp, tc.sin(theta))
            if self.use_gating:
                # openness gate: decisive cells transmit, crossings attenuate
                kap = tc.cos(theta)
                mag = tc.sqrt(tc.mul(kap, kap))
                pre = tc.mul(self.gate_beta,
                             tc.sub(mag, self.gate_delta))
                gv = 1.0 / (1.0 + np.exp(-np.clip(pre.v, -30, 30)))
                g = tc._op(gv, (pre,), None)

                def back(pre=pre, g=g, gv=gv):
                    pre.g += g.g * gv * (1.0 - gv)
                g._back = back
                zx = tc.mul(zx, g)
                zy = tc.mul(zy, g)
            # pyramid convolution (complex mix over shared edge filters)
            ax_e = tc.mul(re_p, _gl(zx, self.pyr_src))
            ax_e = tc.sub(ax_e, tc.mul(im_p, _gl(zy, self.pyr_src)))
            ay_e = tc.add(tc.mul(re_p, _gl(zy, self.pyr_src)),
                          tc.mul(im_p, _gl(zx, self.pyr_src)))
            ax = _sl(ax_e, self.pyr_dst, self.n)
            ay = _sl(ay_e, self.pyr_dst, self.n)
            if self.use_lattice:
                lx = tc.sub(tc.mul(re_l, _gl(zx, self.lat_src)),
                            tc.mul(im_l, _gl(zy, self.lat_src)))
                ly = tc.add(tc.mul(re_l, _gl(zy, self.lat_src)),
                            tc.mul(im_l, _gl(zx, self.lat_src)))
                ax = tc.add(ax, _sl(lx, self.lat_dst, self.n))
                ay = tc.add(ay, _sl(ly, self.lat_dst, self.n))
            # the Kuramoto turn (selective SSM update)
            turn = tc.sub(tc.mul(ay, tc.cos(theta)), tc.mul(ax, tc.sin(theta)))
            theta = tc.add(theta, tc.scale(tc.mul(self.gain, turn),
                                           self.step_size))
            a_amp = tc.sqrt(tc.add(tc.mul(ax, ax), tc.mul(ay, ay)))
            live = (a_amp.v > 1e-12).astype(float)
            amp = tc.add(amp, tc.scale(
                tc.gate(tc.mul(self.relax, tc.sub(a_amp, amp)), live),
                self.step_size))

        # readout features
        zx = tc.mul(amp, tc.cos(theta))
        zy = tc.mul(amp, tc.sin(theta))
        occupied = (amp.v > 1e-9).astype(float)
        kappa = tc.gate(tc.cos(theta), occupied)
        trits = tc.ste_trit(kappa, DEADBAND) if self.use_bottleneck else kappa

        batch = theta0.shape[0]
        f = tc.concat_last([
            _reshape(zx, (batch, self.slots, CELLS)),
            _reshape(zy, (batch, self.slots, CELLS)),
            _reshape(trits, (batch, self.slots, CELLS)),
        ])                                            # [batch, slots, 18]
        f2 = _reshape(f, (batch * self.slots, 3 * CELLS))
        slot_logits = tc.add(tc.matmul(f2, self.w_slot),
                             _row(self.b_slot, batch * self.slots))
        slot_logits = _reshape(slot_logits, (batch, self.slots, 3))

        # ladder pooling on singular states -> global verdict
        gx = _reshape(zx, (batch, self.slots, CELLS))
        gx = _take(gx, SINGULAR)                      # [batch, slots]
        gy = _take(_reshape(zy, (batch, self.slots, CELLS)), SINGULAR)
        for r in range(self.bits):
            half = 2 ** (self.bits - r - 1)
            axl, axr = _split(gx, half)
            ayl, ayr = _split(gy, half)
            ca = math.cos(float(self.ladder_a.v[r]))
            sa = math.sin(float(self.ladder_a.v[r]))
            rot_x = tc.sub(tc.scale(axr, ca), tc.scale(ayr, sa))
            rot_y = tc.add(tc.scale(ayr, ca), tc.scale(axr, sa))
            gx = tc.scale(tc.add(axl, rot_x), 0.5)
            gy = tc.scale(tc.add(ayl, rot_y), 0.5)
        root_amp = tc.sqrt(tc.add(tc.mul(gx, gx), tc.mul(gy, gy)))
        denom = np.clip(root_amp.v, 1e-9, None)
        root_kappa = tc._op(gx.v / denom, (gx,), None)

        def back_rk(gx=gx, root_kappa=root_kappa, denom=denom):
            gx.g += root_kappa.g / denom
        root_kappa._back = back_rk

        mean_trit = tc.mean_last(_reshape(trits, (batch, self.slots * CELLS)))
        gfeat = tc.concat_last([
            root_kappa, root_amp, gx, gy, mean_trit,
        ])                                            # [batch, 5]
        global_logits = tc.add(tc.matmul(gfeat, self.w_glob),
                               _row(self.b_glob, batch))
        return slot_logits, global_logits, trits

    # ------------------------------------------------------------------ #

    def predict(self, theta0, amp0):
        sl, gl, _ = self.forward(theta0, amp0)
        return sl.v.argmax(axis=2) - 1, gl.v.argmax(axis=1) - 1

    def export_weights(self) -> dict:
        return {
            "architecture": "GistHybrid",
            "bits": self.bits, "slots": self.slots, "steps": self.steps,
            "step_size": self.step_size,
            "pyramid_edges": [list(e) for e in PYRAMID_EDGES],
            "pyr_w": self.pyr_w.v.tolist(), "pyr_a": self.pyr_a.v.tolist(),
            "lat_w": self.lat_w.v.tolist(), "lat_a": self.lat_a.v.tolist(),
            "gain": float(self.gain.v[0]), "relax": float(self.relax.v[0]),
            "gate_beta": float(self.gate_beta.v[0]),
            "gate_delta": float(self.gate_delta.v[0]),
            "ladder_a": self.ladder_a.v.tolist(),
            "w_slot": self.w_slot.v.tolist(), "b_slot": self.b_slot.v.tolist(),
            "w_glob": self.w_glob.v.tolist(), "b_glob": self.b_glob.v.tolist(),
            "use": {"lattice": self.use_lattice, "gating": self.use_gating,
                    "bottleneck": self.use_bottleneck,
                    "deploy": self.deploy},
        }

    @staticmethod
    def load(d: dict) -> "GistHybrid":
        m = GistHybrid(bits=d["bits"], steps=d["steps"],
                       step_size=d["step_size"], lattice=d["use"]["lattice"],
                       gating=d["use"]["gating"],
                       bottleneck=d["use"]["bottleneck"],
                       deploy=d["use"].get("deploy", False))
        m.pyr_w.v[:] = d["pyr_w"]
        m.pyr_a.v[:] = d["pyr_a"]
        m.lat_w.v[:] = d["lat_w"]
        m.lat_a.v[:] = d["lat_a"]
        m.gain.v[:] = d["gain"]
        m.relax.v[:] = d["relax"]
        m.gate_beta.v[:] = d["gate_beta"]
        m.gate_delta.v[:] = d["gate_delta"]
        m.ladder_a.v[:] = d["ladder_a"]
        m.w_slot.v[:] = d["w_slot"]
        m.b_slot.v[:] = d["b_slot"]
        m.w_glob.v[:] = d["w_glob"]
        m.b_glob.v[:] = d["b_glob"]
        return m

    def save(self, path):
        with open(path, "w") as fh:
            json.dump(self.export_weights(), fh, indent=1)


# --- small structural helpers on tensorcdc -----------------------------------


def _gl(t, idx):
    """Gather along the last axis (batch-aware)."""
    out = tc._op(t.v[..., idx], (t,), None)

    def back():
        if t.v.ndim == 1:
            np.add.at(t.g, idx, out.g)
        else:
            np.add.at(t.g, (slice(None), idx), out.g)
    out._back = back
    return out


def _sl(t, idx, size):
    return tc.scatter_sum(t, idx, size)


def _reshape(t, shape):
    out = tc._op(t.v.reshape(shape), (t,), None)

    def back():
        t.g += out.g.reshape(t.v.shape)
    out._back = back
    return out


def _row(bias, n):
    out = tc._op(np.tile(bias.v, (n, 1)), (bias,), None)

    def back():
        bias.g += out.g.sum(axis=0)
    out._back = back
    return out


def _take(t, index):
    out = tc._op(t.v[:, :, index], (t,), None)

    def back():
        t.g[:, :, index] += out.g
    out._back = back
    return out


def _split(t, half):
    left = tc._op(t.v[:, :half], (t,), None)
    right = tc._op(t.v[:, half:], (t,), None)

    def back_l():
        t.g[:, :half] += left.g

    def back_r():
        t.g[:, half:] += right.g
    left._back = back_l
    right._back = back_r
    return left, right



# register helpers used above onto tensorcdc namespace for readability
def _tc_concat_last(parts):
    arrs = []
    for p in parts:
        v = p.v
        if v.ndim == 1:
            v = v[:, None]
        arrs.append(v)
    out = tc._op(np.concatenate(arrs, axis=-1), tuple(parts), None)
    offs = np.cumsum([0] + [a.shape[-1] for a in arrs])

    def back():
        for p, lo, hi in zip(parts, offs[:-1], offs[1:]):
            g = out.g[..., lo:hi]
            p.g += g[..., 0] if p.v.ndim == 1 else g
    out._back = back
    return out


def _tc_mean_last(t):
    out = tc._op(t.v.mean(axis=-1), (t,), None)

    def back():
        t.g += out.g[..., None] / t.v.shape[-1]
    out._back = back
    return out


tc.concat_last = _tc_concat_last
tc.mean_last = _tc_mean_last
