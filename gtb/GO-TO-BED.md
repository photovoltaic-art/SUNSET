# PVA no. 2 — GO TO BED

*Concept, on hold. Opened 21 Oct 2026. Not yet a project: this note keeps the idea and its open questions.*

## The idea

A group chat that goes to bed at sunset.

A set of retired PV panels, each with a small board behind it, forms an offline radio network across a town. Anyone with a phone can join a panel's Wi-Fi and take part in one shared conversation, **without a SIM, an internet connection, an account or an app**. The panels pass messages between each other by radio. They run only on their own sunlight: when the light goes, the network goes to bed, and wakes again with the sun.

It is both a **proof of concept for minimal, unattended comms infrastructure** and an **artwork**. The point is that it is unattended and only powers up in the day.

## What it is, and is not

- **A group chat**, not a notice board: one shared room, open to whoever is in range of any panel, at the sun's pace.
- **Store and forward:** messages written while some panels sleep are passed on when they wake. Delivery can take hours. That is part of the work.
- **Unattended:** no operator, no server, no backhaul.
- **No app (aim):** each panel serves the chat as a web page through its own Wi-Fi, the way SUNDIAL serves its dial.

## The tone

Not a record of the day, like SUNDIAL's dial, but a **dial tone you can see**: the first thing on screen when a phone joins a panel's Wi-Fi, answering one question at a glance: *is anyone there?*

- **The tone:** a slow pulse at the centre while the network is awake. No pulse, no network: it has gone to bed.
- **Here:** small marks round the pulse, one per phone connected to this panel now (up to about 10).
- **The town:** a ring of nine points, one per panel, lit if that panel is awake and reachable. The ring fills in the morning and empties towards sunset as panels go to bed, each at its own time.
- **Last voice:** how long ago the last message reached this panel.

That is all: live, simple, wordless enough to read in any language. Its job is to give a **reason to participate**: someone is listening, the town is awake, a message sent now will travel. Below it, the chat.

Bedtime is part of the tone: as a panel's light fails, its pulse slows and its own point dims, then the page says goodnight. Messages left after that wait for the morning.

## Building on SUNDIAL

- **Same principles** ([MANIFESTO](../MANIFESTO.md)): the panel powers only itself; offline by nature; the work keeps no one; slow.
- **Same base hardware where possible:** the SUNDIAL carrier's power path, sun sensor and clock, with lessons from its v1 bench test.
- **The SUNDIAL carrier already has the hooks:** an AUX output that takes spare panel power through its own converter, a switched 5 V output, and spare SPI/UART/I²C pins. The firmware sheds AUX loads the moment the panel voltage sags, so the board always has priority.

## Technical direction (to test, not decided)

- **Board:** ESP32, probably an ESP32-S3 with PSRAM for message storage and a larger web client (SUNDIAL v1 uses the original ESP32).
- **Panel-to-panel radio:** best in class for range at low power, most likely **LoRa** (SX1262 class). Alternative: ESP-NOW long-range mode, if the walls have line of sight. LoRa carries little data, which suits short text.
- **Comms scaled to the available power:** the board already measures the panel's sunlight every 10 s. The radio's transmit power, duty cycle and how often it relays could follow that reading: more sun, more talk; weak sun, a whisper; no sun, sleep. Higher-power radio stages could run from the AUX output.
- **Messages:** short text, signed and with an expiry. Nostr's event format (signed, open, with expiry) is a candidate; a minimal Nostr relay already runs on an ESP32-S3 ([wisp-esp32](https://github.com/privkeyio/wisp-esp32)).
- **Phones:** the panel serves a small chat page over plain `http`; the page and its relay share the panel's address, so the browser can connect without an app. The phone makes a temporary key for the visit: no account, no lasting identity.

## Open questions

1. **Range:** does a radio link reach between real walls in a town of stone? (Test 2.)
2. **Night:** is a network that sleeps the point, or a flaw? The concept says it is the point. A battery would break principle 3.
3. **Open posting in public:** spam, abuse, illegal content, and the operator's responsibility under Italian law. Rate limits, expiry, and perhaps a quiet mode.
4. **Captive-portal browsers:** limited storage and scripts on some phones; does the chat page work in the Wi-Fi pop-up, or must visitors open a full browser?
5. **Capacity:** about 10 phones per panel at once.
6. **How many panels:** SUNDIAL's rule is nine; GO TO BED may need a different number, set by radio range.

## Tests, in order

1. **Bench:** a relay and a minimal web chat on one ESP32-S3, used from two phones with no internet.
2. **Two walls:** two boards on two real walls in Bosa; ESP-NOW long range, then LoRa; measure what gets through, and at what panel power.
3. **Power scaling:** radio power and duty cycle following the sun reading.
4. Only then: a spec and a carrier variant.

## Status

On hold while SUNDIAL v1 goes to manufacture. Prior art to study when it resumes: Meshtastic (LoRa mesh, app over Bluetooth), Bitchat (phone-to-phone Bluetooth mesh with Nostr bridging).
