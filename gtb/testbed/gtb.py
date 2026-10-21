"""GO TO BED format v0: blocks, receipts, signatures, checks (see ../FORMAT.md)."""
import json, hashlib, os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

LIMITS = dict(text_chars=140, msgs_per_block=60, msgs_per_phone_panel_day=3,
              block_bytes=16 * 1024, phone_days=3, panel_days=7)

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def fp(obj):
    return hashlib.sha256(canon(obj)).hexdigest()

def new_key(seed=None):
    if seed is not None:
        return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(seed).digest())
    return Ed25519PrivateKey.generate()

def pub_hex(sk):
    return sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()

def sign(sk, obj):
    body = {k: v for k, v in obj.items() if k != "sig"}
    obj["sig"] = sk.sign(canon(body)).hex()
    return obj

def sig_ok(pub, obj):
    body = {k: v for k, v in obj.items() if k != "sig"}
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub)).verify(bytes.fromhex(obj["sig"]), canon(body))
        return True
    except Exception:
        return False

def block_id(b):
    return f'{b["panel"]}/{b["day"]}'

def seal_block(sk, panel, day, seq, prev, woke, slept, messages, deliveries):
    b = dict(v=0, panel=panel, day=day, seq=seq, prev=prev, woke=woke, slept=slept,
             messages=messages, deliveries=deliveries)
    sign(sk, b)
    if len(canon(b)) > LIMITS["block_bytes"]:
        raise ValueError(f"block {block_id(b)} too big: {len(canon(b))} bytes")
    return b

def make_receipt(sk, panel, block, t):
    secret = os.urandom(32).hex()
    r = sign(sk, dict(v=0, panel=panel, block=block, t=t, secret=secret))
    return r, hashlib.sha256(bytes.fromhex(secret)).hexdigest()

def check_block(pub, b, prev_block=None):
    errs = []
    if not sig_ok(pub, b): errs.append("bad signature")
    if prev_block is None and b["seq"] == 1 and b["prev"] != "": errs.append("first block has prev")
    if prev_block is not None and b["prev"] != fp(prev_block): errs.append("chain broken")
    if len(canon(b)) > LIMITS["block_bytes"]: errs.append("too big")
    if len(b["messages"]) > LIMITS["msgs_per_block"]: errs.append("too many messages")
    if any(len(m["text"]) > LIMITS["text_chars"] for m in b["messages"]): errs.append("message too long")
    if any(not (b["woke"] <= m["t"] <= b["slept"]) for m in b["messages"]): errs.append("message outside awake time")
    return errs

def check_receipt(pubs, r, blocks_by_id, spent):
    """blocks_by_id: {(panel, day): block}. Returns (ok, reason)."""
    if not sig_ok(pubs[r["panel"]], r): return False, "bad panel signature"
    h = hashlib.sha256(bytes.fromhex(r["secret"])).hexdigest()
    found = any(d["rcpt"] == h and d["block"] == r["block"]
                for (p, _), b in blocks_by_id.items() if p == r["panel"] for d in b["deliveries"])
    if not found: return False, "not in the chain"
    if h in spent: return False, "already spent"
    return True, "ok"
