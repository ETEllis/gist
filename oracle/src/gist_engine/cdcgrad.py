"""cdcgrad: the torch-essence for CDC - a minimal reverse-mode autograd.

What torch contributes to Python-as-substrate is exactly two things: a
tensor with a gradient, and reverse-mode differentiation through the ops
that build a computation. cdcgrad supplies precisely that, zero-dep and
sized to the calculus: vector tensors, the elementwise ops the CDC
dynamics are written in (add/mul/sin/cos/sqrt), the sparse SO(2)/complex
mixing product (the channel layer), a straight-through ternary quantizer
(the commit bottleneck), and cross-entropy for readout heads.

It is deliberately tiny and readable rather than fast: the reference
substrate for training CDC-native networks (gistnet.py), and the
semantics oracle for any torch/jax port of the same graph.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence


class Tensor:
    """A vector with a gradient and a backward closure."""

    __slots__ = ("data", "grad", "_back", "_parents", "requires_grad")

    def __init__(self, data: Sequence[float], requires_grad: bool = False,
                 _parents: tuple["Tensor", ...] = (),
                 _back: Callable[[], None] | None = None):
        self.data = [float(x) for x in data]
        self.grad = [0.0] * len(self.data)
        self.requires_grad = requires_grad or any(
            p.requires_grad for p in _parents
        )
        self._parents = _parents
        self._back = _back

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        head = ", ".join(f"{x:.4f}" for x in self.data[:4])
        return f"Tensor([{head}{'...' if len(self.data) > 4 else ''}])"

    # -- graph ----------------------------------------------------------------

    def backward(self) -> None:
        """Reverse-mode sweep from a scalar (len-1) tensor."""
        if len(self.data) != 1:
            raise ValueError("backward() starts from a scalar tensor")
        topo: list[Tensor] = []
        seen: set[int] = set()

        def visit(t: Tensor) -> None:
            if id(t) in seen:
                return
            seen.add(id(t))
            for p in t._parents:
                visit(p)
            topo.append(t)

        visit(self)
        self.grad = [1.0]
        for t in reversed(topo):
            if t._back is not None:
                t._back()

    def zero_grad(self) -> None:
        self.grad = [0.0] * len(self.data)


def tensor(data: Sequence[float], requires_grad: bool = False) -> Tensor:
    return Tensor(data, requires_grad=requires_grad)


def _binary(a: Tensor, b: Tensor, fwd, dfa, dfb) -> Tensor:
    if len(a) != len(b):
        raise ValueError(f"length mismatch {len(a)} vs {len(b)}")
    out = Tensor([fwd(x, y) for x, y in zip(a.data, b.data)],
                 _parents=(a, b))

    def back() -> None:
        for i, g in enumerate(out.grad):
            if g == 0.0:
                continue
            a.grad[i] += g * dfa(a.data[i], b.data[i])
            b.grad[i] += g * dfb(a.data[i], b.data[i])

    out._back = back
    return out


def add(a: Tensor, b: Tensor) -> Tensor:
    return _binary(a, b, lambda x, y: x + y,
                   lambda x, y: 1.0, lambda x, y: 1.0)


def sub(a: Tensor, b: Tensor) -> Tensor:
    return _binary(a, b, lambda x, y: x - y,
                   lambda x, y: 1.0, lambda x, y: -1.0)


def mul(a: Tensor, b: Tensor) -> Tensor:
    return _binary(a, b, lambda x, y: x * y,
                   lambda x, y: y, lambda x, y: x)


def _unary(a: Tensor, fwd, df) -> Tensor:
    out = Tensor([fwd(x) for x in a.data], _parents=(a,))

    def back() -> None:
        for i, g in enumerate(out.grad):
            if g != 0.0:
                a.grad[i] += g * df(a.data[i])

    out._back = back
    return out


def scale(a: Tensor, k: float) -> Tensor:
    return _unary(a, lambda x: k * x, lambda x: k)


def shift(a: Tensor, k: float) -> Tensor:
    return _unary(a, lambda x: x + k, lambda x: 1.0)


def sin(a: Tensor) -> Tensor:
    return _unary(a, math.sin, math.cos)


def cos(a: Tensor) -> Tensor:
    return _unary(a, math.cos, lambda x: -math.sin(x))


def sqrt(a: Tensor, eps: float = 1e-12) -> Tensor:
    return _unary(a, lambda x: math.sqrt(x + eps),
                  lambda x: 0.5 / math.sqrt(x + eps))


def mask(a: Tensor, gate: Sequence[float]) -> Tensor:
    """Non-differentiable elementwise gate (a static routing decision)."""
    g = [float(x) for x in gate]
    out = Tensor([x * gi for x, gi in zip(a.data, g)], _parents=(a,))

    def back() -> None:
        for i, gr in enumerate(out.grad):
            if gr != 0.0:
                a.grad[i] += gr * g[i]

    out._back = back
    return out


def gather(a: Tensor, idx: Sequence[int]) -> Tensor:
    ii = list(idx)
    out = Tensor([a.data[i] for i in ii], _parents=(a,))

    def back() -> None:
        for pos, i in enumerate(ii):
            if out.grad[pos] != 0.0:
                a.grad[i] += out.grad[pos]

    out._back = back
    return out


def scatter_sum(a: Tensor, idx: Sequence[int], size: int) -> Tensor:
    ii = list(idx)
    data = [0.0] * size
    for pos, i in enumerate(ii):
        data[i] += a.data[pos]
    out = Tensor(data, _parents=(a,))

    def back() -> None:
        for pos, i in enumerate(ii):
            if out.grad[i] != 0.0:
                a.grad[pos] += out.grad[i]

    out._back = back
    return out


def concat(parts: Sequence[Tensor]) -> Tensor:
    data: list[float] = []
    for p in parts:
        data.extend(p.data)
    out = Tensor(data, _parents=tuple(parts))

    def back() -> None:
        off = 0
        for p in parts:
            for i in range(len(p)):
                if out.grad[off + i] != 0.0:
                    p.grad[i] += out.grad[off + i]
            off += len(p)

    out._back = back
    return out


def total(a: Tensor) -> Tensor:
    out = Tensor([sum(a.data)], _parents=(a,))

    def back() -> None:
        g = out.grad[0]
        if g != 0.0:
            for i in range(len(a)):
                a.grad[i] += g

    out._back = back
    return out


# ---------------------------------------------------------------------------
# CDC-specific ops
# ---------------------------------------------------------------------------


def complex_mix(
    re_w: Tensor, im_w: Tensor,
    src: Sequence[int], dst: Sequence[int],
    zx: Tensor, zy: Tensor, size: int,
) -> tuple[Tensor, Tensor]:
    """The channel layer: sparse complex matvec A = M z.

    Edge e carries weight (re_w[e] + i*im_w[e]) from cell src[e] to cell
    dst[e]; z is the Cartesian cell state. Returns (Ax, Ay). This is the
    SO(2)-block mixing of NEURAL.md as a differentiable op - gradients
    flow to both the states and the edge parameters (learnable rotations).
    """
    zx_s = gather(zx, src)
    zy_s = gather(zy, src)
    # (re + i im)(zx + i zy) = (re zx - im zy) + i (re zy + im zx)
    ax_e = sub(mul(re_w, zx_s), mul(im_w, zy_s))
    ay_e = add(mul(re_w, zy_s), mul(im_w, zx_s))
    return scatter_sum(ax_e, dst, size), scatter_sum(ay_e, dst, size)


def ste_trit(kappa: Tensor, deadband: float = 0.5) -> Tensor:
    """The commit bottleneck: hard balanced-ternary quantization forward,
    straight-through (identity) gradient backward."""
    out = Tensor(
        [1.0 if k > deadband else (-1.0 if k < -deadband else 0.0)
         for k in kappa.data],
        _parents=(kappa,),
    )

    def back() -> None:
        for i, g in enumerate(out.grad):
            if g != 0.0:
                kappa.grad[i] += g  # straight through

    out._back = back
    return out


def cross_entropy(logits: Tensor, target: int) -> Tensor:
    """Numerically-stable softmax cross-entropy against a class index."""
    m = max(logits.data)
    exps = [math.exp(x - m) for x in logits.data]
    s = sum(exps)
    probs = [e / s for e in exps]
    out = Tensor([-math.log(max(probs[target], 1e-12))], _parents=(logits,))

    def back() -> None:
        g = out.grad[0]
        if g != 0.0:
            for i in range(len(logits)):
                logits.grad[i] += g * (probs[i] - (1.0 if i == target else 0.0))

    out._back = back
    return out


def sgd_step(params: Sequence[Tensor], lr: float, clip: float = 1.0) -> None:
    """SGD with elementwise gradient clipping (recurrent nets through the
    Kuramoto turn can explode without it - a documented realization
    parameter, not calculus)."""
    for p in params:
        for i in range(len(p)):
            g = p.grad[i]
            if g > clip:
                g = clip
            elif g < -clip:
                g = -clip
            p.data[i] -= lr * g
        p.zero_grad()
