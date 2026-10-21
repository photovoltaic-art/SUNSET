#!/usr/bin/env python3
"""GO TO BED test bed: simulate a week of the town and write real, signed blocks and receipts.

Nine panels wake and sleep with their own sun. Visitors arrive, write a few messages,
and some walk on to other panels carrying the sealed blocks they hold. Only sealed
blocks travel (a day's messages leave a panel after it has slept once). The first
phone to bring a panel a block it lacks gets a bearer receipt.

Everything here is invented: panel positions, visitor numbers, messages.
Run:  python3 simulate.py [--seed N] [--walk P] [--days D]
Output: out/blocks/*.json, out/receipts/*.json, out/summary.txt, out/freshness.png
"""
import argparse, json, math, os, random, shutil, datetime as dt
import gtb

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--days", type=int, default=7)
ap.add_argument("--walk", type=float, default=0.25, help="share of visitors who walk on to another panel")
ap.add_argument("--round", type=float, default=0.01, help="share of walkers who try the whole round")
ap.add_argument("--rate", type=float, default=6, help="visitors per hour at the central panel")
ap.add_argument("--out", default="out")
a = ap.parse_args()
rnd = random.Random(a.seed)

# ---- the town (invented): positions in metres, centre ~ (0,0); busier near the centre
PANELS = {1: (0, 0), 2: (180, 60), 3: (-150, 120), 4: (60, -200), 5: (320, -40),
          6: (-320, -60), 7: (-80, 380), 8: (520, 260), 9: (-560, -320)}
BUSY = {p: 1.0 / (1 + math.hypot(*xy) / 250) for p, xy in PANELS.items()}   # visitors per hour scale
VISITORS_PER_HOUR_AT_CENTRE = a.rate
WALK_SPEED = 1.1      # m/s
SHADE = {p: (rnd.randint(0, 50) * 60, rnd.randint(0, 80) * 60) for p in PANELS}   # later wake, earlier bed (s)

START = dt.datetime(2027, 7, 12)        # a Monday in July
SUNRISE, SUNSET = 6 * 3600 + 10 * 60, 20 * 3600 + 55 * 60   # Bosa, mid-July, local time
GATE = 40 * 60       # panels start Wi-Fi ~40 min after sunrise, sleep ~20 min before sunset (vertical panel)
DUSK = 20 * 60

PHRASES = ["the sea is flat today", "who has the key to the boat?", "buongiorno da via Roma",
           "music at the river at 9?", "lost: a blue scarf near the bridge", "the bakery is open",
           "anyone walking to the castle?", "first time here", "sun on the walls, no wind",
           "the fishermen are back", "ciao a tutti", "meet at the fountain", "too hot to walk",
           "carrying news from the other side of town", "goodnight, panel"]

keys = {p: gtb.new_key(f"gtb-testbed-panel-{p}".encode()) for p in PANELS}
pubs = {p: gtb.pub_hex(k) for p, k in keys.items()}

def ts(day, sec): return int((START + dt.timedelta(days=day)).timestamp()) + sec
def awake(p, day):
    return SUNRISE + GATE + SHADE[p][0], SUNSET - DUSK - SHADE[p][1]

# panel state
held = {p: {} for p in PANELS}          # (panel, day) -> block   (blocks this panel holds)
chain_last = {p: None for p in PANELS}
sealed = {}
seq = {p: 0 for p in PANELS}
receipts = []
deliveries_today = {p: [] for p in PANELS}
messages_today = {p: [] for p in PANELS}
first_given = {p: set() for p in PANELS}  # block ids already receipted here
stats = dict(visitors=0, missed_asleep=0, messages=0, refused_msgs=0, walkers=0, deliveries=0, rounds_tried=0)
whole_days = []
freshness = {p: [] for p in PANELS}     # per day: number of other panels whose yesterday's block it holds by bedtime
arrivals = {}                            # (block_id, panel) -> time held; for delay stats
phone_sizes = []

def visible_blocks(p, day):
    """Sealed blocks this panel offers to phones: last PHONE_DAYS days."""
    lo = day - gtb.LIMITS["phone_days"]
    return {k: b for k, b in held[p].items() if (dt.date.fromisoformat(k[1]) - START.date()).days >= lo}

def deliver(p, day, t, carried):
    new = 0
    for k, b in carried.items():
        if k in held[p] or k[0] == p: continue
        held[p][k] = b
        arrivals[(f"{k[0]}/{k[1]}", p)] = t
        bid = f"{k[0]}/{k[1]}"
        if bid not in first_given[p]:
            first_given[p].add(bid)
            r, h = gtb.make_receipt(keys[p], p, bid, t)
            receipts.append(r)
            deliveries_today[p].append(dict(block=bid, t=t, rcpt=h))
            new += 1
    stats["deliveries"] += new
    return new

for day in range(a.days):
    date = (START + dt.timedelta(days=day)).date().isoformat()
    events = []
    for p in PANELS:
        w, s = awake(p, day)
        h = w
        while h < s:
            rate = VISITORS_PER_HOUR_AT_CENTRE * BUSY[p] / 3600
            h += rnd.expovariate(rate)
            if h < s: events.append((h, p))
    events.sort()
    visited_today = []   # (visitor route) for whole-day detection
    queue = list(events)
    while queue:
        t, p = queue.pop(0)
        w, s = awake(p, day)
        if not (w <= t < s):
            stats["missed_asleep"] += 1
            continue
        stats["visitors"] += 1
        carried = dict(visible_blocks(p, day))     # phone picks up what the panel holds
        # write messages
        for _ in range(rnd.choice([0, 0, 0, 1, 1, 2, 3])):
            if len(messages_today[p]) >= gtb.LIMITS["msgs_per_block"]:
                stats["refused_msgs"] += 1; continue
            messages_today[p].append(dict(t=int(ts(day, int(t))), text=rnd.choice(PHRASES)))
            stats["messages"] += 1
        # walk on?
        if rnd.random() < a.walk:
            stats["walkers"] += 1
            if rnd.random() < a.round:
                stats["rounds_tried"] += 1
                route = sorted((q for q in PANELS if q != p), key=lambda q: math.hypot(PANELS[q][0]-PANELS[p][0], PANELS[q][1]-PANELS[p][1]))
            else:
                near = sorted((q for q in PANELS if q != p), key=lambda q: math.hypot(PANELS[q][0]-PANELS[p][0], PANELS[q][1]-PANELS[p][1]))
                route = near[:rnd.choice([1, 1, 2, 3])]
            here, tt, path = p, t, [p]
            for q in route:
                tt += math.hypot(PANELS[q][0]-PANELS[here][0], PANELS[q][1]-PANELS[here][1]) / WALK_SPEED + rnd.randint(60, 900)
                wq, sq = awake(q, day)
                if not (wq <= tt < sq):
                    stats["missed_asleep"] += 1; break
                deliver(q, day, ts(day, int(tt)), carried)
                carried.update(visible_blocks(q, day))
                here = q; path.append(q)
            phone_sizes.append(sum(len(gtb.canon(b)) for b in carried.values()))
            if len(set(path)) == len(PANELS): whole_days.append(date)
    # bedtime: seal
    for p in PANELS:
        w, s = awake(p, day)
        seq[p] += 1
        prev = gtb.fp(chain_last[p]) if chain_last[p] else ""
        b = gtb.seal_block(keys[p], p, date, seq[p], prev, ts(day, w), ts(day, s),
                           messages_today[p], deliveries_today[p])
        chain_last[p] = b
        sealed[(p, date)] = b
        held[p][(p, date)] = b
        messages_today[p], deliveries_today[p] = [], []
        # freshness: how many other panels' blocks from yesterday or today does p hold?
        y = (START + dt.timedelta(days=day - 1)).date().isoformat()
        freshness[p].append(sum(1 for q in PANELS if q != p and ((q, y) in held[p] or (q, date) in held[p])))
    # drop blocks older than panel_days
    for p in PANELS:
        for k in list(held[p]):
            if (START.date() + dt.timedelta(days=day) - dt.date.fromisoformat(k[1])).days >= gtb.LIMITS["panel_days"]:
                del held[p][k]

# ---- write out
if os.path.exists(a.out): shutil.rmtree(a.out)
os.makedirs(f"{a.out}/blocks"); os.makedirs(f"{a.out}/receipts")
all_blocks = dict(sealed)
for (p, d), b in sorted(all_blocks.items()):
    json.dump(b, open(f"{a.out}/blocks/{p}_{d}.json", "w"), ensure_ascii=False, indent=1)
for i, r in enumerate(receipts):
    json.dump(r, open(f"{a.out}/receipts/r{i:04d}.json", "w"), indent=1)
json.dump(pubs, open(f"{a.out}/panel_keys.json", "w"), indent=1)

sizes = [len(gtb.canon(b)) for b in all_blocks.values()]
delays = []
for (bid, q), t in arrivals.items():
    p, d = bid.split("/"); b = all_blocks.get((int(p), d))
    if b: delays.append((t - b["slept"]) / 3600)
delays.sort()
def pct(xs, f): return xs[int(f * (len(xs) - 1))] if xs else float("nan")
lines = [
    f"GO TO BED test bed: {a.days} days, 9 panels, seed {a.seed}, {a.rate} visitors/h at the centre, walk share {a.walk}, whole-round share {a.round}",
    f"visitors served: {stats['visitors']}  (walkers who reached a panel already asleep: {stats['missed_asleep']})",
    f"messages written: {stats['messages']}  (refused, block full: {stats['refused_msgs']})",
    f"walkers: {stats['walkers']}  whole rounds tried: {stats['rounds_tried']}  whole days: {len(set(whole_days))} {sorted(set(whole_days))}",
    f"first deliveries = receipts issued: {len(receipts)}  (max possible {72 * (a.days - 1)})",
    f"block size: median {sorted(sizes)[len(sizes)//2]} B, max {max(sizes)} B (limit {gtb.LIMITS['block_bytes']} B)",
    f"phone storage when walking: median {sorted(phone_sizes)[len(phone_sizes)//2] if phone_sizes else 0} B, max {max(phone_sizes) if phone_sizes else 0} B",
    f"delay from bedtime to arrival elsewhere: median {pct(delays, .5):.1f} h, 90% {pct(delays, .9):.1f} h",
    "freshness at bedtime (other panels whose latest block it holds, of 8), by day:",
] + [f"  panel {p} ({'centre' if BUSY[p] > .6 else 'outlying' if BUSY[p] < .4 else 'middle'}): {freshness[p]}" for p in PANELS]
open(f"{a.out}/summary.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for p in PANELS:
        ax.plot(range(1, a.days + 1), freshness[p], marker="o", lw=1.5 if BUSY[p] > .4 else 1, alpha=.9,
                label=f"panel {p}" + (" (outlying)" if BUSY[p] < .4 else ""))
    ax.set_xlabel("day"); ax.set_ylabel("other panels up to date (of 8)"); ax.set_ylim(-0.3, 8.3)
    ax.set_title("GO TO BED test bed: how fresh each panel is at bedtime")
    ax.legend(fontsize=7, ncol=3); fig.tight_layout(); fig.savefig(f"{a.out}/freshness.png", dpi=120)
except Exception as e:
    print("no chart:", e)
