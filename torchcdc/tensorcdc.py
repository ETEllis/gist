"""tensorcdc: the CDC-torch substrate - numpy reverse-mode autograd.

The torch-essence, sized to the calculus: array tensors with gradients,
reverse-mode differentiation through the ops the CDC dynamics are written
in, the straight-through ternary quantizer (the commit bottleneck), and an
Adam optimizer with gradient clipping. Numpy is the only dependency.

Tier: TRAINING HARNESS (sanctioned 2026-07-02, "go all in"). The mechanism
itself remains native .cdc on the BiDi runtimes; this substrate exists to
train networks that anticipate it, against labels the native C runtime
produces.
"""

from __future__ import annotations

import numpy as np


class T:
    """A tensor node: numpy array + grad + backward closure."""

    __slots__ = ("v", "g", "_back", "_parents", "requires_grad")

    def __init__(self, v, requires_grad=False, parents=(), back=None):
        self.v = np.asarray(v, dtype=np.float64)
        self.g = np.zeros_like(self.v)
        self.requires_grad = requires_grad or any(
            p.requires_grad for p in parents
        )
        self._parents = parents
        self._back = back

    @property
    def shape(self):
        return self.v.shape

    def zero_grad(self):
        self.g = np.zeros_like(self.v)

    def backward(self):
        if self.v.size != 1:
            raise ValueError("backward() starts from a scalar")
        topo, seen = [], set()

        def visit(t):
            if id(t) in seen:
                return
            seen.add(id(t))
            for p in t._parents:
                visit(p)
            topo.append(t)

        visit(self)
        self.g = np.ones_like(self.v)
        for t in reversed(topo):
            if t._back is not None:
                t._back()


def param(v):
    return T(v, requires_grad=True)


def const(v):
    return T(v)


def _op(v, parents, back):
    return T(v, parents=parents, back=back)


def add(a, b):
    out = _op(a.v + b.v, (a, b), None)

    def back():
        a.g += _unbroadcast(out.g, a.v.shape)
        b.g += _unbroadcast(out.g, b.v.shape)

    out._back = back
    return out


def sub(a, b):
    out = _op(a.v - b.v, (a, b), None)

    def back():
        a.g += _unbroadcast(out.g, a.v.shape)
        b.g -= _unbroadcast(out.g, b.v.shape)

    out._back = back
    return out


def mul(a, b):
    out = _op(a.v * b.v, (a, b), None)

    def back():
        a.g += _unbroadcast(out.g * b.v, a.v.shape)
        b.g += _unbroadcast(out.g * a.v, b.v.shape)

    out._back = back
    return out


def scale(a, k: float):
    out = _op(a.v * k, (a,), None)

    def back():
        a.g += out.g * k

    out._back = back
    return out


def sin(a):
    out = _op(np.sin(a.v), (a,), None)

    def back():
        a.g += out.g * np.cos(a.v)

    out._back = back
    return out


def cos(a):
    out = _op(np.cos(a.v), (a,), None)

    def back():
        a.g -= out.g * np.sin(a.v)

    out._back = back
    return out


def sqrt(a, eps=1e-12):
    root = np.sqrt(a.v + eps)
    out = _op(root, (a,), None)

    def back():
        a.g += out.g * 0.5 / root

    out._back = back
    return out


def gate(a, mask):
    """Non-differentiable elementwise gate (static routing)."""
    m = np.asarray(mask, dtype=np.float64)
    out = _op(a.v * m, (a,), None)

    def back():
        a.g += out.g * m

    out._back = back
    return out


def gather(a, idx):
    idx = np.asarray(idx)
    out = _op(a.v[idx], (a,), None)

    def back():
        np.add.at(a.g, idx, out.g)

    out._back = back
    return out


def scatter_sum(a, idx, size):
    """Sum-scatter along the last axis: out[..., idx[k]] += a[..., k]."""
    idx = np.asarray(idx)
    v = np.zeros(a.v.shape[:-1] + (size,), dtype=np.float64)
    if a.v.ndim == 1:
        np.add.at(v, idx, a.v)
    else:
        np.add.at(v, (slice(None), idx), a.v)
    out = _op(v, (a,), None)

    def back():
        if a.v.ndim == 1:
            a.g += out.g[idx]
        else:
            a.g += out.g[:, idx]

    out._back = back
    return out


def total(a):
    out = _op(np.array(a.v.sum()), (a,), None)

    def back():
        a.g += out.g

    out._back = back
    return out


def matmul(a, b):
    out = _op(a.v @ b.v, (a, b), None)

    def back():
        a.g += out.g @ b.v.T
        b.g += a.v.T @ out.g

    out._back = back
    return out


def ste_trit(kappa, deadband=0.5):
    """The commit bottleneck: hard ternary forward, straight-through grad."""
    hard = np.where(kappa.v > deadband, 1.0,
                    np.where(kappa.v < -deadband, -1.0, 0.0))
    out = _op(hard, (kappa,), None)

    def back():
        kappa.g += out.g  # straight through

    out._back = back
    return out


def cross_entropy_rows(logits, targets):
    """Mean softmax cross-entropy: logits [N, C], integer targets [N]."""
    z = logits.v - logits.v.max(axis=1, keepdims=True)
    e = np.exp(z)
    p = e / e.sum(axis=1, keepdims=True)
    n = logits.v.shape[0]
    loss = -np.log(np.clip(p[np.arange(n), targets], 1e-12, None)).mean()
    out = _op(np.array(loss), (logits,), None)

    def back():
        grad = p.copy()
        grad[np.arange(n), targets] -= 1.0
        logits.g += out.g * grad / n

    out._back = back
    return out


def _unbroadcast(g, shape):
    """Sum-reduce a gradient back to a broadcast operand's shape."""
    while g.ndim > len(shape):
        g = g.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and g.shape[i] != 1:
            g = g.sum(axis=i, keepdims=True)
    return g.reshape(shape)


class Adam:
    def __init__(self, params, lr=0.01, betas=(0.9, 0.999), eps=1e-8,
                 clip=1.0):
        self.params = list(params)
        self.lr, self.b1, self.b2, self.eps, self.clip = (
            lr, betas[0], betas[1], eps, clip)
        self.m = [np.zeros_like(p.v) for p in self.params]
        self.s = [np.zeros_like(p.v) for p in self.params]
        self.t = 0

    def step(self):
        self.t += 1
        for i, p in enumerate(self.params):
            g = np.clip(p.g, -self.clip, self.clip)
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.s[i] = self.b2 * self.s[i] + (1 - self.b2) * g * g
            mh = self.m[i] / (1 - self.b1 ** self.t)
            sh = self.s[i] / (1 - self.b2 ** self.t)
            p.v -= self.lr * mh / (np.sqrt(sh) + self.eps)
            p.zero_grad()
