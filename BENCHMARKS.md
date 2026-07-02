# Benchmarks

Reproduce with `./bench.sh` from a fresh checkout. No numbers below are
estimated: each is measured by this script on the machine described at the
bottom, and the accuracy table is computed from the committed `.cdc`
datasets and the runtime's own training/evaluation commands.

## Accuracy - native training (clamped-teacher plasticity, C runtime only)

Task: anticipate the converged (40x0.25-step) fixed-pyramid conclusion
from two flow layers. Labels were computed by the runtime's own converged
reduction and are baked into the committed datasets
(`native/gist_scenes_{train,test}.cdc`; 400/150 scenes, disjoint seeds).

| model | train acc | held-out acc |
|---|---|---|
| majority-class baseline | - | 0.6200 |
| calculus init, untrained | 0.7875 | 0.8133 |
| **natively trained** (10 epochs) | **0.9300** | **0.9333** |
| converged oracle (labeler) | 1.0 | 1.0 |

## Speed

| measurement | value |
|---|---|
| inference latency (`infer`, full process spawn incl. parse) | 2.78 ms/call (1000 calls in 2.78s) |
| native training, 400 scenes x 10 epochs + 11 evals | 0.04s |
| full verification gate (`verify_gist.sh`: all runtime jobs + contract) | 0.15s |

## Reference experiments (construction-tier, code not shipped)

A gradient-trained full hybrid (recurrent state-space x SO(2) convolution
x openness gating x ternary bottleneck x ladder pooling; 109 parameters)
reached 0.984 slot / 0.868 global-verdict accuracy on 64-slot scenes with
27/27 native-inference parity; quoted from the paper, harness kept out of
this repository by the CDC-only constraint.

## Machine

```
Darwin 27.0.0 arm64
Apple clang version 17.0.0 (clang-1700.6.3.2)
Apple M4
```
