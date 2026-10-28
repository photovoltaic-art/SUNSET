# SUNSET tokenomics — two monies, the sun as the rule, a ledger anyone can check

> Status: draft 2, 27 Oct 2026 (the coin press closed for the year; the sun as rule-maker; nine separate owners from year 2, as in PVA's growth model). Brings together the economic design spread across [SUNSET.md](SUNSET.md), [stamp-format.md](stamp-format.md), [interactive-token.md](interactive-token.md) and [interactive-arm-game.md](interactive-arm-game.md), and adds two decisions: **the arm's stamps at a fixed exchange rate to sunlight**, and **a public block explorer**. Nothing built.

---

## TL;DR

- **Two monies.** **Stamps** are digital, expire within days, and are for spending. **Tokens** are 1,000 physical coins, valid until 31 December, and are the only way to keep value.
- **Stamps come from two sources only, both energy:**
  - **proof of walk:** a courier who first carries a node's sealed day to another node earns a stamp. At most **72 a day**, fixed by the network's shape (9 nodes × 8);
  - **the sun's allowance:** the arm game pays from a purse that fills at a **fixed rate: one stamp per R watt-hours of sunlight**, measured by a reference sensor. No cap is needed; **the sun is the rule-maker:** a clear-sky ceiling and a cross-check against the walls' own sun readings stop any sensor claiming more than the sky gave (enforced in the network, not only by the explorer: SECURITY.md 4.4).
- **Everything else moves, converts or burns stamps.** Expiry is the main sink; fees, shouts and flips are the rest.
- **The coin press opens once a year and closes.** All 1,000 coins are made in one batch before the season; the list's fingerprint is in the rules, every node refuses any other coin, and no coins can be added during the year.
- **Couriers are the miners.** The people who carry the chain are paid by it, like miners propagating blocks.
- **The rules are frozen in firmware for each season.** No setting, key or admin page can change emission during a season; a change needs all nine nodes re-flashed at the spring visit (visible in the chain once blocks carry the rules' fingerprint, proposed in 3).
- **A block explorer on the website** rebuilds every total from the signed blocks, so anyone can check the supply. Live totals weekly; the full signed record once the trail has gone cold.
- **Who holds what:** in year 1 (SUNDIAL, no tokens) PVA owns everything. **From year 2 each node is owned separately, by anyone;** owners hold the keys and decide rule changes and the coin list together; PVA writes the firmware and rules and manages the website (5; [GROWTH.md](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md)).
- **The closest relatives:** Bitcoin for issuance by energy and verification by anyone; Gesell's *Freigeld* (the 1932 Wörgl stamp scrip) for money that expires so that it circulates; Liquid's nine-member federation for blocks signed by authority.

---

## 1. Two monies

| | Stamps (digital) | Tokens (coins) |
| --- | --- | --- |
| Supply | Flows in daily, bounded by the sun | A fixed stock of 1,000 coins |
| Life | A few days (7 proposed) | Until 31 December of the year of issue |
| Character | Soft money, to spend | Hard money, to keep |
| Held | In the phone's passport, by holder keys | In the hand: bearer objects |
| Cash value | None, ever: never bought or sold for money | None, ever |

- **Velocity is forced.** Stamps expire, so they circulate: Gesell's argument, built into the format (stamp-format.md 3.5).
- **Saving has a price and a ceiling.** The one way to keep value is to pay the minting fee and turn stamps into tokens (interactive-token.md 2.5). The town can never save more than 1,000 stamps' worth: **the ledger can't grow beyond the token stock.**

---

## 2. Issuance

### 2.1 Proof of walk

- A node pays **one stamp** to the first phone that delivers another node's **sealed block** of the day to it.
- Nine nodes, each sealing one block a day, each deliverable to eight others: **72 walk stamps a day, at most.** The cap is the network's shape; no parameter sets it.
- **The courier as miner:** Bitcoin pays miners for adding blocks to the chain; SUNSET pays couriers for carrying the chain's blocks across town. Speed matters (only the first delivery pays), work matters (walking), and anyone can do it.

### 2.2 The sun's allowance: a fixed exchange rate

**One stamp for every R watt-hours of sunlight**, with **R fixed in the season's rules** (3).

- **Sizing:** if the arm's panel would gather about 350 Wh on a clear summer day, **R ≈ 10 Wh** releases about 35 stamps. The pilot measures the real figure before R is frozen.
- **No cap:** the sun is the cap. Cloud releases fewer stamps; the season sets the difficulty, as Bitcoin's difficulty adjustment does, but done by the sky.
- **Measured as light, not as harvest.** When the battery is full, the Victron throttles the panel, so the harvest falls on exactly the sunny idle days when sunlight is strongest. Counting harvest would release fewest stamps under the brightest sky. So the arm node carries a **reference sensor**: a small reference solar cell in the panel's plane, read through a current monitor on the I2C header (J13), never throttled. Its reading is converted to **panel-equivalent watt-hours** by a constant measured once in the pilot and frozen with R.
- **The purse:** released stamps drop into the arm's **sun's purse**, carry through the day and empty at sunset (interactive-arm-game.md 3.3.1).
- **Checkable:** each day's sunlight and stamps released are in the arm's sealed block, so anyone can check *released = sunlight ÷ R*, to the stamp (4).

**The sun is the ultimate rule-maker, not the sensor.** A sensor can fail or be tampered with, so two limits sit above it:

- **A clear-sky ceiling** in the season's rules: no day can release more stamps than a cloudless sky at that date, at the arm's site, could give, whatever the sensor reads.
- **A cross-check against the walls:** the four walls measure real sunlight (the panel's short-circuit current, as SUNDIAL's panels do). The explorer compares the arm's sunlight with its neighbours' each day, and flags a claim well above them.

So the most anyone could mint at the arm is what the sky actually allowed that day.

### 2.3 Nothing else creates stamps

Refunds, payouts and redemptions only re-issue value first spent into the same node; tokens are only paid out against spent stamps (stamp-format.md 3.2). Any new way to earn must draw from walk or sun, or the rule changes first.

---

## 3. Who controls what, and freezing the rules

| Lever | Set by | How it can change |
| --- | --- | --- |
| Walk cap (72) | The network's shape | Only by changing the number of nodes: it's structural |
| Sun rate R, and the reference constant | The season's rules | Firmware only, at the spring visit |
| Stamp validity (days) | The season's rules | Firmware only |
| Prices: shout, listing, minting, souvenir | The season's rules | Firmware only |
| Token stock (1,000) | **One batch a year,** made before the season | **Closed for the year:** the list's fingerprint is in the rules; every node refuses any other coin ID, and every redeemed stamp names its coin (interactive-token.md 2.2) |
| The nine node keys | PVA | A replaced key is published with its date (stamp-format.md 2) |

**How the rules are frozen:**

1. **One rules file per season** (for example `rules-S1`), compiled into the firmware: every emission and price constant in one place, published in this repository.
2. **No runtime settings:** no admin page, key or command can change a rule. The firmware changes only with the box opened, a tamper bit and a USB cable, once a year (as SUNDIAL's firmware: SUNDIAL.md 4.4).
3. **The rules' fingerprint in every block** (proposed, for the stamp format's next version): each sealed block carries the hash of the rules it was made under, and nodes refuse blocks and stamps made under other rules. Changing the rules then needs all nine nodes re-flashed together: **a hard fork, visible in the chain**, announced a season ahead.

**What can't be removed:** PVA holds the keys and writes the firmware. With the rules frozen and the record public, that power is **one visible decision a year**, not a dial that can be turned on any day.

---

## 4. The block explorer

A part of the website (SUNSET.md 6.2) that **rebuilds every number from the signed blocks**, so nobody has to take PVA's word for the supply.

### 4.1 How it is built

1. **Collected on foot:** the **weekly** gateway visit downloads every sealed block the gettoneria holds (couriers bring every node's blocks there); the **fortnightly** round fills any gaps from all nine nodes.
2. **Verified by a script:** an import tool checks **every signature, every chain link and every block's rules**, building on GO TO BED's verifier (gtb/testbed/verify.py).
3. **Recalculated, never copied:** every total is computed from the raw headers, never from a node's own counts.
4. **Published as static files** and drawn by the website; a GitHub Action can re-verify everything on each push.
5. **Reproducible:** the signed blocks are published (4.3), so anyone can rerun the script and get the same numbers. *Don't trust, verify.*

### 4.2 What anyone can look up

| Page | What it shows |
| --- | --- |
| **Supply** | Stamps issued by source (walk, sun), spent by sink (shouts, fees, flips), expired, **in circulation now**, and due to expire in the next few days |
| **Sun against stamps** | Each day's sunlight at the arm, the stamps released, and the check *released = sunlight ÷ R* |
| **The walk network** | Which pairs of nodes delivered to each other each day, and how much of the 72 was earned (*61 of 72*): where couriers are missing |
| **Coins** | The 1,000: in the hopper, out in town (the town's savings), spent, souvenirs; the batch list's fingerprint; lookup by printed number (interactive-token.md 2.8) |
| **Chain health** | Each node's chain unbroken, days asleep, the rules on every block, so a rule change shows as a fork |
| **Honesty** | Double spends caught, each with its two signed spends (stamp-format.md 5) |
| **Look up a stamp** | By its ID: issued where and when (to the hour), spent or not, expiry date |

**Never shown:** messages, and anything about people.

### 4.3 Privacy: live totals now, the full record later

The full signed blocks are what make the audit independent, but they also show which stamps were **spent together** (so held by one person) and **where and when each was earned**: together, a trace of one visitor's walk, to the hour. The signature covers the whole block, so nothing can be removed after signing. So:

- **Weekly:** the explorer publishes **totals and per-node counts** (4.2), recomputed from the verified blocks, and stamp lookup by ID.
- **At the season's end:** the **full signed blocks** are published, for anyone to verify everything from scratch, once the trail has gone cold.

---

## 5. Governance: nine owners

> **How the owners vote and what binds them is now drafted as the owners' agreement: [GOVERNANCE.md](GOVERNANCE.md)** (28 Oct 2026). Voting is a signature made at the owner's own node and carried in its sealed block; five of nine is enforced by the firmware; PVA holds no key and no vote after handover.

**Adopted for year 2** in PVA's growth model ([GROWTH.md](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md)): from the conversion, **each node is owned separately, and anyone can own one** (a host, a sponsor, a local group); PVA writes the firmware and rules and manages the website. With each node held by its own keyholder, SUNSET moves from one central bank to a **federation of nine**, like Liquid's federation of functionaries.

**The split, as in Bitcoin:**

| Role | Who | What they hold |
| --- | --- | --- |
| **Writes the rules and firmware** | PVA | The rules file and firmware, published, with reproducible builds and a fingerprint for each release |
| **Holds the keys and decides changes** | Nine keyholders | Each node's own signing key, generated on the node and never seen by PVA; a vote on rule changes and on the year's coin list |
| **Carries, earns and verifies** | Anyone | Walk stamps, the sun's allowance at the arm, and the explorer's script |

**Design tasks this needs:**

1. **Keys generated on each node** at installation, the private half never leaving it; the public halves published.
2. **The rules' fingerprint in every sealed block** (3): nodes refuse blocks and stamps made under other rules, so a change needs the keyholders to re-flash their own nodes, and a refusal is a real fork.
3. **The year's coin list co-signed,** for example 5 of 9 keyholders, before the rules accept it.
4. **Every created stamp checkable against its source** (stamp-format.md 3.2): walk stamps against real deliveries, at most 8 per node per day; sun stamps against sunlight ÷ R, the clear-sky ceiling and the walls' readings; redemptions against the coin list.
5. **Reproducible builds:** a keyholder can rebuild the published firmware and get the same fingerprint before flashing it.

**What it changes:**

- **Better:** no single party can mint, add coins or change the rules; a stolen key affects one node; no one can switch SUNSET off; hosts have a stake.
- **New risks:** collusion (with 5 of 9, five keyholders together can do what one PVA can today); coordination (the spring update and repairs need nine people); incentives (owning a node earns no cash, and paying keyholders in stamps would be a third source, so ownership is its own reward); liability (each keyholder answers for their node).
- **The network stays a federation:** nine named keyholders, not an open network. The permissionless part of SUNSET is the couriers.
- **The artwork:** a PVA work becomes a **commons** in year 2, like the sun that powers it. How the work and PVA's authorship are described from then is open (GROWTH.md 3.4).

---

## 6. Risks

| Risk | What bounds it |
| --- | --- |
| **Discretion** by PVA (prices, rates, batches) | Rules frozen per season (3); one coin batch a year, then closed; shared keys if adopted (5) |
| **A stolen node key** minting stamps | Fails wherever the real chain has arrived; every created stamp is checked against its source (stamp-format.md 3.2) |
| **A faulty or tampered sun sensor** | The clear-sky ceiling and the cross-check against the walls (2.2) |
| **Coins added during the year** | Refused everywhere: not on the year's list (3) |
| **More stamps in than out** | Expiry is the backstop; prices tuned in the pilot, then frozen |
| **Coins hoarded** (the hopper runs dry, coins trade above face) | The 1,000-coin ceiling; the buffer of 500; *tokens running low*; savings shown publicly |
| **Farming** | Walk: the 72 cap. Sun: the fixed rate. Neither grows with effort |
| **Double spends, cloned coins** | The recognised bug: bounded, proved, shown (stamp-format.md 5; interactive-token.md 2.4) |
| **Being mistaken for money** | No cash ever goes in or out; tokens are never sold for euros. Any trade for coins is the trader's own business |

---

## 7. Open questions

| Question | Notes |
| --- | --- |
| **R** | The watt-hours per stamp, from the pilot's clear-day measurements; frozen for the season |
| Reference sensor | Which small reference cell and current monitor; its calibration to panel-equivalent watt-hours |
| Rules in the block | The rules' fingerprint in each sealed block: a field for the stamp format's next version (3) |
| Clear-sky ceiling | The model and its margin, from the pilot's measurements at the arm's site (2.2) |
| Owners | Adopted for year 2 (5): the terms of ownership, and the co-signing threshold for the coin list |
| Souvenir coins | From the stock, or a separate coin never on the ledger (interactive-token.md 3.5) |
| Explorer privacy | Weekly totals and full blocks at the season's end (4.3), or full blocks weekly |
| Validity and prices | Set in the pilot, then frozen in `rules-S1` |
