#!/usr/bin/env bash
# verify_gist.sh -- run the whole native GIST gate through the existing BiDi
# runtimes. No new host code: this only invokes cdc_boot.py (contract check)
# and the prebuilt cdc_native_runtime (execution).
#
# Layout assumed:
#   <project>/gist/native/*.cdc          <- this directory
#   <project>/bidi-coherence-delta-calculus/  <- the BiDi repo copy
#
# Override the BiDi location with:  BIDI=/path/to/bidi ./verify_gist.sh
set -euo pipefail

GIST_NATIVE="$(cd "$(dirname "$0")" && pwd)"
VENDORED="$GIST_NATIVE/../runtime"
if [ -z "${BIDI:-}" ] && [ -f "$VENDORED/cdc_native_runtime.c" ]; then
  # self-contained checkout: use the vendored (extended) BiDi micro-bridge
  BOOT="$VENDORED/cdc_boot.py"
  RT="$VENDORED/build/cdc_native_runtime"
  if [ ! -x "$RT" ]; then
    echo "building vendored BiDi native runtime (one-time)..."
    mkdir -p "$VENDORED/build"
    cc -O2 -o "$RT" \
       "$VENDORED/cdc_native_runtime.c" "$VENDORED/cdc_source.c" -lm
  fi
else
  BIDI="${BIDI:-$(cd "$GIST_NATIVE/../../bidi-coherence-delta-calculus" && pwd)}"
  BOOT="$BIDI/cdc_boot.py"
  RT="$BIDI/build/cdc_native_runtime"
  if [ ! -x "$RT" ]; then
    echo "building BiDi native runtime (one-time)..."
    cc -O2 -o "$RT" \
       "$BIDI/runtime/cdc_native_runtime.c" "$BIDI/runtime/cdc_source.c" -lm
  fi
fi

cd "$GIST_NATIVE"
mkdir -p build

echo "======================================================================"
echo "  GIST native runtime jobs (BiDi cdc_native_runtime)"
echo "======================================================================"
echo "--- synthesis pyramid: run / compile / interpret / prove ---"
"$RT" run       gist_pyramid.cdc
"$RT" compile   gist_pyramid.cdc | tail -1
"$RT" interpret gist_pyramid.cdc | tail -1
"$RT" prove     gist_pyramid.cdc
echo "--- Pearl do() counterfactual twin fields ---"
"$RT" run       gist_cf.cdc
echo "--- Pearl cluster 2: sufficiency / backdoor / frontdoor surgeries ---"
"$RT" run       gist_cf2.cdc | tail -1
echo "--- the field as neural network: forward pass / bottleneck / pool ---"
"$RT" run       gist_neural.cdc | tail -1
"$RT" compile   gist_neural.cdc | tail -1
"$RT" interpret gist_neural.cdc | tail -1
echo "--- native learning: plastic weights follow correlation ---"
"$RT" run       gist_learn.cdc | tail -1
echo "--- native inference: weights.cdc + input word -> ternary verdict ---"
"$RT" infer     gist_neural.cdc net '++-'
echo "--- native TRAINING: clamped-teacher plasticity through flow ---"
"$RT" train gist_train_net.cdc net gist_scenes_train.cdc 10 build/gist_trained_check.cdc | tail -2
echo "held-out:" && "$RT" train build/gist_trained_check.cdc net gist_scenes_test.cdc 0 /dev/null | head -1
"$RT" infer gist_trained.cdc net '++-'
echo "--- emergent 64-gate surface ---"
"$RT" surface   gist_gate.cdc | tail -1
echo "--- meta-gate ladder council + decision-stamp self-evolution ---"
"$RT" council   gist_ladder.cdc | tail -1
"$RT" evolve    gist_ladder.cdc | tail -1

echo
echo "======================================================================"
echo "  GIST native contract (BiDi cdc_boot.py)"
echo "======================================================================"
python3 "$BOOT" \
  "$GIST_NATIVE/gist_laws.cdc" \
  "$GIST_NATIVE/gist_lattice.cdc" \
  "$GIST_NATIVE/gist_pyramid.cdc" \
  "$GIST_NATIVE/gist_cf.cdc" \
  "$GIST_NATIVE/gist_cf2.cdc" \
  "$GIST_NATIVE/gist_neural.cdc" \
  "$GIST_NATIVE/gist_learn.cdc" \
  "$GIST_NATIVE/gist_gate.cdc" \
  "$GIST_NATIVE/gist_ladder.cdc" \
  "$GIST_NATIVE/gist.cdc"

echo
echo "GIST native build verified: all runtime jobs executed and the .cdc"
echo "contract passed through the BiDi bootstrap (host-debt 0)."
