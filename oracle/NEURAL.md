# GIST-NN — the functional form, and how to write it into a model

`gist_engine/neural.py` is the answer to two questions at once:

1. **"Could GIST be a neural network right now, in its functional form?"**
   Yes — and it is not a claim, it is a constructed object with equivalence
   proofs. `GistNeural.from_field(field)` derives every weight analytically
   from the calculus structure (no training, no data, no loss), and the
   test suite + contract witnesses prove it computes the *same reduction*
   as the reference engine: flow trajectories, amplitudes, beliefs,
   quantization, barrier, and attribution, state for state, over the full
   64-slot lattice with real evidence in it
   (`tests/test_neural.py`, witnesses `gist-neural-flow-equivalence`,
   `gist-neural-commit-equivalence`, `gist-neural-weight-roundtrip`).

2. **"How would it be written directly into an architecture — weights,
   convolutions — without impairing what it does?"** The invariant-by-
   invariant mapping below. The essence reduction is exact because the
   calculus's operators already *are* tensor-algebra citizens.

## The invariant → architecture map

| CDC invariant | Neural realization | Where proven |
|---|---|---|
| rotation ⟳ (gate ⊙) | **SO(2) weight blocks**: a channel (weight w, angle α) is the 2×2 block `w·[[cosα,−sinα],[sinα,cosα]]` on the cell's Cartesian state (x,y) = (a·cosθ, a·sinθ). Phase is weight *structure*. Complexly: one matrix, `A = M z`. | `test_angular_channel_rotation_block` |
| interfere ⊞ | plain summation — linearity of the afferent layer | flow equivalence |
| corefold ∂ | fixed averaging sub-blocks of M (the pyramid: read → dyad → singular, weights ½) | flow equivalence |
| flow ⟶_d | a **recurrent cell**: `A = Mz`; `dθᵢ = ωᵢ + gain·Im(Aᵢe^{−iθᵢ})` (the Kuramoto turn — `Im(Ae^{−iθ}) = |A|sin(argA−θ)` exactly, a bilinear form of state and afferent); amplitude relaxation `aᵢ += step·relax·(|Aᵢ|−aᵢ)`; belief `bₘ += step·[π(mean ReAₘ − bₘ) − (bₘ − b⁰ₘ)]` (linear pooling + exact gradient) | `test_flow_equivalence_full_lattice`, `test_multi_cycle_trajectory_equivalence` |
| commit ⟶_β quantization | the **ternary bottleneck**: `κ = cosθ` (0 at zero amplitude), `t = sign(κ)·1[|κ|>δ]` — a hard three-way nonlinearity | `test_quantization_equivalence` |
| trit-walk barrier (T1) | `walk = L·t` per module with L the lower-triangular ones matrix (a cumsum — linear!); `admissible = min(walk) ≥ 0`; the violating cell = argmin index (exact attribution) | `test_commit_head_barrier_equivalence` |
| 64-lattice | the vertices of the **6-cube**; slot address = the 6-bit dyadic word | `bridge.py` |
| ladder 64→…→1 | six **hypercube pooling layers**, each contracting one cube dimension (Hamming-1 pair fusion = ⊞ with an alignment rotation — a data-dependent SO(2), i.e. attention-like gating — then ∂) | `ladder.py` (engine-side; same ops) |
| gate + release | a readout head over the pooled state + threshold logic | `gate.py` (control flow) |

## What is tensor math vs control flow (stated, not waved)

The recurrent core — afferents, phase turn, amplitude, belief, quantization,
walk, admissibility, attribution — is pure tensor math and lives in
`GistNeural`. The commit's *hold/accept* branching, the ledger, intents, and
the stamp are control flow around that core; in-architecture they become
gating scalars (multiply the state delta by the accept bit) and host-side
logging. Delayed channels (`delay > 0`) need recurrent taps (a state history
buffer) and are rejected explicitly by `from_field` rather than silently
approximated. Plastic channels freeze at their current weight (Hebbian
updates are a standard outer-product learning rule if you want them live).

## Load it into torch (or jax) in a few lines

```python
from gist_engine import GistEngine, GistNeural
import json, torch

eng = GistEngine(prompt="...")           # or any CDC Field you built
nn_ref = GistNeural.from_field(eng.field)
w = nn_ref.export_weights()               # JSON-safe dict
W_re, W_im = map(torch.tensor, nn_ref.w.dense())   # [384, 384] each

def afferents(x, y):                      # x, y: [384] Cartesian state
    return W_re @ x - W_im @ y, W_re @ y + W_im @ x

def flow_step(theta, amp, step, gain=w["gain"]):
    x, y = amp * torch.cos(theta), amp * torch.sin(theta)
    ax, ay = afferents(x, y)
    a_amp = torch.hypot(ax, ay)
    dtheta = torch.tensor(w["omega"]) + gain * (ay * torch.cos(theta)
                                                - ax * torch.sin(theta))
    theta = theta + step * dtheta          # wrap as desired
    amp = torch.where(a_amp > 0,
                      amp + step * w["amp_relax"] * (a_amp - amp), amp)
    return theta, amp
```

The reference `GistNeural` remains the semantics oracle: any port (torch,
jax, CUDA kernel, silicon) can be differential-tested against it exactly the
way `GistNeural` is tested against the engine.

## Training on top (optional, forward-looking)

Nothing in GIST *requires* training — the weights are the meaning. But the
form is training-ready if you want it to be:

- the ternary bottleneck is the classic quantization nonlinearity: use a
  **straight-through estimator** (identity gradient inside the deadband
  cone) to backpropagate through commits;
- channel weights/angles are ordinary parameters (angles stay angles:
  parameterize the SO(2) blocks by α, not by 4 free entries, to preserve
  the rotation invariant);
- the barrier is a differentiable penalty `relu(−min(L·t̃))` on the soft
  trits `t̃ = tanh((|κ|−δ)/τ)·sign(κ)` if you want admissibility pressure
  in the loss rather than as a hard gate;
- the lattice/ladder is a fixed hypercube graph-conv + pooling stack — you
  can learn *around* it (projector in, readout out) without touching the
  invariants, which is exactly the "generalize without impairing" adapter:
  freeze M's structure, learn the semantic embedding into and out of it.
