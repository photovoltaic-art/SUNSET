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

**The public incentive: who can be the first to deliver a block to a panel.** The panel gives the first deliverer a signed receipt: a **stamp**. Stamps are never cashed in. They have **uses** inside the work: first, bidding at the auction node (see Specialized nodes).

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

**Why both:** the phone's copy is the visitor's stamp; the chain's copy is the public record. Anyone checking a stamp needs only the panels' public keys and the chain: signature valid, recorded in the chain, not yet spent.

**What can go wrong**

- **Lost phone storage:** some phones clear a site's storage after days without a visit; saving receipts as images to the phone's photos avoids this.
- **Cheating:** blocks are sealed and signed by panels, so they cannot be invented; replaying a block earns nothing after the first delivery; and the panel's own clock, not the phone's, stamps the time.
- **Racing to be first:** that is the point. Blocks sealed at sunset can be delivered from dawn, so the first receipts of the day go to whoever reaches the next panel first in the morning.

**The passport**

- **Each panel has its own mark:** a 5 × 5 pixel square, different for every panel, like a stamp. The same mark is on the panel's wall plate, in the tone's ring of nine, and on its receipts.
- **The visitor's page is a passport:** nine empty boxes, one per panel. A successful first delivery fills that panel's box with its mark. Nine filled boxes on the same day is a **whole day**, and earns a page of its own.
- **Each receipt can be saved as an image:** the panel's mark, the date, the block, and the receipt itself encoded in the image (a small code beside the stamp, or in the image file's text fields), so **the picture is the proof**. Saved to the phone's photos, receipts outlive browser storage, and a spending node can read them straight from the image. (Some phones' Wi-Fi pop-up windows cannot save files; saving may need a full browser, as with SUNDIAL's downloads.)
- **Rules for the marks:** nine shapes that are easy to tell apart at a glance and at stamp size; possibly mirror-symmetric, like simple identicons; printable in one colour.

**Security: receipts are bearer stamps**

A stamp works like a token: **whoever presents it first, spends it.** There is no courier key and no phrase. The security rests on three things:

1. **Unforgeable:** every receipt carries the panel's signature, and must match an entry in that panel's sealed block in the chain.
2. **Unspent:** the spending node keeps a list of spent stamps, so each is used once.
3. **Scarce:** one receipt per block per panel means the town can never earn more than **72 stamps a day**.

**The one technical catch: the chain must not give receipts away.** If the sealed block recorded each receipt in full, anyone reading the chain could rebuild and spend it. So each receipt contains a **random secret**, and the block records only the secret's **fingerprint (hash)**. A spending node checks that the secret in a presented stamp matches the fingerprint in the chain. The chain proves the receipt exists; only the image holds the secret.

**What visitors are told:** your stamps are yours to use, so don't share them. Saved to the phone's photos, they last.
**A sharing version:** the passport can also save a picture of the stamps *without* the secret code, safe to post and show off.

**What can go wrong, and why it is accepted:** a stamp photographed or posted with its code can be spent by someone else; a lost image is a lost stamp. That is the same deal as dropping a token. It also matches the work: no key, no account, no lasting identity. The receipt simply records that *someone* walked it there first.

**No cash, only uses (decided).** Stamps are never redeemed for money or sats. They are **spent** at specialized nodes, the first being the auction node, where they buy objects. Spending happens in presence, at a wall, offline: no payment destination, no wallet, no record of who.

## Whisper and shout

Two kinds of message, and the visitor chooses.

| | **Whisper** | **Shout** |
| --- | --- | --- |
| Who sees it | Whoever is at this wall today, live, within seconds | The whole town, carried on foot |
| Where it lives | The panel's memory only. Never sealed, never carried | Sealed into the day's block |
| How long | Until bedtime (or a power cut) | 7 days on panels, 3 on phones |
| Limit | 30 per phone per wall per day | **3 per phone per wall per day** |
| Default | Yes: nobody spends a shout by accident | Chosen with the switch, or by promoting a whisper |

- **Promote to shout:** any whisper, your own or someone else's, can be sent to the town with one tap. It costs the promoter one of their three shouts. Whispers are anonymous, so there is no author to ask; promoting means *this deserves to travel*. A whisper can be promoted once.
- **Shouts are per wall:** spend your three here and the page says *your shouts here are spent — whisper, or try another wall tomorrow*. Walking to another panel gives three more.
- Two people at one wall can talk live by whisper; what they want the town to hear, they shout.

## Courier by default: the bag

Every visitor is a courier, automatically, and can see it.

- **Pickup is automatic.** Each time the page opens at a wall, the phone collects what that wall holds that it lacks (the last 3 days of every panel).
- **Delivery is automatic.** Whatever the phone carries that the wall lacks is handed over. A first delivery earns a stamp.
- **Visible:** the bag shows on the page (*news from 5 panels*), and every pickup and delivery is announced in the ticker.
- **Reversible:** an **empty my bag** button. An empty bag reads only what this wall holds, and delivers nothing.
- **Why default:** the network is only as fast as the number of phones carrying, and carrying costs nothing anyone would notice (under 100 KB, holding no data about anyone). Opt-in would starve outlying panels.

## The visitor's page

1. **Arrive.** A small plate on the wall: the panel's 5 × 5 mark and *join GO TO BED*.
2. **Join the Wi-Fi.** The page opens by itself, or in the browser (the carry test decides which, and what the plate says).
3. **The page wakes,** and the background work begins and is announced.

| Part | What it shows |
| --- | --- |
| **Tone** | The pulse, phones here now, the ring of nine |
| **Ticker** | One line at a time, automatic: what is moving, here and now (below) |
| **Status row** | **Shouts ● ● ○** (left today at this wall) · **Bag:** news from 5 panels · **Passport:** stamps today |
| **Here** | Today's whispers at this wall, live. Each has a small **↑ shout** button |
| **Write** | 140 characters, **Whisper / Shout** switch (whisper by default) |
| **Town** | Shouts carried in from other walls, by panel and day, with replies under the messages they answer |

**The ticker.** Collection and delivery happen in the background, without a button; the ticker makes them visible, so the network feels alive and nothing is hidden:

> *picked up today's news from panel 3*
> *delivered panel 7's news here — first! stamp*
> *delivered 2 blocks — already here*
> *someone just brought panel 8's news*
> *a whisper was shouted to the town*
> *you're carrying news from 5 panels*

The ticker also shows what **other phones** do at this wall, live and anonymously, so a visitor sees that others are carrying too. Ticker lines live in the panel's memory and are gone at bedtime.

4. **Dusk.** The pulse slows, the ticker says *going to bed*, the live room closes and the page says goodnight. Whispers are gone; shouts are sealed for tomorrow's walkers.

## The arrival

New data brings new interaction. When a walker delivers news, **everyone at the wall sees it at once**:

- the ticker: *someone just brought panel 8's news — 12 new shouts*;
- panel 8's point on the ring brightens;
- the new shouts appear in the town feed on every connected phone.

The people at the wall become an audience for the delivery. Watching the ticker is part of taking part: like waiting for the post, the evening paper, or a boat into port. Even someone who never writes sees the network working and sees others carrying, which is the strongest reason to walk: *I could be the one who brings the news.*

- **The wall has a rhythm:** quiet at first light, a burst when the first walker arrives with yesterday's sealed blocks, trickles through the day. The ticker shows the sun's schedule and people's movements together.
- **The day's tally at bedtime,** on the goodnight screen: *today at this wall: 14 arrivals, 3 firsts, 2 whispers shouted to the town.* Counts only, never who.
- **The one caveat, accepted:** with only two people at a wall, an arrival line points at the person who just walked up. That is no more than seeing someone arrive with a letter, and nothing is recorded. Delaying lines at random would hide it but kill the liveness, so the work does not.
- **Optional, for the box design:** a small light on the wall, powered by the panel, that pulses once when news arrives, so passers-by without a phone see the network working too.

## Specialized nodes

Most panels are ordinary walls: tone, ticker, whispers, shouts, stamps. **One panel can be given a job.** It runs the same network (it seals, carries and stamps like any other) and adds one thing of its own. The first is the auction node; others will follow.

### The auction node

An **auction in presence**: the objects are real, on show near the wall; **the dashboard is the bidding platform**; the currency is **stamps**.

- **The gallery:** photos of the lots, held on this panel only (about 1 MB of flash: 10–20 images), never carried. Each lot has a short ID, e.g. *A*, *B*. The town hears about the auction through shouts.
- **Bidding in stamps.** Stamps are earned only by being first to deliver, at most 72 a day across the town. You cannot buy the art with money, only with walking: **proof of walk as the currency.**
- **No cash, just spend.** Stamps are never redeemed for money anywhere in the work; at this node they are spent. Spent stamps go on the node's spent list; the passport shows them as spent.
- **How a bid works:**
  1. The bidder's page offers stamps for a lot. The node checks each one (a valid panel signature; recorded in the chain if the node still holds that block; not spent, not already backing a bid).
  2. The stamps are **held** by the node against the bid. The ticker calls it: *new high bid on lot A: 9 stamps*.
  3. **Outbid:** the held stamps are released and can back a new bid.
  4. **Hammer at bedtime.** An auction runs for **one day** and ends automatically when the panel goes to bed: the sun is the hammer. The winning stamps are **spent**. The winner's page shows a collection code: the secret behind a fingerprint recorded in the node's block, like a receipt. Show it, take the object.
- **One spending node per town** keeps it simple: the spent list lives on that panel, so a stamp cannot be spent twice. The node also writes the day's spent fingerprints into its sealed block, so other walls' passports learn which stamps are gone.
- **Everyone at the wall watches the bidding** in the ticker and the live room. Whispers are the saleroom chatter.

### Event mode (admin, to add)

The auction node needs an admin, unlike an ordinary wall: to load the gallery and set the lots for the day. Bidding opens when the panel wakes and closes at bedtime, with no one pressing a button. **Event mode** borrows SUNDIAL's admin login (challenge-response, no password sent). Outside an event the node goes back to being an ordinary wall, and the gallery is cleared.

### To settle before building

- **Stamps cross an open Wi-Fi.** The page and the panel talk over plain `http` on an open network, so someone nearby with the right tools could capture a stamp's secret as it is issued or spent. When stamps buy objects, that matters. Options: a Wi-Fi password printed on the wall plate with the newer encryption (WPA3), which keeps each phone's traffic private even when everyone knows the password, if the ESP32 supports it in this mode; or spend stamps with a one-time code shown on screen instead of sending the secret. To check on the bench.
- **The format additions:** held and spent stamps, lots, the spent list in the node's block. Format v0 stays as is until the node is built.

### Other specialized nodes (ideas)

- **A vote node:** an in-presence ballot where each vote costs a stamp. Choices made by those who walked.
- **A swap node:** objects left and taken, the exchange agreed in whispers, stamps as the deposit.
- **A gallery node:** a wall that shows images, SUNDIAL-style, alongside the chat.
- **A radio node:** a link to another place (below).

### The radio node: a link to another place

One panel in each of two places, joined by radio. Everything else still moves on foot.

- **The radio:** LoRa on the EU 868 MHz licence-free band. A small board on the carrier's spare pins, powered from AUX and scaled to the sun. Low power, long range: a few km with clear line of sight (for example Bosa to Bosa Marina, about 2.5 km), less through hills and buildings.
- **Enough for GTB:** a day's blocks are a few KB each. At LoRa's slowest settings a block takes tens of seconds; within the band's airtime rules (1 % duty cycle, about 36 seconds an hour) the two radio nodes can swap a town's sealed blocks in an hour or two of a sunny day. Whispers and images never go by radio.
- **Both must be awake:** the link only works while both panels have sun, which is most of a clear day. A cloudy day at one end is a day without news from the other place. Bedtime still rules.
- **Radio earns no stamps.** Stamps are for walking; news that arrives by radio is announced in the ticker (*news from Bosa Marina arrived by radio*) but no one is first. Inside each town, people still carry it from the radio node to the other walls, and they earn stamps for that.
- **Format note:** two places means two sets of panels 1–9. Block IDs would need the place, e.g. `marina-3/2027-07-14`.
- **The story:** the radio node is the port. News from the other place arrives there, and the town's walkers take it inland.

## Messages: no identity, no moderation, replies

- **No identity.** A message has no author, no key and no account. If someone wants a name, they type it into the message, and anyone can type any name. The panel's seal proves only *where and when* a message was written.
- **Don't trust anything that is written.** That is the stance of the work, not a gap in it.
- **No moderation.** Nothing is removed or hidden. Words fade instead: gone from phones after 3 days and from every panel after 7.
- **Replies.** Every message has an address: its panel, day and place in that day's block, e.g. `7/2027-07-13#4`. Tap a message, tap reply; the reply carries that address and the page shows the original above it, or "not here yet" if no one has carried it this far. Threads cross the town one night per hop.
- **Whispers** are anonymous too; your own are marked *you* on your phone only.
- **Reading happens at a panel.** A plain-`http` page cannot install itself for offline use, so the words travel in the phone but are read standing at a wall, in daylight.

## Forgetting

**The network forgets; people may not.** Forgetting is a feature of the work, not a gap in it.

- **Panels** drop every block after 7 days. The chain fades with it: each block holds only the fingerprint of the one before.
- **Phones:** the page drops blocks older than 3 days each time it opens at a panel.
- **Receipts and passports** hold no words: a panel, a block ID, a time, a secret.
- **Checking stamps needs no words.** The panel's seal covers a fingerprint of the day's messages, not the messages themselves ([format](gtb/FORMAT.md)). So the record of which deliveries earned stamps stays provable from block headers alone, and the words can go. The test bed checks this: every block and every receipt verified with the words removed.
- **Panel flash:** the firmware overwrites a block's file before deleting it, so a panel taken off the wall gives up no more than its last 7 days.

**What the work cannot promise, and says so:**
- **A phone forgets only when the page runs.** A phone that visits once and never returns keeps its last blocks until the browser clears them (Safari after about 7 days without a visit; other browsers may keep them longer).
- **People can copy.** A screenshot, a saved page, a walker with a script. Nothing in the work keeps anything; it cannot stop a person keeping something.

## No user data

The work collects nothing about anyone. No accounts, names, keys, phone IDs, logs or analytics.

| What the panel sees | What it keeps | For how long |
| --- | --- | --- |
| A phone's Wi-Fi address (needed to join, and to count 3 messages per phone) | In memory only, as a counter | Until bedtime or power loss. Never written to flash, never in a block |
| How many phones are connected now | A number, for the tone | Live only |
| The message text | In the day's block | 7 days, then gone |
| When a message was written | The hour, not the minute | 7 days |
| A first delivery | Block ID, the hour, the fingerprint of the receipt's secret | 7 days on panels |
| Anything else (web requests, phone types, browsers) | Nothing | — |

- **Times are kept to the hour** in messages, deliveries and receipts, so a person seen at a wall cannot be tied to a message by its timestamp.
- **The passport is the visitor's own record**, kept on their phone. It shows where that phone went; it leaves the phone only when a stamp is spent, and then only that stamp.
- **Spending** happens in presence at a wall: the node sees the stamps offered, nothing else, and keeps only the spent list.
- **What people write is theirs.** Someone may type a name or a number into a message; with no moderation, panels carry it for up to 7 days. That is content people chose to publish, not data the work collects.

**For the Comune (draft line, to check with whoever handles permissions):** *the installation collects no personal data and publishes only what visitors write themselves, for at most seven days.*

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
| 9 | Identity | None (level 0), or a name typed into the message (level 1). Don't trust anything that is written |
| 10 | Moderation | None. Messages fade after 3 days on phones, 7 on panels |
| 11 | Replies | A message can reply to another by its address, `panel/day#n` ([format](gtb/FORMAT.md)) |
| 12 | Forgetting | A feature. All words gone from the network after 7 days at most; stamps stay checkable from block headers, no words |
| 13 | User data | None collected. Wi-Fi addresses counted in memory only; times about people kept to the hour |
| 14 | Whisper and shout | Whispers: live at one wall, memory only, gone at bedtime, 30 per phone. Shouts: sealed and carried, 3 per phone per wall per day |
| 15 | Promote | Any whisper, anyone's, can be shouted once; it costs the promoter a shout |
| 16 | Courier | By default: pickup and delivery automatic, announced in a ticker, bag visible, **empty my bag** to opt out |
| 17 | Arrival | Every delivery is announced live to everyone at the wall; bedtime tally of counts only; an optional arrival light |
| 18 | Specialized nodes | A panel can be given a job on top of the network. First: the auction node |
| 19 | Auction | In presence; the dashboard is the bidding platform; local gallery of the lots; event mode with admin (to add) |
| 20 | Stamps as currency | Bids are paid in stamps: proof of walk as currency. No cash redemption anywhere; stamps only have uses |
| 21 | Auction close | One day per auction; ends automatically at the panel's bedtime |

## Technical direction

- **Board:** the SUNDIAL carrier, ELEGOO ESP32, new firmware.
- **The network:** people carry it (proof of walk). Only sealed blocks travel, so a day's words leave a panel after it has slept once: the network's minimum delay is one night.
- **Radio (later, optional):** a panel-to-panel link where walls can hear each other, most likely LoRa (SX1262 class) on the carrier's spare pins, its power scaled to the sun reading and drawn from AUX. Not needed for the first version.
- **Format:** plain JSON blocks and bearer receipts, Ed25519 signatures ([FORMAT.md](gtb/FORMAT.md)). Nostr remains a possible later bridge, not a dependency.
- **Phones:** the panel serves the chat page over plain `http`; no app, no account.

## What the test bed shows (simulated, invented town)

Three scenarios, one week each, nine panels, a quarter of messages replying to earlier ones, six attacks checked, and a check with the words removed ([details](gtb/testbed/README.md)):

| | Busy | Quiet | Sparse |
| --- | --- | --- | --- |
| Visitors per hour at the central panel | 6 | 1 | 0.3 |
| Visitors served in the week | 2,442 | 405 | 123 |
| Receipts (first deliveries) | 408 | 265 | 163 |
| Typical delay, bedtime to another panel | 14 h | 21 h | 38 h |
| Whole days | 3 | 1 | 0 |
| Largest block | 4.8 KB | 3.4 KB | 2.5 KB |
| Most a walking phone carried | 91 KB | 32 KB | 20 KB |

- **Sizes are comfortably inside the limits** in every scenario: blocks under 5 KB against a 16 KB limit; a phone carries under 100 KB.
- **The busy town saturates:** every panel up to date within a day. The 60-message block limit is reached at the centre.
- **The quiet town shows the imbalance the work is about:** central panels stay partly fresh; outlying panels fall to zero for days, and a single whole round lifts the whole town at once.
- **Headers alone are enough:** with every word removed, all blocks and receipts still check.
- **All six attacks fail:** altered message, forged secret, spending twice, a fake panel, a stolen panel key whose receipts are not in the chain, and a reply pointing at a message not yet written.

## Open questions

1. **Phones in practice:** does browser storage carry blocks between panels, in the Wi-Fi pop-up and in a full browser, on iPhone and Android? (Carry test.)
2. **Night:** the concept says sleeping is the point. A battery would break principle 3.
3. **Capacity:** about 10 phones per panel at once.
4. **Event-mode admin** for specialized nodes: to add, borrowing SUNDIAL's login.
5. **Open Wi-Fi and stamp secrets:** see the auction node.
6. **The radio node:** which two places, line of sight between them, a LoRa board for the carrier's spare pins.

## Tests, in order

1. **Test bed** (done, simulated): format, sizes, receipts, attacks.
2. **Carry test:** one ESP32 playing panel A then panel B; phones on iPhone and Android, Wi-Fi pop-up and full browser.
3. **Two boards on the bench:** the real firmware, a few phones, a day of light from a bench supply.
4. **Two walls in Bosa:** two panels, real walkers, one week.
5. Only then: the full nine, as an event week.

## Status

On hold while SUNDIAL v1 goes to manufacture; the test bed is done and the carry test is ready to run ([steps](gtb/carry_test/TEST.md): four browser paths, iPhone and Android). Prior art to study when it resumes: Meshtastic (LoRa mesh, app over Bluetooth), Bitchat (phone-to-phone Bluetooth mesh with Nostr bridging).
