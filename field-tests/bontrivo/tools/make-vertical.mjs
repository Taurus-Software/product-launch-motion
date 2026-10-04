#!/usr/bin/env node
// make-vertical.mjs: the 9:16 cut as a RE-LAYOUT, not a crop (references/12-deliverables).
// Same frames, same voice, same cues, same timeline: each frame is copied into vertical/
// with its root at 1080×1920, a vertical stylesheet appended after its own (same selectors,
// later rule wins) and the handful of layout numbers its script holds recomputed for the
// tall canvas. Platform safe areas (Reels/TikTok/Shorts): top ~10%, bottom ~20% (captions
// sit at y≈1352, above it), right ~12% at the action rail, so text stays inside x 80–950.
//
// usage: node tools/make-vertical.mjs   (then build + render inside vertical/)
import { readFileSync, writeFileSync, mkdirSync, existsSync, symlinkSync, rmSync } from "node:fs";

const OUT = "vertical";
mkdirSync(`${OUT}/compositions/frames`, { recursive: true });
for (const d of ["assets", "vendor", "audio", "tools", "audio_meta.json", "node_modules"]) {
  if (!existsSync(`${OUT}/${d}`)) symlinkSync(`../${d}`, `${OUT}/${d}`);
}
if (!existsSync(`${OUT}/compositions/lib`)) symlinkSync("../../compositions/lib", `${OUT}/compositions/lib`);

const ROOT = `#root { width: 1080px; height: 1920px; }`;
// Plate centre (540, 520), size 500 → box 290/270. Text column x = 80.
const V = {
  "01-claim": {
    // "DIE APPETIT" at 128px = 1146.9 × 128/168 = 873.8 → left (1080 − 873.8)/2 = 103.
    // Line box 118px at 128px: baseline = (118 − 156)/2 + 0.968·128 = 104.9 below the top.
    // Dot: left 103 + 807.7·128/168 + 5 = 723.4; top (796 + 104.9) − 24 = 876.9 → centre (735.4, 888.9).
    css: `${ROOT}
      .f01-line { left: 103px; height: 150px; }
      .f01-line span { font-size: 128px; line-height: 118px; }
      #f01-l1 { top: 560px; } #f01-l2 { top: 678px; } #f01-l3 { top: 796px; }
      #f01-dot { left: 723.4px; top: 876.9px; width: 24px; height: 24px; }`,
  },
  "02-served": {
    // iris origin = 01's dot centre (735.4, 888.9); farthest corner 1266px → S ≥ 4930 → 10.2
    css: `${ROOT}
      #f02-iris { left: 485.4px; top: 638.9px; }
      #f02-plate { left: 290px; top: 270px; }
      .f02-eyebrow { left: 80px; top: 830px; }
      .f02-line { left: 80px; height: 96px; }
      .f02-line span { font-size: 76px; line-height: 84px; }
      #f02-l1 { top: 872px; } #f02-l2 { top: 956px; } #f02-l3 { top: 1060px; } #f02-l4 { top: 1144px; }
      .f02-body { left: 82px; top: 1250px; font-size: 34px; }`,
    // the serve starts fully off the 1080 canvas (x 290 + 850 = 1140)
    js: [["scale: 11.4", "scale: 10.2"], ["from: { x: 760, y: 26 }", "from: { x: 850, y: 26 }"]],
  },
  "03-speisekarte": {
    css: `${ROOT}
      #f03-plate { left: 290px; top: 270px; }
      #f03-course { left: 465px; top: 445px; }
      .f03-line { left: 80px; height: 108px; }
      .f03-line span { font-size: 86px; line-height: 94px; }
      #f03-l1 { top: 850px; }
      .f03-chip { top: 976px; } #f03-c1 { left: 80px; } #f03-c2 { left: 330px; }
      .f03-body { left: 82px; top: 1078px; }`,
  },
  "04-reservierung": {
    css: `${ROOT}
      #f04-plate { left: 290px; top: 270px; }
      .f04-course { left: 465px; top: 445px; }
      .f04-line { left: 80px; height: 108px; }
      .f04-line span { font-size: 86px; line-height: 94px; }
      #f04-l1 { top: 850px; }
      .f04-body { left: 82px; top: 976px; }
      .f04-rule { left: 82px; top: 1056px; }
      .f04-strong { left: 80px; top: 1074px; }`,
  },
  "05-vorbestellung": {
    css: `${ROOT}
      #f05-carry { left: 290px; top: 270px; }
      .f05-line { left: 80px; height: 108px; }
      .f05-line span { font-size: 86px; line-height: 94px; }
      #f05-l1 { top: 850px; }
      .f05-body { left: 82px; top: 976px; }`,
  },
  "06-branchen": {
    // lock point 680 = centre 540 + the 140px tail, so Catering rests at frame centre
    css: `${ROOT}
      #f06-world { height: 1920px; }
      .f06-runner { top: 600px; }
      .f06-set { top: 640px; }
      .f06-eyebrow { left: 80px; top: 470px; }`,
    js: [["LOCK = 1100", "LOCK = 680"]],
  },
  "07-tage": {
    // steps at x 250 / 540 / 830; links pill-edge to pill-edge with 14px clearance
    css: `${ROOT}
      #f07-steps { width: 1080px; height: 1920px; }
      .f07-step { top: 470px; }
      .f07-link { top: 512px; }
      .f07-label { font-size: 36px; }
      .f07-line { height: 170px; }
      .f07-line span { font-size: 140px; line-height: 150px; }`,
    js: [
      ['style="left:618px;width:284px"', 'style="left:308px;width:174px"'],
      ['style="left:1018px;width:284px"', 'style="left:598px;width:174px"'],
      ['style="left:560px"', 'style="left:250px"'], ['style="left:960px"', 'style="left:540px"'],
      ['style="left:1360px"', 'style="left:830px"'],
      // the sentence stacks, one word group per line, each centred (widths × 140/120)
      ['style="left:222.4px"', 'style="left:313.8px;top:850px"'],
      ['style="left:643.2px"', 'style="left:303.8px;top:1000px"'],
      ['style="left:1081.2px"', 'style="left:184.5px;top:1150px"'],
    ],
  },
  "08-preis": {
    css: `${ROOT}
      .f08-line { left: 80px; height: 130px; }
      .f08-line span { font-size: 110px; line-height: 118px; }
      #f08-l1 { top: 250px; } #f08-l2 { top: 368px; }
      #f08-card { left: 172px; top: 560px; }`,
  },
  "09-cta": {
    // lockup width 920 → scale 1.5945, left 80, centred on y 760 → top 611.7.
    // O centre (80 + 129.93·1.5945, 611.7 + 94.54·1.5945) = (287.2, 762.4); plate box 132.6.
    // Close-up: plate 560 at (540, 740) → K = 560/132.6 = 4.223, T = (252.8, −22.4).
    css: `${ROOT}
      #f09-cam { width: 1080px; height: 1920px; transform-origin: 287.2px 762.4px; }
      #f09-letters { left: 80px; top: 611.7px; width: 920px; height: 296.6px; }
      #f09-plate { left: 220.9px; top: 696.1px; width: 132.6px; height: 132.6px; }
      .f09-tag { width: 1080px; top: 950px; }
      .f09-btn { left: 300px; top: 1030px; }
      .f09-url { left: 437px; top: 1140px; }`,
    js: [["var K = 3.239, TX = 329.8, TY = -3.2;", "var K = 4.223, TX = 252.8, TY = -22.4;"]],
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
