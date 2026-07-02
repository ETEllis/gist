# QUARANTINED — construction oracle only, not the product

Nothing in this directory ships. The GIST deliverable is `../native/`
(pure `.cdc`, executed by BiDi's existing C runtime + `cdc_boot.py`,
host-debt 0).

This Python tree exists solely as the construction oracle: its parity
tests reproduce the BiDi native-runtime witness values exactly, which is
how the expectations baked into the native `.cdc` files were computed and
cross-checked. It may be consulted or deleted; it must not grow.

Hard project constraint (2026-07-02): **all new GIST capability is written
as `.cdc` clauses run by the existing BiDi runtimes — zero new Python.**
