"""GO TO BED format v0: blocks, receipts, signatures, checks (see ../FORMAT.md)."""
import json, hashlib, os, re
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

LIMITS = dict(text_chars=140, msgs_per_block=60, msgs_per_phone_panel_day=3,
              block_bytes=16 * 1024, phone_days=3, panel_days=7)

def hour(t):
    """Times about people are kept to the hour, never finer (no user data: see ../FORMAT.md)."""
    return int(t) // 3600 * 3600

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

def header(b):
    """The block without its words: what the panel signs, and all a spending node needs to check stamps."""
    return {k: v for k, v in b.items() if k != "messages"}

def block_fp(b):
    """A block's fingerprint, used for the chain: SHA-256 of the signed header, so it survives the words."""
    return fp(header(b))

def seal_block(sk, panel, day, seq, prev, woke, slept, messages, deliveries):
    b = dict(v=0, panel=panel, day=day, seq=seq, prev=prev, woke=woke, slept=slept,
             msgs=fp(messages), deliveries=deliveries)
    sign(sk, b)                 # the seal covers the header, including the messages' fingerprint
    b["messages"] = messages    # the words travel beside the header
    if len(canon(b)) > LIMITS["block_bytes"]:
        raise ValueError(f"block {block_id(b)} too big: {len(canon(b))} bytes")
    return b

def make_receipt(sk, panel, block, t):
    secret = os.urandom(32).hex()
    r = sign(sk, dict(v=0, panel=panel, block=block, t=t, secret=secret))
    return r, hashlib.sha256(bytes.fromhex(secret)).hexdigest()

RE = re.compile(r"^([1-9])/(\d{4}-\d{2}-\d{2})#([1-9]\d?)$")   # reply address: panel/day#n (n from 1)

def re_ok(m, b, i):
    """A reply may point at any earlier message: an earlier day anywhere, or earlier today at this panel.
    The panel checks the address only, never that it holds the message."""
    if "re" not in m: return True
    x = RE.match(m["re"])
    if not x or int(x[3]) > LIMITS["msgs_per_block"]: return False
    p, d, n = int(x[1]), x[2], int(x[3])
    return d < b["day"] or (d == b["day"] and p == b["panel"] and n <= i)

def check_block(pub, b, prev_block=None):
    """Works on a full block or on a header alone (words already faded)."""
    errs = []
    if not sig_ok(pub, header(b)): errs.append("bad signature")
    if prev_block is None and b["seq"] == 1 and b["prev"] != "": errs.append("first block has prev")
    if prev_block is not None and b["prev"] != block_fp(prev_block): errs.append("chain broken")
    if len(canon(b)) > LIMITS["block_bytes"]: errs.append("too big")
    if any(d["t"] % 3600 for d in b["deliveries"]): errs.append("delivery time finer than an hour")
    if "messages" not in b: return errs
    if fp(b["messages"]) != b["msgs"]: errs.append("messages altered")
    if len(b["messages"]) > LIMITS["msgs_per_block"]: errs.append("too many messages")
    if any(len(m["text"]) > LIMITS["text_chars"] for m in b["messages"]): errs.append("message too long")
    if any(not (hour(b["woke"]) <= m["t"] <= b["slept"]) for m in b["messages"]): errs.append("message outside awake time")
    if any(m["t"] % 3600 for m in b["messages"]): errs.append("message time finer than an hour")
    if any(not re_ok(m, b, i) for i, m in enumerate(b["messages"])): errs.append("bad reply address")
    if any(set(m) - {"t", "text", "re", "p"} for m in b["messages"]): errs.append("unknown message field")
    if any(m.get("p", 1) != 1 for m in b["messages"]): errs.append("bad promoted flag")
    return errs

def check_receipt(pubs, r, blocks_by_id, spent):
    """blocks_by_id: {(panel, day): block or header}. Headers are enough. Returns (ok, reason)."""
    if not sig_ok(pubs[r["panel"]], r): return False, "bad panel signature"
    if r["t"] % 3600: return False, "time finer than an hour"
    h = hashlib.sha256(bytes.fromhex(r["secret"])).hexdigest()
    found = any(d["rcpt"] == h and d["block"] == r["block"]
                for (p, _), b in blocks_by_id.items() if p == r["panel"] for d in b["deliveries"])
    if not found: return False, "not in the chain"
    if h in spent: return False, "already spent"
    return True, "ok"
