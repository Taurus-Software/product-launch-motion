#!/usr/bin/env bash
# master.sh — two-pass loudness master for a rendered film.
#
#   pass 1  measure with loudnorm
#   pass 2  correct to target, LIMIT the true peak, re-encode the video
#   verify  measure the delivered file and report
#
# Three things this encodes, all of which cost real time to learn:
#
#   1. loudnorm's linear=true applies ONE gain for the whole file and does not back off
#      when a single transient exceeds the target. A master measured +1.1 dBFS — clipped —
#      after one sound effect was made louder. The limiter is not belt-and-braces.
#   2. alimiter applies makeup gain of level_out/limit unless you pass level=disabled.
#      Adding the limiter to fix (1) produced -13.0 LUFS / -0.0 dBFS: louder than the
#      target it was added to protect.
#   3. The video is RE-ENCODED, not copied. Film grain defeats inter-frame compression, so
#      -c:v copy preserves a bloated file; -crf 19 -tune film took 68 MB to 38 MB with no
#      visible loss.
#   4. loudnorm resamples internally (to 192 kHz) and passes that rate on: without an
#      explicit -ar the AAC encoder picked 96 kHz for a delivered web master. Pin 48 kHz.
#   5. The limiter is a SAMPLE-peak limiter; AAC encoding then adds inter-sample peaks.
#      A -1.0 dBFS ceiling measured -0.9 dBTP on the delivered file, which misses the
#      definition of done (true peak <= -1 dBTP). The ceiling sits 0.5 dB lower to leave
#      room for the codec.
#   6. linear=true is only a REQUEST: loudnorm goes linear only if the measured peak plus
#      the gain stays under TP (and the LRA under LRA); otherwise it silently falls back to
#      its dynamic mode, which on a sparse, voice-led mix lands short of the target and
#      squeezes the LRA. A film with long quiet stretches measured -15.9 LUFS / -1.45 dBTP
#      raw, needed +1.9 dB, and was delivered at -14.9 LUFS (LRA 4.0 -> 2.6). So the script
#      checks first: linear possible -> loudnorm as before; not possible -> it applies the
#      one gain itself and the limiter takes the few transients above the ceiling.
#
# usage:
#   ./scripts/master.sh renders/video-v1-raw.mp4 renders/video-v1.mp4 [target_lufs]
#
# Defaults to -14 LUFS / -1.0 dBTP, which is what most social and web platforms normalise
# toward. Deliver louder and the platform turns you down, squashing your dynamics for free.

set -euo pipefail

# `--help` prints the header comment above — one source of truth for the usage text, and it
# exits 0 so wrapping this in a Makefile or CI job does not fail the build.
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  sed -n '2,/^$/p' "$0" | sed -E 's/^# ?//'
  exit 0
fi

IN="${1:-}"
OUT="${2:-}"
TARGET="${3:--14}"
TP="-1.0"
LRA="7"
# 0.841 ≈ -1.5 dBFS: the sample-peak ceiling, 0.5 dB under the -1 dBTP target so the
# AAC encode's inter-sample overshoot still lands under it (measured: a 0.891 ceiling
# delivered -0.9 dBTP)
LIMIT="0.841"

if [[ -z "$IN" || -z "$OUT" ]]; then
  echo "usage: ./scripts/master.sh <in-raw.mp4> <out.mp4> [target_lufs]" >&2
  exit 1
fi
if [[ ! -f "$IN" ]]; then
  echo "no such file: $IN" >&2
  exit 1
fi
if [[ "$IN" == "$OUT" ]]; then
  echo "refusing to overwrite the raw. Version your renders: video-v2.mp4, not in place." >&2
  exit 1
fi
if [[ -f "$OUT" ]]; then
  echo "note: $OUT exists and will be replaced. Version renders rather than overwriting them." >&2
fi

echo "── pass 1 · measuring $IN"
MEASURE=$(ffmpeg -hide_banner -i "$IN" -af "loudnorm=I=${TARGET}:print_format=json" -f null - 2>&1 || true)

read -r M_I M_TP M_LRA M_THRESH <<EOF
$(printf '%s' "$MEASURE" | node -e '
let s = ""; process.stdin.on("data", d => s += d).on("end", () => {
  const m = s.match(/\{[\s\S]*?"target_offset"[\s\S]*?\}/);
  if (!m) { console.error("could not parse loudnorm output"); process.exit(1); }
  const j = JSON.parse(m[0]);
  process.stdout.write([j.input_i, j.input_tp, j.input_lra, j.input_thresh].join(" "));
});')
EOF

echo "   measured  I ${M_I} LUFS · TP ${M_TP} dBTP · LRA ${M_LRA} · thresh ${M_THRESH}"

# Would loudnorm really stay linear? af_loudnorm only goes linear if measured_TP + gain
# <= TP and measured_LRA <= LRA; otherwise it switches to dynamic mode without a word (6).
# (The "--" before the values: they are negative, and node would read them as options.)
read -r GAIN PEAK MODE <<EOF
$(node -e '
const [t, i, tp, lra, ttp, tlra] = process.argv.slice(1).map(Number);
const g = t - i;
const ok = tp + g <= ttp && lra <= tlra;
process.stdout.write([g.toFixed(2), (tp + g).toFixed(2), ok ? "linear" : "gain+limit"].join(" "));
' -- "$TARGET" "$M_I" "$M_TP" "$M_LRA" "$TP" "$LRA")
EOF
echo "   mode      ${MODE} · gain ${GAIN} dB · peak after gain ${PEAK} dBTP"

# Keep the whole filter chain in ONE double-quoted string. Splitting or re-quoting it is
# how you get: Unable to parse "measured_I".
if [[ "$MODE" == "linear" ]]; then
  AF="loudnorm=I=${TARGET}:TP=${TP}:LRA=${LRA}:linear=true"
  AF="${AF}:measured_I=${M_I}:measured_TP=${M_TP}:measured_LRA=${M_LRA}:measured_thresh=${M_THRESH}"
else
  AF="volume=${GAIN}dB"
fi
AF="${AF},alimiter=limit=${LIMIT}:level=disabled:attack=5:release=50"

echo "── pass 2 · correcting, limiting and re-encoding → $OUT"
ffmpeg -hide_banner -y -i "$IN" \
  -c:v libx264 -preset slow -crf 19 -tune film -pix_fmt yuv420p \
  -af "$AF" -ar 48000 \
  -c:a aac -b:a 192k -movflags +faststart \
  "$OUT" 2>&1 | tail -1

echo "── verify · measuring the DELIVERED file (never trust the filter graph's own report)"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true:framelog=quiet -f null - 2>&1 \
  | grep -E "^\s+(I|Peak|LRA):" || true

SIZE=$(du -h "$OUT" | cut -f1)
echo "── $OUT · $SIZE"
echo
echo "Expected: I within 0.5 LUFS of ${TARGET}, Peak (true peak) <= -1.0 dBFS."
echo "(The limiter ceiling is -1.5 dBFS because AAC adds inter-sample peaks on top of it.)"
echo "If I is ~1 dB HOT, something dropped level=disabled from the limiter."
