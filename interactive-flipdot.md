# The flip-dot wall — a cash-only interactive node on carrier v1

A SUNSET interactive node with a **flip-dot panel**: a grid of mechanical pixels, each a small disc that shows one colour or the other. **A dot can only be flipped with a paper stamp.** No phone, no app: the visitor holds a redeem sticker from the print node up to the scanner, turns two knobs to choose a dot, and presses to flip it. Beside the panel is a **sticker wall**, where people stick their spent stickers.

It runs on carrier v1 on the battery tier: the panel feeds a Victron SmartSolar MPPT 75/15 and a 12 V LiFePO₄ battery, with JP1 off and the sun sensor compiled out. The tier is specified in [battery-tier.md](battery-tier.md); the paper stamps in [interactive-print.md](interactive-print.md).

> Status: draft 3, 23 Oct 2026. Alfa-Zeta's quote, power data, serial protocol (rev. Oct 2023) and user manual (rev. 11.0) are in (3.1, 3.3, 3.6, 3.7). Nothing built. **Nothing here changes the carrier board.**

---

## 1. The idea

- **Cash only.** The only way to flip a dot is a paper redeem sticker. Digital stamps can't do it, so paper stamps have a use of their own, and **anyone can take part without a phone:** someone hands them a sticker, they spend it at the wall.
- **Proof of mark.** Every dot on the panel was paid for with paper. Over a season the town draws a shared picture, one paid pixel at a time.
- **Mechanical pixels.** A flip-dot holds its position with no power and needs only a short pulse to change, with an audible click. It is readable in full sun, where screens wash out, and it keeps showing the picture all night with no energy at all.
- **The sticker wall.** A spent sticker has no value, but it is kept: stuck on a wall panel beside the flip-dot panel. The wall becomes a **public ledger of spending,** each round sticker with its serial, readable by anyone.
- **Daylight only,** like all SUNSET business: flipping runs from sunrise to sunset. The picture stays up all night.

### Where it sits in SUNSET

| Node | Proof | Direction |
| --- | --- | --- |
| Wall (message nodes) | walk | earn |
| Arm game ([interactive-arm-game.md](interactive-arm-game.md)) | skill | earn |
| Street auction ([interactive-auction.md](interactive-auction.md)) | bid | transfer; listing fee is a sink |
| Print node ([interactive-print.md](interactive-print.md)) | print | convert digital ⇄ paper; souvenir is a sink |
| **Flip-dot wall** | **mark** | **spend, paper only:** a sink |

---

## 2. A flip, step by step

1. **Pay.** Hold a redeem sticker up to the scanner window. The node reads the QR, checks the signature and that the sticker is unspent (2.1), and marks it spent. A sticker's value is its number of flips: a 5-stamp sticker buys 5 flips.
2. **Choose.** A **cursor dot** starts blinking on the panel. Two knobs move it, one across and one up and down, like an Etch A Sketch.
3. **Flip.** Press the button: the dot under the cursor flips. Repeat until the sticker's flips are used.
4. **Stick.** Peel the spent sticker and put it on the sticker wall.

A sticker that has already been spent is refused: the scanner light shows red, and nothing flips.

### 2.1 No double spending, without a phone

A paper sticker can be copied. If the flip-dot wall and the print node each kept their own spent list, a photocopy could be spent here and redeemed at the print node before couriers carried the news between them.

**The fix: the two nodes share one spent list in real time,** over **ESP-NOW**, the ESP32's own board-to-board radio link. It needs no access point, uses little power, and reaches tens of metres along a street (more in line of sight). Every spend at either node is known to the other within a second, so nothing can be spent twice.

- **This sets the site:** the flip-dot wall must stand within ESP-NOW range of the print node. Placing them as a pair (the mint, and the wall where its paper is spent) suits the story anyway.
- **Signatures are still checked locally:** the stickers carry a public-key signature (interactive-print.md 3.3), so the wall knows a sticker is genuine without asking anyone. The shared list only answers "has it been spent?".
- ESP-NOW and the node's own Wi-Fi access point work together as long as both use the same radio channel.

---

## 3. Hardware

### 3.1 Parts

| Part | Notes |
| --- | --- |
| **Flip-dot panel** | Alfa-Zeta XY5, 13.5 mm dots, controller included (RS-485). **7 × 28: €220; 14 × 28: €440**; shipping to Italy €25; in stock or 1–4 weeks (quote, 23 Oct 2026). White on black or yellow on black. Two 14 × 28 side by side make a 28 × 28 square canvas (€880). A reclaimed bus-sign panel is the later "reuse" version |
| **24 V supply for the panel** | A **fixed-output, regulated** 12 V → 24 V DC-DC converter (industrial, about 1.1 A out, for example Mean Well SD-25A-24 class) from the battery, through its own fuse, with an enable or a switch in its input. Fixed, not an adjustable boost module: the panel's **maximum is 25 V**, only 1 V above nominal. Alfa-Zeta warns that panels fed straight from solar suffer from the unstable voltage; on the battery tier the converter sees a steady 12.8–14.4 V |
| **RS-485 transceiver** | 3.3 V (MAX3485 class), carrier to panel |
| **QR scanner** | Small fixed-mount module (GM65 class), behind a window in the enclosure, reading the sticker held up to it. Its light shows green (paid) or red (refused) |
| **Two knobs and a button** | Rotary encoders with vandal-resistant metal knobs, and a large push button |
| **Sticker wall** | A panel beside the flip-dot panel for spent stickers: smooth, weatherproof, easy to stick to (enamelled steel, aluminium or acrylic, chosen in the pilot) |

### 3.2 Pins

One serial port serves both the panel and the scanner: the panel only listens and the scanner only talks, so the ESP32's second UART sends to the panel on its TX pin and receives from the scanner on its RX pin, both at the same speed (for example 9600 baud, set on both devices).

| Use | GPIO | Header | Notes |
| --- | --- | --- | --- |
| Panel data (RS-485, UART1 TX) | 32 | J9 | Transceiver's driver permanently enabled: the carrier is the only sender on the bus |
| Scanner data (UART1 RX) | 33 | J9 | Scanner set to the same speed as the panel |
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
| Flip-dot pulses | peak 680 mA at 24 V for a 14 × 28 (340 mA for a 7 × 28), while flipping | A complete 14 × 28 redraw takes 160 ms at 680 mA: about **2.6 J**. Negligible, even for hundreds of flips |
| Panel controller, idle | **40 mA at 24 V for a 14 × 28** (20 mA for a 7 × 28): about 1 W | 24 Wh a day if left on, twice the ESP32. So the panel is **powered only while someone is flipping** (3.4) |
| Daily exercise | about 16 W for 5 minutes | about 1.5 Wh a day: the largest single load (3.7) |
| QR scanner | about 0.5–1 W while on | only in business hours |

Holding the picture costs nothing: the dots stay where they are with no power.

**A 14 × 28 is two independent 7 × 28 modules,** joined only mechanically. Each has its own controller and needs its own 24 V feed and RS-485 connection (daisy-chained module to module with short RJ11 cables), each with its own address. The supply is sized at 1 A per 14 × 28 panel.

### 3.4 Powering the panel only when needed

Alfa-Zeta: "You can safely switch off everything between updates to reduce power to zero."

- **A session powers it up:** a valid sticker switches the 24 V converter on (GPIO 17); the cursor blinks while the visitor turns the knobs and flips; a minute after the last flip (or when the sticker's flips are used) the converter switches off.
- **After power-up, resend the picture.** The ESP32 keeps the canvas in flash and sends the whole frame each time the panel wakes, in case the controller clears or tests the dots on start-up (to confirm with Alfa-Zeta).
- **Daily energy:** a few minutes of idle per session plus the flips: well under 1 Wh a day.

### 3.5 Heat and the enclosure

- Alfa-Zeta: operating **−40 to +70 °C**, humidity up to 90 % **without condensation**; outdoors it must be **closed and ventilated.**
- **The risk is heat, not cold.** Black dots behind a window, in the Sardinian sun, can pass 70 °C inside a closed box. Site the wall facing **north or in shade** (it needs no sun of its own: the node's PV panel is separate), use a light-coloured, ventilated enclosure with a UV-stable polycarbonate front, and a breather vent against condensation.
- The enclosure probe (J4/J5) pauses flipping above a set temperature and posts a service notice (SUNSET.md 7.1).
- The manual gives **−40 to +80 °C** and 5–95 % humidity, non-condensing (the email said 70 °C: design for 70). It also asks for a **housing against dust and humidity, ventilated against sun load**. On the coast, the vents need filters against dust and salt.
- **Handling (manual):** the dots are delicate and sensitive to static and dust, especially metal particles. Never drill with the boards fitted; handle modules by their edges; store them dots-down only with all dots turned white. Fixing is by brass threaded tubes on each module (drawings on request).

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
- **Address:** set on each module's DIP switch DS#1, positions 0–5 (up to 64); 255 (`0xFF`) is broadcast. For a 14 × 28: top module 1, bottom module 2. A 28 × 28 (two panels, four modules): 1–4 on one line.
- **Speed:** DIP switch DS#2: 9600, 19200, 38400 or 57600 baud. **9600**, the QR scanner's default, so both share UART1 as 3.2 describes.
- **No single-dot command.** A flip sends the module's whole 28-byte frame with the one dot changed. The ESP32 keeps the canvas, so this is simple: 32 bytes per flip.
- **Updating both modules together:** send each with `0x84` (store), then one `0x80 0x82 0x8F`, so the whole picture changes at once (used for the morning exercise and redraws, 3.7).
- **No reply, so no fault detection.** The controller cannot report a stuck dot. A dot that fails to turn is visible only to the eye, and found at the round (3.7).
- DIP DS#1 position 6 sets magnetising time (500 µs default); position 7 is the module's built-in test mode, off in use.

### 3.7 Keeping the dots turning

The manual is clear that flip-dots outdoors need **exercise and cleaning**:

- **Daily exercise.** After a period without use, dots can become "lazy" or blocked. The manual's remedy is a black–white flip-flop routine: **at least 5 minutes a day,** 10 minutes after more than two days idle. The node does it **once a day, mid-morning** (not at sunrise, out of respect for the neighbours: it is loud), then redraws the town's picture from flash. It costs about 16 W for 5 minutes, **about 1.5 Wh a day**, more than everything else the panel uses. It can become part of the work: *the wall stretches before the town starts drawing.*
- **Cleaning every round.** The manual's preventive cleaning is **at least every 4 weeks**: compressed air at about 3 cm, then a vacuum at minimum suction from at least 5 cm, never closer. **Never any lubricant.** SUNSET's fortnightly round is within that (SUNSET.md 7.2). Lazy or stuck dots are cleaned or replaced from the spare dots supplied.
- **Visitors can't be told when a dot sticks** (3.6), so a paid flip on a stuck dot fails silently. The daily exercise and the fortnightly cleaning keep this rare; the round log records any dot that needed attention.

---

## 4. The picture

- **One shared canvas** for the whole panel, built a paid dot at a time. Any dot can be flipped, including someone else's.
- **The node's page shows it** (in daylight, on the node's Wi-Fi), with a history: how many dots were flipped each day, and the picture at each sunset.
- **At each sunset the node records the picture,** like a sealed dial. A season's sunsets make a time-lapse, and a candidate for the year's PVA print.

---

## 5. The sticker wall

- **What it is:** a wall panel beside the flip-dot panel where spent stickers are stuck, by hand, by the people who spent them.
- **Why:** a spent sticker has no value, so it can be shown in public. Each carries its serial, so the wall is a **readable ledger:** every flip on the panel paid for by a sticker on the wall.
- **Not enforced.** People may keep their spent stickers; the node's spent list is the real record. The wall is an invitation.
- **Upkeep:** photographed at each round as part of the record; cleared or kept as an artwork at the yearly visit (5, open).

---

## 6. Open questions

| Question | Notes |
| --- | --- |
| Panel size | **14 × 28** (392 dots, €440) is the minimum for a picture; 7 × 28 (196 dots) is a ticker more than a canvas. Two 14 × 28 make a 28 × 28 square (784 dots, €880) |
| Colour | White on black or yellow on black (both standard): yellow carries the bus-sign heritage; white reads as paper |
| Start-up behaviour | Does the controller flip or test dots at power-up? Asked of Alfa-Zeta (3.4) |
| Partial updates | Does a frame re-pulse every dot, or only the dots that change? Sets the energy and the noise per flip. Asked of Alfa-Zeta |
| Flips per sticker | Value = flips (one stamp, one flip), or another rate |
| Canvas policy | Never reset, reset yearly, or kept as a permanent record of the town |
| Cursor | Blinking cursor dot on the panel, or a small separate indicator |
| Site | Within ESP-NOW range of the print node; shade for the electronics |
| Sticker wall | Material, size, and what happens when it is full |
| Phone flips | Whether digital stamps should ever flip dots (currently no: cash only) |

## 7. Pilot tasks

| Task | What to settle |
| --- | --- |
| ESP-NOW link | Range and reliability between the print node and the wall on the chosen street, alongside the access point |
| Double spend | Copy a sticker, spend it here and redeem the original at the print node: the second must be refused |
| Scanner | Reading small QR codes on stickers held at different angles, in bright sun |
| Panel controller | Idle draw at 24 V; whether to switch it off at night |
| Controls | Knobs and button usable by first-time visitors without instructions |
| Sticker wall | Stickers stay on in sun and rain; how easily they come off at clearing |
