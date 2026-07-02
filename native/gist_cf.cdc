# gist_cf.cdc -- the Pearl do()-operator counterfactual, native, with no new primitive.
#
# The whole claim: CDC needs no do() primitive. Pearl's intervention decomposes
# into two things that are already native -- a LATCHED cell (fix the node) and a
# SEVERED inbound channel (cut its parents). A slot's channel graph is its
# structural causal model; the counterfactual twin is just a second field.
#
#   run  ./cdc_native_runtime run gist_cf.cdc
#
# Structural causal model (both fields):  u -> r0 -> s   and   r1 -> s
# The conclusion cell s is caused by r0 (itself caused by u) and by r1.
#
# FACTUAL (field cf-fact): evidence agrees. Flow drives the undecided
# conclusion s (theta = pi/2, trit 0) toward the + pole:
#   s := pi/2 + 0.5*sin(r0 - s) + 0.5*sin(r1 - s)
#      = pi/2 + 0.5*sin(-pi/2) + 0.5*sin(-pi/2) = pi/2 - 1 = 0.570796  -> trit +
#   commit -> ++++ , conclusion s = + (asserted).
#
# COUNTERFACTUAL (field cf-twin) under do(r0 := -): r0 is set to the - pole and
# its inbound channel u -> r0 is SEVERED (absent); its outbound r0 -> s remains.
#   s := pi/2 + 0.5*sin(pi - pi/2) + 0.5*sin(0 - pi/2)
#      = pi/2 + 0.5*(1) + 0.5*(-1) = pi/2 = 1.570796  -> trit 0
#   commit -> +-+0 , conclusion s = 0 (dissolved back to the open crossing).
#
# SURVIVAL: factual s = + but twin s = 0. The conclusion did NOT survive
# do(r0 := -); it returned to the aperture. So r0 is causally load-bearing.
# That comparison, over each evidence cell, is GIST's counterfactual-agreement
# metric -- computed entirely by native flow/commit, zero host code.

# --- factual world -------------------------------------------------------
field cf-fact dt=0.125 gain=1.0 deadband=0.5

module claim field=cf-fact belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell claim.u  module=claim theta=0.0 amplitude=1.0 omega=0.0
cell claim.r0 module=claim theta=0.0 amplitude=1.0 omega=0.0
cell claim.r1 module=claim theta=0.0 amplitude=1.0 omega=0.0
cell claim.s  module=claim theta=1.5707963267948966 amplitude=1.0 omega=0.0

# the conclusion's downstream scope (for the upward nest)
module concl field=cf-fact belief=0.0 prior=0.0 precision=1.0 action-gain=1.0 parent=claim
cell concl.a module=concl theta=0.0 amplitude=1.0 omega=0.0
cell concl.b module=concl theta=0.0 amplitude=1.0 omega=0.0
cell concl.c module=concl theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel claim.u  -> claim.r0 weight=0.5 delay=0.0 angle=0.0 lines=1
channel claim.r0 -> claim.s  weight=0.5 delay=0.0 angle=0.0 lines=1
channel claim.r1 -> claim.s  weight=0.5 delay=0.0 angle=0.0 lines=1

# --- counterfactual twin under do(r0 := -), inbound u -> r0 severed -------
field cf-twin dt=0.125 gain=1.0 deadband=0.5

module claimt field=cf-twin belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell claimt.u  module=claimt theta=0.0 amplitude=1.0 omega=0.0
cell claimt.r0 module=claimt theta=3.141592653589793 amplitude=1.0 omega=0.0
cell claimt.r1 module=claimt theta=0.0 amplitude=1.0 omega=0.0
cell claimt.s  module=claimt theta=1.5707963267948966 amplitude=1.0 omega=0.0

# outbound r0 -> s is preserved; inbound u -> r0 is intentionally absent (do)
channel claimt.r0 -> claimt.s weight=0.5 delay=0.0 angle=0.0 lines=1
channel claimt.r1 -> claimt.s weight=0.5 delay=0.0 angle=0.0 lines=1

flow cf-fact-flow field=cf-fact duration=1.0 expect-theta=claim.s:0.570796 tolerance=0.00001
flow cf-twin-flow field=cf-twin duration=1.0 expect-theta=claimt.s:1.570796 tolerance=0.00001
commit cf-fact-commit module=claim expect-trits=++++ expect-balance=admissible expect-status=accepted expect-reason=none
commit cf-twin-commit module=claimt expect-trits=+-+0 expect-balance=admissible expect-status=accepted expect-reason=none
nest cf-nest parent=claim child=concl expect-parent-belief=0.666667 expect-child-prior=0.666667 tolerance=0.000001

witness gist-cf-factual invariant=counterfactual-survival capability=G-counterfactual reducer=cf-fact-commit claim="factual field commits the conclusion as asserted +"
witness gist-cf-intervention invariant=counterfactual-survival capability=G-counterfactual reducer=cf-twin-commit claim="do(r0:=-) with severed inbound dissolves the conclusion to the crossing 0, so r0 is causal"
witness gist-cf-flow invariant=flow-additivity capability=G-synthesis reducer=cf-twin-flow claim="twin field propagates the intervention through the surviving outbound channel"
witness gist-cf-nest invariant=existence-viability capability=G-existence reducer=cf-nest claim="the surviving conclusion nests upward as slot coherence"

expect reducer gist-cf-factual
expect reducer gist-cf-intervention
expect reducer gist-cf-flow
expect reducer gist-cf-nest
