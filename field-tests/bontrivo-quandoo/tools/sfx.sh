#!/usr/bin/env bash
# sfx.sh (film 2): the line's sound. DIRECTION: a held tone that FOLLOWS the line and
# STOPS when it breaks (the silence is the cue), returns brighter when the line reaches
# the restaurant, and resolves in the brand chord from film 1 (chord-c, copied over:
# the same resolution in both films is a sonic logo, not a repetition).
# Everything is synthesised: no third-party samples, nothing to license.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=audio/sfx; SR=48000; mkdir -p "$OUT"

gen() { # name duration expression [extra -af]
  ffmpeg -hide_banner -loglevel error -y -f lavfi -i "aevalsrc=exprs='$3':s=$SR:d=$2" \
    -af "${4:-anull},alimiter=limit=0.89:level=disabled" -ac 1 -c:a libmp3lame -b:a 192k "$OUT/$1.mp3"
}

# The portal tone: A3 + E4, a slow 0.25 Hz beat between two detuned partials so it is
# alive without moving. Exactly as long as the line runs before it breaks (frame 01:
# "keine"@1.70 → 1.72s incl. a 12 ms release), so it ends ON the break, not on a seam.
# 0.1 s attack only: the film opens mid-motion, so the tone is already there.
gen tone-portal 1.72 "(0.34*sin(2*PI*220*t)+0.20*sin(2*PI*220.5*t)+0.24*sin(2*PI*329.6*t)+0.10*sin(2*PI*440*t))*min(t/0.1,1)*min((1.72-t)/0.012,1)"

# The break: a dry crack (bright noise, 25 ms) over a low thud. One hit, then nothing.
gen snap 0.45 "0.55*(random(0)*2-1)*exp(-t*140) + 0.7*sin(2*PI*70*t)*exp(-t*16) + 0.25*sin(2*PI*1900*t)*exp(-t*90)" "highpass=f=40"

# "Ins Leere": the three dead ends exhale once, a glide that falls and fades.
gen glide-down 1.2 "0.5*sin(2*PI*(392*t - 70*t*t))*exp(-t*2.2)*min(t/0.04,1)" "lowpass=f=1800"

# The register wipe at the turn (once): it runs as long as the wipe (frame 05: 0 → 1.22,
# power2.out, so most of the travel is early), an air move that swells fast, then settles
# under the landing.
gen wipe-air 1.3 "(random(0)*2-1)*min(t/0.25,1)*exp(-max(t-0.25,0)*2.6)*min((1.3-t)/0.05,1)" "lowpass=f=2400,highpass=f=300"

# Connected: a bright two-note FM bell (G5 then C6), the olive moment.
bell() { echo "0.6*sin(2*PI*$1*t + 1.4*exp(-t*9)*sin(2*PI*$1*2.756*t))*exp(-t*$2)"; }
gen connect 1.2 "$(bell 783.99 3.5) + $(bell 1046.5 3.2)*gt(t,0.09)*0.9"

# Own-channel tone: C4 + G4 + E5, warmer and brighter than the portal tone. It enters with
# the line at the turn (05 @ 0.0, fading in with the wipe over 1.2 s) and carries through
# the benefits; its 1.4 s fade-out starts 0.31 s into 09 and is still sounding when the
# brand chord enters on "bontrivo" (09 @ 1.47), so the tone resolves INTO the chord.
# Length from the assembled starts: 05 @ 17.579 → fade end 37.40 = 19.82 s.
gen tone-own 19.82 "(0.30*sin(2*PI*261.6*t)+0.16*sin(2*PI*262.1*t)+0.22*sin(2*PI*392*t)+0.10*sin(2*PI*659.3*t))*min(t/1.2,1)*min((19.82-t)/1.4,1)"

# Channels connecting (used twice: Speisekarte, Google-Profil): a short rising zip.
gen zip-up 0.35 "0.6*sin(2*PI*(600*t + 2400*t*t))*sin(PI*t/0.35)^2"

# The Hamburg pin: a wood tick.
gen pin-tick 0.25 "0.7*sin(2*PI*1850*t)*exp(-t*55) + 0.35*sin(2*PI*620*t)*exp(-t*40) + 0.3*(random(0)*2-1)*exp(-t*260)" "highpass=f=300"

for f in "$OUT"/*.mp3; do
  printf '%-22s ' "$(basename "$f")"
  ffmpeg -hide_banner -i "$f" -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume" | sed -E 's/.*\] //' | tr '\n' ' '
  echo
done
