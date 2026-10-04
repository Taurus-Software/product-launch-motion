#!/usr/bin/env node
// make-vertical.mjs (film 2): the 9:16 cut as a RE-LAYOUT, not a crop (references/12).
// Same frames, voice, cues and timeline. Each frame is copied into vertical/ with its root
// at 1080×1920, a vertical stylesheet appended after its own (same selectors, later rule
// wins) and its geometry patched: this film's layout lives largely in SVG path data and
// inline styles, so most patches are exact string replacements, each one checked (a patch
// whose target is missing is an error, never a silent no-op).
// Safe areas (Reels/TikTok/Shorts): text inside x 80–950, nothing important above y 190;
// captions are burned in at y ≈ 1352, so the content stays above ~1300.
//
// usage: node tools/make-vertical.mjs   (then build + render inside vertical/)
import { readFileSync, writeFileSync, mkdirSync, existsSync, symlinkSync } from "node:fs";

const OUT = "vertical";
mkdirSync(`${OUT}/compositions/frames`, { recursive: true });
for (const d of ["assets", "vendor", "audio", "tools", "audio_meta.json", "node_modules"]) {
  if (!existsSync(`${OUT}/${d}`)) symlinkSync(`../${d}`, `${OUT}/${d}`);
}
if (!existsSync(`${OUT}/compositions/lib`)) symlinkSync("../../compositions/lib", `${OUT}/compositions/lib`);

const ROOT = `#root { width: 1080px; height: 1920px; }`;
const SVG = ['viewBox="0 0 1920 1080" width="1920" height="1080"', 'viewBox="0 0 1080 1920" width="1080" height="1920"'];
// a headline whose two words rise separately needs one mask per line once it wraps: with
// both spans in one two-line mask, the first span's hidden state (yPercent 135) sits in the
// second line's slot, visible before its cue
const split = (pre, w1, w2) => [
  `<div class="${pre}-mask" id="${pre}-h"><span id="${pre}-w1">${w1}</span> <span id="${pre}-w2">${w2}</span></div>`,
  `<div class="${pre}-mask" id="${pre}-h"><span id="${pre}-w1">${w1}</span></div>\n      <div class="${pre}-mask" id="${pre}-h2"><span id="${pre}-w2">${w2}</span></div>`,
];

// Shared stage for 01/02: date column at x 80 (112 px: "31. DEZEMBER" = 856 px);
// diagram row y = 900: guest (110, 900) · box 300–580 × 840–960 (280 wide: "Quandoo" is
// 213 px; v1 of this cut had the 16:9 box width, 380–700, and "Ihr Restaurant" (658–950)
// overlapped it) · restaurant (930, 900).
const DATE_CSS = (p) => `
      .${p}-eyebrow { left: 82px; top: 330px; }
      #${p}-date, .${p}-date { left: 80px; top: 370px; height: 134px; font-size: 112px; line-height: 125px; }
      #${p}-year, .${p}-year { left: 80px; top: 500px; height: 72px; font-size: 56px; line-height: 64px; }
      .${p}-label { top: 830px; }
      .${p}-boxl { left: 300px; top: 840px; width: 280px; }`;
// 03/04: labels ABOVE their lines (rows y 600 / 800 / 1000), lines from x 80, solid to 560,
// fading out to 760. 04's box sits under the rows (305–775 × 1100–1220); the three lines
// turn down into its top edge on separate tracks (x 600 / 650 / 700), so none crosses another.
const FADE = ['x1="860" y1="0" x2="1060" y2="0"', 'x1="560" y1="0" x2="760" y2="0"'];
// 05/06: O 260 px centred on (790, 900) → outer radius 128.7, left edge 661.3; its label
// above it (the lines from the lower left would cross it below).
// 09: lockup width 920 → scale 1.5945, left 80, top 611.7; O centre (287.18, 762.44),
// mid radius 49.84, thickness 31.58; plate box 132.58 at (220.89, 696.15).
const V = {
  "01-bruch": {
    css: `${ROOT}${DATE_CSS("f01")}`,
    js: [SVG,
      ['d="M170 760 H812"', 'd="M110 900 H312"'], ['d="M1108 760 H1736"', 'd="M568 900 H916"'],
      ['<rect id="f01-box" x="800" y="700" width="320"', '<rect id="f01-box" x="300" y="840" width="280"'],
      ['<circle id="f01-guest" cx="170" cy="760"', '<circle id="f01-guest" cx="110" cy="900"'],
      ['<circle id="f01-rest" cx="1750" cy="760"', '<circle id="f01-rest" cx="930" cy="900"'],
      ['svgOrigin: "1736 760"', 'svgOrigin: "916 900"'],
      ['id="f01-guest-l" style="left:150px"', 'id="f01-guest-l" style="left:90px"'],
      ['style="left:1478px;width:292px;text-align:right"', 'style="left:658px;width:292px;text-align:right"']],
  },
  "02-export": {
    css: `${ROOT}${DATE_CSS("f02")}`,
    js: [SVG,
      ['d="M170 760 H798"', 'd="M110 900 H298"'],
      ['x="800" y="700" width="320"', 'x="300" y="840" width="280"'],
      ['cx="170" cy="760"', 'cx="110" cy="900"'], ['cx="1750" cy="760"', 'cx="930" cy="900"'],
      ['M960 846 C1010 965 1490 985 1750 850', 'M440 986 C470 1080 800 1100 930 990'],
      ['translate(960 846)', 'translate(440 986)'],
      ['<div class="f02-label" style="left:150px">', '<div class="f02-label" style="left:90px">'],
      ['style="left:1478px;width:292px;text-align:right"', 'style="left:658px;width:292px;text-align:right"']],
  },
  "03-leere": {
    css: `${ROOT}
      .f03-eyebrow { left: 82px; top: 330px; }
      .f03-row { left: 80px; }
      #f03-r1 { top: 520px; } #f03-r2 { top: 720px; } #f03-r3 { top: 920px; }
      .f03-mask { left: 80px; }
      #f03-h1 { top: 1094px; } #f03-h2 { top: 1186px; }`,
    js: [SVG, FADE,
      ['d="M600 440 H1060"', 'd="M80 600 H760"'], ['d="M600 620 H1060"', 'd="M80 800 H760"'],
      ['d="M600 800 H1060"', 'd="M80 1000 H760"']],
  },
  "04-portal": {
    css: `${ROOT}
      .f04-row { left: 80px; }
      .f04-boxl { left: 305px; top: 1100px; }
      .f04-mask { left: 80px; }
      #f04-h { top: 300px; } #f04-h2 { top: 388px; }`,
    js: [SVG, FADE,
      ['style="top:413px">Website-Widget', 'style="top:520px">Website-Widget'],
      ['style="top:593px">Google-Profil', 'style="top:720px">Google-Profil'],
      ['style="top:773px">Instagram', 'style="top:920px">Instagram'],
      ['<path d="M600 440 H861"', '<path d="M80 600 H561"'], ['<path d="M600 620 H861"', '<path d="M80 800 H561"'],
      ['<path d="M600 800 H861"', '<path d="M80 1000 H561"'],
      ['<path d="M860 440 H1060"', '<path d="M560 600 H760"'], ['<path d="M860 620 H1060"', '<path d="M560 800 H760"'],
      ['<path d="M860 800 H1060"', '<path d="M560 1000 H760"'],
      ['d="M860 440 C1080 440 1090 620 1282 620"', 'd="M560 600 H660 Q700 600 700 640 V1112"'],
      ['d="M860 620 H1282"', 'd="M560 800 H610 Q650 800 650 840 V1112"'],
      ['d="M860 800 C1080 800 1090 620 1282 620"', 'd="M560 1000 Q600 1000 600 1040 V1112"'],
      ['x="1270" y="560"', 'x="305" y="1100"'],
      split("f04", "DANN BLEIBT DIE", "ABHÄNGIGKEIT.")],
  },
  "05-direkt": {
    // "RESERVIERUNGEN AB JETZT" wraps after RESERVIERUNGEN (84 px: 836 px; with "AB" 995 > 920)
    css: `${ROOT}
      .f05-mask { left: 80px; width: 920px; }
      .f05-mask span { font-size: 84px; line-height: 92px; white-space: normal; }
      #f05-h1 { top: 300px; height: 196px; white-space: normal; }
      #f05-h2 { top: 484px; height: 104px; }
      #f05-o { left: 660px; top: 770px; width: 260px; height: 260px; }`,
    js: [SVG,
      ['d="M184 620 H1352"', 'd="M124 900 H662"'], ['cx="170" cy="620"', 'cx="110" cy="900"'],
      ['style="left:150px;top:550px"', 'style="left:90px;top:830px"'],
      ['style="left:1364px;top:800px"', 'style="left:654px;top:716px"'],
      ['(1920 * (1 - st.f))', '(1080 * (1 - st.f))']],
  },
  "06-eigen": {
    // channel lines land on the ring at 135° (699, 991) and 115° (735.6, 1016.6)
    css: `${ROOT}
      .f06-mask { left: 80px; }
      #f06-h { top: 300px; } #f06-h2 { top: 404px; }
      .f06-sub { left: 82px; top: 530px; }
      .f06-row { left: 80px; }
      #f06-o { left: 660px; top: 770px; width: 260px; height: 260px; }`,
    js: [SVG,
      ['d="M184 620 H1352"', 'd="M124 900 H662"'], ['cx="170" cy="620"', 'cx="110" cy="900"'],
      ['style="left:150px;top:550px"', 'style="left:90px;top:830px"'],
      ['style="left:1364px;top:800px"', 'style="left:654px;top:716px"'],
      ['style="top:773px">Speisekarte', 'style="top:1123px">Speisekarte'],
      ['style="top:893px">Google-Profil', 'style="top:1233px">Google-Profil'],
      ['d="M452 800 C900 800 1150 700 1357 658.4"', 'd="M382 1150 C560 1150 640 1060 699 991"'],
      ['d="M484 920 C950 920 1180 780 1371.4 694.3"', 'd="M414 1260 C640 1260 720 1120 735.6 1016.6"'],
      split("f06", "IHRE EIGENE", "WEBSITE.")],
  },
  "07-preis": {
    // stacked in the order they are spoken: the fixed price first (top), the per-guest model
    // below it; the flat line at y = 580, continued by 08's line across the push
    css: `${ROOT}
      #f07-left { width: 1080px; height: 1920px; }
      .f07-mask { left: 74px; top: 380px; }
      .f07-per { left: 82px; top: 602px; }
      .f07-small { left: 82px; top: 672px; }
      .f07-guest { top: 960px; }
      .f07-coin { top: 880px; }`,
    js: [SVG,
      ['id="f07-e2" style="left:1052px"', 'id="f07-e2" style="left:82px;top:330px"'],
      ['id="f07-e1" style="left:152px"', 'id="f07-e1" style="left:82px;top:820px"'],
      ['d="M1050 600 H1940"', 'd="M80 580 H1100"'],
      ...[0, 1, 2, 3, 4, 5].flatMap((i) => [
        [`id="f07-g${i}" style="left:${150 + 132 * i}px"`, `id="f07-g${i}" style="left:${80 + 132 * i}px"`],
        [`id="f07-c${i}" style="left:${166 + 132 * i}px"`, `id="f07-c${i}" style="left:${96 + 132 * i}px"`],
      ])],
  },
  "08-hamburg": {
    // "AUS HAMBURG" on line 2: HAMBURG 316–838 → pin (80 px, tip at 87.5 %) on (577, 580)
    css: `${ROOT}
      .f08-mask { left: 80px; }
      #f08-h { top: 300px; } #f08-h2 { top: 404px; }
      .f08-sub { left: 82px; top: 620px; }
      #f08-pin { left: 537px; top: 510px; width: 80px; height: 80px; }`,
    js: [SVG,
      ['d="M-20 600 H1940"', 'd="M-20 580 H1100"'],
      ['B.icon("pin", 96, "#20201E", 1.5)', 'B.icon("pin", 80, "#20201E", 1.5)'],
      split("f08", "EIN TEAM", "AUS HAMBURG")],
  },
  "09-wechseln": {
    css: `${ROOT}
      #f09-letters { left: 80px; top: 611.7px; width: 920px; height: 296.6px; }
      #f09-plate { left: 220.89px; top: 696.15px; width: 132.58px; height: 132.58px; }
      .f09-btn { left: 324.5px; top: 1000px; }
      .f09-url { left: 437.5px; top: 1110px; }
      .f09-legal { left: 90px; width: 900px; top: 1190px; white-space: normal; }`,
    js: [SVG,
      ['d="M-20 492.5 H657.7 A59.59 59.59 0 0 0 657.7 373.32 A59.59 59.59 0 0 0 657.7 492.5"',
        'd="M-20 812.28 H287.18 A49.84 49.84 0 0 0 287.18 712.6 A49.84 49.84 0 0 0 287.18 812.28"'],
      ['C = 2 * Math.PI * 59.59', 'C = 2 * Math.PI * 49.84'],
      ['{ attr: { "stroke-width": 37.76 }', '{ attr: { "stroke-width": 31.58 }']],
  },
};

const film = JSON.parse(readFileSync("film.json", "utf8"));
for (const f of film.frames) {
  let s = readFileSync(f.src, "utf8");
  const v = V[f.id];
  if (!v) throw new Error(`no vertical layout for ${f.id}`);
  s = s.replace('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"');
  for (const [a, b] of v.js || []) {
    if (!s.includes(a)) throw new Error(`${f.id}: vertical patch target not found: ${a}`);
    s = s.split(a).join(b);
  }
  // the vertical stylesheet goes right after the frame's own, inside the template
  s = s.replace("</style>", `</style>\n  <style>\n    /* ── 9:16 re-layout (tools/make-vertical.mjs) ── */\n    ${v.css}\n  </style>`);
  writeFileSync(`${OUT}/${f.src}`, s);
}
const vf = { ...film, width: 1080, height: 1920, _note: ["9:16 re-layout of ../film.json, generated by tools/make-vertical.mjs"] };
writeFileSync(`${OUT}/film.json`, JSON.stringify(vf, null, 2) + "\n");
console.log(`✓ ${film.frames.length} frames re-laid out into ${OUT}/ (1080×1920)`);
