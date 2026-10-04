---
format: 1920x1080 (+ 1080x1920 re-layout)
fps: 30
duration: 40.622s (measured from the voiceover by scripts/assemble.mjs)
claim: "Websites, die Appetit machen."
arc: cold open on the answer → three courses → breadth → speed → price → resolution
---

# STORYBOARD: BONTRIVO

## Video direction

**Direction:** „Serviert auf dem O“ (`DIRECTION.md`). The logo's O is a plate seen from
overhead. Everything is served onto it, and in the finale it turns out to be the O of the
wordmark.

**Register map.** Ink `#20201E` for the argument (F01, F07, F08); cream table `#FFF4E7` for
the product (F02–F06, F09). Flips: F01→F02 (iris through the O), F06→F07 (push in the
truck's direction), F08→F09 (hard cut on "Jetzt", the plate descends).

**Palette.** Tomato is the plate, one word per headline, the price, the CTA. Olive is used
only for "fertig/live" (bean, step 3, the inclusion ticks, the bean in the logo). There is
no third colour.

**Motion.** `fromTo` throughout, entrances 0.2–0.38s `power3.out`, overshoot only on state
flips (pill, tick, dot). The serve gesture is always built the same way (`btv.js:serve`):
travel, shadow from lifted to resting, a squash of 0.05s. Nothing is moving at any cut
(checked in the delivered file, v1–v4).

**Camera.** Fixed overhead. Exactly two camera moves: the truck along the table (F06) and
the pull-back to the logo (F09).

**Type.** Montserrat Variable, self-hosted (`assets/fonts/`, OFL). Display 900 in
uppercase, eyebrows 700 tracked at .14em, figures `tabular-nums`.

**Sound.** Room tone at 0.12 instead of a music bed. A porcelain clink climbs through
C5 → C6 → E6 → G6 and resolves as a C chord on the logo. Sub-bass only under „Fertig“ and
under the logo.

**Negative list.** No stock, no faces, no invented numbers, no restaurant-website mock-up,
no portal named, no cursor, no unattributed quote, no 249 €.

## Frames

Times are frame-relative and measured (`audio_meta.json`, sample-exact from the Piper
alignment).

### F01 · 01-claim · 0.000 + 2.789 (hold 2.289)
- **scene**: the site's h1, word by word; the full stop is a tomato dot
- **voiceover**: "Websites, die Appetit machen."
- **register**: argument · **shot**: 1 kinetic type (adapted) · **camera**: locked
- **cues**: Websites,@0.06 → line 1 · die@1.00 → "DIE" · Appetit@1.13 → "APPETIT" (tomato) · machen.@1.54 → line 3 · word end 1.85 → dot
- **transition out**: cut with 0.5 overlap (F02's iris flies over it)

### F02 · 02-served · 2.289 + 5.686
- **scene**: the dot opens into the O; flight through its well onto the table; the plate is served; on „Fertig“ the bean drops into the notch
- **voiceover**: "Mit Bontrivo: Ihre Restaurant-Website. Fertig eingerichtet, ohne technisches Vorwissen."
- **register**: product · **shot**: signature (serve) + held thesis · **camera**: locked
- **cues**: iris 0→0.5 · eyebrow 0.52 (after the iris, still inside „Bontrivo“) · Ihre@1.11 · Restaurant-Website.@1.37 → plate lands · Fertig@2.82 → „FERTIG“ + bean · eingerichtet@3.25 · ohne@4.07
- **sfx**: whoosh-through@0 · clink-c5@1.37 · sub-drop@2.82 · bean-tick@2.84

### F03 · 03-speisekarte · 7.975 + 4.824
- **scene**: course 1 on the same plate (hard cut, the plate does not move)
- **voiceover**: "Mit Speisekarte. Gerichte und Preise, jederzeit selbst aktualisiert."
- **cues**: Speisekarte.@0.22 → icon + headline · Gerichte@1.30 / Preise@2.02 → chips · jederzeit@2.74 → line
- **sfx**: clink-c6@0.24

### F04 · 04-reservierung · 12.799 + 4.116
- **scene**: course 1 cleared (gone by 0.16), course 2 served
- **voiceover**: "Gäste reservieren direkt über Ihre Website. Ohne Umweg über Drittportale."
- **cues**: reservieren@0.30 · direkt@0.80 · Ohne@2.19 → contrast line (no portal named)
- **sfx**: clink-e6@0.32

### F05 · 05-vorbestellung · 16.915 + 2.703
- **scene**: course 3; on „holen“ the plate lifts, on „ab.“ it is carried away (the departure is the content)
- **voiceover**: "Oder bestellen vor, und holen pünktlich ab."
- **cues**: bestellen@0.36 · holen@1.47 → lift · pünktlich@1.72 · ab.@2.15 → out
- **sfx**: clink-g6@0.38 · swish-out@2.13

### F06 · 06-branchen · 19.618 + 6.055 (hold 5.555)
- **scene**: long table, truck at 560 px/s. Each place setting crosses x=1100 on its word, and the last one comes to rest at frame centre
- **voiceover**: "Für Restaurants, Bistros, Bars, Hotels, Cafés, Biergärten und Catering."
- **camera**: truck (camera move 1 of 2) · **cues**: one per Branche (0.19 / 0.94 / 1.67 / 2.26 / 3.12 / 3.89 / 4.55) → icon + label
- **sfx**: table-slide (one texture, not 7 ticks) · **transition out**: push 0.5

### F07 · 07-tage · 25.173 + 4.726
- **scene**: the site's three steps; step 3 turns olive on „Live“; then „TAGE, NICHT MONATE.“
- **voiceover**: "Anfragen. Einrichten. Live gehen. Tage, nicht Monate."
- **register**: argument · **cues**: 0.03 / 1.02 / 1.80 (olive) / 2.08 · Tage,@2.95 · nicht@3.56 · Monate.@3.81
- **sfx**: wood-tick ×2, live-ding@1.80 · **contrast**: the dimmed, spent steps are below 3:1 on purpose (§7 demotion), see FINDINGS

### F08 · 08-preis · 29.899 + 5.871
- **scene**: **RECONSTRUCTION** of the bontrivo.de pricing card from its CSS (×1.6). It shows 4 of the 7 inclusion rows (the ones the voice names). Small print in #55534C/22px instead of #85817A/12.5px so it is legible
- **voiceover**: "Alles inklusive, auch das Hosting. Neunundzwanzig Euro im Monat, bei jährlicher Zahlung."
- **cues**: Alles@0.05 → headline + card · inklusive@0.34 → 3 ticks · Hosting@1.46 → tick 4 · Neunundzwanzig@2.37 → „29,00 €“ · Monat@3.67 → „/ Monat“ · jährlicher@4.45 → „Jährliche Zahlweise — 348,00 € / Jahr, im Voraus fällig“
- **sfx**: pop-soft ×2, price-thunk@2.36 · **transition out**: hard cut

### F09 · 09-cta · 35.770 + 4.852
- **scene**: the plate comes down onto the table from the camera; CTA; pull-back: the letters were always around it; the plate loses its shadow and becomes the logo
- **voiceover**: "Jetzt Website anfragen. Auf bontrivo.de."
- **camera**: descent (scale 6K→K) + pull-back (camera move 2 of 2, origin = centre of the O, so the plate stays the fixed point)
- **cues**: Jetzt@0.05 → descent · anfragen@0.70 → button · 1.30→2.15 pull-back, landing on „bontrivo“@2.15 · 2.30 claim line · Punkt@2.77 → URL · then a 1.8s still poster
- **sfx**: swish-in@0 · chord-c@2.15 · sub-drop@2.15

## Composition check

- [x] Claim inside the first 10 s (it starts at 0.06 s, as text and voice)
- [x] No identical camera move on adjacent frames (locked ×5 → truck → locked ×2 → descent/pull-back)
- [x] Busy and still alternate (F06 is the only dense frame; F07/F08 are argument frames)
- [x] Every register flip is a turn (promise→service, what→how fast, price→resolution)
- [x] Only approved figures on screen: 29,00 € · / Monat · 348,00 € · 1 · 2 · 3
- [x] Runtime 40.6 s (target band 40–50)

## Reconstructions and drawings (so a reviewer can tell a decision from a lie)

- Logo: vectorised from the user's PNG (`tools/vectorize_logo.py`). The ring has a slight
  flat at 9 o'clock from the low-resolution source. The official `bontrivo-mark.svg`
  would fix that.
- Pricing card (F08): rebuilt faithfully from the site's CSS; subset of the rows; small
  print enlarged for legibility.
- Icons: Anwendungsfälle and calendar are verbatim from the site. **Drawn in the site's
  icon idiom:** the cutlery (the site's glyph reads as the letters "PF" at 150 px) and the
  bag (the supplied HTML has no pick-up icon).
