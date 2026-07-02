"""The 64-Gate: emergent release conditions, all executable.

The gate never commands - it observes slot state (a passive watcher over the
ledger-projected board) and proposes eligibility when ALL checks hold:

  1. coverage    every axis value {0..3} on every axis is represented by at
                 least one *contributing* slot (committed non-void word with
                 coverage >= c_min);
  2. parity      contributing slots are non-degenerately distributed over
                 Σq mod 2 and Σq mod 3 (no empty class, no class dominating
                 beyond p_max);
  3. stability   every contributing slot has u >= tau_u;
  4. cf          every contributing slot has a >= tau_a and the mean
                 >= tau_a_mean;
  5. lift        the median causal lift >= tau_lift;
  6. global      S >= tau_S, sustained for `hysteresis` consecutive gate
                 evaluations;
  7. saturation  every contributing slot is saturated (plateaued with a
                 closed boundary), or the retrieval budget is exhausted
                 (which passes the check but is flagged on the proposal).

Structural spine (T1/T5): every contributing slot's committed word is
admissible by construction (the commit barrier), and the gate reports each
word's normal-form tier; the release headline tier is the weakest
contributing tier. A `localized` or better headline means the synthesis is a
genuine calculus value (normal form), not merely a stopped process.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from statistics import median

from .bridge import address_of_index
from .metrics import SlotMetrics
from .walks import classify, tier_rank


@dataclass
class GateThresholds:
    """Release thresholds. tau_a/tau_a_mean sit below the structural 2/3
    ceiling of counterfactual survival for single-cluster conclusions (see
    metrics.cf_agreement): 0.5 admits robust conclusions and rejects
    contested/knife-edge ones (<= 1/3)."""

    c_min: float = 0.15
    p_max: float = 0.85
    tau_u: float = 0.70
    tau_a: float = 0.50
    tau_a_mean: float = 0.60
    tau_lift: float = 0.30
    tau_S: float = 0.60
    hysteresis: int = 3

    def to_json(self) -> dict:
        return {
            "c_min": self.c_min, "p_max": self.p_max, "tau_u": self.tau_u,
            "tau_a": self.tau_a, "tau_a_mean": self.tau_a_mean,
            "tau_lift": self.tau_lift, "tau_S": self.tau_S,
            "hysteresis": self.hysteresis,
        }


@dataclass
class GateCheck:
    name: str
    passed: bool
    detail: str

    def to_json(self) -> dict:
        return {"name": self.name, "passed": self.passed, "detail": self.detail}


@dataclass
class GateReport:
    checks: list[GateCheck] = dc_field(default_factory=list)
    eligible: bool = False
    contributing: list[int] = dc_field(default_factory=list)
    tier_histogram: dict[str, int] = dc_field(default_factory=dict)
    headline_tier: str = "inadmissible"
    global_S: float = 0.0
    budget_release: bool = False
    scope: str = "full"

    def to_json(self) -> dict:
        return {
            "checks": [c.to_json() for c in self.checks],
            "eligible": self.eligible,
            "contributing": self.contributing,
            "tier_histogram": self.tier_histogram,
            "headline_tier": self.headline_tier,
            "global_S": round(self.global_S, 6),
            "budget_release": self.budget_release,
            "scope": self.scope,
        }


def evaluate_gate(
    slot_words: dict[int, tuple[int, ...]],
    slot_metrics: dict[int, SlotMetrics],
    saturated: set[int],
    S_history: list[float],
    thresholds: GateThresholds,
    budget_exhausted: bool = False,
    scope: str = "full",
    occupied: set[int] | None = None,
) -> GateReport:
    """Evaluate the seven checks.

    scope='full' (research sessions): coverage demands every axis value on
    every axis; parity demands non-degeneracy over all classes.

    scope='occupied' (verdict/tool sessions): coverage and parity are
    evaluated over the *occupied* sub-lattice (slots that received any
    evidence) - every occupied axis value must be carried by a contributing
    slot, and parity applies only across the classes the occupied slots
    inhabit (a single-class occupation passes with a scope note). The
    remaining five checks are identical. Releases record which scope gated
    them; an occupied-scope release is a claim about the evidenced scopes
    only, never silently about the full lattice.
    """
    th = thresholds
    report = GateReport(scope=scope)

    # contributing slots: committed non-void word with enough coverage
    contributing = sorted(
        s for s, w in slot_words.items()
        if any(t != 0 for t in w)
        and s in slot_metrics
        and slot_metrics[s].coverage >= th.c_min
    )
    report.contributing = contributing

    def check(name: str, passed: bool, detail: str) -> bool:
        report.checks.append(GateCheck(name, passed, detail))
        return passed

    if not contributing:
        check("coverage", False, "no contributing slots")
        report.eligible = False
        return report

    # 1. coverage
    missing: list[str] = []
    if scope == "occupied":
        occ = occupied if occupied is not None else set(contributing)
        for axis in range(3):
            wanted = {address_of_index(s)[axis] for s in occ}
            present = {address_of_index(s)[axis] for s in contributing}
            for v in sorted(wanted - present):
                missing.append(f"axis{axis + 1}={v}")
        check(
            "coverage",
            not missing,
            f"all occupied axis values represented ({len(occ)} occupied slots)"
            if not missing else f"occupied but uncovered: {', '.join(missing)}",
        )
    else:
        for axis in range(3):
            present = {address_of_index(s)[axis] for s in contributing}
            for v in range(4):
                if v not in present:
                    missing.append(f"axis{axis + 1}={v}")
        check(
            "coverage",
            not missing,
            "all 3 axes x 4 values represented" if not missing
            else f"missing {', '.join(missing)}",
        )

    # 2. parity (non-degeneracy over Σq mod 2 and mod 3)
    m2: dict[int, int] = {}
    m3: dict[int, int] = {}
    for s in contributing:
        q = address_of_index(s)
        m2[sum(q) % 2] = m2.get(sum(q) % 2, 0) + 1
        m3[sum(q) % 3] = m3.get(sum(q) % 3, 0) + 1
    n = len(contributing)
    if scope == "occupied":
        occ = occupied if occupied is not None else set(contributing)
        occ_m2 = {sum(address_of_index(s)) % 2 for s in occ}
        occ_m3 = {sum(address_of_index(s)) % 3 for s in occ}
        degenerate = (
            any(m2.get(c, 0) == 0 for c in occ_m2)
            or any(m3.get(c, 0) == 0 for c in occ_m3)
            or (len(occ_m2) > 1 and max(m2.values()) / n > th.p_max)
            or (len(occ_m3) > 1 and max(m3.values()) / n > th.p_max)
        )
        detail = (f"occupied classes mod2={sorted(occ_m2)} "
                  f"mod3={sorted(occ_m3)}; contributing mod2={m2} mod3={m3}")
        if len(occ_m2) == 1 and len(occ_m3) == 1:
            detail += " (single-class occupation: scoped pass)"
    else:
        degenerate = (
            any(m2.get(c, 0) == 0 for c in (0, 1))
            or any(m3.get(c, 0) == 0 for c in (0, 1, 2))
            or max(m2.values()) / n > th.p_max
            or max(m3.values()) / n > th.p_max
        )
        detail = f"mod2={m2} mod3={m3} over {n} slots"
    check("parity", not degenerate, detail)

    # 3. stability
    weak_u = [s for s in contributing if slot_metrics[s].stability < th.tau_u]
    check(
        "stability",
        not weak_u,
        f"all u >= {th.tau_u}" if not weak_u else f"below threshold: {weak_u}",
    )

    # 4. counterfactual agreement
    weak_a = [s for s in contributing if slot_metrics[s].cf_agreement < th.tau_a]
    mean_a = sum(slot_metrics[s].cf_agreement for s in contributing) / n
    check(
        "cf_agreement",
        not weak_a and mean_a >= th.tau_a_mean,
        f"mean a={mean_a:.3f}" + ("" if not weak_a else f", below floor: {weak_a}"),
    )

    # 5. causal lift
    med_lift = median(slot_metrics[s].causal_lift for s in contributing)
    check("causal_lift", med_lift >= th.tau_lift, f"median lift={med_lift:.3f}")

    # 6. global agreement with hysteresis
    S = S_history[-1] if S_history else 0.0
    report.global_S = S
    window = S_history[-th.hysteresis:]
    sustained = len(window) >= th.hysteresis and all(x >= th.tau_S for x in window)
    check(
        "global_agreement",
        sustained,
        f"S={S:.3f}, window={['%.3f' % x for x in window]}, "
        f"need {th.hysteresis} x >= {th.tau_S}",
    )

    # 7. retrieval saturation (or budget exhaustion, flagged)
    unsaturated = [s for s in contributing if s not in saturated]
    sat_ok = not unsaturated or budget_exhausted
    report.budget_release = bool(unsaturated) and budget_exhausted
    check(
        "saturation",
        sat_ok,
        "all contributing slots saturated" if not unsaturated
        else f"budget-exhausted release, open slots: {unsaturated}"
        if budget_exhausted
        else f"unsaturated: {unsaturated}",
    )

    # structural tier report (T5 normal-form spine)
    hist: dict[str, int] = {}
    weakest = "catalan"
    for s in contributing:
        tier = classify(slot_words[s])
        hist[tier] = hist.get(tier, 0) + 1
        if tier_rank(tier) < tier_rank(weakest):
            weakest = tier
    report.tier_histogram = hist
    report.headline_tier = weakest

    report.eligible = all(c.passed for c in report.checks)
    return report
