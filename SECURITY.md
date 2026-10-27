# SUNSET security — threat model and audit

> Status: draft 2, 27 Oct 2026. A design-stage audit of SUNSET as specified (no firmware exists yet), in two passes: the authors' own analysis (draft 1), then an **independent review** by a reviewer who had not seen this file or the design discussion ([security/independent-review-2026-10.md](security/independent-review-2026-10.md), summarised in section 8). Draft 2 merges the two. Each threat has a status: **robust** (the design already handles it), **gap** (a fix is proposed), **decision** (a choice for Carl, section 5), or **accepted** (a known, bounded risk, stated in public). References such as C1 or H4 are the reviewer's findings.
>
> **The seal is not changed.** One sealed block per node per day at sunset stays exactly as designed. Every fix here acts on what nodes *check* when they receive stamps and blocks, on the pages, the links and the hardware; none changes when or how a day is sealed.

---

## TL;DR

- **The cryptography is sound; the checks around it are not finished.** Ed25519 everywhere, holder keys, commit and reveal, and the frozen coin list all hold up. But draft 1 was wrong to say issuance stays bounded if a key is stolen: the bounds are checked only by the explorer, after the fact. A stolen key, or a dishonest year-2 owner, can sign **future-dated, never-expiring stamps** that every node accepts, and launder them into coins (C3). **Fix: hard checks at every spend, the bounds enforced in the network, quarantine, and a revocation path** (4.4).
- **The phone is the weakest point, and worse than draft 1 said.** A fake network at the shared address reads the whole passport, and can **poison the browser cache** so that a genuine node later serves the attacker's script (C1). In year 2, any owner's own firmware can do the same. **Fix: encrypted passport, small holdings, actions bound into signatures, no long-lived cached script, and honest wording** (4.1).
- **Cloned coins are not a small bug.** With the live per-coin lookup, a thief can see which coins are in people's pockets, spend clones first, and the honest holder's genuine coin is the one confiscated (C2). **Decision for Carl:** unclonable tags (NTAG 424 DNA), or keep cheap tags and **remove the live per-coin lookup and the confiscation** (5).
- **Fair issuance is open to machines.** Walk stamps go to whoever is fastest at dawn, which is a relay bot, not a walker (H1); the arm game can be replayed by script, and the arm's stock firmware runs its own Wi-Fi (H2). **Decisions for Carl** (5).
- **To specify before firmware:** the gateway's ESP-NOW protocol (H3), maintenance access (H8), key handling on the ESP32 (H6), a clock that cannot roll back (H7), block size limits that match the gateway's traffic (H4), and auction deadlines robust to Wi-Fi flooding (H5).
- **Physical and legal:** a fuse at the battery terminal and temperature-aware charging are missing (M7); a takedown for shouts and content rules for auction lots, checked by a lawyer, before year 2 (H9).
- **Accepted, in public:** the double spend (now honestly bounded at up to about five uses, and guarded at the gettoneria), denial of service on an open network, and the goods in a locker being the seller's risk.

---

## 1. Scope

The SUNSET documents in this repository: [stamp-format.md](stamp-format.md), [tokenomics.md](tokenomics.md), the node specifications, and the carrier board they run on ([SUNDIAL hardware/CARRIER.md](https://github.com/photovoltaic-art/SUNDIAL/blob/main/hardware/CARRIER.md)), including year 2 of [PVA's growth model](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md), when nodes are owned separately.

## 2. What is worth protecting

| Asset | Why it matters |
| --- | --- |
| **Stamps in circulation** | They buy lots, shouts, flips and coins; a forgery or theft is a real loss to a visitor |
| **The issuance rules** | Walk and sun are the only sources; breaking them breaks the economy |
| **Node signing keys** | A stolen key can sign stamps and blocks for that node |
| **The coin ledger and stock** | The town's hard money and savings |
| **Goods in the auction's lockers** | Real objects, real value |
| **The hardware** | Batteries, Victron controllers, the arm, the flip-dot panels: about €300–1,000 per interactive node |
| **The record** | The chain, Sole and the explorer are the work's honesty |
| **People's privacy** | The work keeps no one (manifesto, principle 5) |
| **Public safety and PVA's liability** | Objects, batteries, water and messages in public space |

## 3. Who might attack

| Attacker | Wants | Can |
| --- | --- | --- |
| Curious visitor | To see what happens | Use the pages, the slots, the knobs |
| Cheating visitor | More stamps or coins than earned | Copy their own phone, collude with a friend, shuttle between walls, tamper with a coin |
| **Bot operator** | Walk stamps and the sun's purse without walking or playing | Cheap ESP32 relays at every node, a directional antenna, a script in the arm's queue |
| Nearby radio attacker | To steal or forge | Run a fake access point (about €5), flood or deauthenticate the open Wi-Fi, transmit ESP-NOW |
| Coin cloner | Other people's savings | Read coins with any phone, write clones to €1 "magic" tags, watch the coin lookup |
| Thief or vandal | Hardware, goods, damage | Prise, cut, steal a cabinet or a board |
| **Dishonest node owner (year 2)** | To mint, to steal passports | Hold their node's key, flash their own firmware, tamper with its sensors, log what their radio sees |
| Someone with an extracted key | To mint | Sign as one node, with any date |
| Abuser of the public channels | To fence, defame, harass | Use the auction and the shouts as designed |

---

## 4. Threats by surface

### 4.1 The open Wi-Fi and the shared web address

All nine nodes answer at `http://192.168.4.1`. That shared address is what lets the browser carry the courier's bag of blocks between nodes; it also means every page served there, by a genuine node or by an impostor, can read everything the browser has stored for it.

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Sniffing stamps off the air | **Robust** | Holder keys and one-use, challenge-bound signatures: nothing reusable is sent (stamp-format.md 3.1) |
| Sniffing auction claims | **Robust** | Commit and reveal (interactive-auction.md 3.5) |
| **A fake SUNSET network reads the passport** (C1, attack A) | **Gap: critical** | An evil twin with the wall's SSID is the *same site* to the browser: it reads every stamp's private key and every auction claim, spends them first, and can take a won lot. **Fixes, together:** (a) passport keys stored **encrypted under a PIN** the visitor types (a fake page can still ask for it, but can't empty passports silently or at scale); (b) short expiry; (c) a **holding cap** (about 20 stamps) beyond which the page suggests coins; (d) **actions bound into the spend signature** (M2) so a captured signature can't be re-aimed; (e) the plates and rules say plainly that a fake network can steal a passport, and *SUNSET only asks for your PIN to spend* |
| **Cache poisoning** (C1, attack B) | **Gap: critical** | The impostor serves the page and crypto library with a year-long cache header; the next genuine node then runs the attacker's script, which quietly swaps in the attacker's holder key at every earning. **Fix:** genuine nodes serve one page with the crypto **inlined** and `Cache-Control: no-store`, under a path that changes daily; the page checks the node's identity by asking it to sign a fresh challenge with its published key. Partial: an honest page can detect a fake node, not stop a fully fake page |
| **A dishonest owner's node serves hostile script** (C1, attack C) | **Decision** (5, D1) | Same origin means one bad node reads every visitor's passport. A separate origin per node contains it, but breaks the shared courier bag |
| WPA2/WPA3 with a printed password | **Not adopted** | Stops passive sniffing (already robust) but not an evil twin that knows the printed password; adds a step for every visitor. Revisit only if OWE (Enhanced Open) works on the ESP32 SoftAP, which would also bring protected management frames (H5) |
| Filling or wiping the courier's storage | **Accepted** | Blocks are signed; a wiped bag loses nothing held elsewhere |
| **Association flooding and deauthentication** (H5) | **Gap** for the auction; **accepted** elsewhere | SUNDIAL can accept a jammed artwork; an auction with deadlines cannot. Fixes: **anti-snipe** (a bid in the last 10 minutes extends the hammer by 10, within the sunset rules: the hammer never moves past the node's own close); the collection deadline **pauses** while the node sees a full client table or a deauth storm; a *network under load* line on the page; a physical **reserve button** on the cabinet that holds a slot for the person standing there |
| Fake official notices in shouts; Unicode tricks (L1) | **Gap (small)** | Node notices drawn in a style shouts can't use; strip bidi controls and zero-width characters |
| Whisper and shout flooding (L2) | **Gap (small)** | The v0 per-phone limit counts MAC addresses, which phones randomise; add a per-connection rate limit and a small stamp cost for whispers above a free quota |

### 4.2 The ESP-NOW link (gettoneria ⇄ flip-dot wall)

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **Forged ledger messages** (H3) | **Gap: high** | **The gettoneria is authoritative.** The flip-dot wall sends *request spend coin X*; it acts only on a signed *granted X, seq n* reply. Every message signed with the node key, carrying a counter kept in flash; ESP-NOW encryption (a key per peer) as a second layer only; frames accepted only from the paired peer |
| **Race:** a coin and its clone at both nodes in the same second (H3) | **Gap** | Solved by the single authority: the second request is refused |
| Jamming the link | **Accepted, fail-closed** | No reply within a timeout: the flip-dot wall **returns the coin to the cup** (never keeps it), lights red and shows *link down* |
| The auction on the same link | **Gap (if adopted)** | If the auction joins the live spent list (4.4, H10), it uses the same protocol |

### 4.3 Node keys, the board and the firmware

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Key generated off the node | **Gap (to specify)** | Generated **on the node**, at installation and at the year-2 handover, never exported. **Only after the radio is up** (or with `bootloader_random_enable()`): before that the ESP32's random numbers are not truly random (H6) |
| **The gettoneria's key and the coin batch** (contradiction 1) | **Gap** | The coins are signed by a bench script, but the key lives on the node. Fix: the gettoneria signs the batch itself, over its USB cable at the bench, and only the list leaves; the coin list is then co-signed by the keyholders |
| **A stolen board gives up its key** (H6) | **Gap** | The ELEGOO board unplugs from its sockets in seconds. Fixes: **Secure Boot v2 and flash encryption in Release mode**, ROM download mode secure or off, JTAG off; **chip revision v3** checked on delivery; the module glued or potted in place; yearly updates by a signed image over the cable, not plain `esptool`. Still assume a lab attacker gets the key (published fault-injection attacks on the original ESP32), so **revocation (4.4) must work.** Option for later: a secure element on J13 (NXP SE050 does Ed25519) |
| A memory-safety bug leaks the key at runtime (H6, M5) | **Gap** | Flash encryption doesn't protect a running node. Streaming JSON parsing with strict field limits, a current ESP-IDF, the smallest possible web server |
| **Key replacement mid-season** (contradiction 2) | **Gap** | Public keys are compiled into firmware and firmware changes once a year, so a replaced node is untrusted and the old key stays trusted. Fix: compile in the **keyholders'** public keys too; a revocation or enrolment notice **co-signed by k of n keyholders** travels like a block (4.4) |
| Firmware altered at source or on the build machine (M8) | **Gap** | Pinned and vendored libraries, the build environment published as a container, Secure Boot keys held offline, reproducible builds; an admin action **shows the running firmware's hash**, backed by Secure Boot, so it reflects what the box runs, not what PVA published |
| Firmware altered in the field | **Robust** | No update over Wi-Fi; the box needs a tamper bit and USB. In year 2 an owner can of course flash their own: that is 4.4's quarantine and D1 |
| **The arm's stock firmware** (H2) | **Gap: high** | The RoArm-M2-S ships with its own Wi-Fi access point, web page and ESP-NOW control: anyone in range can drive it past the carrier's limits. Fix: flash a trimmed arm firmware with **Wi-Fi, Bluetooth and ESP-NOW compiled out**, and the soft limits on the arm's own controller as well |
| **Bluetooth Classic on the set** (M10) | **Gap** | Published Bluetooth bugs on the original ESP32 (BrakTooth) include code execution. Never discoverable, outgoing connections only to the bonded speaker, current ESP-IDF; and the set holds **no stamp-signing key**, since it neither issues nor spends |

### 4.4 Issuance, spending and the ledger

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Forged stamps or blocks | **Robust** | Ed25519 everywhere |
| **A stolen key or dishonest owner mints future-dated, never-expiring stamps** (C3) | **Gap: critical** | Check 4 (the stamp is in its issuer's block) is skipped when the block is missing, and a future-dated stamp never has one. **Hard checks at every spend:** `day` ≤ today ≤ `exp`; `exp` − `day` ≤ the rule's validity for that `why`; a **role list** (only walls and other nodes issue `walk`, only the arm `skill`, only the gettoneria `redeem`, only the auction `refund` and `payout`) |
| **Issuance bounds checked only by the explorer** (C3, contradiction 9) | **Gap: critical** | Each node checks every block it receives: walk ≤ 8 with matching deliveries; skill ≤ sunlight ÷ R and ≤ the clear-sky ceiling, and ≤ k × the median of the walls' sun readings that day (M11); refunds and payouts ≤ spends into that node. A node whose block breaks a bound is **quarantined**: its stamps refused from then on, shown on the dial tone |
| Stamps whose issuing block never arrives (C3) | **Gap** | After a grace period (1 day proposed, to set in the pilot) a stamp is accepted only if its issuing block is held and lists it |
| **The gettoneria launders bad stamps into coins** (C3, H10) | **Gap** | The **mint gate:** the gettoneria accepts only stamps whose issuing block it holds and that are at least a few hours old, and checks the live spent list shared with the auction (4.2). Coins minted with a stamp later proved double-spent are marked **tainted** in the ledger |
| **Two different blocks for one node and day** (M4) | **Gap** | Two valid signed blocks for the same `node/day` are proof of misbehaviour: carried like a block, the key quarantined, shown on the dial tone. *The seal is unchanged; this is a check on what arrives* |
| No revocation (C3) | **Gap** | k-of-n keyholder notices (4.3) |
| **The double spend** (H10, contradiction 7) | **Accepted, re-bounded** | Draft 1 and stamp-format.md said at most one extra use. With several copies of the storage, a stamp can be spent once at **every spending node that hasn't heard**: up to about five. Text corrected; the mint gate and taint guard the one route into hard money |
| **The spend signature doesn't bind the action** (M2) | **Gap** | Sign `spend|ids|node|challenge|H(action)`, the action naming the lot, amount, claim hash, refund and change keys, and the shout's text hash |
| **Canonical JSON and signature strictness** (M3) | **Gap** | Adopt RFC 8785 exactly; refuse duplicate keys and floats; verify the received bytes; a strict Ed25519 (reject non-canonical S and small-order points: Monocypher or libsodium); identify blocks by `node/day/seq`; cross-implementation test vectors (Python, JS, ESP32) in the test bed |
| **Block caps freeze the auction and can't carry the gateway** (H4, contradiction 3) | **Gap** | One `spent` entry per *spend request* (up to 50 IDs, one holder signature), one `issued` entry per batch; a size budget per role (the gateway pair needs far more than a wall); a limit on `tokens`; the auction keeps room so refunds always fit. *Changes what a block lists, not the seal* |
| **Shill auctions renew stamps** (M1) | **Decision** (5, D5) | A payout carries a fresh `exp`: auction a pebble to yourself to renew any amount for one stamp |
| **Clock rollback revives spent stamps** (H7) | **Gap: high** | Draft 1 rated this robust; it isn't. A dead coin cell or a nudge moves the clock back and pruned spent IDs become spendable. Fixes: keep spent IDs for a fixed number of **sealed days**, not by the wall clock; a **monotonic day counter** in flash, and no business if the RTC reads earlier than the last sealed day or more than 2 days later; a **cumulative** clock-correction limit (±10 min a week); a coin-cell failure stops spending with a service notice |
| **Resource exhaustion** (M5) | **Gap** | The original ESP32 has no PSRAM: stream-parse, size limits per field, cheap checks before signature checks, a fast Ed25519 measured on the board, a per-connection request rate, and a **storage quota per issuing node** so one node's padded blocks can't evict others'; `spent` records kept first |
| Adding coins | **Robust** | Year's coin list frozen by fingerprint; unknown IDs refused; redemptions name their coin |
| Changing the rules quietly | **Gap (proposed)** | The rules' fingerprint in every block is proposed for the next format version (tokenomics.md 3), not yet in v1: wording in tokenomics.md now says so (contradiction 6) |
| Farming walk stamps by shuttling | **Robust** | One stamp per block per node: the 72 cap |
| **Walk stamps captured by bots** (H1) | **Decision** (5, D3) | First delivery wins, so the race goes to relays at every node or a directional antenna at dawn, not to walkers |
| **The arm game botted** (H2) | **Decision** (5, D4) | Pegs return to the same place and the arm is precise: a recorded sequence wins every time and drains the sun's purse |
| **Sun-sensor tampering** (M11) | **Gap** | Reference cell out of reach; the peer bound above; the arm's day held as provisional until the walls' readings arrive |

### 4.5 Maintenance access

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **Admin actions with no specified protection** (H8) | **Gap: high** | Write SUNSET's admin section: **per-node keys** (no master shared across owners), challenge and response, action-scoped codes, cumulative limits, lockout, an action log kept on the node and downloaded at the round. **Admin secrets never stored by the browser** at the shared address (typed each time, or a separate port): SUNDIAL's "remembered by the browser" round master would be readable by every node in town (C1) |
| Return mode abused | **Gap (small)** | Return mode accepts only coins in the *spent* state, never *issued*, and logs each ID; it issues no stamps |
| **Return mode after sunset** (contradiction 5) | **Gap (to reconcile)** | Business closes at sunset, but return mode is described in the evening. Fix: return mode is a maintenance action at the gettoneria only, by cable or during daylight; to align interactive-token.md 3.7 and SUNSET.md 3 |
| Downloads in clear | **Gap (small)** | Full blocks are meant to stay private until the season's end; download them by cable, or encrypted to PVA's key |

### 4.6 NFC coins and the coin path

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Rewriting a coin's tag | **Robust** | Locked after the batch; the signature covers the ID |
| **Cloning a coin, with a live lookup to choose which** (C2) | **Decision** (5, D2) | Draft 1 accepted cloning as "first use wins". The reviewer shows the cost: the lookup by printed number tells a thief which coins are out in town, the clone is spent first, and the **honest holder's genuine coin is confiscated** |
| **Confiscating the second copy** (C2) | **Gap: adopt now** | Return the second copy to the cup with *this coin was used by someone else at HH:00*, and log both. Confiscation punishes the victim and hides the evidence |
| Bench check | **Gap (small)** | Check the hopper as well as the reject and kept boxes for duplicates, and NXP's originality signature (`READ_SIG`), which catches lazy clones only |
| Real money or slugs in the slot | **Robust** | The acceptor returns non-tokens (interactive-token.md 4.5) |
| **Boot-state glitches** (L4) | **Gap (small)** | PCF8574 outputs and GPIO 17 must power up as **inhibited**: set polarity and add pull resistors |
| Hopper count drift (L6) | **Gap (small)** | Reconcile against ccTalk payout counts; refund automatically if the hopper under-pays |
| **Year-end coins** (contradiction 4) | **Gap (to reconcile)** | Expired coins return "for the new year", yet each year has a new batch and list. Fix: re-keyed into the next year's batch (rewritten, re-signed, on the new list), or retired as souvenirs: to decide with the year's batch |
| The verify links on the coins depend on one domain forever (M8) | **Gap** | Domain registered long-term with registrar lock and 2FA; a hardware key on the GitHub organisation; a versioned verify page in the repository |

### 4.7 Physical security and safety

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **Theft of batteries, controllers, the arm, the panels** | **Gap** | Steel cabinets, security fixings, anchored; batteries out of reach and out of sight; tamper switch posting a service notice; insurance covering theft |
| **Battery fault current** (M7) | **Gap: adopt now** | A **fuse (MRBF class) at the battery terminal** and a disconnect; the battery-tier diagram fuses only the load output |
| **Battery temperature** (M7) | **Gap** | LiFePO₄ must not charge below 0 °C or above about 45 °C: a Victron Smart Battery Sense or a BMS with temperature cut-offs; cabinets ventilated and shaded |
| Lithium items in the lockers (M7) | **Gap** | Rule against cells in lots; the lockers away from the node's battery |
| Prising a locker; magnets on switches and latches (L3) | **Gap (small)** | Polycarbonate, not acrylic; shielded latches; hidden or hall-effect sensors; an inner steel frame |
| Water and electricity at the garden node; climbing; tank tampering (M7, L7) | **Gap** | Electronics high, drip loops, sealed connections, checked by an electrician; a locked tank cap; the IBC cage not climbable |
| The arm's moving parts | **Robust, once H2 is fixed** | Behind perspex; load limits on both controllers |

### 4.8 Privacy, the website and the explorer

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **The live coin lookup tracks coins** (M6, contradiction 10) | **Gap** (with D2) | A lookup by printed number at any wall, any time, contradicts the weekly-only coin table. Fix: away from the gateway, answer only *genuine / not genuine*; per-coin state at the gettoneria only, for the coin in the slot |
| Stamp lookup by ID | **Gap** | Remove, or delay to the season's end |
| Linking stamps spent together; routes from walk stamps (M6) | **Gap, mitigated** | Weekly totals only, full blocks at the season's end (tokenomics.md 4.3); consider publishing only totals and commitments |
| A node owner logs what their radio sees (M6) | **Accepted, stated** | The rules say plainly that a node's owner can log anything their radio hears |
| A fake explorer or altered numbers | **Robust** | Anyone can rerun the verifier on the published blocks |

### 4.9 Legal and abuse

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **The auction as fence or dead drop** (H9) | **Gap** | Lots must show their **contents** (no sealed boxes or envelopes); a size limit; lots visible for a day first; a *withdrawn* state by k-of-n or owner key; the page states the seller's responsibility; a lawyer and the comune before year 2 |
| **Unmoderated paid shouts** (H9) | **Gap** | A **takedown** record (owner-signed or k-of-n) carried like a block: walls hide the words, keep the header, show *a shout was withdrawn*. **A whisper is promoted to a shout only by its own author** (a one-time key held by the writer). A printed notice of what's forbidden and a contact for reports |
| Whispers as an anonymous chat with no age gate (H9) | **Gap (to discuss)** | Foreseeable misuse; the lawyer's review covers it |
| **Tokens traded for goods** (H9) | **Gap** | Whether a circulating unit cafés accept raises payment-services, complementary-currency or tax questions in Italy: a lawyer before launch |
| An obscene picture on the flip-dot wall (L5) | **Gap (small)** | A reset policy and an admin *clear region* |
| Selling coins or stamps for cash | **Accepted** | No cash enters or leaves SUNSET |

---

## 5. Decisions for Carl

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| **D1** | **One shared address, or one per node?** (C1, M9) | **(a)** Keep the shared address: the courier bag works as designed; a hostile node or fake network can still reach the passport, mitigated by PIN encryption, small holdings, bound actions and no cached script. **(b)** A separate address per node: a dishonest owner's node can no longer read anyone else's passport, but the browser's storage no longer travels between nodes, so the courier bag needs redesigning | **(a) for year 2,** with every 4.1 fix, plus a **one-owner-one-node rule** so no single owner controls many nodes; revisit (b) if owners are not people PVA knows |
| **D2** | **Cheap coins with cloning, or unclonable coins?** (C2, M6) | **(a)** NTAG 424 DNA (AES per tag, authenticated at the gettoneria and flip-dot wall): about €0.50–1 more per coin, €500–1,000 for the stock; readers must speak AES. **(b)** Keep NTAG213, **remove the live per-coin lookup**, stop confiscating, check `READ_SIG` | **(b) is the minimum and is adopted either way.** (a) if the coins are meant to hold real savings: cloning then stops being "a recognised bug" and becomes theft from third parties |
| **D3** | **Walk stamps: who wins the race?** (H1) | **(a)** Accept and say so: walk stamps go to the fastest, often a machine. **(b)** A **lottery** among everyone who delivers within the first hour. **(c)** A **physical touch** at the wall (a capacitive pad on J9) within seconds of the delivery. **(d)** A minimum transit time between a signed pickup at A and delivery at B | **(b) + (c):** cheap, and they keep the walker the winner. (b) changes who is paid, not the seal |
| **D4** | **The arm: phone or joystick?** (H2) | **(a)** Phone control, with randomised peg presentation, jitter and per-connection limits. **(b)** A **joystick on the cabinet**; the phone only receives the stamp | **(b):** a player has to be there; it also removes the queue from the Wi-Fi |
| **D5** | **Auction payouts: fresh expiry?** (M1) | **(a)** Keep: the seller's payout is fresh. **(b)** Payout carries the earliest `exp` of the winning bid's stamps (plus a day). **(c)** A seller fee proportional to the price | **(b)**, so the only way to keep value stays the minting fee |

## 6. Fixes, in order

| # | Fix | Before |
| --- | --- | --- |
| 1 | **Spend checks:** `day`/`exp`/role, bounds in the network, quarantine, equivocation proofs, k-of-n revocation and enrolment, the gettoneria's mint gate (4.4) | Any firmware; certainly before the year-2 handover |
| 2 | **The passport:** PIN encryption, holding cap, bound actions (M2), no cached script, node identity check, honest wording (4.1); D1 | The phone-side code |
| 3 | **Coins:** D2; no confiscation; lookup reduced to genuine or not (4.6, 4.8) | Ordering the coins |
| 4 | **The gateway protocol:** gettoneria authoritative, signed, counted, fail-closed (4.2) | The gateway firmware |
| 5 | **Format:** RFC 8785, strict Ed25519, aggregated entries and per-role size budgets, test vectors (4.4) | Extending the test bed to v1 |
| 6 | **Board and keys:** Secure Boot v2 and Release-mode flash encryption, RNG at keygen, chip v3, module fixed, the batch signed by the gettoneria itself (4.3) | Keying the first node |
| 7 | **Clock:** monotonic day counter, spent IDs kept by sealed days, cumulative correction limit (4.4) | Any firmware |
| 8 | **Maintenance access:** SUNSET's admin section, per-node keys, nothing stored by the browser (4.5) | Any firmware |
| 9 | **The auction:** anti-snipe, paused deadlines under flooding, reserve button, contents visible (4.1, 4.9); D5 | The auction firmware |
| 10 | **Fair issuance:** D3 and D4; the arm's own firmware stripped of radios (4.3) | The pilot |
| 11 | **Physical:** battery-terminal fuse, temperature-aware charging, steel cabinets, insurance (4.7) | Building the interactive nodes |
| 12 | **Legal:** takedown, author-only promotion, lot rules, token trade, checked with a lawyer and the comune (4.9) | Year 2's permissions |
| 13 | **Supply chain:** reproducible builds, pinned libraries, offline signing keys, the domain and GitHub organisation locked (4.3, 4.6) | The year-2 handover |

## 7. Accepted risks, stated in public

- **The double spend:** up to about five uses of a copied stamp before the news arrives; proved and shown; guarded at the gettoneria by the mint gate and taint.
- **Denial of service** on an open network, except where 4.1 makes the auction robust.
- **A determined lab attacker** extracting a key from a stolen board, made survivable by quarantine and revocation.
- **The goods in a locker** are the seller's risk.
- **A node's owner can log what their radio hears.**
- **A fake network can still phish a passport's PIN** from someone who types it into a fake page: bounded by the holding cap and short expiry.

---

## 8. Independent review

**Reviewer:** an independent, adversarial reviewer, working from the design documents only; it did not read this file. Full report: [security/independent-review-2026-10.md](security/independent-review-2026-10.md) (3 critical, 10 high, 11 medium, 8 low findings; 15 contradictions).

**How the two passes compare.** Both found the shared-address passport theft, the missing ESP-NOW protocol, maintenance access, ESP32 key handling, theft and battery safety, and the legal exposure of the auction and shouts. The reviewer went further in three places that change draft 1's conclusions: **future-dated stamps** (draft 1 wrongly rated issuance as bounded under a stolen key), **cache poisoning** (worse than reading storage), and **cloned coins plus the live lookup** (draft 1 accepted cloning). Draft 1 had rated clock tampering robust; the reviewer showed rollback. All of these are corrected above.

### 8.1 Findings and resolutions

| # | Finding | Severity | Resolution |
| --- | --- | --- | --- |
| C1 | Shared address over HTTP: evil twin, cache poisoning, hostile owner node | Critical | **Agreed.** Fixes in 4.1; per-node address is **D1** |
| C2 | Cloned coins plus the live coin state: theft of savings, honest coin confiscated | Critical | **Agreed.** No confiscation and no live lookup adopted (4.6, 4.8); tag choice is **D2** |
| C3 | Stolen key or owner mints future-dated, never-expiring stamps; no in-network bounds; no revocation | Critical | **Agreed.** Fix 1 (4.4, 4.3) |
| H1 | Walk stamps captured by relays, antennas, cyclists, deauth | High | **Agreed.** **D3** |
| H2 | Arm game botted; the arm's stock firmware exposes Wi-Fi and ESP-NOW | High | **Agreed.** Firmware stripped (4.3); control is **D4** |
| H3 | Gateway ESP-NOW unspecified: forgery, races, jamming | High | **Agreed**, with the reviewer's stronger design: one authoritative node (4.2) |
| H4 | Block caps freeze the auction and can't carry the gateway's traffic | High | **Agreed.** Aggregated entries, per-role budgets (4.4); the seal untouched |
| H5 | Wi-Fi flooding and deauth snipe the auction and force forfeits | High | **Agreed.** Anti-snipe within the sunset close, paused deadlines, reserve button (4.1) |
| H6 | ESP32 key protection weaker than assumed | High | **Agreed.** 4.3 |
| H7 | Clock rollback revives spent stamps; repeated nudges | High | **Agreed;** draft 1 was wrong. 4.4 |
| H8 | SUNSET admin unspecified; SUNDIAL's leaks the round master at the shared address | High | **Agreed.** 4.5 |
| H9 | Shouts, whispers, the auction and token trade: legal exposure | High | **Agreed.** 4.9 |
| H10 | Double spend up to ~5 uses, laundered into coins | High | **Agreed.** Text corrected; mint gate and taint (4.4) |
| M1 | Shill auctions renew stamps | Medium | **D5** |
| M2 | Spend signature doesn't bind the action | Medium | **Agreed.** 4.4 |
| M3 | Canonical JSON and Ed25519 strictness | Medium | **Agreed.** 4.4 |
| M4 | Equivocation | Medium | **Agreed** as a check on received blocks. The reviewer's suggestion to change sealing is **not adopted: the seal stays as it is.** One seal per day is already the rule; a wall that browns out mid-seal and seals again would be a firmware bug, to test for on the bench (power cut during sealing), not a design change |
| M5 | Resource exhaustion on the ESP32 | Medium | **Agreed.** 4.4 |
| M6 | Deanonymisation | Medium | **Agreed.** 4.8 |
| M7 | Battery fuse, temperature, lithium in lockers, theft, the garden tank | Medium | **Agreed.** 4.7 |
| M8 | Supply chain; the coins' verify links tied to one domain | Medium | **Agreed.** 4.3, 4.6 |
| M9 | Year-2 governance capture; frozen rules bind only honest owners | Medium | **Agreed.** One-owner-one-node, supply changes above a simple majority, quarantine (4.4); tokenomics.md 5 to update |
| M10 | Bluetooth Classic on the set | Medium | **Agreed.** 4.3 |
| M11 | Sun-sensor tampering | Medium | **Agreed.** 4.4 |
| L1–L8 | Fake notices, flooding, locker magnets, boot states, the flip-dot picture, hopper drift, tank tampering, refunds to absent bidders | Low | **Agreed.** 4.1, 4.6, 4.7, 4.9; L8 below |

### 8.2 Contradictions between documents

| # | Contradiction | Resolution |
| --- | --- | --- |
| 1 | The gettoneria's key vs a bench script signing coins | The gettoneria signs its own batch over its cable (4.3). To edit interactive-token.md 2.2, 4.1 |
| 2 | Key replacement impossible mid-season | k-of-n enrolment and revocation (4.3). To edit stamp-format.md 2 |
| 3 | Gateway capacity vs block limits | Aggregated entries, per-role budgets (4.4). To edit stamp-format.md 7 |
| 4 | Expired coins back to the hopper vs a new batch each year | To decide with the year's batch (4.6) |
| 5 | Return mode after sunset | Maintenance action only (4.5). To edit interactive-token.md 3.7, SUNSET.md 3 |
| 6 | Rules fingerprint presented as current | **Fixed** in tokenomics.md (TL;DR now says it is proposed) |
| 7 | Double spend "at most one extra use" | **Fixed** in stamp-format.md 5.2 |
| 8 | Stolen-key stamps "fail check 4" vs check 4 skipped | Hard checks and the grace period (4.4). To edit stamp-format.md 3.3, 3.4, 5.1 |
| 9 | Clear-sky ceiling enforced only by the explorer | **Fixed** in tokenomics.md's wording; enforcement in 4.4 |
| 10 | Weekly coin table vs a live lookup at every node | Lookup reduced (4.8). To edit wall-node.md 1.3, interactive-token.md 3.6 |
| 11 | The close of day: sunset vs dusk by panel voltage | **The seal is unchanged.** Only to write down, in wall-node.md, what a wall already does under GO TO BED when its light fails before sunset |
| 12 | GPIO 17 still listed as VE.Direct TX | **Fixed** in interactive-auction.md and interactive-audio.md |
| 13 | "Nothing worth copying crosses the open Wi-Fi" | **Fixed** in SUNSET.md and stamp-format.md 3.1: true for listeners, not for a fake network |
| 14 | v0's per-phone limits "stand" though MAC addresses can't be trusted | Per-connection limits and a whisper cost (4.1). To edit stamp-format.md 1, 7 |
| 15 | Refunds "at once" to an absent bidder | The refund goes to a holder key committed with the bid, collected at any node, with `exp` at least a few days on (L8). To edit interactive-auction.md 3.4 |

### 8.3 What the reviewer found robust

Holder keys; challenge-bound spend signatures; value held in the ledger, not the coin; commit and reveal against listeners; no update path over the air; flash-before-act and a power-safe file system; fail-secure locks, the redeem flap resting on reject, real money returned; JP1 with the compile-time switch; text-only rendering of messages; data kept to the hour with no phone identifiers; *refuse, never truncate*; the coin list frozen by fingerprint; the explorer recomputing from signed headers; the arm wired by UART rather than radio.
