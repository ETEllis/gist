# gist_laws.cdc -- GIST invariant + capability registry in native .cdc.
#
# GIST (Gated Insight Synthesis Topology) is instantiated entirely out of the
# BiDi Coherence-Delta Calculus at the bootstrap arity n=6 (the 2^6 = 4^3 = 64
# bridge surface). This file is GIST's own laws.cdc + system.cdc: it declares
# the invariants GIST adds on top of the calculus, the capability surface it
# exposes to a host, and the native witnesses that discharge each claim.
#
# GIST invariants are *derived*: each grounds in a CDC metatheorem. The
# scenario files (gist_pyramid, gist_gate, gist_cf, gist_ladder) carry the
# executable witnesses a host runs through the existing BiDi C native runtime.

# ---------------------------------------------------------------------------
# GIST invariants (each grounded in a CDC metatheorem, witnessed below)
# ---------------------------------------------------------------------------

invariant gate-emergence statement="release is proposed only when coverage, parity, stability, counterfactual survival, causal lift, global agreement, and retrieval saturation all hold"
invariant ladder-reduction statement="the 64->32->16->8->4->2->1 Hamming-1 meta-gate ladder keeps every fused round admissible"
invariant retrieval-saturation statement="a plateau with an open boundary emits a retrieval intent; a plateau with a closed boundary saturates"
invariant coverage-parity statement="release requires all four values on each of the three axes plus non-degenerate parity over the address sums"
invariant decision-stamp statement="the released decision is a bridge coordinate bound to the whole reduction through self-evolution"
invariant counterfactual-survival statement="do(cell) is a latched cell with severed inbound channels; a conclusion is causal only if its singular trit survives the twin-field intervention"
invariant native-plasticity statement="plastic channel weights follow phase correlation through the flow reduction; structure and state co-adapt natively"

# ---------------------------------------------------------------------------
# GIST capability surface (declared here, witnessed by runtime jobs elsewhere)
# ---------------------------------------------------------------------------

capability G-synthesis tier=core note="3->2->1 coherence-delta synthesis pyramid over an evidence triad"
capability G-gate tier=core note="emergent 64-gate release watcher over trace/measure/policy"
capability G-ladder tier=core note="council-reconciled meta-gate ladder into one bridge coordinate"
capability G-retrieval tier=core note="openness-driven retrieval-saturation counter loop"
capability G-decision tier=core note="bridge-coordinate decision stamp via source self-evolution"
capability G-compile tier=support note="reducer-IR compilation of the synthesis jobs"
capability G-interpret tier=support note="IR interpretation of the compiled synthesis jobs"
capability G-coverage tier=core note="finite balanced-ternary normal-form spectrum grounding the release tiers"
capability G-counterfactual tier=core note="twin-field do-intervention plus commit-barrier veto as the native Pearl overlay"
capability G-existence tier=core note="nested cross-scale viability exchange (parent context down, child coherence up)"
capability G-neural tier=core note="the field as neural network: channels are SO(2) weights, flow jobs are forward layers, commit is the ternary bottleneck, nest is pooling"

# ---------------------------------------------------------------------------
# Law witnesses: one native witness per GIST invariant
# ---------------------------------------------------------------------------

witness gist-law-gate invariant=gate-emergence claim="all seven coherence checks must hold before a gate proposal is written"
witness gist-law-ladder invariant=ladder-reduction claim="each ladder round re-commits its fused nodes under the same nonnegative-balance barrier"
witness gist-law-retrieval invariant=retrieval-saturation claim="crossing read cells at plateau are maximal-openness apertures that request evidence"
witness gist-law-coverage invariant=coverage-parity claim="the three triadic axes must each present all four values with balanced parity"
witness gist-law-decision invariant=decision-stamp claim="the decision bridge coordinate is appended into an evolved source copy as its stamp"
witness gist-law-counterfactual invariant=counterfactual-survival claim="the twin field latches the intervened cell and drops its inbound channel, then compares singular trits"

# ---------------------------------------------------------------------------
# Capability registry witnesses (claim-level; runtime witnesses live in the
# scenario files and reference the same capability keys)
# ---------------------------------------------------------------------------

witness gist-cap-synthesis capability=G-synthesis claim="synthesis pyramid folds three evidence cells to one gist through flow and commit"
witness gist-cap-gate capability=G-gate claim="gate watcher reads committed trits through a bounded trace window"
witness gist-cap-ladder capability=G-ladder claim="council deliberation reduces member trits to one adopted bridge coordinate"
witness gist-cap-retrieval capability=G-retrieval claim="saturation counter tracks retrieval patience without a global tick"
witness gist-cap-decision capability=G-decision claim="decision coordinate is stamped by bridge-coordinate self-evolution"
witness gist-cap-compile capability=G-compile claim="synthesis jobs compile to a reducer IR listing"
witness gist-cap-interpret capability=G-interpret claim="the compiled reducer IR is executed by the IR interpreter path"
witness gist-cap-coverage capability=G-coverage claim="the finite n=6 walk spectrum 729/267/51/20/5 grounds the release tiers"
witness gist-cap-counterfactual capability=G-counterfactual claim="a balance-violating commit is held as the native counterfactual veto"
witness gist-cap-existence capability=G-existence claim="nested modules exchange parent context and child coherence"

expect law gate-emergence
expect law ladder-reduction
expect law retrieval-saturation
expect law coverage-parity
expect law decision-stamp
expect law counterfactual-survival
expect law native-plasticity

expect capability G-synthesis
expect capability G-gate
expect capability G-ladder
expect capability G-retrieval
expect capability G-decision
expect capability G-compile
expect capability G-interpret
expect capability G-coverage
expect capability G-counterfactual
expect capability G-existence
expect capability G-neural
