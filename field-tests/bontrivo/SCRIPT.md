# SCRIPT: BONTRIVO (Pipeline step 4)

Written for the ear: one clause per beat, the claim at 0 s, numbers written as they are
said. Single source for voice, captions and timings: `tools/script.json`.

**Voice direction (overall):** calm and warm, like serving at the table, not a radio
spot. Short sentences with the pauses at the full stops.

| # | Line (on screen / captions) | Delivery |
|---|---|---|
| 01 | Websites, die Appetit machen. | the claim, without ceremony, held still |
| 02 | Mit Bontrivo: Ihre Restaurant-Website. Fertig eingerichtet, ohne technisches Vorwissen. | „Fertig“ as the turn |
| 03 | Mit Speisekarte. Gerichte und Preise, jederzeit selbst aktualisiert. | a list, matter of fact |
| 04 | Gäste reservieren direkt über Ihre Website. Ohne Umweg über Drittportale. | contrast factual, not cheeky |
| 05 | Oder bestellen vor, und holen pünktlich ab. | light, the pick-up as a smile |
| 06 | Für Restaurants, Bistros, Bars, Hotels, Cafés, Biergärten und Catering. | even, every Branche gets its beat |
| 07 | Anfragen. Einrichten. Live gehen. Tage, nicht Monate. | three short steps, then the point |
| 08 | Alles inklusive, auch das Hosting. Neunundzwanzig Euro im Monat, bei jährlicher Zahlung. | price clear, honesty line without dropping |
| 09 | Jetzt Website anfragen. Auf bontrivo.de. | the one action |

## Voice (step 5) and why the text differs from the TTS input

Local neural TTS: Piper `de_DE-thorsten-high` (Thorsten-Voice dataset, CC0), plus
`length_scale 1.04 · noise 0.6 · noise_w 0.7`. espeak mispronounces several loanwords, so
for those words the voice gets raw IPA. The on-screen text stays correct:

| Word | espeak would say | fed as |
|---|---|---|
| Websites / Website | `vˈɛbziːtəs` („Web-sie-tes“) | `[[vˈɛpsaɪts]]` |
| Hotels | `hˈoːtəls` (stress on the first syllable) | `[[hotˈɛls]]` |
| Cafés | `kˈɑfeːs` | `[[kafˈeːs]]` |
| Catering | `kˈɑteːrˌɪŋ` | `[[kˈeːtəɾɪŋ]]` |
| Live | `lˈiːvə` | `[[lˈaɪf]]` |
| Bontrivo | `bɔntrˈiːvoː`, at the start of a sentence often heard as „und Rivo“ | `[[bˈɔntriːvoː]]`, and **never at the start of a sentence** (02 was restructured) |

**Take selection:** nobody on the machine can listen, so each line was rendered 8 times
and blind-transcribed with Whisper-small (sherpa-onnx). The take with the best transcript
won, with the brand name weighted. Result: 90 % word recovery (before: 82 %), and
„Bontrivo“ recognised in both lines. The scores per line are in `transcripts/*.json`
(`asr_check`).

**Word timings (step 6):** not from a later transcription. They come from the same
synthesis: Piper's alignment output (`include_alignments`), patched into the model at
runtime, gives the sample count per phoneme, and the sum equals the audio length to the
sample. Spot checks against the waveform: first word ±20 ms, words after pauses ±60 ms.

> For a public launch: record with a human voice. The pipeline stays the same (wav + word
> timings), only `tools/vo.py` would be replaced by a transcription.
