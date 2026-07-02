"""The native contract verifier: gist.cdc witnesses run as live checks.

Every `witness ... check=<name>` directive in gist.cdc names a function in
REGISTRY below. `verify_contract()` parses the contract, runs every named
check, and validates the `expect` predicates - so the engine's semantic
claims stay declared in the calculus's source language and stay executable.
"""

from __future__ import annotations

import math
import tempfile
from pathlib import Path
from typing import Callable

from . import cdcread
from .algebra import (
    VOID,
    coh,
    corefold_3_to_2,
    gate,
    gate_identity,
    gate_inverse,
    interfere,
    rotate,
)
from .bridge import generate_codebook, project_trits, verify_bijection
from .crypto import decision_stamp, merkle_node, session_key
from .field import Cell, Channel, Field, Module
from .ledger import Ledger
from .walks import CDC_N6_SPECTRUM, census, from_word, is_admissible

Check = Callable[[], tuple[bool, str]]
REGISTRY: dict[str, Check] = {}


def check(name: str) -> Callable[[Check], Check]:
    def deco(fn: Check) -> Check:
        REGISTRY[name] = fn
        return fn
    return deco


def _close(a: complex, b: complex, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


# -- algebra laws -------------------------------------------------------------


@check("algebra_gate_abelian")
def algebra_gate_abelian() -> tuple[bool, str]:
    a, b, c = (0.5, -1.2, 3.0), (1.0, 2.0, -0.7), (-2.5, 0.1, 0.9)
    ok = all(
        abs(x - y) < 1e-12
        for x, y in zip(gate(gate(a, b), c), gate(a, gate(b, c)))
    )
    ok &= all(abs(x - y) < 1e-12 for x, y in zip(gate(a, b), gate(b, a)))
    ok &= all(abs(x - y) < 1e-12 for x, y in zip(gate(a, gate_identity(3)), a))
    ok &= all(abs(math.sin(x)) < 1e-12 for x in gate(a, gate_inverse(a)))
    return ok, "associative, commutative, identity, inverse"


@check("algebra_interfere_monoid")
def algebra_interfere_monoid() -> tuple[bool, str]:
    x, y, z = coh(1, 0.3), coh(0.5, 2.0), coh(2, -1.2)
    ok = _close(interfere(interfere(x, y), z), interfere(x, interfere(y, z)))
    ok &= _close(interfere(x, y), interfere(y, x))
    ok &= _close(interfere(x, VOID), x)
    return ok, "associative, commutative, void unit"


@check("algebra_rotation_linear")
def algebra_rotation_linear() -> tuple[bool, str]:
    x, y = coh(1, 0.4), coh(0.7, -0.9)
    ok = _close(rotate(1.1, interfere(x, y)),
                interfere(rotate(1.1, x), rotate(1.1, y)))
    return ok, "rotation distributes over superposition"


@check("algebra_corefold_morphism")
def algebra_corefold_morphism() -> tuple[bool, str]:
    t1 = (coh(1, 0.2), coh(1, 1.0), coh(1, -0.5))
    t2 = (coh(0.5, 2.0), coh(2, 0.0), coh(1, 3.0))
    summed = tuple(a + b for a, b in zip(t1, t2))
    lin = all(
        _close(x, y)
        for x, y in zip(
            corefold_3_to_2(summed),
            tuple(a + b for a, b in zip(corefold_3_to_2(t1), corefold_3_to_2(t2))),
        )
    )
    rot = all(
        _close(x, y)
        for x, y in zip(
            corefold_3_to_2(tuple(rotate(0.8, v) for v in t1)),
            tuple(rotate(0.8, v) for v in corefold_3_to_2(t1)),
        )
    )
    return lin and rot, "linear and rotation-equivariant"


# -- finite spectrum and bridge -----------------------------------------------


@check("census_n6")
def census_n6() -> tuple[bool, str]:
    got = census(6)
    return got == CDC_N6_SPECTRUM, f"census(6) = {got}"


@check("bridge_bijection")
def bridge_bijection() -> tuple[bool, str]:
    rows = generate_codebook(6)
    return (len(rows) == 64 and verify_bijection(rows)), "64 rows, bijective"


@check("bridge_trit_projection")
def bridge_trit_projection() -> tuple[bool, str]:
    row = project_trits(from_word("+0-+0-"))
    ok = row.dyadic == "101101" and row.triadic == "231" and row.index == 45
    return ok, f"+0-+0- -> {row.dyadic}/{row.triadic}/{row.index}"


# -- native reducer parity ----------------------------------------------------


def _native_field() -> Field:
    f = Field(name="reducer-field", dt=0.125, gain=1.0, deadband=0.5)
    f.add_module(Module(name="council", cells=[
        Cell(theta=math.pi / 2), Cell(theta=0.0), Cell(theta=math.pi)]))
    f.add_module(Module(name="child", cells=[
        Cell(theta=0.0), Cell(theta=0.0), Cell(theta=math.pi / 2)],
        parent="council"))
    f.add_module(Module(name="holdcase", cells=[
        Cell(theta=math.pi), Cell(theta=0.0), Cell(theta=math.pi / 2)]))
    f.add_channel(Channel(src="council:0", dst="council:1", weight=0.25))
    return f


@check("native_flow_parity")
def native_flow_parity() -> tuple[bool, str]:
    f = _native_field()
    f.flow(1.0, frozen=True)
    theta = f.modules["council"].cells[1].theta
    return abs(theta - 0.25) < 1e-6, f"council.b theta = {theta:.9f}"


@check("native_commit_parity")
def native_commit_parity() -> tuple[bool, str]:
    f = _native_field()
    r = f.commit("council")
    ok = r.word == "0+-" and r.status == "accepted" and r.reason == "none"
    return ok, f"{r.word} {r.status}:{r.reason}"


@check("native_hold_parity")
def native_hold_parity() -> tuple[bool, str]:
    f = _native_field()
    r = f.commit("holdcase")
    ok = (r.word == "-+0" and r.status == "held"
          and r.reason == "balance-violation" and r.violation_cell == 0)
    return ok, f"{r.word} {r.status}:{r.reason} cell={r.violation_cell}"


@check("native_nest_parity")
def native_nest_parity() -> tuple[bool, str]:
    f = _native_field()
    belief, prior = f.nest("council", "child")
    ok = abs(belief - 2 / 3) < 1e-6 and abs(prior - 2 / 3) < 1e-6
    return ok, f"parent belief={belief:.6f} child prior={prior:.6f}"


# -- reduction laws -----------------------------------------------------------


@check("commit_soundness")
def commit_soundness() -> tuple[bool, str]:
    thetas = [0.1, 0.45, 1.2, 2.0, 2.9, 0.7, 1.57, 3.1]
    for i in range(6):
        f = Field(name="s", deadband=0.5)
        cells = [Cell(theta=thetas[(i + j) % len(thetas)], amp=1.0)
                 for j in range(6)]
        f.add_module(Module(name="m", cells=cells))
        r = f.commit("m")
        if r.accepted and r.phi_after > r.phi_before + 1e-9:
            return False, f"accepted commit raised phi at sample {i}"
    return True, "no accepted commit raised phi over samples"


@check("barrier_preservation")
def barrier_preservation() -> tuple[bool, str]:
    for word, thetas in [
        ("-+0", (math.pi, 0.0, math.pi / 2)),
        ("--+", (math.pi, math.pi, 0.0)),
    ]:
        f = Field(name="s", deadband=0.5)
        f.add_module(Module(name="m", cells=[Cell(theta=t) for t in thetas]))
        r = f.commit("m")
        if is_admissible(from_word(word)):
            return False, "test word unexpectedly admissible"
        if r.status != "held" or r.reason != "balance-violation":
            return False, f"{word} not held ({r.status}:{r.reason})"
        if r.violation_cell is None:
            return False, "no attribution"
    return True, "violations held with exact cell attribution"


@check("ternary_carrier")
def ternary_carrier() -> tuple[bool, str]:
    f = Field(name="s", deadband=0.5)
    f.add_module(Module(name="m", cells=[
        Cell(theta=t) for t in (0.0, math.pi / 2, 0.3, 2.8, 1.4, 0.1)]))
    r = f.commit("m")
    ok = all(t in (-1, 0, 1) for t in r.trits)
    return ok, f"committed word {r.word}"


@check("local_confluence")
def local_confluence() -> tuple[bool, str]:
    def build() -> Field:
        f = Field(name="c", deadband=0.5)
        f.add_module(Module(name="a", cells=[Cell(theta=0.0), Cell(theta=1.57)]))
        f.add_module(Module(name="b", cells=[Cell(theta=0.2), Cell(theta=3.1)]))
        return f

    f1, f2 = build(), build()
    f1.commit("a"); f1.commit("b")
    f2.commit("b"); f2.commit("a")
    s1 = [(c.theta, c.sigma) for m in f1.modules.values() for c in m.cells]
    s2 = [(c.theta, c.sigma) for m in f2.modules.values() for c in m.cells]
    return s1 == s2, "disjoint commit orders agree"


@check("flow_additivity")
def flow_additivity() -> tuple[bool, str]:
    f1, f2 = _native_field(), _native_field()
    f1.flow(0.5); f1.flow(0.5)
    f2.flow(1.0)
    t1 = f1.modules["council"].cells[1].theta
    t2 = f2.modules["council"].cells[1].theta
    return abs(t1 - t2) < 1e-9, f"{t1:.9f} vs {t2:.9f}"


@check("trace_passive")
def trace_passive() -> tuple[bool, str]:
    f = _native_field()
    before = [(c.theta, c.amp, c.sigma)
              for m in f.modules.values() for c in m.cells]
    _ = f.trace_trits()
    after = [(c.theta, c.amp, c.sigma)
             for m in f.modules.values() for c in m.cells]
    return before == after, "trace read left state unchanged"


# -- ledger / ladder / engine -------------------------------------------------


@check("ledger_chain")
def ledger_chain() -> tuple[bool, str]:
    led = Ledger()
    led.append("a", {"x": 1})
    led.append("b", {"y": 2})
    ok = led.verify_chain()
    led.entries[0].payload["x"] = 9
    ok &= not led.verify_chain()
    return ok, "chain verifies and detects mutation"


def _demo_engine(session_id: str, ledger_path=None):
    from .democorpus import PROMPT, build_corpus, drive
    from .engine import GistEngine

    engine = GistEngine(prompt=PROMPT, session_id=session_id,
                        ledger_path=ledger_path)
    initial, reserve = build_corpus()
    engine.ingest(initial)
    release = drive(engine, reserve)
    return engine, release


@check("ladder_merkle")
def ladder_merkle() -> tuple[bool, str]:
    engine, release = _demo_engine("contract-ladder")
    if release is None or engine.ladder_result is None:
        return False, "no release/ladder"
    leaf_hashes = engine._leaf_hashes()
    r0 = engine.ladder_result.rounds[0]
    for node in r0.nodes:
        a = int(node.children[0].split("/")[1], 2)
        b = int(node.children[1].split("/")[1], 2)
        if node.hash != merkle_node(leaf_hashes[a], leaf_hashes[b]):
            return False, f"hash mismatch at {node.name}"
    return True, "round-0 node hashes equal merkle of children"


@check("replay_determinism")
def replay_determinism() -> tuple[bool, str]:
    e1, r1 = _demo_engine("contract-det")
    e2, r2 = _demo_engine("contract-det")
    if r1 is None or r2 is None:
        return False, "no release"
    s1 = [(e.kind, e.payload) for e in e1.ledger]
    s2 = [(e.kind, e.payload) for e in e2.ledger]
    ok = s1 == s2 and r1["stamp"] == r2["stamp"]
    return ok, f"streams equal ({len(s1)} events), stamps equal"


@check("release_normal_form")
def release_normal_form() -> tuple[bool, str]:
    engine, release = _demo_engine("contract-nf")
    if release is None:
        return False, "no release"
    for slot in release["gate"]["contributing"]:
        if not is_admissible(engine.slots[slot].last_word):
            return False, f"slot {slot} word inadmissible"
    return True, f"tier={release['tier']} all contributing words admissible"


@check("council_coordinate")
def council_coordinate() -> tuple[bool, str]:
    engine, release = _demo_engine("contract-council")
    if release is None:
        return False, "no release"
    recon = engine.ledger.last_of_kind("reconciliation").payload
    member = from_word(recon["meta_word"] + recon["aggregate_word"])
    row = project_trits(member)
    ok = (row.dyadic == recon["coordinate"]["dyadic"]
          and row.triadic == recon["coordinate"]["triadic"])
    return ok, f"{recon['meta_word']}+{recon['aggregate_word']} -> {row.dyadic}/{row.triadic}"


@check("openness_intent")
def openness_intent() -> tuple[bool, str]:
    engine, release = _demo_engine("contract-open")
    kinds = [e.kind for e in engine.ledger]
    ok = "retrieval_intent" in kinds and "slot_saturated" in kinds
    return ok, "intents emitted and slots saturated in the demo session"


@check("stamp_binding")
def stamp_binding() -> tuple[bool, str]:
    k1 = session_key("question A", "s1")
    k2 = session_key("question B", "s1")
    s1 = decision_stamp(k1, "r" * 64, ["x" * 64], "111111", "h" * 64)
    s1b = decision_stamp(k1, "r" * 64, ["x" * 64], "111111", "h" * 64)
    s2 = decision_stamp(k2, "r" * 64, ["x" * 64], "111111", "h" * 64)
    return (s1 == s1b and s1 != s2), "recomputable, prompt-bound"


@check("lattice_shape")
def lattice_shape() -> tuple[bool, str]:
    from .engine import GistEngine

    engine = GistEngine(prompt="shape", session_id="contract-shape")
    ok = len(engine.field.modules) == 64
    ok &= all(len(m.cells) == 6 for m in engine.field.modules.values())
    ok &= len(engine.field.channels) == 64 * 6
    return ok, "64 slots x 6 cells, 6 pyramid channels each"


@check("ports_standalone")
def ports_standalone() -> tuple[bool, str]:
    from .ports import Atom, HashProjector

    p = HashProjector()
    a1 = p.project(Atom(content="same content"))
    a2 = p.project(Atom(content="same content"))
    ok = (a1.slot, a1.polarity, a1.salience) == (a2.slot, a2.polarity, a2.salience)
    ok &= 0 <= a1.slot < 64 and -1 <= a1.polarity <= 1 and 0 <= a1.salience <= 1
    return ok, f"deterministic projection to slot {a1.slot}"


@check("pipeline_e2e")
def pipeline_e2e() -> tuple[bool, str]:
    from .engine import verify_ledger

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "ledger.jsonl"
        engine, release = _demo_engine("contract-e2e", ledger_path=path)
        if release is None:
            return False, "no release"
        report = verify_ledger(path)
        ok = report["verified"] and len(release["stamp"]) == 64
        return ok, (f"released tier={release['tier']}, replay "
                    f"{'verified' if report['verified'] else 'FAILED'}")


@check("frontend_projection")
def frontend_projection() -> tuple[bool, str]:
    engine, release = _demo_engine("contract-fe")
    state = engine.state_json()
    replay = engine.export_replay()
    ok = len(state["board"]) == 64 and state["release"] is not None
    ok &= len(replay["events"]) == len(engine.ledger)
    ok &= replay["final_state"]["ledger_head"] == engine.ledger.head_hash
    return ok, "board and replay bundles complete"


# -- the ternary bridge / variants ---------------------------------------------


def _support_atoms():
    return [
        {"content": "all tests pass", "polarity": 0.92, "salience": 0.9,
         "address": [0, 0, 0]},
        {"content": "golden snapshots match", "polarity": 0.88,
         "salience": 0.85, "address": [0, 0, 0]},
        {"content": "minor style nit", "polarity": -0.4, "salience": 0.3,
         "address": [0, 0, 0]},
    ]


@check("verdict_ternary")
def verdict_ternary() -> tuple[bool, str]:
    from .verdict import verdict

    y = verdict("claim carried", atoms=_support_atoms(), session_id="c-vy")
    m = verdict("claim untested", atoms=[], session_id="c-vm")
    contested = [
        {"content": "strong support", "polarity": 0.9, "salience": 0.9,
         "address": [0, 0, 0]},
        {"content": "strong contradiction", "polarity": -0.9,
         "salience": 0.88, "address": [0, 0, 0]},
    ]
    c = verdict("claim contested", atoms=contested, session_id="c-vc")
    ok = (y.decision, y.trit) == ("yes", 1)
    ok &= (m.decision, m.trit) == ("maybe", 0)
    ok &= (c.decision, c.trit) == ("maybe", 0)
    return ok, f"yes/{y.trit} maybe/{m.trit} maybe/{c.trit}"


@check("verdict_mirror_no")
def verdict_mirror_no() -> tuple[bool, str]:
    from .verdict import verdict

    against = [
        {"content": "integration fails", "polarity": -0.9, "salience": 0.95,
         "address": [0, 0, 0]},
        {"content": "latency regressed", "polarity": -0.85, "salience": 0.9,
         "address": [0, 0, 0]},
        {"content": "one microbenchmark improved", "polarity": 0.35,
         "salience": 0.25, "address": [0, 0, 0]},
    ]
    v = verdict("claim contradicted", atoms=against, session_id="c-vn")
    ok = (v.decision, v.trit) == ("no", -1)
    return ok, f"no via mirror session ({v.basis})"


@check("mcp_surface")
def mcp_surface() -> tuple[bool, str]:
    import json as _json

    from .mcp_server import handle_message

    init = handle_message({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                           "params": {}})
    tools = handle_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    call = handle_message({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "gist_verdict",
                   "arguments": {"claim": "mcp check",
                                 "atoms": _support_atoms()}},
    })
    ok = init["result"]["serverInfo"]["name"] == "gist-engine"
    names = {t["name"] for t in tools["result"]["tools"]}
    ok &= {"gist_verdict", "gist_open", "gist_verify"} <= names
    payload = _json.loads(call["result"]["content"][0]["text"])
    ok &= payload["decision"] == "yes"
    return ok, f"{len(names)} tools; verdict over MCP = {payload['decision']}"


@check("reasonloop_gate")
def reasonloop_gate() -> tuple[bool, str]:
    from .reasonloop import ReasonLoop

    loop = ReasonLoop(prompt="episode", session_id="c-rl")
    fb = loop.feed("exploratory angle", polarity=0.0, salience=0.5,
                   address=(2, 2, 2))
    ok = fb.proceed == "maybe" and fb.trit == 0
    loop.feed("decisive support", polarity=0.9, salience=0.9,
              address=(0, 0, 0))
    loop.feed("more decisive support", polarity=0.88, salience=0.85,
              address=(0, 0, 0))
    block = loop.steering_block()
    ok &= block.startswith("[GIST field") and len(block) < 1200
    v = loop.gate_answer()
    ok &= v.decision in ("yes", "maybe")
    return ok, f"steering block {len(block)} chars; gate={v.decision}"


@check("gate_scope_occupied")
def gate_scope_occupied() -> tuple[bool, str]:
    from .verdict import verdict

    v = verdict("scoped release", atoms=_support_atoms(), session_id="c-gs")
    ok = v.decision == "yes"
    return ok, f"occupied-scope session decided {v.decision} ({v.basis})"


# -- the neural functional form -------------------------------------------------


def _nn_pair():
    from .democorpus import build_corpus
    from .engine import GistEngine
    from .neural import GistNeural

    eng = GistEngine(prompt="nn", session_id="c-nn")
    initial, _ = build_corpus()
    eng.ingest(initial)
    eng.step()
    return eng, GistNeural.from_field(eng.field)


@check("neural_flow_equivalence")
def neural_flow_equivalence() -> tuple[bool, str]:
    eng, nn = _nn_pair()
    eng.field.flow(2.0)
    nn.flow(2.0)
    worst = 0.0
    i = 0
    for m in eng.field.modules.values():
        for cell in m.cells:
            worst = max(worst, abs(cell.theta - nn.theta[i]),
                        abs(cell.amp - nn.amp[i]))
            i += 1
    return worst < 1e-9, f"max state divergence {worst:.2e} over {i} cells"


@check("neural_commit_equivalence")
def neural_commit_equivalence() -> tuple[bool, str]:
    from .neural import GistNeural

    f = _native_field()
    nn = GistNeural.from_field(f)
    head = nn.commit_head("holdcase")
    r = f.commit("holdcase")
    ok = (list(r.trits) == head["trits"]
          and r.violation_cell == head["violation_cell"]
          and not head["admissible"])
    return ok, f"holdcase head {head['trits']} violation={head['violation_cell']}"


@check("neural_weight_roundtrip")
def neural_weight_roundtrip() -> tuple[bool, str]:
    from .neural import GistNeural

    _eng, nn = _nn_pair()
    nn2 = GistNeural.loads(nn.dumps())
    nn.flow(1.0)
    nn2.flow(1.0)
    worst = max(
        (abs(a - b) for a, b in zip(nn.theta, nn2.theta)), default=0.0
    )
    return worst < 1e-12, f"roundtrip divergence {worst:.2e}"


# -- the verifier -------------------------------------------------------------


def contract_path() -> Path:
    return Path(__file__).with_name("gist.cdc")


def verify_contract(path: str | None = None) -> dict:
    program = cdcread.parse_file(path or contract_path())
    witnesses = program.all("witness")
    results = []
    passed = 0
    seen: dict[str, bool] = {}
    for w in witnesses:
        check_name = w.get("check")
        claim = w.get("claim", "")
        if check_name is None or check_name not in REGISTRY:
            results.append({"witness": w.key, "claim": claim,
                            "passed": False,
                            "detail": f"no live check {check_name!r}"})
            seen[w.key or ""] = False
            continue
        ok, detail = REGISTRY[check_name]()
        results.append({"witness": w.key, "claim": claim,
                        "passed": ok, "detail": detail})
        seen[w.key or ""] = ok
        if ok:
            passed += 1

    # expectations
    counts = {
        "terms": sum(len(d.args) for d in program.all("term")),
        "rules": sum(len(d.args) for d in program.all("rule")),
        "invariants": len(program.all("invariant")),
        "capabilities": len(program.all("capability")),
        "witnesses": len(witnesses),
    }
    expectations_ok = True
    for ex in program.expects():
        if not ex:
            continue
        if ex[0] == "witness" and len(ex) >= 2:
            if not seen.get(ex[1], False):
                expectations_ok = False
        elif len(ex) >= 3 and ex[1] in (">=", "==", "<="):
            key, op, val = ex[0], ex[1], ex[2]
            if key in counts:
                n, v = counts[key], int(val)
                if not ((op == ">=" and n >= v) or (op == "==" and n == v)
                        or (op == "<=" and n <= v)):
                    expectations_ok = False
        elif len(ex) >= 4 and ex[0] == "native" and ex[2] == "==":
            kernel = program.all("kernel")
            target = kernel[0].get("target") if kernel else None
            if target != ex[3]:
                expectations_ok = False

    verified = passed == len(witnesses) and expectations_ok
    return {
        "verified": verified,
        "passed": passed,
        "total": len(witnesses),
        "expectations_ok": expectations_ok,
        "counts": counts,
        "checks": results,
    }
