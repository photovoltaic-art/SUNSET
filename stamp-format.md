# Stamps and blocks — SUNSET's shared format, v1

How every SUNSET node seals its day, issues stamps, checks them and records them spent. Every node depends on it: the walls pay stamps for walking, the arm game for skill, the auction moves them between people, the gettoneria turns them into tokens, and the flip-dot wall burns tokens.

> Status: draft 2, 25 Oct 2026 (valid-until dates; tokens replace paper; the coin ledger held by every node). **Builds on GO TO BED's format v0** ([gtb/FORMAT.md](gtb/FORMAT.md)), whose blocks, seals and receipts were exercised in the [test bed](gtb/testbed/README.md): sizes, chains and six attacks. Everything v0 settled is kept unless this document says otherwise. Nothing built.

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
| Spending nodes | One per town | Several: walls (paid shouts), auction, gettoneria | 5 says how double spends are handled |
| Block header | Deliveries only | Adds `issued` and `spent` (6) | Every node's issues and spends travel with couriers |
| Shouts | 3 free per phone per wall per day | **Paid in stamps;** node notices free | Shouts are community advertising (wall-node.md 2.2) |
| Tokens | None | Tokens from the gettoneria: printed coins with an NFC tag (4) | Taking part without a phone |

---

## 2. Node keys

- **One Ed25519 key per node,** generated on the node at installation and kept in its encrypted flash. **Every stamp, token and block in SUNSET is signed with Ed25519.**
- **The nine public keys are published** in this repository (`keys/`, to add), built into every node's firmware, and on the website's Verify page, so any node or phone can check any signature without asking anyone.
- **A replaced or tampered node gets a new key.** The old key's blocks stay valid up to the replacement date; the new key is published with that date.
- **HMAC stays only where a node checks its own records,** such as the auction's collection claims (interactive-auction.md 3.5), which no other node ever needs to verify.

---

## 3. Digital stamps

### 3.1 Holder keys, not secrets

In v0 the panel handed the phone a secret, and spending meant sending the secret back. On SUNSET's open, plain-HTTP Wi-Fi, anyone in range could read it on the way and spend it first at another node.

In v1 **the phone makes a key for each stamp:**

1. When a stamp is due, the page makes a fresh **Ed25519 key pair** for it and sends only the **public half** (`hk`).
2. The node issues the stamp to that public key and signs it.
3. To spend, the phone **signs** the spend with the private half, which never leaves the phone (3.4).

A bystander sees public keys and signatures, and a signature is good for one spend at one node at one moment. **There is nothing to steal by listening.** An *active* attacker, a fake network at the same address, can read the passport itself: see [SECURITY.md](SECURITY.md) 4.1.

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
| `why` | `walk` (first delivery), `skill` (arm game), `refund` (auction outbid), `payout` (auction seller), `redeem` (a token turned back into digital) |
| `exp` | **Valid until:** the last day the stamp can be spent, by the nodes' clocks (3.5) |
| `coin` | `redeem` stamps only: the ID of the coin redeemed, so every redemption can be checked against the year's coin list (4) |
| `hk` | The holder's public key |
| `sig` | The node's signature over everything above |

- **Every stamp is worth one.** A payout of 9 is nine stamps. Simple to count, to show in the passport and to spend in part.
- **Stamps are created two ways only:**
  - **`walk`: proof of walk,** paid by any node for the first delivery of another node's sealed block: at most 72 a day across the town (7).
  - **`skill`: the sun's allowance,** paid by the arm game from its sun's purse at a fixed rate, one stamp per R Wh of sunlight, measured by a reference sensor (interactive-arm-game.md 3.3.1; tokenomics.md 2.2). Skill decides who wins a stamp; the sun decides how many exist.
- **Everything else moves or burns stamps, never creates them.** `refund`, `payout` and `redeem` re-issue value that was first spent into the same node; tokens are only paid out against spent digital stamps. A node that issues `refund`, `payout` or `redeem` stamps can never issue more than it holds from earlier spends, and its block shows both sides.
- **Any new way to earn** (a new node, a new proof) must draw from one of these two sources, or the rule is changed here first.
- **Every created stamp is checkable against its source:**
  - a `walk` stamp must match a `deliveries` entry in the same block, pointing at a real sealed block of another node, and a node pays at most 8 a day;
  - `skill` stamps on a day can't exceed that day's sunlight ÷ R, nor the clear-sky ceiling, and the sunlight claimed is cross-checked against the walls' own sun readings (tokenomics.md 2.2);
  - a `redeem` stamp must name a coin on the year's list (4).
  Any node and the explorer can run these checks; a node that breaks them shows in its own signed chain.

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
4. All checks pass: the node writes the spend to flash, then acts (opens a locker, accepts the bid, pays out tokens, posts the shout). The spend goes into its next sealed block (`spent`, 6), with the holder's signature as proof.

Check 4 is skipped only when the issuer's block hasn't arrived yet: a fresh stamp from a distant wall is accepted on its signature alone, as in v0.

### 3.5 Valid until

**Every stamp has a valid-until date.** After it, no node accepts it; it stays in the passport as a faded picture, like a message that has gone.

- **Why:** stamps that are never spent would otherwise pile up and lose meaning (SUNSET.md 3.1). Expiry is a sink that needs no node: unspent stamps leave circulation on their own, and holding stamps is pointless, so people spend them. It is SUNSET's forgetting, applied to money as it is to words.
- **How long:** set in the pilot. **Proposed: 7 days,** the same as messages. Shorter makes stamps hotter; longer lets a visitor who comes back next weekend still spend.
- **Re-issued stamps:**
  - `refund` (outbid at the auction): keeps the **earliest** `exp` of the stamps it replaces, so bidding can't be used to renew stamps.
  - `payout` (to the seller): a **fresh** `exp` from the day of issue. The seller earned them by selling.
  - `redeem` (a token back to digital): a **fresh** `exp` from the day of redemption. Tokens are the deliberate way to keep value (4): the minting fee is the price of saving.
- **Checked at every spend** (3.4, check 0): a stamp past its `exp` is refused before anything else.
- **A bonus for storage:** a node only needs to remember spent stamps until they would have expired, so the spent list stays small (5.3). With a validity of 7 days or less, every stamp is still within the 7 days of full headers, so check 4 is always possible.
- **Tokens** are valid until **31 December** of the year they were issued (4). The ledger can't grow beyond the token stock, so a long life costs the nodes nothing.

---

## 4. Tokens

Tokens are specified in [interactive-token.md](interactive-token.md); this is their data.

- **A token** is a printed plastic coin with a cheap NFC tag (NTAG213 class) inside. **Every token is worth one stamp.**
- **The tag** is written once in a batch, then locked. It holds a link to the website's Verify page carrying the token's **ID** (the tag's own unique ID) and the gettoneria's **Ed25519 signature** over that ID, after the `#` so the browser never sends them. Nothing else: no value, no date, no secret.
- **Genuine** is checkable anywhere, offline, from the gettoneria's public key: by any node, and by the website's Verify page on any NFC phone.
- **Live, and until when,** is in the **ledger**, never on the coin: each ID is *in the hopper*, *issued* (with a valid-until date), *spent* or *souvenir* (interactive-token.md 2.3). The gettoneria and the flip-dot wall keep it live and share every change over ESP-NOW (interactive-flipdot.md 2.1). Redemption is at the gettoneria only; spending tokens is at the flip-dot wall only.
- **Every node keeps the whole coin table** (about 12 KB for 1,000 coins), updated from the `tokens` records couriers bring, and answers *live, as far as this node has heard*. The table is published on the website after a **weekly visit to the gettoneria**, *as of* that date (interactive-token.md 2.8).
- **One batch a year, then closed.** The year's coin list is fixed before the season; its fingerprint is in the season's rules, compiled into every node; **every node refuses any coin ID not on the list,** and a `redeem` stamp names its coin (3.2), so no coins can be added during the year (interactive-token.md 2.2).
- **Valid until 31 December** of the year of issue. Digital stamps are for spending; **tokens are for keeping** (interactive-token.md 2.5).
- **The ledger can't grow beyond the token stock.** It has one line per token made, whatever the minting and however long a token is kept. The physical stock bounds the ledger, and the ledger bounds the money that can be kept. This is a fundamental of the design.
- **On 1 January** every live token's state resets: an expired token brought back goes into the hopper with no stamp (interactive-token.md 2.6).
- **Tokens have no holder key.** They are bearer in the old way: whoever holds the coin holds the stamp. That is the point: they work without a phone.
- **Clones are possible, and accepted.** A cheap tag can be copied. The first use of an ID wins; any later copy is refused and kept by the machine that refuses it. This is part of the recognised bug (5).

---

## 5. Double spends

### 5.1 What can and cannot happen

| Attempt | Result |
| --- | --- |
| A bystander copies a stamp off the air | Impossible: only public keys and one-use signatures cross the air (3.1) |
| A forged stamp | Fails the issuer's signature |
| A stamp from a stolen node key | Fails check 4 wherever the real chain has arrived; the key is replaced (2) |
| A node minting walk stamps without deliveries, or sun stamps beyond its sunlight | Shows in its own signed chain: each `walk` stamp must match a real delivery; `skill` stamps can't exceed sunlight ÷ R or the clear-sky ceiling (3.2) |
| Coins added during the year | Refused everywhere: not on the year's coin list (4) |
| The same stamp spent twice at one node | Refused: on that node's spent list |
| A token cloned and used twice | The first use wins; the second is refused and kept, because the gateway pair shares its ledger live. Clones are accepted as possible (4) |
| **A holder copies their own phone's storage and spends the same stamp at two distant nodes before couriers carry the news** | **Possible.** The one double spend v1 cannot prevent offline (5.2) |

### 5.2 The rule: bound it, prove it, show it

Preventing the last case would need a live link between all spending nodes, which SUNSET doesn't have by design. So v1 accepts it, and makes it **bounded, provable and public:**

- **Bounded.** Every node merges every `spent` record that couriers bring into its own spent list. A copied stamp works only at a node that hasn't yet heard of the first spend, and only until the news arrives: in a busy town, within a day. It takes deliberate effort (copying a browser's storage to a second device) and gains at most one extra use per stamp *at each spending node that hasn't yet heard*: up to about five, of a currency with no cash value. The gettoneria, which turns stamps into year-long coins, is the one to guard (SECURITY.md 4.4).
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
"tokens": [ {"id": "04a2…", "t": 1784026800, "ev": "issued", "exp": "2027-12-31"} ]
```

| Field | Meaning |
| --- | --- |
| `issued` | Every stamp this node issued that day, with its holder key (3.3) |
| `spent` | Every digital stamp spent at this node that day, with the holder's spend signature `ss` (3.4) |
| `tokens` | Gettoneria and flip-dot wall only: tokens loaded, issued, redeemed, spent, sold as souvenirs or kept, by ID (4) |
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
| Skill stamps | One per R Wh of sunlight at the arm (about 35 on a clear summer day), at a rate fixed per season | The sun's purse (interactive-arm-game.md 3.3.1) |
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
| Validity | How long a digital stamp is valid (3.5): 7 days proposed; set in the pilot. Tokens: 31 December of the year of issue |
| Passport backup | Whether a visitor can export their stamps (a QR of the keys) to a new phone. Convenient, and exactly the copy that makes double spends possible |
| Double-spend display | Count only, or the stamp IDs too (they identify no one) |
| Auction siting | Within ESP-NOW range of the gateway, to put large spends on the live list (5.2)? |
| Holder-key library | Which library, its size on the node, and speed on older phones |
