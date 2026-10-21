# PVA no. 2 — GO TO BED

*Concept, on hold. Opened 21 Oct 2026. Not yet a project: this note keeps the idea and its open questions.*

## The idea

A group chat that goes to bed at sunset.

A set of retired PV panels, each with a small board behind it, forms an offline radio network across a town. Anyone with a phone can join a panel's Wi-Fi and take part in one shared conversation, **without a SIM, an internet connection, an account or an app**. The panels pass messages between each other by radio. They run only on their own sunlight: when the light goes, the network goes to bed, and wakes again with the sun.

It is both a **proof of concept for minimal, unattended comms infrastructure** and an **artwork**. The point is that it is unattended and only powers up in the day.

## What it is, and is not

- **A group chat**, not a notice board: one shared room, open to whoever is in range of any panel, at the sun's pace.
- **Store and forward:** messages written while some panels sleep are passed on when they wake. Delivery can take hours. That is part of the work.
- **Unattended:** no operator, no server, no backhaul.
- **No app (aim):** each panel serves the chat as a web page through its own Wi-Fi, the way SUNDIAL serves its dial.

## The tone

Not a record of the day, like SUNDIAL's dial, but a **dial tone you can see**: the first thing on screen when a phone joins a panel's Wi-Fi, answering one question at a glance: *is anyone there?*

- **The tone:** a slow pulse at the centre while the network is awake. No pulse, no network: it has gone to bed.
- **Here:** small marks round the pulse, one per phone connected to this panel now (up to about 10).
- **The town:** a ring of nine points, one per panel, showing **how fresh each panel is, as far as this panel knows**: bright for news from today, fading for older. Without radio links a panel can only learn about the others from what visitors carry, so the ring is the town as this panel last heard it.
- **Last update:** the date and time this panel was last brought up to date by a visitor, and how long ago the last message reached it.

That is all: live, simple, wordless enough to read in any language. Its job is to give a **reason to participate**: someone is listening, the town is awake, a message sent now will travel. Below it, the chat.

Bedtime is part of the tone: as a panel's light fails, its pulse slows and its own point dims, then the page says goodnight. Messages left after that wait for the morning.

## The participants are the network

The public are the messengers. A phone that joins one panel picks up what that panel knows; when its owner joins another panel, the phone hands it on. Walking the town moves the conversation. **The participants are the internet.**

- **Blocks of messages.** Each panel gathers the day's messages into a block and seals it at bedtime, as SUNDIAL seals its dial. Each block carries the fingerprint (hash) of the panel's previous block, so the days form a chain, and a missing or altered day shows.
- **Messages are signed,** so a carrier can lose a message but cannot forge or alter one.
- **The clock travels too.** Phones carry the time between panels, as well as messages, so the town keeps time together. Each panel keeps its own clock module and treats carried time as a hint, never an order: one phone can't reset the town.
- **A slow version of Bitcoin's nodes,** in spirit: copies spread by gossip until every panel holds every block. Unlike Bitcoin there is nothing to agree on and nothing to spend; every message is simply added. Panels only ever merge what they are given.
- **Proof of walk.** A message crosses town only if someone carries it, or a radio link reaches. The network's speed is the speed of people, and of the sun.
- **Permissionless.** Anyone can carry; no one needs to be chosen, registered or known. Every walk counts, even between just two panels: each carry brings two panels closer.
- **The imbalance shows.** Each panel shows when it was last updated, and its ring shows how fresh the others are. Busy panels in the centre stay current; outlying panels that few people visit fall behind, and everyone can see it. That gap is an open invitation to walk to them.
- **The whole round.** When one phone visits all nine panels on the same day, the town is whole: every panel holds everything. The day is marked as a *whole day* in the record (a count, never who). Anyone can make it happen, by choosing to walk the full round.

**How a phone carries it (to test).** All the panels answer at the same local web address, so a web page stored by one panel's visit is readable at the next: the phone's browser storage is the courier's bag, with no app. The catch: some phones' Wi-Fi pop-up windows keep no storage, so carrying may need a full browser. Test this first.

**What it may change:** if people can carry the network, **the radio between panels becomes optional**: an accelerator where links reach, not a requirement. A people-powered GO TO BED could run on hardware close to the SUNDIAL carrier, with the radio added later or only where walls can hear each other.

## Accounting layer: a sat per delivery (later, optional)

An idea to keep apart from the core work: each time a carrier brings a panel a block it did not have, the carrier earns a sat.

**The difficulty:** the panels are offline, so no payment can settle at the moment of delivery. The answer is to **account offline and settle later**, in two steps:

1. **Receipts (offline, no money):** the panel signs a small receipt: *this phone's temporary key delivered block B to panel P at time T.* The phone keeps its receipts in browser storage, like stamps in a pilgrim's passport: one per panel, per new block. This works with no internet and no money, and is worth building even on its own.
2. **Settlement (online, later, optional):** receipts are redeemed for sats wherever there is internet, through a Lightning or ecash (Cashu) wallet; for example a page on the website, or a partner in town. Alternatively, each panel could hold a small float of pre-minted ecash, loaded on the round, and hand over a token with each receipt; the visitor redeems it later in any Cashu wallet.

**Rules that keep it honest:**

- **Only new blocks count:** a panel pays only for sealed blocks it did not already hold. Blocks are sealed by the panels themselves at bedtime, so visitors cannot manufacture them; walking back and forth between two panels earns nothing after the first trip.
- **The incentive points the right way:** stale, outlying panels lack the most blocks, so they pay the most. The money rewards exactly the walks that heal the imbalance.
- **A cap per phone per day**, and a fixed total per day: the most the network can ever pay is the number of new blocks it can absorb.
- **A small float:** a panel holding ecash is a small wallet on a wall; keep the float symbolic, so losing a box loses little.

**Questions:** who funds the sats (PVA, sponsors, the town)? Does money change why people take part, from play to farming? Should amounts stay symbolic (one sat) so the receipt matters more than the value? The rules on giving away bitcoin from a public artwork in Italy need checking before step 2.

**Order:** receipts first, as part of the work; settlement only after an event has shown how people carry.

## Building on SUNDIAL

- **Same principles** ([MANIFESTO](../MANIFESTO.md)): the panel powers only itself; offline by nature; the work keeps no one; slow.
- **Same base hardware where possible:** the SUNDIAL carrier's power path, sun sensor and clock, with lessons from its v1 bench test.
- **The SUNDIAL carrier already has the hooks:** an AUX output that takes spare panel power through its own converter, a switched 5 V output, and spare SPI/UART/I²C pins. The firmware sheds AUX loads the moment the panel voltage sags, so the board always has priority.

## Technical direction (to test, not decided)

- **Board:** ESP32, probably an ESP32-S3 with PSRAM for message storage and a larger web client (SUNDIAL v1 uses the original ESP32).
- **Panel-to-panel radio:** best in class for range at low power, most likely **LoRa** (SX1262 class). Alternative: ESP-NOW long-range mode, if the walls have line of sight. LoRa carries little data, which suits short text.
- **Comms scaled to the available power:** the board already measures the panel's sunlight every 10 s. The radio's transmit power, duty cycle and how often it relays could follow that reading: more sun, more talk; weak sun, a whisper; no sun, sleep. Higher-power radio stages could run from the AUX output.
- **Messages:** short text, signed and with an expiry. Nostr's event format (signed, open, with expiry) is a candidate; a minimal Nostr relay already runs on an ESP32-S3 ([wisp-esp32](https://github.com/privkeyio/wisp-esp32)).
- **Phones:** the panel serves a small chat page over plain `http`; the page and its relay share the panel's address, so the browser can connect without an app. The phone makes a temporary key for the visit: no account, no lasting identity.

## Open questions

1. **Range:** does a radio link reach between real walls in a town of stone? (Test 2.)
2. **Night:** is a network that sleeps the point, or a flaw? The concept says it is the point. A battery would break principle 3.
3. **Open posting in public:** spam, abuse, illegal content, and the operator's responsibility under Italian law. Rate limits, expiry, and perhaps a quiet mode.
4. **Captive-portal browsers:** limited storage and scripts on some phones; does the chat page work in the Wi-Fi pop-up, or must visitors open a full browser?
5. **Capacity:** about 10 phones per panel at once.
6. **How many panels:** SUNDIAL's rule is nine; GO TO BED may need a different number, set by radio range.

## Tests, in order

1. **Bench:** a relay and a minimal web chat on one ESP32-S3, used from two phones with no internet.
1b. **Carrying:** two boards on the bench, one phone: write at board A, walk to board B, check the messages arrive. Test the Wi-Fi pop-up and a full browser, on iPhone and Android.
2. **Two walls:** two boards on two real walls in Bosa; ESP-NOW long range, then LoRa; measure what gets through, and at what panel power.
3. **Power scaling:** radio power and duty cycle following the sun reading.
4. Only then: a spec and a carrier variant.

## Status

On hold while SUNDIAL v1 goes to manufacture. Prior art to study when it resumes: Meshtastic (LoRa mesh, app over Bluetooth), Bitchat (phone-to-phone Bluetooth mesh with Nostr bridging).
