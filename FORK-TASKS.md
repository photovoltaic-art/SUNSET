# SUNSET — making the repo forkable

**Goal:** any town that has run a SUNDIAL can fork this repository and turn its own nine panels into its own SUNSET: its own keys, coins, rules and website, without asking anyone and without hunting through the code for Bosa.

> Status: task list, 27 Oct 2026. **State: Visible:** public but not yet licensed for reuse. **Released** when every task is done, SUNSET has run a full season in Bosa (2028), and the licences are added (the last step). Builds on SUNDIAL's [FORK-TASKS.md](https://github.com/photovoltaic-art/SUNDIAL/blob/main/FORK-TASKS.md) and on PVA's growth model ([GROWTH.md 5](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md)). Bosa remains the reference instance.

---

## Summary

**The two rules:**
1. **A SUNSET is nine panels.** Nine is where the network, the economy and the governance work (GROWTH.md 5.1).
2. **A SUNSET is never linked to another.** No shared stamps, coins, keys, chain or explorer between towns (GROWTH.md 5.2). Towns grow by forking.

Everything else (the town, the sites, the languages, the logos, the coins' artwork, the prices, the owners) belongs to the fork.

**The one request:** a link back to this repository and to [photovoltaic.art](https://photovoltaic.art), wherever the fork is presented. A request, not a licence condition.

**The model:** fork and run separately, as SUNDIAL. **The path is SUNDIAL first:** a town runs a year of SUNDIAL, then converts the same nine panels (GROWTH.md 2), then hands the nodes to nine owners (GROWTH.md 3).

**The advantage over SUNDIAL:** SUNSET has no firmware yet, so it can be **forkable from the first line**, not retrofitted. Most of the tasks below are rules for how the code is written, not changes to existing code.

**What would stand in the way, if not designed in now:**

1. **Bosa built in:** sunset times, the clear-sky ceiling, the sun's rate R, prices, texts, the website address on the coins.
2. **Towns that could mix:** every SUNSET answering at `192.168.4.1` would make one town's pages able to read another town's passport (SECURITY.md C1).
3. **One town's keys, coins and rules** as the only example, with nothing to stop a fork shipping them.
4. **Suppliers named but not replaceable:** the flip-dot panels (whose drawing is proprietary and not in this repo), the hopper, the arm.
5. **Law written for Italy:** the shouts, the auction and the tokens raise questions that differ by country (SECURITY.md 4.9).
6. **Security not finished:** a fork inherits every gap in SECURITY.md.

**The fix, in one sentence:** extend SUNDIAL's `site/` folder with what SUNSET needs, make every part read from it, keep towns apart by keys and address, make each fork key, coin and calibrate itself, close the security gaps, prove it in Bosa for a season, and only then add the licences.

**Decided: forks choose their nodes from a catalogue.** PVA builds and tests every node in [NODES.md](NODES.md); a fork picks its own nine from it, respecting each node's needs (no flip-dot wall without the gettoneria beside it). Bosa's nine are the reference set. Before SUNSET is licensed, PVA considers, builds and tests further nodes for the catalogue.

---

## Checklist

### 1. Work-in-progress notice

- [x] README: *"Work in progress. Concept and specifications only; nothing is built yet. Not yet licensed for reuse."*

### 1a. The node catalogue

- [x] [NODES.md](NODES.md): what every node must be, the catalogue with each node's status and needs, the candidates, and how a fork chooses its nine (27 Oct 2026).
- [ ] Each of Bosa's nine nodes taken from *specified* to *field-tested*.
- [ ] **Candidates considered** (NODES.md 3): which to build; each specified, bench-tested and piloted before it enters the catalogue.
- [x] No minimum of walls: any nine catalogue nodes (NODES.md 4, 27 Oct 2026).
- [ ] The build, the budget script and `site.json` take any catalogue mix, not only Bosa's.

### 2. One site folder, shared with SUNDIAL

A SUNSET fork reuses its SUNDIAL fork's `site/` folder and adds to it. A fork replaces this folder and nothing else.

- [ ] **`site/site.json`, SUNSET's additions** to SUNDIAL's schema:
  - **town ID** (short, unique, e.g. `bosa`): names the keys folder, the rules file, the coin list, the website paths
  - **the access point's address** for this town (4)
  - **each panel's year-2 role,** any node from the catalogue ([NODES.md](NODES.md)); Bosa's: walls 1–4 (on a wall or a post), gettoneria, flip-dot wall, auction, arm, the set
  - **the season:** first and last day, the spring visit
  - **the website address** for the verify page, the explorer and the coins' links (5)
  - prices that are the town's choice: shout, souvenir, minting fee, listing fee (set in the pilot; stamp-format.md 9)
- [ ] `site/texts/`: the one-screen rules, the wall plates, the page texts, notices (*what can't be posted*, the contact for reports), in the town's languages.
- [ ] `site/art/`: both faces of the coin, with the town's name in row 3 of the PVA logo on the face ([logos/](logos/README.md)). The nine node logos are shared by every town.
- [ ] **No constants in code:** firmware, the phone page, the explorer, the coin batch tool and the budget script read `site.json` through generated files, as SUNDIAL's `site_build.py` (SUNDIAL FORK-TASKS 2.1).

### 3. The sun, calculated for the town

- [ ] **Sunset from the clock,** from the town's coordinates, with SUNDIAL's `sunTimes` (battery-tier.md 1.2): no Bosa times anywhere.
- [ ] **The clear-sky ceiling from latitude:** a clear-sky model computed for the town's coordinates and the reference cell's tilt, not Bosa's numbers typed in (tokenomics.md 2.2; SECURITY.md M11).
- [ ] **The sun's rate R:** a calibration procedure the fork runs in its own pilot, with the reference sensor, before writing its rules file (TASKS.md, tokenomics).
- [ ] **Southern hemisphere:** follows SUNDIAL's (walls facing north; the model mirrored).

### 4. Towns kept apart

No fork may be able to read, spend or confuse another town's stamps, coins or blocks, even by accident.

- [ ] **Keys:** each node accepts only its own town's nine node keys and its keyholders' keys (stamp-format.md 2; SECURITY.md 4.3). Another town's stamps and blocks fail the first signature check. *No change to the block format or the seal.*
- [ ] **The address:** each town's nodes serve at their own access-point address, from `site.json`, so the phone treats each town as a different site and keeps their storage apart. Inside a town, all nine share one address, as designed (the courier's bag; SECURITY.md D1).
- [ ] **Storage named by town:** the phone page keeps its passport and bag under the town ID as well, as a second guard.
- [ ] **A test:** a phone carrying another town's passport and bag (from a second simulated town in the test bed) is refused cleanly, loses nothing, and the other town's storage is not read.

### 5. Keys, coins and rules per town

- [ ] **Keys:** generated on each node (SECURITY.md 4.3); the public halves published in the fork's `keys/`; the firmware **refuses to start** with Bosa's keys, example keys or an empty key set.
- [ ] **The rules file:** `rules-<town>-S<n>` from a template, with the fork's R, ceiling, validity, prices and coin-list fingerprint; its fingerprint in the firmware (tokenomics.md 3).
- [ ] **The coin batch tool:** reads the town ID and website address; the coins' links point to **the fork's own website**, never Bosa's; the batch signed by the fork's own gettoneria (SECURITY.md 4.3); the list's fingerprint out for the rules file.
- [ ] **The website address for coins:** each fork keeps its own for as long as its coins exist (souvenirs last). Bosa's is to decide (for example a path under SUNDIAL's `bosa.photovoltaic.art`), kept by PVA (SECURITY.md M8).
- [ ] **The terms of ownership** and the keyholders' thresholds as a template (GROWTH.md 3; tokenomics.md 5).

### 6. Security first

A fork inherits every gap, so the release waits for them.

- [ ] Decisions D1–D5 made (SECURITY.md 5).
- [ ] Fixes 1–13 done (SECURITY.md 6), in particular the spend checks, the passport, the gateway protocol and key handling.
- [ ] The independent review repeated on the built firmware before release.

### 7. Reproducible build

- [ ] **One image for all nine nodes,** as SUNDIAL: every catalogue role in one firmware, **the node's role and identity written to its flash at installation**, not compiled in. One build to check, one image to sign, and a year-2 conversion is the same flash for every panel. Check the image fits the carrier's flash with every role in it; split by tier (panel only, battery) only if it doesn't.
- [ ] One build script, sharing SUNDIAL's pinned toolchain; pinned and vendored libraries (SECURITY.md M8).
- [ ] The image signed for Secure Boot; the signing keys held offline, by each fork for its own nodes.
- [ ] `firmware/VERSIONS.md` and a **tagged release** for each tested firmware (the first: Bosa's 2028 season).
- [ ] Cross-implementation test vectors (Python, JavaScript, ESP32) in the test bed (SECURITY.md M3).

### 8. Hardware any town can buy

- [ ] **A parts list per node role,** with each named part's function and at least one alternative: flip-dot panels (Alfa-Zeta or other, on RS-485), coin hopper (Slomatic X3 EXP or another ccTalk hopper), coin acceptor, arm (RoArm-M2-S or another bus-servo arm on UART), MPPT and LiFePO₄ battery, NFC readers.
- [ ] **Envelope dimensions only** for parts with proprietary drawings (the flip-dot panel): a fork asks the supplier for its own copy.
- [ ] Battery tier with the **terminal fuse and temperature-aware charging** (SECURITY.md M7).
- [ ] **Climate notes** generalised: heat (the Sardinian figures as the worked example), and cold (LiFePO₄ must not charge below 0 °C).
- [ ] **The budget script** reads the town's choices (which nodes, how many coins, currency) and produces the fork's own sheet; Bosa's as the example ([budget/](budget/)).

### 9. The guide and templates

- [ ] **`REPLICATE.md`** (Italian and English), SUNSET's half of the town guide, in the order a town works:
  1. A year of SUNDIAL first (SUNDIAL's REPLICATE.md)
  2. Choose each panel's year-2 role (GROWTH.md 1)
  3. **The law where you are:** shouts, the auction and the tokens, checked with a lawyer (a checklist of questions, not legal advice: SECURITY.md 4.9)
  4. Permissions: hosts, the comune or council, amplified sound, an unattended auction
  5. Fill in `site.json`; build
  6. Source and build the five interactive nodes; convert the four walls
  7. Key the nodes; make the coin batch; write the rules file
  8. The pilot: calibrate R and the ceiling; set the prices
  9. The first season
  10. Handing the nodes to their owners
- [ ] **`templates/`** (Italian and English): terms of node ownership; host consent for an interactive node; the one-screen rules; the auction's rules for sellers (contents visible, no cells, the seller's risk); notice of what can't be posted, and a contact for reports; privacy notice; the takedown procedure.

### 10. Checking it works

- [ ] **Automatic check** on every push: build every node role; run the test bed with nine simulated nodes for a simulated week; **Bosa leakage check** (Bosa's name, coordinates, keys, address or website outside `site/` fails); the **two-town isolation test** (4).
- [ ] **Fork rehearsal:** a test fork for a different town and latitude (one northern, one southern), built from `site.json` alone, with its own keys, coins and rules, run in the test bed beside Bosa with no crossover.

### 11. Field test

- [ ] **Bosa's first full SUNSET season (2028)** on the forkable structure, with sections 2–7 in place.
- [ ] Fixes from the season applied; the firmware tagged.

### 12. Release: licences and the rules (last)

Only when every item above is ticked, the season (11) is done, and the catalogue has been reviewed for further nodes (1a). Matching SUNDIAL's:

- [ ] `LICENSE`: **code** (firmware, tools, phone pages, explorer): **MIT**.
- [ ] `hardware/LICENSE`: **hardware** (node builds, cabinets, coin design files): **CERN-OHL-P v2**.
- [ ] `texts/LICENSE`: **texts and artwork**: **CC BY 4.0**.
- [ ] README section **"Licences and the two rules"**: what each licence covers; nine panels; never linked; the link request.
- [ ] `ACKNOWLEDGEMENT.md`: the requested link and a suggested line, e.g. *"Based on SUNSET, a work of PVA (Photovoltaic Art) — photovoltaic.art · github.com/photovoltaic-art/SUNSET"*.

**Note:** licences cannot enforce nine panels or forbid linking. The two rules are stated as the definition of a SUNSET; a bigger or linked network is free to exist, but is not a SUNSET.

- [ ] Tag **v1.0**: the version Bosa ran for its season.

### 13. Optional

- [ ] `CONTRIBUTING.md`: offering improvements back (security fixes first).
- [ ] The **list of towns** on photovoltaic.art, for forks that send their link: towns that can find each other without being networked (GROWTH.md 5.4).

---

## Order of work

| Step | Tasks | Why in this order |
| --- | --- | --- |
| 1 | The two rules, the isolation design and the catalogue's rules (summary, 1a, 4) | Decided before any code, so no code assumes one town or one set of nodes |
| 2 | `site.json` additions and generated config (2, 3) | Every part reads from it from the start |
| 3 | Security decisions and fixes (6) | A fork inherits them |
| 4 | Keys, coins, rules per town; build (5, 7) | Safe, repeatable nodes for any town |
| 5 | Hardware alternatives and budget (8) | Before another town orders parts |
| 6 | Guide and templates (9) | The town-facing part |
| 7 | Automatic checks and fork rehearsal (10) | Proof that the structure works |
| 8 | Bosa's 2028 season (11) | Proof that the system works |
| 8a | Further catalogue nodes built and tested (1a) | Forks choose from tested nodes only |
| 9 | **Release (12)** | Last: the licences are what make the repo forkable |

Steps 1 and 2 cost almost nothing now and save retrofitting later: they are rules for how SUNSET's firmware is written from its first line.
