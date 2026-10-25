# SUNSET

> **Work in progress.** Concept and specifications only; nothing is built yet. Not yet licensed for reuse.

Nine end-of-life solar panels on the walls of a town, forming a small offline network with its own currency. Every day's business closes at sunset.

SUNSET is the second work of **PVA (Photovoltaic Art)**, a manifesto for new uses of end-of-life PV panels: [photovoltaic.art](https://photovoltaic.art). The first is [SUNDIAL](https://github.com/photovoltaic-art/sundial). **A PVA work is nine panels;** that is its one rule. SUNSET grew from GO TO BED, a group chat that goes to bed at sunset ([gtb/](gtb/GO-TO-BED.md)).

People earn **stamps** by walking messages between walls and by skill, and spend them at an auction, a mint and a wall of mechanical pixels. Tokens (printed coins with an NFC tag) pass from hand to hand, so anyone can take part, with or without a phone. Every panel runs on its own sun; everything is unattended, anonymous and over by sunset.

Start with **[SUNSET.md](SUNSET.md)**: the nine panels, the stamp economy, a day of SUNSET, the layout, the pages and the operations.

## The nine panels

| Panel | What it does | Specification |
| --- | --- | --- |
| Walls 1–4 | Message walls: read, write, shout; couriers carry messages between walls and earn stamps (*proof of walk*) | [wall-node.md](wall-node.md) |
| (any wall) | A wall node on a post where there is no wall, watering its own flower bed from a closed tank | [garden-node.md](garden-node.md) |
| Gettoneria (token node) | **The gateway.** Turns digital stamps into tokens and back, from a coin hopper; sells a token as a souvenir | [interactive-token.md](interactive-token.md) |
| Flip-dot wall | Also the gateway. A 28 × 28 square of yellow mechanical pixels flipped only with tokens; a column of the spent ones | [interactive-flipdot.md](interactive-flipdot.md) |
| Street auction | One lot a day in three lit lockers; the hammer falls at sunset | [interactive-auction.md](interactive-auction.md) |
| Arm game | A robot arm behind perspex; drop a peg in a hole, earn a stamp (*proof of skill*) | [interactive-arm-game.md](interactive-arm-game.md) |
| The SUNSET set | Music at sunset to a registered Bluetooth speaker, only on days the sun has filled its battery | [interactive-audio.md](interactive-audio.md) |

## Repository

```
README.md                    this file
SUNSET.md                    the whole work: nine panels, economy, the day, layout, pages, operations
TASKS.md                     what to do next: tests, sourcing, design, site
stamp-format.md              stamps and blocks shared by every node (v1, built on GO TO BED's v0)
wall-node.md                 the four message walls: visitor experience, messages, couriers, proof of walk
garden-node.md               a wall node on a post, for a place with no wall: IBC tank, flower bed, sun-only watering
battery-tier.md              carrier v1 on a battery: the tier every interactive node uses
interactive-auction.md       the street auction
interactive-arm-game.md      the arm game
interactive-token.md         la gettoneria, the token node (proof of mint)
interactive-flipdot.md       the flip-dot wall (cash only)
interactive-audio.md         the SUNSET set
budget/                      SUNSET-budget.xlsx: the cost of the nine panels (draft), and the script that builds it
gtb/                         GO TO BED, the concept SUNSET grew from (moved from the PVA repo with its history)
  GO-TO-BED.md               the concept note and its decisions (21 Oct 2026)
  FORMAT.md                  block and receipt format v0
  carry_test/                ESP32 sketch and steps: do phones carry blocks between panels?
  testbed/                   simulated town producing real signed blocks and receipts; results
```

## Hardware

Every panel uses the **PVA carrier board v1**, unchanged, specified and drawn in the SUNDIAL repository: [hardware/CARRIER.md](https://github.com/photovoltaic-art/sundial/blob/main/hardware/CARRIER.md) and [hardware/carrier/](https://github.com/photovoltaic-art/sundial/tree/main/hardware/carrier). Wall nodes use it exactly as a SUNDIAL panel does; interactive nodes use it on the battery tier ([battery-tier.md](battery-tier.md)).

## Status

Drafts, October 2026. Planned for the second year, after SUNDIAL's first season. Still to come: the firmware, the site plan for a first town, and permissions ([TASKS.md](TASKS.md)). The history of these documents is kept here: SUNSET's were first written in the SUNDIAL repository, GO TO BED's in the PVA repository.
