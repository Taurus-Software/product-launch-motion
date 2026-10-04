#!/usr/bin/env python3
"""verify.py (film 3): evidence from the DELIVERED file (Law 6, Law 9).

1. Cues: energy in each cue's own band, 150 ms after vs before (dB).
2. Stereo: the film's device is the panning (guest left, team right), so for every panned
   cue the left/right energy in its band is measured; the bag's swish must MOVE (right in
   its first half, left in its second).
3. Sync: word-locked visual events (first changed frame for an onset, first still frame
   for a landing), plus the signature: the bag's centroid must be ON the counter at the
   frame of „pünktlich“.

usage: python3 tools/verify.py renders/pickup-vN.mp4
"""
import json, re, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt

MP4 = sys.argv[1]
SR, FPS = 48000, 30
idx = open("index.html").read()
starts = {m[1]: float(m[2]) for m in re.finditer(r'data-composition-id="([^"]+)"\s+data-composition-src="[^"]+"\s+data-start="([\d.]+)"', idx)}
meta = json.load(open("audio_meta.json"))
bad = 0


def word(fid, w):
    for x in meta[fid]["words"]:
        if x["w"].startswith(w):
            return starts[fid] + x["start"]
    raise KeyError(w)


pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", MP4, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
st = np.frombuffer(pcm, dtype=np.float32).reshape(-1, 2)
mono = st.mean(axis=1)


def band(x, t0, t1, lo, hi):
    seg = x[int(t0 * SR):int(t1 * SR)]
    y = sosfiltfilt(butter(4, [lo, hi], btype="band", fs=SR, output="sos"), seg)
    return 10 * np.log10(np.mean(y ** 2) + 1e-12)


def check(ok, line):
    global bad
    bad += not ok
    print(f"  {'✓' if ok else '✗'} {line}")


CUES = [  # label, frame, at, lo, hi
    ("tap-l · vor (order placed)",     "02-gast",       1.02, 1250, 1400),
    ("tap-r · Echtzeit (order seen)",  "03-echtzeit",   1.37, 1250, 1400),
    ("ratchet-r · steuert",            "04-abholzeit",  0.27, 1800, 2600),
    ("bell · pünktlich",               "05-puenktlich", 1.31, 2450, 2530),
    ("tick-l · Gäste",                 "07-einfach",    0.57, 1800, 1900),
    ("tick-r · Team",                  "07-einfach",    2.00, 1800, 1900),
    ("price-thunk · Neunundzwanzig",   "09-preis",      1.92,   60,  160),
    ("chord-c · bontrivo",             "10-anfragen",   2.15, 1040, 1060),
]
print("CUES (band energy 150 ms after vs before, delivered file)")
for label, fid, at, lo, hi in CUES:
    t = starts[fid] + at
    d = band(mono, t + 0.02, t + 0.17, lo, hi) - band(mono, t - 0.15, t, lo, hi)
    check(d > 6, f"{label:32s} @{t:7.3f}s  {lo:>4}-{hi:<4} Hz  {d:+6.1f} dB")

PANS = [  # label, frame, at, dur, lo, hi, expected side
    ("open-r · the team's side opens", "01-split",    0.02, 0.18,  300, 1600, "R"),  # before the voice (0.24)
    ("tap-l",                          "02-gast",     1.02, 0.12, 1250, 1400, "L"),
    ("tap-r",                          "03-echtzeit", 1.37, 0.12, 1250, 1400, "R"),
    ("ratchet-r",                      "04-abholzeit", 0.27, 0.42, 1800, 2600, "R"),
    ("tick-l",                         "07-einfach",  0.57, 0.10, 1800, 1900, "L"),
    ("tick-r",                         "07-einfach",  2.00, 0.10, 1800, 1900, "R"),
    # the swish is read between the bell's 1245 and 2490 Hz partials (the bell is centred)
    ("swish-rl, first half",           "05-puenktlich", 1.12, 0.14, 1500, 2300, "R"),
    ("swish-rl, second half",          "05-puenktlich", 1.33, 0.14, 1500, 2300, "L"),
]
print("STEREO (left vs right energy in the cue's band; guest = left, team = right)")
for label, fid, at, dur, lo, hi, side in PANS:
    t = starts[fid] + at
    L, R = band(st[:, 0], t, t + dur, lo, hi), band(st[:, 1], t, t + dur, lo, hi)
    d = (R - L) if side == "R" else (L - R)
    check(d > 4, f"{label:32s} @{t:7.3f}s  L {L:6.1f}  R {R:6.1f} dB  → {side} by {d:+5.1f} dB")


def frames(t0, n, box):
    x, y, w, h = box
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", MP4, "-frames:v", str(n),
                          "-vf", f"crop={w}:{h}:{x}:{y}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w).astype(np.float32)


SYNC = [  # label, word time, box, mode, lead
    ("'BESTELLEN VOR.' rises",  word("02-gast", "bestellen"),     (312, 220, 588, 84), "onset", 0.3),
    ("team tag on 'Echtzeit'",  word("03-echtzeit", "Echtzeit"),  (1316, 576, 88, 88), "onset", 0.3),
    ("hand lands 'pünktlich'",  word("05-puenktlich", "pünktlich"), (780, 440, 360, 360), "settle", 1.2),
    ("'FÜR IHR TEAM.' rises",   word("07-einfach", "für") + 1.28, (1020, 532, 748, 96), "onset", 0.3),
    ("price lands",             word("09-preis", "29,00"),        (652, 380, 616, 180), "onset", 0.3),
    ("mark registers",          word("10-anfragen", "bontrivo"),  (410, 252, 1100, 356), "settle", 0.8),
]
print("SYNC (first changed frame for an onset, first still frame for a landing, vs the word)")
for label, tw, box, mode, lead in SYNC:
    t0 = tw - lead
    f = frames(t0, int((lead + 0.5) * FPS), box)
    first = np.ceil(t0 * FPS - 1e-6) / FPS
    # a frame "changes" when more than 20 pixels move by more than 16 levels: a mean over the
    # box missed the last, slow frames of a thin clock hand easing in (v1 of this check)
    changed = lambda a, b: np.count_nonzero(np.abs(a - b) > 16) > 20
    if mode == "onset":
        k = next((i for i in range(len(f)) if changed(f[i], f[0])), None)
    else:
        # settled = from this frame on, every frame matches the last one (a fixed reference
        # is robust to codec flicker; frame-to-frame deltas were not)
        ref = f[-1]
        near = [np.count_nonzero(np.abs(x - ref) > 40) < 30 for x in f]
        k = next((i for i in range(len(f)) if all(near[i:])), None)
    if k is None:
        check(False, f"{label:26s} no change found"); continue
    off = (first + k / FPS - tw) * 1000
    check(-70 <= off <= 70, f"{label:26s} word {tw:7.3f}s  frame {first + k / FPS:7.3f}s  ({off:+5.0f} ms)")

# the signature: where is the bag at the frame of „pünktlich“? (16:9 only: y 805-915)
tp = word("05-puenktlich", "pünktlich")
fr = frames(tp - 0.5 / FPS, 1, (300, 805, 1400, 110))[0]
xs = np.arange(300, 1700)[None, :].repeat(110, 0)
guest = (xs < 960) & (fr < 200)     # ink strokes on cream
team = (xs >= 960) & (fr > 90)      # cream strokes on ink
m = guest | team
cx = float((xs * m).sum() / max(m.sum(), 1))
check(abs(cx - 960) < 45, f"bag on the counter at 'pünktlich' ({tp:.3f}s): centroid x {cx:.0f} (seam 960)")
sys.exit(1 if bad else 0)
