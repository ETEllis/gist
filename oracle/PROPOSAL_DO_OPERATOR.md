# PROPOSAL — Full do-operator integration into GIST

**Status: awaiting sign-off.** This is the design + refinement-test protocol
for integrating Judea Pearl's do-operator into the GIST engine — the full,
no-handwaving sort: all three rungs of the causal ladder, executable
do-calculus rules, identification with honest refusal, and
abduction–action–prediction counterfactuals — derived from the calculus the
engine is already built on, not bolted beside it. Nothing below requires
changing the CDC kernel semantics; the causal layer is *derived*, exactly
the way the trace/window observer layer is derived.

---

## 0 · Gap analysis: what exists, what "full" adds

The engine today already executes two genuinely interventional mechanics:

- `metrics.cf_agreement`: do(read-cell ← pole flip) on an exact twin module
  (the twin network), re-reduce, test survival — a rung-2 *probe*;
- `field.commit`'s energy/barrier guards and the mutilate-style vacuum twin
  in `causal_lift`.

What full Pearl adds, in his own ladder:

| Rung | Query form | Engine today | This proposal |
|---|---|---|---|
| 1 Association | P(Y \| X) | superposition + coherence metrics | unchanged |
| 2 Intervention | P(Y \| do(X)) | structural probes, no identification | first-class `do()`, d-separation, Rules 1–3, backdoor/frontdoor identification, honest refusal on non-identifiable queries |
| 3 Counterfactual | P(Y_x \| X=x′, Y=y′) | survival probes only | abduction–action–prediction with an exact exogenous posterior; PN / PS / PNS |

**The load-bearing insight (why this drops in cleanly):** the calculus
already supplies the three hard parts of causal inference.

1. **Graph surgery is native.** Channels are first-class terms. do(X=x) is
   literally: sever X's inbound channels, latch X's cells at the pole for
   x. That is Pearl's mutilated graph G_X̄, and it is a five-line operation
   on a `Field` copy — the same mechanics `cf_agreement` already uses,
   promoted to a first-class operator.
2. **The balanced-ternary carrier makes exact inference tractable.** The
   exogenous variables U of the induced SCM are the cells' initial states,
   and the deadband quantizes them into trit classes. A query touching k
   undetermined cells has at most 3^k exogenous classes — *enumerable
   exactly* for the scoped subgraphs GIST works with (typically k ≤ 8–10,
   i.e. ≤ 59,049 classes; a hard cap with an honest "scope too wide"
   refusal beyond it). No MCMC, no variational hand-waving: exact sums,
   replay-verifiable like everything else in the ledger.
3. **The twin network is the nesting operator.** Pearl's twin-network
   counterfactual construction (factual and counterfactual worlds sharing
   exogenous state) is exactly `m⟦F⟧` — the calculus's nested field with
   shared cell initializations — already executable via `field.nest` and
   the twin copies the metrics build.

---

## 1 · Design

New module `src/gist_engine/causal.py` plus small, listed touch-points.
No kernel changes; every existing test stays green.

### 1.1 The SCM surface

```python
@dataclass
class CausalVariable:
    name: str                 # "SCFA_production"
    slots: tuple[int, ...]    # lattice scopes carrying its evidence
    cells: tuple[str, ...]    # bound cell paths ("slot/000101:4", ...)

@dataclass
class CausalModel:            # induced, never asserted
    variables: dict[str, CausalVariable]
    edges: list[tuple[str, str, float]]   # from channel structure/weights
    def digraph(self) -> ...              # the DAG (cycles rejected w/ report)
```

The host names variables and binds them to scopes (the projector seam,
consistent with the engine's semantics/geometry boundary); the *edges*
come from declared channels or from a host-declared DAG compiled INTO
channels (`compile_scm(dag) -> Field`) — the same object serves both
"extract the SCM the lattice already embodies" and "load a known SCM and
reason over it."

### 1.2 Rung 2 — `do`, d-separation, rules, identification

```python
field.do({"X": +1}) -> Field          # mutilated twin: sever + latch (exact)
causal.d_separated(G, X, Y, Z) -> bool
causal.rule1/rule2/rule3(G, query) -> rewritten query | None   # executable
causal.identify(G, "P(Y|do(X))") -> Estimand | NotIdentifiable
```

- **d-separation**: pure graph algorithm on the module DAG (Bayes-ball).
- **Rules 1–3 of do-calculus** implemented as query rewrites whose side
  conditions are d-separation checks on the mutilated graphs G_X̄, G_X̄Z̲ —
  each application is *logged to the ledger* as a derivation step, so an
  identification is itself a replayable proof object.
- **Identification tiering** (each tier exact, each refusal honest):
  - Tier A: backdoor criterion → adjustment formula;
  - Tier B: frontdoor criterion → frontdoor formula;
  - Tier C: the full Shpitser–Pearl ID algorithm (hedge detection) — this
    is the stretch tier; Phase 1 ships A+B with ID-algorithm refusal
    semantics ("not identified by backdoor/frontdoor; ID-algorithm tier
    pending"), Phase 2 ships C.
  - Non-identifiable ⇒ **refusal with a VDR hint** ("confounded X↔Y;
    seek an instrument / evidence closing backdoor set {Z}") — the causal
    analogue of the barrier holding a debt-bearing commit. The engine
    *refusing* unidentifiable causal claims is the do-operator's version of
    zero-handwaving.
- **Estimation**: identified estimands evaluate by exact enumeration over
  the trit-class ensemble (finite sums of reductions of mutilated twins),
  every term a deterministic engine run.

### 1.3 Rung 3 — abduction · action · prediction

```python
causal.counterfactual(engine, evidence, do={"X": -1}, query="Y")
  # 1 abduction : posterior over exogenous trit-classes consistent with
  #               the ledger's evidence (exact enumeration, amplitude-
  #               weighted)  — the ledger IS the evidence record
  # 2 action    : graph surgery on the twin (field.do)
  # 3 prediction: reduce; aggregate over the posterior
causal.pn(...), causal.ps(...), causal.pns(...)   # probabilities of causation
```

PN/PS/PNS computed exactly on the enumerable classes, with Tian–Pearl
bounds reported whenever point identification fails (bounds, not guesses).

### 1.4 Metric and gate integration

- `cf_agreement` upgrades from "flip survival" to **twin-network CF
  validity** over identified interventions (the current metric remains as
  the fast structural probe; both reported).
- `causal_lift` upgrades to **do-lift**: the identified-estimand contrast
  E[Y | do(X)] − E[Y], replacing the vacuum-twin proxy where variables are
  declared (proxy remains for undeclared scopes; which one produced the
  number is recorded).
- **Gate check #8 — identification coverage**: every causal edge asserted
  in a release is identified (tier recorded) or explicitly flagged
  non-causal/associational. The stamp binds the SCM hash and every
  do-calculus derivation, so a third party replays not just *what* was
  concluded but *why it was identifiable*.

### 1.5 Bridge surfaces (inherited for free)

`gist_verdict` gains optional `causal={"treatment": ..., "outcome": ...}`;
MCP gains `gist_do`, `gist_counterfactual`, `gist_identify`; the reason
loop's steering block reports identification status of causal claims in
the chain. One mechanism, same ternary bridge: *identified-yes /
identified-no / not-identified-so-maybe-with-asks*.

---

## 2 · The refinement test protocol (what you sign off to run)

Everything below is deterministic and self-contained except T4, which is
the LLM A/B you said you want to run and post.

**T1 — Random-SCM ground truth (the core rigor test).** Generate 200 random
SCMs (3–8 variables; mixed chains/forks/colliders; 30% with latent
confounders), compile each into a lattice field, compute ground truth by
brute-force enumeration *outside* the engine, then require:

- rung-2: 100% exact agreement on identifiable P(Y|do(X)) queries;
- refusals: 100% correct non-identifiability verdicts (no silent numbers);
- rung-3: exact PN/PS on point-identifiable cases; valid Tian–Pearl bounds
  (truth inside bounds) on the rest.

**T2 — Canonical Pearl fixtures.** Smoking→tar→cancer (frontdoor, exact
adjustment result), Simpson's-paradox dataset (backdoor reversal —
aggregate association flips under adjustment), bow-graph (must refuse),
napkin graph (A+B tiers refuse; Phase-2 ID tier identifies).

**T3 — Rule-soundness property tests.** For random graphs and random legal
rule applications, the rewritten query's enumerated value equals the
original's (a do-calculus rule application may never change the answer).

**T4 — Harness A/B (the posting-grade eval).** Same model, with vs without
the `gist_verdict`+`gist_do` tools, on rung-2/3 causal-inference items
(CLadder-style ladder-of-causation benchmark items and/or your own set):
report accuracy delta, correct-refusal rate, and hallucinated-causation
rate (model asserts causal direction the tool refused). Protocol, prompts,
and scoring script ship in `eval/` so the posted results are reproducible.

**Acceptance criteria (numeric, all-or-nothing per row):**

| Criterion | Bar |
|---|---|
| T1 identifiable rung-2 agreement | 100% (exact) |
| T1 refusal correctness | 100% |
| T1 rung-3 point cases | 100% exact; bounds always contain truth |
| T2 fixtures | all pass |
| T3 property tests | 0 counterexamples in 10k trials |
| Existing suite + contract | stays green, no threshold loosening |
| New contract witnesses | `gist-do-surgery`, `gist-d-separation`, `gist-rules-sound`, `gist-backdoor`, `gist-frontdoor`, `gist-refusal-honest`, `gist-abduction-exact`, `gist-pn-ps` all live |

---

## 3 · Effort, phasing, and files

- **Phase 1** (one focused build session, like this one): `causal.py`
  (~700 lines: DAG, d-sep, rules, backdoor/frontdoor, do(), abduction
  enumeration, PN/PS), `field.do()`, metric/gate integration, T1–T3 suites,
  contract witnesses, DERIVATION.md §7. Ships usable and posting-testable.
- **Phase 2**: full Shpitser–Pearl ID algorithm (hedges), napkin-class
  identification, Tian–Pearl bound tightening, `eval/` harness for T4.
- **Non-goals (explicit):** causal *discovery* from raw data (the engine
  reasons over declared/compiled structure; discovery is a host/port
  concern), continuous-treatment estimands (ternary treatments first —
  the carrier's natural grain), and any probabilistic claim the finite
  enumeration cannot ground exactly.

**Sign-off checklist** — approve/adjust any of: (a) the design §1, (b) the
protocol §2 and its bars, (c) Phase-1/Phase-2 split, (d) the T4 benchmark
choice. On your go, Phase 1 executes in full.
