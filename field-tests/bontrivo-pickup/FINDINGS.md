# FINDINGS: third field test of the `product-launch-motion` skill (BONTRIVO · Vorbestellen & Abholen)

The third film for the same brand, after `../bontrivo/` (film 1) and `../bontrivo-quandoo/`
(film 2). What this test adds: a single-feature film with thin sources (one paragraph on
the supplied pickup page), a direction killed by law 10 because the skill's own earlier
films had become a house style, stereo as a design dial, and a 9:16 cut produced from the
same frame files instead of by patching.

## Short verdict

The skill produced a third film that differs from both predecessors on every structural
axis (DIRECTION.md, table against three references): space instead of time as the register
switch (cream and ink side by side, all film), a locked stage with hard cuts only, a
convergence beat (the bag crosses the counter on „pünktlich“) instead of a turn, an ending
that assembles the mark across the seam instead of transforming something into its O, and
a sound design built on stereo position. The truth pass kept the film honest with very
little source material: no ordering UI, no device, no payment, no figures.

## What the skill demonstrably caught

- **Its own house style.** The strongest-looking idea, „the O is a clock, the bean its
  hand“, was killed by law 10: it would have been the third film in a row whose device is
  the logo's O turning into something (plate, ring, clock).
- **Thin sources, no invention.** The pickup page says what happens (order ahead, real
  time, pickup time controlled, on time), not how. The film shows only the what: a guest,
  an order tag, a team, a clock without numerals, a bag. „Zahlungssystem“ is a separate
  solution; whether it is in the 29,00 € package is not stated, so it is not in the film.
- **A truth question about film 1.** Film 1's „holen pünktlich ab“ was re-checked against
  the supplied pages before reuse: it is verbatim from the pickup page (`source/SOURCES.md`).
- **Law 9 again.** Gates were green on v1 while the frames showed: a pulse ring visible on
  the team's side before the order had arrived, and the wordmark's halves showing each
  other's letters, swapped („TRIVO … BONT“), from the frame's first instant. Both fixed in
  v2 by looking. The delivered-file checks then found a ratchet only +4 dB over the voice
  and a swish whose pan did not read in its second half; fixed in v3 by measurement.

## Findings for the skill

| # | Where | Finding | Status |
|---|---|---|---|
| 1 | `references/12` / vertical tooling | A frame can carry BOTH layouts: the 9:16 rules under `#root[data-width="1080"]` (HyperFrames scopes `#root` per composition, the attribute selector survives), plus the few timeline numbers read from the declared size (`split.js: SP.geo`). The 9:16 cut is then a copy with the root size swapped (`tools/make-vertical.mjs`, 30 lines) instead of films 1–2's string patching of CSS and SVG geometry. | done here; proposal: make it the skeleton's default |
| 2 | `scripts/wire-audio.mjs` / `references/07` | Stereo works end to end (the renderer keeps stereo sources as stereo, mono ones centred), but cues have no `pan`; the panning has to be baked into each asset (`tools/sfx.sh`), and a moving pan is a two-expression source. | proposal: a `pan` (and `panTo`) field per cue |
| 3 | verification | `tools/verify.py` now measures L/R energy per cue in the delivered file (guest cues left, team cues right, 7–14 dB apart; the swish R then L) and the signature directly (the bag's centroid at the frame of „pünktlich“: x 964, seam 960). | proposal: a stereo mode for `verify-cue.sh`; promote `verify.py` (cue bands, sync onset/settle) to `scripts/` |
| 4 | `references/10` (trap 11, again) | Third occurrence of the same GSAP trap: a `fromTo` that starts after t=0 paints its from-state at t=0 unless `immediateRender: false` (film 1: the serve; film 3: the pulse ring at opacity 0.8). | proposal: state the trap as a rule: any `fromTo` with a visible from-state and a start > 0 |
| 5 | sync verification | A frame-to-frame mean change misses the easing tail of a thin moving line (the clock hand read −136 ms, then +464 ms with codec flicker). Comparing every frame to the settled final frame measured +31 ms. | done in `tools/verify.py`; same proposal as #3 |
| 6 | HyperFrames layout/contrast audit | Two-colourway objects (one copy per half, clip-path) are reported as `content_overlap` (fixed with `data-layout-allow-overlap`, documented by HyperFrames) and once as a contrast failure „1:1“ (the cream copy measured against the cream ground, although it is only visible over ink). Also a hidden-by-mask transient in 9:16 (one sample). Same root cause as film 2's wipe: the auditor does not model clip-path or overflow masks. | triaged and documented; proposal: one line in `references/10` |
| 7 | pattern | A locked stage across hard cuts is safest when the persistent parts are generated once (`tools/frames.py`): measured 0 changed pixels across 02→03 and 05→06. | proposal: mention the pattern for „stage films“ in the references |
| 8 | `scripts/master.sh` (film 2 fix) | Used again: the raw needed +3.7 dB, linear was impossible, the gain + limiter path delivered −14.2 LUFS / −1.1 dBTP (16:9), −14.2 / −1.3 (9:16). | confirmed |

## Gates (law 9) and definition of done

| Item | Status |
|---|---|
| Three directions, two killed, choice documented | ✅ A inherited (killed), B „Die Uhr im O“ (killed, law 10), C chosen |
| Signature in one sentence | ✅ „Zwei Seiten, eine Zeit: Die Tüte geht genau zur gesetzten Minute über die Theke.“ |
| Different from the reference film, film 1 AND film 2 | ✅ structure table in DIRECTION.md |
| Only approved figures on screen | ✅ 29,00 € · / Monat · 348,00 € (no clock numerals) |
| Gates | ✅ 16:9 and 9:16: 0 errors; 1 triaged contrast warning each (#6); 9:16 also the caption-track density warning (as in films 1–2) |
| Root/clip durations = wrapper durations (trap 4) | ✅ `tools/check-durations.mjs`, 10/10 |
| Reveals on the word (7 checks in the delivered file) | ✅ +22 to +65 ms for onsets; hand settles +31 ms on „pünktlich“; mark settles −25 ms on „bontrivo“ |
| The signature, measured | ✅ bag centroid x 964 at the „pünktlich“ frame (seam 960) |
| Every SFX cue measurably present | ✅ 8 cue bands +6.8 to +39.1 dB (v3) |
| Stereo device measurably present | ✅ 8 pan checks: left/right as designed, 7.3 to 13.8 dB |
| Nothing moving at a cut | ✅ 9/9 crossings + end hold |
| Loudness of the delivered files | ✅ 16:9 −14.2 LUFS / −1.1 dBTP · 9:16 −14.2 / −1.3 · 48 kHz stereo |
| Renders versioned | ✅ 16:9 v1–v3, 9:16 v1–v2 in `renders/` (not in git) |
| Deliverable set | ✅ 16:9, 9:16 with burned captions, SRT, poster, 10 stills, loop, YouTube texts |
| Licences | ✅ font OFL · voice dataset CC0 · all sounds self-synthesised · logo/copy/tokens supplied by the user |

## What I would fix next (honest defect list)

1. **The voice** is a TTS placeholder; record a human voice for publication.
2. **Stereo collapses on a phone speaker.** The device is a bonus for headphones and
   stereo speakers; the film does not depend on it (the split carries visually), but in a
   mono feed the tap-l / tap-r pair is just two taps.
3. **F07 → F08 are two type-only frames in a row.** The claim needs its bare stage; F08
   could get a small visual (it has none the sources would support).
4. **The receipt glyph** may read as „invoice“ rather than „order“ to some viewers.
5. **The clock is a time-lapse**: the hand travels 105° in a second. Intended, but it is a
   compression of real time a viewer may not read as such.
6. **Unheard.** The mix is measured, not heard. One listening pass on headphones is due.
