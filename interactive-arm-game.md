# The arm game — a dexterity interactive node on carrier v1

A SUNSET interactive node with a robot arm in a transparent enclosure, played from visitors' phones. The game is **pegs in holes**: drop a peg cleanly into a hole and the machine pays a stamp. It is SUNSET's first **earning node by skill**, beside the walls, which pay for walking.

It runs on carrier v1 on the battery tier: the panel feeds a Victron SmartSolar MPPT 75/15 and a 12 V LiFePO₄ battery, with JP1 off and the sun sensor compiled out. The tier is specified in [battery-tier.md](battery-tier.md); this document covers only what is different.

> Status: draft 2, 22 Oct 2026. The arm is now the **Waveshare RoArm-M2-S** (was the Joy-IT Grab-it): closed-loop bus servos that report position, load and temperature, so the node knows when it has failed. Nothing built. **Nothing here changes the carrier board.**

---

## 1. The idea

- **An arcade claw, turned into a test of skill.** A robot arm behind perspex, steered from the visitor's phone. Nothing is won and nothing leaves the box; the prize is a stamp.
- **Proof of skill.** SUNSET pays stamps for real acts: walking a message between walls is *proof of walk*, getting a peg into a hole is *proof of skill*. Both earn the same stamp.
- **The machine is the witness.** A sensor under each hole confirms the drop, so the stamp is issued by the hardware, not claimed by the player.
- **The sun sets the issuance.** Every move costs energy. The node can only pay out as many stamps as its battery allows: a dull week mints fewer stamps.
- **Daylight only,** like all SUNSET business: play runs from sunrise to sunset.

### Where it sits in SUNSET

| Node | Proof | Direction |
| --- | --- | --- |
| Wall (message nodes) | walk | earn |
| **Arm game** | **skill** | **earn** |
| Street auction ([interactive-auction.md](interactive-auction.md)) | bid | transfer buyer → seller; listing fee is a sink |
| Flip-dot wall ([interactive-flipdot.md](interactive-flipdot.md)) | mark | spend, paper only |

**One stamp type** everywhere. Each stamp carries the 5 × 5 logo of the node that issued it, so its origin is visible, but every stamp spends the same.

---

## 2. Hardware

### 2.1 The arm: Waveshare RoArm-M2-S

A 4-axis desktop arm with its own ESP32 motion controller and **serial bus servos with feedback.** Chosen because an unattended arm has to know what it is doing.

| | Waveshare RoArm-M2-S |
| --- | --- |
| Axes | 4: 360° base, shoulder, elbow, gripper (direct-drive clamp); no wrist rotation |
| Servos | ST3215 serial bus servos, 30 kg·cm at 12 V, 12-bit magnetic encoders |
| Feedback, every servo | Position, load, temperature, voltage, current |
| Frame | Carbon fibre and aluminium, about 826 g |
| Reach | About 28 cm horizontal; about 1.09 m workspace diameter with the base turning |
| Payload | Up to 0.5 kg (manufacturer's figure) |
| Power | DC 7–13 V input (12 V, 5 A supply in the box) |
| Controller | On-board ESP32-WROOM-32U; JSON commands over UART, USB, HTTP or ESP-NOW; control code open source |
| Price | About $205–225; stocked in Europe (RobotShop EU, Grobotronics) |

**Why it, over the alternatives:**

- **It knows where it is.** A hobby servo is sent a pulse and the controller has to assume it got there. The RoArm's servos report their real angle and load on every move, so the node can catch a stall, a jam or a slipped joint, home itself each morning, and back off before a servo burns out (3.5).
- **Faults become public.** A stall or a missed position stops the game and posts a **service notice**, like the auction's faults ([SUNSET.md](SUNSET.md) 7.1).
- **12 V native,** so it lives on the battery tier with one regulator (2.3), not a separate servo supply.
- **It reads as an instrument,** carbon and aluminium behind perspex, not a classroom kit.

**Considered and set aside:**

| Arm | Why not |
| --- | --- |
| Arduino TinkerKit Braccio | Reads as a school or hobby kit; hobby servos, no feedback |
| Joy-IT Grab-it (Robot02) | Strong aluminium arm, but hobby PWM servos with no feedback, and a separate 6–7.4 V servo supply. The previous choice |
| Adeept 5-DOF (Arduino) | 9 g plastic-gear micro servos and an acrylic STEM-kit frame; would not last a season. Could serve as a cheap desk mule for firmware |

**Strength cuts both ways.** 30 kg·cm can crack a peg board or push on the perspex. The firmware sets **soft angle limits and speed limits** on every joint, and the load feedback stops a move that meets resistance.

### 2.2 The board: pegs, holes and the gravity loop

Nothing needs resetting:

- The holes are **through-holes.** A peg dropped in falls through the board onto a **sloped ramp** below and rolls back to a **hopper**, where the arm picks it up again. The pegs circulate like a marble run, and the board is always empty and ready.
- **A sensor under each hole** (IR break-beam or a small microswitch flap) gives the ESP32 a trustworthy "success" for that hole.
- **Round pegs, holes from loose to tight,** so some drops are easy and some very hard. The arm has no wrist rotation, so square or keyed pegs are out unless the gripper is set up as an extra axis.
- **Jams:** if a peg sticks on the ramp or lands outside the hopper, the arm runs a **self-clearing routine** after sunset, when play has closed. It can double as a small evening performance.

### 2.3 Wiring the arm to the carrier

**Wired and in one unit.** The arm sits in the same enclosure as the carrier and battery, joined by a UART cable. The carrier sends moves ("go to hole 3", "grip", "release") as JSON; the arm's own ESP32 runs the motion and replies with what actually happened. The PCA9685 board of draft 1 is gone, and J13 is free.

The arm's ESP-NOW link could in principle let it sit away from the panel, but the stock firmware sends no feedback over ESP-NOW, the link would need its own signing, and the arm would still need 12 V from the battery. Wired is simpler and cannot be spoofed.

| Use | GPIO / bus | Header | Notes |
| --- | --- | --- | --- |
| Arm UART: carrier TX → arm RX | 26 | J9 | UART1, 115200 baud; check the arm's UART is 3.3 V logic before wiring |
| Arm UART: carrier RX ← arm TX | 27 | J9 | **Remove R19** (as on the auction node): 27 no longer switches U4/J11 |
| Arm power enable | 17 | J10 | MOSFET or relay on the arm's 12 V feed; off at boot (pull-down), off outside play and on any fault. GPIO 17 is J10's TX line, free because VE.Direct text mode is receive-only (3.6) |
| Hole sensors 1–5 | 32, 33, 36, 13, 14 | J9 | 36 is input only and needs an external pull-up; GPIO 14 toggles at boot, harmless on an input |
| Hopper / jam sensor (optional) | J13 | J13 | An I2C port expander (MCP23017 class) if more inputs are needed; J13 is free now |
| VE.Direct | 16 RX | J10 | Text mode, receive only |
| Enclosure temperature probe | 4 | J4 / J5 | Heat check (3.5); the servos also report their own temperature |

**Arm supply:** the arm takes **7–13 V**, but a LiFePO₄ battery sits at about 13.2–13.4 V and reaches 14.2–14.6 V while charging. So the arm is fed through a **regulated 12 V DC-DC converter rated 5 A or more,** from the battery through its own fuse and the power-enable switch, never through the carrier. The sun gate stops play long before the battery is low enough to starve the converter.

### 2.4 The enclosure

- **Transparent perspex box,** like an arcade claw cabinet: the arm, the peg board, the ramp and the hopper all visible.
- **Sealed:** nothing for a hand to reach. Thick enough that the arm cannot crack it at its soft limits.
- **Heat:** servos and electronics in a perspex box in the Sardinian sun. Shade or a north-facing site, ventilation, and the temperature probe (3.5).

### 2.5 Power

| Load | Draw | Notes |
| --- | --- | --- |
| ESP32, Wi-Fi on, sunrise to sunset | about 0.5 W | about 6 Wh a day |
| Arm, during a turn | roughly 10–40 W, peaks up to 60 W (12 V × 5 A) | depends on moves; torque off between turns, power off outside play |
| Arm, waiting between turns | about 1 W | arm controller awake, servo torque off |
| Arm, per day | set by play | each turn costs energy; this is what the sun gate meters (3.3) |

A 12 V 20–40 Ah LiFePO₄ pack (about 250–500 Wh) covers a busy day with reserve. The real cost per turn is measured in the pilot.

---

## 3. The rules

### 3.1 A turn

1. **Join the node's Wi-Fi;** the game page opens. If someone is playing, join the queue.
2. **Start a turn.** The phone makes a fresh holder key for the stamp it may earn and sends only the public half ([stamp-format.md](stamp-format.md) 3.1), so the stamp can't be copied off the open network.
3. **Steer the arm:** pick a peg from the hopper, carry it to a hole, release.
4. **A sensor confirms the drop:** the node issues the stamp (`why: skill`) to that holder key, signed by the node, into the player's passport page.
5. **The turn ends** on the timer, or when the player ends it. Next in the queue.

One player at a time; the access point serves up to 10 phones, so the queue is short by design.

### 3.2 Controls and difficulty

- **Coarse moves** (rotate, reach, raise, lower) and a **fine-adjust mode** for the final placement, then **release**.
- **A turn timer,** so the queue keeps moving.
- **Difficulty pays in quantity:** an easy hole earns 1 stamp, the tightest earns 3 (values set in the pilot). One stamp type, varied earning.

### 3.3 The sun gate

- **Each turn costs energy,** so turns are offered only when the battery's charge state allows (from the Victron over VE.Direct). The page shows a charge bar filling: the sun is the coin slot.
- **Issuance is energy-backed.** The node can only mint as many stamps as its battery can pay for in moves. A cloudy week means fewer turns and fewer stamps in circulation.
- **Anti-farming,** with no identities: the sun gate, the turn timer and the queue together cap how many stamps any one person can take in a day. A daily cap per node can be added if the pilot shows it is needed.

### 3.4 Daylight only

Play runs from sunrise to sunset, like all SUNSET business. At sunset the Wi-Fi closes, the self-clearing routine (2.2) runs if needed, and the arm's power goes off until morning.

### 3.5 Feedback, faults and safety

The arm's feedback is what lets the game run unattended for a season.

- **Morning homing.** At sunrise the arm powers up, moves to its home pose and checks every joint reads where it should before the first turn.
- **Every move is checked.** After each move the carrier reads back the joint angles. A joint that didn't arrive, or arrived and then drifted, is a fault.
- **Load limit.** If a joint's load climbs past a threshold (gripper jammed on a peg, arm pressed against the board or the perspex), the move stops and the arm backs off.
- **Heat.** No play above a set enclosure temperature or servo temperature; the page says why. Torque off whenever no turn is running.
- **On a fault:** the turn ends, the player keeps any stamp already confirmed, the page shows "resting", the arm's power is cut, and the node posts a **service notice** naming the fault (stall, joint error, heat). It retries once after sunset during the clearing routine; if the fault clears, play resumes next morning.
- **Soft limits and speed limits** on every joint (2.1); the load limit is the backstop.

### 3.6 Victron link on this node

VE.Direct runs in **text mode, receive only:** the Victron broadcasts its readings every second and the carrier only listens. This frees GPIO 17 (J10's TX line) for the arm's power switch. The node cannot send HEX commands to the Victron; it doesn't need to.

---

## 4. Firmware: the interactive build, arm role

Same interactive build as the other SUNSET nodes (interactive-auction.md 4), with the node role set to **arm game**:

- arm control over UART1 (JSON commands to the RoArm's controller), with per-joint soft limits, speed limits and a load limit;
- read-back after every move, morning homing, fault handling and service notices (3.5);
- the turn queue, turn timer and controls page;
- hole sensors, and stamp issue on a confirmed drop (holder keys, stamp-format.md 3);
- the sun gate on the Victron's charge state;
- the self-clearing routine after sunset;
- every stamp issued written to flash before it is shown, so a reboot can neither lose nor repeat one.

---

## 5. Open questions

| Question | Notes |
| --- | --- |
| Number of holes and tolerances | How many holes, which shapes, how tight; how many stamps each pays |
| Control scheme | Joint-by-joint buttons, or simpler moves ("left, right, down, grip"); tested with first-time players |
| Daily stamp cap | **Likely needed:** uncapped, the arm could pay 50–150 stamps on a busy sunny day against the walls' 72 (SUNSET.md 3.1). About 30–40 a day proposed; set in the pilot |
| Peg and board materials | Durable, quiet, and kind to the arm's gripper |
| Jam handling | Whether a hopper sensor is needed, or the nightly clearing routine is enough |
| Site | Shade and ventilation for servos in summer |
| Arm firmware | Keep Waveshare's stock firmware and use its JSON commands, or flash a trimmed build (open source) that accepts only the game's moves |
| Gripper | Stock clamp, or a custom jaw shaped for the pegs |

## 6. Pilot tasks

| Task | What to settle |
| --- | --- |
| Energy per turn | Measured, to set the sun gate's thresholds |
| Difficulty | Hole tolerances and stamp values that make the game hard but winnable |
| Soft limits | Joint angles and speeds that keep the arm off the perspex and the board |
| Load thresholds | Load readings for a clean grip, a jammed peg and a push against the perspex; where to set the stop |
| UART and power | The arm's UART logic level; the 12 V converter's behaviour across the battery's range; the arm's idle draw with torque off |
| Sensor reliability | No missed drops, no false stamps (a peg brushing the sensor without dropping through) |
| Heat | Temperature inside the enclosure on a summer afternoon, servos idle and working |
| Gravity loop | Pegs return to the hopper every time; how often the clearing routine is needed |
