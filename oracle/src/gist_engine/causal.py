"""The do-operator layer: full Pearl over the balanced-ternary carrier.

Implements Phase 1 of PROPOSAL_DO_OPERATOR.md, signed off 2026-07-02:

  rung 2   first-class graph surgery (`TernarySCM.do`, `Field.do` in
           field.py), d-separation, the three rules of do-calculus as
           executable side-condition checks, backdoor and frontdoor
           identification with honest refusal, and exact estimation by
           enumeration;
  rung 3   abduction - action - prediction counterfactuals over the exact
           exogenous posterior (the finite ternary carrier makes the
           posterior an enumerable sum, not an approximation), twin-network
           evaluated; probabilities of causation PN / PS / PNS, plus the
           Tian-Pearl bounds for the distribution-only setting.

Everything is exact and deterministic. There is no sampling, no
approximation, and no silent answer: a query the implemented tiers cannot
identify returns `NotIdentifiable` with the reason (the causal analogue of
the commit barrier holding a debt-bearing word). The Shpitser-Pearl ID
algorithm (hedges, napkin-class graphs) is the declared Phase-2 tier.

The SCM family is CDC-native: every mechanism is the calculus's own
quantization applied to a weighted superposition of parent values plus an
exogenous trit,

    v  =  tau_delta( sum_i w_i * pa_i  +  b  +  c * u_v ),

with tau the deadband trit from algebra.py. Exogenous variables u_v are
balanced trits with explicit priors - the discrete image of the cells'
initial phases. Latent confounders are ordinary variables marked
unobserved. Because the carrier is finite, observational joints,
interventional joints, and counterfactual posteriors are all finite sums
over the exogenous configuration space (3^n), computed exactly.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field as dc_field
from itertools import combinations, product
from typing import Any, Callable, Iterable, Mapping, Sequence

from .algebra import DEADBAND_CANONICAL

Trit = int
TRITS: tuple[Trit, ...] = (-1, 0, 1)
Assignment = dict[str, Trit]


def tau(x: float, deadband: float = DEADBAND_CANONICAL) -> Trit:
    """The carrier quantizer (identical rule to algebra.trit on kappa)."""
    if x > deadband:
        return 1
    if x < -deadband:
        return -1
    return 0


# ---------------------------------------------------------------------------
# The structural causal model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Mechanism:
    """v = tau(sum(w_i * pa_i) + b + c * u_v). Roots: v = u_v (w empty, c=1)."""

    parents: tuple[str, ...]
    weights: tuple[float, ...]
    bias: float = 0.0
    noise_gain: float = 1.0

    def evaluate(self, pa: Mapping[str, Trit], u: Trit,
                 deadband: float = DEADBAND_CANONICAL) -> Trit:
        s = self.bias + self.noise_gain * u
        for name, w in zip(self.parents, self.weights):
            s += w * pa[name]
        return tau(s, deadband)


@dataclass
class TernarySCM:
    """A finite structural causal model on the balanced-ternary carrier.

    variables    topologically ordered names;
    mechanisms   name -> Mechanism (roots have no parents);
    noise_priors name -> (P(u=-1), P(u=0), P(u=+1)), summing to 1;
    observed     the measurable subset (everything else is latent).
    interventions: name -> constant trit (graph surgery already applied).
    """

    variables: tuple[str, ...]
    mechanisms: dict[str, Mechanism]
    noise_priors: dict[str, tuple[float, float, float]]
    observed: tuple[str, ...]
    deadband: float = DEADBAND_CANONICAL
    interventions: dict[str, Trit] = dc_field(default_factory=dict)

    # -- structure ----------------------------------------------------------

    def parents(self, v: str) -> tuple[str, ...]:
        if v in self.interventions:
            return ()
        return self.mechanisms[v].parents

    def digraph(self) -> dict[str, tuple[str, ...]]:
        return {v: self.parents(v) for v in self.variables}

    def children(self, v: str) -> tuple[str, ...]:
        return tuple(c for c in self.variables if v in self.parents(c))

    def descendants(self, xs: Iterable[str]) -> set[str]:
        out: set[str] = set()
        frontier = list(xs)
        while frontier:
            node = frontier.pop()
            for c in self.children(node):
                if c not in out:
                    out.add(c)
                    frontier.append(c)
        return out

    def ancestors(self, xs: Iterable[str]) -> set[str]:
        out: set[str] = set()
        frontier = list(xs)
        while frontier:
            node = frontier.pop()
            for p in self.parents(node):
                if p not in out:
                    out.add(p)
                    frontier.append(p)
        return out

    def latents(self) -> tuple[str, ...]:
        obs = set(self.observed)
        return tuple(v for v in self.variables if v not in obs)

    def scm_hash(self) -> str:
        payload = {
            "variables": list(self.variables),
            "mechanisms": {
                v: {
                    "parents": list(m.parents),
                    "weights": list(m.weights),
                    "bias": m.bias,
                    "noise_gain": m.noise_gain,
                }
                for v, m in sorted(self.mechanisms.items())
            },
            "noise_priors": {k: list(v) for k, v in
                             sorted(self.noise_priors.items())},
            "observed": list(self.observed),
            "deadband": self.deadband,
            "interventions": dict(sorted(self.interventions.items())),
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

    # -- surgery (the do-operator, rung 2) ------------------------------------

    def do(self, assignments: Mapping[str, Trit]) -> "TernarySCM":
        """Graph surgery: sever inbound mechanisms, pin constants. Pure."""
        for v in assignments:
            if v not in self.mechanisms:
                raise KeyError(f"unknown variable {v!r}")
        merged = dict(self.interventions)
        merged.update(assignments)
        return TernarySCM(
            variables=self.variables,
            mechanisms=self.mechanisms,
            noise_priors=self.noise_priors,
            observed=self.observed,
            deadband=self.deadband,
            interventions=merged,
        )

    # -- exact evaluation ------------------------------------------------------

    def evaluate(self, u: Mapping[str, Trit]) -> Assignment:
        """Deterministic world given a full exogenous configuration."""
        values: Assignment = {}
        for v in self.variables:
            if v in self.interventions:
                values[v] = self.interventions[v]
            else:
                m = self.mechanisms[v]
                values[v] = m.evaluate(values, u[v], self.deadband)
        return values

    def exogenous_space(self) -> Iterable[tuple[Assignment, float]]:
        """All exogenous configurations with their prior probabilities."""
        names = self.variables
        priors = [self.noise_priors[v] for v in names]
        for combo in product(TRITS, repeat=len(names)):
            p = 1.0
            for t, prior in zip(combo, priors):
                p *= prior[t + 1]
            if p > 0.0:
                yield dict(zip(names, combo)), p

    def joint(self, over: Sequence[str] | None = None) -> dict[tuple, float]:
        """Exact joint distribution over `over` (default: observed vars)."""
        over = tuple(over) if over is not None else self.observed
        dist: dict[tuple, float] = {}
        for u, p in self.exogenous_space():
            world = self.evaluate(u)
            key = tuple(world[v] for v in over)
            dist[key] = dist.get(key, 0.0) + p
        return dist

    def prob(self, event: Mapping[str, Trit],
             given: Mapping[str, Trit] | None = None) -> float:
        """Exact P(event | given) on this (possibly mutilated) model."""
        num = 0.0
        den = 0.0
        for u, p in self.exogenous_space():
            world = self.evaluate(u)
            if given and any(world[k] != v for k, v in given.items()):
                continue
            den += p
            if all(world[k] == v for k, v in event.items()):
                num += p
        if den == 0.0:
            return 0.0
        return num / den


# ---------------------------------------------------------------------------
# d-separation (Bayes-ball on the possibly-mutilated DAG)
# ---------------------------------------------------------------------------


def d_separated(
    scm: TernarySCM,
    xs: Iterable[str],
    ys: Iterable[str],
    zs: Iterable[str] = (),
    remove_in: Iterable[str] = (),
    remove_out: Iterable[str] = (),
) -> bool:
    """Are X and Y d-separated by Z in G with the listed edge surgeries?

    remove_in:  variables whose inbound edges are cut  (the bar, G_X̄);
    remove_out: variables whose outbound edges are cut (the underline, G_Z̲).
    Latent variables participate as ordinary nodes (confounding paths are
    real paths through them).
    """
    xs, ys, zs = set(xs), set(ys), set(zs)
    rin, rout = set(remove_in), set(remove_out)
    parents = {
        v: tuple(p for p in scm.parents(v) if v not in rin and p not in rout)
        for v in scm.variables
    }
    children: dict[str, list[str]] = {v: [] for v in scm.variables}
    for v, ps in parents.items():
        for p in ps:
            children[p].append(v)
    # ancestors of Z (for collider opening)
    z_anc = set(zs)
    frontier = list(zs)
    while frontier:
        node = frontier.pop()
        for p in parents[node]:
            if p not in z_anc:
                z_anc.add(p)
                frontier.append(p)

    # reachability with direction memory: (node, direction) where direction
    # 'up' = arrived from a child (moving against arrows), 'down' = from a
    # parent (moving with arrows)
    visited: set[tuple[str, str]] = set()
    frontier2 = [(x, "up") for x in xs]
    while frontier2:
        node, direction = frontier2.pop()
        if (node, direction) in visited:
            continue
        visited.add((node, direction))
        if node in ys and node not in xs:
            return False
        if direction == "up":
            if node not in zs:
                for p in parents[node]:
                    frontier2.append((p, "up"))
                for c in children[node]:
                    frontier2.append((c, "down"))
        else:  # arrived along an arrow into node
            if node not in zs:
                for c in children[node]:
                    frontier2.append((c, "down"))
            if node in z_anc:  # collider (or its ancestor chain) opened by Z
                for p in parents[node]:
                    frontier2.append((p, "up"))
    return True


# ---------------------------------------------------------------------------
# The three rules of do-calculus (executable side conditions)
# ---------------------------------------------------------------------------


def rule1_deletes_observation(scm: TernarySCM, y: str, z: str,
                              do_x: Iterable[str],
                              given_w: Iterable[str] = ()) -> bool:
    """P(y | do(X), z, w) = P(y | do(X), w)  iff  (Y ⊥ Z | X, W) in G_X̄."""
    x = set(do_x)
    return d_separated(scm, {y}, {z}, x | set(given_w), remove_in=x)


def rule2_exchange_action_observation(scm: TernarySCM, y: str, z: str,
                                      do_x: Iterable[str],
                                      given_w: Iterable[str] = ()) -> bool:
    """P(y | do(X), do(z), w) = P(y | do(X), z, w)
    iff (Y ⊥ Z | X, W) in G_X̄, Z̲."""
    x = set(do_x)
    return d_separated(scm, {y}, {z}, x | set(given_w),
                       remove_in=x, remove_out={z})


def rule3_deletes_action(scm: TernarySCM, y: str, z: str,
                         do_x: Iterable[str],
                         given_w: Iterable[str] = ()) -> bool:
    """P(y | do(X), do(z), w) = P(y | do(X), w)
    iff (Y ⊥ Z | X, W) in G_X̄, Z̄(W), where Z(W) = Z \\ An(W) in G_X̄."""
    x = set(do_x)
    w = set(given_w)
    # ancestors of W in G_X̄
    parents = {v: tuple(p for p in scm.parents(v) if v not in x)
               for v in scm.variables}
    anc_w = set(w)
    frontier = list(w)
    while frontier:
        node = frontier.pop()
        for p in parents[node]:
            if p not in anc_w:
                anc_w.add(p)
                frontier.append(p)
    z_bar = {z} - anc_w
    return d_separated(scm, {y}, {z}, x | w, remove_in=x | z_bar)


# ---------------------------------------------------------------------------
# Identification: backdoor, frontdoor, honest refusal
# ---------------------------------------------------------------------------


class PositivityError(Exception):
    """Identified graphically, but not estimable from observational data:
    an adjustment stratum the formula must condition on carries zero
    probability (the overlap assumption fails). The violating strata are
    attributed - the estimation-layer analogue of the commit barrier."""

    def __init__(self, query: str, strata: list[dict[str, Trit]], ask: str):
        self.query = query
        self.strata = strata
        self.ask = ask
        super().__init__(
            f"{query}: positivity violated in strata {strata}; {ask}"
        )


@dataclass
class Estimand:
    """An identified interventional query with an executable formula."""

    query: str                      # human-readable
    tier: str                       # 'backdoor' | 'frontdoor'
    treatment: str
    outcome: str
    adjustment: tuple[str, ...]     # Z (backdoor) or M (frontdoor)
    derivation: list[str] = dc_field(default_factory=list)

    def positivity_violations(self, scm: TernarySCM,
                              x: Trit) -> list[dict[str, Trit]]:
        """Strata the formula must condition on that carry zero mass.

        backdoor:  every z with P(z) > 0 needs P(X=x, z) > 0;
        frontdoor: every m with P(m | X=x) > 0 and every x' with
                   P(X=x') > 0 needs P(m, X=x') > 0.
        """
        bad: list[dict[str, Trit]] = []
        if self.tier == "backdoor":
            for z_vals in product(TRITS, repeat=len(self.adjustment)):
                z = dict(zip(self.adjustment, z_vals))
                if scm.prob(z) > 0.0:
                    stratum = dict(z)
                    stratum[self.treatment] = x
                    if scm.prob(stratum) == 0.0:
                        bad.append(stratum)
        elif self.tier == "frontdoor":
            if scm.prob({self.treatment: x}) == 0.0:
                bad.append({self.treatment: x})
            for m_vals in product(TRITS, repeat=len(self.adjustment)):
                m = dict(zip(self.adjustment, m_vals))
                if scm.prob({self.treatment: x}) > 0.0 and \
                        scm.prob(m, given={self.treatment: x}) > 0.0:
                    for x_prime in TRITS:
                        if scm.prob({self.treatment: x_prime}) == 0.0:
                            continue
                        stratum = dict(m)
                        stratum[self.treatment] = x_prime
                        if scm.prob(stratum) == 0.0:
                            bad.append(stratum)
        return bad

    def evaluate(self, scm: TernarySCM, x: Trit, y: Trit) -> float:
        """Compute P(Y=y | do(X=x)) from the *observational* model only.

        The estimand touches nothing but conditional/marginal probabilities
        of observed variables on the un-mutilated model - that is the whole
        point of identification. Raises PositivityError (with the violating
        strata attributed) when the overlap assumption fails: graphical
        identification never licenses estimating from strata that carry no
        observational mass.
        """
        violations = self.positivity_violations(scm, x)
        if violations:
            raise PositivityError(
                query=self.query,
                strata=violations,
                ask=(
                    f"collect evidence covering {self.treatment}={x} within "
                    f"those strata (or intervene experimentally)"
                ),
            )
        if self.tier == "backdoor":
            total = 0.0
            for z_vals in product(TRITS, repeat=len(self.adjustment)):
                z = dict(zip(self.adjustment, z_vals))
                pz = scm.prob(z)
                if pz == 0.0:
                    continue
                cond = dict(z)
                cond[self.treatment] = x
                total += scm.prob({self.outcome: y}, given=cond) * pz
            return total
        if self.tier == "frontdoor":
            total = 0.0
            for m_vals in product(TRITS, repeat=len(self.adjustment)):
                m = dict(zip(self.adjustment, m_vals))
                p_m_given_x = scm.prob(m, given={self.treatment: x})
                if p_m_given_x == 0.0:
                    continue
                inner = 0.0
                for x_prime in TRITS:
                    px = scm.prob({self.treatment: x_prime})
                    if px == 0.0:
                        continue
                    cond = dict(m)
                    cond[self.treatment] = x_prime
                    inner += scm.prob({self.outcome: y}, given=cond) * px
                total += p_m_given_x * inner
            return total
        raise ValueError(f"unknown tier {self.tier!r}")

    def to_json(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "tier": self.tier,
            "treatment": self.treatment,
            "outcome": self.outcome,
            "adjustment": list(self.adjustment),
            "derivation": self.derivation,
        }


@dataclass
class NotIdentifiable:
    """The honest refusal, with attribution and a repair ask (VDR-style)."""

    query: str
    reason: str
    ask: str

    def to_json(self) -> dict[str, Any]:
        return {"query": self.query, "identified": False,
                "reason": self.reason, "ask": self.ask}


def _satisfies_backdoor(scm: TernarySCM, x: str, y: str,
                        z: tuple[str, ...]) -> bool:
    if set(z) & scm.descendants({x}):
        return False
    # Z blocks every back-door path: X ⊥ Y | Z in G with X's out-edges cut
    return d_separated(scm, {x}, {y}, set(z), remove_out={x})


def _directed_paths(scm: TernarySCM, x: str, y: str) -> list[tuple[str, ...]]:
    paths: list[tuple[str, ...]] = []

    def walk(node: str, acc: tuple[str, ...]) -> None:
        if node == y:
            paths.append(acc)
            return
        for c in scm.children(node):
            if c not in acc:
                walk(c, acc + (c,))

    walk(x, (x,))
    return paths


def _satisfies_frontdoor(scm: TernarySCM, x: str, y: str,
                         m: tuple[str, ...]) -> bool:
    mset = set(m)
    # (i) M intercepts every directed path X -> Y
    for path in _directed_paths(scm, x, y):
        if not (set(path[1:-1]) & mset):
            return False
    # (ii) no unblocked backdoor path from X to M
    for mi in m:
        if not d_separated(scm, {x}, {mi}, set(), remove_out={x}):
            return False
    # (iii) all backdoor paths from M to Y blocked by X
    for mi in m:
        if not d_separated(scm, {mi}, {y}, {x}, remove_out={mi}):
            return False
    return True


def identify(scm: TernarySCM, treatment: str, outcome: str,
             max_set_size: int = 3) -> Estimand | NotIdentifiable:
    """Identify P(outcome | do(treatment)) from observed variables.

    Tier A: minimal backdoor set search; Tier B: frontdoor set search;
    otherwise an honest refusal naming the Phase-2 tier. Every acceptance
    carries its derivation (the criterion instance that licensed it).
    """
    query = f"P({outcome} | do({treatment}))"
    obs = [v for v in scm.observed if v not in (treatment, outcome)]

    if treatment not in scm.observed or outcome not in scm.observed:
        return NotIdentifiable(
            query=query,
            reason="treatment or outcome is not observed",
            ask="bind the variable to evidence scopes before asking",
        )

    for size in range(0, min(max_set_size, len(obs)) + 1):
        for z in combinations(obs, size):
            if _satisfies_backdoor(scm, treatment, outcome, z):
                return Estimand(
                    query=query,
                    tier="backdoor",
                    treatment=treatment,
                    outcome=outcome,
                    adjustment=z,
                    derivation=[
                        f"backdoor: Z={list(z)} contains no descendant of "
                        f"{treatment}",
                        f"backdoor: {treatment} ⊥ {outcome} | Z in "
                        f"G with out-edges of {treatment} removed",
                        "estimand: sum_z P(y|x,z) P(z)",
                    ],
                )

    for size in range(1, min(max_set_size, len(obs)) + 1):
        for m in combinations(obs, size):
            if _satisfies_frontdoor(scm, treatment, outcome, m):
                return Estimand(
                    query=query,
                    tier="frontdoor",
                    treatment=treatment,
                    outcome=outcome,
                    adjustment=m,
                    derivation=[
                        f"frontdoor: M={list(m)} intercepts all directed "
                        f"paths {treatment}->{outcome}",
                        f"frontdoor: no unblocked backdoor {treatment}->M; "
                        f"backdoor M->{outcome} blocked by {treatment}",
                        "estimand: sum_m P(m|x) sum_x' P(y|m,x') P(x')",
                    ],
                )

    return NotIdentifiable(
        query=query,
        reason=(
            "no backdoor or frontdoor identification over observed "
            "variables (Shpitser-Pearl ID tier is Phase 2)"
        ),
        ask=(
            f"seek an instrument for {treatment}, or evidence closing a "
            f"backdoor set between {treatment} and {outcome}"
        ),
    )


def ground_truth_do(scm: TernarySCM, treatment: str, x: Trit,
                    outcome: str, y: Trit) -> float:
    """P(Y=y | do(X=x)) by actual surgery + enumeration (the oracle)."""
    return scm.do({treatment: x}).prob({outcome: y})


# ---------------------------------------------------------------------------
# Rung 3: abduction - action - prediction (twin network, exact)
# ---------------------------------------------------------------------------


@dataclass
class CounterfactualResult:
    query: str
    probability: float
    posterior_mass: float           # P(evidence): abduction normalizer
    worlds: int                     # exogenous classes consistent w/ evidence

    def to_json(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "probability": round(self.probability, 12),
            "posterior_mass": round(self.posterior_mass, 12),
            "worlds": self.worlds,
        }


def counterfactual(
    scm: TernarySCM,
    evidence: Mapping[str, Trit],
    do: Mapping[str, Trit],
    query: Mapping[str, Trit],
) -> CounterfactualResult:
    """P( query holds in the do-world | evidence held in the actual world ).

    1. abduction:  posterior over exogenous configurations u consistent
                   with the evidence (exact enumeration);
    2. action:     graph surgery on the twin (same u - Pearl's twin
                   network, which in CDC is the shared-initialization
                   nested field);
    3. prediction: evaluate the twin under each posterior u; sum.
    """
    twin = scm.do(do)
    num = 0.0
    mass = 0.0
    worlds = 0
    for u, p in scm.exogenous_space():
        actual = scm.evaluate(u)
        if any(actual[k] != v for k, v in evidence.items()):
            continue
        mass += p
        worlds += 1
        cf = twin.evaluate(u)
        if all(cf[k] == v for k, v in query.items()):
            num += p
    label = (
        f"P({dict(query)} in do({dict(do)}) | {dict(evidence)})"
    )
    if mass == 0.0:
        return CounterfactualResult(label, 0.0, 0.0, 0)
    return CounterfactualResult(label, num / mass, mass, worlds)


def pn(scm: TernarySCM, treatment: str, outcome: str,
       x: Trit = 1, y: Trit = 1, x_alt: Trit = -1) -> float:
    """Probability of necessity: had X been x_alt, would Y have differed?

    PN = P( Y_{X=x_alt} != y  |  X = x, Y = y ), exact via the twin.
    """
    r = counterfactual(
        scm,
        evidence={treatment: x, outcome: y},
        do={treatment: x_alt},
        query={outcome: y},
    )
    if r.posterior_mass == 0.0:
        return 0.0
    return 1.0 - r.probability


def ps(scm: TernarySCM, treatment: str, outcome: str,
       x: Trit = 1, y: Trit = 1, x_alt: Trit = -1) -> float:
    """Probability of sufficiency: had X been x, would Y have become y?

    PS = P( Y_{X=x} = y  |  X = x_alt, Y != y ), exact via the twin.
    """
    total = 0.0
    mass = 0.0
    twin = scm.do({treatment: x})
    for u, p in scm.exogenous_space():
        actual = scm.evaluate(u)
        if actual[treatment] != x_alt or actual[outcome] == y:
            continue
        mass += p
        if twin.evaluate(u)[outcome] == y:
            total += p
    if mass == 0.0:
        return 0.0
    return total / mass


def pns(scm: TernarySCM, treatment: str, outcome: str,
        x: Trit = 1, y: Trit = 1, x_alt: Trit = -1) -> float:
    """Probability of necessity and sufficiency:
    PNS = P( Y_{X=x} = y  AND  Y_{X=x_alt} != y ), exact via twins."""
    twin_x = scm.do({treatment: x})
    twin_alt = scm.do({treatment: x_alt})
    total = 0.0
    for u, p in scm.exogenous_space():
        if twin_x.evaluate(u)[outcome] == y and \
                twin_alt.evaluate(u)[outcome] != y:
            total += p
    return total


def pn_bounds(
    p_y: float, p_xy: float, p_y_do_alt: float,
    p_ny_do_alt: float, p_nx_ny: float,
) -> tuple[float, float]:
    """Tian-Pearl bounds on PN from distributions alone (no mechanisms):

    max(0, [P(y) - P(y | do(x'))] / P(x, y))
      <= PN <=
    min(1, [P(y' | do(x')) - P(x', y')] / P(x, y)).

    For the mechanism-known setting `pn()` is exact; these bounds serve the
    distribution-only setting (e.g. observational + experimental data).
    """
    if p_xy == 0.0:
        return (0.0, 0.0)
    lower = max(0.0, (p_y - p_y_do_alt) / p_xy)
    upper = min(1.0, (p_ny_do_alt - p_nx_ny) / p_xy)
    return (lower, max(lower, upper))


# ---------------------------------------------------------------------------
# Random SCM generation (the T1 ground-truth suite's generator)
# ---------------------------------------------------------------------------


def _rng(seed: int) -> Callable[[], float]:
    """Deterministic uniform stream from SHA-256 (no random module)."""
    state = {"n": 0}

    def draw() -> float:
        state["n"] += 1
        digest = hashlib.sha256(f"{seed}:{state['n']}".encode()).digest()
        return int.from_bytes(digest[:8], "big") / 2**64

    return draw


WEIGHT_CHOICES = (-1.5, -1.0, -0.6, 0.6, 1.0, 1.5)
BIAS_CHOICES = (-0.4, 0.0, 0.4)
NOISE_GAIN_CHOICES = (0.75, 1.0, 1.25)


def random_scm(
    seed: int,
    n_observed: int = 4,
    edge_prob: float = 0.45,
    latent_prob: float = 0.3,
) -> TernarySCM:
    """A random CDC-native ternary SCM with optional latent confounders."""
    draw = _rng(seed)
    obs = tuple(f"V{i}" for i in range(n_observed))
    variables: list[str] = []
    mechanisms: dict[str, Mechanism] = {}
    priors: dict[str, tuple[float, float, float]] = {}

    def prior() -> tuple[float, float, float]:
        a, b, c = 0.2 + 0.6 * draw(), 0.2 + 0.6 * draw(), 0.2 + 0.6 * draw()
        s = a + b + c
        return (a / s, b / s, c / s)

    # latent confounders come first (roots)
    latent_pairs: list[tuple[str, str, str]] = []
    idx = 0
    for i in range(n_observed):
        for j in range(i + 1, n_observed):
            if draw() < latent_prob:
                name = f"H{idx}"
                idx += 1
                variables.append(name)
                mechanisms[name] = Mechanism(parents=(), weights=())
                priors[name] = prior()
                latent_pairs.append((name, obs[i], obs[j]))

    for i, v in enumerate(obs):
        parents: list[str] = []
        weights: list[float] = []
        for p in obs[:i]:
            if draw() < edge_prob and len(parents) < 3:
                parents.append(p)
                weights.append(WEIGHT_CHOICES[int(draw() * len(WEIGHT_CHOICES))
                                              % len(WEIGHT_CHOICES)])
        for h, a, b in latent_pairs:
            if v in (a, b):
                parents.append(h)
                weights.append(WEIGHT_CHOICES[int(draw() * len(WEIGHT_CHOICES))
                                              % len(WEIGHT_CHOICES)])
        variables.append(v)
        mechanisms[v] = Mechanism(
            parents=tuple(parents),
            weights=tuple(weights),
            bias=BIAS_CHOICES[int(draw() * len(BIAS_CHOICES))
                              % len(BIAS_CHOICES)],
            noise_gain=NOISE_GAIN_CHOICES[
                int(draw() * len(NOISE_GAIN_CHOICES))
                % len(NOISE_GAIN_CHOICES)],
        )
        priors[v] = prior()

    return TernarySCM(
        variables=tuple(variables),
        mechanisms=mechanisms,
        noise_priors=priors,
        observed=obs,
    )


# ---------------------------------------------------------------------------
# Canonical fixtures (the T2 suite)
# ---------------------------------------------------------------------------


def frontdoor_fixture() -> TernarySCM:
    """Smoking (X) -> Tar (M) -> Cancer (Y), confounded X <-H-> Y.

    Deadband saturation (a real CDC phenomenon this layer surfaced): with a
    single ternary noise term, full per-stratum support forces the
    quantizer's u -> class map to be the same bijection in every stratum -
    full support and parent dependence are mutually exclusive for
    single-input mechanisms. The mediator therefore carries a second
    independent observed input D (a dither), which widens the superposition
    grid so every class is reachable in every treatment stratum while the
    distribution still depends on X: positivity and confounding coexist,
    and the frontdoor estimand must match surgery truth exactly at every
    treatment value.
    """
    return TernarySCM(
        variables=("H", "D", "X", "M", "Y"),
        mechanisms={
            "H": Mechanism(parents=(), weights=()),
            "D": Mechanism(parents=(), weights=()),
            "X": Mechanism(parents=("H",), weights=(1.0,), noise_gain=0.75),
            "M": Mechanism(parents=("X", "D"), weights=(0.6, 0.45),
                           noise_gain=0.75),
            "Y": Mechanism(parents=("M", "H"), weights=(1.0, 0.8),
                           noise_gain=0.75),
        },
        noise_priors={
            "H": (0.3, 0.3, 0.4),
            "D": (0.35, 0.3, 0.35),
            "X": (0.25, 0.4, 0.35),
            "M": (0.2, 0.5, 0.3),
            "Y": (0.3, 0.4, 0.3),
        },
        observed=("D", "X", "M", "Y"),
    )


def backdoor_fixture() -> TernarySCM:
    """Z -> X, Z -> Y, X -> Y (adjust for Z; Simpson-style gap). Strong
    weights: see frontdoor_fixture on deadband saturation - the estimand
    is exact on positivity-clean treatment values and refuses elsewhere."""
    return TernarySCM(
        variables=("Z", "X", "Y"),
        mechanisms={
            "Z": Mechanism(parents=(), weights=()),
            "X": Mechanism(parents=("Z",), weights=(1.2,), noise_gain=0.75),
            "Y": Mechanism(parents=("X", "Z"), weights=(0.8, -1.2),
                           noise_gain=0.75),
        },
        noise_priors={
            "Z": (0.35, 0.3, 0.35),
            "X": (0.25, 0.4, 0.35),
            "Y": (0.3, 0.4, 0.3),
        },
        observed=("Z", "X", "Y"),
    )


def random_binary_scm(seed: int, n_observed: int = 4,
                      edge_prob: float = 0.5,
                      latent_prob: float = 0.25) -> TernarySCM:
    """A binary sub-family (values in {-1, +1}) for the Tian-Pearl bounds
    setting: the classic PN bounds are a binary-treatment/outcome theorem.
    A tiny bias keeps every superposition off exact zero, and a near-zero
    deadband makes tau a sign function."""
    draw = _rng(seed * 7919 + 13)
    obs = tuple(f"B{i}" for i in range(n_observed))
    variables: list[str] = []
    mechanisms: dict[str, Mechanism] = {}
    priors: dict[str, tuple[float, float, float]] = {}

    def prior() -> tuple[float, float, float]:
        p = 0.25 + 0.5 * draw()
        return (p, 0.0, 1.0 - p)

    latent_pairs: list[tuple[str, str, str]] = []
    idx = 0
    for i in range(n_observed):
        for j in range(i + 1, n_observed):
            if draw() < latent_prob:
                name = f"HB{idx}"
                idx += 1
                variables.append(name)
                mechanisms[name] = Mechanism(parents=(), weights=())
                priors[name] = prior()
                latent_pairs.append((name, obs[i], obs[j]))

    weight_choices = (-1.0, -0.6, 0.6, 1.0)
    for i, v in enumerate(obs):
        parents: list[str] = []
        weights: list[float] = []
        for p in obs[:i]:
            if draw() < edge_prob and len(parents) < 3:
                parents.append(p)
                weights.append(weight_choices[
                    int(draw() * len(weight_choices)) % len(weight_choices)])
        for h, a, b in latent_pairs:
            if v in (a, b):
                parents.append(h)
                weights.append(weight_choices[
                    int(draw() * len(weight_choices)) % len(weight_choices)])
        variables.append(v)
        mechanisms[v] = Mechanism(parents=tuple(parents),
                                  weights=tuple(weights),
                                  bias=0.07, noise_gain=1.0)
        priors[v] = prior()

    return TernarySCM(
        variables=tuple(variables),
        mechanisms=mechanisms,
        noise_priors=priors,
        observed=obs,
        deadband=1e-9,
    )


def bow_fixture() -> TernarySCM:
    """The bow graph: X -> Y with latent X <-H-> Y. Must refuse."""
    return TernarySCM(
        variables=("H", "X", "Y"),
        mechanisms={
            "H": Mechanism(parents=(), weights=()),
            "X": Mechanism(parents=("H",), weights=(1.0,), noise_gain=0.75),
            "Y": Mechanism(parents=("X", "H"), weights=(1.0, 1.0),
                           noise_gain=0.75),
        },
        noise_priors={
            "H": (0.3, 0.35, 0.35),
            "X": (0.3, 0.35, 0.35),
            "Y": (0.3, 0.35, 0.35),
        },
        observed=("X", "Y"),
    )
