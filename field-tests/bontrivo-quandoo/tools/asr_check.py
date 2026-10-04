#!/usr/bin/env python3
"""asr_check.py: blind-transcribe every VO line with Whisper (sherpa-onnx) and diff it
against the script. A synthetic voice nobody on this machine can listen to needs an
independent ear; if Whisper cannot recover the words, a viewer will struggle too."""
import json, sys, wave, re, difflib
from pathlib import Path
import numpy as np, sherpa_onnx
M = sys.argv[1]
ROOT = Path(__file__).resolve().parent.parent
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{M}/small-encoder.int8.onnx", decoder=f"{M}/small-decoder.int8.onnx",
    tokens=f"{M}/small-tokens.txt", language="de", task="transcribe", num_threads=4)
norm = lambda s: re.sub(r"[^a-zäöüß0-9 ]", "", s.lower().replace("-", " ")).split()
script = json.loads((ROOT / "tools/script.json").read_text())
tot = ok = 0
for fr in script["frames"]:
    import subprocess
    pcm = subprocess.run(["ffmpeg","-loglevel","error","-i",str(ROOT/f"assets/voice/{fr['id']}.wav"),
                          "-ar","16000","-ac","1","-f","s16le","-"],capture_output=True,check=True).stdout
    a = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768
    s = rec.create_stream(); s.accept_waveform(16000, a); rec.decode_stream(s)
    hyp = s.result.text.strip()
    ref_w, hyp_w = norm(fr["text"]), norm(hyp)
    sm = difflib.SequenceMatcher(a=ref_w, b=hyp_w)
    match = sum(b.size for b in sm.get_matching_blocks())
    tot += len(ref_w); ok += match
    print(f"{fr['id']:18s} {match:2d}/{len(ref_w):2d}  heard: {hyp}")
print(f"\nword recovery {ok}/{tot} = {100*ok/tot:.0f}%")
