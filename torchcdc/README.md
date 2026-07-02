# torchcdc — the GIST training harness

The training tier of the stack (the *mechanism* is `../native/`; this
directory trains networks that anticipate it, against labels the native C
runtime produces).

- `tensorcdc.py` — numpy reverse-mode autograd sized to the calculus
  (SO(2) mixing, Kuramoto ops, straight-through ternary quantizer, Adam).
- `hybrid.py` — **GistHybrid**: recurrent nonlinear state-space core ×
  convolutional filtration (weight-shared corefold pyramid + Hamming-1
  hypercube lattice convolution) × learnable openness gating ×
  balanced-ternary bottleneck × ladder pooling. `init_calculus()` starts
  at the provably-equivalent GIST-NN point.
- `data.py` — scenes compile to `.cdc`; the **BiDi runtime labels them**
  (mass-weighted pyramid compilation; mirror rule for negatives).
- `train.py` — the full protocol: early stopping decides the rounds,
  ablations, majority baselines, native `.cdc` export, 27/27 parity check.
- `test_torchcdc.py` — the battery (10 tests).

```bash
python3 train.py          # full protocol -> build/RESULTS.md (~6 min CPU)
python3 test_torchcdc.py  # the battery (~3 s + short training runs)
```

Headline results (numpy, single CPU; see `build/RESULTS.md`):
64-slot full hybrid slot accuracy **0.984** (from 0.785 at calculus init),
global verdict **0.868**, deployment export **27/27 native parity**.
