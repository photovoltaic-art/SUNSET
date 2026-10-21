#!/usr/bin/env python3
"""Check a test-bed run: every block's signature, chain and limits; every receipt against the chain;
then three attacks that must fail (altered message, forged receipt, receipt redeemed twice)."""
import json, glob, sys, copy, os, hashlib
import gtb

out = sys.argv[1] if len(sys.argv) > 1 else "out"
pubs = {int(k): v for k, v in json.load(open(f"{out}/panel_keys.json")).items()}
blocks = {}
for f in glob.glob(f"{out}/blocks/*.json"):
    b = json.load(open(f)); blocks[(b["panel"], b["day"])] = b
receipts = [json.load(open(f)) for f in sorted(glob.glob(f"{out}/receipts/*.json"))]

bad = 0
for p in sorted(pubs):
    prev = None
    for k in sorted(k for k in blocks if k[0] == p):
        errs = gtb.check_block(pubs[p], blocks[k], prev)
        if errs: bad += 1; print("BLOCK", k, errs)
        prev = blocks[k]
print(f"blocks: {len(blocks)} checked, {bad} with errors")

spent, okc = set(), 0
for r in receipts:
    ok, why = gtb.check_receipt(pubs, r, blocks, spent)
    if ok:
        okc += 1; spent.add(hashlib.sha256(bytes.fromhex(r["secret"])).hexdigest())
    else:
        print("RECEIPT", r["panel"], r["block"], why)
print(f"receipts: {len(receipts)} checked, {okc} valid and redeemed once")

# attacks
fails = 0
k = sorted(blocks)[len(blocks) // 2]; b = copy.deepcopy(blocks[k])
if b["messages"]:
    b["messages"][0]["text"] = "altered"
    errs = gtb.check_block(pubs[k[0]], b)
    print("attack 1, altered message:", "detected" if "bad signature" in errs else "NOT DETECTED"); fails += "bad signature" not in errs
r = copy.deepcopy(receipts[0]); r["secret"] = os.urandom(32).hex()
ok, why = gtb.check_receipt(pubs, r, blocks, set())
print("attack 2, forged secret:", "refused (" + why + ")" if not ok else "ACCEPTED"); fails += ok
r = receipts[0]
ok, why = gtb.check_receipt(pubs, r, blocks, spent)
print("attack 3, redeem twice:", "refused (" + why + ")" if not ok else "ACCEPTED"); fails += ok
fake = gtb.sign(gtb.new_key(b"not-a-panel"), dict(v=0, panel=3, block="7/2027-07-13", t=0, secret=os.urandom(32).hex()))
ok, why = gtb.check_receipt(pubs, fake, blocks, set())
print("attack 4, receipt signed by a fake panel:", "refused (" + why + ")" if not ok else "ACCEPTED"); fails += ok
stolen = gtb.new_key(b"gtb-testbed-panel-3")   # a stolen panel key (test-bed keys are derived from public seeds)
fake2, _ = gtb.make_receipt(stolen, 3, "7/2027-07-13", 0)
ok, why = gtb.check_receipt(pubs, fake2, blocks, set())
print("attack 5, stolen panel key, receipt not in any sealed block:", "refused (" + why + ")" if not ok else "ACCEPTED"); fails += ok
sys.exit(1 if bad or fails or okc != len(receipts) else 0)
