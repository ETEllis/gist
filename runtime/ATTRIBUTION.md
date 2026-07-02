# Vendored BiDi runtime (the bootstrap GIST rides on)

These four files are the BiDi Coherence-Delta Calculus micro-bridge,
vendored from https://github.com/ETEllis/bidi-coherence-delta-calculus
(MIT license) so this repository is runnable out of the box:

- `cdc_native_runtime.c` / `cdc_source.c` / `cdc_source.h` - the C native
  runtime, **extended here** with (i) native Hebbian plasticity
  (`plastic=1 rate=r` channels; weights follow phase correlation through
  flow) and (ii) the `infer` command (load a weights `.cdc`, feed a ternary
  input word, get the committed verdict). The extension is slated for
  upstreaming to the BiDi repository.
- `cdc_boot.py` - BiDi's single Python bootloader (loader/checker only).

GIST adds no host code of its own on top of this bridge: host-debt 0.
