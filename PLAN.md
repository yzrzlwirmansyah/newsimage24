# PLAN — news-image-20261124

Competition: news-image-20261124 — "Sum up 24 November's world news in one image", $100, program/v1.
Build turn: t1 recon + anchor (this turn only — no main.py written, nothing committed beyond init).

## Anchor

makefun anchor 6b9d73038e5d9919134bb0d24dade4946a71746e round 34235724

(Printed by `makefun init` in the empty repo dir, before any other write.)

## Repo

- Local: /home/hatch/workspace/makefun/newsimage24
- GitHub: https://github.com/yzrzlwirmansyah/newsimage24 (fresh, public, created 24 Nov 2026)
- Remote: origin = https://github.com/yzrzlwirmansyah/newsimage24.git (added, NOT pushed yet)
- Local git identity: user.name = user.email = 3PzMbJEm38BnNzmedWJY5GuJQRGytFGWBQcHEzdn4QtE
- License: MIT (committed by init: c8479a4 LICENSE: MIT; 6b9d730 makefun anchor: drand round 34235724)
- Entry: Python 3.13 stdlib-only `main.py` at repo root, writing one deterministic 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png), ≤1 MiB, byte-identical across two runs.

## Verification (fresh searches, 24 Nov 2026, ~16:00 WIB)

All six coordinator stories confirmed in fresh reports today. Timing note for
faithfulness: several were announced Monday 23 Nov (US/Europe time) and dominate
Tuesday 24 Nov coverage — the labels below never claim a story "happened today",
only what happened, as reported. No story was contradicted; none dropped.
Swap candidates checked and NOT used: the UN Libya probe (UNSMIL statement was
early Monday 23 Nov) and the Houthi Hodeidah claim (strikes Monday 23 Nov,
unverified by AFP, Saudi silent) are both older than the Grok suits and weaker.

1. DRONE OVER POLAND — confirmed. Overnight 23→24 Nov, Russian jet-powered
   reconnaissance drone (Geran-5, cameras) entered near Dorohusk, flew ~20 km
   to Chelm, ~9 minutes inside; tracked by three Polish air-defence systems;
   shootdown authorised but held back over civilian risk; turned back east.
   Follows 3 Russian Kh-101 missiles landing in Poland on 20 Nov; NATO
   emergency meeting 23 Nov; AWACS to be deployed to Poland.
2. ZELENSKY FOUR-WAY TALKS — confirmed. Spoke by video to NATO lawmakers in
   Berlin on Monday; called for Ukraine, Europe, America and Russia to meet
   "as soon as possible", "literally tomorrow" (Tuesday 24 Nov); partners
   aim for before Christmas. First reported widely 24 Nov (France 24, 01:30 UTC).
3. MEGASPEED BLACKLISTED — confirmed. US Commerce/BIS put Megaspeed
   International (Singapore) plus six affiliates (MSFusion, PT Megaspeed
   International, Speedmatrix, Apex Enterprise Solutions, Swiftdata,
   Megaspeed Thailand) on the Entity List on Monday, over alleged diversion
   of Nvidia AI chips to China; licences now required, presumed denied.
4. NEPAL QUAKE — confirmed. Tuesday morning 24 Nov, ~07:02–07:17 local,
   Taplejung district, Koshi Province, near Olangchung Gola / Nepal–Tibet
   border. Nepal's centre: magnitude 5.6; USGS/EMSC: 5.3. Tremors felt in
   India, Bhutan, Bangladesh, China. No casualties or major damage reported.
5. STATES SUE SPACEX OVER GROK — confirmed. Oregon (filed 22 Nov) and
   Virginia (filed 23 Nov) sued SpaceX / SpaceX Super Intelligence (ex-xAI)
   on Monday, alleging Grok was marketed as safe while generating
   non-consensual sexualised images of real people, including children;
   consumer-protection claims, penalties and injunctions sought. Allegations,
   not findings; SpaceX has not commented.
6. EU CUTS BANKS FROM SWIFT — confirmed. Von der Leyen presented the 22nd
   Russia sanctions package in Strasbourg on Monday 23 Nov: transaction ban
   extended to ~60 Russian banks, all to be removed from SWIFT; also crypto
   crackdown, 70+ shadow-fleet vessels, visa/sports bans. Proposal only —
   needs unanimous Council approval.
- TICKER (markets) — confirmed. Monday's Wall Street rally, reported 24 Nov:
  S&P 500 +4.7% (7,237), Nasdaq Composite +6.5% (24,090; Nasdaq 100 +6.9%),
  Nikkei +3.9% (58,654), Brent $86.68 (fell 3.6% Monday). Rally driven by
  Jensen Huang's return as Nvidia CEO (Nvidia +31%).

## FINAL 6 LABELS (exact spelling — use verbatim in main.py)

Masthead: THE WORLD TODAY — TUESDAY 24 NOVEMBER 2026

1. LEAD — RUSSIAN DRONE OVER POLAND
   Recon drone enters Polish airspace near Dorohusk; tracked, not shot down
2. FOUR-WAY TALKS URGED
   Zelensky: Ukraine, Russia, US and Europe should meet as soon as possible
3. US BLACKLISTS MEGASPEED
   Singapore chip firm and six affiliates put on Entity List over Nvidia chips
4. QUAKE SHAKES NEPAL
   Magnitude 5.6 tremor hits Koshi Province near the China border
5. STATES SUE SPACEX OVER GROK
   Oregon and Virginia sue over Grok's sexualised images of real people
6. EU CUTS 60 BANKS
   Von der Leyen proposes 22nd sanctions package cutting banks from SWIFT

Ticker strip: MARKETS RALLY: S&P 500 +4.7%  NASDAQ +6.5%  NIKKEI +3.9%  BRENT $86.7

## Layout plan (1024x1024 newspaper front page)

- Canvas 1024x1024, off-white paper background, thin black outer border.
- Masthead band (top, ~0–110 px): "THE WORLD TODAY" in large bold capitals,
  centred; below it a rule line and the dateline "TUESDAY 24 NOVEMBER 2026"
  centred, smaller; thin double rule under the masthead.
- Lead panel (~y 120–560, full width): big drawn scene — night sky, Polish
  border landscape, a drone silhouette with camera, radar dishes and a
  "HELD FIRE" style cue kept purely visual (no extra words); headline
  "RUSSIAN DRONE OVER POLAND" large, subhead one line below, in a caption
  strip at the panel's foot.
- Grid of 5 smaller panels (~y 570–940): two rows — row 1 has 3 panels
  (talks / Megaspeed / quake), row 2 has 2 panels (Grok suit / EU banks)
  plus a small filler? No filler: make row 2 three cells too, with the
  third cell a compact "ALSO" mini-list? Simpler: 5 panels in a 3+2 grid,
  each ~330x180, each with a small drawn scene on top, headline + one-line
  subhead below. Scenes: four flags/table for talks; chip + "NO ENTRY" stamp
  for Megaspeed; cracked mountains for the quake; gavel + phone screen for
  Grok; bank building + cut cable for SWIFT.
- Bottom ticker strip (~y 950–1010): dark band, white text, the market
  ticker line above, single line, legible at 300 px.
- All text uppercase in the bitmap font; keep every label short; no text
  smaller than ~11 px tall; check legibility at 300 px after render.

## Drawing technique (pure stdlib, deterministic)

- Python 3.13, standard library only: zlib + struct to encode the PNG by
  hand (IHDR, IDAT with zlib.compress level 9, IEND, CRC32 per chunk).
- Canvas: bytearray of RGB triples, 1024x1024; helpers: fill_rect,
  draw_rect (outline), line (Bresenham), circle (filled/outline),
  ellipse, polygon (scanline fill), triangle; colours as fixed tuples.
- Small built-in bitmap font: hand-drawn 5x7 (uppercase A–Z, digits 0–9,
  and punctuation . , : % + $ / ' - ( ) &) stored as tuples of row bitmasks
  in the source; text drawn by scaling the glyphs (scale 2–4) with
  draw_text(x, y, string, scale, colour); word-wrap subheads to fit panel
  width by measuring with the same font metrics.
- Scenes drawn only with the primitives above (no images, no fonts from
  disk, no network, no file reads besides main.py itself).
- Output: write PNG bytes to $MAKEFUN_OUTPUT_DIR/entry.png
  (default /output/entry.png); create the directory if needed.
- Determinism: no random, no time, no os.urandom, no dict-order dependence
  on hashes, no environment reads; fixed colour palette and fixed geometry;
  same bytes on every run. Verify by running twice and comparing sha256.

## Determinism / gate notes

- PNG ≤ 1 MiB, exactly 1024x1024; run twice locally, sha256 must match.
- No network, no imports beyond stdlib (zlib, struct, os, sys only).
- Do NOT copy code from newsimage22/main.py or newsimage23/main.py —
  write main.py fresh in turn 2 (type it out in full); the design above is
  the reuse, the code is new.
- Next turns: t2 write main.py (run `makefun init` again first in the repo),
  t3 test + render + visual check, t4 revise, t5 commit + push.
