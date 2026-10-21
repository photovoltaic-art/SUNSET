# GO TO BED test bed

A simulated town that produces **real** GTB data: signed blocks, chained per panel, and bearer receipts, in [format v0](../FORMAT.md). Everything else is invented: panel positions, visitor numbers, the messages.

```
pip install cryptography matplotlib
python3 simulate.py                         # busy town: 6 visitors/h at the centre, 25 % walk on
python3 simulate.py --rate 1 --walk 0.15 --out out_quiet
python3 simulate.py --rate 0.3 --walk 0.15 --out out_sparse
python3 verify.py out                       # checks every block and receipt, then runs five attacks
```

| File | What |
| --- | --- |
| `gtb.py` | The format: canonical JSON, Ed25519 signing, sealing blocks, issuing receipts, checks |
| `simulate.py` | Nine panels waking and sleeping at their own times; visitors write messages and some walk on, carrying sealed blocks; first deliveries earn receipts |
| `verify.py` | Signatures, chains, limits, every receipt against the chain; then five attacks that must fail |
| `out*/` | Generated: blocks, receipts, panel public keys, `summary.txt`, `freshness.png` (not in git) |
| `results/` | The three runs' summaries and freshness charts |

**Model, in brief.** Panels wake about 40 minutes after sunrise (plus up to 50 minutes of shade) and sleep about 20 minutes before sunset (plus up to 80 minutes). Visitors arrive at random, more at central panels. Each writes 0–3 messages. A share walk on to 1–3 nearby panels at walking pace, carrying everything their phone picked up; 1 % of walkers try the whole round. Only sealed blocks travel; phones carry the last 3 days; panels keep the last 7.

**Test-bed keys** are derived from public seeds so runs are repeatable. They are not secret and must never be used on a real panel.

**Freshness** (in the chart) = how many of the other eight panels' latest blocks a panel holds at bedtime.

The test bed answers format and incentive questions. It cannot answer whether phones really carry: that is the [carry test](../carry_test/TEST.md).
