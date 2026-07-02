# GistHybrid training results (native-labeled)

Labeler: **BiDi `cdc_native_runtime`** (every label is a committed
word of the actual mechanism; mirror rule for negatives).
Protocol: Adam lr 0.02, batch 64, early stopping patience 8 (max 60).

## Primary - full hybrid, 64-slot lattice (109 params)

| metric | untrained (calculus-init) | trained |
|---|---|---|
| slot accuracy | 0.785 | **0.9841** |
| slot macro-F1 | 0.6436 | **0.9802** |
| global verdict accuracy | 0.54 | **0.868** |

Training rounds (early stopping): **46 epochs**. Majority baselines: slot 0.6613, global 0.532.

Global verdict confusion (rows = truth no/maybe/yes):

```
[[ 45  12   0]
 [  5 124   4]
 [  0  12  48]]
```

## Ablations (8-slot lattice)

| variant | slot acc | global acc | epochs |
|---|---|---|---|
| calculus_init | 0.9505 | 0.84 | 48 |
| random_init | 0.9681 | 0.75 | 36 |
| no_lattice | 0.9868 | 0.775 | 28 |
| no_gating | 0.9835 | 0.745 | 47 |
| no_bottleneck | 0.9527 | 0.825 | 44 |

## Deployment (single-slot, C-parity mode)

Trained slot accuracy 0.9846; exported to `gist_hybrid.cdc`;
**native parity 27/27** - the exported `.cdc` reproduces the
trained model's singular trit under `cdc_native_runtime infer` on every one
of the 27 ternary input words.

Wall time: 351.5s (single CPU, numpy).
