# The garden node — a wall node on a post, watering its own flower bed

A SUNSET **wall node** for a place with no wall: the panel stands on a post on private ground (a café's or bar's outdoor seating area), above a **closed 1000-litre tank in an IBC cage** with a **flower bed** on top. The panel's own sun pumps water to the bed, drip by drip, only when a soil probe says the bed is dry, and only while the sun shines.

It does everything a wall node does (messages, shouts, couriers, walk stamps: [wall-node.md](wall-node.md)) and adds one thing: **the sun waters what it dries.**

> Status: draft 1, 23 Oct 2026. Nothing built. **No battery, no change to the carrier board:** the pump runs off the board's AUX output, switched by its spare outputs. The post, base and heights follow SUNDIAL's free-standing panel ([hardware/POST.md](https://github.com/photovoltaic-art/SUNDIAL/blob/main/hardware/POST.md)). Structural figures there are indicative; an engineer signs off post and base.

---

## 1. Where it sits in SUNSET

- **It is one of the four walls.** SUNSET stays at nine panels: any of Walls 1–4 can be a garden node where the layout needs a wall and the place has none (SUNSET.md 4). Same wall tier: panel straight into the carrier, no battery, awake dawn to dusk.
- **Its host** is the owner of the seating area: they get a flower bed that waters itself, a wall node at their tables, and the couriers that come with it. No money and no endorsement either way (SUNSET.md 4.2).
- **Operations in public.** The tank, the soil and the pump report on the dial tone like any other node's upkeep: *tank low*, *tank empty* (SUNSET.md 7.1).

---

## 2. The object

```
            ┌──────────┐  ← gnomon root, panel top, about 2.6 m
            │  panel   │     (the gnomon, hour lines and date marks as on every PVA panel)
            │  (south) │
            │          │
            └────┬─────┘  ← panel bottom edge
   ░░░░░░░░░░░░░░│░░░░░  ← flower bed, a planter on the tank's top
 ┌───────────────┼─────┐
 │  IBC tank     │post │  ← 1000 L, closed, opaque; steel cage
 │  1.2 × 1.0 m  │     │
 └───────────────┴─────┘  ← steel base frame, bolted down
```

| Part | Specification |
| --- | --- |
| Panel and sundial | As every PVA panel: vertical, due south, 45 cm gnomon at 50°, hour lines and date marks, no numbers ([GNOMON.md](https://github.com/photovoltaic-art/SUNDIAL/blob/main/hardware/GNOMON.md)) |
| Post | Steel upright(s) rising from a base frame that also holds the IBC cage; heights as POST.md 3.1, raised as needed so the gnomon tip clears heads standing at the bed |
| Tank | A standard **IBC** (intermediate bulk container): about 1000 L, about 1.2 × 1.0 × 1.15 m, a steel cage around an HDPE bottle |
| Flower bed | A shallow planter on the cage top (about 1.2 × 1.0 m), or a bed around the base |
| Board | Carrier v1, wall build, in its box high on the back of the panel |

### 2.1 The IBC

- **Food-grade only.** Use a new IBC, or one that held only food-grade contents (it will water plants people sit beside). Never one that held chemicals.
- **Opaque.** A translucent IBC grows algae in a week of Sardinian sun, and sunlight weakens the HDPE. Use a black or opaque bottle, or clad the cage (wood, which also makes it look like a planter, not a tank).
- **Closed, and meshed.** An open water tank is a **tiger-mosquito** nursery. The fill cap stays closed; the vent and the overflow get fine stainless mesh.
- **Fill:** from the host's tap with a hose, through the top cap. A vertical panel collects almost no rain, so rainwater only if an awning or roof gutter is nearby.

### 2.2 The base: weight that comes and goes

A full IBC weighs about a tonne: that is roughly the ballast the post needs against wind (POST.md 3.2). **But the water is used up**, and an empty IBC weighs about 60 kg. So:

- **The base is designed for the empty tank.** The post is bolted to a slab or footing as POST.md 3.2 says; the water's weight is a bonus, never counted on.
- The base frame carries both the post and the cage, so the cage takes no load from the post.
- Drain plan: the IBC's bottom valve stays, locked, so the tank can be emptied for cleaning or removal.

### 2.3 How long a fill lasts

A drip-watered bed of about 1 m² needs roughly 3–6 litres a day in a Sardinian summer, much less in spring and autumn. **One fill of 1000 L lasts the dry season.** The host fills it in spring; the node says when it needs more.

---

## 3. Water, power and sensors

### 3.1 Wiring

```
 PV panel ──► carrier J1 ──► F4 (3 A) ──► D5 ──► J12 AUX ──► 12 V buck (60 V+ in) ──► I/O board VIN ──► LS1 ──► pump ──► drip lines
                                                               ▲ EN                                 ▲
                                       J11 "5V SW" (GPIO 27) ──┘                    GPIO 26 (J9 cable)
 floats, soil probe ──► I/O board inputs ──► J9 cable ──► GPIO 33, 36, 32
```

| Use | GPIO | Header | Notes |
| --- | --- | --- | --- |
| 12 V converter enable | 27 (U4) | J11 `5V SW` | Unchanged board: the converter is off whenever the board says so |
| Pump on/off | 26 | J9 | The I/O board's LS1 ([io-board.md](io-board.md)): low-side MOSFET with flyback diode, off at boot |
| Soil moisture | 32 | J9 | Capacitive probe (no exposed metal, so it doesn't corrode), powered from the carrier's 3.3 V (a few mA); analog, ADC1, works with Wi-Fi on; through the I/O board's protection, without the filter |
| Tank low (refill soon) | 33 | J9 | Float switch at about a fifth of the tank |
| Tank empty (dry-run stop) | 36 | J9 | Float switch just above the pump's intake; input only, the I/O board's pull-up |

- **The pump:** a small 12 V diaphragm or brushless pump, about 5–15 W, inside the tank or beside it, feeding drip lines on the bed.
- **No carrier change:** AUX, switched 5 V and the J9 spare pins are all on carrier v1 as built. The pump switch and the sensor inputs are on **the SUNSET I/O board** ([io-board.md](io-board.md)), as on every node that switches something: the garden node is the one wall-tier node that uses it. The I/O board is powered only while the 12 V converter is on; the floats and the soil probe are still read at any time, because their pull-ups and probe supply come from the carrier's 3.3 V.
- **Water below, electronics above:** the board's box stays high on the panel's back; every cable to the tank gets a drip loop; the pump's connections are sealed (IP68 or potted).

### 3.2 When it waters

The pump runs only when **all** of these hold:

1. The soil probe reads **dry** (threshold set in the pilot).
2. The **sun** is up and the panel's voltage is comfortably above what the board needs. The board always comes first: the converter is cut the moment the panel sags.
3. The tank is **not empty** (float switch).
4. Today's watering is **under its daily cap** (set in the pilot), so a failed probe can't empty the tank in a day.

It waters in **pulses** (for example 2 minutes on, 15 minutes to soak in, then the probe reads again), so water goes into the soil rather than off the edge.

**Without a battery it waters only in sunshine.** The hottest, sunniest days get the most water, which is when the bed needs it. Drip lines put water straight into the soil, so midday watering loses little.

### 3.3 What it reports

Honest measure: only what the node knows.

- On the **dial tone**, beside the network: the bed's moisture (dry / moist), minutes watered today, and the tank's state.
- **Service notices** (SUNSET.md 7.1): *tank low* when the first float drops, *tank empty* when the second does (the pump stops), *soil probe fault* if it reads impossible values.
- The number of fills and minutes watered over the season go to the website's archive with the other counts.

---

## 4. Power, roughly

| Load | Draw | Per day |
| --- | --- | --- |
| Board, wall build | under 1 W | as every wall node |
| Pump | 5–15 W while running | 20–40 minutes in high summer: about 3–10 Wh |

A vertical panel gives about 50–60 W at noon in June. Watering takes a sliver of it, and only around the middle of the day.

---

## 5. Open questions

| Question | Notes |
| --- | --- |
| Planting | Mediterranean plants that cope with sun-only, midday watering and a dry spell if the tank runs out: rosemary, lavender, helichrysum, salvia, sedum |
| Bed on top or around | A planter on the cage (compact) or a bed around the base (more soil, more planting) |
| Cladding | Wood around the cage, making it read as a planter |
| Proof of water? | A stamp for whoever refills the tank. **Not as it stands:** stamps are created only by proof of walk or the sun's allowance (stamp-format.md 3.2). Possible only if paid from a sun's purse of the garden node's own, like the arm's; otherwise refilling stays a host's task |
| USB sockets too | The garden node could also carry POST.md's USB charger. Priority: board, then pump, then USB |

## 6. Pilot tasks

| Task | What to settle |
| --- | --- |
| Soil threshold | The probe reading for "dry" in the chosen soil, and the pulse timing |
| Water use | Litres per day across a summer; how long a fill really lasts |
| Pump under the sun | Starts reliably on a sagging panel; never browns out the board |
| Mosquitoes and algae | The closed, meshed, opaque tank stays clean through a summer |
| Base | Slab or footing at the first site; the engineer's sign-off with the tank empty |
