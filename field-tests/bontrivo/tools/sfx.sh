#!/usr/bin/env bash
# sfx.sh: synthesise the film's whole sound kit with ffmpeg. No third-party samples, so
# there is no licence to track (references/07, "Licensing"): every asset is an equation.
#
# The palette is DIRECTION.md's: one porcelain "clink" that recurs and builds into a chord
# (C5 plate set · C6/E6/G6 the three courses · C-E-G-C on the logo), a soft air move for a
# serve/clear, wood ticks for steps, one sub-bass, and a room tone instead of a music bed.
#
# usage: bash tools/sfx.sh            (writes audio/sfx/*.mp3 and audio/room.mp3)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=audio/sfx
mkdir -p "$OUT"
SR=48000

gen() { # name duration expression [extra -af]
  local name=$1 dur=$2 expr=$3 af=${4:-anull}
  ffmpeg -hide_banner -loglevel error -y -f lavfi \
    -i "aevalsrc=exprs='$expr':s=$SR:d=$dur" \
    -af "$af,alimiter=limit=0.89:level=disabled,afade=t=out:st=$(awk -v d="$dur" 'BEGIN{print d-0.04}'):d=0.04" \
    -ac 1 -c:a libmp3lame -b:a 192k "$OUT/$name.mp3"
}

# A porcelain clink: FM bell (inharmonic 2.756 ratio, index decaying fast, like struck
# ceramic) plus a 6 ms bright attack so it reads as a hit, not a tone. t=0 is the hit.
bell() { # freq decay
  echo "0.62*sin(2*PI*$1*t + 1.6*exp(-t*9)*sin(2*PI*$1*2.756*t))*exp(-t*$2) + 0.18*sin(2*PI*$1*4.07*t)*exp(-t*($2*3)) + 0.22*(random(0)*2-1)*exp(-t*160)"
}

gen clink-c5 1.2  "$(bell 523.25 4.2) + 0.5*sin(2*PI*92*t)*exp(-t*22)"   # plate set down: tone + table thud
gen clink-c6 0.9  "$(bell 1046.5 5.5)"                                     # course 1
gen clink-e6 0.9  "$(bell 1318.5 5.5)"                                     # course 2
gen clink-g6 0.9  "$(bell 1568.0 5.5)"                                     # course 3
gen bean-tick 0.5 "$(bell 2093.0 9)*0.8"                                   # the garnish lands (C7, short)

# The resolution: C5 E5 G5 C6 struck 8 ms apart (a hand, not a sampler), longer ring.
gen chord-c 2.6 "($(bell 523.25 1.8) + $(bell 659.25 1.9)*0.85*gt(t,0.008) + $(bell 783.99 2.0)*0.8*gt(t,0.016) + $(bell 1046.5 2.4)*0.6*gt(t,0.024))*0.5"

# Sub-bass: 58→46 Hz glide, felt not heard (references/07: under thesis and CTA only).
gen sub-drop 1.8 "0.9*sin(2*PI*(58*t - 3.3*t*t))*(1-exp(-t*30))*exp(-t*1.6)"

# Air moves: pink-ish noise through a lowpass, shaped. Three variants, each used once.
gen whoosh-through 0.65 "(random(0)*2-1)*(t/0.5)^2*exp(-max(t-0.5,0)*30)" "lowpass=f=1400,highpass=f=180"
gen swish-out 0.45 "(random(0)*2-1)*sin(PI*t/0.45)^2" "lowpass=f=2600,highpass=f=400"
gen swish-in 0.45 "(random(0)*2-1)*sin(PI*t/0.45)^3" "lowpass=f=2200,highpass=f=300"

# Steps: wood tick (two uses) and a brighter ding for "live" (the olive beat).
gen wood-tick 0.25 "0.7*sin(2*PI*1850*t)*exp(-t*55) + 0.35*sin(2*PI*620*t)*exp(-t*40) + 0.3*(random(0)*2-1)*exp(-t*260)" "highpass=f=300"
gen live-ding 0.9 "$(bell 1567.98 6)*0.9"

# Proof: a soft pop group for the inclusions, and one wooden thunk for the price.
gen pop-soft 0.18 "0.8*sin(2*PI*(1100*t - 2600*t*t))*exp(-t*38)"
gen price-thunk 0.5 "0.8*sin(2*PI*140*t)*exp(-t*14) + 0.4*sin(2*PI*420*t)*exp(-t*30) + 0.25*(random(0)*2-1)*exp(-t*120)" "lowpass=f=3000"

# The long table: one low slide texture under the whole pan (not a tick per plate).
gen table-slide 5.2 "(random(0)*2-1)*0.5*(1-exp(-t*4))*exp(-max(t-4.6,0)*6)" "lowpass=f=520,highpass=f=60"

# Room tone in place of a music bed: brown noise, low-passed. Mixed at ~0.1.
ffmpeg -hide_banner -loglevel error -y -f lavfi -i "anoisesrc=color=brown:amplitude=0.6:s=$SR:d=60:seed=7" \
  -af "lowpass=f=420,highpass=f=50,volume=-6dB" -ac 1 -c:a libmp3lame -b:a 128k audio/room.mp3

for f in "$OUT"/*.mp3 audio/room.mp3; do
  printf '%-28s ' "$(basename "$f")"
  ffmpeg -hide_banner -i "$f" -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume" | sed -E 's/.*\] //' | tr '\n' ' '
  echo
done
