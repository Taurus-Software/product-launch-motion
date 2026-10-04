# FINDINGS: field test of the `product-launch-motion` skill on BONTRIVO

**Task:** "Test the skill with a video for Bontrivo.de" (the domain is `bontrivo.de`).
**Result:** a 40.6 s launch film in two formats (16:9 master, 9:16 re-layout with burned-in
captions) plus SRT, silent cut, poster, stills and loop. Four versions (v1–v4), every
render versioned, raws kept locally.
**Date:** 2026-10-04 · **Renderer:** HyperFrames 0.8.119 · **Environment:** cloud
sandbox with no access to bontrivo.de, Hugging Face or the Whisper CDNs.

## Short verdict

The skill holds up in practice. Its strengths are exactly the steps it calls mandatory:
the truth pass caught three real problems on the site. Voice-first plus measured
durations gave a cut with no estimated number in it. Direction before build produced a
film that does not look like the reference film. "Verify the delivered file" found two
real bugs in its own scripts. Weak spots: the toolchain implicitly assumes 16:9 and
Whisper. Captions and vertical cuts are described but not tooled.

## What the skill demonstrably caught

| Step | Finding in this film |
|---|---|
| Truth pass (law 1) | **249 € means two incompatible things on the site** (setup add-on vs. "one-off instead of monthly"). The testimonial has no author. The gallery is stock. None of the three is in the film. All are reported in `source/SOURCES.md` |
| Truth pass (law 1) | 29,00 € is billed yearly, so the film only shows it together with "348,00 € / Jahr, im Voraus fällig" and says "bei jährlicher Zahlung" |
| Truth pass → direction | No real product UI → no fake restaurant site; the product stays abstracted (direction C) |
| Mechanical rule "inherited direction is killed" | Direction A (= reference film) killed on purpose; the result differs from it on structure, not only colour (see `DIRECTION.md`) |
| Law 9 / step 12 | Master was at **−0.9 dBTP** (target ≤ −1) and **96 kHz**; only measuring the delivered file showed it |
| Self-review (step 13) | v1: two O's on screen at once (F09), umlaut dots peeking out of masks, the site's cutlery icon reads as "PF", shadow on a single letter of the logo · v2: course swaps double-printed (trap 13) · v3: a plate visible ahead of its cue in 9:16 (trap 11 in a new form) |

## Bugs found in the skill, with fix status

| # | Where | Problem | Status |
|---|---|---|---|
| 1 | `scripts/master.sh` | `loudnorm` resamples to 192 kHz; without `-ar` the delivered AAC master was **96 kHz** | **fixed** (`-ar 48000`) |
| 2 | `scripts/master.sh` vs. SKILL.md | Script expects "Peak ≤ −0.8 dBFS"; the definition of done demands "≤ −1 dBTP". A 0.891 sample-peak ceiling delivered −0.9 dBTP after AAC | **fixed**: ceiling 0.841 (−1.5 dBFS), result −1.3/−1.4 dBTP; `references/07` updated to match |
| 3 | `scripts/transitions.mjs` | `push` hardcoded ±1920 px. Wrong in a 1080-wide cut | **fixed**: width read from the index root |
| 4 | `scripts/wire-grade.mjs` | Grain SVG hardcoded at 1920×1080; in 9:16 it covers only the top 56 % | **fixed**: size read from the index root |
| 5 | `scripts/level-sfx.mjs` | The "silent head" check misfires on **swells** (whoosh, riser), whose peak comes late on purpose | open, proposal: a `--swell` mode that reports the peak position instead of warning |
| 6 | `references/03` | Word timings assume Whisper. In sandboxes the model downloads are often blocked. Better and exact for TTS: let the voice report its own alignment (Piper `include_alignments`, sample-exact) | open, proposal: a section "TTS self-alignment" (implementation: `tools/vo.py`) |
| 7 | `references/12` | Captions "from your word timings" are described, but there is no script | open, proposal: promote `tools/captions.mjs` to `scripts/` |
| 8 | Skeleton / references | Vertical cut "re-layout, not crop" is required, but the skeleton has fixed px coordinates and there is no tooling | open, proposal: the `tools/make-vertical.mjs` pattern (per frame: own CSS block + recomputed constants) as a template |
| 9 | `references/10` | Missing traps: (a) `tl.set(…, 0)` is **not rendered** at t=0 (HyperFrames lint `gsap_timeline_set_initial_hide`): initial states belong in CSS/`gsap.set`; (b) a mask reveal at ~108 % lets **umlaut dots** peek out (German!); (c) trap 11 also bites when a re-layout moves a from-position into the canvas | open, proposal: add the three entries |
| 10 | `references/07` vs. direction | "Nothing repeats more than twice" collides with a recurring signature sound | open, proposal: name pitch variation (C5→C6→E6→G6→chord) as the legitimate exception |
| 11 | `references/01` | HyperFrames needs `HYPERFRAMES_BROWSER_PATH` in sandboxes (no Chrome download) and sends telemetry by default (`hyperframes telemetry disable`) | open, proposal: one line in the renderer contract |

## Gates (law 9) and definition of done

| Item | Status |
|---|---|
| Three directions written, two killed, choice documented | ✅ `DIRECTION.md` |
| Signature in one sentence | ✅ "Everything is served on the O, and at the end the plate returns to the logo as its O." |
| Does not look like the examples in the repo | ✅ different on surface **and** structure (table in DIRECTION.md) |
| Only approved figures on screen | ✅ 29,00 € · / Monat · 348,00 € · 1/2/3 |
| Reveals on the word (5 random checks) | ✅ APPETIT, FERTIG+bean, RESERVIERUNG, BARS, 29,00 €: absent 80 ms before the word, present 250 ms after (in the delivered file) |
| Gates: 0 errors with grade · contrast without grade | ✅ 0 errors in both formats. Contrast: 3 warnings on the **deliberately dimmed** spent steps in F07 (§7 demotion), triaged and accepted |
| Nothing moving at a cut | ✅ last frame of every shot extracted from the master and checked |
| Delivered file sampled at the changed beats | ✅ v1–v4, `snapshots/delivered-*` (locally) |
| Loudness of the delivered file −14 LUFS ±0.5, TP ≤ −1 dBTP | ✅ 16:9: −14.1 LUFS / −1.4 dBTP · 9:16: −14.1 / −1.4 (both 48 kHz) |
| Every SFX cue measurably present | ✅ narrow band at the cue frequency, +8 to +42 dB against the window before (clink C5/C6/E6/G6, bean, live, chord) |
| Renders versioned, raws kept | ✅ v1–v4 + raws in `renders/` (not in git) |
| Deliverable set | ✅ 16:9, 9:16 with captions, SRT, silent cut, poster (readable at 200 px), 6 stills, loop |
| Licences | ✅ font OFL · voice dataset CC0 · all sounds self-synthesised · logo/copy/tokens from Bontrivo (supplied by the user) |
| What I would fix next | ✅ see below |

## What I would fix next (honest defect list)

1. **The voice.** Local TTS is audibly synthetic, and Whisper still mishears „Website“
   at times. For publication: a human voice, then re-transcribe (the pipeline is built
   for it).
2. **The logo.** The trace from a 577 px PNG has a slight flat at 9 o'clock on the ring.
   The official `bontrivo-mark.svg` from the site would fix it in a minute.
3. **The 249 € contradiction and the testimonial** need clearing with Bontrivo.
   A named, consenting customer with a photo would be the strongest missing beat
   (shot 9).
4. **Real product UI.** A capture of a real customer site / `app.bontrivo.de` would allow
   one honest demo shot.
5. **Banding** in the large cream light areas (H.264, 8-bit). Fix with a little more grain
   or a 10-bit master.
6. **Unheard.** The mix (room tone, clinks, chord) is measured, not heard; nobody on this
   machine could listen. One listening pass by a human is still due.
7. F08: the price box stands empty for 2.3 s before the price lands. That is deliberate
   (the box waits like a plate), but it can read like a placeholder.
