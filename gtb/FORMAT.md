# GO TO BED — block and receipt format, v0

*Draft, 21 Oct 2026. Sized for simple, failsafe operation on the SUNDIAL carrier's ESP32 (no PSRAM, ~2 MB of storage).*

Plain JSON. Every number below is a limit the panel enforces; anything over a limit is refused, never truncated.

## Messages

```json
{"t": 1784021220, "text": "the sea is flat today"}
```

- `t`: when the panel received it, by **the panel's clock** (Unix seconds). Phones never set times.
- `text`: up to **140 characters**, plain text, no markup.
- No author, no key, no phone identifier. Messages are not signed one by one: the panel's seal on the block covers them.

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
  "messages": [ … ],
  "deliveries": [ {"block": "7/2027-07-13", "t": 1784006520, "rcpt": "4b1e…"} ],
  "sig": "…"
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
| `messages` | That day's messages written at this panel, oldest first |
| `deliveries` | The day's first deliveries to this panel: which block arrived, when, and the **fingerprint** of the receipt's secret |
| `sig` | The panel's Ed25519 signature over the block without `sig` |

**Fingerprint** = SHA-256 of the block as canonical JSON (keys sorted, no spaces, UTF-8), including `sig`. Block ID = `panel/day`, e.g. `7/2027-07-13`.

**Limits**

| Limit | Value | Why |
| --- | --- | --- |
| Messages per block | 60 | A block stays under about 12 KB |
| Messages per phone per panel per day | 3 | Flood control; counted in RAM, forgotten at night |
| Message length | 140 characters | An art installation, not a forum |
| Block size | 16 KB, hard | Refused above this |
| Days a phone carries | the last 3 days of every panel | At most 27 blocks, about 300 KB in browser storage |
| Days a panel keeps | the last 7 days of every panel | At most 63 blocks, about 750 KB of flash |

Older blocks fade out of the network. The chain's fingerprints keep it verifiable; the words do not need to last.

## Receipts (bearer stamps)

Issued to the first phone that delivers a block new to this panel.

```json
{"v": 0, "panel": 3, "block": "7/2027-07-13", "t": 1784006520, "secret": "7f3c…a91d", "sig": "…"}
```

- `secret`: 32 random bytes from the panel, hex. **Whoever holds the receipt holds the secret.**
- `sig`: the panel's signature over the receipt without `sig`.
- The panel records only `rcpt` = SHA-256 of the secret in its next block, so the chain proves the receipt exists without giving it away.
- One receipt per block per panel: at most 9 blocks × 8 other panels = **72 receipts a day**.

## Checking a receipt (the redeem layer, separate)

1. The panel signature is valid (panel public keys are published).
2. SHA-256(`secret`) appears as `rcpt` in a delivery entry of that panel's block for that day, with the same `block`.
3. It is not on the public spent list.

## Panel keys

Each panel has its own Ed25519 key, generated at installation and kept in the panel's private storage. The nine public keys are published in the repository. A replaced or tampered panel gets a new key; the old key's blocks stay valid up to the replacement date.
