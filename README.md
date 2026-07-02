# GIST — Gated Insight Synthesis Topology

**A synthesis mechanism written in a calculus, verified by its runtime, and
trainable as the neural network it already is.**

GIST is built *entirely* out of the
[BiDi Coherence-Delta Calculus](https://github.com/ETEllis/bidi-coherence-delta-calculus)
— this repository is the first system to bootstrap CDC-first: the mechanism
is native `.cdc` executed by BiDi's C micro-bridge (vendored here,
extended with native learning and inference), with **zero host code of its
own** (`host-debt 0`, machine-checked).

```bash
./run.sh '++-'     # the natively-trained net: evidence word -> verdict
./run.sh           # the full gate: verify, TRAIN (in C, from .cdc data,
                   # to .cdc weights), evaluate held-out, infer
```

## The one idea, at every scale

Evidence superposes as phases; a corefold pyramid distills a triad to a
dyad to a singular; a guarded **balanced-ternary commit** quantizes it —
`+` asserted, `−` opposed, `0` a live open aperture (never "false") —
behind a barrier that *holds* contradiction-debt instead of latching it.
The same operation runs fractally: within a slot, across the 64-slot
(2⁶ = 4³, bridge64-addressed) lattice, and up a Hamming ladder whose
reduction tree is its own Merkle tree. Release is gated, attributed, and
replayable.

## What is in this repository

| layer | where | what is proven |
|---|---|---|
| **The mechanism** (native `.cdc`) | [`native/`](native) | kernel contract, 64-lattice, synthesis pyramid + veto, Pearl **do()** as latched cell + severed channel (necessity, sufficiency, backdoor, frontdoor — twin fields), the field-as-neural-network forward pass, **native Hebbian learning**, emergent 64-gate, ladder council + decision stamp. `./verify_gist.sh`: **83/83 expectations, 70 witnesses, host-debt 0** through BiDi's own runtime + bootloader. |
| **The runtime bridge** (vendored, extended) | [`runtime/`](runtime) | BiDi's C native runtime + `cdc_boot.py`, extended with `plastic=1 rate=r` channel learning and the `infer` command (weights `.cdc` + input word → committed verdict). |
| **Native training** (`.cdc` in, `.cdc` out) | [`native/`](native) | `gist_train_net.cdc` + `gist_scenes_*.cdc` (datasets **as `.cdc`**, labels computed by the runtime's own converged reduction) → `cdc_native_runtime train` — clamped-teacher plasticity through flow, no host code — → `gist_trained.cdc`. Held-out accuracy **0.813 untrained → 0.933 trained**. The learned weights load straight back into `infer`. |
| **The hybrid reference** (results quoted; harness not shipped) | [`paper/`](paper) §4 | the full GistHybrid — recurrent state-space × convolution × gating × ternary bottleneck × ladder pooling — trained by gradient as a construction-tier experiment: 64-slot slot accuracy 0.984, global verdict 0.868, 27/27 native parity. The code stays out of this repo by project constraint: **the repo is CDC**. |
| **Adapters** (described, not shipped) | [`paper/`](paper) §5 | an MCP server, an architecture-agnostic tool-call spec, and a reasoning-loop stitcher exist as a reference-tier implementation (100 tests, 36-witness contract of its own, replay-verified ledgers). Deliberately **not** in this repository: the mechanism is the `.cdc`, and this repo stays that way. |
| **The paper** | [`paper/`](paper) | what GIST is pre-neural-net, the calculus derivation, the do-operator, the hybrid architecture and results, and the LLM training-translation plan. |

## Why the neural network is not a metaphor

The forward pass **is** the calculus: channels are SO(2) weight blocks,
flow steps are recurrent layers (the Kuramoto turn — a selective nonlinear
state-space update), commit is the ternary bottleneck, nest/ladder is the
pooling stack, and learning exists natively (plastic weights follow phase
correlation — `native/gist_learn.cdc`, runtime-checked). Training is
native too: `cdc_native_runtime train` clamps the conclusion cell at the
teacher label (a do()-style latch) and lets plasticity adapt the weights
through ordinary flow — datasets are `.cdc`, learned weights are `.cdc`,
and the same runtime that verifies the mechanism trains and runs it. One
substrate, closed loop.

## Trying it

```bash
./run.sh '++-'          # decisive support        -> yes
./run.sh '-0-'          # leading contradiction   -> held, mirror -> no
./run.sh '000'          # open aperture           -> maybe (ask for evidence)
cd native && ../runtime/build/cdc_native_runtime \
   train gist_train_net.cdc net gist_scenes_train.cdc 10 my_weights.cdc
                        # train it yourself - in C, from .cdc, to .cdc
cd native && ./verify_gist.sh             # the whole gate incl. training
```

> **Note on the language bar:** GitHub labels `.cdc` files as "Cadence" (an
> unrelated language sharing the extension). Every `.cdc` file here is BiDi
> Coherence-Delta Calculus source — the mechanism itself.

## Lineage

GIST is the first CDC-native system: the
[BiDi Coherence-Delta Calculus](https://github.com/ETEllis/bidi-coherence-delta-calculus)
is the substrate and bootstrap (its `cdc_boot.py` + C runtime are the only
non-`.cdc` code in the loop). The runtime extension (plasticity + infer)
is slated for upstreaming. MIT license throughout.
