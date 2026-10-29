# The flip-dot wall — a cash-only interactive node on carrier v1

A SUNSET interactive node with a **flip-dot panel**: a grid of mechanical pixels, each a small disc that shows one colour or the other. **A dot can only be flipped with a token.** No phone, no app: the visitor drops a token from the gettoneria into the slot, turns two knobs to choose a dot, and presses to flip it. Spent tokens stack up in a **token column** beside the panel, the day's spending in view.

It runs on carrier v1 on the battery tier: the panel feeds a Victron SmartSolar MPPT 75/15 and a 12 V LiFePO₄ battery, with JP1 off and the sun sensor compiled out. The tier is specified in [battery-tier.md](battery-tier.md); the tokens in [interactive-token.md](interactive-token.md).

> Status: draft 6, 25 Oct 2026 (Alfa-Zeta's second reply: start-up, partial updates, housing, spares). Paid with **tokens** from the gettoneria (coin reader and NFC reader), no longer paper stickers. Sized: two 14 × 28 panels as a 28 × 28 square, yellow on black. Alfa-Zeta's quote, power data, serial protocol (rev. Oct 2023) and user manual (rev. 11.0) are in (3.1, 3.3, 3.6, 3.7). Nothing built. **Nothing here changes the carrier board.**

---

## 1. The idea

- **Cash only.** The only way to flip a dot is a token. Digital stamps can't do it, so tokens have a use of their own, and **anyone can take part without a phone:** someone hands them a token, they spend it at the wall.
- **Proof of mark.** Every dot on the panel was paid for with a token. Over a season the town draws a shared picture, one paid pixel at a time.
- **Mechanical pixels.** A flip-dot holds its position with no power and needs only a short pulse to change, with an audible click. It is readable in full sun, where screens wash out, and it keeps showing the picture all night with no energy at all.
- **The token column.** Spent tokens drop into a tall perspex tube beside the panel: the day's spending, stacked in view. At the round they go back to the gettoneria and into circulation again (5).
- **Daylight only,** like all SUNSET business: flipping runs from sunrise to sunset. The picture stays up all night.

### Where it sits in SUNSET

| Node | Proof | Direction |
| --- | --- | --- |
| Wall (message nodes) | walk | earn |
| Arm game ([interactive-arm-game.md](interactive-arm-game.md)) | skill | earn |
| Street auction ([interactive-auction.md](interactive-auction.md)) | bid | transfer; listing fee is a sink |
| Gettoneria ([interactive-token.md](interactive-token.md)) | mint | convert digital ⇄ tokens; souvenir is a sink |
| **Flip-dot wall** | **mark** | **spend, tokens only:** a sink |

---

## 2. A flip, step by step

1. **Pay.** Drop a token into the slot. The **coin acceptor** turns away anything that isn't a token (euro coins, foreign coins, washers) straight back to a return cup; a token it accepts rests on a flap over the **NFC reader** while its tag is read, as at the gettoneria (interactive-token.md 4.5). The node checks it is genuine (the gettoneria's signature), *issued* and within its date (2.1), marks it spent, and the token falls into the column. **One token, one flip;** drop more for more.
2. **Choose.** A **cursor dot** starts blinking on the panel. Two knobs move it, one across and one up and down, like an Etch A Sketch.
3. **Flip.** Press the button: the dot under the cursor flips. Repeat until the flips paid for are used.

**Non-tokens come back; bad tokens are kept.** The acceptor returns anything that isn't a token, so real money is never kept. A token that fails the NFC check (unknown, already spent, a souvenir, expired, or a clone of a token already used) is **kept**: the light shows red, nothing flips, and the token falls into a separate locked box, out of circulation. The page explains why. An expired genuine token goes back into circulation from there at the round; a clone does not.

### 2.1 No double spending, without a phone

The coins use unclonable NTAG 424 DNA tags (SECURITY.md D2), but a shared ledger is still needed: if the flip-dot wall and the gettoneria each kept their own ledger, a coin spent here (and dropped in the column) would still look live at the gettoneria until couriers carried the news between them.

**The fix: the two nodes share one ledger in real time,** over **ESP-NOW**, the ESP32's own board-to-board radio link. It needs no access point, uses little power, and reaches tens of metres along a street (more in line of sight). Every spend at either node is known to the other within a second, so nothing can be spent twice.

- **This sets the site:** the flip-dot wall must stand within ESP-NOW range of the gettoneria. Placing them as a pair (the mint, and the wall where its tokens are spent) suits the story anyway.
- **Signatures are still checked locally:** each token's tag carries the gettoneria's Ed25519 signature over its ID (interactive-token.md 2.1), so the wall knows a token is genuine without asking anyone. The shared ledger answers "is it live, and until when?".
- **Clones remain possible, and accepted** as part of SUNSET's recognised bug: the first use wins, and the other copy is kept by the machine that refuses it (interactive-token.md 2.4).
- ESP-NOW and the node's own Wi-Fi access point work together as long as both use the same radio channel.

---

## 3. Hardware

### 3.1 Parts

| Part | Notes |
| --- | --- |
| **Flip-dot panel** | **Two Alfa-Zeta XY5 14 × 28 panels, stacked to make a 28 × 28 square: 784 dots, yellow on black (like the sun).** 13.5 mm dots; four 7 × 28 modules, each with its controller (RS-485). **€880** (2 × €440) plus €25 shipping; in stock or 1–4 weeks (quote, 23 Oct 2026). A reclaimed bus-sign panel is the later "reuse" version |
| **24 V supply for the panel** | A **fixed-output, regulated** 12 V → 24 V DC-DC converter (industrial, about 2 A out for the two panels, for example Mean Well SD-50A-24 class; its input fused for about 5 A peaks from the battery) from the battery, through its own fuse, with an enable or a switch in its input. Fixed, not an adjustable boost module: the panel's **maximum is 25 V**, only 1 V above nominal. Alfa-Zeta warns that panels fed straight from solar suffer from the unstable voltage; on the battery tier the converter sees a steady 12.8–14.4 V |
| **RS-485 transceiver** | 3.3 V (MAX3485 class), carrier to panel |
| **Coin acceptor** | A programmable coin acceptor taught on sample tokens, the same model as the gettoneria's: tokens go on to the reader, everything else to a **return cup**. Refuses everything while inhibited (out of hours, at noon, on a fault, unpowered). A light beside it shows green (paid) or red (kept) |
| **NFC reader** | PN532 class, its antenna on the chute just below the slot, reading each token as it falls; on the I2C header J13 |
| **Token column and kept-token box** | A tall perspex tube for spent tokens, in view; a small locked box for refused ones. Both emptied at the round |
| **Two knobs and a button** | Rotary encoders with vandal-resistant metal knobs, and a large push button |

### 3.2 Pins

The panel only listens, so it needs only the TX pin of the ESP32's second UART. The coin reader's signal takes the RX pin's place as a plain input; the NFC reader sits on the I2C header.

| Use | GPIO | Header | Notes |
| --- | --- | --- | --- |
| Panel data (RS-485, UART1 TX) | 32 | J9 | Transceiver's driver permanently enabled: the carrier is the only sender on the bus |
| Coin acceptor: token accepted | 33 | J9 | A pulse per accepted token |
| Coin acceptor inhibit, flap | I2C 21 / 22 | J13 | Every J9 pin is in use: an I2C port expander (PCF8574 class) beside the NFC reader drives the acceptor's inhibit and the two-way flap (column or kept-token box) |
| NFC reader | I2C 21 / 22 | J13 | Shared with the DS3231 (different addresses) |
| Knob 1 (across), A / B | 26, 13 | J9 | |
| Knob 2 (up and down), A / B | 14, 36 | J9 | 36 is input only and needs an external pull-up |
| Flip button | 27 | J9 | **Remove R19** on the carrier (gives up the switched 5 V output, unused here) |
| 24 V converter on/off | 17 | J10 | J10's TX line, free because VE.Direct runs in text mode, receive only (as on the arm game: interactive-arm-game.md 3.6). Drives the converter's enable, or a MOSFET in its input; off at boot |
| VE.Direct | 16 RX | J10 | Text mode, receive only |
| Clock | 21 / 22 | on board | Sunrise and sunset; dates in the log |
| Enclosure temperature probe | 4 | J4 / J5 | Heat check |

Every J9 pin is in use; the panel's power switch takes GPIO 17 from J10 instead (3.3).

### 3.3 Power

| Load | Draw | Notes |
| --- | --- | --- |
| ESP32, Wi-Fi and ESP-NOW on, sunrise to sunset | about 0.5 W | about 6 Wh a day |
| Flip-dot pulses | peak 680 mA at 24 V per 14 × 28 panel, so about 1.4 A for the square, while flipping | A complete 14 × 28 redraw takes 160 ms at 680 mA: about **2.6 J**, so about 5 J for the square. Negligible, even for hundreds of flips |
| Panel controllers, idle | **40 mA at 24 V per 14 × 28**, 80 mA for the square: about 2 W | 46 Wh a day if left on, four times the ESP32. So the panels are **powered only while someone is flipping** (3.4) |
| Daily exercise | about 32 W for 5 minutes (both panels) | about 2.7 Wh a day: the largest single load (3.7) |
| Coin and NFC readers | about 0.3–0.5 W while on | only in business hours |

Holding the picture costs nothing: the dots stay where they are with no power.

**A 14 × 28 is two independent 7 × 28 modules,** joined only mechanically. Each has its own controller and needs its own 24 V feed and RS-485 connection (daisy-chained module to module with short RJ11 cables), each with its own address. The supply is sized at 1 A per 14 × 28 panel: **2 A for the square.**

### 3.4 Powering the panel only when needed

Alfa-Zeta: "You can safely switch off everything between updates to reduce power to zero."

- **A session powers it up:** a valid token switches the 24 V converter on (GPIO 17); the cursor blinks while the visitor turns the knobs and flips; a minute after the last flip (or when the flips paid for are used) the converter switches off.
- **At power-up the controller does nothing** but wait for data: no flipping, no test (Alfa-Zeta, 25 Oct 2026). The picture stays exactly as it was.
- **But it forgets which way each dot points.** So the **first frame after power-up energises every dot** in its correct direction. Dots already in place don't move, so nothing visible happens, but that first frame costs more energy. **After that, a frame only flips the dots that change.**
- **So on each wake the ESP32 first sends the whole stored canvas** (from flash): invisible, and it puts the controller back in step. Every flip after it moves one dot.
- **A second controller exists** with a shift register, which pulses truly one dot at a time even after power-up. Not needed: on the battery tier the extra energy of the first frame is negligible (about 5 J for the square, 3.3), and the standard controller already moves only the dots that change.
- **Daily energy:** a few minutes of idle per session plus the flips: well under 1 Wh a day.

### 3.5 Heat and the enclosure

- Alfa-Zeta: operating **−40 to +70 °C**, humidity up to 90 % **without condensation**; outdoors it must be **closed and ventilated.**
- **The risk is heat, not cold.** Black dots behind a window, in the Sardinian sun, can pass 70 °C inside a closed box. Site the wall facing **north or in shade** (it needs no sun of its own: the node's PV panel is separate), use a light-coloured, ventilated enclosure and a breather vent against condensation. **Alfa-Zeta's recommendation: a steel housing with a glass window** (glass for scratch and UV resistance; the steel painted light against heat).
- The enclosure probe (J4/J5) pauses flipping above a set temperature and posts a service notice (SUNSET.md 7.1).
- The manual gives **−40 to +80 °C** and 5–95 % humidity, non-condensing (the email said 70 °C: design for 70). It also asks for a **housing against dust and humidity, ventilated against sun load**. On the coast, the vents need filters against dust and salt.
- **Handling (manual):** the dots are delicate and sensitive to static and dust, especially metal particles. Never drill with the boards fitted; handle modules by their edges; store them dots-down only with all dots turned white. Fixing is by brass threaded tubes on each module (3.8).

### 3.6 The protocol

From Alfa-Zeta's *Flipdots display control protocols* (October 2023). One-way serial over RS-485: the carrier talks, the panels never answer.

```
0x80   command   address   data …   0x8F
```

| Command | Data bytes | Shown at once? | Display |
| --- | --- | --- | --- |
| `0x83` | 28 | yes | 7 × 28 |
| `0x84` | 28 | no: stored until a refresh | 7 × 28 |
| `0x82` | 0 | (the refresh itself: `0x80 0x82 0x8F`) | all displays on the line |

- **Data:** one byte per column of 7 dots, 28 bytes per module. Bit 0 (LSB) is the top dot, bit 6 the bottom; bit 7 is ignored and set to 0.
- **Address:** set on each module's DIP switch DS#1, positions 0–5 (up to 64); 255 (`0xFF`) is broadcast. For the 28 × 28 square: **modules 1–4, top to bottom,** on one RS-485 line. Each frame addresses one 7-dot band of the square.
- **Speed:** DIP switch DS#2: 9600, 19200, 38400 or 57600 baud. **9600.**
- **No single-dot command.** A flip sends the module's whole 28-byte frame with the one dot changed. The ESP32 keeps the canvas, so this is simple: 32 bytes per flip.
- **Updating both modules together:** send each with `0x84` (store), then one `0x80 0x82 0x8F`, so the whole picture changes at once (used for the morning exercise and redraws, 3.7).
- **No reply, so no fault detection.** The controller cannot report a stuck dot. A dot that fails to turn is visible only to the eye, and found at the round (3.7).
- DIP DS#1 position 6 sets magnetising time (500 µs default); position 7 is the module's built-in test mode, off in use.

### 3.7 Keeping the dots turning

The manual is clear that flip-dots outdoors need **exercise and cleaning**:

- **Daily exercise at noon.** After a period without use, dots can become "lazy" or blocked. The manual's remedy is a black–white flip-flop routine: **at least 5 minutes a day,** 10 minutes after more than two days idle. The node runs it **every day at solar noon** (from the clock, `sunTimes`, as SUNDIAL's dial keeps solar time), then redraws the town's picture from flash. It costs about 32 W for 5 minutes, **about 2.7 Wh a day**, more than everything else the panel uses. It is part of the work: *the wall marks noon.*
- **Noon overrides everything on the panel.**
  - **Before:** from 5 minutes before noon, the coin acceptor is inhibited: any coin dropped comes straight back to the return cup, the light shows red, and the page says when flipping resumes.
  - **During:** a session still running at noon is paused. Its tokens are already spent, so its **remaining flips are kept** (written to flash) and the cursor comes back for them after the exercise, for 10 minutes; unused flips then lapse, as any unused flips do.
  - **Nothing else drives the panel** during the exercise: no flips, no redraws, no knob input.
  - **After:** the picture is redrawn exactly as it was, and flipping reopens.
  - After more than two days without power (a dark spell, a repair), the first noon runs 10 minutes, as the manual asks.
- **Cleaning every round.** The manual's preventive cleaning is **at least every 4 weeks**: compressed air at about 3 cm, then a vacuum at minimum suction from at least 5 cm, never closer. **Never any lubricant.** SUNSET's fortnightly round is within that (SUNSET.md 7.2). Lazy or stuck dots are cleaned or replaced. **Spare dots:** none come with a panel, but Alfa-Zeta gives a few and keeps yellow-on-black in stock at **€0.50 a dot**; keep a box of spares with PVA's kit.
- **Visitors can't be told when a dot sticks** (3.6), so a paid flip on a stuck dot fails silently. The daily exercise and the fortnightly cleaning keep this rare; the round log records any dot that needed attention.

### 3.8 Size and fixing

From Alfa-Zeta's dimension drawing for the 14 × 28 panel (rev. 2, received 25 Oct 2026). **The drawing is proprietary and issued in confidence:** PVA keeps it privately; only the envelope SUNSET needs is recorded here.

| | One 14 × 28 panel | The 28 × 28 square (two stacked) |
| --- | --- | --- |
| Face | about **432 × 213 mm** | about **432 × 427 mm** |
| Depth | about **67 mm**, dots to the back of the controllers | the same |
| Dot pitch | about 15.4 mm across (13.5 mm dots) | |
| Fixing | **24 × M3 threaded tubes, 12 mm**, on the back; the drawing marks the suggested fixing points and the alignment of the mounting structure | |
| Clearance | a **15 mm zone** at the controller side for plugging in the connectors | |

- **The enclosure** for the square is therefore roughly **480 × 470 × 100 mm** inside, before the converter, the readers and the board: a steel box with a glass window (3.5), the panels on a flat plate fixed through the M3 tubes, connector side kept clear.
- **The drawing's own notes:** orientation arrows face up; store with all dots set; the panels must be in a weatherproof enclosure that keeps them within their operating temperature.

---

## 4. The picture

- **One shared canvas, a 28 × 28 square of yellow dots,** built a paid dot at a time. Any dot can be flipped, including someone else's.
- **The node's page shows it** (in daylight, on the node's Wi-Fi), with a history: how many dots were flipped each day, and the picture at each sunset.
- **At each sunset the node records the picture,** like a sealed dial. A season's sunsets make a time-lapse, and a candidate for the year's PVA print.

---

## 5. The token column

- **What it is:** a tall perspex tube beside the panel, where every spent token lands: the day's spending, stacked in view.
- **Why:** a spent token has no value until it is back in the hopper, so it can be shown in public. The column grows through the day; its height is the town's spending.
- **Every day:** the gateway's host (or PVA) empties the column into the gettoneria next door, in its return mode, so the tokens are back in the hopper by morning (interactive-token.md 3.7). A photograph of the column before emptying goes in the log.
- **At the round:** PVA empties the kept-token box for the bench check.

---

## 6. Open questions

| Question | Notes |
| --- | --- |
| Bench and spare module | One extra 7 × 28 module (€220): the bench piece for all the firmware now, and the installation's spare later (a fifth module for the four of the square) |
| Flips per token | One token, one flip (decided with the gettoneria: every token is worth one stamp) |
| Canvas policy | Never reset, reset yearly, or kept as a permanent record of the town |
| Cursor | Blinking cursor dot on the panel, or a small separate indicator |
| Site | Within ESP-NOW range of the gettoneria; shade for the electronics |
| Token column | Height and capacity, so it holds a busy day |
| Phone flips | Whether digital stamps should ever flip dots (currently no: cash only) |

## 7. Pilot tasks

| Task | What to settle |
| --- | --- |
| ESP-NOW link | Range and reliability between the gettoneria and the wall on the chosen street, alongside the access point |
| Double spend | Clone a token, spend the clone here and redeem the original at the gettoneria: the second must be refused and kept |
| Readers | Every token seen by the coin reader and read by the NFC reader as it falls |
| Panel controller | Idle draw at 24 V; whether to switch it off at night |
| Controls | Knobs and button usable by first-time visitors without instructions |
