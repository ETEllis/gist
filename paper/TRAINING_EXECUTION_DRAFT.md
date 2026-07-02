# GIST → Weights: Training-Translation Execution Draft

**Status:** pick-up-and-execute plan (a document, not code — per the hard
constraint, all executable GIST capability lives in `../native/*.cdc` on
BiDi's runtimes). Model landscape verified live against the Hugging Face
hub on **2026-07-02**. The deliverable this plan trains toward: a local
open-weights LLM that runs the GIST discipline *from its weights* —
scoped decomposition, balanced-ternary commitment with a native "still
open, I need evidence" state, contradiction debt it must repair, and
gate-shaped conclusions — verified during training by the native runtime.

---

## 1 · The two claims, stated honestly (the frame the plan implements)

**Claim 1 — the chain-of-thought can execute GIST.** Real and defensible.
A model can be trained to decompose into scoped sub-claims, gather
evidence per scope, run counterfactual-survival checks on load-bearing
claims, and refuse to conclude until coverage and agreement hold — with
the balanced-ternary `0` giving it a first-class open state instead of
confabulation.

**Claim 2 — "living in the weights," split in two.** *Behavioral
internalization* is real: train on verified GIST traces (SFT) with the
gate as the RL reward, and the model learns to anticipate what the gate
will accept — the discipline present at inference with no engine in the
loop. The stronger reading — that the transformer's forward pass literally
runs balanced-ternary commits in its activations — is **not claimed**; it
is an interpretability bet (homologous internal structure), not a promise.

**The sharp form:** GIST is the **training-time verifier and the output
grammar**, not an inference-time engine. Pay the gate cost during
training; inference gets the behavior free; spin up the full native
machinery only for high-stakes releases.

## 2 · Stage 0 — the trace flywheel (the verifier is a C runtime)

The generator and the reward function already exist and cost microseconds:

- **Generate:** procedurally emit `.cdc` scenario files in the exact shape
  of `gist_pyramid.cdc` / `gist_cf.cdc` / `gist_cf2.cdc` (vary cell
  phases, weights, topologies over the six-cell slot; sweep the 64-slot
  addresses of `gist_lattice.cdc`), run them through
  `cdc_native_runtime run|prove|surface|council`, and harvest the checked
  outputs: flow trajectories, commit words with accepted/held+reason,
  nest exchanges, gate/bridge coordinates, council decisions.
- **Serialize** each run as a natural-language trace paired with its
  ledger-style skeleton: *question → scoped claims (slot addresses) →
  evidence stances (+/0/−, salience) → committed words → verdict
  (yes/no/maybe) → asks/repairs*. Every trace is replay-verifiable by
  re-running its `.cdc`.
- **Scale:** 50k–200k traces; stratify by outcome (accepted / held with
  balance-violation / contested-open / mirror-negative) and by the T5
  tier census (729/267/51/20/5) so the model sees the whole spectrum,
  especially the `0`-state and the veto.

## 3 · Stage 1 — SFT (the grammar and the 0-state)

Fine-tune on the traces so the model *speaks* GIST: decompose → scope →
stance → commit → ternary verdict, with `maybe` always carrying concrete
asks and `no` always carrying attributed contradictions. Include
adversarial negatives (traces whose conclusions the runtime *held*) with
the repair move as the target continuation. QLoRA is sufficient at this
stage; full-FT only if Stage-2 gains plateau.

## 4 · Stage 2 — RL with the gate as reward

GRPO-style rounds: the model emits a trace for a fresh question; a parser
compiles the trace's skeleton to a `.cdc` scenario; the **native runtime
is the reward function** — accepted commits, admissible words, gate-shaped
conclusions score; balance-violations, unidentified causal claims, and
manufactured verdicts cost. Because the verifier is a compiled C binary
checking exact expectations, reward evaluation is effectively free and
deterministic — no judge model in the loop.

**Routing and curriculum come from the mechanism's own signals:**
escalation-intents (a scope that keeps failing) route those episodes to
the larger model tier or more sampling; openness/aperture states rank
episodes easy → contested → knife-edge (near the counterfactual-survival
ceiling) for curriculum ordering.

**The three deltas, guarded:** (1) *the projector is where truth enters* —
stance/salience labeling is grounded on generated scenarios (ground truth
known) and adversarially perturbed so the model cannot place atoms to
win; (2) *reward hacking* — hold out projector variants and replay-verify
sampled episodes end-to-end each round; the letter of the gate is
structural, which resists gaming, but the projector is the soft underbelly
and gets the audit; (3) *cost* — verification is offline/batched; nothing
GIST-shaped runs at inference except the learned behavior.

## 5 · Model selection (verified on the hub, 2026-07-02)

| Tier | Model | Why | Local footprint |
|---|---|---|---|
| **Primary** | [google/gemma-4-12B-it](https://hf.co/google/gemma-4-12B-it) | Apache-2.0, unified architecture, official QAT w4a16/GGUF, biggest fine-tune ecosystem (unsloth et al.) | QLoRA on 1×24 GB GPU or 32 GB unified Mac; QAT-int4 inference ≈ 8–9 GB |
| Edge ablation | [google/gemma-4-E4B-it](https://hf.co/google/gemma-4-E4B-it) / E2B | tiny effective params, same family — cheap ablations of every training choice | laptop-class |
| MoE efficiency | [google/gemma-4-26B-A4B-it](https://hf.co/google/gemma-4-26B-A4B-it) | 26B quality, ~4B active — the scale-up if 12B gains hold | 1×24–48 GB with QAT |
| Cross-family replication | Qwen3.5-9B (e.g. base of [Ornith-1.0-9B](https://hf.co/deepreinforce-ai/Ornith-1.0-9B)) / [Qwen3.6-27B](https://hf.co/nvidia/Qwen3.6-27B-NVFP4) | proves the effect isn't Gemma-specific; Apache/MIT; NVFP4 quants | 9B ≈ Gemma-12B class |
| MoE runtime alt | Qwen3.5/3.6-35B-A3B ([NVFP4](https://hf.co/nvidia/Qwen3.6-35B-A3B-NVFP4), [AgentWorld tune](https://hf.co/Qwen/Qwen-AgentWorld-35B-A3B)) | ~3B active params; agentic-tuned variants exist | consumer-GPU friendly |
| Teacher / judge-free distill | [GLM-5.2](https://hf.co/zai-org/GLM-5.2) (MIT, [GGUF](https://hf.co/unsloth/GLM-5.2-GGUF)), [DeepSeek-V4-Flash](https://hf.co/deepseek-ai/DeepSeek-V4-Flash) (MIT) | trace-quality bootstrapping and comparison ceilings | inference-only locally |
| Geometry-adjacent exotics | [google/diffusiongemma-26B-A4B-it](https://hf.co/interfaze-ai/diffusion-gemma-asr-small) (the diffusion Gemma — confirmed), [nvidia Nemotron TwoTower-30B-A3B](https://hf.co/nvidia/Nemotron-Labs-TwoTower-30B-A3B) (diffusion + **mamba** hybrid) | the SSM/diffusion cousins of GIST's own geometry — Phase-C research targets, not the workhorse | 30B-A3B class |

**Call:** Phase A = `gemma-4-12B-it` QLoRA (ablate on E4B). Phase B =
replicate on Qwen3.5-9B; scale winner to `26B-A4B`. Phase C (research) =
the TwoTower/diffusiongemma geometry-cousins.

## 6 · Evaluation (the posting-grade protocol)

Same base vs GIST-trained, and each ± the native verifier available as a
tool: (a) rung-2/3 causal items (CLadder-style + the native cf/cf2
scenario families with known ground truth); (b) **refusal correctness**
(does it say `maybe`/`no` exactly when the runtime holds?); (c)
**hallucinated-causation rate**; (d) contested-question calibration (the
`0`-state); (e) trace replay-verification rate (what fraction of its
reasoning parses and passes the runtime). Publish prompts, parser,
scenario generator, and scoring so results are reproducible.

## 7 · Pickup checklist

1. Scenario generator + trace serializer (host-side tooling around the
   native runtime; touches no engine semantics).
2. 50k-trace corpus v0; SFT gemma-4-12B-it (QLoRA, unsloth or MLX).
3. Parser + reward harness (`trace → .cdc → cdc_native_runtime` verdict).
4. 3–5 GRPO rounds with routing/curriculum from escalation + openness.
5. Run §6; compare against base and against tool-augmented base.
6. Scale/replicate per §5; write up.

*Sources (hub, checked 2026-07-02):* [gemma-4 family](https://hf.co/google/gemma-4-12B-it) ·
[gemma-4-26B-A4B-it](https://hf.co/google/gemma-4-26B-A4B-it) ·
[gemma-4-E4B-it](https://hf.co/google/gemma-4-E4B-it) ·
[GLM-5.2](https://hf.co/zai-org/GLM-5.2) ·
[DeepSeek-V4-Flash](https://hf.co/deepseek-ai/DeepSeek-V4-Flash) ·
[Qwen3.6-35B-A3B-NVFP4](https://hf.co/nvidia/Qwen3.6-35B-A3B-NVFP4) ·
[Qwen-AgentWorld-35B-A3B](https://hf.co/Qwen/Qwen-AgentWorld-35B-A3B) ·
[Ornith-1.0-9B](https://hf.co/deepreinforce-ai/Ornith-1.0-9B) ·
[Nemotron TwoTower-30B-A3B](https://hf.co/nvidia/Nemotron-Labs-TwoTower-30B-A3B) ·
[diffusiongemma reference](https://hf.co/interfaze-ai/diffusion-gemma-asr-small)
