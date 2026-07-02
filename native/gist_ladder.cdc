# gist_ladder.cdc -- the meta-gate ladder + decision stamp as council/evolve jobs.
#
# The 64->...->1 reduction ends in one final reconciliation: Meta_Imagination
# (extrapolative) against Aggregate_Internal (evidence-bound), plus the horizon
# reconciler. GIST runs it as a native council deliberation, and stamps the
# adopted decision by self-evolving a source copy with the decision witness --
# the decision-stamp made native (self-evolution IS the stamp).
#
#   council  ./cdc_native_runtime council gist_ladder.cdc
#   evolve   ./cdc_native_runtime evolve  gist_ladder.cdc
#
# Three council members, six cells: trits +0 -+ 0- concatenate to +0-+0- ->
# occupancy 101101 = triadic 231 (the decision coordinate). Occupancy 4 meets
# quorum 4 -> decision adopt. The evolve job appends the decision witness into
# build/gist_evolved_ladder.cdc, binding the coordinate to the reduction.

field council-field dt=0.125 gain=1.0 deadband=0.5

module meta field=council-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell meta.a module=meta theta=0.0 amplitude=1.0 omega=0.0
cell meta.b module=meta theta=1.5707963267948966 amplitude=1.0 omega=0.0

module aggregate field=council-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell aggregate.a module=aggregate theta=3.141592653589793 amplitude=1.0 omega=0.0
cell aggregate.b module=aggregate theta=0.0 amplitude=1.0 omega=0.0

module horizon field=council-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell horizon.a module=horizon theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell horizon.b module=horizon theta=3.141592653589793 amplitude=1.0 omega=0.0

council gist-council field=council-field members=meta,aggregate,horizon quorum=4 expect-decision=adopt expect-dyadic=101101 expect-triadic=231
deliberate gist-deliberation council=gist-council
evolve gist-decision-stamp source=gist_ladder.cdc output=build/gist_evolved_ladder.cdc coordinate=101101 append-witness=gist-decision-witness expect-contains=gist-decision-witness

witness gist-council-native invariant=ladder-reduction capability=G-ladder council=gist-deliberation claim="the meta/aggregate/horizon council reduces to the adopted decision coordinate 231"
witness gist-stamp-native invariant=decision-stamp capability=G-decision evolution=gist-decision-stamp claim="the decision coordinate is stamped into an evolved source copy"

expect council gist-council-native
expect evolution gist-stamp-native
