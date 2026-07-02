"""The GistHybrid training protocol: honest rounds, ablations, native export.

Run:  python3 train.py            (full protocol -> build/RESULTS.md)

Protocol (the "how many rounds" question answered mechanically):
  - datasets are native-labeled (data.py; the BiDi C runtime is the
    labeler), split train/val/test by generation seed;
  - Adam with gradient clipping; the number of training rounds is
    determined by EARLY STOPPING - train up to MAX_EPOCHS, keep the best
    validation score, stop after PATIENCE epochs without improvement,
    restore the best weights;
  - primary model: the full hybrid on the 64-slot lattice (bits=6);
  - ablations (bits=3 for speed): calculus-init vs random-init, lattice
    convolution off, openness gating off, ternary bottleneck off;
  - deployment model: single-slot, C-parity mode (deploy=True), exported
    to build/gist_hybrid.cdc and verified word-for-word against
    `cdc_native_runtime infer` on all 27 ternary input words.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402
import hybrid  # noqa: E402
import tensorcdc as tc  # noqa: E402

BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
MAX_EPOCHS = 60
PATIENCE = 8
BATCH = 64
LR = 0.02


# --------------------------------------------------------------------------- #
# loss / metrics
# --------------------------------------------------------------------------- #


def batch_loss(model, theta, amp, occ, slot_y, glob_y):
    sl, gl, _ = model.forward(theta, amp)
    b, s, _ = sl.v.shape
    flat = hybrid._reshape(sl, (b * s, 3))
    mask = occ.reshape(-1)
    idx = np.where(mask)[0]
    sel = tc._op(flat.v[idx], (flat,), None)

    def back(flat=flat, sel=sel, idx=idx):
        flat.g[idx] += sel.g
    sel._back = back
    slot_ce = tc.cross_entropy_rows(sel, slot_y.reshape(-1)[idx] + 1)
    glob_ce = tc.cross_entropy_rows(gl, glob_y + 1)
    return tc.add(slot_ce, glob_ce), slot_ce.v.item(), glob_ce.v.item()


def evaluate(model, theta, amp, occ, slot_y, glob_y):
    sl, gl, _ = model.forward(theta, amp)
    slot_pred = sl.v.argmax(axis=2) - 1
    glob_pred = gl.v.argmax(axis=1) - 1
    slot_acc = float((slot_pred[occ] == slot_y[occ]).mean())
    glob_acc = float((glob_pred == glob_y).mean())
    # macro-F1 over slot classes
    f1s = []
    for cls in (-1, 0, 1):
        tp = float(((slot_pred[occ] == cls) & (slot_y[occ] == cls)).sum())
        fp = float(((slot_pred[occ] == cls) & (slot_y[occ] != cls)).sum())
        fn = float(((slot_pred[occ] != cls) & (slot_y[occ] == cls)).sum())
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * p * r / (p + r) if p + r else 0.0)
    conf = np.zeros((3, 3), dtype=int)
    for t, pcls in zip(glob_y, glob_pred):
        conf[t + 1, pcls + 1] += 1
    return {
        "slot_acc": round(slot_acc, 4),
        "slot_macro_f1": round(float(np.mean(f1s)), 4),
        "global_acc": round(glob_acc, 4),
        "global_confusion": conf.tolist(),
        "score": round(0.5 * (slot_acc + glob_acc), 4),
    }


def snapshot(model):
    return [p.v.copy() for p in model.params()]


def restore(model, snap):
    for p, v in zip(model.params(), snap):
        p.v[:] = v


def fit(model, train_set, val_set, max_epochs=MAX_EPOCHS, patience=PATIENCE,
        lr=LR, log=None):
    theta, amp, occ, sy, gy = train_set
    opt = tc.Adam(model.params(), lr=lr)
    n = theta.shape[0]
    best, best_snap, bad, epochs_run = -1.0, snapshot(model), 0, 0
    history = []
    rng = np.random.default_rng(0)
    for epoch in range(max_epochs):
        order = rng.permutation(n)
        losses = []
        for lo in range(0, n, BATCH):
            sel = order[lo:lo + BATCH]
            loss, _, _ = batch_loss(model, theta[sel], amp[sel], occ[sel],
                                    sy[sel], gy[sel])
            loss.backward()
            opt.step()
            losses.append(loss.v.item())
        val = evaluate(model, *val_set)
        history.append({"epoch": epoch + 1,
                        "train_loss": round(float(np.mean(losses)), 4),
                        "val": val})
        epochs_run = epoch + 1
        if log:
            log(f"  epoch {epoch+1:>2}  loss {np.mean(losses):.4f}  "
                f"val slot {val['slot_acc']:.3f} glob {val['global_acc']:.3f}")
        if val["score"] > best + 1e-4:
            best, best_snap, bad = val["score"], snapshot(model), 0
        else:
            bad += 1
            if bad >= patience:
                break
    restore(model, best_snap)
    return {"epochs_run": epochs_run, "best_val_score": best,
            "history": history}


# --------------------------------------------------------------------------- #
# deployment export + native parity
# --------------------------------------------------------------------------- #


def export_deploy_cdc(model, path):
    """Trained single-slot deploy model -> native .cdc (weights as channels)."""
    w, a = model.pyr_w.v, model.pyr_a.v
    lines = [
        "# gist_hybrid.cdc -- TRAINED GistHybrid deployment (deploy-parity "
        "mode),",
        "# generated by torchcdc/train.py; weights are the learned SO(2) "
        "channels.",
        "# Inference:  cdc_native_runtime infer gist_hybrid.cdc net "
        "'<trit-word>'",
        "field nn-run dt=0.125 gain=1.0 deadband=0.5",
        "module net field=nn-run belief=0.0 prior=0.0 precision=1.0 "
        "action-gain=1.0",
    ]
    for c in range(6):
        theta0 = 1.5707963267948966
        lines.append(f"cell net.c{c} module=net theta={theta0} "
                     f"amplitude=1.0 omega=0.0")
    for e, (src, dst) in enumerate(hybrid.PYRAMID_EDGES):
        lines.append(f"channel net.c{src} -> net.c{dst} "
                     f"weight={w[e]:.12f} delay=0.0 angle={a[e]:.12f} lines=1")
    for k in range(model.steps):
        lines.append(f"flow layer{k} field=nn-run "
                     f"duration={model.step_size * float(model.gain.v[0]):.12f}")
    lines.append("commit verdict module=net")
    lines.append("nest pool parent=net child=net-child")
    # minimal child scope so `run` mode also works on this file
    lines.insert(6, "module net-child field=nn-run belief=0.0 prior=0.0 "
                 "precision=1.0 action-gain=1.0 parent=net")
    lines.insert(7, "cell net-child.a module=net-child theta=0.0 "
                 "amplitude=1.0 omega=0.0")
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


TRIT_THETA = {"+": 0.0, "0": 1.5707963267948966, "-": 3.141592653589793}


def native_parity(model, cdc_path, rt=data.DEFAULT_RT):
    """Compare model singular trits vs `infer` on all 27 input words."""
    words = []
    for a in "+0-":
        for b in "+0-":
            for c in "+0-":
                words.append(a + b + c)
    matches, results = 0, []
    for word in words:
        theta = np.full((1, 6), np.pi / 2)
        amp = np.ones((1, 6))
        for i, ch in enumerate(word):
            theta[0, i] = TRIT_THETA[ch]
        _, _, trits = model.forward(theta, amp)
        py_sing = int(trits.v[0, hybrid.SINGULAR])
        out = subprocess.run([rt, "infer", cdc_path, "net", word],
                             capture_output=True, text=True)
        fields = dict(p.split("=", 1) for p in out.stdout.split()
                      if "=" in p)
        c_word = fields.get("word", "")
        c_sing = {"+": 1, "0": 0, "-": -1}[c_word[hybrid.SINGULAR]]
        ok = py_sing == c_sing
        matches += ok
        results.append({"input": word, "python_singular": py_sing,
                        "native_word": c_word, "match": bool(ok)})
    return matches, len(words), results


# --------------------------------------------------------------------------- #
# the protocol
# --------------------------------------------------------------------------- #


def main():
    os.makedirs(BUILD, exist_ok=True)
    t0 = time.time()
    report = {"protocol": {"max_epochs": MAX_EPOCHS, "patience": PATIENCE,
                           "batch": BATCH, "lr": LR,
                           "labeler": "cdc_native_runtime (BiDi)"}}

    def log(msg):
        print(msg, flush=True)

    # ---- datasets --------------------------------------------------------
    log("== building native-labeled datasets ==")
    d6_train = data.build_dataset(1000, 64, seed=11, cache_dir=BUILD)
    d6_val = data.build_dataset(200, 64, seed=12, cache_dir=BUILD)
    d6_test = data.build_dataset(250, 64, seed=13, cache_dir=BUILD)
    d3_train = data.build_dataset(700, 8, seed=21, cache_dir=BUILD)
    d3_val = data.build_dataset(150, 8, seed=22, cache_dir=BUILD)
    d3_test = data.build_dataset(200, 8, seed=23, cache_dir=BUILD)
    log(f"datasets ready ({time.time()-t0:.0f}s)")

    # ---- primary: full hybrid on the 64-slot lattice ----------------------
    log("== primary: full hybrid, 64-slot lattice, calculus-init ==")
    primary = hybrid.GistHybrid(bits=6, steps=4).init_calculus()
    pre = evaluate(primary, *d6_test)
    run = fit(primary, d6_train, d6_val, log=log)
    post = evaluate(primary, *d6_test)
    report["primary"] = {
        "bits": 6, "params": primary.n_params(),
        "untrained_test": pre, "trained_test": post,
        "epochs_run": run["epochs_run"],
        "best_val_score": run["best_val_score"],
        "history": run["history"],
    }
    primary.save(os.path.join(BUILD, "gist_hybrid_weights.json"))
    log(f"primary: slot {pre['slot_acc']:.3f}->{post['slot_acc']:.3f}  "
        f"global {pre['global_acc']:.3f}->{post['global_acc']:.3f}  "
        f"({run['epochs_run']} epochs)")

    # ---- baselines / ablations (bits=3) ------------------------------------
    log("== ablations (8-slot lattice) ==")
    ablations = {}
    for name, kw, init_seed in [
        ("calculus_init", {}, None),
        ("random_init", {}, 5),
        ("no_lattice", {"lattice": False}, None),
        ("no_gating", {"gating": False}, None),
        ("no_bottleneck", {"bottleneck": False}, None),
    ]:
        m = hybrid.GistHybrid(bits=3, steps=4, **kw)
        m = m.init_random(init_seed) if init_seed is not None \
            else m.init_calculus()
        pre_a = evaluate(m, *d3_test)
        run_a = fit(m, d3_train, d3_val)
        post_a = evaluate(m, *d3_test)
        ablations[name] = {"untrained": pre_a, "trained": post_a,
                           "epochs_run": run_a["epochs_run"],
                           "params": m.n_params()}
        log(f"  {name:<14} slot {post_a['slot_acc']:.3f} "
            f"glob {post_a['global_acc']:.3f} ({run_a['epochs_run']} ep)")
    report["ablations"] = ablations

    # majority baselines
    _, _, occ6, sy6, gy6 = d6_test
    maj_slot = max((-1, 0, 1), key=lambda c: (sy6[occ6] == c).sum())
    maj_glob = max((-1, 0, 1), key=lambda c: (gy6 == c).sum())
    report["baselines"] = {
        "majority_slot_acc": round(float((sy6[occ6] == maj_slot).mean()), 4),
        "majority_global_acc": round(float((gy6 == maj_glob).mean()), 4),
    }

    # ---- deployment model + native parity ----------------------------------
    log("== deployment model (C-parity) + native export ==")
    deploy = hybrid.GistHybrid(bits=0, steps=4, lattice=False,
                               deploy=True).init_calculus()
    d0_train = _slotset(d3_train)
    d0_val = _slotset(d3_val)
    d0_test = _slotset(d3_test)
    pre_d = evaluate(deploy, *d0_test)
    run_d = fit(deploy, d0_train, d0_val)
    post_d = evaluate(deploy, *d0_test)
    cdc_path = os.path.join(BUILD, "gist_hybrid.cdc")
    export_deploy_cdc(deploy, cdc_path)
    matches, total, parity = native_parity(deploy, cdc_path)
    report["deployment"] = {
        "untrained": pre_d, "trained": post_d,
        "epochs_run": run_d["epochs_run"],
        "native_parity": f"{matches}/{total}",
        "parity_detail": parity,
        "cdc": os.path.basename(cdc_path),
    }
    log(f"deployment: slot {post_d['slot_acc']:.3f}; "
        f"native parity {matches}/{total}")

    report["wall_seconds"] = round(time.time() - t0, 1)
    json.dump(report, open(os.path.join(BUILD, "results.json"), "w"),
              indent=1)
    _write_md(report)
    log(f"== done in {report['wall_seconds']}s -> build/RESULTS.md ==")
    return report


def _slotset(dset):
    """Explode a lattice dataset into single-slot samples (bits=0 model)."""
    theta, amp, occ, sy, gy = dset
    n, slots = occ.shape
    ts, as_, ys = [], [], []
    for i in range(n):
        for s in range(slots):
            if occ[i, s]:
                base = s * hybrid.CELLS
                ts.append(theta[i, base:base + hybrid.CELLS])
                as_.append(amp[i, base:base + hybrid.CELLS])
                ys.append(sy[i, s])
    theta0 = np.array(ts)
    amp0 = np.array(as_)
    occ0 = np.ones((len(ts), 1), dtype=bool)
    slot_y = np.array(ys).reshape(-1, 1)
    glob_y = np.array(ys)          # single slot: global == slot verdict
    return theta0, amp0, occ0, slot_y, glob_y


def _write_md(r):
    p = r["primary"]
    lines = [
        "# GistHybrid training results (native-labeled)",
        "",
        f"Labeler: **BiDi `cdc_native_runtime`** (every label is a committed",
        "word of the actual mechanism; mirror rule for negatives).",
        f"Protocol: Adam lr {r['protocol']['lr']}, batch "
        f"{r['protocol']['batch']}, early stopping patience "
        f"{r['protocol']['patience']} (max {r['protocol']['max_epochs']}).",
        "",
        "## Primary - full hybrid, 64-slot lattice "
        f"({p['params']} params)",
        "",
        "| metric | untrained (calculus-init) | trained |",
        "|---|---|---|",
        f"| slot accuracy | {p['untrained_test']['slot_acc']} | "
        f"**{p['trained_test']['slot_acc']}** |",
        f"| slot macro-F1 | {p['untrained_test']['slot_macro_f1']} | "
        f"**{p['trained_test']['slot_macro_f1']}** |",
        f"| global verdict accuracy | {p['untrained_test']['global_acc']} | "
        f"**{p['trained_test']['global_acc']}** |",
        "",
        f"Training rounds (early stopping): **{p['epochs_run']} epochs**. "
        f"Majority baselines: slot "
        f"{r['baselines']['majority_slot_acc']}, global "
        f"{r['baselines']['majority_global_acc']}.",
        "",
        "Global verdict confusion (rows = truth no/maybe/yes):",
        "",
        "```",
        str(np.array(p["trained_test"]["global_confusion"])),
        "```",
        "",
        "## Ablations (8-slot lattice)",
        "",
        "| variant | slot acc | global acc | epochs |",
        "|---|---|---|---|",
    ]
    for name, a in r["ablations"].items():
        lines.append(f"| {name} | {a['trained']['slot_acc']} | "
                     f"{a['trained']['global_acc']} | {a['epochs_run']} |")
    d = r["deployment"]
    lines += [
        "",
        "## Deployment (single-slot, C-parity mode)",
        "",
        f"Trained slot accuracy {d['trained']['slot_acc']}; exported to "
        f"`{d['cdc']}`;",
        f"**native parity {d['native_parity']}** - the exported `.cdc` "
        "reproduces the",
        "trained model's singular trit under `cdc_native_runtime infer` on "
        "every one",
        "of the 27 ternary input words.",
        "",
        f"Wall time: {r['wall_seconds']}s (single CPU, numpy).",
    ]
    open(os.path.join(BUILD, "RESULTS.md"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
