#!/usr/bin/env python3
"""verify.py: evidence from the DELIVERED file (Law 6, Law 9), not from the composition.

1. Cues: for each sound cue, the energy in the cue's own frequency band in the 150 ms after
   its time vs the 150 ms before (dB). A cue that is in the index but not in the mix shows
   ~0 dB. The portal tone is checked the other way round: it must STOP on the break.
2. Sync: for five word-locked visual events, the first video frame whose pixels change in
   the event's box, compared with the word's onset from audio_meta.json + frame start.

usage: python3 tools/verify.py renders/quandoo-vN.mp4
"""
import json, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt

MP4 = sys.argv[1]
SR = 48000
idx = open("index.html").read()
import re
starts = {m[1]: float(m[2]) for m in re.finditer(r'data-composition-id="([^"]+)"\s+data-composition-src="[^"]+"\s+data-start="([\d.]+)"', idx)}
meta = json.load(open("audio_meta.json"))

def word(fid, w):
    for x in meta[fid]["words"]:
        if x["w"].startswith(w):
            return starts[fid] + x["start"]
    raise KeyError(w)

pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", MP4, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(pcm, dtype=np.float32)

def band_db(t0, t1, lo, hi):
    seg = a[int(t0 * SR):int(t1 * SR)]
    sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos")
    y = sosfiltfilt(sos, seg)
    return 10 * np.log10(np.mean(y ** 2) + 1e-12)

# (label, frame, local time, band lo, hi, expectation[, (pre window, post window) in s rel. to t])
# The snap is measured on its 70 Hz thud: its bright crack shares the band with the "k" of
# "keine", which starts on the same frame. The own-channel tone fades in over 1.2 s, so it is
# compared over a wide gap (before the turn vs. after the fade-in), not 150 ms either side.
CUES = [
    ("snap · keine (break)",        "01-bruch",    1.70,   55,   85, "up"),
    ("tone-portal stops on break",  "01-bruch",    1.72,  210,  230, "down"),
    ("glide-down · ins Leere",      "03-leere",    4.90,  360,  400, "up"),
    ("tone-own enters at the turn", "05-direkt",   0.00,  255,  268, "up", ((-0.5, -0.2), (1.0, 1.3))),
    ("connect · direkt",            "05-direkt",   1.22,  770,  800, "up"),
    ("zip-up · Speisekarte",        "06-eigen",    3.68,  700, 1300, "up"),
    ("zip-up · Google-Profil",      "06-eigen",    4.66,  700, 1300, "up"),
    ("price-thunk · Neunundzwanzig","07-preis",    2.90,   60,  160, "up"),
    ("pin-tick · Hamburg",          "08-hamburg",  1.00, 1800, 1900, "up"),
    ("chord-c · bontrivo",          "09-wechseln", 1.47, 1040, 1060, "up"),
]
print("CUES (band energy 150 ms after vs before, delivered file)")
bad = 0
for label, fid, at, lo, hi, exp, *win in CUES:
    t = starts[fid] + at
    (p0, p1), (q0, q1) = win[0] if win else ((-0.15, 0.0), (0.02, 0.17))
    pre, post = band_db(t + p0, t + p1, lo, hi), band_db(t + q0, t + q1, lo, hi)
    d = post - pre
    ok = d > 6 if exp == "up" else d < -6
    bad += not ok
    print(f"  {'✓' if ok else '✗'} {label:30s} @{t:7.3f}s  {lo:>4}-{hi:<4} Hz  {d:+6.1f} dB")

# ── sync: first changed frame in a box vs the word onset
FPS = 30
def frames(t0, n, box):
    x, y, w, h = box
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", MP4, "-frames:v", str(n),
                          "-vf", f"crop={w}:{h}:{x}:{y}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w).astype(np.float32)

# mode "onset": an arrival that STARTS on its word (rise); "settle": a landing that ENDS on
# its word (the pin is set down over 0.28 s and comes to rest on "Hamburg").
# `lead` = how far before the word to start looking (the '31.' box is busy until the old
# date has left, 0.15 s before the word).
SYNC = [
    ("'31.' rises",             word("02-export", "31."),      (150, 180, 260, 226), "onset", 0.12),
    ("'INS LEERE.' rises",      word("03-leere", "ins"),        (1130, 608, 540, 112), "onset", 0.3),
    ("'DIREKT BEI IHNEN.'",     word("05-direkt", "direkt"),    (150, 236, 940, 112), "onset", 0.3),
    ("price lands",             word("07-preis", "29,00"),      (1044, 400, 620, 180), "onset", 0.3),
    ("pin on 'Hamburg'",        word("08-hamburg", "Hamburg"),  (1110, 516, 96, 96), "settle", 0.5),
]
print("SYNC (first changed frame for an onset, first still frame for a landing, vs the word)")
for label, tw, box, mode, lead in SYNC:
    t0 = tw - lead
    f = frames(t0, 30, box)
    # pts of the first decoded frame: the next frame boundary at or after t0
    first = np.ceil(t0 * FPS - 1e-6) / FPS
    if mode == "onset":
        diffs = [np.mean(np.abs(f[i] - f[0])) for i in range(len(f))]
        k = next((i for i, v in enumerate(diffs) if v > 0.5), None)
    else:
        steps = [np.mean(np.abs(f[i + 1] - f[i])) for i in range(len(f) - 1)]
        moving = [i for i, v in enumerate(steps) if v > 0.5]
        k = moving[-1] + 1 if moving else None
    if k is None:
        print(f"  ✗ {label:24s} no change found"); bad += 1; continue
    tv = first + k / FPS
    off = (tv - tw) * 1000
    ok = -70 <= off <= 70
    bad += not ok
    print(f"  {'✓' if ok else '✗'} {label:24s} word {tw:7.3f}s  first change {tv:7.3f}s  ({off:+5.0f} ms)")
sys.exit(1 if bad else 0)
