# SUNSET: independent security review of the design

Reviewer: independent, adversarial. Date: 27 Oct 2026. Scope: design documents only (nothing is built).

Documents read: `sunset/README.md`, `SUNSET.md`, `stamp-format.md`, `tokenomics.md`, `interactive-token.md`, `interactive-flipdot.md`, `interactive-auction.md`, `interactive-arm-game.md`, `wall-node.md`, `battery-tier.md`, `interactive-audio.md`, `garden-node.md`, `gtb/FORMAT.md`, `gtb/GO-TO-BED.md` (security parts), `gtb/testbed/gtb.py` (canonicalisation only), `sundial/SUNDIAL.md` 4.1–4.4, `sundial/hardware/CARRIER.md`, `pva/GROWTH.md`.

Note: a file `sunset/SECURITY.md` (the authors' own threat model) appeared in the repository at 08:46, while this review was under way. I did not read it. A few of its lines showed up in a repository-wide grep, and I did not use them. This review was written from the design documents alone, so it is independent of that file. Where we agree, that is corroboration and not copying.

Severity scale used here: **critical** means the core promise of the work fails (theft of visitors' value, unlimited minting, or confiscation of honest holders' coins) through an attack that is cheap and repeatable. **High** means a serious, practical failure of one node or one mechanism, or serious legal or safety exposure. **Medium** means a real weakness that is bounded, or that needs effort or insider position. **Low** means nuisance, edge cases or hygiene.

---

## Summary table

| # | Finding | Severity |
| --- | --- | --- |
| C1 | Shared origin `http://192.168.4.1` plus plain HTTP: any fake AP or any node steals every passport key and auction claim, and can persist through cache poisoning | **Critical** |
| C2 | NTAG213 tokens are trivially cloned. A clone library plus the public live coin state lets an attacker redeem other people's savings, and the honest coin is then confiscated | **Critical** |
| C3 | A stolen or extracted node key, or a dishonest year-2 owner, mints stamps that every node accepts: no bounds on `day` or `exp`, no in-network source checks, no revocation | **Critical** |
| H1 | Proof of walk is not proof of walk: relay bots or a directional antenna capture all 72 walk stamps every morning | High |
| H2 | Arm game is botable (replayable moves), and the stock RoArm firmware exposes its own Wi-Fi AP and ESP-NOW control | High |
| H3 | The gateway's ESP-NOW ledger is unspecified: no authentication, no replay protection, no fail-closed rule, and a race window | High |
| H4 | The 100-entry `issued`/`spent` block caps let one person freeze the auction, and contradict the gateway's stated capacity | High |
| H5 | Wi-Fi association flood or deauth lets an attacker snipe the auction and force forfeits | High |
| H6 | ESP32 key protection is weaker than assumed: removable dev board, reachable USB, flash-encryption mode, fault injection, first-boot RNG, runtime exposure | High |
| H7 | Clock rollback brings pruned spent stamps back to life; the ±5 min "round key" nudge can be repeated; a dead coin cell is not handled | High |
| H8 | Admin and maintenance access for SUNSET is unspecified; SUNDIAL's model leaks its round master through the shared origin | High |
| H9 | Legal exposure: unmoderated paid shouts with no takedown path, and an anonymous unattended auction that works as a dead drop or fence | High |
| H10 | The double-spend bound is wrong: up to ~5 extra uses per stamp, and the gettoneria converts them into year-long hard money | High |
| M1 | Shill auctions renew any amount of stamps (fresh `exp` on payout), bypassing expiry and the 1,000-coin savings ceiling | Medium |
| M2 | The spend signature does not bind the action (bid amount, claim hash, refund key, shout text) | Medium |
| M3 | Underspecified canonical JSON, duplicate keys, Ed25519 strictness and malleability | Medium |
| M4 | Equivocation (two signed blocks for one `node/day`) is not detected or handled | Medium |
| M5 | Resource exhaustion on the ESP32: 48 KB JSON from strangers, Ed25519 cost, storage eviction | Medium |
| M6 | Deanonymisation through the live coin check, stamp lookup, auction collection and season-end blocks | Medium |
| M7 | Physical safety and theft: unfused LiFePO₄ battery path, heat, lithium items in lockers, resale theft | Medium |
| M8 | Firmware and web supply chain; the locked NFC URLs depend on one domain forever | Medium |
| M9 | Year-2 governance: Sybil ownership, owner-run firmware, and "frozen rules" that cannot be enforced | Medium |
| M10 | Bluetooth Classic attack surface on the audio node | Medium |
| M11 | The reference sun sensor can be tampered with so every day counts as a clear-sky day | Medium |
| L1–L8 | Fake service notices and Unicode spoofing; whisper floods; locker magnets; boot-state glitches; obscene flip-dot art; hopper count drift; tank tampering; refunds to absent bidders | Low |

---

## Critical

### C1. One shared web origin over plain HTTP: every node, and every fake access point, owns every visitor's wallet

**Severity:** critical.
**Concerns:** stamp-format.md 3.1 and 8; wall-node.md 5.1; interactive-auction.md 3.5; SUNSET.md 8 ("Nothing worth copying crosses the open Wi-Fi"); gtb/GO-TO-BED.md (passport "for the panels' shared local address"); SUNDIAL.md 4.3 (which already names the risk for the admin key).

The design guards against **passive** sniffing (holder keys, commit-and-reveal). It does nothing against an **active** attacker, and on an open, plain-HTTP network that is the attacker who matters. All nine nodes serve from the same origin, `http://192.168.4.1`. Browser storage (localStorage and IndexedDB) is scoped to scheme, host and port, so every page any node serves, and every page any impostor serves at that address, can read the whole passport: every per-stamp private key and every auction claim secret.

**Attack A: evil twin, about €5 of hardware.**
1. Flash an ESP32 or ESP8266 to broadcast the same SSID as Wall 3 (the SSID is printed on the wall plate), with a captive portal at `192.168.4.1`. Place it near the real wall or near the auction, at higher transmit power.
2. A visitor's phone joins it (same SSID, stronger signal; open networks have no way to authenticate the AP).
3. The impostor's page runs at the same origin and reads `localStorage`: all stamp private keys and all claim secrets. It shows a convincing "network is busy" page.
4. The attacker spends the stamps at real nodes before the victim does. That beats the victim, because the first spend wins. The attacker also reveals the victim's winning-bid claim at the auction locker and takes the lot. The *seller's* claim works too: take the goods back after midday **and** redeem the stamps.

**Attack B: persistent cache poisoning.** Service workers need a secure context, but the ordinary HTTP cache does not.
1. The impostor serves `/`, `/app.js` and the crypto library with `Cache-Control: max-age=31536000, immutable`.
2. The next time the phone is at a **genuine** node, the browser uses the cached, malicious script. That script runs against the genuine node, so it can silently (a) submit the **attacker's** holder key in place of the victim's every time the victim earns a walk or skill stamp, redeems a token, receives a refund or receives a payout; and (b) spend the victim's stamps on the attacker's lot.
3. The victim sees normal-looking pages, and every future earning goes to the attacker. No exfiltration channel is needed.

**Attack C: a dishonest node owner (year 2, GROWTH.md 3).** An owner opens their own box and flashes their own firmware (tokenomics.md 3 itself says this needs only a tamper bit and USB). Their node then serves script at the shared origin and does Attack A or B to every visitor who passes. No radio trickery is needed, and the firmware fingerprint published by PVA proves nothing about what that one box actually runs.

**Why the existing text is wrong:** stamp-format.md 3.1 says "There is nothing to steal on the air." There is nothing to steal *passively*. Actively, everything can be stolen, and the shared origin turns one compromised or impersonated node into a compromise of all nine.

**Fixes (layered; none is complete on open HTTP):**
1. **Give each node its own origin:** a different subnet and IP per node (for example `10.0.N.1`). This contains a malicious *node*, since a dishonest owner then cannot read other nodes' origins. It does **not** stop an impersonator of that same node, so in addition:
2. **Split the passport per node:** keep each stamp's key only at the origin of the node that issued it, or better, store keys encrypted under a passphrase the visitor types, so that a script reading storage gets ciphertext. Spending still needs the passphrase typed at the node, and a malicious script can capture it then, so this only narrows the window.
3. **Encrypt the link:** consider WPA2 or WPA3-Personal with the passphrase printed on the plate. WPA3-SAE gives per-session keys even when the password is public, which defeats passive sniffing and makes deauth-assisted attacks harder. It does **not** stop an evil twin that knows the printed password. OWE (Enhanced Open) does the same without a password if ESP-IDF's SoftAP supports it.
4. **Defeat cache poisoning:** serve every page and script at a path that includes a per-day or per-boot random component that the genuine captive-portal redirect chooses, and inline the crypto in the HTML with `Cache-Control: no-store`. Tell visitors to clear site data if a page "looks wrong". This is partial at best.
5. **Bind actions (M2)** so that a captured signature cannot be retargeted.
6. **Lower the stakes:** state honestly, in the rules, that an active attacker within Wi-Fi range can steal a passport. Keep balances small: a per-passport cap and short expiry, which already exists. Treat auction lots as "the risk is the seller's". Remove the sentence claiming nothing can be stolen.

---

### C2. Token cloning is not a "minor recognised bug": it is theft of the town's savings, with the honest holder punished

**Severity:** critical.
**Concerns:** interactive-token.md 2.1, 2.4, 2.8, 3.2, 3.6, 3.7; stamp-format.md 4 and 5.1; interactive-flipdot.md 2.1; SUNSET.md 2.3–2.4 and 7.2.

The tag holds a static link: the UID plus the gettoneria's signature over that UID. That signature proves the tag was *once* written by PVA. It does nothing against copying, because a clone copies the UID and the signature verbatim. UID-changeable "magic" NTAG21x tags cost about €1–2, and the coin acceptor (plastic, optical or size-based, per interactive-token.md 6) is fooled by a 3D-printed disc.

**Attack: a clone library plus a live-state oracle.**
1. **Harvest IDs.** Mint tokens, read each one with a phone (any phone opens the NDEF link), then redeem them. Each mint draws random coins from the hopper, so over a few weeks the attacker reads a large share of the 1,000 coins. Other sources: tapping coins through the thin perspex of the flip-dot token column (NFC works through plastic at a few millimetres), borrowing coins "to check them", and the café that accepts tokens.
2. **Map printed number to UID** from the coins read.
3. **Watch the live state.** Every wall's coin check by printed number (wall-node.md 1.3), the gettoneria's status pad and page (3.6), and the weekly coin table (2.8) tell anyone which coins are *issued* right now, which means in someone's pocket. The page can be polled by script for all 1,000 numbers.
4. **Cash out.** Drop the clone of an *issued* coin into the gettoneria's redeem slot, get a fresh digital stamp, and repeat. Or spend clones at the flip-dot wall.
5. **Victim outcome.** The honest holder later presents the genuine coin. It is "a clone already used", so it is refused **and kept** in the reject box (interactive-token.md 3.2.6, flipdot 2). At the round, PVA "removes duplicate IDs, which can only be clones" from the reject and kept boxes. But the attacker's clone, spent first at the flip-dot wall, went into the column and back into the hopper **in return mode**. So the clone stays in circulation and the genuine coin is the one destroyed.
6. **Reuse.** Coins are reused all season (return mode puts them back in the hopper). One clone is valid **every time** that ID is in the *issued* state. A clone made in May still pays in September.

Scale: the attacker can take up to the whole of the town's savings (the 250–750 coins out in town), and every victim is publicly told their coin was a "clone". Tokens are explicitly the money that may trade for coffee (SUNSET.md 2.4), so this is real loss to third parties.

**Fixes:**
1. **Use a tag that cannot be cloned:** NTAG 424 DNA (or NTAG 223/224 DNA, or DESFire EV3) with an AES key per tag. The gettoneria and the flip-dot wall authenticate the tag (mutual AES challenge, or SUN/SDM with a rolling CMAC and a read counter). Budget about €0.50–1 more per token. The public Verify page can still check a static signature for "genuine design", with a disclaimer.
2. If cheap tags stay: **stop publishing live per-coin state.** Answer only "genuine / not genuine" away from the gateway, publish only aggregates weekly, and drop status-by-printed-number. It is a liveness oracle for thieves.
3. **Change ID on each circulation:** reissue under a fresh random serial each time a coin leaves the hopper. This needs writable tags plus an authenticated write, which brings you back to fix 1.
4. **Do not confiscate on duplicate.** Return the second copy to the cup with "this coin was used by someone else at HH:00", and log both. Confiscating punishes the victim and hides the evidence from them.
5. **Bench check:** check the *hopper* too, not only the reject and kept boxes, and check NXP's originality signature (`READ_SIG`). This catches lazy clones only, since some magic tags emulate `READ_SIG`.

---

### C3. A stolen or extracted key, or a dishonest owner, mints stamps every node accepts

**Severity:** critical (from year 2 onward; high in year 1, where the threat is theft plus key extraction).
**Concerns:** stamp-format.md 2, 3.2, 3.3, 3.4, 5.1; tokenomics.md 2.2, 3, 5, 6; GROWTH.md 3.

The spend check (stamp-format.md 3.4) is: (0) today ≤ `exp`; (1) issuer signature; (2) holder signature; (3) not on the spent list; (4) "if the node holds the issuer's block for that day", the stamp is in `issued`. **Check 4 is skipped when the block is missing.** Nothing checks:
- that `day` ≤ today;
- that `exp` − `day` ≤ the rule's validity;
- that `why` ∈ {walk, skill, …} is consistent with the issuing node's role;
- that issuance is within its source bound (at most 8 walk stamps, sunlight ÷ R, the clear-sky ceiling, refunds and payouts ≤ earlier spends). These are described as things "any node and the explorer **can** run" (3.2). They are not in the spend path, and they could not be anyway without the issuer's block.

**Attack (key holder):**
1. Sign stamps with `day` = some date next week (or next year) and `exp` = 2099-12-31, `why: walk`. No node will ever hold "the issuer's block for that day" before that day, so check 4 is always skipped. The stamps never expire, and their IDs stay in the spent list until 2099, which also grows storage (M5).
2. Spend them everywhere: shouts, auction bids, and **the gettoneria, which converts them into tokens valid to 31 December**. Tokens are not linked back to the stamps that bought them, so the laundering sticks.
3. A dishonest owner does not even need key extraction: they hold the key by design (GROWTH.md 3.2) and can flash any firmware into their own box.

**There is no revocation.** "A replaced or tampered node gets a new key... the old key's blocks stay valid up to the replacement date" (stamp-format.md 2). But (a) the public keys are **compiled into every node's firmware** (same section), and the rules allow firmware changes only once a year with all nine boxes opened (tokenomics.md 3). So the stolen key stays trusted in the field for the rest of the season, and the replacement node's new key is *unknown* to the other eight, so its genuine stamps fail check 1. (b) "Valid up to the replacement date" is meaningless when the signer chooses `day`: backdated blocks and stamps pass.

The test bed's "stolen panel key whose receipts are not in the chain" attack (gtb/GO-TO-BED.md) passes only because the test bed assumes the real chain has already arrived. That is exactly the case the attacker avoids.

**Fixes:**
1. **Hard checks at every spend:** `day` ≤ today ≤ `exp`; `exp` − `day` ≤ `rules.validity[why]` (and the earliest-`exp` rule for refunds); a role whitelist (only walls and other nodes issue `walk`, only the arm issues `skill`, only the gettoneria issues `redeem`, only the auction issues `refund` and `payout`).
2. **Require the issuer's block after a grace period:** a stamp whose `day` is older than, say, 1 day is accepted only if its issuing block is held and lists it. On a densely walked network this closes the window to about one day.
3. **Check bounds in the network, not only in the explorer:** on receiving a block, each node verifies the source bounds (walk ≤ 8 with matching deliveries; skill ≤ min(sunlight ÷ R, ceiling); refunds and payouts ≤ spends into that node). A node whose block breaks a bound is **quarantined**: none of its stamps are accepted from then on, and the event is shown on the dial tone.
4. **A revocation path that does not need re-flashing:** a key-revocation notice co-signed by k of n keyholders (the same threshold as the coin list), carried by couriers like a block. Enrolment of a new key works the same way. Compile the *keyholder* public keys, not only the node keys, into firmware.
5. **Mint gate at the gettoneria:** accept only stamps whose issuing block it holds, and that are at least N hours old. This stops laundering into hard money.
6. Put the rules fingerprint in every block **now** (tokenomics.md 3 says "proposed, for the next version", yet the TL;DR presents the fork-visibility property as current).

---

## High

### H1. Proof of walk can be captured by bots, relays or a directional antenna

**Concerns:** tokenomics.md 2.1; wall-node.md 1.5, 3.3; stamp-format.md 3.2 and 7; GO-TO-BED.md ("racing to be first: that is the point").

Only the **first** delivery pays, the cap is global (72) rather than per person, and blocks become deliverable at dawn. So the issuance goes to whoever is fastest at dawn, and that is never a pedestrian.

**Attacks:**
1. **Relay farm.** Put a €10 ESP32 near each node (or one per pair). Each connects to its node as a client at wake-up, pulls the sealed blocks, and pushes blocks received from the other relays (over LoRa, a cheap 4G stick or a long Wi-Fi link) with the attacker's own holder keys. All 72 walk stamps go to the bot within seconds of dawn, every day.
2. **Directional antenna.** From one rooftop, a laptop with a yagi reaches several walls (an ESP32 AP is easily heard at hundreds of metres line-of-sight with a high-gain receive antenna). No walking at all.
3. **Cyclist.** One person on a bicycle does two passes of all nine nodes at sunrise and takes most of the 72.
4. **Deauth-and-steal.** On open Wi-Fi without 802.11w, an attacker sniffs a courier's block upload, deauthenticates the courier mid-upload, and submits the captured blocks with the attacker's own holder key.

The walls show "where couriers are missing", so the network also tells the bot where to go.

**Fixes:** accept that "walk" cannot be proved, and design for fairness instead of speed:
- Pay **by lottery** among all distinct deliverers within a window (for example the first hour after a node wakes), not to the first.
- Require a **physical act** at the wall: a push button or a capacitive touch pad wired to J9, pressed within a few seconds of the delivery. This raises a bot's cost to a servo plus hardware at every wall.
- Require a **minimum transit time** between a signed pickup ticket at node A (bound to the courier's key) and delivery at B.
- **Rate-limit per holder key lineage** (pickup tickets chain), so one passport cannot collect from every node in one sweep.
- At minimum, rewrite the claim "the people who carry the chain are paid by it" to admit that the race is open to machines.

### H2. The arm game can be botted, and the stock arm firmware is a second attack surface

**Concerns:** interactive-arm-game.md 2.1, 2.3, 3.1–3.3, 5 ("Arm firmware" open question).

1. **Replay bot.** The pegs return by gravity to a hopper at nearly the same place, and the arm has 12-bit encoders with closed-loop position. So a scripted sequence of the same JSON-level moves ("go to hopper, grip, go to hole 1, release") succeeds deterministically. A script on a laptop sits in the queue (or holds most of the 10 slots), plays whenever the page says *"next stamp in about 12 minutes"*, and drains the whole sun's purse (about 35 stamps a day) every day. The page helpfully announces when to play.
2. **The stock RoArm-M2-S firmware** runs its own Wi-Fi access point and web UI and accepts ESP-NOW and HTTP control. Unless it is replaced, anyone in range can drive the arm directly, bypassing the carrier's soft limits and load limits (which live in the *carrier* firmware). They can push the arm into the perspex, burn out a servo, or steer a peg during someone else's turn.

**Fixes:** flash a trimmed arm firmware with Wi-Fi, Bluetooth and ESP-NOW **compiled out**, with soft limits enforced on the arm's own controller too. Randomise peg presentation (a rotating or shaking hopper) and add jitter so recorded sequences fail. Cap turns per connection and per hour. Consider a **physical** control (a joystick on the cabinet) instead of the phone, so playing needs a person standing at the case. The phone only receives the stamp.

### H3. The gateway's shared live ledger over ESP-NOW is not specified, and as written it can be forged, raced and jammed

**Concerns:** interactive-flipdot.md 2.1, 7; interactive-token.md 2.3, 2.8, 3.3, 5; SUNSET.md 2.3, 4 (and the auction "within ESP-NOW range", stamp-format.md 5.2).

The documents say the two nodes share every state change "within a second". They say nothing about authentication, encryption, replay protection, ordering or behaviour when the link is down.

**Attacks:**
1. **Forgery.** ESP-NOW frames carry a spoofable source MAC. An attacker broadcasts "coin X: spent" for every coin, and every honest token is then refused and **confiscated** (griefing; destroys savings). Or they send "coin X: issued" for coins sitting *in the hopper* or *in the column*, then spends clones of those (combine with C2).
2. **Race.** Two people drop the genuine coin and its clone at the gettoneria and the flip-dot wall within the same second. Both nodes check their local state before the update lands, and both accept.
3. **Jamming.** Jam the shared channel (which also takes down both APs, though a narrow-band or timed jammer can target ESP-NOW frames). If the firmware fails *open*, double spends are free; if it fails closed, it is a denial of service, which is acceptable.

**Fixes:** make **one node authoritative** (the gettoneria). The flip-dot wall sends "request spend X" and acts only on a signed "granted X, seq n" reply. Use timeouts: if there is no reply, return the coin to the cup and do not keep it. Sign every message with the node keys and include a monotonic counter stored in flash. Enable ESP-NOW's own encryption (LMK per peer) as a second layer only; do not rely on it for replay protection. Accept frames only from the paired peer. **Fail closed** whenever the link is down. Apply the same protocol to the auction if it joins the live list.

### H4. The block entry caps let one person lock up the auction, and they contradict the gateway's capacity

**Concerns:** stamp-format.md 7 (100 `issued`, 100 `spent` per block; 48 KB; "anything over a limit is refused"); 3.2 ("every stamp is worth one... a payout of 9 is nine stamps"); interactive-auction.md 3.4; SUNSET.md 3.1.

Each stamp is a separate entry. A bid of 50 stamps uses 50 `spent` entries; every outbid refund uses `issued` entries.

**Attack, auction freeze:**
1. In the morning, place a modest top bid from phone A.
2. Using phones B and C, bid against each other with a few stamps each, round after round. Each cycle adds spends and refunds; even simpler, two bids of 50 stamps each fill all 100 `spent` entries.
3. Once `spent` is at 100, the auction must refuse every further bid ("refused, never truncated"). Bidding is closed by noon, and A wins at whatever price A chose. As seller, the same trick freezes your own lot at your own bid (see also M1).

**Contradiction:** SUNSET.md 3.1 gives the gettoneria 300–500 mints or redeems a day. At one `spent` entry per stamp plus the fee, 100 entries is about 15–20 mints a day. The flip-dot wall's ~1,000 flips a day each produce a `tokens` entry (about 80–90 bytes), so roughly 90 KB, over the 48 KB block limit. The `tokens` array has no stated limit at all.

**Fixes:** aggregate entries (one `spent` entry per *spend request* carrying up to 50 IDs and one holder signature over all of them; one `issued` entry per batch). Give each role its own size budget (the gettoneria and flip-dot wall need far more). Consider *denominations* or value fields so a 50-stamp bid is one object. Specify behaviour at the cap: the auction should reserve capacity for bids (for example, refunds always fit).

### H5. Wi-Fi association flooding and deauthentication let an attacker manipulate the auction

**Concerns:** interactive-auction.md 3.2, 3.6 ("up to 10 phones at once"); SUNDIAL.md 4.3 ("occupying all 10 connections... accepted" for an artwork with no value).

SUNDIAL could accept this. SUNSET cannot, because the auction has deadlines with money-like consequences.

1. **Sniping.** At sunset minus 20 minutes, bid. Then fill all 10 association slots with spoofed MACs (an ESP8266 script) and broadcast deauth frames (open networks have no Protected Management Frames). Nobody else can bid before the hammer.
2. **Forced forfeit (seller fraud).** List a lot, and let a real buyer win. From sunrise to midday the next day, flood the auction's AP. The winner cannot collect, forfeits at midday, and the seller (the attacker) keeps **both** the stamps and the goods (3.2).
3. The same works against the arm queue, the gettoneria's one-at-a-time flow, and the walls.

**Fixes:** enable 802.11w or PMF with WPA3/OWE if the stack allows (open legacy Wi-Fi cannot do it). Make deadlines robust: extend the hammer by N minutes after any bid in the last N minutes (anti-snipe), and suspend the collection deadline while the node detects association flooding or a full client table. Give the auction a physical fallback (a button on the cabinet that reserves a slot). Log and show "network under load" on the page.

### H6. Key protection on the ESP32 is weaker than the documents assume

**Concerns:** stamp-format.md 2 ("kept in its encrypted flash"); interactive-auction.md 3.5 ("flash encryption on, so a stolen board does not give up the signing key"); CARRIER.md 4 (ELEGOO dev board in **removable sockets**, "USB-C must stay reachable for programming with the board in the box"); SUNDIAL.md 4.3–4.4 (USB re-flash every spring; derived admin keys "compiled in" `panel_config.h`); GROWTH.md 2.1 (key generated at handover).

1. **Theft takes seconds.** The ESP32 module unplugs from its sockets. The tamper screws only slow down someone without a €3 bit set.
2. **Flash encryption without Secure Boot, or in Development mode,** does not protect the key. Development mode is what a team that re-flashes over USB every spring will tend to use. With UART download mode enabled, an attacker flashes a small firmware (the ROM encrypts it on the way in) that prints the decrypted key. In Release mode with Secure Boot v2, ROM download mode disabled or secure, and JTAG disabled, the remaining attacks are physical.
3. **Fault injection.** Voltage and EM glitching attacks on the original ESP32 are published: secure boot bypass (CVE-2019-15894) and eFuse key readout of the flash-encryption and secure-boot keys (CVE-2019-17391). ECO V3 silicon mitigates some of these. Cheap boards still ship older revisions, and the ESP32 is not designed to resist a lab attacker. A thief with a few hundred euros of equipment and time should be assumed to get the key.
4. **First-boot RNG.** `esp_random()` is a true RNG only while the Wi-Fi or Bluetooth radio is on, or after `bootloader_random_enable()`. A key generated "at installation" early in boot with the radio off can be **predictable**.
5. **Runtime exposure.** Flash encryption is transparent to running code. Any memory-safety bug in the HTTP server, the JSON parser (parsing up to 48 KB of attacker-supplied JSON), the Wi-Fi stack or the Bluetooth stack (M10) gives up the key without anyone touching the box.
6. **Admin keys** in `panel_config.h` (SUNDIAL) are plaintext in firmware unless flash encryption is on.

**Fixes:** check the chip revision on delivered boards (require V3). Use Secure Boot v2 plus Flash Encryption in **Release** mode, with ROM download in secure mode or disabled and JTAG disabled. Do yearly updates by **signed OTA over a cable-local channel**, or with a pre-encrypted image process, not plain `esptool`. Generate the key only after the RF is up (or with `bootloader_random_enable()`), and mix in extra entropy. Better still, hold the node key in a **secure element** on J13: an NXP SE050 supports Ed25519, while ATECC608 would need a move to P-256. Pot or glue the module in place, add a tamper switch that destroys the key, and make **revocation** work (C3), because extraction must be survivable.

### H7. Clock manipulation brings spent stamps back to life and moves the hammer

**Concerns:** stamp-format.md 3.4 (check 0), 3.5, 5.3 (spent IDs dropped "once its stamp's `exp` has passed"); SUNDIAL.md 4.3 ("clock corrections of up to ±5 minutes" with the round key) and 4.1 (dead coin cell); battery-tier.md 1.2.

1. **Rollback resurrection.** A node prunes spent IDs whose `exp` is past *by its own clock*. If its clock is then moved backwards (dead CR2032 resetting the DS3231 to 2000-01-01; an I2C fault; an admin nudge), every pruned stamp is unexpired again and no longer on the spent list. Everyone who kept old stamp keys in their browser (or copied their storage, H10) spends them again.
2. **Repeated nudges.** The ±5-minute round-key correction is per call, with no cumulative limit. Twelve calls move the clock an hour: end the auction early, extend it, or shift "today" past someone's `exp`. A leaked round key (H8) makes this a remote attack.
3. **The dead coin cell** is handled in SUNDIAL by "records undated data". SUNSET does not say what an interactive node does without valid time: it must refuse all business.

**Fixes:** keep spent IDs for a fixed number of **sealed days**, not "until `exp` by the wall clock". Store a monotonic day counter in flash, and refuse to run business if the RTC ever reads earlier than the last sealed block or later than last + 2 days. Limit cumulative clock correction to, say, ±10 minutes per week, and log it in the sealed block. Cross-check the time against incoming blocks from other nodes (a median of peers' `woke` times). Treat a coin-cell failure as a service notice and a full stop for spending.

### H8. Admin and maintenance access for SUNSET is unspecified, and borrowing SUNDIAL's leaks the master

**Concerns:** interactive-token.md 3.2 step 7 (return mode "opened from the admin page, by PVA or the gateway's host"), 2.8 (weekly coin-table download by the host); interactive-audio.md 2.2 and 3.2 (pairing and music "by the admin"); SUNSET.md 7.2; GO-TO-BED.md ("borrows SUNDIAL's login"); SUNDIAL.md 4.3.

Nothing in the SUNSET documents says how admin is authenticated, who holds which key in year 2, or what each admin action can do. SUNDIAL 4.3 is good for a single owner, but it fails when reused here:
- The round master is "remembered by the browser" at `192.168.4.1`. Under C1, any SUNSET node (including an owner-modified one) or any impostor reads it from the walker's storage. With nine owners, PVA's master would be readable by every owner's node.
- In year 2 the gateway's **host** holds return-mode access but is not the owner. Return mode with no check on coin *state* lets a host (or anyone who can open return mode) push arbitrary coins to *in the hopper*. The design is safe for value only because return mode issues no stamps. Make sure it stays that way, and that return mode refuses coins in the *issued* state, so a host cannot quietly wipe others' savings.
- Downloads cross open Wi-Fi in clear (accepted in SUNDIAL for 7 days). In SUNSET, raw downloads include the full blocks, which tokenomics.md 4.3 wants kept private until season end.

**Fixes:** write the admin section for SUNSET: per-node keys (no shared master across owners), challenge-response, action-scoped HMACs, cumulative limits, logging into the sealed block, and **never** store admin secrets in origin storage (type them each time, or use a separate admin origin such as a different port). Return mode must accept only coins in the *spent* state and log each ID.

### H9. Legal exposure: unmoderated paid shouts, and an anonymous unattended auction

**Concerns:** wall-node.md 2.2–2.3 ("No moderation... Nothing is checked or removed by hand"); GO-TO-BED.md; interactive-auction.md 3.6 ("Visibility is the moderation"), 5 (permission); interactive-flipdot.md 4; SUNSET.md 2.4.

1. **Shouts.** Anyone can pay to broadcast any text, including someone else's whisper, to every wall in town for 7 days: defamation of a named neighbour, doxxing (a phone number or address), harassment, hate speech, threats, illegal adverts. Promotion of *someone else's* whisper means the author never chose publication. There is **no takedown path**. Blocks are signed, though the words sit outside the signature (bound only by the `msgs` hash), so words *can* be dropped while the header is kept. Under the EU DSA and Italian law a host is expected to act on notice. PVA, owners and hosts are identifiable defendants; the authors are not.
2. **Whispers** are live anonymous chat at a wall, with no age gate. Grooming and arranging meetings are foreseeable.
3. **Auction.** An anonymous, unattended exchange of physical goods with bearer claims is a dead drop: opaque packages (drugs, a knife, stolen goods), with the claim secret forwarded remotely. "Visibility is the moderation" fails for any sealed box or envelope. Fencing and receiving stolen goods (the Italian offence of *ricettazione*) and unlicensed sales are plausible problems. The "no food, liquids or batteries" rule cannot be enforced.
4. **Tokens as currency.** SUNSET.md 2.4 anticipates cafés pricing in tokens. Whether a circulating, transferable unit that trades for goods raises payment-services, complementary-currency or tax questions in Italy needs a lawyer before launch. "No cash value, ever" is a statement of intent, not a legal shield, once a street market exists.
5. **Flip-dot art.** An unmoderated, persistent 28 × 28 public image at the town's entrance will eventually show something obscene or hateful.

**Fixes:** a **takedown** mechanism (an owner-signed or k-of-n "withdraw message" record carried like a block; the walls hide the words and keep the header). A printed notice of what is forbidden, plus a contact address for reports. Shouts promoted only by their own author (a whisper carries a one-time promotion key held by the writer). No opaque packaging in lots (lots must be visible *contents*), with a maximum size and a takedown or "quarantine locker" state. Legal review of the auction and token trade before launch; a canvas reset policy and an admin "clear region" for the flip-dot wall.

### H10. Double spends are not bounded at "one extra use", and they launder into tokens

**Concerns:** stamp-format.md 5.1–5.2 ("gains at most one extra use per stamp"), 9 (passport backup); tokenomics.md 6.

With N copies of the browser storage (desktop browsers export storage easily; one device can run several profiles), a stamp can be spent once at **every spending node that has not yet heard**: four walls (shouts), the auction and the gettoneria. That is up to about 5 extra uses, not 1. Spent at the gettoneria first, the copies become **tokens valid until 31 December**, which can neither be traced nor revoked. "Proved" is true, but it identifies no one by design, so the proof has no consequence.

**Fixes:** the gettoneria (the only route into hard money) and the auction (the largest spends) should share the live spent list over the authenticated link (H3), and both should apply C3 fix 5 (mint only stamps whose issuer block is held and which are at least N hours old). Revoke **coins minted with a stamp later proved double-spent**: mark their IDs "tainted" in the ledger. Correct the text to the real bound.

---

## Medium

### M1. Shill auctions renew any amount of stamps and bypass the savings ceiling
**Concerns:** stamp-format.md 3.5 (payout gets a **fresh** `exp`; only refunds keep the earliest); interactive-auction.md 3.4; tokenomics.md 1 ("the one way to keep value is to pay the minting fee").
**Attack:** list a pebble for 1 stamp. From a second phone, bid all your stamps that are about to expire. Win, then redeem the payout as fresh 7-day stamps. That is 1 stamp of fee to renew any amount, not capped by the 1,000-coin ceiling. Do it daily from the wings. It also gives control of the one daily auction slot.
**Fix:** a payout's `exp` should be the earliest `exp` of the winning bid's stamps (or that plus a small extension). Add a seller fee proportional to the price, or burn a share of the proceeds.

### M2. The spend signature does not bind the action
**Concerns:** stamp-format.md 3.4 (the signed string is `spend|id|node|day|challenge`).
**Attack:** a man-in-the-middle (C1) passes the genuine node's challenge to the victim, collects the victim's signatures, and uses them for *the attacker's* action at the genuine node: a bid with the attacker's claim hash, a refund to the attacker's holder key, or the attacker's shout text.
**Fix:** sign `spend|ids|node|challenge|H(action)`, where the action includes the lot ID, the amount, the claim-commit hash, the refund or change holder keys, and the shout text hash. The node checks that H(action) matches the request.

### M3. Canonical JSON and signature verification are underspecified
**Concerns:** stamp-format.md 1 ("keys sorted, no spaces, UTF-8"); gtb/FORMAT.md; gtb/testbed/gtb.py (`json.dumps(sort_keys=True, separators, ensure_ascii=False)`, and it verifies by re-serialising the *parsed* object).
**Issues:**
- Python sorts keys by code point; JavaScript and C implementations differ on non-ASCII keys, number formatting (`1e3`, `1.0`), escaping (`é` versus `é`, `\/`) and Unicode normalisation.
- **Duplicate keys:** Python keeps the last value; ArduinoJson and JS parsers differ. A malicious signer can craft a block whose *re-serialised* form verifies in one implementation while the content seen by another differs, for example two `issued` arrays. Then the explorer and the nodes disagree about what was issued.
- **Ed25519 strictness:** TweetNaCl-class libraries do not all reject non-canonical `S` (S ≥ L) or small-order points. A malleated signature produces a different block **fingerprint** (the fingerprint includes `sig`), so the same block exists under two fingerprints. That breaks `prev` links and any dedup keyed on fingerprint.

**Fix:** adopt RFC 8785 (JCS) exactly. Reject duplicate keys, non-integers and floats. Sign and verify the **received bytes** (or a strict re-encoding that must byte-match). Use a library that verifies strictly (RFC 8032, reject S ≥ L and small-order A and R): Monocypher, libsodium or ed25519-dalek-equivalent logic. Identify blocks by `node/day/seq`, and treat fingerprints over `sig` with care. Add cross-implementation test vectors (Python, JS and ESP32) to the test bed.

### M4. Equivocation is not handled
**Concerns:** stamp-format.md 1 and 6; gtb/FORMAT.md (chain by `prev`).
A key holder (C3), or an honest wall that browns out mid-seal at dusk and seals again at dawn, produces two different signed blocks for the same `node/day`. Nodes keep whichever arrives first, and check 4 then gives different answers in different parts of town.
**Fix:** two valid blocks for the same `node/day` with different content are a **proof of misbehaviour**. Carry it in blocks, quarantine the key (C3), and show it on the dial tone. Make sealing idempotent: write the sealed block to flash before any further action, and never re-seal a day.

### M5. Resource exhaustion on the ESP32
**Concerns:** stamp-format.md 7 (48 KB blocks; 1.2 MB of storage; 50 stamps per spend); wall-node.md 3.2; SUNSET.md 3.1 (10 clients).
- **Memory:** the original ESP32 has no PSRAM and about 100–150 KB of free heap with Wi-Fi up. Parsing a 48 KB JSON block with a DOM parser needs a multiple of that. Several clients uploading at once means out-of-memory and a reboot loop.
- **CPU:** a 50-stamp spend needs 100 Ed25519 verifications. Merging couriers' blocks needs a holder-signature check on every `spent` entry (needed to trust "proved" double spends). A slow library (TweetNaCl is very slow on microcontrollers) lets garbage requests tie up the node for minutes.
- **Storage eviction:** "oldest out first" within 1.2 MB means anyone producing maximal blocks (paid shouts filling 60 × 140 characters, or a malicious node's padded blocks) evicts other nodes' recent blocks. That disables check 4 and slows the propagation of `spent` records, which widens H10.
- Unbounded challenges or queue entries per connection.

**Fix:** streaming parsing with strict size limits per field. Verify the issuer signature first, and the holder signatures only after cheap checks. Use a fast Ed25519 implementation and measure it on the board. Set a per-connection request rate. Give each node a fixed storage quota, so a large block from node X evicts only X's own old blocks. Keep `spent` records preferentially.

### M6. Deanonymisation
**Concerns:** tokenomics.md 4.2–4.3; interactive-token.md 2.8, 3.6; SUNSET.md 6.2, 7.2.
- The **coin check by printed number** at every wall, plus the status pad, is a live oracle. Polling all 1,000 numbers hourly from any wall gives full coin movements. That makes the "weekly at most, more often would make coin movements easier to link" reasoning (SUNSET.md 7.2) moot. It also serves C2.
- **Stamp lookup by ID** (weekly) shows where and when a stamp was issued, to the hour, and whether it is spent. Anyone who sees a friend's passport (or a shared screenshot, if images show IDs) can trace it.
- **Auction collection is public:** the person opening the locker is seen. The winning bid's stamps are in the auction's `spent`, and each stamp's `issued` entry gives its earning node and hour. So the winner's walk (where and when they earned) can be reconstructed from the season-end blocks, and from the weekly lookup by ID before then.
- Stamps spent together (one request) are linked; walk stamps earned in sequence at different nodes trace a route.
- A **malicious node owner** can log MAC addresses, timestamps to the second, and message authorship, all of which the format promises not to keep.

**Fix:** drop live per-coin lookup (aggregates only). Drop stamp lookup by ID, or delay it to season end. Allow spending in fixed-size batches, and refresh change through a re-issue that breaks links. Publish the full blocks only after a longer delay, or never, publishing Merkle commitments and zero-detail totals instead. Say plainly in the rules that a node owner can log anything their radio sees.

### M7. Physical safety and theft
**Concerns:** battery-tier.md 2.1 (the fuse is shown only on the MPPT load output; the battery ↔ MPPT path is unfused in the diagram); interactive-auction.md 2.3, 3.6; interactive-audio.md 2.3; interactive-flipdot.md 3.1; garden-node.md 2.
- A 20–40 Ah LiFePO₄ pack can deliver very large fault currents. A vandal cutting the cables with bolt cutters, or water ingress, can start a fire. A **fuse or MRBF at the battery terminal** is mandatory and missing.
- Charging LiFePO₄ above about 45 °C or below 0 °C damages it. The Victron needs battery temperature (Smart Battery Sense, or a BMS with temperature cut-offs). Perspex boxes in the Sardinian sun get very hot.
- Lockers will hold lithium power banks and vapes despite the rule. A damaged cell in a hot perspex box next to the node's battery is a fire risk in the street.
- Theft for resale: Victron MPPT units, batteries, Bluetooth speakers, the RoArm (about €220), and the flip-dot panels (€880). Five sites carry more than €1,000 of resaleable kit each.
- Garden node: a 1 t water mass next to a 2.6 m post, children climbing the IBC cage, and the tank cap not locked (dye, soap or fuel poured in to kill the bed).

**Fix:** a battery-terminal fuse and a disconnect. Temperature-aware charging. Locked, tamper-switched cabinets with a service notice on opening. A ban on cells in lots, plus a thermal cut-off for the lockers' own circuits. Insurance covering theft and third-party fire. A locked tank cap.

### M8. Supply chain, and the locked NFC URLs
**Concerns:** tokenomics.md 3 and 5 (reproducible builds); interactive-token.md 2.1–2.2 (tags written once, then locked); SUNSET.md 6.2.
- Every coin permanently opens `https://<website>/verify#...`. If the domain lapses or the GitHub Pages account is compromised, 1,000 coins in strangers' pockets open the attacker's page. The fragment "is never sent anywhere" only for as long as the page's code is honest.
- Reproducible ESP32 Arduino builds are hard (toolchain, paths, timestamps). Even when achieved, they show what PVA *published*, not what a given box *runs*. There is no attestation.
- Third-party libraries (web server, JSON, NaCl port) and the build machine are single points of compromise. Their output is then flashed into nine boxes and served as JavaScript to every visitor.

**Fix:** register the domain long-term with registrar lock and 2FA. Use a hardware key on the GitHub org. Put a Subresource Integrity-pinned, versioned Verify bundle in the repository. Pin library versions and vendor them. Sign firmware with Secure Boot keys held offline. Publish the build environment as a container. Give owners a "show firmware hash" admin action backed by Secure Boot, so it reflects what is actually running.

### M9. Year-2 governance can be captured, and its rules cannot be enforced
**Concerns:** tokenomics.md 5; GROWTH.md 3.
- "Anyone can own a node", with no rule against one party owning several. Owning 5 of 9 gives control of the 5-of-9 coin list and of rule votes.
- "Each node's key... never seen by PVA" is not true: PVA writes the firmware that generates and holds it. In the other direction, each owner can flash anything into their own node, so "rules frozen in firmware" binds only honest owners.
- "Collusion: five keyholders together can do what one PVA can today" is understated. One dishonest owner can already mint without limit (C3) and steal passports (C1).

**Fix:** a one-owner-one-node rule (public register). Thresholds above a simple majority for anything touching supply. The in-network enforcement and quarantine of C3, so a single misbehaving owner is cut off automatically rather than by vote. Origin isolation (C1).

### M10. Bluetooth Classic attack surface on the audio node
**Concerns:** interactive-audio.md 2.1–2.2.
The original ESP32's Bluetooth Classic stack had serious published bugs, including the BrakTooth family (2021), with crashes and at least one code-execution case reported against ESP32. The node is connectable at sunset in a crowd, holds a signing key, and accepts "Just Works" pairing semantics. Re-pairing by an impostor with the speaker's address is accepted in the document as "a lot of effort for a free set". The real risk is code execution, not the stolen music.
**Fix:** use a current, patched ESP-IDF. Never be discoverable; page-scan off; outgoing connections only to the bonded address; no re-pairing without the admin key. Consider not holding a stamp-signing key on this node at all, since it neither issues nor spends.

### M11. Sun-sensor tampering turns every day into a clear-sky day
**Concerns:** tokenomics.md 2.2; interactive-arm-game.md 3.3.1.
A torch or lamp on the reference cell (if reachable from the street), or tampering by the owner, gives the ceiling every day: about 35 skill stamps even under cloud. The walls' cross-check runs only in the explorer, after the fact. Covering the cell is a cheap denial of service. Covering a *wall* panel lowers the cross-check baseline, which makes an honest arm look like a cheat.
**Fix:** put the reference cell out of reach. Have nodes enforce the ceiling and a *peer-relative* bound in the network (the arm's daily sunlight ≤ k × the median of the walls' readings that day, once those blocks arrive). Hold back the arm's stamps for the day as a provisional total until the cross-check passes.

---

## Low

- **L1. Fake official notices.** A paid shout styled "SUNSET: tokens must be exchanged at Bar X by Friday" invites coin theft through social engineering. Unicode bidi overrides and homoglyphs make it look official. *Fix:* render node notices (`node: 1`, signed by the node) in a visually distinct style that shouts cannot imitate, and strip bidi controls and zero-width characters (wall-node.md 2.3; stamp-format.md 6).
- **L2. Whisper and shout flooding.** v0's limits (30 whispers per phone per day, counted by MAC address) "stand" (stamp-format.md 1 and 7), but MAC randomisation and spoofing defeat them, and the 200-per-panel daily cap is exhausted in seconds. *Fix:* proof-of-work or a small stamp cost on whispers above a free quota, and a per-connection rate limit.
- **L3. Locker hardware.** Reed door switches can be fooled with a magnet. Some cheap solenoid latches can be pulled with a strong neodymium magnet or shimmed. Perspex doors can be pried or cut. *Fix:* magnetically shielded latches, hidden or hall-effect sensors with tamper detection, polycarbonate rather than acrylic, and an internal steel frame (interactive-auction.md 2.3, 3.3, 3.7).
- **L4. Boot-state glitches.** PCF8574 outputs power up *high* (flip-dot inhibit and flap, interactive-flipdot.md 3.2), and GPIO 17 floats until configured (gettoneria inhibit, interactive-token.md 4.2). If inhibit is active-low, the acceptor accepts coins during boot and an honest coin can be swallowed or sent to the kept box. *Fix:* define inhibit polarity so that "power-up default = inhibited", and add hardware pull resistors.
- **L5. Obscene flip-dot picture** at the entrance (see H9). *Fix:* a reset policy and admin region-clear.
- **L6. Hopper count drift.** A missed read pays one more (interactive-token.md 3.1), and a coin on a string at the redeem flap (read, stamp issued, pulled back) leaves the ledger believing the coin is in the hopper. Value is safe, because the ledger state makes the coin worthless, which is good. But the count drifts, and a later mint can take stamps and pay fewer coins. *Fix:* reconcile against ccTalk payout counts, and refund automatically if the hopper under-pays.
- **L7. Garden-node tank tampering** (an unlocked cap) and a soil-probe spoof that drains the tank (capped daily, which is good). *Fix:* a locked cap.
- **L8. Refunds to absent bidders.** "Outbid: the node at once issues fresh stamps... back to the bidder" (interactive-auction.md 3.4), but the outbid bidder is usually gone, and the refund keeps the *earliest* `exp`, so it can expire before they return. *Fix:* specify that the refund is issued to a holder key committed at bid time and collected later at any node (as a signed refund note), with `exp` extended to at least N days.

---

## What is genuinely robust

- **Holder keys instead of v0 secrets:** a passive sniffer gains nothing reusable from issue or spend traffic.
- **Challenge-bound spend signatures** (node and fresh challenge): no replay of a captured spend at another node or later.
- **Token value lives in the ledger, not the coin:** stealing the hopper, the reserve tube, the column or the reject box yields worthless coins, and "coin on a string" tricks gain nothing in value (L6 aside).
- **Commit-and-reveal claims** are sound against *passive* listeners.
- **No OTA path:** remote firmware replacement is impossible; the box must be opened.
- **Flash-before-act** for every state change, and a power-safe file system, make brown-outs safe.
- **Fail-secure locks; the redeem flap rests on reject; the coin acceptor returns real money.**
- **JP1 physical interlock plus the compile-time switch** against shorting a battery with the sun sensor.
- **Text-only rendering** (`textContent`) everywhere, so no stored XSS from messages.
- **Data minimisation in records:** times to the hour, no phone identifiers, words fade while headers stay verifiable.
- **"Refuse, never truncate"** limits, and expiry that bounds the spent list in normal operation.
- **The coin list frozen by fingerprint**, with the coin ID inside `redeem` stamps, so new coins cannot be added mid-season by honest firmware.
- **Explorer recomputation from signed raw headers**, plus delayed publication of full blocks: the right instincts, though enforcement must move into the network (C3).
- **Wired arm UART** rather than ESP-NOW, once the stock arm firmware is replaced (H2).

---

## Contradictions between documents

1. **Where the gettoneria's key lives.** stamp-format.md 2, tokenomics.md 5 and GROWTH.md 3.2 say each key is generated on its node, never leaves it, and is "never seen by PVA". interactive-token.md 2.2 and 4.1 have tags "written, **signed**, locked" by a **bench** batch writer and script. Either the private key is on PVA's laptop, or the node must sign the batch over a link that isn't described.
2. **Key replacement.** stamp-format.md 2 says a replaced node gets a new key, published with its date. The same section says public keys are compiled into every node's firmware, and tokenomics.md 3 allows firmware changes only once a year. A mid-season replacement leaves the new node untrusted and the old key trusted.
3. **Capacity versus block limits.** SUNSET.md 3.1 gives 300–500 mints or redeems and up to about 1,000 flips a day. stamp-format.md 7 sets 100 `issued` and 100 `spent` entries per block and 48 KB per block, with one entry per stamp. The `tokens` array has no limit, and a flip-dot day would exceed 48 KB.
4. **Year-end coins.** interactive-token.md 2.6 says expired tokens go back into the hopper "for the new year". 2.2 and SUNSET.md 7.2 say a new batch of 1,000 coins is made each year, with its own closed list, and every node refuses IDs not on that list.
5. **Business after sunset.** battery-tier.md 1.2 and SUNSET.md 3 say all business, including returning, happens only between sunrise and sunset, and Wi-Fi closes at sunset. SUNSET.md 3 ("Evening") and interactive-token.md 3.7 have return mode run after sunset, and it is opened from the admin page over Wi-Fi.
6. **Rules fingerprint.** tokenomics.md TL;DR and 3 present "a hard fork, visible in the chain" as a property. 3.3 and 7 say the field is only *proposed* for the next format version; v1 blocks have no rules field.
7. **Double-spend bound.** stamp-format.md 5.2 says "at most one extra use per stamp". The same document has several spending nodes (1, table), so up to about 5 extra uses are possible.
8. **Stolen key.** stamp-format.md 3.3 and 5.1 say forged stamps "fail check 4 wherever the real chain has arrived", while 3.4 skips check 4 whenever the block is missing. Future-dated stamps never have a block.
9. **Clear-sky ceiling.** tokenomics.md 2.2 says "stop any sensor claiming more" and "the most anyone could mint is what the sky allowed". It is checked only by the explorer, after the fact.
10. **Coin-table privacy.** SUNSET.md 7.2 says weekly at most, because more often would make movements linkable. wall-node.md 1.3 and interactive-token.md 3.6 provide a live per-coin check at every node, at any time.
11. **Close of day.** SUNSET.md 3 says all business stops on every node at sunset. interactive-auction.md 4 says walls close at **dusk from panel voltage**. When a wall seals its block if it browns out early is unspecified.
12. **GPIO 17.** battery-tier.md 2.1 says VE.Direct is receive-only, freeing GPIO 17. interactive-auction.md 2.2 and interactive-audio.md 2.4 still list "16 RX, 17 TX".
13. **"Nothing worth copying crosses the open Wi-Fi"** (SUNSET.md 8) against the shared-origin passport and an active attacker (C1). This is also inconsistent with SUNDIAL.md 4.3, which already warns about fake networks at the shared origin.
14. **v0 limits "stand"** (stamp-format.md 1), including the MAC-based per-phone counts, while v1 drops the per-phone shout limit as unenforceable. The whisper limit has the same weakness.
15. **Auction refunds** are issued "at once" (interactive-auction.md 3.4) to a bidder who is normally absent, with no holder key or delivery path specified.

---

## Priority order for fixes

1. C1: per-node origins, an honest threat statement, action binding (M2), and anti-cache-poisoning measures.
2. C3 and M4: hard `day`/`exp`/role checks, in-network source bounds, quarantine, and k-of-n revocation. Do this before any year-2 handover.
3. C2: unclonable tags (NTAG 424 DNA class), and remove the live per-coin oracle.
4. H3: a specified, signed, fail-closed gateway protocol with one authoritative node.
5. H4 and H5: aggregate entries; anti-snipe and anti-flood rules at the auction.
6. H6, H7 and H8: Secure Boot v2 and Release-mode flash encryption, RNG at key generation, a monotonic day counter, and a written SUNSET admin design.
7. H1 and H2: fairness mechanisms for walk issuance; arm firmware lock-down and anti-replay.
8. H9 and M7: takedown, auction content rules, legal review, battery fusing and temperature limits.
