# DERIVATION — GIST out of the BiDi Coherence-Delta Calculus

**GIST (Gated Insight Synthesis Topology)** is not software that *uses* the
BiDi Coherence-Delta Calculus (CDC). It is the calculus **instantiated** at
its own bootstrap surface: the arity n = 6, where the dyadic and triadic
closures first meet (2⁶ = 4³ = 64). Every mechanism in the engine is a named
CDC construct wearing its GIST role. This document is the complete
correspondence — the derivation, the formulas, the design decisions, and the
honest seams.

The source calculus is the `bidi-coherence-delta-calculus` repository
(v0.2.4): `BIDI_CALCULUS_CORE.md` (terms, reduction, operator algebra, five
metatheorems), `bridge64.cdc` (the 64-row codebook), `native_reducer.cdc` /
`native_surface.cdc` / `council_bridge.cdc` (executable witnesses), and
`TERNARY_TRACE_WINDOW_SEMANTICS.md` (the derived observer layer).

---

## 0 · The one operation

The whole engine is a single operation applied fractally at three scales:

```
superpose (⊞)  →  flow (⟶_d)  →  commit (⟶_β, guarded)
```

- **Within a slot:** evidence atoms superpose into the read cone, the
  corefold pyramid flows the triad down to a singular, the commit quantizes
  the result to balanced trits behind the barrier.
- **Across the lattice:** slots pair (Hamming-1), their syntheses superpose
  into a parent, flow settles it, the commit gates it — six rounds from 64
  to 1 (the ladder).
- **At the top:** the two final perspectives (imagination and internal
  aggregate) superpose through mutual channels, flow to reconciliation, and
  the committing measurement latches the decision.

That is the "simplex" property: no scale introduces a new mechanism.

---

## 1 · The correspondence table

| GIST mechanism | CDC ground | Where |
|---|---|---|
| Coherence value of any claim-state | carrier algebra 𝒞 = (C, ⊞, ⊥, ⟳, \|·\|, κ), standard model C = ℝ² ≅ ℂ | `algebra.py` |
| "Supports / contradicts / open" | derived balanced trit τ(x) with deadband δ = ½; 0 is a live crossing, not false | `algebra.trit` |
| "This scope can still absorb evidence" | boundary openness ϰ(x) = max(0, 1 − \|κ\|/δ), maximal at the crossing | `algebra.openness` |
| 64-slot lattice, address (q1,q2,q3) | `bridge64` codebook: dyadic 6-bit ↔ triadic 3-digit, bijective | `bridge.py` |
| A slot | **module**, n = 6 cells: read cone (0,1,2) = the working **triad**, write cone (3,4,5) = dyad-L, **singular**, dyad-R | `engine._build_field` |
| Evidence atom | a coherence value ⟨a, θ⟩: amplitude = salience, phase = arccos(polarity) in the slot's thesis frame | `ports.polarity_to_theta` |
| TriadicGate "add/subtract until coherent" | ⊞ superposition — contradicting phases cancel destructively, agreeing phases reinforce; clustering angle π/3 equals the deadband cone (cos π/3 = δ), so a cluster *is* a commitment class | `engine._absorb` |
| The 3→2→1 loop | corefold ∂ pyramid realized as channel structure: read → dyad → singular, weights ½; ∂ is ⊞-linear, ⟳-equivariant, strictly abstracting (laws tested) | `algebra.corefold_*`, pyramid channels |
| Continuous synthesis | flow ⟶_d: phase turns toward the afferent superposition, amplitude relaxes, belief descends the exact gradient of Φ's belief terms | `field.flow` |
| Gate / veto / accept | commit ⟶_β: quantize → snap → **barrier** → jitter → belief → **energy guard** → latch; total (accepts or holds, never partial) | `field.commit` |
| VDR (veto-diff-repair) | held commits carry the CDC native statuses and reasons: `balance-violation` (with the exact violating cell — the barrier knows), `energy-increase`, `deadband-jitter`; hints are ledger events, never forced | `field.commit`, `engine._commit_slot` |
| Retrieval saturation | plateau + openness split: a plateaued slot whose read cone sits at crossings (ϰ high) is *maximally open to relation* — that state **is** the retrieval intent; a plateaued closed boundary is saturated | `engine._measure_slot` |
| Ladder 64→32→…→1 | nest / bidiγΔ iterated over the six address bits; pairing = XOR bit k; fusion = ⊞ of write cones with ⊙ gate-alignment (the angled reference-frame transfer), then ∂ | `ladder.py` |
| Merkle verification | **the ladder tree is the Merkle tree**: leaf = slot commit hash, node = H(left ∥ right); verifying the root verifies the reduction — proof structure = reasoning structure | `ladder.py`, `crypto.py` |
| Release eligibility tiers | metatheorem T5 normal forms: admissible (267/729) ⊂ localized (51, Motzkin) ⊃ catalan (5); the census 729/267/51/20/5 is re-verified live | `walks.py` |
| Meta ↔ All reconciliation | **council** of two members (per `council_bridge.cdc`): concatenated write-cone trit words → occupancy → bridge coordinate; quorum = committed-trit count; adoption also needs the coherence-delta γΔ of the two singulars within τ | `engine._reconcile` |
| Meta_Imagination | the **action** half of the dual minimizer: root synthesis with phase pulled toward the prior, pull scaled by \|prior\| (uninformed prior = no pressure — E0) | `engine._reconcile` |
| Aggregate_Internal | ⊞ over all 64 leaf write cones per cone position, then ∂ | `engine._reconcile` |
| Ledger | the derived **trace/window** layer: append-only, hash-chained, passive projections (`TraceWindow`), local counters, no global tick (T6) | `ledger.py` |
| "No orchestrator, reactors react" | T3 local confluence: channel-disjoint commits commute, so independent reactors on disjoint slots are order-safe | tested in `test_field_reduction` |
| Decision stamp | HKDF(prompt, session) → PRF challenge → HMAC over (leaf root ∥ round roots ∥ decision coordinate ∥ ledger head) | `crypto.py` |
| Session lifecycle | E0 existence viability: intentional → reactive → agentic → passive persistence, each defined by transition capacity | `engine.viability` |

---

## 2 · The metric formulas (all deterministic, no estimation)

| Metric | Formula | Meaning |
|---|---|---|
| coherence | phase-order magnitude R = \|Σ aᵢe^{iθᵢ}\| / Σ aᵢ over the write cone | internal consistency of the synthesis |
| coverage c | 1 − exp(−A/λ), A = cumulative absorbed afferent amplitude, λ = 3 | evidence mass (amplitude *is* the calculus's evidence-mass carrier) |
| stability u | survival fraction of the committed word under 8 fixed sign-patterned phase jitters (±0.15 rad) | robustness under ablation, executed |
| cf agreement a | survival fraction of the **singular** trit under do(read-cell ← pole flip) on the exact-corefold twin (the twin network) | Pearl-style counterfactual robustness on the engine's own causal fabric. Structural ceiling: (n−1)/n = 2/3 for single-cluster conclusions — flipping the dominant evidence *must* flip an honest synthesis; scores below ⅓ mark contested/knife-edge conclusions |
| causal lift ℓ | clamp₀₁[(Φ_vacuum − Φ_actual)/(1 + \|Φ_vacuum\|)], vacuum twin = afferents removed | how much the evidence genuinely lowers variational free energy vs prior-only existence |
| global S | phase-order magnitude over all 64 singular cells (amplitude-weighted) | field-level agreement, gated with hysteresis |

The potential (identical to the calculus):

```
Φ_m = Σᵢ [ ½·π·(Re Âᵢ − b)²  +  ½·(b − b⁰)²  −  |Âᵢ|·cos(arg Âᵢ − θᵢ) ]
```

---

## 3 · The seven gate checks (all executable)

1. **coverage** — every axis value {0..3} × 3 axes carried by ≥ 1
   contributing slot (committed non-void word, c ≥ c_min);
2. **parity** — contributing slots non-degenerate over Σq mod 2 and mod 3;
3. **stability** — all u ≥ τ_u;
4. **cf agreement** — all a ≥ τ_a and mean ≥ τ̄_a;
5. **causal lift** — median ℓ ≥ τ_ℓ;
6. **global agreement** — S ≥ τ_S sustained `hysteresis` consecutive checks;
7. **saturation** — all contributing slots saturated, or budget exhausted
   (which passes but flags `budget_release` on the proposal — honest
   downgrade, never silent).

Plus the structural spine: the barrier makes every latched word admissible
by construction (T1), and the release reports each word's T5 tier with the
weakest as headline.

---

## 4 · Design decisions and honest seams

**Where prose and executable witnesses diverged, the executable witness
won.** The CDC core document describes the commit barrier as rotating
violating cells to their crossing; the native runtime *holds* with
`balance-violation`. This engine defaults to hold (matching
`native_reducer.cdc` exactly) and offers `barrier="repair"` (the prose
semantics) — GIST drives repair through visible VDR ledger events, so both
sources are honored and nothing is silent. Likewise, the CDC prose gates
afferents by openness; the native flow witness number (0.25) is ungated;
this engine follows the witness.

**The commit snap applies to the read cone only.** Afferents are frozen at
commit time and read cells carry no incident afferent, so hardening the
evidence triad is exactly Φ-neutral: the energy guard then judges only the
belief step. Combined with the belief step targeting the Φ-minimizing blend
b\* = (π·m̄ + b⁰)/(π+1) — the discrete counterpart of the belief flow's
exact gradient descent — commits become **event-driven**: they accept when
evidence is fresh and hold (`deadband-jitter`) at plateau, which is
precisely the plateau signal saturation consumes. T2 soundness holds by
construction rather than by luck.

**Counterfactuals are structural and exact.** The twin network is a literal
module copy; do() latches a flipped cell; the corefold pyramid is recomputed
algebraically (its exact fixpoint) rather than by relaxation, because an
antipodal intervention exerts zero Kuramoto torque under flow and would
spuriously read as survival. A *semantic* counterfactual validator (an LLM
judging counterfactual claims) can be layered through the ports; the
structural one is the mechanism's own and is exact.

**What the stamp does and does not claim.** HKDF/HMAC/SHA-256 give
integrity (any payload mutation changes the head, roots, and stamp),
binding (the stamp cannot be transplanted to another prompt/session), and
replay verifiability (`verify_ledger` recomputes everything from the ledger
alone — it re-runs the engine on the recorded inputs and compares every
derived event). It is not a zero-knowledge proof and does not attest that
evidence is *true* — it attests the released synthesis is exactly what this
ledger derives.

**Semantics → geometry is a port, deliberately.** The mechanism computes
over phase geometry. What maps meaning onto geometry (address, polarity,
salience) is the `Projector` seam: callers may pass explicit fields, supply
embedding vectors (`VectorProjector`), or let the deterministic
`HashProjector` fill gaps so the mechanism runs standalone. This is the
honest boundary between the mechanism (executable, verifiable, model-free)
and meaning (host-supplied).

**Ladder bit order is semantic.** Addresses are bridge64 dyadic words, so
consuming bits LSB-first reconciles the fine bit of axis 3 upward to the
coarse bit of axis 1: evidence-type first, then abstraction, then temporal
(under default labels). If a round's pairing holds anywhere, alternate bits
are tried deterministically (VDR `swap_pairing`); if all hold, the round
runs in repair mode, visibly.

**The triad fills dialectically.** First cluster → one end, second
(typically opposing) cluster → the far end, third → the middle — because ∂
double-weights the middle cell: the mediating position carries the bridge.
A slot holding thesis + antithesis + open middle that plateaus with the
middle at its crossing saturates at openness exactly ⅓ and commits a
localized word: *thesis, antithesis, question held open* is a normal form.

---

## 5 · Parity with the CDC repository (executed, not claimed)

| CDC witness | Expected | This engine |
|---|---|---|
| `flow reducer-flow` | council.b θ = 0.25 ± 1e-6 | reproduced (`test_field_reduction`, contract `native_flow_parity`) |
| `commit reducer-commit` | trits `0+-`, accepted, reason none | reproduced |
| `commit reducer-hold` | trits `-+0`, held, balance-violation | reproduced, with cell attribution |
| `nest reducer-nest` | parent belief = child prior = 0.666667 | reproduced |
| `proof trit-walk-n6` | 729 / 267 / 51 / 20 / 5 | reproduced (`census(6)`) |
| `bridge64.cdc` | all 64 rows | byte-parity when the repo copy is present; the generation rule is verified bijective always |
| `trace surface-trace` + `bridge surface-bridge` | `+0-+0-` → dyadic `101101` → triadic `231` | reproduced |
| `council bridge-council` | member trits → occupancy → coordinate, quorum = committed count | the reconciliation implements exactly this shape |

---

## 6 · What was *not* carried over, and why

- **LLM-agent pool choreography** (the "30–45 concurrent agents" of the
  original skill) is a *deployment pattern*, not mechanism. The engine is
  the ledger-reactive substrate those reactors coordinate through; T3
  confluence makes disjoint-slot reactors order-safe. Any host (Claude
  skill, agent framework, queue workers, humans) plays the reactor roles
  through `ingest` / `fulfill` / ledger reads.
- **Web search execution** is IO; the engine emits `retrieval_intent` and
  consumes fulfillments. The demo fulfills from a static corpus to stay
  deterministic.
- **Model escalation** is a host decision; the engine emits
  `escalation_intent` when fulfillments keep arriving without closing a
  slot's aperture.
