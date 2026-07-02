# gist_lattice.cdc -- the GIST 64-slot address system over the bridge64 surface.
#
# GIST's lattice IS the CDC dyadic/triadic bridge: every slot has a six-bit
# dyadic address and a three-digit triadic address (2^6 = 4^3 = 64). The three
# triadic digits are GIST's three semantic axes, each with four values:
#
#   axis 1 (temporal):    0 past      1 present   2 future       3 meta
#   axis 2 (abstraction): 0 micro     1 meso      2 macro        3 systems
#   axis 3 (evidence):    0 empirical 1 theoretic 2 computation  3 synthetic
#
# The six dyadic bits are the Hamming coordinates the meta-gate ladder consumes
# one per round (gist_ladder). This file is a declaration codebook in the
# spirit of bridge64.cdc: it names the axes, the axis values, and reference
# corner slots, each as a native witness. It carries no reducer steps.

# --- axis value declarations (coverage-parity requires all four per axis) ---

witness gist-axis-temporal-0 invariant=coverage-parity axis=temporal value=0 label=past claim="temporal axis value 0 is past"
witness gist-axis-temporal-1 invariant=coverage-parity axis=temporal value=1 label=present claim="temporal axis value 1 is present"
witness gist-axis-temporal-2 invariant=coverage-parity axis=temporal value=2 label=future claim="temporal axis value 2 is future"
witness gist-axis-temporal-3 invariant=coverage-parity axis=temporal value=3 label=meta claim="temporal axis value 3 is meta"

witness gist-axis-abstraction-0 invariant=coverage-parity axis=abstraction value=0 label=micro claim="abstraction axis value 0 is micro"
witness gist-axis-abstraction-1 invariant=coverage-parity axis=abstraction value=1 label=meso claim="abstraction axis value 1 is meso"
witness gist-axis-abstraction-2 invariant=coverage-parity axis=abstraction value=2 label=macro claim="abstraction axis value 2 is macro"
witness gist-axis-abstraction-3 invariant=coverage-parity axis=abstraction value=3 label=systems claim="abstraction axis value 3 is systems"

witness gist-axis-evidence-0 invariant=coverage-parity axis=evidence value=0 label=empirical claim="evidence axis value 0 is empirical"
witness gist-axis-evidence-1 invariant=coverage-parity axis=evidence value=1 label=theoretical claim="evidence axis value 1 is theoretical"
witness gist-axis-evidence-2 invariant=coverage-parity axis=evidence value=2 label=computational claim="evidence axis value 2 is computational"
witness gist-axis-evidence-3 invariant=coverage-parity axis=evidence value=3 label=synthetic claim="evidence axis value 3 is synthetic"

# --- reference corner slots (dyadic -> triadic through the bridge64 rule) ---

witness gist-slot-000000-000 invariant=dyadic-triadic-closure dyadic=000000 triadic=000 index=0 role=core-foundational claim="slot 000000 is triadic 000 = past/micro/empirical, the core foundational scope"
witness gist-slot-010101-111 invariant=dyadic-triadic-closure dyadic=010101 triadic=111 index=21 role=balanced-mid claim="slot 010101 is triadic 111 = present/meso/theoretical, the balanced mid scope"
witness gist-slot-101101-231 invariant=dyadic-triadic-closure dyadic=101101 triadic=231 index=45 role=decision-coordinate claim="slot 101101 is triadic 231 = future/systems/theoretical, the reference decision coordinate"
witness gist-slot-111111-333 invariant=dyadic-triadic-closure dyadic=111111 triadic=333 index=63 role=edge-extreme claim="slot 111111 is triadic 333 = meta/systems/synthetic, the edge extreme scope"

expect witness gist-axis-temporal-0
expect witness gist-axis-temporal-1
expect witness gist-axis-temporal-2
expect witness gist-axis-temporal-3
expect witness gist-axis-abstraction-0
expect witness gist-axis-abstraction-1
expect witness gist-axis-abstraction-2
expect witness gist-axis-abstraction-3
expect witness gist-axis-evidence-0
expect witness gist-axis-evidence-1
expect witness gist-axis-evidence-2
expect witness gist-axis-evidence-3
expect witness gist-slot-000000-000
expect witness gist-slot-010101-111
expect witness gist-slot-101101-231
expect witness gist-slot-111111-333
