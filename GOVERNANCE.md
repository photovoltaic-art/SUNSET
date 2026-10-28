# SUNSET — Governance: the owners' agreement

**First draft, 28 October 2026.** The private agreement between the owners of SUNSET's nine nodes, intended to become part of each node's future sales contract. Not yet reviewed by a lawyer or notary; nothing here is legal advice. Italian law is assumed and must be checked locally before anyone signs.

SUNSET is year 2 of PVA's growth model: SUNDIAL's nine panels become SUNSET's nodes for a trial season run by PVA (2028), and **at the summer solstice of 2029 the nine nodes are sold at auction,** each to its own owner ([GROWTH.md](https://github.com/photovoltaic-art/PVA/blob/main/GROWTH.md) 3.0). This document says how those owners run the work together. The technical design behind it is in [tokenomics.md](tokenomics.md) 3 and 5.

---

## In short

- **Owners vote with their feet.** A vote is cast by walking to your own node and signing there. There is no other way to vote.
- **The artwork is the voting booth.** The node signs with its own key, which never leaves it.
- **The vote is public.** Every signature goes into the node's sealed block at sunset, is carried through the town by couriers, and is shown on the explorer.
- **Proposals are discussed in public; owners decide.** Anyone may propose and speak. Only owners sign.
- **Five of nine, enforced by the work itself.** The firmware refuses to install rules that do not carry five owners' signatures. This is a hard rule in the code, not a promise.
- **The manifesto is the constitution.** No vote can change what makes SUNSET a PVA work.
- **PVA is the enabling layer, with no say after handover.** PVA writes the firmware, publishes it and runs the website. It does not vote, has no veto, and holds no power over the owners.

---

## Part A. The agreement

### 1. The parties

1.1 **The owners:** the nine holders of SUNSET's nodes in one town, each named in the schedule at the end of this agreement (Part C).

1.2 **PVA (Photovoltaic Art):** the project that designed SUNSET, writes its firmware and rules, and runs its website. PVA is a party to this agreement only for the obligations in section 10.

1.3 **The host** of each node (the owner of the wall or ground it stands on) is not a party. The host's consent is a separate agreement between the host and the node's owner (section 9).

### 2. Definitions

| Term | Meaning |
| --- | --- |
| **Node** | One of SUNSET's nine panels, with its carrier board, enclosure, gnomon, and, for an interactive node, its battery tier and its own hardware |
| **The work** | SUNSET as installed in this town: the nine nodes together, their network, their stamps and tokens |
| **Node key** | The signing key generated on the node at handover. Its private half never leaves the node; its public half is published |
| **Rules** | The season's rules file (for example `rules-S2`): every price, rate and validity period, identified by its fingerprint |
| **Coin list** | The year's batch of token IDs, identified by its fingerprint |
| **Proposal** | A published rules file, coin list, or other change listed in section 5, with its fingerprint |
| **Signature** | A node key's signature on a proposal's fingerprint, made at the node by its owner |
| **The chain** | The nodes' signed daily blocks, sealed at sunset and carried between nodes by couriers |
| **The manifesto** | PVA's manifesto ([MANIFESTO.md](https://github.com/photovoltaic-art/PVA/blob/main/MANIFESTO.md)) as it stands on the date this agreement is signed |

### 3. What an owner holds

3.0 **Buying a node.** Nodes are first sold at auction at the summer solstice of 2029, one lot per node. Agreeing to this agreement is a condition of bidding, and a bidder may win only one lot (3.3). **Each lot comes with its provenance and condition report:** the node's public record from its installation as a SUNDIAL panel to the day of the sale (days awake, blocks sealed, stamps issued and spent, service notices and repairs), drawn from its signed daily blocks and checkable by anyone on the explorer. PVA aims to offer all nine nodes, repairing or rebuilding any that failed in the trial season.

3.1 **The node:** its hardware, and the right to keep it in place under the host's consent.

3.2 **The node key,** and with it **one vote**, cast only at the node (section 6).

3.3 **One owner, one node.** No person, business or group may hold more than one node key. Two nodes held by related parties (the same family, the same business under two names) count as one holder for this rule.

3.4 An owner does **not** hold any share of the stamps or tokens in circulation, any income from the work, or any right over another owner's node. Owning a node earns no money; ownership is its own reward.

### 4. The manifesto is the constitution

4.1 The work always keeps to PVA's principles. In particular, no vote may:

- connect any node to the grid, or power a node from anything but its own sun;
- connect any node to the internet, or add accounts or tracking;
- record who a visitor is;
- make stamps or tokens redeemable for money, or sell them;
- change the number of nodes from nine;
- remove a node's sundial.

4.2 **A change outside the manifesto is not a SUNSET change.** If owners build such a change themselves, they are free to do so, but the result is no longer a PVA work and may not use the names PVA, SUNDIAL or SUNSET.

### 5. What the owners decide

| Decision | Threshold |
| --- | --- |
| The season's rules: prices, stamp validity, the arm's rate R | **5 of 9** |
| The year's coin list | **5 of 9** |
| Admitting a new owner's key, when an owner leaves or a key is lost (section 8) | **5 of 9** |
| Retiring a node that can no longer run, and choosing a tested catalogue node to replace it ([NODES.md](NODES.md)) | **5 of 9** |
| Changes to this agreement (section 12) | **5 of 9**, within the limits of section 4 |

5.1 **Not decided by vote:** a firmware release that fixes a fault and leaves the rules' fingerprint unchanged. PVA publishes it with a reproducible build; each owner decides whether to install it on their own node.

5.2 **If no proposal reaches five signatures, nothing changes.** The current rules continue for another season. Inaction never stops the work.

### 6. How a vote is cast

6.1 **On foot, at the node.** The owner walks to their own node in daylight, opens its owner page on the node's own Wi-Fi, and signs the proposal. The node signs with its key. There is no remote vote, no proxy and no other channel.

6.2 **In public.** The signature is written into the node's sealed block at that day's sunset, carried to the other nodes by couriers, and shown on the website's explorer. Anyone can see which node signed which proposal, and when.

6.3 **Yes, or nothing.** A node can sign a proposal or not. Not signing within the voting period is an abstention. An owner may publish their reasons for voting either way; the chain records only the signatures.

6.4 **The count.** A proposal passes when signatures from five different node keys for the same fingerprint are in the chain within its voting period. Anyone can check the count with the explorer's published script.

### 7. The yearly cycle

| When | What | Who |
| --- | --- | --- |
| Autumn and winter | Proposals are gathered | Anyone: owners, hosts, visitors, PVA |
| By 1 February | PVA publishes the draft rules and coin list for the next season, each with its fingerprint and a reproducible build | PVA |
| March | **A public meeting** in the town: every proposal to be signed is presented and discussed in the open | Open to all; owners present |
| Four weeks, March to April | **The voting period:** owners sign at their nodes | Owners |
| The spring visit | If a proposal has five signatures in the chain, it is installed on all nine nodes | Each owner, or whoever they ask to do it |

7.1 **A proposal not presented at the public meeting cannot be signed** that season.

7.2 **The firmware enforces the result.** A node refuses to install rules or a coin list that do not carry five valid owner signatures. This check is a hard rule in the firmware and cannot be switched off by any setting or key.

### 8. Losing a vote, leaving, and handing on

8.1 **The result binds every owner.** An owner who did not sign agrees, by signing this agreement, to install a proposal that has passed. Their dissent stays on the public record.

8.2 **An owner who cannot accept a result may leave** by handing their node on (8.3). A node left running the old rules no longer agrees with the other nodes: its blocks and stamps are refused, and it drops out of the network. This is visible in the chain and is the cost of refusing.

8.3 **Handing a node on.** An owner may sell or give their node to anyone who meets section 3.3. At the handover a new key is generated on the node in the new owner's presence, the old key is retired and published with its end date, and **five of the other eight owners sign the new key** (section 5).

8.4 **A lost or broken key.** A node whose key is lost or whose board has failed cannot sign and counts as abstaining. A replacement key is admitted by five of the other eight owners.

8.5 **Unclaimed nodes.** Until a node has its first owner (a lot that does not sell at the auction is offered again at the next solstice), PVA keeps it running. **A node held by PVA always abstains:** its key never signs a proposal. The threshold therefore always means five owners.

### 9. The host

9.1 Each owner is responsible for the agreement with their node's host: consent to the node's presence and access for its care.

9.2 Hosting a node gives no vote. An owner and a host may be the same person.

9.3 If a host withdraws consent, the owner moves the node to another site that fits the layout ([SUNSET.md](SUNSET.md) 4), with five of the other eight owners' agreement to the new site.

### 10. PVA: the enabling layer

10.1 **PVA has no say after handover.** It holds no node key, no vote and no veto, and it has no power to change the rules, the coin list or this agreement.

10.2 **What PVA provides:**
- the firmware and rules files, published with reproducible builds and fingerprints;
- the draft rules and coin list each year (section 7), written from the proposals received;
- the website: the map, the explorer, the Verify page and the archive;
- the year's coin batch, made to the coin list the owners have signed.

10.3 **What PVA will not do:** write firmware that breaks the manifesto (section 4). Owners remain free to write their own, outside the PVA name (4.2).

10.4 PVA may propose and speak at the public meeting like anyone else.

### 11. Care, insurance and liability

11.1 Each owner is responsible for their node: its care, its repair, and public liability insurance for it.

11.2 *Open:* whether the nine owners take one shared policy or nine separate ones; who does the fortnightly rounds (the owners, PVA as a paid service, or both); how shared costs (the coin batch, the website) are met.

### 12. Changing this agreement

12.1 This agreement may be changed by five of nine owners' signatures on the new text's fingerprint, through the same yearly cycle (section 7), and never so as to break section 4.

### 13. Duration and law

13.1 This agreement lasts as long as the work runs in this town.

13.2 *To check:* the governing law (Italian law assumed), whether the owners form an unincorporated association (*associazione non riconosciuta*) or keep a private agreement among themselves (*scrittura privata*), and how this agreement attaches to each node's sales contract.

---

## Part B. What the firmware enforces

These are the rules above that the work itself enforces, for the firmware specification.

| Rule | How |
| --- | --- |
| Votes only at the node (6.1) | An **owner page** on the node's own Wi-Fi, opened with the owner's credential, offers the open proposals; signing uses the node key, which never leaves the node |
| Votes public (6.2) | A **signatures field** in the sealed block: proposal fingerprint, node key, date |
| Five of nine (6.4, 7.2) | Before installing rules or a coin list, the firmware checks for **five valid signatures from distinct current node keys** on its fingerprint; otherwise it refuses. No setting disables the check |
| Rules in force are visible (8.2) | The rules' fingerprint is in every sealed block (tokenomics.md 3); nodes refuse blocks and stamps made under other rules |
| PVA-held nodes abstain (8.5) | A node flagged as unclaimed at installation cannot sign; the flag clears only when a new owner's key is generated |
| Keys replaced in public (8.3, 8.4) | A new key is accepted by the network only with five signatures from the other nodes; the retired key is published with its end date |

**Open technical questions:**
- The owner's credential at the owner page (a passphrase set at handover, or a physical token), and how it is reset if lost.
- How the voting period is fixed in the firmware (dates in the draft rules, or a period counted from the public meeting).
- Signing the agreement text itself (section 12) with the same mechanism.

---

## Part C. Schedule of owners

| Node | Owner | Host | Key fingerprint | Handover date |
| --- | --- | --- | --- | --- |
| Wall 1 | | | | |
| Wall 2 | | | | |
| Wall 3 | | | | |
| Wall 4 | | | | |
| Gettoneria | | | | |
| Flip-dot wall | | | | |
| Street auction | | | | |
| Arm game | | | | |
| The SUNSET set | | | | |

---

## Open questions

| Question | Notes |
| --- | --- |
| The auction | Set by the 2029 solstice auction (3.0); still open: who runs it, reserves, currency (euros or bitcoin), VAT and the artist's resale right on later resales |
| The first vote | The 2029 rules, written by PVA, run until spring 2030; the owners' first vote is on the 2030 rules |
| Insurance and rounds | Section 11.2 |
| Legal form | Section 13.2; a local lawyer or notary to review before the first sale |
| Italian text | The agreement is signed in Italian; this English draft is the working copy |
| The owner's credential | Part B |
