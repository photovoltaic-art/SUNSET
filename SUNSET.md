# SUNSET — PVA no. 2

SUNSET is the second work of **PVA (Photovoltaic Art)**, after [SUNDIAL](https://github.com/photovoltaic-art/sundial). Where SUNDIAL is about time, SUNSET is about one moment in it: **every day's business closes at sunset.** It grew from **GO TO BED**, a group chat that goes to bed at sunset, whose concept, block format and tests are kept in [gtb/](gtb/GO-TO-BED.md).

SUNSET is **nine recycled solar panels** on the walls of a town, forming a small offline network with its own currency. People earn **stamps** by walking messages between walls and by skill, and spend them at an auction, a mint and a wall of mechanical pixels. Every panel runs on its own sun, on the same carrier board as SUNDIAL, and everything that happens is unattended, anonymous and over by sunset.

> Status: draft 3, 25 Oct 2026 (reviewed after the gettoneria, tokens, expiry, the sun's purse and the shared coin ledger). The five interactive nodes are specified in their own documents, the wall nodes in [wall-node.md](wall-node.md), and the stamps and blocks shared by all of them in [stamp-format.md](stamp-format.md). Tasks: [TASKS.md](TASKS.md). Nothing is built. **SUNSET is year 2 of PVA's growth model: SUNDIAL's own nine panels become SUNSET's nodes** (4 walls by a firmware update, 5 interactive nodes on the battery tier), **each then owned separately** ([GROWTH.md](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md)).

---

## 1. Nine panels

**A PVA work is always nine panels.** Bosa's SUNSET has four wall nodes and five interactive nodes, the reference set; a fork chooses its own nine from the node catalogue ([NODES.md](NODES.md)).

| Panel | Kind | What it does | Specification |
| --- | --- | --- | --- |
| Wall 1–4 | **Wall node** | Message walls: visitors post and read messages; couriers (visitors) carry messages between walls and earn stamps for it. The network's news, and the main source of new stamps | [wall-node.md](wall-node.md) |
| (any wall) | Wall node, on a post | Where there is no wall: a wall node on a post on private ground, above a closed water tank, watering its own flower bed from its sun | [garden-node.md](garden-node.md) |
| Street auction | Interactive | One lot a day in three lit perspex lockers; bids in stamps; the hammer falls at sunset | [interactive-auction.md](interactive-auction.md) |
| Arm game | Interactive | A robot arm in a perspex case; drop a peg in a hole, earn a stamp | [interactive-arm-game.md](interactive-arm-game.md) |
| Gettoneria (token node) | Interactive | Turns digital stamps into tokens (printed coins with an NFC tag) and back, from a coin hopper; sells a token as a souvenir | [interactive-token.md](interactive-token.md) |
| Flip-dot wall | Interactive | Mechanical pixels flipped only with tokens; a column of the spent ones | [interactive-flipdot.md](interactive-flipdot.md) |
| The SUNSET set | Interactive | Plays music at sunset to a registered Bluetooth speaker, only on days the sun has filled its battery | [interactive-audio.md](interactive-audio.md) |

### 1.1 Two power tiers, one board

Every panel uses the **PVA carrier board v1** ([CARRIER.md](https://github.com/photovoltaic-art/sundial/blob/main/hardware/CARRIER.md)), unchanged. **The power tier follows the load, not the role** ([battery-tier.md](battery-tier.md) 1):

| | Wall nodes (4) | Interactive nodes (5) |
| --- | --- | --- |
| Power | The panel straight into the carrier, no battery | Panel → Victron MPPT 75/15 → 12 V LiFePO₄ battery → carrier |
| Awake | Dawn to dusk | Business sunrise to sunset; some keep lights or music after sunset on stored sun |
| Sun reading | The panel's short-circuit current: true light | The Victron's figures: energy harvested |
| Firmware | Wall build | Interactive build, one role per node |

---

## 2. The stamp economy

**One stamp type** everywhere. Each stamp carries the **5 × 5 logo** of the node that issued it, so its origin is visible, but every stamp spends the same. **Every node's logo is unique, and no node's logo is ever the same as the Photovoltaic Art logo:** the PVA mark stands for the project, never for a node or a stamp. Stamps are **bearer**: no accounts, no names. They live in the visitor's **passport page** on their phone, or as **tokens**, coins in the hand (2.3).

### 2.1 Every node is a proof

| Node | Proof | Direction | Notes |
| --- | --- | --- | --- |
| Wall nodes | **walk** | earn, and spend | Stamps for carrying messages between walls; **shouts are paid for**, a sink |
| Arm game | **skill** | earn | Stamps for a peg dropped cleanly, paid from the **sun's purse**; harder holes pay more |
| Street auction | **bid** | transfer | Buyer's stamps go to the seller; the listing fee is a sink |
| Gettoneria | **mint** | convert, and spend | Digital ⇄ tokens; the minting fee and the souvenir are sinks |
| Flip-dot wall | **mark** | spend, **tokens only** | Each flip spends a token |
| The SUNSET set | **sun** | (none) | No stamps: the sun pays for the music |

### 2.2 Stamps in, stamps out

- **In: two sources only.** **Proof of walk** (first deliveries between nodes, at most 72 a day) and **the sun's allowance** at the arm game (one stamp per R watt-hours of sunlight, a rate fixed for the season: about 35 on a clear summer day). Both are limited by the sun: the walls are awake only in daylight, and the arm's stamps are released by the sunlight itself. The whole economic design is summarised in [tokenomics.md](tokenomics.md). **Issuance is energy-backed.** Every other node moves, converts or burns stamps; none creates them (stamp-format.md 3.2).
- **Out (sinks):** paid shouts, the auction's listing fee and burned relists, the gettoneria's fee and souvenirs, every flip of a dot, and **time: every stamp has a valid-until date** (stamp-format.md 3.5), so unspent stamps leave circulation on their own, except those saved as tokens until 31 December.
- **Moving:** auctions move stamps between people; tokens move them hand to hand, with no phone.
- **No cash value, ever.** Stamps cannot be bought or redeemed for money. Their value is only in what they can be used for in the town.

### 2.3 Token money

The gettoneria turns digital stamps into **tokens**: printed coins the size of a trolley token, each with an NFC tag, each worth one stamp. Tokens pass from hand to hand like cash, so **people without a phone can take part:** someone hands them a token, and they spend it at the flip-dot wall, which accepts only tokens. Tokens are reused: spent ones go back to the hopper every day. **Tokens are valid until 31 December; digital stamps fade within days.** So SUNSET has two kinds of money: **stamps to spend, coins to keep.** Saving costs the minting fee, and the town's savings can never exceed the number of coins made: the ledger can't grow beyond the token stock (interactive-token.md 2.5). Tokens can be used in only two places, the gettoneria and the flip-dot wall, which share one live ledger over ESP-NOW, so a token is honoured once at most; every other node keeps a delayed copy (interactive-token.md 2.8).

---

### 2.4 Stamps in the town: a possible outcome, not a feature

Tokens pass from hand to hand, so nothing stops people trading with them outside the nodes. A café owner might shout that today a coffee costs a few stamps, cash only, to bring people in.

- **SUNSET neither invites nor prevents it.** It does not recruit shops, set prices or promise any value. Stamps are never sold or redeemed for money by SUNSET.
- **What a trader can do with stamps taken:** spend tokens at the flip-dot wall, hand them on, or redeem them at the gettoneria and bid, list a lot, buy souvenirs or pay for shouts. The auction is the only place stamps buy *things* from other people.
- **Coins suit trade.** Tokens last until 31 December, so a trader taking them needn't worry about a date for months. And when the hopper runs dry, a token is the only way to keep value, so a token may come to trade for more than a stamp: a market finding the price of durability (interactive-token.md 2.5).
- **What it would mean:** stamps would find a price in the real town, and walking and skill would be worth more. The sun-limited issuance would become the currency's real monetary policy.
- **The trader's risks are the trader's:** a token can be checked as **genuine** with the gettoneria's public key, and checked as live *as far as a wall has heard* or *as of the last weekly visit* online, but only the gettoneria and the flip-dot wall know for certain, so prompt redemption is the protection. Any sale for stamps is the trader's own business, receipts and tax included.

## 3. A day of SUNSET

| When | What happens |
| --- | --- |
| **Sunrise** | The nodes wake. Business opens. Last night's auction winners can collect their lot (until midday) from **wings out**. The flip-dot panel still shows yesterday's picture |
| **Morning** | A newcomer joins the first wall they meet: a passport page, the rules on one screen, and a message to carry. A few minutes' walk later, at the next wall, their first stamp |
| **Through the day** | Walking wall to wall earns stamps. The arm game is the playful detour: a queue, a peg, a cheer when it drops. The lit lockers show today's lot on stage and tomorrow's in the wings, so people come back to check the bids |
| **Solar noon** | The flip-dot wall marks noon: five minutes of every dot flipping black and white (the panel's daily exercise), then the town's picture comes back. Nothing can be flipped while it runs |
| **Afternoon** | If the SUNSET set's battery is full, its shout goes round the walls: *the set plays tonight*. People spend at the gettoneria, for a souvenir or for tokens to take to the flip-dot wall. Spent tokens stack up in the wall's column |
| **Sunset** | **The moment.** The auction's hammer falls. All business stops on every node. If the sun has earned it, the set begins at the sunset spot |
| **Evening** | The lockers glow in their state colours for a few hours; the flip-dot picture holds with no power; the set plays out. The gateway's host empties the flip-dot column into the gettoneria. Nothing can be bought or sold until sunrise |
| **Night** | Dark and silent. The wall nodes are off; the interactive nodes sleep |

### 3.1 How much a day can hold

A first sketch of capacity, from the node specifications: design maximums for a **14-hour summer business day**. Each node's Wi-Fi takes up to 10 phones at once. Real numbers will be set by footfall, long before the hardware; the pilot measures them.

| Node | At once | Per hour (max) | Per day (max) | What limits it |
| --- | --- | --- | --- | --- |
| Walls 1–4 (incl. a garden node) | 10 phones each | ~120 visits each (3–5 minute stays) | ~1,500 visits each; **60 messages** sealed per wall | Wi-Fi; 60 messages per block |
| Walk stamps (all nodes) | — | — | **72 across the town** | Hard cap: 9 nodes × 8 first deliveries (stamp-format.md 7) |
| Arm game | **1 player** (queue of up to ~9) | 20–30 turns | ~150–250 turns; **one skill stamp per R Wh of sunlight** (about 35 on a clear day) | Turn timer, battery, and the sun's purse (interactive-arm-game.md 3.3.1) |
| Street auction: bidding | 10 phones | dozens of bids | Unlimited bidders | Wi-Fi only |
| Street auction: selling | — | — | **1 lot sold, 1 listed, 1 collected** | Three lockers, one stage |
| Gettoneria | **1 at a time** | 30–60 mints or redeems | ~300–500 | One hopper; the **tokens in it** (refilled by redemptions and the daily return; 1,000 in stock) |
| Flip-dot wall | **1 at a time** (one cursor) | 20–40 sessions | ~300–500 sessions; a few hundred to ~1,000 flips | One cursor; noon blocks 5–10 minutes; 784 dots |
| The SUNSET set | Everyone in earshot | — | **1 set**, on days the battery is full | Sun |
| **Whole town** | **~90 phones** | — | Several thousand visits; 1 auction; ~100–110 new stamps on a clear day | Footfall |

**What it shows:**

- **The auction is the narrowest point, by design.** Bidding scales to anyone in range, but **one person sells each day**: about 180 sellers in a season. Ways to treat it are open (10): keep it as the day's event, with sellers queueing through the wings; **auction the slot**, sellers bidding stamps for tomorrow's listing, which turns scarcity into a sink; or a second stage (five lockers, two lots a day) in a later season.
- **The arm could out-mint the walls,** so its stamps are **released by the sun at a fixed rate:** one per R watt-hours of sunlight, into a purse that carries through the day, so a busy morning can't empty the afternoon and walking stays the main way to earn (interactive-arm-game.md 3.3.1).
- **Stamps in against stamps out.** On a busy day the sinks (paid shouts, listing fees, minting fees, souvenirs, flips) may not absorb 100–110 new stamps; **every stamp also has a valid-until date** (stamp-format.md 3.5), so what is not spent leaves circulation on its own. Prices are tuned in the pilot to keep the two in balance.
- **Three nodes serve one person at a time:** the arm, the gettoneria and the flip-dot wall. Each page shows its queue.
- **The hopper's stock** is the gettoneria's real daily limit: redemptions refill it, and *tokens running low* covers the rest (7.1).

---

## 4. Layout

The positions are chosen on site, framed for the best possible outcomes. The logic:

| Panel | Where | Why |
| --- | --- | --- |
| **Gettoneria + flip-dot wall: the gateway** | **As a pair (a hard requirement),** within ESP-NOW range of each other, at the **entrance** to the installation, **near businesses that already have footfall** | The way in to SUNSET (4.1). They share one ledger; the mint, and the wall where its money is spent |
| **Walls 1–4** | Spread to the edges of the installation | Distance is what makes proof of walk mean something: the walls set the shape of the walk |
| **Street auction** | Where people already pass; **within ESP-NOW range of the gateway if possible** | Its catalogue is the street itself; near the gateway, its spends join the live list (stamp-format.md 5.2) |
| **The SUNSET set** | The town's **sunset spot,** a west-facing place where people already gather to watch the sun go down | The set starts at sunset; choose neighbours who can live with an hour of music |
| **Arm game** | In shade | Servos and electronics in a perspex case |
| **Garden node** | In place of a wall, where the layout needs one and there is no wall: private ground, such as a café terrace | A wall node on a post, watering its own bed (garden-node.md) |

The walls and the interactive nodes are interleaved across the area, so walks between walls pass the places to spend. There is no set route (4.3).

### 4.1 The gateway

The gettoneria and the flip-dot wall together are **the entrance to the installation.**

- **The first thing people see:** the flip-dot picture, made by the town a paid dot at a time, and the column of spent tokens beside it. It shows at a glance that something is happening, and that people take part.
- **Where the rules are explained** (5), and where most visitors first see the map.
- **Where tokens meet the town.** Placed near bars, cafés and shops that already have footfall, the gateway draws their customers in, and gives those businesses the infrastructure to take part: tokens redeemed or checked at the gettoneria from their own counter (4.2), and paid shouts to advertise on every wall.

### 4.2 Hosts

Every panel needs a wall, and the owner's consent. Hosting is a fair exchange: wall space and consent for the node's presence. **No money and no endorsement.** From year 2 each node has its own **owner**, who may or may not be the host: anyone can own a node and hold its key, while PVA writes the firmware and rules and manages the website ([GROWTH.md](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md) 3; tokenomics.md 5).

| Host of | What the host gets |
| --- | --- |
| **The gateway** (gettoneria, flip-dot wall) | Two small tasks if they agree: the **daily** return of the flip-dot column, and the **weekly** coin-table download (7.2). In return, the installation's entrance at the door: footfall, and, within the gettoneria's Wi-Fi range (roughly 30–50 m outdoors, less through walls), **live settlement** of tokens from the counter: redeem a token the moment it is handed over, or check whether it is live (interactive-token.md 3.6) |
| **A wall node** | Couriers arriving all day; the town's shouts on the wall; spends and coins known "as far as this wall has heard" |
| **A garden node** | A flower bed that waters itself, and a wall node at their tables; the tank filled from their tap in spring |
| **Any node** | A place on people's daily routes, and the shouts that point people to it |

Hosts are chosen because their wall fits the layout, not the other way round: walls stay spread, and the gateway pair stays together.

---

### 4.3 Routes

**SUNSET has no route.** The map shows where the nodes are, not how to walk between them.

- **Each visitor makes their own.** Which nodes, in what order, and how often depends on what they want: stamps from walking, a turn at the arm game, a bid before the hammer, tokens for the flip-dot wall, the set at sunset.
- **Route planning is part of the daily routine.** The town's state changes every day, and the nodes show it: each wall's dial tone shows which walls haven't heard from each other for a while (where a courier is most needed, and where the first delivery is still to be made), the shouts say what is happening where, and the auction's lockers show what is on stage and in the wings.
- **The same people walk different routes on different days.** Over a season, the paths people choose are the shape of the network.

SUNDIAL is a trail; SUNSET is a town to move through.

## 5. The first five minutes

A visitor meets six kinds of node in one day (walls, the auction, the arm, the gettoneria, the flip-dot wall, the set). Each needs one obvious first step. **The gateway explains the whole economy on one screen** when people arrive, and every wall repeats it for those who start elsewhere:

1. **Earn** by walking messages between walls, or by skill at the arm game.
2. **Spend** at the auction, the gettoneria or the flip-dot wall.
3. **Tokens** work without a phone.
4. **Everything closes at sunset.**

---

## 6. Pages

SUNSET has two sets of pages: those served by the nodes themselves, offline, and a small static website.

### 6.1 On the nodes (offline)

The real dashboard of SUNSET, seen only standing at a node, on its own Wi-Fi:

| Node | Pages |
| --- | --- |
| Wall nodes | The dial tone, messages, paid shouts, the courier ticker, the passport page, and a **coin check** by printed number: *live, as far as this wall has heard* (wall-node.md; interactive-token.md 2.8) |
| Gateway: gettoneria | The one-screen rules; mint, souvenir, redeem; a token's status (interactive-token.md) |
| Gateway: flip-dot wall | The picture and its history (interactive-flipdot.md) |
| Street auction | Today's lot, bidding, claims, the lockers' states (interactive-auction.md) |
| Arm game | The queue and the controls (interactive-arm-game.md) |
| The SUNSET set | Whether tonight's set plays, and past sets (interactive-audio.md) |

### 6.2 The website (online, static)

Published like SUNDIAL's website (GitHub Pages), in Italian and English:

| Page | What it shows |
| --- | --- |
| **The map** | The nine panels with their type, the gateway marked as the way in, and the visitor's own position. **Nodes only, no route** (4.3). Can reuse SUNDIAL's map code |
| **Today** | Sunrise and sunset for the town, computed in the browser: when business opens and closes today |
| **How it works** | The economy in plain words: earn, spend, tokens, sunset; the six kinds of node; hosts |
| **Verify** | The token check: tap a token with an NFC phone and confirm it is **genuine** with the gettoneria's public key. The token's link opens this page with its ID and signature in the part of the address that is never sent anywhere; the check runs entirely on the phone, and the page can be saved to work offline. It also looks the coin up in the **coin table published after each weekly gateway visit** (numbers and states only, identifying no one), and says so: *live as of* that date. The live answer is at the gateway (interactive-token.md 2.8) |
| **Explorer** | The supply, the sun against stamps, the walk network, coins, chain health and double spends, all recomputed from the signed blocks; totals weekly, the full signed record at the season's end ([tokenomics.md](tokenomics.md) 4) |
| **Archive** | Only what is collected from the nodes: the flip-dot picture at each sunset (the season's time-lapse) and simple counts (lots auctioned, stamps minted, dots flipped). **Never messages, and nothing attributable** |

**The honest limit:** the website shows nothing live. The nodes have no internet, so it cannot know today's bids, tonight's set or the current shouts. The map says so: *the network is in the street; this is only the map.*

## 7. Operations in public

**SUNSET runs its own upkeep in the open.** The nodes know when they need care, and they say so publicly, the same way they announce everything else.

### 7.1 Service notices

Any node can post a **service notice:** a free node notice, carried by couriers like a shout, that asks for upkeep.

| Node | Notices (examples) | How it knows |
| --- | --- | --- |
| Gettoneria | *Tokens running low* · *Out of tokens* · *Reject box full* | Counts tokens in and out of the hopper; the hopper's own status as a backstop (interactive-token.md 4.4) |
| Flip-dot wall | *Token column full* | Counts tokens taken |
| Arm game | *Arm resting* | A stall, a joint error or heat, from the arm's own feedback (interactive-arm-game.md 3.5) |
| Garden node | *Tank low* · *Tank empty* · *Soil probe fault* | Its float switches and soil probe (garden-node.md 3.3) |
| Street auction | *Locker B out of service* | Lock or door-switch faults, a door left open, repeated restarts (interactive-auction.md 3.7) |
| Any interactive node | *Battery low* · *Too hot, paused* | The Victron's figures; the enclosure temperature probe |
| Any node | *Not heard from in N days* | Seen at the walls: a node whose updates stop arriving (wall-node.md 1.2) |

- **Service notices don't take the headlines.** The three shouts are paid community advertising; service notices sit on their own line on the dial tone, so upkeep never crowds out the town's news.
- **Worded safely.** A notice says *what* needs care, never *how* a fault could be exploited: "Locker B out of service", not which part failed. Locks are fail-secure, so a faulty locker stays shut.
- **Anyone can read them; the right person acts.** PVA, or a host who has agreed to a small task (7.2), sees the notice on the next wall they pass. The town sees the installation looking after itself.

### 7.2 The rhythm of care

| Task | Rhythm |
| --- | --- |
| **Coin table** | **Weekly:** a dedicated visit to the gettoneria to download the coin table and publish it for the Verify page, never more than a week old. A few minutes; PVA or the gateway's host (interactive-token.md 2.8). Weekly at most: more often would make coin movements easier to link |
| Data collection (archive, counts) | **Fortnightly**, with SUNDIAL's round when both are in the same town. SUNSET produces very little data: a day's flip-dot picture is under 50 bytes, so even a monthly round would lose nothing |
| Battery, Victron, heat and enclosure checks | Fortnightly, on the same round |
| Flip-dot panel | Every round: compressed air, then a vacuum at minimum suction; replace stuck dots. The manual asks for at least every 4 weeks (interactive-flipdot.md 3.7) |
| **Tokens** | **Daily:** the host empties the flip-dot wall's column into the gettoneria in return mode (photograph it first). **Every round:** empty the kept-token box and the reject box, check those on a bench reader (removing duplicate IDs, which are clones), load them back; top up the hopper from the reserve tube (interactive-token.md 2.7, 3.7) |
| **Gettoneria stock** | **Once a year, before the season:** the year's batch of 1,000 coins, written, assembled and loaded by PVA, its list's fingerprint in the rules. No coins are added during the year (interactive-token.md 2.2) |
| Faults | On demand, from the service notice |

## 8. Rules shared by every node

| Rule | Where it is specified |
| --- | --- |
| Business only in daylight; sunset from the clock, as SUNDIAL's seal | battery-tier.md 1.2 |
| **Stamps are created only by proof of walk or the sun's allowance;** every other node moves, converts or burns them | stamp-format.md 3.2 |
| Every digital stamp has a valid-until date a few days ahead (7 proposed); tokens are valid until 31 December, and turning stamps into tokens is the one way to keep value, at the price of the minting fee | stamp-format.md 3.5, 4 |
| The coin press opens once a year and closes: every node refuses coins not on the year's list. The ledger can't grow beyond the token stock; tokens are used only at the gateway pair, which holds the live ledger; every node keeps a copy | stamp-format.md 4; interactive-token.md 2.8 |
| Every node's 5 × 5 logo is unique, and never the same as the Photovoltaic Art logo | stamp-format.md 3.2 |
| Every node seals one signed block a day at sunset, chained to the day before | stamp-format.md 6 |
| All signatures Ed25519; the nine public keys published | stamp-format.md 2 |
| No identities: no accounts, no names; bearer stamps, tokens and the auction's claims | interactive-auction.md 3.5 |
| Nothing reusable crosses the open Wi-Fi to a listener: holder keys for stamps, commit and reveal for the auction's claims. A **fake network** is another matter: it can read a passport (SECURITY.md 4.1) | stamp-format.md 3.1, interactive-auction.md 3.5 |
| A double spend that can't be stopped offline is bounded, proved and shown in public | stamp-format.md 5 |
| Every state change written to flash before it is acted on | interactive-auction.md 3.5 |
| Interactive nodes: JP1 off, sun sensor compiled out | battery-tier.md 1.1 |
| Messages on the walls vanish within 7 days; nothing attributable is kept | wall-node.md 2.3 |

---

## 9. Not in the first season

Candidates for the node catalogue, to consider before SUNSET is licensed ([NODES.md](NODES.md) 3):

- **A miner node:** a Bitaxe on a panel's spare midday power (the SolarSats idea). It needs a pool over the internet, so it would be the one node that is not offline; to decide (gtb/GO-TO-BED.md, other specialized nodes).
- **A second flip-dot wall,** or a reclaimed bus-sign panel instead of a new one.
- **Distributed sound:** phones playing layers of the set (interactive-audio.md 4).

**Set aside:** the **radio node** linking SUNSET to the next village over LoRa (gtb/GO-TO-BED.md). A SUNSET is never linked to another; towns grow by forking ([FORK-TASKS.md](FORK-TASKS.md); [GROWTH.md 5](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md)).

---

## 10. Open questions

| Question | Notes |
| --- | --- |
| Stamp format | Drafted in [stamp-format.md](stamp-format.md); its own open questions (how many days a stamp is valid, passport backup) are listed there |
| Onboarding | The one-screen explanation at the first wall; the first stamp |
| Site plan | Where each of the nine panels goes, against section 4 |
| Permissions | Comune, wall owners, amplified sound, an unattended street auction |
| Build order | Which nodes are piloted first, and in which order the nine are built |
| Budget | First draft: about €12,300 to build with contingency, €12,800 with the first year ([budget/SUNSET-budget.xlsx](budget/SUNSET-budget.xlsx)); estimates to firm up with quotes |
| **The auction slot** | One seller a day (3.1): keep it as the day's event, auction tomorrow's listing slot for stamps, or add a second stage later |
| The arm's exchange rate R | Decided: one stamp per R Wh of sunlight, fixed per season; R measured in the pilot (tokenomics.md 2.2) |
| Rules frozen per season, and the explorer's privacy | Proposed in [tokenomics.md](tokenomics.md) 3 and 4.3 |
| Stamps in and out | Whether the sinks absorb a busy day's new stamps; prices tuned in the pilot (3.1) |
| **Token material** | Hopper weight, coin acceptor and NFC together: plastic with an optical acceptor, or a metal weight behind ferrite with an on-metal tag (interactive-token.md 6) |
