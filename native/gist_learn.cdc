# gist_learn.cdc -- native learning: plastic weights follow correlation.
#
# The calculus has always DECLARED learning ("plastic weights follow
# correlation" -- the Hebbian half of the flow relation); as of this build the
# BiDi C native runtime EXECUTES it: channels may carry plastic=1 rate=r, and
# every flow step updates their weights on the same frozen phases it reads:
#
#     w  +=  rate * ( cos(theta_src + angle - theta_dst) - w ) * duration
#
#   run  ./cdc_native_runtime run gist_learn.cdc
#
# Scenario: a presynaptic assertion (pre = +) coupled to a nearly-aligned
# postsynaptic cell (post = 0.2 rad) through a weak plastic channel (w = 0.1,
# rate = 0.5). Two flow steps of native learning:
#
#   step 1: correlation cos(0 - 0.2)      = 0.980067
#           w    -> 0.1 + 0.5*(0.980067 - 0.1)      = 0.540033
#           post -> 0.2 + 0.1*sin(-0.2)             = 0.180133
#   step 2: correlation cos(0 - 0.180133) = 0.983821
#           w    -> 0.540033 + 0.5*(0.983821 - 0.540033) = 0.761927
#           post -> 0.180133 + 0.540033*sin(-0.180133)   = 0.083380
#
# The weight LEARNED the alignment (0.1 -> 0.76) while the phases entrained
# (0.2 -> 0.08): structure and state co-adapt through one reduction -- this is
# the native substrate the torchcdc harness's gradient training rides on top
# of, and the reason "training" is not foreign to the calculus.

field learn-field dt=0.125 gain=1.0 deadband=0.5

module hebb field=learn-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell hebb.pre  module=hebb theta=0.0 amplitude=1.0 omega=0.0
cell hebb.post module=hebb theta=0.2 amplitude=1.0 omega=0.0

# the learned conclusion's downstream scope (for the upward nest)
module learned field=learn-field belief=0.0 prior=0.0 precision=1.0 action-gain=1.0 parent=hebb
cell learned.a module=learned theta=0.0 amplitude=1.0 omega=0.0
cell learned.b module=learned theta=0.0 amplitude=1.0 omega=0.0
cell learned.c module=learned theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel hebb.pre -> hebb.post weight=0.1 delay=0.0 angle=0.0 lines=1 plastic=1 rate=0.5

flow learn-step1 field=learn-field duration=1.0 expect-weight=hebb.pre->hebb.post:0.540033 tolerance=0.00001
flow learn-step2 field=learn-field duration=1.0 expect-weight=hebb.pre->hebb.post:0.761927 expect-theta=hebb.post:0.083380 tolerance=0.00001

commit learn-commit module=hebb expect-trits=++ expect-balance=admissible expect-status=accepted expect-reason=none
nest learn-nest parent=hebb child=learned expect-parent-belief=0.666667 expect-child-prior=0.666667 tolerance=0.000001

witness gist-learn-hebbian invariant=native-plasticity capability=G-neural reducer=learn-step2 claim="the C native runtime executes plastic weight adaptation: the channel learned the phase alignment through flow"
witness gist-learn-entrain invariant=flow-additivity capability=G-neural reducer=learn-step1 claim="phases entrain while weights learn: state and structure co-adapt in one reduction"
witness gist-learn-commit invariant=preservation capability=G-neural reducer=learn-commit claim="the learned configuration commits to an admissible word"
witness gist-learn-nest invariant=existence-viability capability=G-existence reducer=learn-nest claim="the learned conclusion nests upward as coherence"

expect reducer gist-learn-hebbian
expect reducer gist-learn-entrain
expect reducer gist-learn-commit
expect reducer gist-learn-nest
