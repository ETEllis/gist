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
./run.sh '+0-'     # the trained hybrid, natively: evidence word -> verdict
./run.sh           # the full verification gate: 83/83 expectations,
                   # 70 native witnesses, host-debt 0
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
| **The trained hybrid** | [`torchcdc/`](torchcdc) | **GistHybrid** — recurrent nonlinear state-space core × convolutional filtration (corefold pyramid + hypercube lattice conv) × openness gating × balanced-ternary bottleneck × ladder pooling. Trained against labels the **native runtime itself produces**: 64-slot slot accuracy **0.984**, global verdict **0.868**, and the exported weights reproduce the model **27/27** under native `infer`. |
| **Reference + adapters** (Python) | [`oracle/`](oracle) | the full-featured reference engine with MCP server, tool-call spec, reasoning-loop stitcher, replay-verified ledgers — 100 tests + a 36-witness contract. Construction/adapter tier, not the mechanism. |
| **The paper** | [`paper/`](paper) | what GIST is pre-neural-net, the calculus derivation, the do-operator, the hybrid architecture and results, and the LLM training-translation plan. |

## Why the neural network is not a metaphor

The forward pass **is** the calculus: channels are SO(2) weight blocks,
flow steps are recurrent layers (the Kuramoto turn — a selective nonlinear
state-space update), commit is the ternary bottleneck, nest/ladder is the
pooling stack, and learning exists natively (plastic weights follow phase
correlation — `native/gist_learn.cdc`, runtime-checked). `torchcdc`
initializes **at the calculus** and trains to *anticipate* the converged
native reduction — then exports back to `.cdc`, where the same C runtime
that verifies the mechanism runs the trained model. One substrate,
closed loop.

## Trying it

```bash
./run.sh '++-'          # decisive support        -> yes
./run.sh '-0-'          # leading contradiction   -> held, mirror -> no
./run.sh '000'          # open aperture           -> maybe (ask for evidence)
cd torchcdc && python3 train.py           # reproduce the training results
cd torchcdc && python3 test_torchcdc.py   # the harness battery
cd native  && ./verify_gist.sh            # the whole native gate
```

## Lineage

GIST is the first CDC-native system: the
[BiDi Coherence-Delta Calculus](https://github.com/ETEllis/bidi-coherence-delta-calculus)
is the substrate and bootstrap (its `cdc_boot.py` + C runtime are the only
non-`.cdc` code in the loop). The runtime extension (plasticity + infer)
is slated for upstreaming. MIT license throughout.
