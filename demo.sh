#!/usr/bin/env bash
# demo.sh -- 60-second walkthrough: verify, train, evaluate, judge.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RT="$HERE/runtime/build/cdc_native_runtime"
[ -x "$RT" ] || { mkdir -p "$HERE/runtime/build"; cc -O2 -o "$RT" \
  "$HERE/runtime/cdc_native_runtime.c" "$HERE/runtime/cdc_source.c" -lm; }
cd "$HERE/native"
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

say "1. The mechanism verifies itself (83/83 expectations, host-debt 0):"
./verify_gist.sh 2>/dev/null | grep -E "expectations met|OK host-debt"

say "2. Pearl's do() runs natively (twin fields: latch + severed channel):"
"$RT" run gist_cf.cdc | grep commit=

say "3. Train the net - in C, from .cdc data, to .cdc weights:"
"$RT" train gist_train_net.cdc net gist_scenes_train.cdc 10 build/demo_trained.cdc | sed -n '1p;$p'

say "4. Held-out evaluation (150 unseen scenes):"
"$RT" train build/demo_trained.cdc net gist_scenes_test.cdc 0 /dev/null | head -1

say "5. Judge evidence with the trained weights:"
for w in '++-' '0+0' '-0-' '000'; do
  "$HERE/run.sh" "$w" | tail -1 | sed "s/^/   $w  ->  /"
done

say "Done: one substrate verified, trained, and judging - zero host code."
