# GO TO BED — carry test

*Draft, 21 Oct 2026. Not yet run.*

**The question:** does a phone's ordinary browser keep what one panel gave it, and hand it to the next panel, with no app?

All GTB panels answer at `http://192.168.4.1`, so the browser treats them as one site. `carry_test.ino` makes one ESP32 act as panel A, then restart as panel B, to test this.

## What you need

- One ESP32 (the ELEGOO board is fine) and a USB cable
- Arduino IDE with the ESP32 core 3.x; flash `carry_test.ino`
- An iPhone and an Android phone (ideally a second Android from another maker, e.g. Samsung + Pixel: the Wi-Fi pop-up differs by maker)
- About an hour, plus a check the next day

## The four paths

| # | Phone | How the page opens |
| --- | --- | --- |
| 1 | iPhone | The Wi-Fi pop-up (sheet) appears by itself |
| 2 | iPhone | Open Safari and type `http://192.168.4.1` |
| 3 | Android | Tap the "Sign in to Wi-Fi network" notification |
| 4 | Android | Open Chrome and type `http://192.168.4.1` |

## Steps (repeat for each path)

1. **Start on A.** The page header shows the panel. If it says B, tap "switch panel" first.
2. **Join `gtb-test-A` and open the page** the way the path says. Expect "nothing to deliver yet", and `A/test` under "This phone carries".
3. **Close the page completely** (Done on the sheet, or close the tab). Rejoin if the phone left the network, and open the page again. `A/test` still listed = **survives close**.
4. **Tap "switch panel".** The board restarts as B in a few seconds.
5. **Join `gtb-test-B` and open the page** the same way. Pass = **carried**:
   - "delivered 1 block(s); new to this panel: 1"
   - "This panel has received" shows `A/test`
   - the phone now carries `A/test` and `B/test`
6. **Next day**, open the page again. Both blocks still listed = **survives a day**.

## Live room (two phones, one panel)

7. **Both phones on the same panel**, page open on each. Type a whisper on one. Within about 3 seconds it should appear under "Here" on the other. Then reply from the second phone. Pass = **live**.

Try it in each path that passed, and mixed (an iPhone in Safari with an Android in Chrome).

## Order and tips

- **iPhone: path 1 before path 2.** After path 1, open Safari *before* clearing anything and look at "This phone carries": that shows whether the sheet and Safari share storage. Then clear it (Settings → Safari → Advanced → Website Data → delete 192.168.4.1) and run path 2 clean.
- **Android: path 3 before path 4**, same check in Chrome, then clear Chrome's site data for 192.168.4.1.
- **Path 2:** when the sheet appears, choose Cancel, then the option to use the network without internet (wording varies by iOS version), so the phone stays joined.
- **Leave mobile data on** (real life). If a path fails, repeat it once with mobile data off and note it.

## Results

One row per path per phone.

| Path | Phone, OS version | Opened by itself? | Survives close | A → B carried | Survives a day | Shares storage with the other path? | Live whispers | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |

## What the results mean

| Outcome | Meaning |
| --- | --- |
| 2 and 4 pass | GTB works. Each panel needs a small sign: "open your browser at 192.168.4.1" |
| 1 and 3 also pass | No sign needed; the pop-up is enough |
| Pop-ups fail, browsers pass | Likely on iPhone; acceptable, use the sign |
| 2 or 4 fails | "The browser is the bag" fails on that phone; rethink before more firmware |

## Second round (after a pass)

Real panels will probably share one Wi-Fi name. Change the sketch to use the same name for A and B, and check that each phone still opens the page at each panel.

## Known limits of the sketch

- Panel B forgets what it received when the board restarts (RAM only). Fine for A → B.
- Whispers are kept in memory, at most 30, and vanish when the board restarts (as on a real panel at bedtime).
- Test blocks are tiny. Size limits are checked separately in the test bed (`../testbed`).
