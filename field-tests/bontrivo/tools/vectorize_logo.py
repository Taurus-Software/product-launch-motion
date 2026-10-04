#!/usr/bin/env python3
"""vectorize_logo.py: trace the user-supplied 577x186 PNG into a crisp SVG, one path per
colour layer, so the mark survives 1080p (and the 6x scale-up of the O-plate) without
going soft. This is a RECONSTRUCTION of the supplied raster, not a new logo: every layer
is traced from its own pixels, the fills are the PNG's measured colours, and the viewBox is
the PNG's own pixel grid so positions can be read straight off the source image."""
import subprocess, re, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage, optimize
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source/bontrivo-logo-user-supplied.png"
UP = 8
im = Image.open(SRC).convert("RGBA")
W, H = im.size
big = np.array(im.resize((W * UP, H * UP), Image.LANCZOS)).astype(int)
r, g, b, a = (big[:, :, i] for i in range(4))
# Smooth before thresholding: the source O is only ~81 px across and the film shows it at
# ~6x, where threshold noise on an anti-aliased edge reads as a wobble. sigma is in
# upscaled px (UP per source px); the shapes are geometric, so this costs no detail.
def smooth(mask, sigma_src):
    return ndimage.gaussian_filter(mask.astype(float), sigma_src * UP) > 0.5
letters = smooth((r < 110) & (g < 110) & (b < 110) & (a > 128), 0.35)
ring_t = smooth((r > 170) & (g < 160) & (b < 130) & (a > 128), 1.0)
bean = smooth((g > 160) & (r > 130) & (r < 215) & (b < 140) & (a > 128), 0.8)
# The ring's inner and outer edges are circles: fit them, and keep only the trace's
# ANGULAR extent (the cut ends hugging the bean). Least squares on the edge pixels.
# Fit the OUTER rim first (edge pixels clearly outside the band's middle are rim pixels;
# the cut ends near the bean are excluded by taking only the outermost 35% of radii), then
# read the inner radius per angle away from the gap. A plain median split on all edge
# pixels lets the cut ends drag the inner radius outward and thins the ring.
edge = ring_t ^ ndimage.binary_erosion(ring_t)
ey, ex = np.nonzero(edge)
def fit_circle(xs, ys, c0):
    f = lambda c: np.hypot(xs - c[0], ys - c[1]) - np.hypot(xs - c[0], ys - c[1]).mean()
    c = optimize.least_squares(f, c0).x
    return c, np.hypot(xs - c[0], ys - c[1]).mean()
cy0, cx0 = ndimage.center_of_mass(ring_t)
d = np.hypot(ex - cx0, ey - cy0)
outer = d > np.percentile(d, 65)
c, r_out = fit_circle(ex[outer], ey[outer], [cx0, cy0])
ry, rx = np.nonzero(ring_t)
ang = np.degrees(np.arctan2(ry - c[1], rx - c[0])) % 360
dist = np.hypot(rx - c[0], ry - c[1])
bins = np.floor(ang / 10).astype(int)
mins = [dist[bins == k].min() for k in range(36) if (bins == k).sum() > 0.8 * np.bincount(bins).max()]
r_in = float(np.median(mins))
yy, xx = np.mgrid[0:H * UP, 0:W * UP]
dd = np.hypot(xx - c[0], yy - c[1])
annulus = (dd >= r_in) & (dd <= r_out)
# Tried: annulus ∩ trace, and annulus − dilated bean. Neither reproduced the cut ends (best
# IoU 0.95 against the source), so the hero ring IS the smoothed trace; the fitted circle
# is kept only as positioning data (ring-geometry.json) for the film's camera maths.
ring = ring_t
GEOM = {"cx": c[0] / UP, "cy": c[1] / UP, "r_in": r_in / UP, "r_out": r_out / UP}
print("ring fit (source px):", {k: round(v, 2) for k, v in GEOM.items()})
layers = {
    # name: (mask, fill measured from the PNG)
    "letters": (letters, "#242220"),
    "ring":    (ring, "#E65F3C"),
    "bean":    (bean, "#B7CF4A"),
}
out = {}
tmp = ROOT / "tools/.trace"; tmp.mkdir(exist_ok=True)
for name, (mask, fill) in layers.items():
    pbm = tmp / f"{name}.pbm"
    Image.fromarray(np.where(mask, 0, 255).astype("uint8")).convert("1").save(pbm)
    svg = tmp / f"{name}.svg"
    subprocess.run(["potrace", str(pbm), "-s", "-o", str(svg), "--turdsize", "40",
                    "--alphamax", "1.0", "--opttolerance", "0.2", "--flat"], check=True)
    txt = svg.read_text()
    tr = re.search(r'<g transform="([^"]+)"', txt).group(1)
    paths = re.findall(r'<path d="([^"]+)"', txt, re.S)
    out[name] = (tr, [p.replace("\n", " ") for p in paths], fill)
# potrace writes in its own point space; wrap each layer in its transform, then scale the
# whole thing back to the PNG's pixel grid (1/UP) so the viewBox is 0 0 577 186.
def group(name):
    tr, paths, fill = out[name]
    d = " ".join(paths)
    return (f'  <g id="logo-{name}" fill="{fill}">\n'
            f'    <g transform="scale({1/UP}) {tr}"><path d="{d}"/></g>\n  </g>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       f'  <!-- traced from source/bontrivo-logo-user-supplied.png by tools/vectorize_logo.py -->\n'
       + "\n".join(group(n) for n in ("letters", "ring", "bean")) + "\n</svg>\n")
(ROOT / "assets/brand/bontrivo-logo-traced.svg").write_text(svg)
for n in ("letters", "ring", "bean"):
    (ROOT / f"assets/brand/bontrivo-{n}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">\n{group(n)}\n</svg>\n')
import json
(ROOT / "assets/brand/ring-geometry.json").write_text(json.dumps({k: round(v, 3) for k, v in GEOM.items()}, indent=2) + "\n")
print("wrote assets/brand/bontrivo-logo-traced.svg (+ per-layer files, ring-geometry.json)")
