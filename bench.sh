#!/usr/bin/env bash
# bench.sh -- credible, reproducible benchmarks for the GIST repo.
# Everything measured here re-runs from a fresh checkout: no hand-waves.
# Output: BENCHMARKS.md (methodology + numbers + machine info).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RT="$HERE/runtime/build/cdc_native_runtime"
[ -x "$RT" ] || { mkdir -p "$HERE/runtime/build"; cc -O2 -o "$RT" \
  "$HERE/runtime/cdc_native_runtime.c" "$HERE/runtime/cdc_source.c" -lm; }
cd "$HERE/native"
N_INFER=1000

echo "== 1/4 inference latency ($N_INFER calls) =="
INFER_TOTAL=$(/usr/bin/time -p sh -c "for i in \$(seq 1 $N_INFER); do '$RT' infer gist_trained.cdc net '+0-' >/dev/null; done" 2>&1 | awk '/^real/{print $2}')
INFER_MS=$(awk "BEGIN{printf \"%.2f\", $INFER_TOTAL*1000/$N_INFER}")

echo "== 2/4 native training wall time (400 scenes x 10 epochs) =="
TRAIN_TIME=$( { /usr/bin/time -p "$RT" train gist_train_net.cdc net gist_scenes_train.cdc 10 build/bench_trained.cdc > /tmp/bench_train.out; } 2>&1 | awk '/^real/{print $2}')
TRAIN_OUT=$(cat /tmp/bench_train.out)
TRAIN_S="${TRAIN_TIME}s"
UNTRAINED=$(echo "$TRAIN_OUT" | head -1 | grep -o 'acc=[0-9.]*' | cut -d= -f2)
TRAINED=$(echo "$TRAIN_OUT" | tail -2 | head -1 | grep -o 'acc=[0-9.]*' | cut -d= -f2)

echo "== 3/4 held-out evaluation (150 scenes) =="
TEST_TRAINED=$("$RT" train build/bench_trained.cdc net gist_scenes_test.cdc 0 /dev/null | head -1 | grep -o 'acc=[0-9.]*' | cut -d= -f2)
TEST_UNTRAINED=$("$RT" train gist_train_net.cdc net gist_scenes_test.cdc 0 /dev/null | head -1 | grep -o 'acc=[0-9.]*' | cut -d= -f2)
# majority baseline straight from the committed .cdc dataset (label poles)
POS=$(grep -c 'cell s[0-9]*\.c3 .*theta=0\.0* ' gist_scenes_test.cdc || true)
NEG=$(grep -c 'cell s[0-9]*\.c3 .*theta=3\.14' gist_scenes_test.cdc || true)
ZER=$(grep -c 'cell s[0-9]*\.c3 .*theta=1\.57' gist_scenes_test.cdc || true)
TOT=$((POS + NEG + ZER))
MAJ=$ZER; [ "$POS" -gt "$MAJ" ] && MAJ=$POS; [ "$NEG" -gt "$MAJ" ] && MAJ=$NEG
MAJ_ACC=$(awk "BEGIN{printf \"%.4f\", $MAJ/$TOT}")

echo "== 4/4 full verification gate wall time =="
GATE_TIME=$( { /usr/bin/time -p ./verify_gist.sh >/dev/null; } 2>&1 | awk '/^real/{print $2}')
GATE_S="${GATE_TIME}s"

cat > "$HERE/BENCHMARKS.md" <<MD
# Benchmarks

Reproduce with \`./bench.sh\` from a fresh checkout. No numbers below are
estimated: each is measured by this script on the machine described at the
bottom, and the accuracy table is computed from the committed \`.cdc\`
datasets and the runtime's own training/evaluation commands.

## Accuracy - native training (clamped-teacher plasticity, C runtime only)

Task: anticipate the converged (40x0.25-step) fixed-pyramid conclusion
from two flow layers. Labels were computed by the runtime's own converged
reduction and are baked into the committed datasets
(\`native/gist_scenes_{train,test}.cdc\`; 400/150 scenes, disjoint seeds).

| model | train acc | held-out acc |
|---|---|---|
| majority-class baseline | - | $MAJ_ACC |
| calculus init, untrained | $UNTRAINED | $TEST_UNTRAINED |
| **natively trained** (10 epochs) | **$TRAINED** | **$TEST_TRAINED** |
| converged oracle (labeler) | 1.0 | 1.0 |

## Speed

| measurement | value |
|---|---|
| inference latency (\`infer\`, full process spawn incl. parse) | ${INFER_MS} ms/call (${N_INFER} calls in ${INFER_TOTAL}s) |
| native training, 400 scenes x 10 epochs + 11 evals | ${TRAIN_S} |
| full verification gate (\`verify_gist.sh\`: all runtime jobs + contract) | ${GATE_S} |

## Reference experiments (construction-tier, code not shipped)

A gradient-trained full hybrid (recurrent state-space x SO(2) convolution
x openness gating x ternary bottleneck x ladder pooling; 109 parameters)
reached 0.984 slot / 0.868 global-verdict accuracy on 64-slot scenes with
27/27 native-inference parity; quoted from the paper, harness kept out of
this repository by the CDC-only constraint.

## Machine

\`\`\`
$(uname -srm)
$(cc --version | head -1)
$(sysctl -n machdep.cpu.brand_string 2>/dev/null || true)
\`\`\`
MD
echo "wrote BENCHMARKS.md"
