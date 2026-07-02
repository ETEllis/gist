# GIST — native `.cdc` build

**GIST (Gated Insight Synthesis Topology)** built completely out of the BiDi
Coherence-Delta Calculus, **in `.cdc`**, with **zero new host code**. It rides
subordinate on the BiDi bootstrap (`cdc_boot.py`) and the existing BiDi C
native runtime — the only non-`.cdc` "micro-bridge" in the loop, unchanged.

## Files (all native `.cdc`)

| file | role | runtime job |
|---|---|---|
| `gist.cdc` | kernel/self-hosting contract (`host-debt <= 0`) | `cdc_boot.py` |
| `gist_laws.cdc` | 6 invariants + 11 capabilities + witness registry | `cdc_boot.py` |
| `gist_lattice.cdc` | the 64-slot address system over bridge64 (3 axes × 4 values) | `cdc_boot.py` |
| `gist_pyramid.cdc` | the 3→2→1 synthesis pyramid + veto | `run` / `compile` / `interpret` / `prove` |
| `gist_cf.cdc` | Pearl `do()` counterfactual as twin fields (latch + severed channel) | `run` |
| `gist_cf2.cdc` | intervention cluster 2: sufficiency restoration, backdoor severance, frontdoor mediation | `run` |
| `gist_neural.cdc` | the field as neural net: flow jobs = layers, commit = ternary bottleneck, nest = pooling | `run` / `compile` / `interpret` |
| `gist_gate.cdc` | the emergent 64-gate (trace/measure/policy/bridge/counter/guard) | `surface` |
| `gist_ladder.cdc` | meta-gate ladder council + decision-stamp self-evolution | `council` / `evolve` |

## Verify (runs the whole gate through the existing BiDi runtimes)

```bash
# from this directory, with the BiDi repo at ../../bidi-coherence-delta-calculus
./verify_gist.sh
# or point at BiDi explicitly:
BIDI=/path/to/bidi-coherence-delta-calculus ./verify_gist.sh
```

The script executes every native job on the prebuilt `cdc_native_runtime`
(building it once from BiDi's own C sources if needed) and then checks the
`.cdc` contract through `cdc_boot.py`.

## What each job proves (all numbers are runtime-checked expectations)

- **pyramid** — `flow` folds evidence (θ→0.25); `commit` distils the triad to
  the admissible singular gist `0+-` (accepted); `nest` exchanges child
  coherence up (belief 2/3) and context down; the contested word `-+0` is
  **held** (`balance-violation`) — the native VDR veto. `prove` checks the
  finite n=6 normal-form spectrum **729 / 267 / 51 / 20 / 5** that grounds the
  release tiers.
- **counterfactual** — `do(r0 := -)` = a latched cell + a severed inbound
  channel (no new primitive). Factual conclusion commits `+`; the twin field
  under the intervention dissolves it to the crossing `0` — so `r0` is causal.
- **gate** — the committed slot word `+0-+0-` is read as a passive trace
  (4 events), a committing measurement (`+0-`, potential non-increasing), a
  policy window, a saturation counter (2+3−1=4), and a bridge coordinate
  **101101 → triadic 231**; the crossing cell reports an **open** aperture.
- **ladder** — the meta/aggregate/horizon council reconciles to coordinate
  **231**, meets quorum → **adopt**, and stamps it by self-evolving a source
  copy with the decision witness.

## Provenance / oracle

The Python package under `../src/gist_engine` (in the work folder) is **not**
the deliverable — it is the construction oracle. Its parity tests reproduce
the BiDi native-runtime witness values exactly, which is how every
expectation baked into these `.cdc` files was computed and cross-checked.
The shipped mechanism is the `.cdc` above; the calculus describes itself and
the BiDi micro-bridge runs it.
