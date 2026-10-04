# SCRIPT: BONTRIVO · Quandoo-Alternative (Pipeline step 4)

Written for the ear, problem first and deliberately long (DIRECTION: the turn at ~45 %), the
claim verbatim at the turn, numbers written as they are said. Single source for voice,
captions and timings: `tools/script.json`.

**Voice direction (overall):** factual and calm in the first half (a date, not an alarm),
warmer after the turn. No urgency in the voice; the dates carry it.

| # | Line (on screen / captions) | Delivery |
|---|---|---|
| 01 | Seit dem 1. Oktober laufen keine Reservierungen mehr über Quandoo. | a fact, by date; no drama |
| 02 | Ihre Daten exportieren Sie nur noch bis zum 31. Dezember. | the one deadline that is still open |
| 03 | Das Widget auf Ihrer Website, der Link im Google-Profil, bei Instagram: Alles läuft ins Leere. | a list, then the consequence |
| 04 | Einfach das nächste Portal? Dann bleibt die Abhängigkeit. | the obvious fix as a question, the answer flat |
| 05 | Reservierungen ab jetzt direkt bei Ihnen. | **the claim**, verbatim from the CTA headline of all three pages |
| 06 | Auf Ihrer eigenen Website, auf Wunsch unter Ihrer Domain. Mit Speisekarte und Google-Profil. | what "bei Ihnen" means |
| 07 | Ein fester Preis statt Gebühren pro Gast. Neunundzwanzig Euro im Monat, bei jährlicher Zahlung. | price clear, honesty line without dropping |
| 08 | Und ein Team aus Hamburg hilft beim Umstieg. | the answer to "effort before Christmas" |
| 09 | Jetzt wechseln. Auf bontrivo.de. | the site's own CTA |

Approved figures only (`BRIEF.md`): 1. Oktober, 31. Dezember, 29,00 € (spoken), and on
screen 348,00 € beside it. No countdown, no savings figure, nothing about data migration or
existing bookings.

## Voice (step 5)

As in film 1: local Piper `de_DE-thorsten-high` (CC0 dataset),
`length_scale 1.04 · noise 0.6 · noise_w 0.7`, raw IPA for words espeak gets wrong:

| Word | fed as | why |
|---|---|---|
| Widget | `[[vˈɪdʒət]]` | espeak reads it as a German word |
| Website | `[[vˈɛpsaɪt,]]` | as film 1; the comma goes INSIDE the IPA block, or the pause is lost |
| Bontrivo | `[[bˈɔntriːvoː]]` | mid-sentence only (film 1: at a sentence start it is heard as „und Rivo“) |
| 1. / 31. | „ersten“ / „einunddreißigsten“ | spelled as said; the screen shows the figures |

**Quandoo** is fed as plain text. The blind ASR heard the first takes of line 01
as „Quantum“. `tools/vo.py` now weights the brand like Bontrivo (+0.5 if the transcript
contains quand(u|oo|o)) and line 01 was rendered with 12 takes instead of 8. The chosen
take is heard as „Quandu“: the name is recognisable, the vowel is the voice's limit.

**Take selection:** 8 takes per line (12 for 01), blind Whisper-small transcription
(sherpa-onnx), best transcript wins. Word recovery 98 % over the film; per-line scores and
transcripts in `transcripts/*.json`.

**Word timings (step 6):** from the synthesis itself (Piper alignment, sample-exact), as in
film 1. Measured lengths: 01 3.669 · 02 3.541 · 03 5.468 · 04 3.201 · 05 2.159 · 06 5.406 ·
07 5.941 · 08 2.334 · 09 2.817 s.

> For publication: a human voice. Pipeline unchanged (wav + word timings), only
> `tools/vo.py` is replaced by a transcription of the recording.
