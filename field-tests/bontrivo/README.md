# Field test: BONTRIVO launch film

A test run of the `product-launch-motion` skill (this repo) on a real product:
**bontrivo.de**, restaurant websites. Result and verdict: `FINDINGS.md`.

| Read | What is in it |
|---|---|
| `BRIEF.md` | Step 1+3: product, audience, the one claim, approved figures, negative list |
| `source/SOURCES.md` | The evidence: every on-screen sentence with its source on the site; contradictions |
| `DIRECTION.md` | Step 2: three directions, two killed, signature, structure vs. the reference film |
| `SCRIPT.md` | Step 4–6: script, voice, take selection, word timings |
| `STORYBOARD.md` | Step 7: every frame with measured times, cues, camera, reconstructions |
| `FINDINGS.md` | Test report: bugs found in the skill (four fixed), gates, definition of done |
| `deliverables/` | 16:9 master, 9:16 with captions, SRT, silent cut, poster, stills, loop |

## Rebuild

Requirements: Node 22, ffmpeg, Python 3.11, a Chromium headless shell.

```bash
npm install                                         # hyperframes, gsap, Montserrat
pip install piper-tts onnx sherpa-onnx fonttools brotli pillow scipy
export HYPERFRAMES_BROWSER_PATH=/path/to/headless_shell
npx hyperframes telemetry disable

# voice + word timings (the voice reports its own alignment; Whisper only chooses the take)
python3 tools/vo.py --model <de_DE-thorsten-high.onnx> --takes 8 --asr <sherpa-onnx-whisper-small>
node ../../scripts/word-timings.mjs --in transcripts --out audio_meta.json

# brand + sound
python3 tools/vectorize_logo.py && node tools/build-lib.mjs
bash tools/sfx.sh                                    # then level the swells, see audio/cues.json

# build chain, ALWAYS in this order (SKILL.md, step 9)
node ../../scripts/assemble.mjs
node ../../scripts/transitions.mjs
node ../../scripts/wire-audio.mjs
node ../../scripts/wire-grade.mjs --grain 0.05 --vignette 0
node tools/check-durations.mjs                       # trap 4

# gates, render, master
npx hyperframes check . --no-contrast
node ../../scripts/wire-grade.mjs --off && npx hyperframes check . ; node ../../scripts/wire-grade.mjs --grain 0.05 --vignette 0
npx hyperframes render . -o renders/bontrivo-vN-raw.mp4 --quality high
bash ../../scripts/master.sh renders/bontrivo-vN-raw.mp4 renders/bontrivo-vN.mp4

# 9:16
node tools/make-vertical.mjs && cd vertical
node ../../../scripts/assemble.mjs && node ../../../scripts/transitions.mjs
node ../../../scripts/wire-audio.mjs && node ../../../scripts/wire-grade.mjs --grain 0.05 --vignette 0
node ../tools/captions.mjs --index index.html --burn --y 1352
npx hyperframes render . -o ../renders/bontrivo-9x16-vN-raw.mp4 --quality high
```

## Licences

- Montserrat: SIL Open Font License 1.1 (`assets/fonts/OFL-Montserrat.txt`)
- Voice: Piper `de_DE-thorsten-high`, trained on the Thorsten-Voice dataset (CC0)
- Sounds: all synthesised with ffmpeg (`tools/sfx.sh`), no third-party samples
- Logo, copy, colours: BONTRIVO, supplied by the user for this test
- Renderer: HyperFrames (Apache-2.0), GSAP (vendored)
