# Wall nodes — the message walls of SUNSET

The four **wall nodes** are the backbone of [SUNSET](SUNSET.md). Each is a recycled panel on a wall, serving its own Wi-Fi with no internet. On it, anyone can read and leave short messages. Visitors' phones carry messages from wall to wall as they walk, and the first to deliver new messages to a wall earns a **stamp**: *proof of walk*. The walls are where most visitors meet SUNSET, where its news travels, and where most new stamps come from.

A wall node is a **wall-tier** panel: the panel straight into the carrier board, no battery, awake from dawn to dusk, the same hardware as a SUNDIAL panel ([SUNDIAL.md](https://github.com/photovoltaic-art/sundial/blob/main/SUNDIAL.md), [CARRIER.md](https://github.com/photovoltaic-art/sundial/blob/main/hardware/CARRIER.md)).

> Status: draft 3, 22 Oct 2026. Blocks and stamps now follow [stamp-format.md](stamp-format.md), which builds on GO TO BED's format v0 ([gtb/FORMAT.md](gtb/FORMAT.md)): messages, replies, limits and fading come from there. Nothing built.

---

## 1. The visitor's experience

### 1.1 Finding a wall

A panel on a wall, with a small plate: the panel's number and its 5 × 5 logo. The visitor joins the panel's Wi-Fi (the network name is on the plate) and the wall's page opens.

### 1.2 The first screen: the dial tone

Every wall opens on its **dial tone:** a simple picture that says the network is alive.

- **Who is here:** how many phones are connected to this wall right now.
- **The network:** the other nodes, each with the **time of its last update** from this wall's point of view. A wall that hasn't heard from another for a long time shows it, so the network's gaps are visible, and so is where to walk.
- **The three shouts:** the town's current news (2.2).
- **Service notices,** on their own line: the installation asking for upkeep, in public (SUNSET.md 7.1).
- **The rules on one screen** (SUNSET.md 5): earn by walking messages or by skill; spend at the auction, the gettoneria or the flip-dot wall; tokens work without a phone; everything closes at sunset.

### 1.3 Reading and writing

- **Read** the wall's messages: whispers left here, and shouts from around the town.
- **Write** a short message. No account, no login. A name is only what someone types into the message.
- **Reply** to a message with one tap.
- **Shout:** pay to promote any whisper to a shout (2.2).

### 1.4 Carrying, without trying

The visitor's phone is a **courier by default**. On connecting to a wall, the page quietly picks up that wall's latest messages; on connecting to the next wall, it delivers them. A **ticker** on the page shows it happening: *picked up 14 messages from Wall 2… delivered to Wall 3.* The visitor only has to walk.

### 1.5 The first stamp

If the visitor is **the first to deliver** a wall's sealed day of messages to another wall, that wall pays a stamp. A newcomer's first stamp is a few minutes' walk from their first wall. It lands in their **passport page** (5.1), stamped with the 5 × 5 logo of the wall that paid it.

### 1.6 What it feels like

A town where the walls talk to each other only through the people walking between them. Messages travel at walking pace; the news is hours old by the time it crosses town, and that is the point. The visitors are the network: **the participants are the internet.**

---

## 2. Messages

### 2.1 Whisper

- A message left at one wall, **readable at that wall.**
- Short, with a fixed length limit (set in the pilot).
- Time-stamped by the panel's own clock, never by the phone.

### 2.2 Shout

- A message **carried to the whole town:** couriers take shouts from wall to wall, so every wall shows them as they arrive.
- **The dashboard shows three shouts** at a time: the town's current headlines.
- **Shouts are paid for.** Anyone can promote any whisper to a shout, their own or someone else's, by spending stamps (the price is set in the pilot). A shout is **community advertising:** whoever wants the town to hear something pays for it, whether it's a party, a lost dog or a café selling coffee for stamps. The stamps spent leave circulation: a sink.
- **Node notices are free.** Interactive nodes shout too: the auction's "Locker A uncollected", the SUNSET set's "the set plays tonight". They enter the network the same way and couriers carry them.

### 2.3 Rules

| Rule | Detail |
| --- | --- |
| **Open posting** | Anyone in range can write; constrained length |
| **No identity** | Anonymous, or a name typed into the message. "Don't trust anything that is written" |
| **No moderation** | Nothing is checked or removed by hand |
| **Seven days** | Every message is gone within 7 days. This is a feature, not a bug |
| **Nothing attributable** | No user data is held; no phone identifiers are stored with messages |
| **Text only** | Shown as text, never as HTML, on every page (as SUNDIAL's visitors' book, SUNDIAL.md 4.2) |

---

## 3. Couriers and blocks

### 3.1 Blocks

Each node seals **one block a day, at sunset:** that day's shouts, and in its header the stamps it issued and spent. Each block is signed by the node and chained to its previous day, so a courier can lose a block but never forge or alter one (stamp-format.md 6; v0: [gtb/FORMAT.md](gtb/FORMAT.md)). A day's news leaves a wall after it has sealed, so the network's shortest delay is one night.

### 3.2 The courier's journey

1. **Pick-up.** A phone connected to Wall A receives the sealed blocks A holds that the phone lacks: A's own and other nodes'.
2. **Carry.** The phone keeps it in the browser while the visitor walks.
3. **Delivery.** At Wall B, the phone hands its blocks over. B checks each seal, keeps what is new, and gives the phone what B holds in return.

Every SUNSET node, wall or interactive, takes part: interactive nodes post their shouts into a block and receive the town's news and stamp records the same way.

### 3.3 Proof of walk

- **The first delivery** of a node's sealed block to another node earns the courier a stamp from the receiving node: one per block per node, so at most 72 a day across the town. Shuttling between two walls earns nothing more once the blocks are delivered, which is the farming limit.
- **Valid between any two nodes:** there is no fixed route and no centre. Two walls are already a network.
- **Permissionless:** anyone walking with a phone can be a courier; no sign-up.
- **Bounded by the sun:** wall nodes are awake only in daylight, so the number of deliveries, and of stamps paid, follows the length of the day.

### 3.4 Why it works on paper and fails gently

- **No backhaul:** nothing reaches the internet. If no one walks, the walls drift apart, and the dial tone shows it.
- **Slow by design:** news is as fast as feet.
- **Lost phones lose nothing:** a courier's block is a copy; every node keeps its own.

---

## 4. Hardware and power

| | Wall node |
| --- | --- |
| Board | PVA carrier v1, wall build, unchanged |
| Power | The panel straight into the carrier; no battery |
| Awake | Dawn to dusk; off at night |
| Wi-Fi | Open access point, up to 10 phones at once, plain HTTP |
| Clock | DS3231 with coin cell: every message and stamp is time-stamped by the panel |
| Storage | LittleFS for messages (7 days), blocks and the stamp records |
| Sun sensor | **Used:** the panel's short-circuit current, as on SUNDIAL panels: the walls' record of real sunlight, against which the arm's sun claim is cross-checked ([tokenomics.md](tokenomics.md) 2.2) |

A wall node draws well under 1 W. It needs nothing that a SUNDIAL panel doesn't already have.

---

## 5. Stamps

Specified in **[stamp-format.md](stamp-format.md)**, shared by every node. In short:

- **A walk stamp** is paid by a wall to the first phone that delivers another node's sealed block to it: at most 72 a day across the town (stamp-format.md 7).
- **Holder keys:** the phone makes a key for each stamp and spends it by signing, so nothing worth copying crosses the open Wi-Fi (stamp-format.md 3.1).
- **Node logos:** each stamp shows the 5 × 5 logo of the node that issued it; every logo is unique and never the PVA logo (stamp-format.md 3.2).
- **Walls are spending nodes too:** shouts are paid in stamps, checked and recorded spent like any other spend (stamp-format.md 3.4).

### 5.1 The passport page

- A page on the visitor's phone, a grid of boxes **filled by stamps** as they are earned, each showing the logo of the node that paid it.
- **Saved as images,** so the passport can be shown or shared with nothing installed. The images are a picture of the stamps; the stamps themselves, and their keys, live in the browser (stamp-format.md 8).
- The auction's collection claims are kept here too.

---

## 6. Open questions

| Question | Notes |
| --- | --- |
| **Phone storage** | Couriers carry blocks in the browser. The captive-portal pop-up browser on some phones keeps no storage between networks; visitors may need to open the page in their normal browser. **The carry test is ready to run:** [gtb/carry_test/TEST.md](gtb/carry_test/TEST.md) |
| Message length | 140 characters in v0; confirm in the pilot |
| Shout price | How many stamps a shout costs, and whether the price rises when many shouts are waiting |
| Wall plate | Number, logo, network name, and a QR code. **The node's logo sits in the centre of the QR code** (error correction level H), so the plate shows one mark that people recognise and any phone can scan; the same plate as SUNDIAL's, which opens `/?p=N` ([logos/](logos/README.md)) |

## 7. Pilot tasks

| Task | What to settle |
| --- | --- |
| Courier storage | Blocks survive from one wall to the next on common phones and browsers |
| Block size | How large a block grows over 7 days of messages, and how long a hand-over takes |
| Dial tone | Readable at a glance by a first-time visitor |
| First stamp | A newcomer earns one within a short walk, without instructions |
| Seven-day expiry | Messages and records drop off cleanly, on every node |
