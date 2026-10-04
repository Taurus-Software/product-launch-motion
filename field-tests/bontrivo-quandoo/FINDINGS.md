# FINDINGS: second field test of the `product-launch-motion` skill (BONTRIVO · Quandoo-Alternative)

The second film made with the skill for the same brand, after `../bontrivo/` (film 1).
What this test adds: a second film for the same brand (the skill's
anti-sameness rule now has a precedent to beat), a claim about a **third party** (a
competitor shutting down), and a film whose design lives in SVG path geometry rather than in
DOM boxes.

## Short verdict

The skill holds up a second time, and the second film is structurally different from the
first (DIRECTION.md, table against both references): mid-motion open instead of a cold
open on the claim, a late turn (43 %) instead of none, flat diagram instead of overhead
depth, no grain, a push-chain journey instead of a fixed camera, a sound that stops instead
of one that recurs. The truth pass did real work: two claims were verified independently,
one (existing bookings) was dropped because the sources disagree. Two skill-level bugs were
found and fixed (mastering, line drawing), and the field tool `captions.mjs` was fixed.

## What the skill demonstrably caught

- **A claim that would have been false the next day.** The obvious beat, "Noch 89 Tage",
  was refused by the approved-figures rule (BRIEF), and the whole countdown direction (B)
  was killed by question 3: every competitor runs the same countdown right now.
- **A third-party claim that the sources disagree on.** Bontrivo: "Über Quandoo laufen weder
  neue noch bestehende Buchungen." The press reports say existing bookings stay with the
  restaurants. The film says neither (`source/SOURCES.md`).
- **The competitor rule.** "No competitor named on screen" could not be kept, because the
  shutdown IS the subject. The skill made this a documented exception (BRIEF, negative
  list: factual naming, no logo or colours, the site's disclaimer, UWG §6 check before
  publication) instead of a silent break.
- **Anti-sameness against the skill's own last output.** Film 1's vocabulary (plate,
  serve, shadow, clink scale) was banned for film 2 up front; nothing of it is reused
  except the brand chord, kept on purpose as a sonic logo.
- **Law 9 again.** Gates were green on v1 while the frame showed: 03/04 sitting 60 px high,
  08 with an empty lower half and a pin far from its word, a line grazing a label in 06,
  guests too small to read as people in 07, and a 1-px tick at an undrawn line's origin.
  All fixed in v2 by looking at the delivered frames.

## Bugs found in the skill, with fix status

| # | Where | Problem | Status |
|---|---|---|---|
| 1 | `scripts/master.sh` | `loudnorm … linear=true` is only a request: if measured peak + gain would exceed TP, ffmpeg **silently switches to dynamic mode**, which on a sparse, voice-led film lands short and squeezes the LRA. Film 2 v2: raw −15.9 LUFS / −1.45 dBTP → delivered **−14.9 LUFS** (LRA 4.0 → 2.6). Film 1's raw was in the same situation (needed +2.6 dB), it just landed closer by luck (−14.1). | **fixed**: the script now predicts the mode (af_loudnorm's own condition) and, when linear is impossible, applies the one gain itself and lets the existing limiter take the transients. Film 2: −14.1 / −1.3 dBTP, LRA 3.5. Film 1 re-mastered as a check: −14.2 / −1.3. Header note 6. |
| 2 | drawn lines (`btv.js`, the pattern references/04 describes for strokes) | A primed line with `dasharray L, L+2` and `dashoffset = L` paints a **1-px tick at its origin** before it is drawn: the dash's end sits exactly on the path's start. Found at 06's Google-Profil line, visible from frame 0 of the shot. | **fixed** here (dash over L+1, offset (L+1)·(1−f)); proposal: one line in `references/10` traps |
| 3 | `tools/captions.mjs` (field tool, proposed for `scripts/` in film 1's #7) | (a) An ordinal („31.“) counted as a full stop: one card ended „… bis zum 31.“, the next was „Dezember.“; (b) „?“ did not end a clause: „… Portal? Dann bleibt die“ / „Abhängigkeit.“; (c) greedy filling left „über Quandoo.“ alone on a one-second card. | **fixed** in film 2's copy: ordinals excluded, `?!` added, overlong cards split at the most balanced word boundary, never after a short function word. Film 1's SRT is unaffected (no ordinals, no questions). Promote this version. |
| 4 | HyperFrames layout check | Flags `content_overlap` between an outgoing frame and the incoming frame's text during a **clip-path wipe**, although the incoming frame's ground covers the outgoing one wherever its text is visible (the check does not model clip-path occlusion). | worked around with `data-layout-allow-overlap` on the three elements, with the reason in a comment (`05-direkt.html`); proposal: a note in `references/10` |
| 5 | `references/12` / vertical tooling | In a film whose layout is SVG path data, a 9:16 re-layout is mostly **string patches of geometry**. The film-1 pattern (CSS block + a few constants) does not reach path data; a patch that silently misses is the main risk. | done here: `tools/make-vertical.mjs` throws on any missing patch target; proposal: make "every patch must hit" part of the template |
| 6 | `references/10` (new trap) | A headline whose two words rise separately must get **one mask per line** once it wraps (9:16): in a shared two-line mask, the first word's hidden state (yPercent 135) sits in the second line's slot and is visible before its cue. | avoided by construction (`split()` in make-vertical.mjs); proposal: add the trap |

Still open from film 1 and confirmed again here: #5 (level-sfx swell mode), #6 (TTS
self-alignment docs: used again, sample-exact), #7 (captions script), #9 (traps), #11
(HyperFrames env/telemetry note).

## Gates (law 9) and definition of done

| Item | Status |
|---|---|
| Three directions, two killed, choice documented | ✅ `DIRECTION.md` (A inherited and killed, B countdown killed) |
| Signature in one sentence | ✅ „Die Reservierung ist eine Linie. Sie reißt beim Portal, und sie schließt sich zum O von BONTRIVO.“ |
| Different from the reference film AND from film 1 | ✅ structure table in DIRECTION.md; every structural axis differs from film 1 |
| Only approved figures on screen | ✅ 1. Oktober · 31. Dezember · 2026 · 29,00 € · 348,00 € |
| Third-party claims verified independently | ✅ Tageskarte, gastro.news, t-online (`source/SOURCES.md`); one claim dropped |
| Gates | ✅ 0 errors, 0 warnings (16:9); 9:16: 0 errors, 1 warning (caption track density, as film 1); contrast 24/24 and 28/28 WCAG AA |
| Root/clip durations = wrapper durations (trap 4) | ✅ `tools/check-durations.mjs`, 9/9 |
| Reveals on the word (5 checks in the delivered file) | ✅ `tools/verify.py`: „31.“ +23 ms · „INS LEERE.“ +57 ms · „DIREKT BEI IHNEN.“ +35 ms · price +40 ms (first changed frame) · pin −33 ms (frame it comes to rest) |
| Every SFX cue measurably present | ✅ `tools/verify.py`, own band, 150 ms after vs before: +13.6 to +43.9 dB on all 9 cues; the portal tone measurably **stops** on the break (−6.6 dB) |
| Nothing moving at a cut | ✅ 8/8 crossings + the end hold, from the master |
| Hard cuts hold the diagram | ✅ 03→04 and 05→06: 0 changed pixels outside the dropped text; 01→02: 20 px (codec noise) |
| Loudness of the delivered files | ✅ 16:9 −14.1 LUFS / −1.3 dBTP · 9:16 −14.1 / −1.3 · 48 kHz |
| Renders versioned, raws kept | ✅ v1, v2 (16:9), 9:16 v1, v2 in `renders/` (not in git) |
| Deliverable set | ✅ 16:9, 9:16 with burned captions, SRT, poster, 9 stills, loop, YouTube texts |
| Licences | ✅ font OFL · voice dataset CC0 · all sounds self-synthesised (`tools/sfx.sh`) · logo/copy/tokens supplied by the user |

## What I would fix next (honest defect list)

1. **Legal check before publication.** The film names Quandoo (deliberate exception,
   BRIEF). Comparative advertising (UWG §6) has to be checked by someone qualified. Same
   for the YouTube title and description.
2. **Expiry date: 31 December 2026.** After the export deadline, F02 is false. Take the
   film down or re-cut F02.
3. **The voice.** TTS placeholder; „Quandoo“ is heard as „Quandu“ by the blind ASR. A
   human voice for publication.
4. **Unexplained 1-px ticks at the 02→03 push seam** for about two frames (a tomato and a
   grey hairline at the frames' common edge). Not found in the frames' content;
   sub-perceptual at 30 fps, but unexplained, so it is listed.
5. **Unheard.** The mix is measured, not heard. One listening pass by a human is due,
   especially the snap → silence at 1.7 s, which carries the first half.
6. **The diagram's restraint is a risk** (DIRECTION named it): if the line reads as
   decoration, the first half reads as a chart. A test with three restaurant owners muted
   on a phone would answer it.
