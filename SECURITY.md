# SUNSET security — threat model and audit

> Status: draft 1, 27 Oct 2026. A design-stage audit of SUNSET as specified (no firmware exists yet), written in two passes: the authors' own analysis, then an **independent review** by a reviewer who had not seen the design discussion (section 7, pending). Each threat has a status: **robust** (the design already handles it), **gap** (a fix is proposed), or **accepted** (a known, bounded risk, stated in public).

---

## TL;DR

- **The money's cryptography is sound:** Ed25519 signatures on every stamp, coin and block; holder keys so nothing reusable crosses the air; sealed, chained daily blocks; issuance bounded even if a node key is stolen.
- **The weakest point is the phone, not the node.** Every node answers at the same web address, so a **fake SUNSET Wi-Fi** can read a passport's stored stamp keys. Fix: a passport PIN, short-lived stamps, and limits on how much a passport holds (4.1).
- **Three things still need designing before firmware:**
  - the **ESP-NOW link** between the gettoneria and the flip-dot wall (authenticated, encrypted, replay-proof);
  - **maintenance access** for SUNSET nodes (SUNDIAL's challenge-and-response login, extended to owners);
  - **key handling** on the ESP32 (generation on the node, flash encryption, what a stolen board means, and replacement).
- **Physical and legal risks are as real as the digital ones:** batteries worth stealing in public cabinets; an anonymous auction that could fence stolen goods; unmoderated paid shouts on public walls.
- **Accepted, in public:** the cloned-phone double spend, cloned coins (first use wins), and denial of service on an open network.

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
| Nearby radio attacker | To steal or forge | Sniff the open Wi-Fi, run a fake access point, transmit ESP-NOW |
| Thief or vandal | Hardware, goods, damage | Prise, cut, steal a cabinet or a board |
| Dishonest node owner (year 2) | To mint for themselves | Open their own box, hold their node's key, tamper with its sensors |
| Someone with an extracted key | To mint | Sign as one node |
| Abuser of the public channels | To fence, defame, harass | Use the auction and the shouts as designed |

---

## 4. Threats by surface

### 4.1 The open Wi-Fi and the shared web address

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Sniffing stamps off the air | **Robust** | Holder keys and one-use signatures: nothing reusable is sent (stamp-format.md 3.1) |
| Sniffing auction claims | **Robust** | Commit and reveal: the secret is revealed only as it is used (interactive-auction.md 3.5) |
| **A fake SUNSET network steals the passport** | **Gap: the most serious** | Every node is `http://192.168.4.1`, which is what lets the browser's storage carry blocks between nodes. But a fake access point serving the same address is the *same site* to the browser, and can read the passport: **every stamp's private key**. Fixes, together: **(a)** the passport's keys stored encrypted under a short **PIN** chosen by the visitor (a fake page can still ask for the PIN, but can't empty passports silently or at scale); **(b)** stamps expire in days, so a theft is short-lived; **(c)** a **cap on what one passport holds** (for example 20 stamps), beyond which the page suggests coins; **(d)** the wall plates and one-screen rules say: *SUNSET never asks for your PIN except to spend* |
| A fake network serves altered pages or a malicious crypto library | **Gap** (same root) | Same fixes; plus the page checks the node's identity by asking it to sign a fresh challenge with its published key before showing balances, so a fake node is visible to an honest page (it cannot stop a fully fake page) |
| Filling or wiping the courier's storage | **Accepted** | Blocks are signed; a wiped bag loses nothing that isn't held elsewhere. Storage limits per phone already apply (stamp-format.md 7) |
| Ten connections taken, jamming | **Accepted** | An open network can't prevent it; it ends when the person leaves. As SUNDIAL.md 4.3 |

### 4.2 The ESP-NOW link (gettoneria ⇄ flip-dot wall)

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **Forged ledger messages** (mark coins live: minting; mark coins spent: denial of service) | **Gap** | The specs say the two share the ledger live but not how. Fix: every message **signed** with the sender's node key, carrying a **counter** (replay-proof) and the coin ID; ESP-NOW's own encryption on (a shared key per pair) as a second layer; each node accepts only its known peer |
| Jamming the link | **Accepted, with a fail-safe** | If the link is down, the flip-dot wall **stops accepting coins** (light red, *link down* notice) rather than accept without the live ledger |

### 4.3 Node keys and the board

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Key generated off the node | **Gap (to specify)** | Keys **generated on the node** at installation (and at the year-2 handover), never exported; only the public half leaves |
| A stolen board gives up its key | **Gap** | Flash encryption and secure boot on. The **original ESP32** has published fault-injection attacks on both, depending on chip revision, so assume a determined thief with the board *can* extract the key. Fix: check the ELEGOO boards' chip revision (v3 or later); and rely on the **issuance bounds** (4.4) so an extracted key buys little |
| Key replacement | **Gap (to write down)** | Procedure: new key on the node, old key's last valid day published, stamps signed after it refused (stamp-format.md 2 states the rule; the steps and who signs the announcement are still to write) |
| Firmware altered | **Robust in the field** | No update path over Wi-Fi; the box needs a tamper bit and USB (as SUNDIAL). **Gap at source:** reproducible builds and published fingerprints, so owners can check what they flash (tokenomics.md 5) |

### 4.4 Issuance and the ledger

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Forged stamps or blocks | **Robust** | Ed25519 everywhere |
| A node (or extracted key) minting walk stamps | **Robust, once checks are built** | At most 8 a day per node, each matched to a real delivery of another node's signed block (stamp-format.md 3.2) |
| Minting sun stamps beyond the sky | **Robust, once checks are built** | Sunlight ÷ R, the clear-sky ceiling, and the cross-check against the walls (tokenomics.md 2.2) |
| Adding coins | **Robust** | The year's coin list is frozen in the rules; unknown IDs refused everywhere; redemptions name their coin |
| Changing the rules quietly | **Robust (once added)** | Rules frozen per season; the rules' fingerprint in every block (tokenomics.md 3) |
| **The cloned-phone double spend** | **Accepted** | Bounded, proved, shown (stamp-format.md 5) |
| Cloned coins | **Accepted** | First use wins; later copies kept (interactive-token.md 2.4) |
| Farming walk stamps by shuttling | **Robust** | One stamp per block per node: the 72 cap |
| Clock tampering to dodge expiry or the seal | **Robust in the field** | Visitors can never set the clock (as SUNDIAL); the DS3231 keeps time through the night; clock changes need the admin login (4.5) and are logged |

### 4.5 Maintenance access

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **Admin actions with no specified protection** (return mode, coin-table download, block download, the auction's lots, the set's music) | **Gap** | Adopt SUNDIAL's design (SUNDIAL.md 4.3) for every SUNSET node: challenge and response, a **round key** (downloads, return mode) and a **setup key** (anything that changes a node), lockout, an action log carried in the sealed block. In year 2, each **owner** holds their node's setup key |
| Return mode abused to launder clones into the hopper | **Gap (small)** | Return mode only accepts IDs the ledger shows as *spent*; anything else goes to the reject box as usual; the action is logged |

### 4.6 NFC coins and the coin path

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Rewriting a coin's tag | **Robust** | Tags are locked after the batch; the signature covers the ID |
| Cloning a tag | **Accepted** | 4.4 |
| Real money or slugs in the slot | **Robust** | The coin acceptor returns non-tokens; only tokens reach the reader (interactive-token.md 4.5) |
| Forcing the flap or reject box | **Physical** (4.7) | Locked boxes, steel housing |

### 4.7 Physical security and safety

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **Theft of batteries, controllers, the arm, the panels** | **Gap** | Each interactive cabinet: steel, security fixings, anchored to the wall, no visible value; batteries out of reach and out of sight; insurance that covers theft; a *node offline* notice tells the town at once |
| Prising a locker | **Partly robust** | Fail-secure locks; perspex thick enough; a forced door shows on the door switch and posts a notice. The goods themselves are the seller's risk, stated on the page |
| **Battery safety** (LiFePO₄ in a public cabinet) | **Gap (to check)** | LiFePO₄ with a built-in BMS, fused at the battery, ventilated, away from the panel's heat; a temperature cut-off in firmware; a fire-safety check with the host |
| Water and electricity at the garden node | **Gap (to check)** | Electronics high, drip loops, sealed pump connections (garden-node.md 3.1); a residual-current device is not needed at 12 V, but the build should be checked by an electrician |
| The arm's moving parts | **Robust** | Behind perspex; load limits; stops on a fault (interactive-arm-game.md 3.5) |

### 4.8 The website and the explorer

| Threat | Status | Detail and fix |
| --- | --- | --- |
| Deanonymising a visitor from the blocks | **Gap, mitigated** | Full blocks show stamps spent together and where they were earned. Fix adopted: weekly totals only, full blocks at the season's end (tokenomics.md 4.3) |
| A fake explorer or altered numbers | **Robust** | Anyone can rerun the verifier on the published blocks |
| The coin table linking a coin to a person | **Accepted** | Weekly at most; coins identify no one |

### 4.9 Legal and abuse

| Threat | Status | Detail and fix |
| --- | --- | --- |
| **The auction used to fence stolen goods** | **Gap** | An anonymous, unattended sale is attractive to a thief. Fixes: lots visible to the street for a day before sale (the wings already do this); a value ceiling in the rules (a locker's size already limits it); the page states the seller's responsibility; any lot can be withdrawn by PVA on a credible report; check with the comune and a lawyer before year 2 |
| **Unmoderated paid shouts: defamation, harassment, personal data** | **Gap** | "No moderation" is the work's stance, but the shouts go up on public walls in Italy. Fixes: a **takedown** that hides a shout from all walls (the owner's setup key, logged and announced as *a shout was withdrawn*); shouts fade in 7 days anyway; a line on the page about what can't be posted; check with a lawyer |
| Selling coins or stamps for cash | **Accepted** | No cash ever enters or leaves SUNSET; trades between people are their own business (SUNSET.md 2.4) |

---

## 5. Fixes, in order

| # | Fix | Before |
| --- | --- | --- |
| 1 | The passport: PIN-encrypted keys, a holding cap, node identity check, wording on the plates (4.1) | The phone-side code |
| 2 | The ESP-NOW protocol: signed, counted, encrypted, fail-safe (4.2) | The gateway firmware |
| 3 | Maintenance access: SUNDIAL's login for every SUNSET node; owners' keys in year 2 (4.5) | Any firmware |
| 4 | Key handling: on-node generation, chip revision, flash encryption, replacement procedure (4.3) | Keying the first node |
| 5 | Issuance checks and the rules' fingerprint built into nodes and the explorer (4.4) | The first season |
| 6 | Physical: steel cabinets, anchoring, battery safety, insurance against theft (4.7) | Building the interactive nodes |
| 7 | Legal: the auction and the shouts, checked with a lawyer and the comune; the takedown (4.9) | Year 2's permissions |
| 8 | Reproducible builds and published fingerprints (4.3) | The year-2 handover |

## 6. Accepted risks, stated in public

The cloned-phone double spend; cloned coins; denial of service on the open network; a determined thief extracting a key from a stolen board (bounded by the issuance checks); the goods in a locker being the seller's risk.

---

## 7. Independent review

*To be added: the reviewer's findings, and how each is resolved.*
