# Field test 3: BONTRIVO · Vorbestellen & Abholen

The third film made with the `product-launch-motion` skill (this repo) for **bontrivo.de**,
about one feature: pre-ordering for pickup („Pick Up Order System“). Claim, verbatim from
the site: **„Einfach für Gäste. Einfach für Ihr Team.“** Films 1 and 2: `../bontrivo/`,
`../bontrivo-quandoo/`. Result and verdict: `FINDINGS.md`.

> Best heard on headphones: the guest's sounds sit left, the team's right.

| Read | What is in it |
|---|---|
| `BRIEF.md` | Product, audience, the one claim, approved figures, negative list |
| `source/SOURCES.md` | The pickup page verbatim, every sentence's source, what the sources do NOT say |
| `DIRECTION.md` | Three directions (one killed by law 10 as the earlier films' house style), signature, structure vs. three references |
| `SCRIPT.md` | Script by side of the counter, voice, take selection, word timings |
| `STORYBOARD.md` | Every frame with measured times, cues, the 9:16 layout, reconstructions |
| `FINDINGS.md` | Test report: findings for the skill, gates incl. stereo and the signature measured, defects |
| `deliverables/` | 16:9 master, 9:16 with captions, SRT, poster, stills, loop, `YOUTUBE.md` |

## Rebuild

Requirements as in film 1 (Node 22, ffmpeg, Python 3.11 with numpy/scipy, a Chromium
headless shell).

```bash
npm install
export HYPERFRAMES_BROWSER_PATH=/path/to/headless_shell
npx hyperframes telemetry disable

# voice (line 10 is film 1's take: assets/voice/10-anfragen.wav + its transcript)
python3 tools/vo.py --model <de_DE-thorsten-high.onnx> --takes 8 --asr <sherpa-onnx-whisper-small> --only 01-split   # … each of 01–09
node ../../scripts/word-timings.mjs --in transcripts --out audio_meta.json
bash tools/sfx.sh                                    # the stereo kit (pan baked in)

# frames are GENERATED (the stage persists across hard cuts): edit tools/frames.py
node ../../scripts/assemble.mjs                      # durations first (frames.py reads them)
python3 tools/frames.py
node ../../scripts/assemble.mjs && node ../../scripts/transitions.mjs && node ../../scripts/wire-audio.mjs
node tools/check-durations.mjs                       # trap 4

# gates, render, master, evidence from the delivered file
npx hyperframes check .
npx hyperframes render . -o renders/pickup-vN-raw.mp4 --quality high
bash ../../scripts/master.sh renders/pickup-vN-raw.mp4 renders/pickup-vN.mp4
python3 tools/verify.py renders/pickup-vN.mp4       # cue bands, stereo, sync, the bag on the counter

# 9:16 (same frame files, the root's declared size swapped)
node tools/make-vertical.mjs && cd vertical
node ../../../scripts/assemble.mjs && node ../../../scripts/transitions.mjs
node ../../../scripts/wire-audio.mjs --cues ../audio/cues.json
node ../tools/captions.mjs --index index.html --burn --y 1352 --width 1080 --srt ../deliverables/bontrivo-pickup-16x9-vN.srt
npx hyperframes render . -o ../renders/pickup-9x16-vN-raw.mp4 --quality high
```

## Licences

- Montserrat: SIL Open Font License 1.1 (`assets/fonts/OFL-Montserrat.txt`)
- Voice: Piper `de_DE-thorsten-high`, trained on the Thorsten-Voice dataset (CC0)
- Sounds: all synthesised with ffmpeg (`tools/sfx.sh`); `chord-c`, `sub-drop`,
  `price-thunk`, `bean-tick` come from film 1's kit, also synthesised
- Logo, copy, colours: BONTRIVO, supplied by the user
