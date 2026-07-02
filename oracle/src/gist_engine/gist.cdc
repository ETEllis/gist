# gist.cdc -- native contract for GIST (Gated Insight Synthesis Topology).
#
# GIST is an instantiation of the BiDi Coherence-Delta Calculus at the
# bootstrap arity n=6 (the bridge64 surface, 2^6 = 4^3 = 64). This file
# declares that instantiation in the calculus's own source language. It is a
# loader/checker surface in the spirit of cdc_boot.py: every witness below
# names a live executable check in gist_engine.contract, and
# `gist contract` (or tests/test_contract.py) runs them all.

kernel gist stage=1 target=cdc-instantiation arity=6 lattice=64
  term atom slot triad dyad singular lattice ladder gate intent stamp release
  rule superpose flow commit nest saturate watch reduce reconcile release replay
  provides sixty-four-lattice dyadic-triadic-address corefold-pyramid
  provides balanced-ternary-commit trit-walk-barrier normal-form-tiers
  provides openness-saturation retrieval-intents vdr-attribution
  provides hamming-ladder merkle-reduction-tree council-reconciliation
  provides hkdf-decision-stamp ledger-replay-verification
  provides projector-ports host-embedding frontend-state-projection
  bootloader read-source parse-directives run-live-checks report
end

# -- invariants inherited from the calculus (laws.cdc keys) ------------------

invariant balanced-ternary-carrier statement="committed outcomes are -1/0/+1 around equilibrium"
invariant dyadic-triadic-closure statement="2^6 equals 4^3 equals 64 bridge states"
invariant preservation statement="commits preserve admissible nonnegative trit walks"
invariant soundness statement="accepted commits do not increase local potential"
invariant local-confluence statement="disjoint commits commute"
invariant flow-additivity statement="flow composes over duration"
invariant normalforms statement="localized committed modules are stable values"
invariant trace-order-locality statement="trace time is local to bounded observer windows"
invariant existence-viability statement="frames persist by bounded coherent continuity plus transition capacity"
invariant gate-abelian statement="gate composition is an abelian phase group"
invariant interfere-monoid statement="interference is a commutative monoid"
invariant rotation-linear statement="rotation distributes over interference"
invariant corefold-morphism statement="core-fold is linear and rotation-equivariant"

# -- GIST-specific invariants -------------------------------------------------

invariant ladder-merkle-equality statement="the ladder reduction tree and the merkle verification tree are the same tree"
invariant replay-determinism statement="a session is a pure fold over its ledger inputs"
invariant stamp-binding statement="the decision stamp binds prompt, session, reduction roots, and ledger head"
invariant openness-retrieval statement="plateaued open boundaries emit retrieval intents; closed ones saturate"
invariant ternary-verdict-bridge statement="yes/no/maybe is the balanced-ternary carrier: decisive latch, mirrored latch, open crossing"
invariant mirror-symmetry statement="no on C is a gate-guarded yes on the mirrored session NOT(C)"
invariant functional-form-equivalence statement="the analytically-built neural form computes the same reduction as the reference engine"

# -- capabilities -------------------------------------------------------------

capability G-LATTICE statement="64-slot lattice addressed through the bridge64 codebook"
capability G-PIPELINE statement="superpose, flow, commit, measure, saturate, gate, reduce, reconcile, stamp, release"
capability G-PORTS statement="projector and retrieval ports allow host embedding without engine modification"
capability G-VERIFY statement="third parties replay-verify sessions from the ledger alone"
capability G-BRIDGE-TOOL statement="architecture-agnostic ternary verdict via tool call, MCP, and reasoning-loop stitch"
capability G-NEURAL statement="weight-exportable functional form for in-architecture implementation"

# -- witnesses: each names a live executable check ---------------------------

witness gist-algebra-gate-abelian invariant=gate-abelian check=algebra_gate_abelian claim="gate phase composition forms an abelian group on the torus"
witness gist-algebra-interfere-monoid invariant=interfere-monoid check=algebra_interfere_monoid claim="superposition is a commutative monoid with void unit"
witness gist-algebra-rotation-linear invariant=rotation-linear check=algebra_rotation_linear claim="rotation distributes over superposition"
witness gist-algebra-corefold-morphism invariant=corefold-morphism check=algebra_corefold_morphism claim="the corefold pyramid is linear and rotation-equivariant"
witness gist-census-n6 invariant=normalforms check=census_n6 claim="the n=6 walk spectrum is exactly 729/267/51/20/5"
witness gist-bridge-bijection invariant=dyadic-triadic-closure check=bridge_bijection claim="the generated 64-row codebook is bijective both ways"
witness gist-bridge-trit-projection invariant=dyadic-triadic-closure check=bridge_trit_projection claim="trits +0-+0- project to dyadic 101101 and triadic 231"
witness gist-flow-parity invariant=flow-additivity check=native_flow_parity claim="the native reducer flow witness number 0.25 is reproduced"
witness gist-commit-parity invariant=preservation check=native_commit_parity claim="the native reducer accepted commit 0+- is reproduced"
witness gist-hold-parity invariant=preservation check=native_hold_parity claim="the native reducer held commit -+0 balance-violation is reproduced"
witness gist-nest-parity invariant=existence-viability check=native_nest_parity claim="the native reducer nest exchange 2/3 is reproduced"
witness gist-commit-soundness invariant=soundness check=commit_soundness claim="accepted commits never increase the module potential"
witness gist-barrier-preservation invariant=preservation check=barrier_preservation claim="commits latch only admissible words and hold violations with attribution"
witness gist-ternary-carrier invariant=balanced-ternary-carrier check=ternary_carrier claim="every committed outcome is a balanced trit"
witness gist-local-confluence invariant=local-confluence check=local_confluence claim="channel-disjoint commits commute"
witness gist-flow-additivity invariant=flow-additivity check=flow_additivity claim="split and combined flow durations agree on the grid"
witness gist-trace-passive invariant=trace-order-locality check=trace_passive claim="passive observation leaves field state unchanged"
witness gist-ledger-chain capability=G-VERIFY check=ledger_chain claim="the ledger hash chain detects any payload mutation"
witness gist-ladder-merkle invariant=ladder-merkle-equality check=ladder_merkle claim="every ladder node hash is the merkle node of its children"
witness gist-replay-determinism invariant=replay-determinism check=replay_determinism claim="two identical-input sessions produce identical ledgers and stamps"
witness gist-release-normal-form invariant=normalforms check=release_normal_form claim="the demo session releases with all contributing words admissible"
witness gist-council-coordinate invariant=dyadic-triadic-closure check=council_coordinate claim="the reconciliation decision projects through bridge64 occupancy"
witness gist-openness-intent invariant=openness-retrieval check=openness_intent claim="open plateaus emit intents and closed plateaus saturate"
witness gist-stamp-binding invariant=stamp-binding check=stamp_binding claim="stamps are recomputable and differ across prompts"
witness gist-lattice-shape capability=G-LATTICE check=lattice_shape claim="the engine builds 64 six-cell slots with corefold pyramid channels"
witness gist-ports-standalone capability=G-PORTS check=ports_standalone claim="the hash projector runs the mechanism standalone and deterministically"
witness gist-pipeline-e2e capability=G-PIPELINE check=pipeline_e2e claim="the full pipeline reaches a verified stamped release"
witness gist-frontend-projection capability=G-VERIFY check=frontend_projection claim="state and replay projections carry the full board for a UI"
witness gist-verdict-ternary invariant=ternary-verdict-bridge check=verdict_ternary claim="the bridge answers yes on decisive support, maybe at the crossing and under contest"
witness gist-verdict-mirror-no invariant=mirror-symmetry check=verdict_mirror_no claim="decisive contradiction returns no through the gated mirror session"
witness gist-mcp-surface capability=G-BRIDGE-TOOL check=mcp_surface claim="the MCP server exposes the verdict and session tools over JSON-RPC"
witness gist-reasonloop-gate capability=G-BRIDGE-TOOL check=reasonloop_gate claim="the reasoning loop feeds steps, emits steering blocks, and gates conclusions"
witness gist-gate-scope-occupied capability=G-BRIDGE-TOOL check=gate_scope_occupied claim="occupied-scope sessions reach honest scoped releases"
witness gist-neural-flow-equivalence invariant=functional-form-equivalence check=neural_flow_equivalence claim="the neural form reproduces the engine's flow trajectories on the full lattice"
witness gist-neural-commit-equivalence invariant=functional-form-equivalence check=neural_commit_equivalence claim="the neural quantization head reproduces trits, barrier, and attribution"
witness gist-neural-weight-roundtrip capability=G-NEURAL check=neural_weight_roundtrip claim="exported weights reload and reproduce identical trajectories"

# -- expectations -------------------------------------------------------------

expect native substrate == cdc-instantiation
expect terms >= 12
expect rules >= 10
expect invariants >= 20
expect capabilities >= 6
expect witnesses >= 36

expect witness gist-census-n6
expect witness gist-bridge-bijection
expect witness gist-flow-parity
expect witness gist-commit-parity
expect witness gist-hold-parity
expect witness gist-nest-parity
expect witness gist-commit-soundness
expect witness gist-barrier-preservation
expect witness gist-ladder-merkle
expect witness gist-replay-determinism
expect witness gist-pipeline-e2e
expect witness gist-verdict-ternary
expect witness gist-verdict-mirror-no
expect witness gist-neural-flow-equivalence
expect witness gist-neural-commit-equivalence
