# learned natively: clamped-teacher plasticity through flow (cdc_native_runtime train)
# gist_train_net.cdc -- the trainable native net (initialized AT the calculus).
#
# Layout: c0,c1,c2 evidence inputs | c3,c4 dyads | c5 singular (conclusion,
# last cell by convention). All six pyramid channels are plastic: training is
# clamped-teacher plasticity through flow, executed by the C runtime:
#
#   cdc_native_runtime train gist_train_net.cdc net gist_scenes_train.cdc 10 gist_trained.cdc
#   cdc_native_runtime train gist_trained.cdc  net gist_scenes_test.cdc  0 /dev/null   # eval
#   cdc_native_runtime infer gist_trained.cdc  net '+0-'
#
# The two flow layers are the anticipation budget: labels are the CONVERGED
# fixed-pyramid singular (40 x 0.25 steps); the net must learn to reach the
# same conclusion in two steps.

field nn-train dt=0.125 gain=1.0 deadband=0.5

module net field=nn-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell net.c0 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.c1 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.c2 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.c3 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.c4 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0
cell net.c5 module=net theta=1.5707963267948966 amplitude=1.0 omega=0.0

channel net.c0 -> net.c3 weight=0.671100745847 delay=0.000000 angle=0.000000000000 lines=1 plastic=1 rate=0.050000
channel net.c1 -> net.c3 weight=0.678593554754 delay=0.000000 angle=0.000000000000 lines=1 plastic=1 rate=0.050000
channel net.c1 -> net.c4 weight=0.637654511171 delay=0.000000 angle=0.000000000000 lines=1 plastic=1 rate=0.050000
channel net.c2 -> net.c4 weight=0.578428485134 delay=0.000000 angle=0.000000000000 lines=1 plastic=1 rate=0.050000
channel net.c3 -> net.c5 weight=0.670138890142 delay=0.000000 angle=0.000000000000 lines=1 plastic=1 rate=0.050000
channel net.c4 -> net.c5 weight=0.693383601961 delay=0.000000 angle=0.000000000000 lines=1 plastic=1 rate=0.050000

flow layer1 field=nn-train duration=1.0
flow layer2 field=nn-train duration=1.0

commit conclude module=net
nest ground parent=net child=net-scope

module net-scope field=nn-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0 parent=net
cell net-scope.a module=net-scope theta=0.0 amplitude=1.0 omega=0.0
