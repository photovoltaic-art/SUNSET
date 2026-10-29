# La gettoneria — the token node, an interactive node on carrier v1

A SUNSET interactive node that **turns digital stamps into tokens, and back.** The visitor spends stamps from their phone and a coin hopper pays out **tokens**: small printed coins, the size of a shopping-trolley token, each with an NFC tag inside. A token can be handed to anyone in the street, with no phone involved. Brought back to the gettoneria, tokens turn into digital stamps again; spent at the flip-dot wall, they buy dots.

*Gettoneria*, like *pizzeria*: the place that makes *gettoni*.

It runs on carrier v1 on the battery tier: the panel feeds a Victron SmartSolar MPPT 75/15 and a 12 V LiFePO₄ battery, with JP1 off and the sun sensor compiled out. The tier is specified in [battery-tier.md](battery-tier.md); the token's data in [stamp-format.md](stamp-format.md) 4.

> Status: draft 1, 24 Oct 2026. **Replaces the print node** (paper stamps from a label printer), whose drafts are in this repository's history. Nothing built. **Nothing here changes the carrier board.**

---

## 1. The idea

- **A mint and a shop.** The gettoneria **converts** digital stamps to tokens and back, and **sells** a token as a souvenir, to keep.
- **Proof of mint.** Every token is genuine because the node signed it, and live because the node issued it. It is the same stamp in a different body.
- **Tokens circulate by hand,** like cash: no phone, no network. That is how people without a phone take part in SUNSET.
- **Nothing is used up.** Tokens are reused: spent at the flip-dot wall, they are collected and come back to the hopper. Where the print node used a roll of labels a day, the gettoneria uses the same few hundred tokens all season.
- **Daylight only,** like all SUNSET business.

### Where it sits in SUNSET

| Node | Proof | Direction |
| --- | --- | --- |
| Wall (message nodes) | walk | earn |
| Arm game ([interactive-arm-game.md](interactive-arm-game.md)) | skill (the sun's allowance) | earn |
| Street auction ([interactive-auction.md](interactive-auction.md)) | bid | transfer; listing fee is a sink |
| **Gettoneria** | **mint** | **convert** (digital ⇄ tokens) and **spend** (souvenir); the minting fee is a sink |
| Flip-dot wall ([interactive-flipdot.md](interactive-flipdot.md)) | mark | spend, tokens only |

The gettoneria **creates no stamps.** Tokens are only ever paid out against digital stamps spent, and redeeming gives back what was spent: the two-source rule holds (stamp-format.md 3.2).

---

## 2. The token

### 2.1 The object

| | |
| --- | --- |
| **Coin** | Printed plastic, the size of a trolley token: about 23 mm across, 2–3 mm thick. Printed both sides. **Face: the Photovoltaic Art logo with row 3 replaced by the town's name, BOSA, and the centre of row 2 left empty: nine squares, one for each panel** ([logos/coin-face.svg](logos/coin-face.svg)), not a node logo: a coin belongs to the town's whole network, not to the gettoneria. Other face: the coin's **number, 0001–1000**, and any further artwork (to be designed, 6). The number works like a banknote's serial: the number to check it by anywhere (2.8) |
| **Tag** | A small round NFC tag (NTAG213 class) set into a recess in the coin, under the print |
| **Value** | **Every token is worth one stamp**, as every digital stamp is. A hopper pays out one kind of coin, so there are no denominations: five stamps are five tokens |
| **Assembly** | By PVA, in **one batch a year,** before the season: write each tag, record it, assemble, load the hopper (2.2) |

- **What the tag holds** (written once, then locked): a link to the website's **Verify** page, with the token's ID and the gettoneria's **Ed25519 signature** over that ID in the part of the address after `#`, which a browser never sends anywhere (stamp-format.md 4). Tapping a token with an NFC phone opens it.
- **What the tag doesn't hold:** value, owner or date. Whether a token is live, and until when, is in the **ledger** (2.3), never on the coin.

### 2.2 The batch: once a year, then closed

1. A roll of NFC tags is written on the bench: each tag gets its link and signature, and is locked so no phone can rewrite it.
2. Each tag's ID is recorded in the batch list against the coin's printed number, state *in the hopper*.
3. Tags are set into the coins; the coins are loaded into the hopper.
4. The batch list goes into the gettoneria's flash, and from there into its sealed block (`tokens`, stamp-format.md 6), so every node learns which IDs exist.
5. **The list's fingerprint goes into the season's rules** ([tokenomics.md](tokenomics.md) 3), compiled into the firmware of all nine nodes, and is published.

**The coin press opens once a year, in public, and then closes.**

- **Every node refuses any coin ID not on the year's list:** the flip-dot wall won't accept it, the gettoneria won't redeem it, a wall's coin check reports it *unknown*, and the explorer flags it.
- **A redeemed stamp carries the coin's ID** (stamp-format.md 3.2), so even a tampered gettoneria redeeming coins that aren't on the list would show, at every node that checks it and in the explorer.
- **The signature alone isn't enough:** whoever holds the gettoneria's key could sign new tags. What closes the press is the frozen list, checked by every node.
- **No coins are added during the year,** by PVA or anyone: lost coins and souvenirs aren't replaced until the next year's batch. The stock can only shrink in a season; the buffer of 500 (2.7) is what absorbs it.
- **Optionally co-signed:** if the nodes are held by separate keyholders, the year's list can need, say, 5 of 9 of their signatures before the rules accept it (tokenomics.md 5).

### 2.3 The ledger

Each token ID has one state at a time, recorded by the gettoneria and the flip-dot wall in their blocks and shared live between them over ESP-NOW (interactive-flipdot.md 2.1):

| State | Meaning |
| --- | --- |
| **in the hopper** | Genuine, not in circulation, worth nothing |
| **issued, valid until 31 December** | In circulation, worth one stamp until the end of the year it was issued |
| **spent** | Used at the flip-dot wall; kept there until the round |
| **souvenir** | Bought to keep; worth nothing; never accepted |

**Valid until 31 December.** Digital stamps fade within days (stamp-format.md 3.5); **a token is valid until 31 December of the year it was issued.** Coins are SUNSET's way to keep value.

**The ledger can't grow beyond the token stock.** It has one line per token ever made, and no more: however many stamps are minted, however long a token is kept, the ledger is as large as the batch list and never larger. That is what lets a token live for a year at no cost to the nodes. It is a fundamental of the design: **the physical stock bounds the ledger, and the ledger bounds the money that can be kept.**

### 2.4 Its weaknesses, stated

- **Cheap tags can be cloned.** A copy of a token's tag, set into another coin, is as good as the original until one of them is used. SUNSET accepts this as part of its **recognised bug** (stamp-format.md 5): the first to be used wins, and the other is refused and kept by the machine that refuses it, which takes it out of circulation.
- **Tokens get lost,** and a lost token's stamp is gone, as with cash. The coin leaves the stock until it turns up.
- **A kept token has more time to be cloned.** The first use still wins; this is minor.

### 2.5 Saving in coins

Because tokens last the year and digital stamps don't, SUNSET has two kinds of money: **stamps to spend, coins to keep.**

- **Saving costs the minting fee.** Anyone holding stamps near their date can turn them into tokens to keep their value. The fee (3.4) is the **price of saving,** like a vault's charge: converting stamps to tokens and back renews them, deliberately, at that price.
- **Savings are capped by the coins.** There are only as many tokens as PVA has made (**1,000**: 2.7), so the town can never keep more than that many stamps' worth, however many are minted. When every token is out, the hopper says *out of tokens* and saving stops until someone redeems.
- **The town's savings are on show.** The gettoneria's page shows **tokens out in town:** the number issued and not yet back. It is the town's savings, counted, with no names (4.4).
- **A coin may come to be worth more than a stamp.** When the hopper runs dry, a token is the only way to keep value, so people might trade one for more than a stamp in the street. SUNSET neither invites nor prevents it (SUNSET.md 2.4): a market finding the price of durability.
- **Traders prefer coins.** A café taking tokens for coffee needn't worry about a date for months. The street economy runs on coins; play runs on stamps.
- **The sink weakens, and the pilot watches it.** Expiry is SUNSET's main sink, and saved coins escape it until 31 December. Late in the season, savings may come back as large bids at the auction: drama, or a problem. Prices and the minting fee are tuned in the pilot.
- **The loop thins.** Kept coins don't come back to the hopper, so the stock in the gettoneria falls over the season, and no coins are added until next year (2.2). *Tokens running low* is a public sign that the town is saving.

### 2.6 The end of the year

- **On 31 December every live token expires.** From 1 January it is worth nothing.
- **Brought back** to the gettoneria or the flip-dot wall after that, an expired token goes back into the hopper with no stamp, *in the hopper* again for the new year.
- **Kept,** it is a keepsake: a coin from that year of SUNSET.
- **Nothing carries across years:** the ledger's live states reset with the year, and the batch list stays as it was.

---

### 2.7 The stock: 1,000 tokens

**Err on the side of more.** The art pieces must never stop for want of coins, and the town's real-world use of tokens (a café's coffee, a trade in the street) shouldn't take coins from the nodes. So the stock is **1,000 tokens: 500 for the core, 500 as a buffer.**

| Part | About | What it's for |
| --- | --- | --- |
| **Core: savings** | 250 | Coins people keep (2.5) |
| **Core: float** | 100 | Coins changing hands day to day, and the flip-dot wall's spending |
| **Core: in transit** | 100 | Spent coins in the flip-dot column, returned **daily** (3.7) |
| **Core: hopper and losses** | 50 | Coins ready in the hopper; souvenirs, losses, the reject box |
| **Buffer** | 500 | Everything beyond the core: **non-core activity** in the town (trading, saving, coins held by businesses), busy weeks, and a reserve so the hopper never runs dry |

- **Redemption can never fail.** Redeeming re-issues digital stamps, which need no reserve, so a rush to redeem is just a busy hour, never a run on the bank. The only shortage possible is the opposite: the hopper running out of coins to mint with, which is what the buffer is for.
- **Where the coins are:** the hopper holds a few hundred (to confirm with Slomatic for these tokens: 4.1). The rest wait in a **reserve tube** inside the enclosure, which PVA tips into the hopper when *tokens running low* appears. All 1,000 are made in the year's one batch (2.2): there is no store of extra coins.
- **The ledger stays tiny:** 1,000 lines, whatever happens (2.3).
- **The cost:** at very roughly €0.50–1.50 a token (tag, plastic, printing, assembly), **€500–1,500** for the stock, in the budget (TASKS.md).

### 2.8 One ledger, held by every node

Because the ledger is only 1,000 lines (about 12 KB), **every SUNSET node keeps the whole coin table**, not only the gateway pair.

- **How it spreads:** every change of state is written into the gettoneria's or the flip-dot wall's sealed block (`tokens`, stamp-format.md 6). Couriers carry those blocks to every node, as they carry everything else, and each node updates its own copy of the table. Nothing new travels and nothing goes online.
- **Where the final answer is:** the gettoneria and the flip-dot wall hold the **live** state, shared within a second over ESP-NOW. They are the only places a coin can be used, so theirs is the answer that counts.
- **Everywhere else, honestly delayed:** any node can answer *"live, as far as this node has heard"*, with the date of its latest news from the gateway, the same honest wording the walls already use for news.
- **Online, as of the last weekly visit:** once a week, PVA (or the gateway's host) makes a **dedicated visit to the gettoneria**, downloads the coin table over its Wi-Fi in a few seconds, and publishes it on the website: numbers and states only, which identify no one. Anyone with internet can look a coin up, clearly marked *as of* that date (SUNSET.md 6.2).

**Three answers, each honest about its age:** live at the gateway; as far as this node has heard at any wall; as of the last weekly visit online (never more than a week old). That is the compromise: a transparent ledger, copied across every node and published, while SUNSET itself stays offline, always.

## 3. The flows

### 3.1 Stamps to tokens (minting)

1. At the gettoneria, the visitor opens the mint page and chooses how many tokens.
2. The stamps are **spent into the node** from the passport page, plus the minting fee (3.4).
3. The hopper pays out the tokens one at a time. Each passes an **NFC reader in the exit chute**; the node records its ID as *issued, valid until 31 December* (2.3), and writes it to flash.
4. The visitor takes them from the cup.

If a token passes the reader unread, the node pays one more and records the miss (6, pilot).

### 3.2 Tokens to stamps (redeeming)

1. The holder joins the gettoneria's Wi-Fi and opens the redeem page on their phone.
2. They **drop the tokens into the slot,** one at a time. The coin acceptor turns away anything that isn't a token, straight back to the return cup (euro coins, foreign coins, washers); each token it accepts rests on the reader's flap and its tag is read (4.5).
3. For each token the node checks: genuine (the signature), *issued*, not past its date.
4. **Valid:** the node issues one digital stamp, carrying the coin's ID, to a holder key the phone makes, with a **fresh** valid-until date from today (stamp-format.md 3.5): the token was the store, and the minting fee paid for it. A flap sends the token **back into the hopper**, *in the hopper* again. **The gettoneria refills itself** from what is redeemed.
5. **Expired** (genuine, issued in an earlier year): back into the hopper, no stamp (2.6).
6. **Not valid** (unknown, spent, souvenir, or a clone already used): the flap sends it to the **reject box**, where it stays until the round. The page says why.
7. **Return mode** (opened from the admin page, by PVA or the gateway's host): spent tokens from the flip-dot wall's column go **back into the hopper**, *in the hopper* again, with no stamp. That is how the column is emptied each day (3.7).

### 3.3 Why tokens are redeemed here only

SUNSET nodes learn of each other's spends only when couriers carry blocks. **Tokens are redeemed only at the gettoneria, and spent only at the flip-dot wall,** and those two share their ledger live over ESP-NOW. So the two places a token can be used always agree, and a token is honoured once at most.

**Checking is everywhere.** Any NFC phone can check that a token is **genuine**: tapping it opens the website's Verify page, which checks the signature against the gettoneria's public key on the phone itself, offline once the page has been saved (SUNSET.md 6.2). Whether it is **live** is known for certain at the gettoneria and the flip-dot wall, as far as it has heard at any other node, and as of the last round online (2.8, 3.6).

### 3.4 The minting fee

Minting costs a small fee in stamps (for example 1 per mint, whatever the number of tokens), set in the pilot. It is the **price of saving** (2.5), and pays for the wear on the tokens and the hopper. It is a **sink.** Redeeming is free.

### 3.5 The souvenir

A visitor can **buy a token to keep,** for a price in stamps set in the pilot. It is paid out like any other, recorded as *souvenir*, and is worth nothing: the stamps spent leave circulation (a sink). The hopper loses one token, not replaced until next year (2.2). **Option:** a separate souvenir coin, of its own design and never on the ledger, so souvenirs don't draw down the hard money.

| Mode | The visitor spends | The hopper pays | Value leaves digital circulation? |
| --- | --- | --- | --- |
| **Convert** | the tokens' value + the fee | that many live tokens | The value moves into tokens; only the fee leaves |
| **Souvenir** | the souvenir price | one souvenir token | All of it: a sink |

### 3.6 Status by token

**Touch a token on the gettoneria's status pad,** a marked spot on its front with a reader behind it. The light shows green (live) or red (not), and the gettoneria's page shows the token's state and valid-until date to anyone on its Wi-Fi. No phone is needed to check, only to read the date on the page.

**At any other node:** type the coin's printed number on the node's page: *live, as far as this node has heard* (2.8). **Online:** the Verify page looks the coin up in the table published after the last weekly gateway visit, *as of* that date.

Useful to anyone accepting tokens, such as a bar near the gettoneria (SUNSET.md 4.2). A bar can also **redeem a token on the spot** the moment it is handed over: a token redeemed this second cannot have been used elsewhere.

**The gettoneria is also the gateway** to SUNSET: the entrance to the installation, paired with the flip-dot wall and placed near businesses with footfall (SUNSET.md 4.1).

### 3.7 The round trip

```
 hopper ──mint──► in circulation ──hand to hand──► flip-dot wall (spent, kept in its column)
   ▲                    │                                         │
   │                 redeem                              the round: PVA brings
   └────────────────────┘                                the spent tokens back
   └──────────────────────────────────────────────────────────────┘
```

**Every day,** after sunset or before opening, the gateway's host (or PVA) empties the flip-dot wall's column into the gettoneria's slot in **return mode** (3.2): the two nodes stand together, so this is a few steps. Only a day's spending is ever out of circulation.

**At each round,** PVA empties the gettoneria's reject box and the flip-dot wall's kept-token box, checks those tokens on a bench reader (removing any duplicate IDs, which can only be clones), and loads the good ones back into the hopper.

---

## 4. Hardware

### 4.1 Parts

| Part | Notes |
| --- | --- |
| **Coin hopper** | **Slomatic X3 EXP**, 12 V version: coins 21–29 mm across, 1.5–3.1 mm thick; about 850 €1 coins (fewer plastic tokens, by volume); pays 3–8 coins a second; **ccTalk** serial interface. **To confirm with Slomatic:** that it pays plastic tokens of this weight reliably (6) |
| **Exit chute reader** | NFC reader (PN532 class) at the hopper's exit, reading each token as it leaves |
| **Status pad** | A third NFC reader behind a marked spot on the front, with a light: touch a token to see whether it is live (3.6) |
| **Redeem path** | Mounted **above the hopper:** slot, a **programmable coin acceptor** taught on sample tokens (non-tokens to a **return cup**), then an NFC reader under a **two-way flap** that holds the coin while its tag is read and tips it to the hopper or the reject box (4.5) |
| **Reject box** | Locked, inside the enclosure; emptied at the round |
| **Tokens** | **1,000**: 500 core, 500 buffer (2.7). Those not in the hopper wait in a reserve tube inside the enclosure, or in PVA's store |
| **Batch writer** | On the bench, not in the node: a USB NFC writer and a script that writes, signs, locks and lists each tag |

### 4.2 Pins

| Use | GPIO | Header | Notes |
| --- | --- | --- | --- |
| Hopper ccTalk TX | 32 | J9 | UART1; ccTalk is one shared data line, so TX and RX meet through a small open-collector interface |
| Hopper ccTalk RX | 33 | J9 | |
| Hopper power | 26 | J9 | MOSFET or relay on the hopper's 12 V; off at boot (pull-down) and between payouts |
| Coin acceptor: token accepted | 36 | J9 | Input only, external pull-up; a pulse per accepted token |
| Coin acceptor: inhibit | 17 | J10 | J10's TX line, free with VE.Direct receive-only. While set, the acceptor refuses everything to the return cup: out of hours, while paying out, on any fault. Unpowered, it returns every coin |
| Redeem flap | 14 | J9 | Solenoid through a MOSFET, with a flyback diode. GPIO 14 toggles at boot: the flap's rest position is *to the reject box*, so a boot glitch can never send a token into the hopper |
| NFC readers (three) | I2C 21 / 22 | J13 | Exit chute, redeem chute and status pad: three PN532 behind an I2C multiplexer (TCA9548A class), shared with the DS3231 (different addresses) |
| Status light | 13 | J9 | Two-colour LED, green or red |
| VE.Direct | 16 RX | J10 | Text mode, receive only |
| Enclosure temperature probe | 4 | J4 / J5 | Heat check |
| Spare | 27 | J9 | Via R19 to the switched 5 V output, unchanged |

### 4.3 Power

| Load | Draw | Notes |
| --- | --- | --- |
| ESP32, Wi-Fi and ESP-NOW on, sunrise to sunset | about 0.5 W | about 6 Wh a day |
| Hopper | 12 V motor, a second or two per payout | powered only to pay out: well under 1 Wh a day |
| NFC readers | about 0.5 W together while on | only in business hours |
| Flap | a pulse per token | negligible |

One of the lightest interactive nodes.

### 4.4 Counting tokens

- The node counts what goes into the hopper (batches loaded, tokens redeemed) and what comes out (paid out), and writes the count to flash.
- **Below a threshold** (set in the pilot), it posts the service notice *tokens running low*; at zero, *out of tokens*, and minting pauses. The hopper's ccTalk status is the backstop if the count drifts.
- *Reject box full* is posted the same way (SUNSET.md 7.1).
- **Tokens out in town:** issued and not yet back, shown on the gettoneria's page: the town's savings (2.5). Live ledger states reset on 1 January (2.6).

### 4.5 The redeem path, top to bottom

```
            slot  (sized to the token)
              │
     programmable coin acceptor ── not a token ──► return cup  (back to the visitor)
              │ token
              ▼
     two-way flap over the NFC reader   (the coin rests while its tag is read)
         │                     │
   valid, or expired     not valid: spent, souvenir,
   (earlier year)        clone already used, unreadable
         ▼                     ▼
       HOPPER             reject box (locked)
```

- **Real money never reaches the reject box.** A €1 coin (23.25 mm) is almost exactly the size of a trolley token, and 20c and 50c are close, so a sized slot alone would take them. The acceptor, taught on sample tokens, sends every non-token back to the return cup before the reader.
- **Out of hours, at a fault, or without power,** the acceptor refuses everything: every coin comes back.
- **Reading at rest, not in flight:** the flap holds the coin over the antenna for the read, then tips. Simpler and more reliable than reading a falling coin.
- **Rejects should be few.** Tokens last the year, so the reject box sees only clones, souvenirs and the odd unreadable tag. Expired tokens from an earlier year go into the hopper.
- **The flap's rest position is towards the reject box,** so a boot glitch never sends a token into the hopper (4.2). If anything that isn't a token ever does reach the reject box, it is logged at the round.

---

## 5. Firmware: the interactive build, gettoneria role

- ccTalk to the hopper: pay one, confirm, count;
- the three NFC readers, and the ledger: states, valid-until dates, written to flash before any token moves;
- the redeem flow and the flap, resting on *reject*;
- ESP-NOW to the flip-dot wall: every change of state shared within a second;
- the status pad, its light and the status page;
- the `tokens` record in the sealed block (stamp-format.md 6).

---

## 6. Open questions

| Question | Notes |
| --- | --- |
| **Token material: hopper, acceptor and NFC together** | The first thing to settle. Hoppers want weight, and coin acceptors recognise coins mainly by their metal, **but metal near an NFC tag detunes it, and a metal ring around the tag stops it working.** Options: plastic only, with a size-and-optical acceptor (not inductive); or a metal weight behind the tag with a ferrite layer and an *on-metal* NFC tag. Ask Slomatic for the hopper's tested range; test acceptor and tag together in the pilot |
| **Artwork** | The design of both faces of the token |
| Tag size | A tag small enough for a 23 mm coin that still reads reliably at the chutes and with phones |
| Souvenir price | How many stamps a token to keep costs (3.5) |
| Minting fee | How many stamps per mint (3.4) |
| Reject box | What happens to its contents: counted and shown, like the double-spend count (stamp-format.md 5.2) |
| Stock size | **Decided: 1,000**, made in one batch a year and closed (2.2, 2.7). The pilot shows how the buffer is used, and whether the hopper and reserve tube hold enough |
| Souvenirs | From the stock (a sink of hard money), or a separate coin never on the ledger (3.5) |
| Late-season savings | Whether saved coins returning as big auction bids is drama or a problem; minting fee tuned in the pilot (2.5) |

## 7. Pilot tasks

| Task | What to settle |
| --- | --- |
| Hopper and tokens | Paying plastic tokens one at a time, all day, without jams |
| Reading in the chutes | Every token read as it falls, at the exit and at the redeem slot |
| Phone taps | Tokens open the Verify page on common iPhones and Androids, and the page checks them offline once saved |
| Clones | Clone a token's tag, use the copy, then the original: the second is refused and kept |
| The round trip | Tokens from the flip-dot wall back into the hopper; duplicate IDs caught on the bench |
| Heat | The enclosure on a summer afternoon: hopper, readers and tokens |
