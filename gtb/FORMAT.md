# GO TO BED — block and receipt format, v0

*Draft, 21 Oct 2026 (revised the same day: replies; whisper and shout; the seal covers a fingerprint of the words, so they can fade; times about people kept to the hour). Sized for simple, failsafe operation on the SUNDIAL carrier's ESP32 (no PSRAM, ~2 MB of storage).*

> **Superseded by [stamp-format.md](../stamp-format.md)** (SUNSET's stamp and block format, v1), which builds on this v0 and keeps its blocks, seals and receipts. Kept as written; the [test bed](testbed/README.md) implements v0.

Plain JSON. Every number below is a limit the panel enforces; anything over a limit is refused, never truncated.

## Whispers and shouts

- **Shouts** are the messages below: sealed into the day's block and carried across town.
- **Whispers** are live messages at one wall. They are **not part of this format**: held in the panel's memory, served to phones at that wall, never sealed, never carried, gone at bedtime or on power loss. A whisper has the same `text` limit and may carry `re`.
- **Promotion:** a whisper sent to the town becomes a shout with `p: 1`, timed at the hour it was promoted. Each whisper can be promoted once; it counts against the promoter's shouts.

## Messages (shouts)

```json
{"t": 1784019600, "text": "the sea is flat today"}
{"t": 1784023200, "text": "it was flat here too — Maria", "re": "7/2027-07-13#4"}
```

- `t`: the **hour** the panel received it, by **the panel's clock** (Unix seconds, rounded down to the hour). Phones never set times. Order within the block gives the sequence; nothing needs seconds.
- `text`: up to **140 characters**, plain text, no markup. A name, if any, is just part of the text.
- `re` (optional): the address of the message this one replies to.
- `p` (optional): `1` if this shout was promoted from a whisper (by anyone).
- No author, no key, no phone identifier. Messages are not signed one by one: the panel's seal on the block covers them. **The seal proves where and when a message was written, never who wrote it.** Don't trust anything a message says, including a name.

**Message address** = `panel/day#n`: the block ID, then the message's place in that block's `messages`, counting from 1. Messages are only ever added at the end and anything over a limit is refused, never dropped, so the address a message gets when it is written is final.

**Replies**
- A reply may point at an earlier day at any panel, or at an earlier message today at this panel. The panel checks the address is well formed and in the past; it does **not** check that it holds the message.
- The page shows the replied-to message above the reply if the phone or panel holds it; otherwise "reply to 7/2027-07-13#4 — not here yet". It may arrive with a later walker.
- Replies to replies make threads. One hop between panels takes at least a night.

## Blocks

One block per panel per day, sealed at bedtime.

```json
{
  "v": 0,
  "panel": 3,
  "day": "2027-07-14",
  "seq": 12,
  "prev": "9f2c…",
  "woke": 1784002800,
  "slept": 1784054100,
  "msgs": "c81a…",
  "deliveries": [ {"block": "7/2027-07-13", "t": 1784005200, "rcpt": "4b1e…"} ],
  "sig": "…",
  "messages": [ … ]
}
```

| Field | Meaning |
| --- | --- |
| `v` | Format version |
| `panel` | 1–9 |
| `day` | Local date of the panel's day |
| `seq` | 1 for the panel's first block, then +1 per sealed block (days asleep all day make no block) |
| `prev` | Fingerprint of this panel's previous block (`""` for the first): the chain |
| `woke`, `slept` | When the panel woke and went to bed (panel clock) |
| `msgs` | SHA-256 of `messages` (canonical JSON): the words' fingerprint |
| `deliveries` | The day's first deliveries to this panel: which block arrived, the hour it arrived, and the **fingerprint** of the receipt's secret |
| `sig` | The panel's Ed25519 signature over the **header**: the block without `sig` and without `messages` |
| `messages` | That day's messages written at this panel, oldest first. Outside the signature, but bound to it by `msgs` |

**Header** = the block without `messages`. The seal covers the header, and the header covers the words through `msgs`, so changing a word is caught either way.

**Fingerprint** of a block = SHA-256 of its header as canonical JSON (keys sorted, no spaces, UTF-8), including `sig`. The chain (`prev`) uses it, so the chain survives when the words are gone. Block ID = `panel/day`, e.g. `7/2027-07-13`.

**Why:** the words can fade while the record stays provable. Panels and phones carry whole blocks; anyone who needs to check receipts later keeps headers only.

**Limits**

| Limit | Value | Why |
| --- | --- | --- |
| Messages per block | 60 | A block stays under about 12 KB |
| Shouts per phone per panel per day | 3 (a promotion counts as one) | Flood control; counted by the phone's Wi-Fi address in RAM only, never written to flash or a block, forgotten at bedtime |
| Whispers per phone per panel per day | 30 | Memory only, not in blocks; at most 200 per panel per day |
| Time precision | 1 hour | Messages, deliveries and receipts: a time to the second could tie a person seen at the wall to a message |
| Message length | 140 characters | An art installation, not a forum |
| Reply address | up to 18 characters | Adds about 25 bytes to a message; a full block of replies stays under 14 KB |
| Block size | 16 KB, hard | Refused above this |
| Days a phone carries | the last 3 days of every panel | At most 27 blocks, about 300 KB in browser storage |
| Days a panel keeps | the last 7 days of every panel | At most 63 blocks, about 750 KB of flash |

Older blocks fade out of the network. The chain's fingerprints keep it verifiable; the words do not need to last.

**No moderation.** Nothing is removed or hidden. Fading is the only forgetting: after 7 days a message is gone from every panel, and after 3 days from phones.

## Receipts (bearer stamps)

Issued to the first phone that delivers a block new to this panel.

```json
{"v": 0, "panel": 3, "block": "7/2027-07-13", "t": 1784005200, "secret": "7f3c…a91d", "sig": "…"}
```

- `secret`: 32 random bytes from the panel, hex. **Whoever holds the receipt holds the secret.**
- `t`: the hour of the delivery (rounded down). Who was first is decided by the panel at the moment of delivery, not by the stored time.
- `sig`: the panel's signature over the receipt without `sig`.
- The panel records only `rcpt` = SHA-256 of the secret in its next block, so the chain proves the receipt exists without giving it away.
- One receipt per block per panel: at most 9 blocks × 8 other panels = **72 receipts a day**.

## Checking a stamp (at a spending node)

1. The panel signature is valid (panel public keys are published).
2. SHA-256(`secret`) appears as `rcpt` in a delivery entry of that panel's block for that day, with the same `block`.
3. It is not on the spending node's spent list.

A spending node needs **block headers only**, never `messages`. Headers are enough for all three checks. Stamps are never redeemed for money; they are spent at specialized nodes (first: the auction node).

## Panel keys

Each panel has its own Ed25519 key, generated at installation and kept in the panel's private storage. The nine public keys are published in the repository. A replaced or tampered panel gets a new key; the old key's blocks stay valid up to the replacement date.
