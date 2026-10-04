---
format: 1920x1080 (+ 1080x1920 re-layout)
fps: 30
duration: 40.286s (measured from the voiceover by scripts/assemble.mjs)
claim: "Reservierungen ab jetzt direkt bei Ihnen."
arc: mid-motion open → the break → what is lost → the obvious fix (rejected) → TURN (43 %) → what is yours → price → help → resolution
---

# STORYBOARD: BONTRIVO · Quandoo-Alternative

## Video direction

**Direction:** „Der Weg gehört Ihnen“ (`DIRECTION.md`). A single tomato line IS the
reservation. In the portal world it runs through someone else's box and breaks; at the turn
it runs straight into the O; at the end it coils into the O of the wordmark.

**Register map.** Ink `#20201E` F01–F04 (portal world), cream `#FFF4E7` F05–F09 (own
channel). One flip, at the story turn: F05's cream wipes in left to right with the line.

**Palette and accent budget.** Tomato: (1) the line, (2) the price, (3) the CTA button
(added to the budget during the build: the site's own button colour; it is the only solid
tomato shape apart from the price). Olive: only the bean, twice: when the line connects to
the O (F05) and in the logo (F09). Labels in the ink world are cream / `#A69F97`; in the
cream world ink / `#55534C` / `#85817A`.

**Motion.** Flat, no shadows, no grain, no grade (`wire-grade.mjs` deliberately not run:
DIRECTION "clinical"; film 1 had grain). Lines are drawn by path length against the
playhead (`btv.js: prime/draw`); the head of a line, a travelling folder and the cream edge
are read off the same tween, so they cannot disagree. Entrances 0.26–0.34 s `power3.out`,
no overshoot. Nothing is moving at any cut (checked in the delivered file, all 8 crossings).

**Camera.** None in the frames. The journey is the push chain (02→03, 06→07, 07→08); at
07→08 the flat price line runs straight on into 08's line across the push.

## Frames

Times: start + duration (hold), from `index.html`. Cues are frame-relative (`audio/cues.json`).

### F01 · 01-bruch · 0.000 + 4.019 · ink
Opens mid-motion: the line is already 40 % of the way from „Gast“ to the portal box
(800–1120 × 700–820). It passes through and reaches „Ihr Restaurant“ at 1.53. **„keine“
@1.70:** the segment after the box swings down about the restaurant end and falls away;
the restaurant dims. „SEIT DEM“ @0.05 · „1.“ @0.43 · „OKTOBER“ @0.78 (190 px) · „2026“.
„Quandoo“ appears in the box only on its word @3.13, as plain text. Sound: the portal tone
runs from 0 and ends ON the break (1.72 s asset); snap @1.70; then silence.

### F02 · 02-export · 4.019 + 4.391 (hold 3.891) · hard cut, same stage
„Daten“ @0.29: a folder „Ihre Daten“ surfaces under the box; „exportieren“ @0.63 it travels
a dotted arc to the restaurant (trail and folder from one proxy). „bis“: the date column
turns over (old date out upwards, power2.in); „31.“ @2.12 · „DEZEMBER“ @2.91 · „2026“.
On „Dezember“ the box goes dashed and dim. No sound: the portal world is silent after the
break.

### F03 · 03-leere · 7.910 + 5.918 · push in
„WAS WEGFÄLLT“. Three rows, each on its word: Website-Widget @0.34, Google-Profil @1.83,
Instagram @3.34; each line is drawn out of its label and runs out into a gradient to
nothing (no endpoint). „ALLES LÄUFT“ @4.23 · „INS LEERE.“ @4.90 beside the middle dead
end. Glide-down @4.90.

### F04 · 04-portal · 13.828 + 5.001 (hold 3.751; alive 1.25 s under F05's wipe) · hard cut
Same rows; 03's text dropped on the cut. „nächste“ @0.58: a dashed box; the faded ends
give way and the three lines bend into it; „Nächstes Portal?“ @0.91. „DANN BLEIBT DIE“
@1.84 · „ABHÄNGIGKEIT.“ @2.47: the box sets solid, the same stroke and radius as F01's
portal box. 0.55 s pad: a breath before the turn.

### F05 · 05-direkt · 17.579 + 2.759 · THE TURN
One value f (0→1, 1.22 s, power2.out) drives the cream edge (x = 1920·f) and the line
(guest → O, 184 → 1352): the cream reaches the right edge as the line lands in the ring on
**„direkt“ @1.22**. The claim rises inside the advancing cream (@0.13, uncovered left to
right) and „DIREKT BEI IHNEN.“ @1.22. The bean drops into the notch, landing 1.30 (olive
1/2). „Ihr Restaurant“ @1.74. Sound: wipe-air @0; the own-channel tone enters @0 (fade-in
1.2 s) and carries to F09; connect (G5→C6 bell) @1.22.

### F06 · 06-eigen · 20.338 + 6.256 (hold 5.756) · hard cut, same diagram
„IHRE EIGENE“ @0.51 · „WEBSITE.“ @0.89 · „auf Wunsch unter Ihrer Domain“ @1.75. Speisekarte
@3.63 and Google-Profil @4.61: each line is drawn into the ring, aimed at its centre
(landing at 165° and 150°; the guest line is at 180°). Zip-up on each.

### F07 · 07-preis · 26.095 + 6.941 (hold 6.441) · push in
Right: „FESTER PREIS“ @0.46, the flat line drawn on „fester Preis“, running off the right
edge. Left: „GEBÜHREN PRO GAST“ @1.49, six guests, each with a € coin (staggered to
„Gast“). **„29,00 €“ @2.90** (150 px, tomato) lands on the line, price-thunk; the per-guest
side steps back to 30 %. „/ Monat“ @4.15 · „Jährliche Zahlweise — 348,00 € / Jahr, im
Voraus fällig“ @4.95. No euro figure on the left, no axes, no crossing point: nothing
implies a break-even claim (none is supplied).

### F08 · 08-hamburg · 32.535 + 3.134 · push in, the line continues
„EIN TEAM“ @0.51 · „AUS HAMBURG“ @0.80. On „Hamburg“ @1.00 a pin settles onto the line
under the word (about its tip, so it never passes through the type); pin-tick. „Online, am
Telefon oder vor Ort.“ (site copy) @1.40, under the line. 0.8 s pad: reading time.

### F09 · 09-wechseln · 35.669 + 4.617 · hard cut on „Jetzt“
A piece of line exactly one circumference long travels in along the O's floor and coils
into a circle (visible = [head − C, head]), closes at 1.30, thickens to the ring's real
thickness by „bontrivo“ @1.47, and the traced ring takes over (its notch opens); the bean
lands 1.62 (olive 2/2), the letters fade in from 1.50. „JETZT WECHSELN →“ @0.33 (the one
solid accent shape) · „bontrivo.de“ on „Punkt“ @2.00 · the disclaimer @2.40, verbatim from
the site. Locked still from 2.8; the last frame is the poster. Sound: chord-c (film 1's
resolution, a sonic logo) + sub-drop @1.47, bean-tick @1.62; the own-channel tone's fade
is still sounding under the chord.

## Composition check

- Each frame's content block sits roughly on the vertical centre (v1 had 03/04 60 px
  high and 08 with everything above the line and an empty lower half; fixed in v2).
- Safe margins 150 px left (16:9); the right-most text ends at 1795 px.
- 9:16: text inside x 80–950, nothing below ~1300 except the burned captions at y 1352.

## Reconstructions and drawings (so a reviewer can tell a decision from a lie)

- **No Quandoo assets.** The name is plain text in Montserrat; the box is a generic
  rounded rectangle in the film's own neutral stroke. No logo, no colours, no UI.
- **The portal box, the dashed „Nächstes Portal?“ box, the channel rows** are diagrams,
  not product screens.
- **Icons:** `folder`, `guest` and `pin` are drawn in the site's icon idiom (24 grid, round
  caps) because the supplied HTML has none for these; `arrow` is the site's own.
- **Logo:** vectorised from the supplied PNG (film 1, `tools/vectorize_logo.py`). In F09
  the drawn circle is a stand-in for 0.1 s during the crossfade; the frame that holds is the
  traced logo.
- **The coins** carry no figure: the site gives no per-guest fee („je nach Anbieter“).
