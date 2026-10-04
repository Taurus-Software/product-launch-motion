# Field test 2: BONTRIVO · Quandoo-Alternative

The second film made with the `product-launch-motion` skill (this repo) for **bontrivo.de**:
restaurants whose reservations ran through Quandoo until 30 September 2026. Claim, verbatim
from the site: **„Reservierungen ab jetzt direkt bei Ihnen.“** Film 1: `../bontrivo/`.
Result and verdict: `FINDINGS.md`.

> **Expiry date:** correct until 31 December 2026 (data export deadline). **Before
> publication:** have the naming of the competitor checked (UWG §6), see `BRIEF.md`.

| Read | What is in it |
|---|---|
| `BRIEF.md` | Product, audience, the one claim, approved figures, negative list (incl. the competitor exception) |
| `source/SOURCES.md` | Evidence: third-party claims checked against the press, Bontrivo wording per on-screen sentence |
| `DIRECTION.md` | Three directions, two killed (incl. the countdown), signature, structure vs. the reference film AND film 1 |
| `SCRIPT.md` | Script, voice, take selection, word timings |
| `STORYBOARD.md` | Every frame with measured times, cues, reconstructions |
| `FINDINGS.md` | Test report: skill bugs (two fixed in `scripts/`/library, one in the captions tool), gates, definition of done |
| `deliverables/` | 16:9 master, 9:16 with captions, SRT, poster, stills, loop, `YOUTUBE.md` (title, description, tags) |

## Rebuild

Requirements as in film 1 (Node 22, ffmpeg, Python 3.11 with numpy/scipy, a Chromium
headless shell).

```bash
npm install
export HYPERFRAMES_BROWSER_PATH=/path/to/headless_shell
npx hyperframes telemetry disable

# voice + word timings (8 takes; line 01 was rendered with 12)
python3 tools/vo.py --model <de_DE-thorsten-high.onnx> --takes 8 --asr <sherpa-onnx-whisper-small>
node ../../scripts/word-timings.mjs --in transcripts --out audio_meta.json
bash tools/sfx.sh

# build chain (no wire-grade: DIRECTION "clinical", no grain, no grade)
node ../../scripts/assemble.mjs
node ../../scripts/transitions.mjs
node ../../scripts/wire-audio.mjs
node tools/check-durations.mjs                       # trap 4

# gates, render, master, evidence from the delivered file
npx hyperframes check .
npx hyperframes render . -o renders/quandoo-vN-raw.mp4 --quality high
bash ../../scripts/master.sh renders/quandoo-vN-raw.mp4 renders/quandoo-vN.mp4
python3 tools/verify.py renders/quandoo-vN.mp4      # cue bands + 5 sync checks

# 9:16
node tools/make-vertical.mjs && cd vertical
node ../../../scripts/assemble.mjs && node ../../../scripts/transitions.mjs
node ../../../scripts/wire-audio.mjs --cues ../audio/cues.json
node ../tools/captions.mjs --index index.html --burn --y 1352 --width 1080 --srt ../deliverables/bontrivo-quandoo-16x9-vN.srt
npx hyperframes render . -o ../renders/quandoo-9x16-vN-raw.mp4 --quality high
```

## Licences

- Montserrat: SIL Open Font License 1.1 (`assets/fonts/OFL-Montserrat.txt`)
- Voice: Piper `de_DE-thorsten-high`, trained on the Thorsten-Voice dataset (CC0)
- Sounds: all synthesised with ffmpeg (`tools/sfx.sh`); `chord-c`, `sub-drop`,
  `price-thunk`, `bean-tick` come from film 1's kit, also synthesised
- Logo, copy, colours: BONTRIVO, supplied by the user. „Quandoo“ appears only as plain
  text; no Quandoo assets are used. Quandoo is a trademark of its owner; BONTRIVO is not
  affiliated with Quandoo.
