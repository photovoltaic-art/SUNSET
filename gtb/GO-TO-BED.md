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
- **Blocks are sealed and signed by the panel,** so a carrier can lose a block but cannot forge or alter one. Messages themselves carry no signature and no author.
- **The clock travels too.** Phones carry the time between panels, as well as messages, so the town keeps time together. Each panel keeps its own clock module and treats carried time as a hint, never an order: one phone can't reset the town.
- **A slow version of Bitcoin's nodes,** in spirit: copies spread by gossip until every panel holds every block. Unlike Bitcoin there is nothing to agree on and nothing to spend; every message is simply added. Panels only ever merge what they are given.
- **Proof of walk.** A message crosses town only if someone carries it, or a radio link reaches. The network's speed is the speed of people, and of the sun.
- **Permissionless.** Anyone can carry; no one needs to be chosen, registered or known. Every walk counts, even between just two panels: each carry brings two panels closer.
- **The imbalance shows.** Each panel shows when it was last updated, and its ring shows how fresh the others are. Busy panels in the centre stay current; outlying panels that few people visit fall behind, and everyone can see it. That gap is an open invitation to walk to them.
- **The whole round.** When one phone visits all nine panels on the same day, the town is whole: every panel holds everything. The day is marked as a *whole day* in the record (a count, never who). Anyone can make it happen, by choosing to walk the full round.

**How a phone carries it (to test).** All the panels answer at the same local web address, so a web page stored by one panel's visit is readable at the next: the phone's browser storage is the courier's bag, with no app. The catch: some phones' Wi-Fi pop-up windows keep no storage, so carrying may need a full browser. Test this first.

**What it may change:** if people can carry the network, **the radio between panels becomes optional**: an accelerator where links reach, not a requirement. A people-powered GO TO BED could run on hardware close to the SUNDIAL carrier, with the radio added later or only where walls can hear each other.

## Receipts: first to deliver

**The public incentive: who can be the first to deliver a block to a panel.** The panel gives the first deliverer a signed receipt. The reward is symbolic (one sat). This work issues **receipts only**; turning receipts into sats is a separate redeem layer, outside the work.

**How it works**

1. **No account and no key.** Anyone can carry; the phone just holds the blocks it has picked up.
2. **The delivery.** At a panel, the phone offers the sealed blocks it carries. The panel checks each block's seal (the signature of the panel that sealed it) and keeps the ones it lacks.
3. **First only.** For each block that is new to this panel, the panel issues one receipt, to the first phone that brings it. A second delivery of the same block to the same panel earns nothing. So each receipt can exist only once: nine panels each seal one block a day, each can be delivered to eight others, so **at most 72 receipts a day** can ever be earned.
4. **The receipt.** A few lines, signed with the panel's key:

   ```
   panel 3 · received block 7/2027-07-14 (sealed by panel 7)
   first delivery · secret 7f3c…a91d
   at 2027-07-15 09:42 (panel 3's clock)
   ```

5. **Where it lives.** The receipt is kept in **two places**:
   - **on the visitor's phone**, in the browser's storage for the panels' shared local address, so the receipt book is visible at every panel, like a pilgrim's passport;
   - **in the panel's next sealed block,** as a fingerprint only (see Security below). The day's deliveries are written into that panel's block at bedtime, so the record travels round the town with the messages and becomes part of the chain: a public, tamper-evident record that each block was delivered, and when.

**Why both:** the phone's copy is the visitor's stamp; the chain's copy is the public record. A redeem layer only needs the chain and the panels' public keys to check a receipt: signature valid, recorded in the chain, not yet spent.

**What can go wrong**

- **Lost phone storage:** some phones clear a site's storage after days without a visit; saving receipts as images to the phone's photos avoids this.
- **Cheating:** blocks are sealed and signed by panels, so they cannot be invented; replaying a block earns nothing after the first delivery; and the panel's own clock, not the phone's, stamps the time.
- **Racing to be first:** that is the point. Blocks sealed at sunset can be delivered from dawn, so the first receipts of the day go to whoever reaches the next panel first in the morning.

**The passport**

- **Each panel has its own mark:** a 5 × 5 pixel square, different for every panel, like a stamp. The same mark is on the panel's wall plate, in the tone's ring of nine, and on its receipts.
- **The visitor's page is a passport:** nine empty boxes, one per panel. A successful first delivery fills that panel's box with its mark. Nine filled boxes on the same day is a **whole day**, and earns a page of its own.
- **Each receipt can be saved as an image:** the panel's mark, the date, the block, and the receipt itself encoded in the image (a small code beside the stamp, or in the image file's text fields), so **the picture is the proof**. Saved to the phone's photos, receipts outlive browser storage, and the redeem layer can read them straight from the image. (Some phones' Wi-Fi pop-up windows cannot save files; saving may need a full browser, as with SUNDIAL's downloads.)
- **Rules for the marks:** nine shapes that are easy to tell apart at a glance and at stamp size; possibly mirror-symmetric, like simple identicons; printable in one colour.

**Security: receipts are bearer stamps**

A receipt works like cash: **whoever presents it first, redeems it.** There is no courier key and no phrase. The security rests on three things:

1. **Unforgeable:** every receipt carries the panel's signature, and must match an entry in that panel's sealed block in the chain.
2. **Unspent:** the redeem layer keeps a public list of redeemed receipts, so each pays once.
3. **Scarce and symbolic:** one receipt per block per panel means the town can never pay out more than **72 sats a day**, so there is little worth stealing.

**The one technical catch: the chain must not give receipts away.** If the sealed block recorded each receipt in full, anyone reading the chain could rebuild and redeem it. So each receipt contains a **random secret**, and the block records only the secret's **fingerprint (hash)**. The redeem layer checks that the secret in a presented receipt matches the fingerprint in the chain. The chain proves the receipt exists; only the image holds the secret.

**What visitors are told:** your stamps are like cash, so don't share them. Saved to the phone's photos, they last.
**A sharing version:** the passport can also save a picture of the stamps *without* the secret code, safe to post and show off.

**What can go wrong, and why it is accepted:** a stamp photographed or posted with its code can be redeemed by someone else; a lost image is a lost sat. At one sat a stamp, that is the same deal as dropping a coin. It also matches the work: no key, no account, no lasting identity. The receipt simply records that *someone* walked it there first.

**Privacy at redemption:** the redeem layer sees a receipt and a payment destination, nothing else.

**The redeem layer (separate, not part of this work):** reads receipts from the chain or a visitor's saved file, checks them against the panels' public keys, and pays the symbolic sat by Lightning or ecash wherever there is internet. Its rules on giving away bitcoin in Italy are its own question.

## Building on SUNDIAL

- **Same principles** ([MANIFESTO](../MANIFESTO.md)): the panel powers only itself; offline by nature; the work keeps no one; slow.
- **Same base hardware where possible:** the SUNDIAL carrier's power path, sun sensor and clock, with lessons from its v1 bench test.
- **The SUNDIAL carrier already has the hooks:** an AUX output that takes spare panel power through its own converter, a switched 5 V output, and spare SPI/UART/I²C pins. The firmware sheds AUX loads the moment the panel voltage sags, so the board always has priority.

## Decided (21 Oct 2026)

| # | Question | Decision |
| --- | --- | --- |
| 1 | How to test | A test bed first: a simulated town that writes real, signed blocks and receipts ([gtb/testbed](gtb/testbed/README.md)), then a one-board phone carry test ([gtb/carry_test](gtb/carry_test/carry_test.ino), steps in [TEST.md](gtb/carry_test/TEST.md)) |
| 2 | Open posting | Fine: it is an art installation. Messages are short (140 characters) and expire |
| 3 | Flooding | Limits per phone and per block, sized together with 4 |
| 4 | Sizes | Sized for simple, failsafe operation: [format v0](gtb/FORMAT.md) |
| 5 | Time | Stamped by the panel's clock only |
| 6 | Hardware | **The SUNDIAL carrier and its ESP32 (ELEGOO 30-pin), unchanged.** Format v0 needs no PSRAM, no Nostr relay and no radio: blocks are a few KB, signatures are light work. An ESP32-S3 is only needed if a later version adds a panel-to-panel radio or a large relay |
| 7 | Relation to SUNDIAL | New firmware; same carrier board and hardware; its own set of PV panels |
| 8 | Panels | Nine. PVA works are nine panels |

## Technical direction

- **Board:** the SUNDIAL carrier, ELEGOO ESP32, new firmware.
- **The network:** people carry it (proof of walk). Only sealed blocks travel, so a day's words leave a panel after it has slept once: the network's minimum delay is one night.
- **Radio (later, optional):** a panel-to-panel link where walls can hear each other, most likely LoRa (SX1262 class) on the carrier's spare pins, its power scaled to the sun reading and drawn from AUX. Not needed for the first version.
- **Format:** plain JSON blocks and bearer receipts, Ed25519 signatures ([FORMAT.md](gtb/FORMAT.md)). Nostr remains a possible later bridge, not a dependency.
- **Phones:** the panel serves the chat page over plain `http`; no app, no account.

## What the test bed shows (simulated, invented town)

Three scenarios, one week each, nine panels, five attacks checked ([details](gtb/testbed/README.md)):

| | Busy | Quiet | Sparse |
| --- | --- | --- | --- |
| Visitors per hour at the central panel | 6 | 1 | 0.3 |
| Visitors served in the week | 2,442 | 405 | 123 |
| Receipts (first deliveries) | 408 | 265 | 163 |
| Typical delay, bedtime to another panel | 14 h | 21 h | 38 h |
| Whole days | 3 | 1 | 0 |
| Largest block | 4.3 KB | 3.2 KB | 2.4 KB |
| Most a walking phone carried | 83 KB | 29 KB | 18 KB |

- **Sizes are comfortably inside the limits** in every scenario: blocks under 5 KB against a 16 KB limit; a phone carries under 100 KB.
- **The busy town saturates:** every panel up to date within a day. The 60-message block limit is reached at the centre.
- **The quiet town shows the imbalance the work is about:** central panels stay partly fresh; outlying panels fall to zero for days, and a single whole round lifts the whole town at once.
- **All five attacks fail:** altered message, forged secret, redeeming twice, a fake panel, and a stolen panel key whose receipts are not in the chain.

## Open questions

1. **Phones in practice:** does browser storage carry blocks between panels, in the Wi-Fi pop-up and in a full browser, on iPhone and Android? (Carry test.)
2. **Night:** the concept says sleeping is the point. A battery would break principle 3.
3. **Capacity:** about 10 phones per panel at once.
4. **The redeem layer:** separate; who runs it, funding, Italian rules.

## Tests, in order

1. **Test bed** (done, simulated): format, sizes, receipts, attacks.
2. **Carry test:** one ESP32 playing panel A then panel B; phones on iPhone and Android, Wi-Fi pop-up and full browser.
3. **Two boards on the bench:** the real firmware, a few phones, a day of light from a bench supply.
4. **Two walls in Bosa:** two panels, real walkers, one week.
5. Only then: the full nine, as an event week.

## Status

On hold while SUNDIAL v1 goes to manufacture; the test bed is done and the carry test is ready to run ([steps](gtb/carry_test/TEST.md): four browser paths, iPhone and Android). Prior art to study when it resumes: Meshtastic (LoRa mesh, app over Bluetooth), Bitchat (phone-to-phone Bluetooth mesh with Nostr bridging).
