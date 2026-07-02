# gist_cf2.cdc -- the second intervention cluster: sufficiency, backdoor,
# frontdoor -- all native, no new primitive (do() = latched cell + severed
# inbound channel, twin fields; same construction as gist_cf.cdc).
#
#   run  ./cdc_native_runtime run gist_cf2.cdc
#
# Cluster 1 (gist_cf.cdc) established NECESSITY: do(r0 := -) dissolves the
# factual conclusion, so r0 is load-bearing. This file completes the Pearl
# surface with three more surgeries, each a factual/twin field pair whose
# expectations the C runtime checks:
#
# A. SUFFICIENCY-RESTORATION (cs-obs / cs-do)
#    SCM: r0 -> s <- r1, evidence contested (r0 supports +, r1 opposes -).
#    Observational: s = pi/2 + 0.5 sin(-pi/2) + 0.5 sin(pi/2) = pi/2 -> trit 0:
#    the conclusion is dissolved at the crossing (word +-0, admissible).
#    do(r1 := +): r1 is a root, so the surgery is a pure latch (nothing to
#    sever). s = pi/2 - 0.5 - 0.5 = 0.570796 -> trit +: forcing the opposing
#    evidence restores the conclusion. Removing the opposition is SUFFICIENT;
#    r1 was the blocking cause. Word +++.
#
# B. BACKDOOR SEVERANCE (bd-obs / bd-do)
#    SCM: confounder h -> x (0.7), h -> y (0.7), and x -> y (0.5).
#    Observational: h drives both; x = y = 0.870796 -> both + (word +++).
#    x and y co-move, but mostly through the back door h.
#    do(x := -): x latched at the - pole, its inbound h -> x SEVERED; the
#    direct x -> y and the h -> y stay. y = pi/2 - 0.7 + 0.5 = 1.370796 ->
#    trit 0 (word +-0). The naive association predicts y flips with x; the
#    surgery shows y only dissolves: the confounded co-movement OVERSTATES
#    the causal effect of x. Association != causation, natively.
#
# C. FRONTDOOR MEDIATION (fd-obs / fd-do)
#    SCM: x -> m -> y with the same confounder h -> x, h -> y.
#    Observational: y rides the confounder (y = 0.870796 -> +) while the
#    mediator idles at its crossing (word ++0+).
#    do(m := -): m latched -, its inbound x -> m SEVERED; m -> y and h -> y
#    stay. y = pi/2 - 0.7 + 0.5 = 1.370796 -> trit 0 (word ++-0): despite
#    full confounder support, intervening on the mediator alone dissolves
#    the conclusion -- the causal path x -> y is exactly the mediated one.

# --- A. sufficiency: contested observational world --------------------------
field cs-obs dt=0.125 gain=1.0 deadband=0.5

module csobs field=cs-obs belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell csobs.r0 module=csobs theta=0.0 amplitude=1.0 omega=0.0
cell csobs.r1 module=csobs theta=3.141592653589793 amplitude=1.0 omega=0.0
cell csobs.s  module=csobs theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel csobs.r0 -> csobs.s weight=0.5 delay=0.0 angle=0.0 lines=1
channel csobs.r1 -> csobs.s weight=0.5 delay=0.0 angle=0.0 lines=1

# --- A. sufficiency: twin under do(r1 := +) (root: pure latch) --------------
field cs-do dt=0.125 gain=1.0 deadband=0.5

module csdo field=cs-do belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell csdo.r0 module=csdo theta=0.0 amplitude=1.0 omega=0.0
cell csdo.r1 module=csdo theta=0.0 amplitude=1.0 omega=0.0
cell csdo.s  module=csdo theta=1.5707963267948966 amplitude=1.0 omega=0.0

# the restored conclusion's downstream scope (for the upward nest)
module csup field=cs-do belief=0.0 prior=0.0 precision=1.0 action-gain=1.0 parent=csdo
cell csup.a module=csup theta=0.0 amplitude=1.0 omega=0.0
cell csup.b module=csup theta=0.0 amplitude=1.0 omega=0.0
cell csup.c module=csup theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel csdo.r0 -> csdo.s weight=0.5 delay=0.0 angle=0.0 lines=1
channel csdo.r1 -> csdo.s weight=0.5 delay=0.0 angle=0.0 lines=1

# --- B. backdoor: confounded observational world ----------------------------
field bd-obs dt=0.125 gain=1.0 deadband=0.5

module bdobs field=bd-obs belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell bdobs.h module=bdobs theta=0.0 amplitude=1.0 omega=0.0
cell bdobs.x module=bdobs theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell bdobs.y module=bdobs theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel bdobs.h -> bdobs.x weight=0.7 delay=0.0 angle=0.0 lines=1
channel bdobs.h -> bdobs.y weight=0.7 delay=0.0 angle=0.0 lines=1
channel bdobs.x -> bdobs.y weight=0.5 delay=0.0 angle=0.0 lines=1

# --- B. backdoor: twin under do(x := -), inbound h -> x severed --------------
field bd-do dt=0.125 gain=1.0 deadband=0.5

module bddo field=bd-do belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell bddo.h module=bddo theta=0.0 amplitude=1.0 omega=0.0
cell bddo.x module=bddo theta=3.141592653589793 amplitude=1.0 omega=0.0
cell bddo.y module=bddo theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel bddo.h -> bddo.y weight=0.7 delay=0.0 angle=0.0 lines=1
channel bddo.x -> bddo.y weight=0.5 delay=0.0 angle=0.0 lines=1

# --- C. frontdoor: mediated observational world ------------------------------
field fd-obs dt=0.125 gain=1.0 deadband=0.5

module fdobs field=fd-obs belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell fdobs.h module=fdobs theta=0.0 amplitude=1.0 omega=0.0
cell fdobs.x module=fdobs theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell fdobs.m module=fdobs theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell fdobs.y module=fdobs theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel fdobs.h -> fdobs.x weight=0.7 delay=0.0 angle=0.0 lines=1
channel fdobs.x -> fdobs.m weight=0.5 delay=0.0 angle=0.0 lines=1
channel fdobs.h -> fdobs.y weight=0.7 delay=0.0 angle=0.0 lines=1
channel fdobs.m -> fdobs.y weight=0.5 delay=0.0 angle=0.0 lines=1

# --- C. frontdoor: twin under do(m := -), inbound x -> m severed --------------
field fd-do dt=0.125 gain=1.0 deadband=0.5

module fddo field=fd-do belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell fddo.h module=fddo theta=0.0 amplitude=1.0 omega=0.0
cell fddo.x module=fddo theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell fddo.m module=fddo theta=3.141592653589793 amplitude=1.0 omega=0.0
cell fddo.y module=fddo theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel fddo.h -> fddo.x weight=0.7 delay=0.0 angle=0.0 lines=1
channel fddo.h -> fddo.y weight=0.7 delay=0.0 angle=0.0 lines=1
channel fddo.m -> fddo.y weight=0.5 delay=0.0 angle=0.0 lines=1

# --- runtime jobs -------------------------------------------------------------
flow cs-obs-flow field=cs-obs duration=1.0 expect-theta=csobs.s:1.570796 tolerance=0.00001
flow cs-do-flow  field=cs-do  duration=1.0 expect-theta=csdo.s:0.570796 tolerance=0.00001
flow bd-obs-flow field=bd-obs duration=1.0 expect-theta=bdobs.y:0.870796 tolerance=0.00001
flow bd-do-flow  field=bd-do  duration=1.0 expect-theta=bddo.y:1.370796 tolerance=0.00001
flow fd-obs-flow field=fd-obs duration=1.0 expect-theta=fdobs.y:0.870796 tolerance=0.00001
flow fd-do-flow  field=fd-do  duration=1.0 expect-theta=fddo.y:1.370796 tolerance=0.00001

commit cs-obs-commit module=csobs expect-trits=+-0 expect-balance=admissible expect-status=accepted expect-reason=none
commit cs-do-commit  module=csdo  expect-trits=+++ expect-balance=admissible expect-status=accepted expect-reason=none
commit bd-obs-commit module=bdobs expect-trits=+++ expect-balance=admissible expect-status=accepted expect-reason=none
commit bd-do-commit  module=bddo  expect-trits=+-0 expect-balance=admissible expect-status=accepted expect-reason=none
commit fd-obs-commit module=fdobs expect-trits=++0+ expect-balance=admissible expect-status=accepted expect-reason=none
commit fd-do-commit  module=fddo  expect-trits=++-0 expect-balance=admissible expect-status=accepted expect-reason=none

nest cf2-nest parent=csdo child=csup expect-parent-belief=0.666667 expect-child-prior=0.666667 tolerance=0.000001

# --- witnesses ------------------------------------------------------------------
witness gist-cf2-contested invariant=counterfactual-survival capability=G-counterfactual reducer=cs-obs-commit claim="contested evidence dissolves the conclusion to the crossing without vetoing the triad"
witness gist-cf2-sufficiency invariant=counterfactual-survival capability=G-counterfactual reducer=cs-do-commit claim="do(r1:=+) on the opposing root restores the conclusion, so removing the opposition is sufficient"
witness gist-cf2-association invariant=soundness capability=G-synthesis reducer=bd-obs-commit claim="the confounded observational field co-moves x and y through the back door"
witness gist-cf2-backdoor invariant=counterfactual-survival capability=G-counterfactual reducer=bd-do-commit claim="do(x:=-) with the backdoor severed shows the causal effect is weaker than the association"
witness gist-cf2-mediated invariant=soundness capability=G-synthesis reducer=fd-obs-commit claim="the mediated observational field carries the conclusion on the confounder while the mediator idles open"
witness gist-cf2-frontdoor invariant=counterfactual-survival capability=G-counterfactual reducer=fd-do-commit claim="do(m:=-) on the mediator alone dissolves the conclusion, isolating the mediated causal path"
witness gist-cf2-obs-flow invariant=flow-additivity capability=G-synthesis reducer=bd-obs-flow claim="the confounded field flows both descendants toward the confounder pole"
witness gist-cf2-do-flow invariant=flow-additivity capability=G-synthesis reducer=fd-do-flow claim="the intervened mediator propagates through its surviving outbound channel"
witness gist-cf2-nest invariant=existence-viability capability=G-existence reducer=cf2-nest claim="the restored conclusion nests upward as slot coherence"

expect reducer gist-cf2-nest
expect reducer gist-cf2-contested
expect reducer gist-cf2-sufficiency
expect reducer gist-cf2-association
expect reducer gist-cf2-backdoor
expect reducer gist-cf2-mediated
expect reducer gist-cf2-frontdoor
expect reducer gist-cf2-obs-flow
expect reducer gist-cf2-do-flow
