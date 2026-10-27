# SUNSET — the node catalogue

The nodes a SUNSET can be built from. **PVA builds and tests every node in this catalogue; a fork chooses which to use in its own nine.** Bosa's nine are the reference set.

> Status: draft 1, 27 Oct 2026. Nothing is built, so every node is at *specified* or earlier. A node enters the release catalogue only when it is **field-tested**. The catalogue is reviewed, and new nodes considered, before SUNSET is licensed ([FORK-TASKS.md](FORK-TASKS.md) 12).

---

## 1. What every node must be

A node belongs in the catalogue only if it keeps SUNSET's design. Every node:

1. **Runs on its own panel and its own sun,** on the PVA carrier board v1, unchanged; a battery only on the battery tier, storing its own sun ([battery-tier.md](battery-tier.md); the manifesto's principle 3).
2. **Seals one block a day at sunset,** in the shared format ([stamp-format.md](stamp-format.md)). **The seal is the same on every node;** no node changes it.
3. **Creates no stamps except from walk or the sun.** Every node pays walk stamps for first deliveries; only a node measuring sunlight with a reference sensor may pay from the sun's allowance. Everything else moves, converts or burns stamps (tokenomics.md 2).
4. **Is offline:** no internet, and no link to another town.
5. **Closes its business at sunset.**
6. **Passes the security checklist** ([SECURITY.md](SECURITY.md)): spend checks, admin access, key handling, its own surfaces reviewed.
7. **Keeps no one:** no names, no phone identifiers, times to the hour (the manifesto's principle 5).
8. **Has a build a fork can repeat:** parts list with alternatives, firmware role in the reproducible build, a test procedure.

## 2. The catalogue

Status: **specified** (a document), **bench-tested** (built and run on the bench), **piloted** (run in Bosa with real visitors), **field-tested** (a full season).

| Node | Kind | Tier | Does | Needs | Status | Specification |
| --- | --- | --- | --- | --- | --- | --- |
| **Wall** | Wall | Panel only | Messages, shouts, couriers, proof of walk | — | Specified | [wall-node.md](wall-node.md) |
| **Garden** | Wall, on a post | Panel only | A wall node watering its own bed from a closed tank | — | Specified | [garden-node.md](garden-node.md) |
| **Gettoneria** | Interactive | Battery | Mint and redeem tokens; souvenirs | — | Specified | [interactive-token.md](interactive-token.md) |
| **Flip-dot wall** | Interactive | Battery | A 28 × 28 picture flipped with tokens | Gettoneria, within ESP-NOW range (the gateway pair) | Specified | [interactive-flipdot.md](interactive-flipdot.md) |
| **Street auction** | Interactive | Battery | One lot a day, hammer at sunset | — (better within range of the gettoneria) | Specified | [interactive-auction.md](interactive-auction.md) |
| **Arm game** | Interactive | Battery | Proof of skill, paid from the sun's allowance | Reference sun sensor | Specified | [interactive-arm-game.md](interactive-arm-game.md) |
| **The SUNSET set** | Interactive | Battery | Music at sunset on a full battery | — | Specified | [interactive-audio.md](interactive-audio.md) |

**Bosa's reference nine:** walls 1–4 (any of them may be a garden node), gettoneria, flip-dot wall, street auction, arm game, the SUNSET set.

## 3. Candidates

Considered for the catalogue before SUNSET is licensed. Each must meet section 1, then be specified, built and tested like the others.

| Candidate | Idea | Against section 1 |
| --- | --- | --- |
| **Swap node** | Objects left and taken; the exchange agreed in whispers; stamps as the deposit | Fits; overlaps with the auction's lockers |
| **Gallery node** | A wall that shows images, SUNDIAL-style, beside the chat | Fits; a wall build variant |
| **Second flip-dot wall,** or a reclaimed bus-sign panel | More pixels, or a recycled display | Fits; needs the gateway pair's protocol for two walls (SECURITY.md 4.2) |
| **Distributed sound** | Phones playing layers of the set | Fits; an extension of the set, not a node |
| **Miner node** | A Bitaxe on spare midday power (SolarSats) | **Fails rule 4:** it needs a pool over the internet. Out unless a way is found to run it offline |
| ~~Radio node~~ | A LoRa link to the next village | **Set aside: fails rule 4,** and towns are never linked (GROWTH.md 5) |

## 4. Choosing nine (for a fork)

- **Nine panels,** never linked: SUNSET's two rules ([FORK-TASKS.md](FORK-TASKS.md)).
- **Any mix of catalogue nodes,** respecting each node's *Needs*: no flip-dot wall without a gettoneria beside it; a fork **with coins** builds the gettoneria.
- **The economy follows the choice,** and is written in the fork's rules file: without an arm game there is no sun's allowance, so walk stamps are the only source; the prices and sinks are set in the fork's pilot (tokenomics.md).
- **No minimum of walls:** any nine catalogue nodes will do (decided 27 Oct 2026). **Nine is the number that matters:** an edition of nine, tested and proven in Bosa before any town copies it, never more, never less. Every node seals and pays walk stamps, so the walk economy works with any mix.
