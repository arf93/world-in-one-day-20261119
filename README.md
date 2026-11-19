# The World in One Day — Thursday, 19 November 2026

Entry for make.fun `news-image-20261119`: one image that sums up the
world's news of Thursday 19 November 2026. A clean newspaper front page
with six verified stories, each with a hand-drawn pictogram, a bold
headline and one factual summary line.

## The six stories

1. **UKRAINE — "CRIMEAN BRIDGE HIT A THIRD TIME"**
   Overnight strike closes the Kerch crossing again; Crimea's
   Russian-installed governor confirms the attack as damage is assessed.

2. **SHENZHEN — "TRUMP, XI AND PUTIN MEET IN SHENZHEN"**
   First-ever trilateral of the three leaders at APEC; nuclear arms and
   Iran on the table, Ukraine left off the agenda.

3. **GAMING — "GTA VI BEGINS GLOBAL ROLLOUT"**
   Rockstar's long-awaited game launches worldwide; players return to
   Vice City on release day.

4. **SAUDI ARABIA — "HOUTHI MISSILE THREAT HITS RIYADH"**
   Saudi-led coalition says it dealt with a missile threat over the
   capital; debris fell and damage was reported, then the all-clear
   sounded.

5. **BANGLADESH — "BANGLADESH BRACES FOR LOCKDOWN"**
   Paramilitary troops deploy nationwide as unrest grows over ex-PM
   Hasina's planned return; blasts and arson blamed on her banned party.

6. **CLIMATE — "COP31 ENTERS FINAL STRETCH"**
   New draft text expected in Antalya as the climate summit nears its
   Friday close; IEA releases its World Energy Outlook.

## Sources

Reuters · Al Jazeera · The Hindu BusinessLine · Oil Change International · UN

## Files

- `render.py` — draws the whole page with Python 3 + PIL and writes
  `entry.png` (1024×1024, ≤ 1 MiB).
- `main.ts` — Node 22 entrypoint (standard library only). Copies
  `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`), after
  validating the PNG magic bytes and confirming the copy is byte-identical.
- `entry.png` — the rendered front page.
- `LICENSE` — MIT.

## Run

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
