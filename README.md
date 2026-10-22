# SUNSET

> **Work in progress.** Concept and specifications only; nothing is built yet. Not yet licensed for reuse.

Nine end-of-life solar panels on the walls of a town, forming a small offline network with its own currency. Every day's business closes at sunset.

SUNSET is the second work of **PVA (Photovoltaic Art)**, a manifesto for new uses of end-of-life PV panels: [photovoltaic.art](https://photovoltaic.art). The first is [SUNDIAL](https://github.com/photovoltaic-art/sundial). **A PVA work is nine panels;** that is its one rule. (SUNSET's working title was GO TO BED.)

People earn **stamps** by walking messages between walls and by skill, and spend them at an auction, a mint and a wall of mechanical pixels. Paper stamps pass from hand to hand, so anyone can take part, with or without a phone. Every panel runs on its own sun; everything is unattended, anonymous and over by sunset.

Start with **[SUNSET.md](SUNSET.md)**: the nine panels, the stamp economy, a day of SUNSET, the layout, the pages and the operations.

## The nine panels

| Panel | What it does | Specification |
| --- | --- | --- |
| Walls 1–4 | Message walls: read, write, shout; couriers carry messages between walls and earn stamps (*proof of walk*) | [wall-node.md](wall-node.md) |
| Print node | **The gateway.** Turns digital stamps into paper stamps and back; sells the artwork stamp as a souvenir | [interactive-print.md](interactive-print.md) |
| Flip-dot wall | Also the gateway. Mechanical pixels flipped only with paper stamps; a sticker wall for the spent ones | [interactive-flipdot.md](interactive-flipdot.md) |
| Street auction | One lot a day in three lit lockers; the hammer falls at sunset | [interactive-auction.md](interactive-auction.md) |
| Arm game | A robot arm behind perspex; drop a peg in a hole, earn a stamp (*proof of skill*) | [interactive-arm-game.md](interactive-arm-game.md) |
| The SUNSET set | Music at sunset to a registered Bluetooth speaker, only on days the sun has filled its battery | [interactive-audio.md](interactive-audio.md) |

## Repository

```
README.md                    this file
SUNSET.md                    the whole work: nine panels, economy, the day, layout, pages, operations
wall-node.md                 the four message walls: visitor experience, messages, couriers, proof of walk, stamp format (outline)
battery-tier.md              carrier v1 on a battery: the tier every interactive node uses
interactive-auction.md       the street auction
interactive-arm-game.md      the arm game
interactive-print.md         the print node (proof of print)
interactive-flipdot.md       the flip-dot wall (cash only)
interactive-audio.md         the SUNSET set
```

## Hardware

Every panel uses the **PVA carrier board v1**, unchanged, specified and drawn in the SUNDIAL repository: [hardware/CARRIER.md](https://github.com/photovoltaic-art/sundial/blob/main/hardware/CARRIER.md) and [hardware/carrier/](https://github.com/photovoltaic-art/sundial/tree/main/hardware/carrier). Wall nodes use it exactly as a SUNDIAL panel does; interactive nodes use it on the battery tier ([battery-tier.md](battery-tier.md)).

## Status

Drafts, 22 October 2026. Still to be written: the full **stamp format** (outlined in wall-node.md 5), the firmware, the site plan for a first town, and permissions. The history of these documents up to the move is kept here; they were first written in the SUNDIAL repository.
