#!/usr/bin/env bash
# sfx.sh (film 3): the split in sound. DIRECTION: STEREO is the device. The guest's side
# sits LEFT, the team's side RIGHT (in the 16:9 frame: cream left, ink right), so a muted
# viewer sees the split and a listener hears it. The real-time moment is the same sound
# answered on the other side; the bag crosses the stereo field as it crosses the counter;
# one service bell at the pass on „pünktlich“; the brand chord (films 1-2) resolves.
# Everything is synthesised: no third-party samples, nothing to license.
# chord-c, sub-drop, bean-tick, price-thunk are copied from film 1's kit.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=audio/sfx; SR=48000; mkdir -p "$OUT"

# mono source, then placed: gen <name> <dur> <expr> <gainL> <gainR> [extra -af]
gen() {
  ffmpeg -hide_banner -loglevel error -y -f lavfi -i "aevalsrc=exprs='$3':s=$SR:d=$2" \
    -af "${6:-anull},pan=stereo|c0=$4*c0|c1=$5*c0,alimiter=limit=0.89:level=disabled" \
    -c:a libmp3lame -b:a 192k "$OUT/$1.mp3"
}
# true stereo source (two expressions, for movement): gen2 <name> <dur> <exprL> <exprR> [-af]
gen2() {
  ffmpeg -hide_banner -loglevel error -y -f lavfi -i "aevalsrc=exprs='$3|$4':c=stereo:s=$SR:d=$2" \
    -af "${5:-anull},alimiter=limit=0.89:level=disabled" -c:a libmp3lame -b:a 192k "$OUT/$1.mp3"
}

# The team's side opens from the seam (F01): a soft air move with a low body, on the right.
gen open-r 0.7 "(0.5*(random(0)*2-1)*sin(PI*min(t/0.55,1))^2 + 0.5*sin(2*PI*90*t)*exp(-t*5)*min(t/0.05,1))*min((0.7-t)/0.08,1)" 0.30 1.0 "lowpass=f=1600"

# An order is placed (guest, LEFT) and the same order arrives (team, RIGHT): one timbre, a
# soft wooden tap with a short pitched body, so the right one reads as the same event.
TAP="0.65*sin(2*PI*1320*t)*exp(-t*38) + 0.35*sin(2*PI*660*t)*exp(-t*24) + 0.25*(random(0)*2-1)*exp(-t*300)"
gen tap-l 0.3 "$TAP" 1.0 0.22 "highpass=f=200"
gen tap-r 0.3 "$TAP" 0.22 1.0 "highpass=f=200"

# The team sets the pickup time (RIGHT): a short ratchet, 6 detents over 0.42 s. (v1 was
# 8 dB under the other cues after the band-pass and measured only +4 dB over the voice in
# the delivered file; the detents are now 2.5x hotter, the limiter holds the peaks.)
gen ratchet-r 0.5 "2.5*(0.8*(random(0)*2-1)*exp(-mod(t,0.07)*260)*lt(t,0.42) + 0.3*sin(2*PI*2100*t)*exp(-mod(t,0.07)*180)*lt(t,0.42))" 0.25 1.0 "bandpass=f=2200:width_type=o:w=1.6"

# The bag crosses the counter right → left (F05): a paper swish whose pan travels with it.
# The pan turns over between 0.10 and 0.30 s, centred on 0.20 s = the seam crossing (the
# cue starts 0.20 s before „pünktlich“). v1 panned linearly over the whole 0.4 s and read
# only 3 dB left in its second half against the centred voice and bell.
SW="(random(0)*2-1)*sin(PI*t/0.4)^2"
PL="min(max((t-0.1)/0.2,0),1)"
gen2 swish-rl 0.4 "$SW*$PL" "$SW*(1-$PL)" "bandpass=f=1800:width_type=o:w=2"

# The service bell at the pass (centre): inharmonic partials of a counter bell, long ring.
gen bell 1.8 "(0.5*sin(2*PI*2490*t) + 0.32*sin(2*PI*3610*t) + 0.2*sin(2*PI*5230*t) + 0.12*sin(2*PI*1245*t))*exp(-t*2.4)*min(t/0.003,1)" 1.0 1.0

# The claim, set across the counter (F07): two soft ticks, left then right.
TICK="0.6*sin(2*PI*1850*t)*exp(-t*60) + 0.3*sin(2*PI*930*t)*exp(-t*40)"
gen tick-l 0.25 "$TICK" 1.0 0.25 "highpass=f=300"
gen tick-r 0.25 "$TICK" 0.25 1.0 "highpass=f=300"

for f in "$OUT"/*.mp3; do
  printf '%-18s ' "$(basename "$f")"
  ffmpeg -hide_banner -i "$f" -af "astats=measure_overall=none:measure_perchannel=RMS_level" -f null /dev/null 2>&1 \
    | grep -E "RMS level dB" | sed -E 's/.*RMS level dB: //' | tr '\n' ' '
  echo
done
