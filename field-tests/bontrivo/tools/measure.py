#!/usr/bin/env python3
"""measure.py: exact advance widths of a string in Montserrat at a given weight and size,
from the same woff2 the frames load, so layout constants are computed instead of guessed."""
import sys, functools
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
FONT = "assets/fonts/montserrat-variable-latin.woff2"
@functools.lru_cache(None)
def inst(w):
    f = TTFont(FONT); return instancer.instantiateVariableFont(f, {"wght": w})
def width(text, size, weight=900, tracking_em=0.0):
    f = inst(weight); cmap = f.getBestCmap(); hmtx = f["hmtx"]; upm = f["head"].unitsPerEm
    adv = sum(hmtx[cmap[ord(c)]][0] for c in text)
    return adv * size / upm + tracking_em * size * len(text)
if __name__ == "__main__":
    size, weight = float(sys.argv[1]), int(sys.argv[2]); track = float(sys.argv[3])
    for t in sys.argv[4:]:
        print(f"{width(t, size, weight, track):8.1f}  {t!r}")
