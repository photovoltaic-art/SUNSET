# The SUNSET I/O board — one driver board for every interactive node

A small second board that sits **beside** the PVA carrier v1 and does everything the carrier is not built for: switching locks, motors and pumps, powering modules, and protecting the lines that leave the box. **One design for every interactive node:** each node fits only the parts it uses.

> Status: draft 1, 28 Oct 2026. Specification only; nothing drawn or built. Replaces the per-node "off-board driver" (interactive-auction.md 2.3). **Nothing here changes the carrier board.** Part classes are given, as in the carrier's first spec; part numbers come with the schematic.

---

## 1. Why one board

Every interactive node needs the same handful of parts around the carrier ([NODES.md](NODES.md), checked 28 Oct 2026):

| Node | Needs |
| --- | --- |
| Street auction | 3 lock switches (solenoids); 12 V → 5 V for the LED strips; 3.3 → 5 V level shift for the LED data; pull-up on GPIO 36 |
| Gettoneria | Hopper power switch; flap solenoid switch; ccTalk interface (hopper); I²C multiplexer for 3 NFC readers; pull-up on GPIO 36 |
| Flip-dot wall | 24 V converter switch; RS-485 transmitter; I²C port expander (acceptor inhibit, flap); NFC reader; pull-up on GPIO 36 |
| Arm game | Arm 12 V power switch (up to 5 A); reference sun sensor (INA219 module); pull-up on GPIO 36; optional port expander |
| SUNSET set, with speaker locker | Lock switch; speaker charger (12 V → 5 V USB) switch |
| Garden node | Pump switch; pull-up on GPIO 36 |
| **All battery-tier nodes** | VE.Direct input with a divider in case the Victron sends 5 V |

Designing these as one board, populated per node, keeps PVA's rule: **one board everywhere** (GROWTH.md 6). A fork builds one I/O board design and fits it differently for each node.

Wall nodes, and the SUNSET set without its locker, don't use the I/O board.

## 2. How it connects to the carrier

**By three short cables from the carrier's existing headers.** No change to the carrier.

| Carrier header | Pins | Cable to the I/O board's |
| --- | --- | --- |
| **J9** spare GPIO | 3V3, GND, 32, 33, 36, 26, 27, 13, 14 | J9-mirror (1 × 9) |
| **J10** UART | 3V3, GND, 16 (RX), 17 (TX) | J10-mirror (1 × 4) |
| **J13** I²C | 3V3, GND, SDA, SCL | J13-mirror (1 × 4) |

- **Locking, keyed 2.54 mm housings** (Molex KK 254 class) on both ends, never loose jumper wires: the cables can't go on backwards or shake loose in the box. Secure them with a cable tie.
- **Beside, not on top:** switching current, heat and noise stay away from the carrier's sun-sense signals and the ESP32 antenna; the I/O board can be any size, with big terminals.
- **The carrier's headers are grouped on one edge** (requested for the carrier layout, 28 Oct 2026), so the three cables leave the carrier together.
- Most of these nodes **remove R19** on the carrier, freeing GPIO 27 (the carrier's switched 5 V output is then unused).

## 3. Three rules

1. **Its own power.** The I/O board takes **12 V** directly: the battery tier's fused load line, or, on a garden node, the 12 V converter fed from the carrier's AUX output. It makes its own 5 V and 3.3 V. **The carrier's 3V3 pin (fused at 0.2 A) is used only as the logic reference** and to power pull-ups; modules such as NFC readers run from the I/O board's own 3.3 V.
2. **Heavy current never returns through the carrier.** Solenoid, motor, pump and LED currents return to the battery's negative through the I/O board's own power ground. The cables' GND wires carry signal reference only. The I/O board joins its power ground to the signal ground at one point, near its power input.
3. **Every line back to the ESP32 is protected on the I/O board.** Inputs from switches, sensors and long cables get a series resistor and clamps to 3.3 V and GND, so a fault or a static discharge outdoors can't reach a GPIO pin.

## 4. What is on the board

### 4.1 Power in

| Block | Specification |
| --- | --- |
| VIN | 12 V nominal, 9–16 V (LiFePO₄ charging reaches 14.6 V); screw terminal for 4 mm² wire |
| Protection | Input blade fuse (ATO), sized per node; reverse-polarity protection; TVS across VIN |
| 5 V | Buck converter, 12 V → 5 V, **3 A** (LED strips, speaker charging, modules) |
| 3.3 V | Regulator from 5 V, **1 A** (NFC readers, expanders, transceiver) |
| Indicators | One LED each for VIN, 5 V, 3.3 V (dim) |

### 4.2 Switched outputs

| Channels | Kind | Rating | For |
| --- | --- | --- | --- |
| **LS1–LS3** | Low-side N-MOSFET (logic-level), flyback diode, 100 kΩ gate pull-down, gate resistor | 3 A continuous, 12 V | Dumb loads: lock solenoids, the flap, the pump |
| **HS1–HS2** | High-side switch (P-MOSFET with a small driver, or an integrated high-side switch), own fuse each | **6 A** continuous, 12 V | **Devices with a data connection:** the arm, the hopper, the 24 V converter, the speaker charger |

**Why two kinds:** a device that also has a data line to the carrier (UART, ccTalk, RS-485) must keep its ground. Switching its ground (low side) would let it power itself backwards through the data line. So those are switched on the 12 V side.

**Every channel is off at boot and on any reset:** gate pull-downs, and the firmware drives the channel only in business hours (battery-tier.md 1.2).

### 4.3 Inputs

**6 protected inputs** for reed switches, float switches, coin-acceptor pulses, knobs and the button: series resistor, clamps, a 10 kΩ pull-up to the carrier's 3.3 V (fitted per input), and an optional 100 nF filter for switches. **GPIO 36 always gets its pull-up,** because it has no internal one.

### 4.4 Interfaces (fit what the node uses)

| Block | Part class | For |
| --- | --- | --- |
| Level shifter | 74AHCT125, 3.3 → 5 V, 4 channels | Addressable LED data (auction) |
| RS-485 transmitter | MAX3485 class, 3.3 V, driver always on; A/B/GND terminal | Flip-dot panel (transmit only) |
| ccTalk interface | Open-collector, TX and RX joined on one line, with pull-up to the hopper's logic level | Coin hopper (gettoneria) |
| VE.Direct | Victron's 4-pin connector; a resistor divider on the receive line (fit if the Victron sends 5 V) | Every battery-tier node |
| I²C | 3 module headers (4-pin) at 3.3 V, from the I/O board's 3.3 V; footprints for a **TCA9548A** multiplexer and an **MCP23017** port expander | NFC readers, INA219, inhibit and flap lines |

### 4.5 Linking GPIOs to functions

Each GPIO line from the cables goes to **a protected terminal** and, through a **solder jumper or 0 Ω link**, to one channel's gate or one interface. A node is configured by which links are fitted; the per-node table (5) is printed in the build notes. No GPIO drives two things.

## 5. Population per node

GPIOs follow each node's existing pin table.

| Node | Channels | Inputs | Interfaces |
| --- | --- | --- | --- |
| Street auction | LS1–LS3: locks (26, 13, 27) | Door switches (32, 33, 36) | Level shifter (LED data on 14); VE.Direct |
| Gettoneria | LS1: flap (14); HS1: hopper (26) | Accept pulse (36) | ccTalk (32, 33); acceptor inhibit (17) passed through; VE.Direct; I²C: TCA9548A + 3 NFC; status LED on 13 |
| Flip-dot wall | HS1: 24 V converter (17) | Accept pulse (33); knobs (26, 13, 14, 36); button (27) | RS-485 (32); VE.Direct; I²C: expander (inhibit, flap) + NFC |
| Arm game | HS1: arm 12 V, 5 A (17) | Hole sensors (32, 33, 36, 13, 14) | Arm UART (26, 27) passed through with protection; VE.Direct; I²C: INA219 (+ optional MCP23017) |
| SUNSET set, with locker | LS1: lock (26); HS1: charger (32) | Door switch (33) | VE.Direct |
| Garden node | LS1: pump (26) | Floats (33, 36); soil probe (32, analog: passed through without the filter) | — (no battery). Keeps R19: the 12 V converter on AUX is enabled from the carrier's `5V SW` (garden-node.md 3) |

## 6. Size and mounting

About 100 × 60 mm, 2 layers, 2 oz copper for the switched paths, 4 × M3 holes. It sits beside the carrier in the same enclosure on the battery tier's mounting plate, its power terminals on the edge facing the battery and loads, its three headers on the edge facing the carrier.

## 7. To settle when it is drawn

| Item | Question |
| --- | --- |
| Part numbers | MOSFETs, high-side switch, buck, regulator, as for the carrier's BOM |
| HS rating | 6 A is set by the arm (12 V × 5 A peaks); check the hopper's start current |
| ccTalk level | The hopper's ccTalk logic level (5 V or 12 V pull-up) sets the interface's pull-up |
| VE.Direct level | The 75/15's TX voltage decides whether the divider is fitted (battery-tier.md 1.3) |
| Arm UART level | Whether the RoArm's UART is 3.3 V (interactive-arm-game.md 3) |

## 8. Tests

1. **Bench, unloaded:** VIN, 5 V and 3.3 V; every channel off at power-up and through an ESP32 reset.
2. **Each channel under load:** a lock solenoid on LS1 (flyback clamps the kick); a 5 A dummy load on HS1 for an hour (temperature of the switch).
3. **Ground separation:** solenoid pulses while the carrier reads its ADCs; no shift in the readings.
4. **Inputs:** a static discharge to each input terminal; the ESP32 keeps running.
5. **Per node:** the node's own tests, with its population.
