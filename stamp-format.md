# Stamps and blocks — SUNSET's shared format, v1

How every SUNSET node seals its day, issues stamps, checks them and records them spent. Every node depends on it: the walls pay stamps for walking, the arm game for skill, the auction moves them between people, the print node turns them into paper, and the flip-dot wall burns paper.

> Status: draft 1, 22 Oct 2026. **Builds on GO TO BED's format v0** ([gtb/FORMAT.md](gtb/FORMAT.md)), whose blocks, seals and receipts were exercised in the [test bed](gtb/testbed/README.md): sizes, chains and six attacks. Everything v0 settled is kept unless this document says otherwise. Nothing built.

---

## 1. What carries over from v0, and what changes

**Kept from v0, unchanged:**

- **One block per node per day,** sealed at sunset, chained to the node's previous block by its fingerprint (`prev`).
- **Header and words:** the seal covers the header; the header covers the words through their fingerprint (`msgs`). Words fade after 7 days; headers keep the record checkable.
- **Plain JSON,** canonical form for fingerprints (keys sorted, no spaces, UTF-8), SHA-256.
- **Times about people to the hour,** always by the node's clock, never the phone's.
- **No identities:** no author, no account, no phone identifier in any record.
- **Message addresses** `node/day#n`, replies, whispers and shouts as v0 defines them, and v0's limits unless 7 says otherwise.
- **Anything over a limit is refused, never truncated.**

**Changed in v1:**

| | v0 (GO TO BED) | v1 (SUNSET) | Why |
| --- | --- | --- | --- |
| Who seals blocks | Nine walls | All nine nodes, walls and interactive | Every SUNSET node issues or spends stamps |
| How a stamp is held | A 32-byte **secret** sent to the phone | A **holder key** made on the phone; nothing reusable ever crosses the air (3.1) | v0's secret crosses the open Wi-Fi at issue and at spend; a bystander could copy it |
| Ways to earn | First delivery of a block | First delivery (walk), the arm game (skill); plus transfers: refunds, payouts, redemptions | SUNSET's proofs (SUNSET.md 2.1) |
| Spending nodes | One per town | Several: walls (paid shouts), auction, print node | 5 says how double spends are handled |
| Block header | Deliveries only | Adds `issued` and `spent` (6) | Every node's issues and spends travel with couriers |
| Shouts | 3 free per phone per wall per day | **Paid in stamps;** node notices free | Shouts are community advertising (wall-node.md 2.2) |
| Paper | None | Paper stamps from the print node (4) | Taking part without a phone |

---

## 2. Node keys

- **One Ed25519 key per node,** generated on the node at installation and kept in its encrypted flash. **Every stamp, paper stamp and block in SUNSET is signed with Ed25519.** (This settles the print node's open question: interactive-print.md 5.)
- **The nine public keys are published** in this repository (`keys/`, to add), built into every node's firmware, and on the website's Verify page, so any node or phone can check any signature without asking anyone.
- **A replaced or tampered node gets a new key.** The old key's blocks stay valid up to the replacement date; the new key is published with that date.
- **HMAC stays only where a node checks its own records,** such as the auction's collection tokens (interactive-auction.md 3.5), which no other node ever needs to verify.

---

## 3. Digital stamps

### 3.1 Holder keys, not secrets

In v0 the panel handed the phone a secret, and spending meant sending the secret back. On SUNSET's open, plain-HTTP Wi-Fi, anyone in range could read it on the way and spend it first at another node.

In v1 **the phone makes a key for each stamp:**

1. When a stamp is due, the page makes a fresh **Ed25519 key pair** for it and sends only the **public half** (`hk`).
2. The node issues the stamp to that public key and signs it.
3. To spend, the phone **signs** the spend with the private half, which never leaves the phone (3.4).

A bystander sees public keys and signatures, and a signature is good for one spend at one node at one moment. **There is nothing to steal on the air.**

**On the phone:** the node's pages are plain HTTP, so the browser's built-in cryptography (WebCrypto `subtle`) is not available: browsers only offer it on secure (HTTPS) pages. The node serves a small Ed25519 and SHA-256 library with the page (a TweetNaCl-class library, about 7 KB minified). Random numbers come from `crypto.getRandomValues`, which browsers do allow on plain HTTP. To check in the carry test (8).

**One key per stamp,** never reused, so no two stamps can be linked to the same phone.

### 3.2 A stamp

```json
{"v": 1, "node": 3, "day": "2027-07-14", "n": 17, "t": 1784019600, "why": "walk", "exp": "2027-07-21", "hk": "5d0e…", "sig": "…"}
```

| Field | Meaning |
| --- | --- |
| `node` | The issuing node, 1–9. Its 5 × 5 logo is drawn from this number; the logo is not in the data. **Every node's logo is unique, and never the same as the Photovoltaic Art logo:** the PVA mark stands for the project, never for a node or a stamp |
| `day`, `n` | The node's day and the stamp's serial that day, from 1. **Stamp ID** = `node/day/n`, e.g. `3/2027-07-14/17` |
| `t` | The hour of issue, by the node's clock |
| `why` | `walk` (first delivery), `skill` (arm game), `refund` (auction outbid), `payout` (auction seller), `redeem` (paper turned back into digital) |
| `exp` | **Valid until:** the last day the stamp can be spent, by the nodes' clocks (3.5) |
| `hk` | The holder's public key |
| `sig` | The node's signature over everything above |

- **Every stamp is worth one.** A payout of 9 is nine stamps. Simple to count, to show in the passport and to spend in part.
- **Only `walk` and `skill` create stamps.** `refund`, `payout` and `redeem` re-issue value that was spent into the node first, so they never add to the total.

### 3.3 Issuance is recorded

The node writes each stamp it issues into its next sealed block (`issued`, 6). So the chain proves that every stamp exists, and a stolen node key cannot mint stamps that other nodes accept once they hold the real chain (v0's attack 5, still covered).

### 3.4 Spending

1. The spending node's page sends a fresh **challenge** (random, one use).
2. The phone signs `spend|<stamp ID>|<spending node>|<day>|<challenge>` with the stamp's private key, for each stamp it spends, and sends the stamps and signatures.
3. The node checks, for each stamp:
   0. today is not after its `exp` (3.5);
   1. the issuer's signature (published keys);
   2. the holder's signature over this spend and this challenge;
   3. not on its **spent list** (5.2);
   4. if the node holds the issuer's block for that day: the stamp is in its `issued` record.
4. All checks pass: the node writes the spend to flash, then acts (opens a locker, accepts the bid, prints, posts the shout). The spend goes into its next sealed block (`spent`, 6), with the holder's signature as proof.

Check 4 is skipped only when the issuer's block hasn't arrived yet: a fresh stamp from a distant wall is accepted on its signature alone, as in v0.

### 3.5 Valid until

**Every stamp has a valid-until date.** After it, no node accepts it; it stays in the passport as a faded picture, like a message that has gone.

- **Why:** stamps that are never spent would otherwise pile up and lose meaning (SUNSET.md 3.1). Expiry is a sink that needs no node: unspent stamps leave circulation on their own, and holding stamps is pointless, so people spend them. It is SUNSET's forgetting, applied to money as it is to words.
- **How long:** set in the pilot. **Proposed: 7 days,** the same as messages. Shorter makes stamps hotter; longer lets a visitor who comes back next weekend still spend.
- **Re-issued stamps:**
  - `refund` (outbid at the auction): keeps the **earliest** `exp` of the stamps it replaces, so bidding can't be used to renew stamps.
  - `payout` (to the seller) and `redeem` (paper back to digital): a **fresh** `exp` from the day of issue.
- **Checked at every spend** (3.4, check 0): a stamp past its `exp` is refused before anything else.
- **A bonus for storage:** a node only needs to remember spent stamps until they would have expired, so the spent list stays small (5.3). With a validity of 7 days or less, every stamp is still within the 7 days of full headers, so check 4 is always possible.
- **Paper stamps** carry their own valid-until date on the sticker, set separately (4).

---

## 4. Paper stamps

Paper is specified in [interactive-print.md](interactive-print.md); this is its format.

- **The redeem sticker's QR** carries: the print node's number, serial, value, day, a **redeem code** (random, 16 bytes), and the print node's Ed25519 signature over all of it.
- **Valid until:** the sticker carries a valid-until date, printed and in the QR; its length is set separately from digital stamps (3.5).
- **Genuine** is checkable anywhere, offline, from the print node's public key: by any node, and by the website's Verify page on any phone.
- **Unspent** is known only to the print node and the flip-dot wall, which share one live spent list over ESP-NOW (interactive-flipdot.md 2.1). Redemption is at the print node only; spending paper is at the flip-dot wall only. So a copied sticker is honoured once, at most.
- **Paper has no holder key.** It is bearer in the old way: the code is on the paper. That is the point of paper: it works without a phone. Its weakness (a photocopy is as good as the original until one is used) is stated in interactive-print.md 2.3.
- Paper spends are recorded in the print node's and the flip-dot wall's blocks by **serial**, never by code.

---

## 5. Double spends

### 5.1 What can and cannot happen

| Attempt | Result |
| --- | --- |
| A bystander copies a stamp off the air | Impossible: only public keys and one-use signatures cross the air (3.1) |
| A forged stamp | Fails the issuer's signature |
| A stamp from a stolen node key | Fails check 4 wherever the real chain has arrived; the key is replaced (2) |
| The same stamp spent twice at one node | Refused: on that node's spent list |
| Paper copied and used twice | Refused: the gateway pair shares its list live |
| **A holder copies their own phone's storage and spends the same stamp at two distant nodes before couriers carry the news** | **Possible.** The one double spend v1 cannot prevent offline (5.2) |

### 5.2 The rule: bound it, prove it, show it

Preventing the last case would need a live link between all spending nodes, which SUNSET doesn't have by design. So v1 accepts it, and makes it **bounded, provable and public:**

- **Bounded.** Every node merges every `spent` record that couriers bring into its own spent list. A copied stamp works only at a node that hasn't yet heard of the first spend, and only until the news arrives: in a busy town, within a day. It takes deliberate effort (copying a browser's storage to a second device) and gains at most one extra use per stamp, of a currency with no cash value.
- **Proved.** Two spend records for the same stamp, each carrying the holder's signature, sealed into two nodes' blocks: that is a cryptographic proof of a double spend. No accusation is needed, and none can be made, because there are no identities.
- **Shown.** Walls show the count on the dial tone ("2 stamps spent twice this week"), and the website's archive keeps the season's total. The installation runs its own honesty in public (SUNSET.md 7).
- **Live where it matters.** Any spending nodes within ESP-NOW range of each other share their spent list live, as the gateway pair already does. When siting the auction, prefer a place within range of the gateway: that puts SUNSET's largest spends on the live list.

### 5.3 The spent list

- Each node keeps the **spent IDs of every stamp not yet expired,** from its own spends and every `spent` record couriers bring; an ID is dropped once its stamp's `exp` has passed (3.5). An ID is about 6 bytes packed (node, day, serial): with 7-day validity, a few KB.
- Full headers fade after 7 days, as in v0, so after a week check 4 (3.4) is no longer possible for a stamp; the issuer's signature and the spent list still are.

---

## 6. Blocks, v1

A v0 block, with these additions to the **header** (so they survive when the words fade):

```json
"issued": [ {"n": 17, "t": 1784019600, "why": "walk", "hk": "5d0e…"} ],
"spent":  [ {"id": "7/2027-07-13/4", "t": 1784023200, "ss": "…"} ],
"paper":  [ {"serial": 412, "t": 1784026800, "ev": "minted", "val": 5} ]
```

| Field | Meaning |
| --- | --- |
| `issued` | Every stamp this node issued that day, with its holder key (3.3) |
| `spent` | Every digital stamp spent at this node that day, with the holder's spend signature `ss` (3.4) |
| `paper` | Print node and flip-dot wall only: paper minted, redeemed or flipped, by serial (4) |
| `deliveries` | As v0, but with the holder key of the walk stamp in place of v0's fingerprint of the secret |

**Messages** keep v0's form, with two additions:

- `paid` (optional): the number of stamps paid for a shout. The stamps themselves are in the same block's `spent`.
- `node` (optional): `1` for a **node notice** (the auction's "Locker A uncollected", a service notice). Free, and shown on its own line on the dial tone.

---

## 7. Limits

v0's limits stand, with these added or changed:

| Limit | Value | Why |
| --- | --- | --- |
| Walk stamps | At most 72 a day across the town | One per first delivery of each node's block to each other node: 9 × 8. v0's cap, unchanged |
| Skill stamps | At most `C` a day (about 30–40), released by the sun as the arm's panel harvests | The sun's purse (interactive-arm-game.md 3.3.1) |
| `issued` and `spent` entries per block | 100 each | An `issued` entry is about 110 bytes, a `spent` entry about 180 (the signature): at most about 29 KB of header. A wall issues at most 8 walk stamps a day; 100 is for the busiest interactive node |
| Block size | 48 KB hard (v0: 16 KB) | Headers now carry stamps; words still limited to 60 messages |
| Storage | A node keeps 7 days of every node's blocks **within 1.2 MB**, oldest out first; a phone carries 3 days **within 500 KB**, newest first | Budgeted, not worst-cased: nine full blocks a day for a week would not fit in the ESP32's flash. A typical block is a few KB (v0's test bed: under 5 KB), so the budget is rarely reached |
| Stamps per spend | 50 | One request stays small |
| Shouts | Paid, so v0's 3-per-phone limit is dropped; price set in the pilot | wall-node.md 2.2 |
| Spent list | Until each stamp's `exp` (5.3) | Expired stamps can't be spent, so need no record |

The test bed (gtb/testbed) is extended to v1 to confirm these sizes before firmware (TASKS.md).

---

## 8. Phones

- **The passport page holds the stamps,** and only the browser holds their private keys. Clearing the browser's storage loses the stamps, like losing cash. The passport's saved images are a picture of the stamps, not the stamps.
- **The carry test** ([gtb/carry_test/TEST.md](gtb/carry_test/TEST.md)) now checks two more things: the crypto library runs in each browser path (pop-up and full browser), and the stamp keys survive a day.

---

## 9. Open questions

| Question | Notes |
| --- | --- |
| Validity | How long a stamp is valid (3.5): 7 days proposed; set in the pilot. Paper's validity, separately |
| Passport backup | Whether a visitor can export their stamps (a QR of the keys) to a new phone. Convenient, and exactly the copy that makes double spends possible |
| Double-spend display | Count only, or the stamp IDs too (they identify no one) |
| Auction siting | Within ESP-NOW range of the gateway, to put large spends on the live list (5.2)? |
| Holder-key library | Which library, its size on the node, and speed on older phones |
