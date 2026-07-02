# gist_gate.cdc -- the emergent 64-gate as the native trace/measure surface.
#
# The gate never commands; it OBSERVES committed slot state through a bounded
# window and proposes a release coordinate. This file exercises the whole
# observer surface for one gate reading, through the BiDi C native runtime:
#
#   surface  ./cdc_native_runtime surface gist_gate.cdc
#
# The gate field holds two committed slots (alpha, beta), six cells total:
# thetas 0, pi/2, pi repeated -> trit word +0-+0-. That word is:
#   * a passive trace over the field (events = 4 committed poles);
#   * a committing measurement read from beta by alpha (outcome +0-);
#   * a policy window (local sampling, guarded commit, recursive adapt);
#   * a bridge coordinate: occupancy 101101 -> triadic 231 (the decision slot);
#   * a saturation counter: patience 2 + 3 arrivals - 1 spend = 4.
#   * a guard on the crossing cell alpha.b (trit 0): boundary OPEN -> the slot
#     is still an aperture requesting evidence (retrieval-saturation signal).

field gate-field dt=0.125 gain=1.0 deadband=0.5

module gate-alpha field=gate-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell gate-alpha.a module=gate-alpha theta=0.0 amplitude=1.0 omega=0.0
cell gate-alpha.b module=gate-alpha theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell gate-alpha.c module=gate-alpha theta=3.141592653589793 amplitude=1.0 omega=0.0

module gate-beta field=gate-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell gate-beta.a module=gate-beta theta=0.0 amplitude=1.0 omega=0.0
cell gate-beta.b module=gate-beta theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell gate-beta.c module=gate-beta theta=3.141592653589793 amplitude=1.0 omega=0.0

guard aperture-guard cell=gate-alpha.b expect-state=open
trace gate-trace field=gate-field expect-trits=+0-+0- expect-events=4
measure gate-measure observer=gate-alpha target=gate-beta mode=commit expect-outcome=+0- expect-potential=nonincrease
policy gate-policy window=gate-trace sampling=local commit=guarded adapt=recursive expect-sampling=local expect-commit=guarded expect-adapt=recursive
bridge gate-bridge trace=gate-trace via=bridge64 expect-dyadic=101101 expect-triadic=231
counter saturation-counter value=2 increment=3 decrement=1 expect-value=4

witness gist-gate-trace-native invariant=trace-order-locality capability=G-gate trace=gate-trace claim="the gate reads committed slot trits through a bounded local trace window"
witness gist-gate-guard-native capability=G-gate guard=aperture-guard claim="a crossing read cell reports an open boundary, the retrieval-saturation aperture"
witness gist-gate-measure-native invariant=soundness capability=G-gate measure=gate-measure claim="the committing gate measurement does not increase potential"
witness gist-gate-policy-native invariant=trace-order-locality capability=G-gate policy=gate-policy claim="the gate window carries local sampling, guarded commit, and recursive adapt policy"
witness gist-gate-bridge-native invariant=dyadic-triadic-closure capability=G-decision bridge=gate-bridge claim="the gate trace projects to bridge coordinate 101101 = triadic 231"
witness gist-gate-counter-native capability=G-retrieval counter=saturation-counter claim="the saturation counter tracks retrieval patience without a global tick"

expect guard gist-gate-guard-native
expect trace gist-gate-trace-native
expect measure gist-gate-measure-native
expect policy gist-gate-policy-native
expect bridge gist-gate-bridge-native
expect counter gist-gate-counter-native
