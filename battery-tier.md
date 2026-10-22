# The battery tier — carrier v1 for SUNSET's interactive nodes

The PVA carrier board v1 ([CARRIER.md](https://github.com/photovoltaic-art/sundial/blob/main/hardware/CARRIER.md)) was designed for a SUNDIAL wall panel: no battery, awake from dawn to dusk. SUNSET's **interactive nodes** use **the same board, unchanged,** on a battery. This document specifies that tier; each interactive node's own document adds only what is different (pins, off-board loads, power).

> Status: draft 1, 22 Oct 2026, split out of interactive-auction.md when SUNSET moved to its own repository. Nothing here changes the carrier board.

---

## 1. Two power tiers, one board

**The rule: the power tier follows the load, not the role.** A node that only serves pages and keeps records is a wall node. A node that moves, flips, lights or releases something is an interactive node.

| | Wall node | Interactive node |
| --- | --- | --- |
| Examples | SUNDIAL panels; SUNSET message walls; a data-only auction | The street auction (lockers); the robot arm; the flip-dot wall |
| Panel connects to | Carrier J1 directly | Victron SmartSolar MPPT 75/15 → 12 V LiFePO₄ battery → MPPT load output → carrier J1 |
| JP1 (sun-sensor jumper) | **On** | **Off**, and the sun sensor compiled out of the firmware |
| Sun reading | The carrier's own short-circuit current: true light level | Victron PV voltage and power over VE.Direct: energy harvested |
| GPIO 34 divider reads | Panel voltage (dawn and dusk gates) | Battery voltage (a cross-check of the Victron's figure) |
| Battery data | None | Victron: battery voltage and current, charge state, yield today |
| Awake | Dawn to dusk, off at night | Business sunrise to sunset; some nodes use stored sun after sunset (lights, the SUNSET set), then sleep until sunrise (1.2) |
| Temperature probe, clock, Wi-Fi, storage | Same | Same |
| Firmware | Wall build | Interactive build |

### 1.1 Why JP1 must be off

Every 10 seconds the sun sensor's MOSFET (Q1) shorts `PV+` to ground through the 5 mΩ shunt, before the fuse. A panel is a current source and gives at most about 6 A into that short, which is the whole point of the sensor. **A battery is not a current source:** the same pulse would be a dead short of a 12 V LiFePO₄ pack.

- **JP1 is a physical jumper** (a 2-pin header between GPIO 25 and the gate driver U3). With the jumper removed, Q1 cannot be switched on, whatever the firmware does.
- **The interactive build also compiles the sun sensor out** (`SUN_SENSOR 0`), so GPIO 25 is never driven high, even if someone refits the jumper.
- The Victron's own load-output protection is a third line, not a substitute for the first two.

The carrier cannot keep its own sun measurement on this tier: the panel now feeds the Victron, and shorting the Victron's input every 10 seconds would discharge its input capacitors through Q1 and upset its tracking.

### 1.2 Sunset is the moment

SUNDIAL seals each day's dial at Bosa's sunset. SUNSET keeps the same moment: **the day's business closes at sunset.** The auction's hammer falls, the day's records seal, and the whole network keeps one rhythm.

- **Sunset comes from the clock,** computed for Bosa as SUNDIAL's seal already is (`sunTimes`), not from the panel or battery voltage. A cloudy afternoon must not end the auction early.
- **All business is in daylight.** Earning, spending, listing, bidding, minting, collecting and returning happen between sunrise and sunset, and nowhere else. At sunset the Wi-Fi closes.
- **Stored sun after sunset is for showing, not trading.** Some nodes use the battery in the evening: the auction's lockers stay lit for a few hours (interactive-auction.md 1), and the SUNSET set plays on days the sun has earned it (interactive-audio.md). Nothing can be bought or sold until sunrise.
- **Then the node sleeps** until sunrise.
- The battery smooths cloudy days and motor or solenoid surges, and lights the evening. It does not move the close of the day.

**The sun is the coin slot.** Actions that cost energy (a grab, a flip, a door) are offered only when the battery's charge state allows. A dull week means fewer actions, and the page says so.

### 1.3 What the Victron data means

The VE.Direct text protocol sends a block of values about once a second (19200 baud): battery voltage and current, PV voltage and power, charge state, yield today, load-output state.

- **PV power is energy harvested, not light.** When the battery is full the Victron backs off the panel, so on full-battery days an interactive node's dial understates the sun. Interactive-node dials are labelled accordingly. Only wall nodes measure the sun.
- **Check the 75/15's VE.Direct signal level before wiring.** If its TX is 5 V, put a resistor divider on the ESP32's RX pin.

---

## 2. Carrier v1 on the battery tier

### 2.1 Wiring

```
 PV panel ──► Victron MPPT 75/15 (PV in)        battery ◄──► MPPT (battery terminals)
                     │
                     ├── LOAD out (low-voltage disconnect) ──► fuse ──► carrier J1 (PANEL +/−)
                     │                                           └──► fuse ──► 12 V line to the node's off-board loads
                     └── VE.Direct ──► carrier J10 (GPIO 16 RX, 17 TX, GND)
```

- **Panel to MPPT:** a recycled panel's open-circuit voltage (44.5 V on the TSM-185DC01 label, about 48 V on a cold morning) is well inside the 75 V limit.
- **Carrier power:** J1 takes the MPPT load output. The buck converter turns about 13 V into the usual 5 V rail. The low-voltage disconnect protects the battery.
- **Supercapacitors:** harmless with a battery; fit them or leave them out.
- **Heavy loads stay off the carrier.** Solenoids and lights run from their own fused 12 V line through a small off-board driver, specified per node. The carrier's take-offs (F2 0.5 A at 5 V, F3 0.2 A at 3.3 V) are for small sensors, not locks.
- **AUX (J12)** is not used on this tier: the battery and load output replace it.
