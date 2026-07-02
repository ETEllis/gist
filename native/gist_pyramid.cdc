# gist_pyramid.cdc -- the GIST 3->2->1 synthesis pyramid as native reducer jobs.
#
# This is the executable heart of one GIST slot: the TriadicGate -> DyadCompressor
# -> SingularSynth pyramid plus the veto (VDR) case, all as flow/commit/nest jobs
# the BiDi C native runtime executes and checks.
#
#   run       ./cdc_native_runtime run       gist_pyramid.cdc
#   compile   ./cdc_native_runtime compile   gist_pyramid.cdc
#   interpret ./cdc_native_runtime interpret gist_pyramid.cdc
#   prove     ./cdc_native_runtime prove     gist_pyramid.cdc
#
# Semantics (deadband 0.5, gain 1.0):
#   * flow gist-fold couples the first evidence cell into the second across a
#     weight-0.25 channel: theta(triad.r1) = 0 + 0.25*sin(pi/2 - 0) = 0.25.
#   * commit gist-synth quantizes the evidence triad to the balanced-ternary
#     word 0+- (r0 crossing, r1 asserted +, r2 opposed -): admissible walk
#     0,+1,0 -> accepted. This is the singular gist of the slot.
#   * nest gist-nest carries child gist coherence up into the triad belief
#     (mean child trit = (+1+1+0)/3 = 2/3) and the belief back down as prior.
#   * commit gist-veto shows the counterfactual/VDR case: the word -+0 forces
#     the prefix walk negative at the first cell -> held, balance-violation.
#     Nothing latches; the slot emits a repair signal instead of a false gist.

field gist-synthesis dt=0.125 gain=1.0 deadband=0.5

# the evidence triad (TriadicGate input); r0 undecided, r1 supports, r2 opposes
module triad field=gist-synthesis belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell triad.r0 module=triad theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell triad.r1 module=triad theta=0.0 amplitude=1.0 omega=0.0
cell triad.r2 module=triad theta=3.141592653589793 amplitude=1.0 omega=0.0

# the distilled singular gist (SingularSynth output), child of the triad scope
module gist field=gist-synthesis belief=0.0 prior=0.0 precision=1.0 action-gain=1.0 parent=triad
cell gist.d module=gist theta=0.0 amplitude=1.0 omega=0.0
cell gist.s module=gist theta=0.0 amplitude=1.0 omega=0.0
cell gist.e module=gist theta=1.5707963267948966 amplitude=1.0 omega=0.0

# the contested case: contradictory evidence that cannot admissibly commit
module contested field=gist-synthesis belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell contested.r0 module=contested theta=3.141592653589793 amplitude=1.0 omega=0.0
cell contested.r1 module=contested theta=0.0 amplitude=1.0 omega=0.0
cell contested.r2 module=contested theta=1.5707963267948966 amplitude=1.0 omega=0.0

# the fold channel of the pyramid (r0 -> r1 coherence-delta transfer)
channel triad.r0 -> triad.r1 weight=0.25 delay=0.0 angle=0.0 lines=1

flow gist-fold field=gist-synthesis duration=1.0 expect-theta=triad.r1:0.25 tolerance=0.000001
commit gist-synth module=triad expect-trits=0+- expect-balance=admissible expect-status=accepted expect-reason=none
nest gist-nest parent=triad child=gist expect-parent-belief=0.666667 expect-child-prior=0.666667 tolerance=0.000001
commit gist-veto module=contested expect-trits=-+0 expect-balance=violated expect-status=held expect-reason=balance-violation
compile gist-ir source=gist_pyramid.cdc expect-ops=4 expect-flow=1 expect-commit=2 expect-nest=1
interpret gist-ir-exec source=gist_pyramid.cdc expect-ops=4 expect-flow=1 expect-commit=2 expect-nest=1
proof gist-spectrum carrier=balanced-ternary arity=6 expect-total=729 expect-admissible=267 expect-localized=51 expect-saturated=20 expect-catalan=5

witness gist-fold-native invariant=flow-additivity capability=G-synthesis reducer=gist-fold claim="C native runtime folds the first evidence cell into the second across the pyramid channel"
witness gist-synth-native invariant=preservation capability=G-synthesis reducer=gist-synth claim="C native runtime commits the evidence triad to the admissible singular gist 0+-"
witness gist-nest-native invariant=existence-viability capability=G-existence reducer=gist-nest claim="C native runtime exchanges child gist coherence up and belief down through nest"
witness gist-veto-native invariant=soundness capability=G-counterfactual reducer=gist-veto claim="C native runtime holds the contested word -+0 as a balance-violation veto"
witness gist-compile-native capability=G-compile compile=gist-ir claim="C native runtime compiles the synthesis jobs into reducer IR with four ops"
witness gist-interpret-native capability=G-interpret interpret=gist-ir-exec claim="C native runtime interprets the compiled synthesis reducer IR"
witness gist-proof-native invariant=normalforms capability=G-coverage proof=gist-spectrum claim="C native runtime checks the finite n=6 normal-form spectrum grounding the release tiers"

expect reducer gist-fold-native
expect reducer gist-synth-native
expect reducer gist-nest-native
expect reducer gist-veto-native
expect compile gist-compile-native
expect interpret gist-interpret-native
expect proof gist-proof-native
