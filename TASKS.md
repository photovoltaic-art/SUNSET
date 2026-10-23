# SUNSET — tasks

Tasks for SUNSET (PVA no. 2). Tasks for the PVA organisation and manifesto live in the [PVA repository](https://github.com/photovoltaic-art/PVA/blob/main/TASKS.md); the carrier board's in [SUNDIAL](https://github.com/photovoltaic-art/SUNDIAL/blob/main/FORK-TASKS.md).

> Updated 22 Oct 2026. Nothing is built.

## Tests, in order

Carried over from GO TO BED (gtb/GO-TO-BED.md, "Tests, in order"), extended for SUNSET.

- [x] **Test bed** (simulated): format v0, sizes, receipts, six attacks ([gtb/testbed](gtb/testbed/README.md)).
- [ ] **Carry test:** one ESP32 playing two walls; iPhone and Android, Wi-Fi pop-up and full browser ([steps](gtb/carry_test/TEST.md)). Add the v1 checks: the Ed25519 library runs in each browser path, and stamp keys survive a day (stamp-format.md 8). **The first thing to do; one ESP32 and two phones.**
- [ ] **Extend the test bed to v1:** holder keys, `issued`/`spent` in headers, the new size limits and storage budget, and a cloned-phone double spend that is caught and proved (stamp-format.md 5, 7).
- [ ] **Two boards on the bench:** wall firmware, a few phones, a day of light from a bench supply.
- [ ] **Pilot:** two walls and the gateway pair (print node, flip-dot wall). Enough to test walking, minting, paper, spending and the live spent list.
- [ ] Then the full nine.

## Format

- [ ] Choose the phone-side Ed25519 and SHA-256 library; measure its size on the node and its speed on an old phone (stamp-format.md 3.1).
- [ ] Publish the node public keys in `keys/` once nodes are keyed (stamp-format.md 2).
- [ ] Decide: stamps at season's end; passport backup; how double spends are shown (stamp-format.md 9).

## Hardware to source

- [ ] **Arm:** Waveshare RoArm-M2-S (interactive-arm-game.md 2.1). Check the servos' and UART's voltage limits before wiring.
- [ ] **Flip-dot panel:** Alfa-Zeta quoted 23 Oct 2026: 14 × 28 €440, 7 × 28 €220, controller included, shipping €25, 1–4 weeks (interactive-flipdot.md 3). Protocol and manual received; follow-up sent 23 Oct (start-up behaviour, partial updates, outdoor housing, drawings, spare dots, the 1 × 11 row for BINARY). Choose size (14 × 28) and colour.
- [ ] **Battery tier, per interactive node:** Victron SmartSolar MPPT 75/15, 12 V LiFePO₄, fuses, enclosure (battery-tier.md).
- [ ] **Print node:** a die-cut label printer with cutter that runs on 12 V (interactive-print.md 4.1).
- [ ] **The SUNSET set:** a Bluetooth speaker for the speaker locker (interactive-audio.md).

## Design still open

- [ ] Garden node (garden-node.md): planting, cladding, and whether refilling the tank earns a stamp (*proof of water*).

- [ ] Artwork for the paper stamp and the redeem sticker (interactive-print.md 5).
- [ ] The nine 5 × 5 node logos: unique, never the PVA logo.
- [ ] The one-screen rules and the first five minutes (SUNSET.md 5).
- [ ] Shout price, souvenir price, printing fee, listing fee: set in the pilot.

## Site and permissions

- [ ] Site plan for a first town, against SUNSET.md 4: gateway pair together near footfall; walls spread; auction within ESP-NOW range of the gateway if possible (stamp-format.md 5.2).
- [ ] Hosts and permissions: comune, wall owners, amplified sound, an unattended street auction (SUNSET.md 10).

## Repository

- [x] Repository public (22 Oct 2026), "not yet licensed for reuse" (as SUNDIAL).
- [ ] Licence, at release: match SUNDIAL.
