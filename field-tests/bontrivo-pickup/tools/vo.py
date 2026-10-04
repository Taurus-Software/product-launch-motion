#!/usr/bin/env python3
"""vo.py: render the narration and its word timings from the same synthesis call.

Law 2 needs the measured start of every word. The usual route is transcribe-after-the-fact
(Whisper). Here the voice can report its own alignment: Piper's VITS duration predictor
decides how many audio samples each phoneme gets, and `include_alignments=True` exposes
those counts. Summed, they equal the audio length to the sample (checked below), so word
starts come straight from the audio the frames will be cut against, not from an estimate.

Writes, per frame:
  assets/voice/<id>.wav           48 kHz mono, peak-normalised to -1 dBFS for the whole line
  transcripts/<id>.json           Whisper-shaped {duration, segments:[{words:[...]}]}
Then run:  node ../../scripts/word-timings.mjs --in transcripts --out audio_meta.json

usage: python3 tools/vo.py --model <de_DE-thorsten-high.onnx> [--only 03-speisekarte]
                          [--takes 8 --asr <sherpa-onnx-whisper-small dir>]

Take selection. VITS samples noise, so every take differs. Nobody on this machine can
listen, so with --asr each line is rendered --takes times, blind-transcribed by Whisper,
and the take whose transcript best matches the script wins (brand name weighted: a launch
film that loses its own name has failed). The score is printed and written into the
transcript so the choice is on the record.
"""

import argparse
import difflib
import re
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

ROOT = Path(__file__).resolve().parent.parent
PUNCT = set(",.;:!?")
SKIP = {"^", "$"}  # BOS / EOS


def words_from_alignment(alignments, sr, offset):
    """Group phoneme alignments into words. A word is a run of phonemes between spaces.

    start = first sample of the run's first phoneme; end = last sample of its last
    non-punctuation phoneme (the pause a comma or period buys is not part of the word).
    """
    words, cur, t = [], None, offset
    for a in alignments:
        dur = a.num_samples / sr
        p = a.phoneme
        if p in SKIP or p == " ":
            if cur:
                words.append(cur)
                cur = None
        else:
            if cur is None:
                cur = {"ph": "", "start": t, "end": t}
            cur["ph"] += p
            if p not in PUNCT:
                cur["end"] = t + dur
        t += dur
    if cur:
        words.append(cur)
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--script", default=str(ROOT / "tools/script.json"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--takes", type=int, default=1)
    ap.add_argument("--asr", default=None)
    args = ap.parse_args()

    script = json.loads(Path(args.script).read_text())
    syn = SynthesisConfig(normalize_audio=False, **script["syn"])
    gap = float(script.get("sentence_gap", 0.2))
    voice = PiperVoice.load(args.model, include_alignments=True)
    sr = voice.config.sample_rate

    (ROOT / "assets/voice").mkdir(parents=True, exist_ok=True)
    (ROOT / "transcripts").mkdir(exist_ok=True)

    rec = None
    if args.asr:
        import sherpa_onnx
        a = args.asr
        rec = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=f"{a}/small-encoder.int8.onnx", decoder=f"{a}/small-decoder.int8.onnx",
            tokens=f"{a}/small-tokens.txt", language="de", task="transcribe", num_threads=4)

    norm = lambda s: re.sub(r"[^a-zäöüß0-9 ]", "", s.lower().replace("-", " ")).split()

    def score(chunks, text):
        audio = np.concatenate([c.audio_float_array for c in chunks])
        n = int(len(audio) * 16000 / sr)
        x = np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio)
        st = rec.create_stream()
        st.accept_waveform(16000, x.astype(np.float32))
        rec.decode_stream(st)
        hyp = st.result.text.strip()
        r = difflib.SequenceMatcher(a=norm(text), b=norm(hyp)).ratio()
        if "bontrivo" in text.lower():
            r += 0.5 if re.search(r"bon.?.?trivo", hyp.lower()) else 0.0
        # a third-party name Whisper does not know: "Quandu" IS the right sound (kvˈanduː);
        # "Quantum" is the take where the name got lost
        if "quandoo" in text.lower():
            r += 0.5 if re.search(r"quand(u|oo|o)\b", hyp.lower()) else 0.0
        return r, hyp

    for fr in script["frames"]:
        if args.only and fr["id"] != args.only:
            continue
        pieces, words, t = [], [], 0.0
        best = None
        for k in range(max(1, args.takes)):
            cand = list(voice.synthesize(fr["tts"], syn_config=syn, include_alignments=True))
            if rec is None:
                best = (0.0, "", cand)
                break
            sc, hyp = score(cand, fr["text"])
            print(f"   take {k}: {sc:.3f}  {hyp}")
            if best is None or sc > best[0]:
                best = (sc, hyp, cand)
        chunks = best[2]
        for i, c in enumerate(chunks):
            if c.phoneme_alignments is None:
                sys.exit(f"{fr['id']}: no alignments — model not patched / onnx missing")
            n = sum(a.num_samples for a in c.phoneme_alignments)
            if n != len(c.audio_float_array):
                sys.exit(f"{fr['id']}: alignment sums to {n} samples, audio has "
                         f"{len(c.audio_float_array)} — refusing to trust it")
            words += words_from_alignment(c.phoneme_alignments, sr, t)
            pieces.append(c.audio_float_array)
            t += len(c.audio_float_array) / sr
            if i < len(chunks) - 1:
                pieces.append(np.zeros(int(round(gap * sr)), dtype=np.float32))
                t += gap

        if len(words) != len(fr["words"]):
            sys.exit(f"{fr['id']}: voice produced {len(words)} word groups "
                     f"{[w['ph'] for w in words]} but script lists {len(fr['words'])}")

        audio = np.concatenate(pieces)
        peak = float(np.max(np.abs(audio))) or 1.0
        audio = audio * (10 ** (-1 / 20) / peak)  # whole-line peak at -1 dBFS
        pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")

        raw = ROOT / f"assets/voice/{fr['id']}.22k.wav"
        with wave.open(str(raw), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(pcm.tobytes())
        out = ROOT / f"assets/voice/{fr['id']}.wav"
        # Resample only: a sample-rate change keeps every timestamp exactly where it was.
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw),
                        "-ar", "48000", "-ac", "1", str(out)], check=True)
        raw.unlink()

        duration = len(audio) / sr
        transcript = {
            "duration": round(duration, 4),
            "source": f"piper alignment ({script['voice']}), sample-exact",
            "asr_check": {"score": round(best[0], 3), "heard": best[1]} if rec else None,
            "segments": [{"words": [
                {"word": disp, "start": round(w["start"], 4), "end": round(w["end"], 4),
                 "phonemes": w["ph"]}
                for disp, w in zip(fr["words"], words)
            ]}],
        }
        (ROOT / f"transcripts/{fr['id']}.json").write_text(
            json.dumps(transcript, ensure_ascii=False, indent=2) + "\n")
        print(f"{fr['id']:18s} {duration:6.3f}s  {len(words):2d} words  "
              + " ".join(f"{d}@{w['start']:.2f}" for d, w in zip(fr["words"], words)))


if __name__ == "__main__":
    main()
