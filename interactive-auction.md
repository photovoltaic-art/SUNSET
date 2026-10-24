# The street auction — an interactive node on carrier v1

The first of SUNSET's interactive nodes: **the street auction.** It runs on carrier v1 on the battery tier ([battery-tier.md](battery-tier.md)).

The interactive nodes belong to **SUNSET** (PVA no. 2, formerly GO TO BED), a network of panels that carry messages and stamps between walls. Where SUNDIAL is about time, SUNSET is about one moment in it: every day's business closes at sunset. They are a use of the PVA carrier v1, like the three layers of SUNDIAL ([SUNDIAL.md](https://github.com/photovoltaic-art/sundial/blob/main/SUNDIAL.md)).

> Status: draft 2, 22 Oct 2026 (three lockers; business in daylight only; evening lights on the battery). Concept and rules settled in discussion; nothing built. Nothing here changes the carrier board.

---

## 1. The auction on the battery tier

The auction is an interactive node: carrier v1 on the battery tier, specified in [battery-tier.md](battery-tier.md) (two tiers, JP1 off, sunset as the close of business, the Victron data, wiring). Particular to the auction:

- **The battery keeps the lockers lit after sunset,** about four hours as the starting point. In Sardinia the street is busiest in the evening, so the lockers stay lit: the result of the day's hammer, and tomorrow's lot waiting in the wings, readable from the pavement. Nothing can be done until sunrise; then the lights go out and the ESP32 deep-sleeps until sunrise.
- **The lighting routine is not fixed here.** Which lockers are lit, in which colours, how bright, by day or only in the evening, and for how long, is a firmware setting, tuned on the built hardware during the pilot (6).

---

## 2. Carrier v1 on the battery tier

### 2.1 Wiring

As in [battery-tier.md](battery-tier.md) 2.1. The auction's off-board driver (2.3) hangs on the fused 12 V line from the Victron's load output.

### 2.2 Pins for the auction node

All from the spare-pins header J9 and the UART header J10. Nothing on the ESP32 strapping pins.

| Use | GPIO | Header | Notes |
| --- | --- | --- | --- |
| Lock, locker A | 26 | J9 | To the driver's MOSFET gate; pull-down on the driver board |
| Lock, locker B | 13 | J9 | Same |
| Lock, locker C | 27 | J9 | Same. **Remove R19** on the carrier: this gives up the switched 5 V output (U4), which nothing on the battery tier uses |
| Door switch, locker A | 32 | J9 | Reed switch to GND, pull-up to the header's 3V3 |
| Door switch, locker B | 33 | J9 | Same |
| Door switch, locker C | 36 | J9 | Same; input only, and has no internal pull-up, so the external pull-up is required |
| Interior lights (LED data) | 14 | J9 | One data line for all three lockers (addressable strips chain). Through a 3.3 → 5 V level shifter on the driver board. GPIO 14 toggles briefly at boot: the lights may flicker on reset, the locks never do |
| VE.Direct | 16 RX, 17 TX | J10 | Divider on RX if the Victron sends 5 V |
| Clock | 21 / 22 | on board | DS3231, already fitted |
| Temperature probe | 4 | J4 | Inside the locker housing: the heat check (3.6) |

Every J9 pin is now in use. More lockers, or a switch for the light supply, would come from an I2C port expander (MCP23017 class, 16 pins) on the I2C header J13, with no other change.

### 2.3 The off-board driver

A small board beside the carrier, on the 12 V line:

- 3 logic-level N-MOSFETs with flyback diodes and gate pull-downs, one per lock;
- a 12 V → 5 V buck for the interior lights (addressable RGB, a short strip per locker);
- a 74AHCT125-class level shifter for the LED data line;
- screw terminals for the locks, lights and door switches.

**Locks are fail-secure:** solenoid latches that stay locked without power and open on a short pulse (about 1 s). Doors stay shut through any fault, reboot or flat battery.

### 2.4 Power, roughly

| Load | Draw | Per day |
| --- | --- | --- |
| ESP32, Wi-Fi on, sunrise to sunset | ~0.5 W | ~6 Wh over 12 h |
| ESP32, Wi-Fi off, evening lights | ~0.1–0.2 W | < 1 Wh |
| Interior lights, three lockers, dimmed | ~1–2 W per locker | the largest item: ~12–24 Wh for four evening hours, plus any daytime lighting. An estimate until the pilot sets the routine |
| Light strips switched to black overnight | standby of the LED chips | ~1–3 Wh; removable later with a supply switch on an expander pin |
| Locks | ~0.5–1 A at 12 V for ~1 s, a few times a day | negligible |

Roughly 30–40 Wh a day. A 12 V 20–40 Ah LiFePO₄ pack (about 250–500 Wh) and a recycled panel cover this with several dull days in reserve. Size the battery to the lights. If the charge state falls low, the evening lights are the first thing to shorten.

---

## 3. The street auction

A fully automated street auction: three lockers with lit interiors and transparent perspex doors, one lot a day, settled in SUNSET stamps. Nobody attends it. **The catalogue is the street itself:** everything for sale is visible from the pavement all day.

### 3.1 Stage and wings

Three lockers, each with one job a day. The roles rotate at every sunrise:

| Locker | Today's job | At next sunrise becomes |
| --- | --- | --- |
| **Wings in** | Takes tomorrow's lot, any time from sunrise to sunset (1 stamp to list) | Stage |
| **Stage** | Today's lot on auction; the hammer falls at sunset | Wings out |
| **Wings out** | Yesterday's lot: the winner collects until midday, then the seller takes it back until sunset | Wings in (empty) |

One lot is auctioned per day. If nobody lists a lot, tomorrow's stage is empty and it is a rest day.

Each door has one job a day, so a seller can list at any hour of daylight, and the winner and the seller never compete with a new listing for the same door.

### 3.2 A lot's life

| When | What happens |
| --- | --- |
| Day N, sunrise to sunset | The lot is on the **stage**. Anyone at the node can bid in stamps |
| Day N, sunset | **The hammer.** Bidding ends; no further bids. The highest bid wins |
| Day N, sunset to four hours after | Business is closed. The stage locker shows *sold* or *unsold* in its light |
| Day N+1, sunrise to midday | The locker is now **wings out**. The winner collects with their winning-bid claim |
| Day N+1, from sunrise | The seller can redeem the winning stamps at any time in daylight (no locker needed; the node holds them) |
| Day N+1, midday to sunset | If not collected, the winner forfeits: the seller keeps the stamps **and** can take the goods back with their seller claim. The node posts an automatic **shout** ("Locker A uncollected"), which couriers carry to every wall |
| Day N+1, still full at sunset | The lot is abandoned. At the next sunrise it **goes back on stage**, relisted automatically; its proceeds are burned |

A lot with no bids at the hammer goes to wings out for the seller to take back, under the same timings, and is relisted the same way if still there at sunset.

**When an abandoned lot is relisted,** two lots want tomorrow's stage: the relisted one and the new one waiting in wings in. **The relisted lot goes on stage first; the new lot waits one more day in wings in,** and no new listings are taken until it moves. It is rare, and the rotation stays intact.

### 3.3 Locker states

| State | Light colour | Who can open the door |
| --- | --- | --- |
| Empty (wings in) | (dim or off) | A seller, for 1 stamp |
| On stage | for sale | Nobody |
| Sold, awaiting collection | sold | The winner's claim, until midday |
| Uncollected or unsold | return to seller | The seller's claim, until sunset |
| Listed, waiting in wings in | coming tomorrow | Nobody |
| Relisted | for sale (next day) | Nobody |

**The light is the message.** Without accounts or contact details, the node cannot tell anyone anything directly; the colour of each locker, readable from the street, is the status. The seller claim also shows the lot's status on the node's page, and uncollected lots are announced by shout.

After sunset the lights can show the day's result to the evening street (1); the colours and routine are set in the pilot (6).

A door switch on each locker confirms that the door was opened and closed again, so each locker resets itself.

### 3.4 Stamps and settlement

- **Listing costs 1 stamp.** It is the auction's only sink, apart from burned relist proceeds. Everything else is a transfer from buyer to seller.
- **A bid needs the stamps in hand.** Bidding spends them into the node (marked spent on the public list) and gives the bidder a bid receipt.
- **Outbid:** the node at once issues fresh stamps of the same value back to the bidder.
- **Won:** the stamps stay with the node until the seller redeems them, as fresh stamps.
- **Why spent, not "locked":** SUNSET nodes learn of each other's spends only when couriers carry blocks between walls. A stamp merely marked as locked at the auction would still be spendable everywhere else. Spent into the node, it is recorded spent and its replacement exists only at the node. To the user it behaves exactly like "locked until paid or returned". The one double spend no offline node can stop (a holder copying their own phone) is bounded and made public (stamp-format.md 5).

No separate escrow is needed: **the firmware is the escrow.** Every lot ends with the seller holding either the stamps or the goods (or, if the winner never comes, both).

### 3.5 Claims on an open network

The node's Wi-Fi is open and plain HTTP: anything sent can be read by anyone in range (SUNDIAL.md 4.3). A claim sent in clear could be copied by a bystander, who would reach the locker first. So claims are **commit and reveal**:

1. **At bid time** (or at listing, for the seller), the phone makes its own random secret and sends only its hash. The node records the hash against the bid or lot and signs the receipt (HMAC-SHA256 with a key only the node holds: only this node ever checks it). **Stamps themselves are not claims:** they use holder keys and Ed25519 ([stamp-format.md](stamp-format.md) 3).
2. **At collection,** the phone reveals the secret. The node checks it against the hash, opens the door at once and marks the claim used.

Anyone listening sees the secret only at the moment it stops being worth anything. Claims are bearer: whoever holds the phone's secret holds the claim. Claims are saved in the visitor's passport page beside their stamps.

**On the node:** flash encryption on, so a stolen board does not give up the signing key. Every state change (bids, claims issued and used, locker states) is written to flash before it is acted on, so a reboot or brown-out resumes exactly where it was and no door ever opens twice.

### 3.6 Practical rules

- **No food, liquids or batteries.** A lit perspex box in the Sardinian sun is an oven. Choose a shaded or north-facing site; the temperature probe sits inside the housing and the page shows the reading.
- **Size limit:** whatever fits the locker and closes the door.
- **Visibility is the moderation.** Nothing can be hidden behind perspex, and listing costs a stamp, so dumping has a price.
- **Client limit:** up to 10 phones at once; pages keep connections short (bid, then go).

---

### 3.7 Service notices

The auction watches its own lockers and posts a service notice (SUNSET.md 7.1) when something needs care:

- a lock that doesn't confirm (the door switch shows no opening after a pulse);
- a door switch that reads open with no lock pulse (a forced or badly closed door);
- a door left open after a collection or listing;
- repeated restarts, a low battery or excessive heat.

The notice names only the locker ("Locker B out of service"), never the fault. A locker in fault is taken out of the rotation: if it was the stage, that day is a rest day; if it holds a lot, the lot stays safe behind its fail-secure lock until PVA attends.

## 4. Firmware: the interactive build

Same firmware family as the wall nodes, built with:

| Setting | Wall build | Interactive build |
| --- | --- | --- |
| `SUN_SENSOR` | 1 | 0 (GPIO 25 never driven) |
| `PANEL_SENSE` | panel voltage, dawn and dusk gates | battery voltage, cross-check only |
| `VE_DIRECT` | 0 | 1, on UART2 (GPIO 16/17) |
| Close of the day | dusk from panel voltage | Bosa's sunset from the clock: Wi-Fi closes, the evening lighting routine runs, then deep sleep until sunrise |
| Node role | wall | auction (locks, door switches, lights) |

New for the auction: the three-locker rotation (3.1) and locker states (3.3), bid handling and stamp issue (3.4), commit-and-reveal claims (3.5), the automatic shout, and the colour code on the lights.

---

## 5. Open questions

| Question | Notes |
| --- | --- |
| **One seller a day** | The auction's capacity limit (SUNSET.md 3.1). Options: keep it as the day's event; auction tomorrow's listing slot for stamps (a sink, still one seller); a second stage later |
| A maintenance path for a dead controller | BOX's rule is "no override, ever", but a dead board would trap a lot. Decide between that purity and a sealed, tamper-screwed manual release |
| Exact cut-off times | Midday for collection, sunset for seller returns: confirm against how people actually use the street |
| Bid steps and opening bid | Minimum increment; whether the seller can set a reserve |
| Comune permission | An unattended street exchange is the piece most likely to need a word with the comune before Bosa 2027 |
| Stamp format | Drafted: [stamp-format.md](stamp-format.md). Siting within ESP-NOW range of the gateway would put the auction's spends on the live spent list (stamp-format.md 5.2) |
| Prior art | Check "world's first fully automated street auction" before using it publicly |

---

## 6. Pilot tasks

Settled on the built hardware, not on paper. The firmware is written so each of these is a setting, not a rebuild.

| Task | What to settle |
| --- | --- |
| **Lighting routine** | Which lockers are lit and when (day, evening, both), colours for each state, brightness, how long after sunset (about four hours to start), and how the routine shortens when the battery is low |
| Cut-off times | Midday for collection and sunset for seller returns, against how people actually use the street |
| Heat | Temperature inside the housing on a summer afternoon, with and without daytime lighting |
| Power budget | The real daily draw against the estimate in 2.4, and the battery size it calls for |
