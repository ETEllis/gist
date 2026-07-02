#!/usr/bin/env bash
# One-line GIST: build the (vendored, extended) BiDi runtime once, then run
# the TRAINED GistHybrid natively on your ternary evidence word.
#
#   ./run.sh '+0-'      -> verdict from the trained .cdc weights
#   ./run.sh            -> full verification gate (native + trained parity)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RT="$HERE/runtime/build/cdc_native_runtime"
if [ ! -x "$RT" ]; then
  mkdir -p "$HERE/runtime/build"
  cc -O2 -o "$RT" "$HERE/runtime/cdc_native_runtime.c" "$HERE/runtime/cdc_source.c" -lm
fi
if [ $# -eq 0 ]; then
  exec "$HERE/native/verify_gist.sh"
fi
WORD="$1"
OUT="$("$RT" infer "$HERE/torchcdc/build/gist_hybrid.cdc" net "$WORD")"
echo "$OUT"
VERDICT="$(echo "$OUT" | tr ' ' '\n' | grep '^verdict=' | cut -d= -f2)"
if [ "$VERDICT" = "maybe" ]; then
  MIRROR="$(echo "$WORD" | tr '+-' '-+')"
  MOUT="$("$RT" infer "$HERE/torchcdc/build/gist_hybrid.cdc" net "$MIRROR")"
  MV="$(echo "$MOUT" | tr ' ' '\n' | grep '^verdict=' | cut -d= -f2)"
  if [ "$MV" = "yes" ]; then
    echo "mirror($MIRROR) -> yes  =>  final verdict: no"
  else
    echo "final verdict: maybe (open aperture - contribute evidence)"
  fi
else
  echo "final verdict: $VERDICT"
fi
