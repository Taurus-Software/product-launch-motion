# SCRIPT: BONTRIVO · Vorbestellen & Abholen (Pipeline step 4)

Written for the ear and for a split screen: each line belongs to one side of the counter
(guest or team), except the opening, the claim and the price, which are set across it.
Single source for voice, captions and timings: `tools/script.json`.

**Voice direction (overall):** calm and precise, like a good pass at service. No urgency:
the time is a promise kept, not a countdown.

| # | Line (on screen / captions) | Side | Delivery |
|---|---|---|---|
| 01 | Vorbestellen und abholen, ganz einfach. | across | the site's headline, light |
| 02 | Ihre Gäste bestellen vor, direkt über Ihre Website. | guest | „vor“ is the order |
| 03 | Ihr Team sieht die Bestellung in Echtzeit. | team | „Echtzeit“ lands the mirror |
| 04 | Und steuert die Abholzeit. | team | short, decisive |
| 05 | So holen Ihre Gäste pünktlich ab. | guest | „pünktlich“ is the signature beat |
| 06 | Weniger Wartezeit, mehr zufriedene Gäste. | guest · team | the site's sentence, split across |
| 07 | **Einfach für Gäste. Einfach für Ihr Team.** | guest · team | **the claim**, verbatim (menu teaser of the pickup page) |
| 08 | Wir richten die Vorbestellung für Sie ein. In wenigen Tagen live. | team · guest | reassurance |
| 09 | Vorbestellung inklusive. Neunundzwanzig Euro im Monat, bei jährlicher Zahlung. | across | price clear, honesty line without dropping |
| 10 | Jetzt Website anfragen. Auf bontrivo.de. | across | the sign-off |

Approved figures only (`BRIEF.md`): 29,00 € spoken, 348,00 € on screen beside it. No
clock time, no count of orders or minutes, no payment, no device.

## Voice (step 5)

As in films 1–2: local Piper `de_DE-thorsten-high` (CC0 dataset),
`length_scale 1.04 · noise 0.6 · noise_w 0.7`; raw IPA for „Website“ (`[[vˈɛpsaɪt.]]`, full
stop inside the block) and „live“ (`[[lˈaɪf.]]`).

**Line 10 is film 1's take, reused.** Same sign-off, already ASR-checked; reusing it keeps
the brand's last words identical across films 1 and 3, and its word timings come with it
(`transcripts/10-anfragen.json`).

**Take selection:** 8 takes per line, blind Whisper-small transcription (sherpa-onnx), best
transcript wins. All nine new lines were recognised word for word by the best take (09
scores 0.889 only because the transcript writes „29“ for „Neunundzwanzig“). Scores and
transcripts in `transcripts/*.json`.

**Word timings (step 6):** from the synthesis itself (Piper alignment, sample-exact).
Measured lengths: 01 2.566 · 02 2.775 · 03 1.950 · 04 1.533 · 05 2.020 · 06 2.961 ·
07 2.399 · 08 3.723 · 09 4.884 · 10 3.552 s (28.4 s of voice in a 37.6 s film).

> For publication: a human voice. Pipeline unchanged (wav + word timings).
