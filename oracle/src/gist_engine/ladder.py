"""The meta-gate ladder: 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1.

The ladder is the nest operator (bidiγΔ) iterated over the six dyadic address
bits. Round k pairs every surviving node with its Hamming-1 partner on bit k
(partner = address XOR 2^k), fuses the pair into a parent node, and commits
the parent under the same guards as any commit. Six rounds consume the six
bits; the last node standing is the root synthesis.

Because addresses are the bridge64 dyadic words, the bit order is semantic:
bits 0,1 (LSB) are the two bits of axis q3, bits 2,3 of q2, bits 4,5 of q1 -
so the ladder reconciles the evidence-type axis first, then abstraction, then
temporal (with the default axis labelling).

Fusion is pure calculus:

  read cone   parent read cell i = interfere(A.write[i], gate-aligned
              B.write[i]) - the two children's syntheses superpose, with B
              rotated into A's reference frame by the circular-mean phase
              delta of their write cones (the angled bidiγΔ transfer);
  write cone  the corefold pyramid 3 -> 2 -> 1 of the fused read cone;
  belief      up-cone: mean child coherence enters the parent belief;
  prior       superposition-weighted mean of child priors.

The ladder tree IS the Merkle tree: each leaf hash covers a slot's commit
record; each parent hash covers the pair fusion record plus its children's
hashes. Verifying the released root hash therefore verifies the entire
reduction - the proof structure and the reasoning structure are the same
object.

If a pair's commit is held, the round is retried on the remaining unconsumed
bits (deterministic order). If every bit ordering holds, the engine falls
back to repair-mode commits (the prose-spec barrier semantics) and records a
visible `repair` in the ledger - VDR made mechanical: nothing is silently
forced, everything is attributed.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field

from .algebra import (
    coherence_delta,
    corefold_2_to_1,
    corefold_3_to_2,
    interfere,
    kappa,
    phase,
    phase_order,
    rotate,
)
from .crypto import merkle_leaf, merkle_node
from .field import Cell, Field, Module
from .walks import classify, to_word


@dataclass
class LadderNode:
    name: str
    address: int              # address within the round's shrinking space
    bits: int                 # remaining address bits
    module: Module
    hash: str
    children: tuple[str, str] | None = None
    commit_status: str = "leaf"
    commit_reason: str = "none"
    word: str = ""
    tier: str = ""
    coherence_delta: float = 0.0

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "address": self.address,
            "bits": self.bits,
            "hash": self.hash,
            "children": list(self.children) if self.children else None,
            "commit_status": self.commit_status,
            "commit_reason": self.commit_reason,
            "word": self.word,
            "tier": self.tier,
            "coherence_delta": round(self.coherence_delta, 6),
        }


@dataclass
class LadderRound:
    round_index: int
    bit: int
    nodes: list[LadderNode]
    root: str
    holds: int
    repairs: int

    def to_json(self) -> dict:
        return {
            "round": self.round_index,
            "bit": self.bit,
            "nodes": [n.to_json() for n in self.nodes],
            "merkle_root": self.root,
            "holds": self.holds,
            "repairs": self.repairs,
        }


@dataclass
class LadderResult:
    rounds: list[LadderRound] = dc_field(default_factory=list)
    root_node: LadderNode | None = None
    round_roots: list[str] = dc_field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "rounds": [r.to_json() for r in self.rounds],
            "root": self.root_node.to_json() if self.root_node else None,
            "round_roots": self.round_roots,
        }


def _mean_phase_delta(a_vals: list, b_vals: list) -> float:
    """Circular-mean phase difference between two cone vectors (B's frame vs A's)."""
    acc = 0j
    for va, vb in zip(a_vals, b_vals):
        if abs(va) > 0.0 and abs(vb) > 0.0:
            # unit rotor carrying vb's phase onto va's
            acc += rotate(phase(va) - phase(vb), 1.0 + 0j)
    if abs(acc) == 0.0:
        return 0.0
    return phase(acc)


def fuse_pair(
    parent_name: str,
    a: Module,
    b: Module,
) -> tuple[Module, float]:
    """Fuse two nodes into a parent module (the bidiγΔ pair reduction).

    Returns (parent_module, coherence_delta) where coherence_delta is the
    signed phase mismatch between the two children's syntheses before
    alignment - the γΔ the fusion had to absorb.
    """
    a_write = a.write_values()
    b_write = b.write_values()
    alpha = _mean_phase_delta(a_write, b_write)
    gamma_delta = coherence_delta(
        interfere(*a_write) if a_write else 0j,
        interfere(*b_write) if b_write else 0j,
    )

    read_vals = []
    for va, vb in zip(a_write, b_write):
        read_vals.append(interfere(va, rotate(alpha, vb)) / 2.0)
    dyad = corefold_3_to_2(read_vals)
    singular = corefold_2_to_1(dyad)
    cells = [
        Cell(theta=phase(v), amp=abs(v)) for v in read_vals
    ] + [
        Cell(theta=phase(dyad[0]), amp=abs(dyad[0])),
        Cell(theta=phase(singular), amp=abs(singular)),
        Cell(theta=phase(dyad[1]), amp=abs(dyad[1])),
    ]
    # up-cone: mean child coherence enters the parent belief
    child_kappas = [kappa(v) for v in a_write + b_write if abs(v) > 0.0]
    belief = sum(child_kappas) / len(child_kappas) if child_kappas else 0.0
    mass_a = sum(abs(v) for v in a_write)
    mass_b = sum(abs(v) for v in b_write)
    total = mass_a + mass_b
    prior = (
        (a.prior * mass_a + b.prior * mass_b) / total if total > 0.0
        else (a.prior + b.prior) / 2.0
    )
    parent = Module(
        name=parent_name,
        cells=cells,
        belief=belief,
        prior=prior,
        precision=(a.precision + b.precision) / 2.0,
        action_gain=(a.action_gain + b.action_gain) / 2.0,
    )
    return parent, gamma_delta


def run_ladder(
    leaf_modules: dict[int, Module],
    leaf_hashes: dict[int, str],
    field_params: Field,
    flow_duration: float = 0.5,
) -> LadderResult:
    """Execute the six-round reduction over the 64 leaves.

    `leaf_modules` maps slot index -> committed slot module (copies are made;
    the live field is not mutated). `leaf_hashes` maps slot index -> the
    slot's ledger commit hash (Merkle leaf material).
    """
    result = LadderResult()

    # working set: address -> (node_name, module, hash)
    current: dict[int, LadderNode] = {}
    for addr in range(64):
        m = leaf_modules[addr].copy()
        current[addr] = LadderNode(
            name=f"L0/{addr:06b}",
            address=addr,
            bits=6,
            module=m,
            hash=leaf_hashes[addr],
            word=to_word(m.latched_word()),
            tier=classify(m.latched_word()),
        )

    # Each round re-packs the address space, so pairing bits are indices in
    # the *current* space. Bit 0 (LSB) first preserves the original axis
    # order: rounds fuse the fine bit of axis 3 upward to the coarse bit of
    # axis 1. If a bit's round holds anywhere, alternate bits are tried
    # deterministically (VDR swap_pairing); if all hold, the round runs in
    # repair mode on bit 0 with the repair visible in the ledger.
    for round_index in range(6):
        n_bits = 6 - round_index
        chosen = None
        for bit in range(n_bits):
            trial = _reduce_round(current, bit, n_bits, field_params,
                                  flow_duration, barrier="hold",
                                  round_index=round_index)
            assert trial is not None
            if trial[1].holds == 0:
                chosen = trial
                break
        if chosen is None:
            chosen = _reduce_round(current, 0, n_bits, field_params,
                                   flow_duration, barrier="repair",
                                   round_index=round_index)
            assert chosen is not None
        next_nodes, round_record = chosen
        result.rounds.append(round_record)
        result.round_roots.append(round_record.root)
        current = next_nodes

    assert len(current) == 1
    result.root_node = next(iter(current.values()))
    return result


def _reduce_round(
    current: dict[int, LadderNode],
    bit: int,
    n_bits: int,
    field_params: Field,
    flow_duration: float,
    barrier: str,
    round_index: int,
) -> tuple[dict[int, LadderNode], LadderRound] | None:
    """One Hamming-1 pairing round on `bit`. Returns None if bit >= n_bits."""
    if bit >= n_bits:
        return None
    mask = 1 << bit
    pairs: list[tuple[int, int]] = []
    for addr in sorted(current):
        partner = addr ^ mask
        if addr < partner and partner in current:
            pairs.append((addr, partner))
    next_nodes: dict[int, LadderNode] = {}
    round_nodes: list[LadderNode] = []
    holds = 0
    repairs = 0

    for lo, hi in pairs:
        a_node, b_node = current[lo], current[hi]
        # collapse the consumed bit out of the address
        low_part = lo & (mask - 1)
        high_part = (lo >> (bit + 1)) << bit
        new_addr = high_part | low_part
        parent_name = f"L{7 - n_bits}/{new_addr:0{max(1, n_bits - 1)}b}"
        parent, gamma_delta = fuse_pair(parent_name, a_node.module, b_node.module)

        # commit the fused node under the standard guards in a scratch field
        scratch = Field(
            name=f"ladder-r{round_index}",
            dt=field_params.dt,
            gain=field_params.gain,
            deadband=field_params.deadband,
            snap=field_params.snap,
            belief_gain=field_params.belief_gain,
        )
        scratch.add_module(parent)
        scratch.flow(flow_duration)
        commit = scratch.commit(parent.name, barrier=barrier)
        # only invariant-violating holds block a round; a deadband-jitter
        # hold means "nothing decisive to commit" (e.g. fusing void scopes)
        if commit.status == "held" and commit.reason != "deadband-jitter":
            holds += 1
        if commit.repaired_cells:
            repairs += 1
        committed_module = scratch.modules[parent.name]

        node_hash = merkle_node(a_node.hash, b_node.hash)
        node = LadderNode(
            name=parent_name,
            address=new_addr,
            bits=n_bits - 1,
            module=committed_module,
            hash=node_hash,
            children=(a_node.name, b_node.name),
            commit_status=commit.status,
            commit_reason=commit.reason,
            word=commit.word,
            tier=classify(commit.trits),
            coherence_delta=gamma_delta,
        )
        next_nodes[new_addr] = node
        round_nodes.append(node)

    # round Merkle root over the new nodes' hashes (address order)
    from .crypto import merkle_root as _root
    root = _root([next_nodes[a].hash for a in sorted(next_nodes)])
    record = LadderRound(
        round_index=round_index,
        bit=bit,
        nodes=round_nodes,
        root=root,
        holds=holds,
        repairs=repairs,
    )
    return next_nodes, record
