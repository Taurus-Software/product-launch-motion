---
format: 1920x1080 (+ 1080x1920 from the same frame files)
fps: 30
duration: 37.563s (measured from the voiceover by scripts/assemble.mjs)
claim: "Einfach für Gäste. Einfach für Ihr Team."
arc: the split opens → guest orders → team sees it (same instant) → team sets the time → handover on the minute → gains on both sides → claim across the counter → setup → price → mark across both sides
---

# STORYBOARD: BONTRIVO · Vorbestellen & Abholen

## Video direction

**Direction:** „Zwei Seiten, eine Zeit“ (`DIRECTION.md`). The frame is split for the whole
film: guest's side cream (16:9 left / 9:16 top), team's side ink (right / bottom). The seam
is the counter. Every beat happens on it or mirrored across it.

**Register map.** Both registers at once, all film. **Accent:** tomato = the order tag, the
pickup-time arc, the price, the CTA button. **Olive:** the check on the bag at handover;
the bean in the logo.

**Two-colourway objects.** The clock, the travelling bag, the price lines, the URL and the
wordmark exist twice (ink copy clipped to the guest's half, cream copy to the team's),
driven by one tween, so each reads as one object that changes colour exactly at the
counter (`compositions/lib/split.js`).

**Motion and camera.** Locked, symmetric stage; hard cuts only (`film.json`); the stage
(grounds, side labels, icons, tags, clock, bag) is drawn identically on both sides of every
cut by construction (`tools/frames.py`), measured: 0 changed pixels across 02→03 and
05→06. Entrances 0.24–0.34 s `power3.out`, no overshoot. Nothing is moving at any cut.

**Sound.** Stereo is the device: guest cues left, team cues right (measured 7–14 dB apart
in the delivered file), the bag's swish travels right → left, one service bell on
„pünktlich“, the brand chord on „bontrivo“.

## Frames

Times: start + duration, from `index.html`. Cues are frame-relative (`audio/cues.json`).

### F01 · 01-split · 0.000 + 3.266
A cream field; the team's side opens from the seam outwards (0 → 0.55, open-r on the
right). „VORBESTELLEN“ @0.24 flush right to the seam, „UND ABHOLEN.“ @1.01 flush left;
„ganz | einfach.“ @1.82 / 2.02; side labels „GAST | IHR TEAM“ appear as the split settles.

### F02 · 02-gast · 3.266 + 3.375 · hard cut
Guest's side only: the guest @0.31, „BESTELLEN VOR.“ @0.63, the order tag @1.02 („vor“,
tap-l, left), „direkt über Ihre Website“ @1.52. The team's side stays dark and empty.

### F03 · 03-echtzeit · 6.641 + 2.550 · hard cut
Guest side holds. The team @0.24, „Ihr Team sieht die Bestellung“ @0.49, „IN ECHTZEIT.“
@1.22; on **„Echtzeit“ @1.37** the same order tag appears on the team's side, mirrored, and
both tags pulse once together; tap-r on the right. Nothing crosses the seam: real time is
simultaneity.

### F04 · 04-abholzeit · 9.191 + 2.533 · hard cut
Copy cleared, cast holds. One clock appears ON the counter @0.03 (half ink, half cream).
„steuert“ @0.23: the tomato pickup arc turns from 12 o'clock to 105° (the team's half of
the dial) and locks; ratchet-r on the right. „STEUERT DIE / ABHOLZEIT.“ on the team's side.
No numerals on the dial.

### F05 · 05-puenktlich · 11.724 + 3.220 · hard cut · THE SIGNATURE
The bag is ready on the team's side @0.20. The hand sweeps 12 → the arc, landing on
**„pünktlich“ @1.31**; the bag travels 1.06 → 1.56, symmetric, so it is ON the counter at
1.31 (measured: centroid x 964, seam 960) and changes colour as it crosses. Olive check on
arrival @1.60; the order tags retire @1.74. „HOLEN / PÜNKTLICH AB.“ on the guest's side.
Sound: swish-rl (pan turns over at the crossing), the service bell @1.31.

### F06 · 06-weniger · 14.944 + 3.661 · hard cut
The stage after the handover holds. „WENIGER / WARTEZEIT.“ (guest) · „MEHR ZUFRIEDENE /
GÄSTE.“ (team), each on its words.

### F07 · 07-einfach · 18.604 + 3.399 · hard cut · THE CLAIM
Bare stage. „EINFACH / FÜR GÄSTE.“ flush right (tick-l @0.57), „EINFACH / FÜR IHR TEAM.“
flush left (tick-r @2.00), 92 px.

### F08 · 08-live · 22.004 + 4.323 · hard cut
„WIR RICHTEN DIE / VORBESTELLUNG EIN.“ on the team's side (spoken first, rises first),
„IN WENIGEN / TAGEN LIVE.“ on the guest's side.

### F09 · 09-preis · 26.327 + 5.684 · hard cut
Side labels go. „VORBESTELLUNG | INKLUSIVE“; **„29,00 €“ @1.92** on the counter
(price-thunk), „/ Monat“ @3.25 and „Jährliche Zahlweise — 348,00 € / Jahr, im Voraus
fällig“ @3.96 straddle the seam in two colourways.

### F10 · 10-anfragen · 32.011 + 5.552 · hard cut
„JETZT WEBSITE ANFRAGEN →“ @0.68 on the counter. The wordmark arrives in two parts, BONT
from the left edge, RIVO from the right (9:16: top half from above, bottom half from below),
and they meet in register on **„bontrivo“ @2.15** (measured: settled −25 ms) with
chord-c + sub-drop. „bontrivo.de“ @2.77. Locked still from 2.8; the last frame is the
poster: one mark across both sides.

## 9:16

Same frame files: `#root[data-width="1080"]` rules move the seam to y 760 (guest on top,
team below; the team's half is taller because the burned captions sit in it at y 1352).
The clock moves to the right edge of the seam, the bag travels upwards across it, and the
wordmark is cut horizontally by the seam. `tools/make-vertical.mjs` only swaps the root's
declared size.

## Reconstructions and drawings (so a reviewer can tell a decision from a lie)

- **No ordering UI, no device, no printer.** The order is a tomato disc with a receipt
  glyph; the team's side is a diagram. The sources describe neither (`source/SOURCES.md`).
- **The clock has no numerals;** 105° is a position, not a time.
- **Icons:** `guest`, `bag`, `cloche` from films 1–2's library (site idiom); `receipt` is
  new, drawn in the same idiom. The olive check is the film's own.
- **Logo:** vectorised from the supplied PNG (film 1); in F10 it is split by the seam into
  two colourways, the brand colours of ring and bean unchanged.
