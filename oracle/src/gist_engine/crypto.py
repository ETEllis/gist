"""Verification primitives: canonical hashing, hash chain, Merkle tree, HKDF/PRF.

Honest crypto with honest claims. Everything here is standard-library
SHA-256/HMAC (RFC 2104) and HKDF (RFC 5869). What the GIST decision stamp
guarantees:

  - integrity: any mutation of any replayed ledger payload changes the head
    hash, the Merkle roots, and therefore the stamp;
  - binding: the stamp is bound to the session prompt and session id through
    HKDF, so a stamp cannot be transplanted onto a different question;
  - replay verifiability: a third party can recompute every hash, root, and
    the stamp from the append-only ledger alone.

It is *not* a zero-knowledge proof and does not attest that evidence content
is true - it attests that the released synthesis is exactly the one this
ledger derives.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Sequence

LEAF_DOMAIN = b"\x00"
NODE_DOMAIN = b"\x01"


def canonical_json(payload: Any) -> bytes:
    """Deterministic JSON encoding (sorted keys, tight separators, UTF-8)."""
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_hash(payload: Any) -> str:
    return sha256_hex(canonical_json(payload))


def chain_hash(prev_hash_hex: str, payload: Any) -> str:
    """Hash-chain link: H(prev || canonical(payload))."""
    return sha256_hex(bytes.fromhex(prev_hash_hex) + canonical_json(payload))


GENESIS = sha256_hex(b"gist-engine/genesis/v1")


# ---------------------------------------------------------------------------
# Merkle tree (domain-separated; odd nodes promote)
# ---------------------------------------------------------------------------


def merkle_leaf(payload: Any) -> str:
    return sha256_hex(LEAF_DOMAIN + canonical_json(payload))


def merkle_node(left_hex: str, right_hex: str) -> str:
    return sha256_hex(NODE_DOMAIN + bytes.fromhex(left_hex) + bytes.fromhex(right_hex))


def merkle_root(leaves: Sequence[str]) -> str:
    """Root over pre-hashed leaves (hex). Empty input roots the empty payload."""
    if not leaves:
        return merkle_leaf(None)
    level = list(leaves)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                nxt.append(merkle_node(level[i], level[i + 1]))
            else:
                nxt.append(level[i])  # odd node promotes
        level = nxt
    return level[0]


def merkle_levels(leaves: Sequence[str]) -> list[list[str]]:
    """All levels leaf->root (for audit display and proofs)."""
    if not leaves:
        return [[merkle_leaf(None)]]
    levels = [list(leaves)]
    while len(levels[-1]) > 1:
        prev = levels[-1]
        nxt = []
        for i in range(0, len(prev), 2):
            if i + 1 < len(prev):
                nxt.append(merkle_node(prev[i], prev[i + 1]))
            else:
                nxt.append(prev[i])
        levels.append(nxt)
    return levels


# ---------------------------------------------------------------------------
# HKDF (RFC 5869) and PRF (HMAC-SHA256)
# ---------------------------------------------------------------------------


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac.new(salt or b"\x00" * 32, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: bytes, info: bytes, length: int = 32) -> bytes:
    out = b""
    t = b""
    counter = 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        out += t
        counter += 1
    return out[:length]


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int = 32) -> bytes:
    return hkdf_expand(hkdf_extract(salt, ikm), info, length)


def prf(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def session_key(prompt: str, session_id: str) -> bytes:
    """K = HKDF(ikm=prompt, salt=session_id, info='gist-engine/64-gate/v1')."""
    return hkdf(
        ikm=prompt.encode("utf-8"),
        salt=session_id.encode("utf-8"),
        info=b"gist-engine/64-gate/v1",
    )


def gate_challenge(key: bytes) -> str:
    """T = PRF(K, '64-gate') - the challenge the gate must answer."""
    return prf(key, b"64-gate")


def decision_stamp(
    key: bytes,
    leaf_root: str,
    round_roots: Sequence[str],
    decision_coordinate: str,
    head_hash: str,
) -> str:
    """The co-signable release stamp binding gate, ladder, decision, and ledger."""
    material = canonical_json(
        {
            "leaf_root": leaf_root,
            "round_roots": list(round_roots),
            "decision": decision_coordinate,
            "head": head_hash,
            "challenge": gate_challenge(key),
        }
    )
    return prf(key, material)
