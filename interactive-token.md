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
| **Coin** | Printed plastic, the size of a trolley token: about 23 mm across, 2–3 mm thick. Printed both sides: the artwork (to be designed, 6) and the gettoneria's 5 × 5 logo |
| **Tag** | A small round NFC tag (NTAG213 class) set into a recess in the coin, under the print |
| **Value** | **Every token is worth one stamp**, as every digital stamp is. A hopper pays out one kind of coin, so there are no denominations: five stamps are five tokens |
| **Assembly** | By PVA, in batches before the season: write each tag, record it, assemble, load the hopper (2.2) |

- **What the tag holds** (written once, then locked): a link to the website's **Verify** page, with the token's ID and the gettoneria's **Ed25519 signature** over that ID in the part of the address after `#`, which a browser never sends anywhere (stamp-format.md 4). Tapping a token with an NFC phone opens it.
- **What the tag doesn't hold:** value, owner or date. Whether a token is live, and until when, is in the **ledger** (2.3), never on the coin.

### 2.2 The batch

1. A roll of NFC tags is written on the bench: each tag gets its link and signature, and is locked so no phone can rewrite it.
2. Each tag's ID is recorded in the batch list, state *in the hopper*.
3. Tags are set into the coins; the coins are loaded into the hopper.
4. The batch list goes into the gettoneria's flash, and from there into its sealed block (`tokens`, stamp-format.md 6), so every node learns which IDs exist.

### 2.3 The ledger

Each token ID has one state at a time, recorded by the gettoneria and the flip-dot wall in their blocks and shared live between them over ESP-NOW (interactive-flipdot.md 2.1):

| State | Meaning |
| --- | --- |
| **in the hopper** | Genuine, not in circulation, worth nothing |
| **issued, valid until *date*** | In circulation, worth one stamp until its date |
| **spent** | Used at the flip-dot wall; kept there until the round |
| **souvenir** | Bought to keep; worth nothing; never accepted |

**Valid until:** a token issued against digital stamps takes the **earliest valid-until date** of the stamps spent for it, so converting to tokens never renews a stamp; redeeming keeps the token's date (stamp-format.md 3.5).

### 2.4 Its weaknesses, stated

- **Cheap tags can be cloned.** A copy of a token's tag, set into another coin, is as good as the original until one of them is used. SUNSET accepts this as part of its **recognised bug** (stamp-format.md 5): the first to be used wins, and the other is refused and kept by the machine that refuses it, which takes it out of circulation.
- **Tokens get lost,** and a lost token's stamp is gone, as with cash. It also expires on its date anyway.

---

## 3. The flows

### 3.1 Stamps to tokens (minting)

1. At the gettoneria, the visitor opens the mint page and chooses how many tokens.
2. The stamps are **spent into the node** from the passport page, plus the minting fee (3.4).
3. The hopper pays out the tokens one at a time. Each passes an **NFC reader in the exit chute**; the node records its ID as *issued, valid until* the earliest date of the stamps spent (2.3), and writes it to flash.
4. The visitor takes them from the cup.

If a token passes the reader unread, the node pays one more and records the miss (6, pilot).

### 3.2 Tokens to stamps (redeeming)

1. The holder joins the gettoneria's Wi-Fi and opens the redeem page on their phone.
2. They **drop the tokens into the slot,** one at a time. Each passes an NFC reader in the chute.
3. For each token the node checks: genuine (the signature), *issued*, not past its date.
4. **Valid:** the node issues one digital stamp to a holder key the phone makes, valid until the token's own date, and a flap sends the token **back into the hopper**, *in the hopper* again. **The gettoneria refills itself** from what is redeemed.
5. **Expired** (genuine, past its date): back into the hopper, no stamp.
6. **Not valid** (unknown, spent, souvenir, or a clone already used): the flap sends it to the **reject box**, where it stays until the round. The page says why.

### 3.3 Why tokens are redeemed here only

SUNSET nodes learn of each other's spends only when couriers carry blocks. **Tokens are redeemed only at the gettoneria, and spent only at the flip-dot wall,** and those two share their ledger live over ESP-NOW. So the two places a token can be used always agree, and a token is honoured once at most.

**Checking is everywhere.** Any NFC phone can check that a token is **genuine**: tapping it opens the website's Verify page, which checks the signature against the gettoneria's public key on the phone itself, offline once the page has been saved (SUNSET.md 6.2). Whether it is **live** only the gettoneria and the flip-dot wall know (3.6).

### 3.4 The minting fee

Minting costs a small fee in stamps (for example 1 per mint, whatever the number of tokens), set in the pilot. It pays for the wear on the tokens and the hopper. It is a **sink.** Redeeming is free.

### 3.5 The souvenir

A visitor can **buy a token to keep,** for a price in stamps set in the pilot. It is paid out like any other, recorded as *souvenir*, and is worth nothing: the stamps spent leave circulation (a sink). The hopper loses one token, replaced at the next batch.

| Mode | The visitor spends | The hopper pays | Value leaves digital circulation? |
| --- | --- | --- | --- |
| **Convert** | the tokens' value + the fee | that many live tokens | The value moves into tokens; only the fee leaves |
| **Souvenir** | the souvenir price | one souvenir token | All of it: a sink |

### 3.6 Status by token

**Touch a token on the gettoneria's status pad,** a marked spot on its front with a reader behind it. The light shows green (live) or red (not), and the gettoneria's page shows the token's state and valid-until date to anyone on its Wi-Fi. No phone is needed to check, only to read the date on the page.

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

At each round, PVA empties the flip-dot wall's column and the gettoneria's reject box, checks the tokens on a bench reader (removing any duplicate IDs, which can only be clones), and loads the good ones back into the hopper, *in the hopper* again.

---

## 4. Hardware

### 4.1 Parts

| Part | Notes |
| --- | --- |
| **Coin hopper** | **Slomatic X3 EXP**, 12 V version: coins 21–29 mm across, 1.5–3.1 mm thick; about 850 €1 coins (fewer plastic tokens, by volume); pays 3–8 coins a second; **ccTalk** serial interface. **To confirm with Slomatic:** that it pays plastic tokens of this weight reliably (6) |
| **Exit chute reader** | NFC reader (PN532 class) at the hopper's exit, reading each token as it leaves |
| **Status pad** | A third NFC reader behind a marked spot on the front, with a light: touch a token to see whether it is live (3.6) |
| **Redeem slot** | A slot sized to the token, a sensor that sees each token pass (optical or a coin validator that handles the token's material), an NFC reader in the chute, and a **solenoid flap**: to the hopper, or to the reject box |
| **Reject box** | Locked, inside the enclosure; emptied at the round |
| **Tokens** | A season's stock: a few hundred, plus spares for souvenirs and losses |
| **Batch writer** | On the bench, not in the node: a USB NFC writer and a script that writes, signs, locks and lists each tag |

### 4.2 Pins

| Use | GPIO | Header | Notes |
| --- | --- | --- | --- |
| Hopper ccTalk TX | 32 | J9 | UART1; ccTalk is one shared data line, so TX and RX meet through a small open-collector interface |
| Hopper ccTalk RX | 33 | J9 | |
| Hopper power | 26 | J9 | MOSFET or relay on the hopper's 12 V; off at boot (pull-down) and between payouts |
| Redeem slot sensor | 36 | J9 | Input only, external pull-up |
| Redeem flap | 14 | J9 | Solenoid through a MOSFET, with a flyback diode. GPIO 14 toggles at boot: the flap's rest position is *to the reject box*, so a boot glitch can never send a token into the hopper |
| NFC readers (three) | I2C 21 / 22 | J13 | Exit chute, redeem chute and status pad: three PN532 behind an I2C multiplexer (TCA9548A class), shared with the DS3231 (different addresses) |
| Status light | 13 | J9 | Two-colour LED, green or red |
| VE.Direct | 16 RX | J10 | Text mode, receive only |
| Enclosure temperature probe | 4 | J4 / J5 | Heat check |
| Spare | 27, 17 | J9 / J10 | 27 via R19 to the switched 5 V output, unchanged |

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
| **Plastic in a hopper** | Hoppers are built for metal coins; light plastic tokens can jam or double-feed. Ask Slomatic for its tested range; the alternative is a heavier token (a brass ring or a metal insert around the tag), which also suits coin validators |
| **Artwork** | The design of both faces of the token |
| Tag size | A tag small enough for a 23 mm coin that still reads reliably at the chutes and with phones |
| Souvenir price | How many stamps a token to keep costs (3.5) |
| Minting fee | How many stamps per mint (3.4) |
| Stock | How many tokens a season needs, given losses and souvenirs |
| Reject box | What happens to its contents: counted and shown, like the double-spend count (stamp-format.md 5.2) |

## 7. Pilot tasks

| Task | What to settle |
| --- | --- |
| Hopper and tokens | Paying plastic tokens one at a time, all day, without jams |
| Reading in the chutes | Every token read as it falls, at the exit and at the redeem slot |
| Phone taps | Tokens open the Verify page on common iPhones and Androids, and the page checks them offline once saved |
| Clones | Clone a token's tag, use the copy, then the original: the second is refused and kept |
| The round trip | Tokens from the flip-dot wall back into the hopper; duplicate IDs caught on the bench |
| Heat | The enclosure on a summer afternoon: hopper, readers and tokens |
