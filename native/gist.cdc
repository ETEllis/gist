# gist.cdc -- the GIST native self-hosting contract (kernel entry).
#
# GIST is Gated Insight Synthesis Topology: a 64-slot (2^6 = 4^3) lattice of
# balanced-ternary coherence modules, reduced by guarded commits, a six-round
# Hamming meta-gate ladder, council reconciliation, and a bridge-coordinate
# decision stamp -- instantiated entirely out of the BiDi Coherence-Delta
# Calculus.
#
# This kernel is SUBORDINATE. It declares no bootloader of its own: it rides on
# the BiDi bootstrap (cdc_boot.py) and the BiDi C native runtimes that are
# already instantiated. `expect host-debt <= 0` asserts exactly that -- GIST
# adds no host debt. The full artifact is native .cdc; the only non-.cdc code
# in the loop is BiDi's existing runtime micro-bridge.
#
# Check this contract with the BiDi bootloader over the GIST source set:
#   python3 <bidi>/cdc_boot.py gist_laws.cdc gist_lattice.cdc gist_pyramid.cdc \
#           gist_cf.cdc gist_gate.cdc gist_ladder.cdc gist.cdc
# (see verify_gist.sh for the full runtime + contract gate).

kernel gist stage=1 target=cdc
  term slot triad dyad singular gist gate ladder council retrieval saturation
  term decision stamp coverage parity aperture twin conclusion

  rule synthesize fold commit nest gate saturate reconcile stamp cover
  rule deliberate evolve intervene

  provides G-synthesis G-gate G-ladder G-retrieval G-decision
  provides G-compile G-interpret G-coverage G-counterfactual G-existence
  provides gist-64-lattice gist-synthesis-pyramid gist-emergent-gate
  provides gist-meta-ladder gist-decision-stamp gist-counterfactual-twin

  expect native substrate == cdc
  expect host-debt <= 0
  expect terms >= 15
  expect rules >= 10
  expect invariants >= 6
  expect capabilities >= 10
  expect witnesses >= 45

  expect provides G-synthesis G-gate G-ladder G-retrieval G-decision
  expect provides G-compile G-interpret G-coverage G-counterfactual G-existence
  expect provides gist-64-lattice gist-synthesis-pyramid gist-emergent-gate
  expect provides gist-meta-ladder gist-decision-stamp gist-counterfactual-twin
end
