# gist_neural.cdc -- the neural network IS the field: the GIST forward pass
# as native reducer jobs. No tensors, no host code -- the decided hybrid form
# (selective nonlinear state-space recurrence x convolutional filtration x
# balanced-ternary bottleneck) is executed literally by flow/commit/nest.
#
#   run       ./cdc_native_runtime run       gist_neural.cdc
#   compile   ./cdc_native_runtime compile   gist_neural.cdc
#   interpret ./cdc_native_runtime interpret gist_neural.cdc
#
# The isomorphism, clause by clause:
#   * WEIGHTS are channels: weight w and angle alpha form the SO(2) mixing
#     block w*[[cos a,-sin a],[sin a,cos a]] -- here the corefold pyramid
#     (fixed filtration topology, six edges, w=0.5, alpha=0).
#   * LAYERS are flow jobs: each frozen-afferent flow step is one forward
#     layer of the recurrence theta += Sum w*sin(theta_src - theta_dst) --
#     the Kuramoto turn, a selective (state-dependent) nonlinear update.
#     Three sequential flow jobs below = a three-layer forward pass on
#     shared state.
#   * The TERNARY BOTTLENECK is commit: cos(theta) quantized at the deadband
#     into {-,0,+} behind the trit-walk barrier (the semantic quantizer, not
#     a compression trick).
#   * POOLING is nest: child coherence aggregates upward as the readout.
#   * The IR is the network graph: compile/interpret list and execute the
#     same jobs as reducer ops.
#
# Forward pass (inputs r0=+, r1=+, r2=-; hidden d0,d1 and output s open):
#   layer1: d0 = pi/2 + 0.5 sin(-pi/2) + 0.5 sin(-pi/2) = 0.570796 (+)
#           d1 = pi/2 + 0.5 sin(-pi/2) + 0.5 sin(+pi/2) = pi/2      (0)
#           s unchanged (hidden still at the crossing).
#   layer2: d0 -> 0.030494, d1 pinned by symmetry, s -> 1.150061.
#   layer3: s -> 0.904321 -> cos = 0.618 > deadband -> trit +.
#   bottleneck: word ++-+0+ (walk 1,2,1,2,2,3 admissible) -> accepted.
#   The network concludes + from mixed evidence, with the dissenting input
#   and the balanced hidden unit visible in the word -- an interpretable
#   ternary activation record, gate-checked.

field nn-forward dt=0.125 gain=1.0 deadband=0.5

# the slot as network: inputs r0,r1,r2 | hidden d0,d1 | output s
module net field=nn-forward belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell net.r0 module=net theta=0.0 amplitude=1.0 omega=0.0
cell net.r1 module=net theta=0.0 amplitude=1.0 omega=0.0
cell net.r2 module=net theta=3.141592653589793 amplitude=1.0 omega=0.0
cell net.d0 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.d1 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.s  module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0

# the readout scope pooled from the network's conclusion (for nest)
module readout field=nn-forward belief=0.0 prior=0.0 precision=1.0 action-gain=1.0 parent=net
cell readout.a module=readout theta=0.0 amplitude=1.0 omega=0.0
cell readout.b module=readout theta=0.0 amplitude=1.0 omega=0.0
cell readout.c module=readout theta=1.5707963267948966 amplitude=1.0 omega=0.0

# the filtration weights: the corefold pyramid as SO(2) channel blocks
channel net.r0 -> net.d0 weight=0.5 delay=0.0 angle=0.0 lines=1
channel net.r1 -> net.d0 weight=0.5 delay=0.0 angle=0.0 lines=1
channel net.r1 -> net.d1 weight=0.5 delay=0.0 angle=0.0 lines=1
channel net.r2 -> net.d1 weight=0.5 delay=0.0 angle=0.0 lines=1
channel net.d0 -> net.s  weight=0.5 delay=0.0 angle=0.0 lines=1
channel net.d1 -> net.s  weight=0.5 delay=0.0 angle=0.0 lines=1

# --- the forward pass: three layers = three flow jobs on shared state --------
flow nn-layer1 field=nn-forward duration=1.0 expect-theta=net.d0:0.570796 tolerance=0.00001
flow nn-layer2 field=nn-forward duration=1.0 expect-theta=net.s:1.150061 tolerance=0.00001
flow nn-layer3 field=nn-forward duration=1.0 expect-theta=net.s:0.904321 tolerance=0.00001

# --- the ternary bottleneck: quantize the whole state behind the barrier ------
commit nn-bottleneck module=net expect-trits=++-+0+ expect-balance=admissible expect-status=accepted expect-reason=none

# --- pooling: the conclusion aggregates upward as readout coherence -----------
nest nn-pool parent=net child=readout expect-parent-belief=0.666667 expect-child-prior=0.666667 tolerance=0.000001

# --- the network graph as reducer IR -------------------------------------------
compile nn-ir source=gist_neural.cdc expect-ops=5 expect-flow=3 expect-commit=1 expect-nest=1
interpret nn-ir-exec source=gist_neural.cdc expect-ops=5 expect-flow=3 expect-commit=1 expect-nest=1

# --- witnesses --------------------------------------------------------------------
witness gist-nn-weights invariant=flow-additivity capability=G-neural reducer=nn-layer1 claim="channels are the network weights: the pyramid filtration mixes inputs into the hidden layer as SO(2) blocks"
witness gist-nn-layers invariant=flow-additivity capability=G-neural reducer=nn-layer3 claim="sequential flow jobs are forward layers: three frozen Kuramoto steps carry the conclusion across the deadband"
witness gist-nn-bottleneck invariant=preservation capability=G-neural reducer=nn-bottleneck claim="commit is the ternary bottleneck: the forward state quantizes to the admissible word ++-+0+ behind the barrier"
witness gist-nn-pool invariant=existence-viability capability=G-neural reducer=nn-pool claim="nest is the pooling layer: network conclusion coherence aggregates upward into the readout scope"
witness gist-nn-graph capability=G-compile compile=nn-ir claim="the compiled reducer IR is the network graph: five ops, three layers, one bottleneck, one pool"
witness gist-nn-exec capability=G-interpret interpret=nn-ir-exec claim="the interpreted IR executes the same forward pass the reducer ran"

expect reducer gist-nn-weights
expect reducer gist-nn-layers
expect reducer gist-nn-bottleneck
expect reducer gist-nn-pool
expect compile gist-nn-graph
expect interpret gist-nn-exec
