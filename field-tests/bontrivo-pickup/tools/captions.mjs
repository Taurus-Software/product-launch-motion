#!/usr/bin/env node
// captions.mjs: caption cards from the word timings the film was cut against
// (references/12-deliverables.md: strictly better than re-transcribing, because they match
// the shipped audio). Writes an .srt and, with --burn, injects the cards into an assembled
// index as clips (idempotent, marked block), set in the film's own typeface.
//
// Cards: break at clause punctuation (not after an ordinal like "31.") once a card holds
// ~18+ chars; a card over MAX chars is split at its most balanced word boundary, never
// after a short function word; ≤ 2 lines. Times: first word's start → next card's start (or last word end + 0.35s,
// capped at the frame's hold).
//
// usage: node tools/captions.mjs --index index.html --srt out.srt [--burn --y 1352 --width 1080]
import { readFileSync, writeFileSync } from "node:fs";

const argv = process.argv.slice(2);
const flag = (n, d) => { const i = argv.indexOf(`--${n}`); return i === -1 ? d : argv[i + 1]; };
const INDEX = flag("index", "index.html");
const SRT = flag("srt", null);
const BURN = argv.includes("--burn");
const Y = Number(flag("y", 1352));
const MAX = Number(flag("max", 56)); // a card may wrap to two ~38-char lines; breaks prefer punctuation

const meta = JSON.parse(readFileSync("audio_meta.json", "utf8"));
const script = JSON.parse(readFileSync("tools/script.json", "utf8"));
let html = readFileSync(INDEX, "utf8");
const W = Number(html.match(/data-composition-id="main"[^>]*data-width="(\d+)"/)?.[1] ?? 1920);

// frame starts and holds, off the assembled wrappers (the truth after transitions)
const frames = {};
for (const m of html.matchAll(/data-composition-id="([^"]+)"\s+data-composition-src="[^"]+"\s+data-start="([\d.]+)"\s+data-duration="([\d.]+)"/g)) {
  frames[m[1]] = { start: Number(m[2]), dur: Number(m[3]) };
}
const ids = Object.keys(frames);
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9äöüß]/g, "");

const cards = [];
ids.forEach((id, fi) => {
  const f = frames[id];
  const holdEnd = fi < ids.length - 1 ? frames[ids[fi + 1]].start : f.start + f.dur;
  const words = meta[id].words;
  const tokens = script.frames.find((x) => x.id === id).text.split(/\s+/);
  // map each caption token to the start of a measured word: positional when the counts
  // agree ("Neunundzwanzig" ↔ "29,00 €"), else by concatenating word groups until the
  // token is covered ("bontrivo.de." ↔ "bontrivo" "." "d" "e.")
  const timed = [];
  if (tokens.length === words.length) {
    tokens.forEach((t, i) => timed.push({ t, start: words[i].start, end: words[i].end }));
  } else {
    let wi = 0;
    for (const t of tokens) {
      const target = norm(t); let acc = ""; const s = words[wi].start; let e = words[wi].end;
      while (wi < words.length && acc.length < target.length) { acc += norm(words[wi].w); e = words[wi].end; wi++; }
      if (acc !== target) throw new Error(`${id}: cannot align caption token "${t}" (got "${acc}")`);
      timed.push({ t, start: s, end: e });
    }
  }
  // clauses end at punctuation, but an ordinal ("1.", "31.") is not a full stop: film 2's
  // first cut split "… bis zum 31." | "Dezember." across two cards. "?" and "!" end a
  // clause too (it merged "… Portal? Dann bleibt die" | "Abhängigkeit.").
  const txt = (ws) => ws.map((x) => x.t).join(" ");
  const ends = (t) => /[.,:;?!]$/.test(t) && !/^\d+\.$/.test(t);
  const clauses = [];
  let cl = [];
  for (const w of timed) { cl.push(w); if (ends(w.t)) { clauses.push(cl); cl = []; } }
  if (cl.length) clauses.push(cl);
  // a card over MAX splits at the word boundary nearest its middle (balanced), never
  // greedily: greedy filling left "über Quandoo." alone on a one-second card
  const fit = (ws) => {
    const L = txt(ws).length;
    if (L <= MAX || ws.length < 2) return [ws];
    let k = 1, best = Infinity;
    for (let j = 1; j < ws.length; j++) {
      // a card should not end on a short function word ("nur", "die", "im"): it belongs
      // to the phrase that follows ("nur noch bis zum 31. Dezember.")
      const last = ws[j - 1].t;
      const d = Math.abs(txt(ws.slice(0, j)).length - L / 2) + (/^[a-zäöüß]{1,3}$/.test(last) ? 4 : 0);
      if (d < best) { best = d; k = j; }
    }
    return [...fit(ws.slice(0, k)), ...fit(ws.slice(k))];
  };
  let cur = [];
  const flush = () => { for (const p of fit(cur)) if (p.length) cards.push({ id, words: p }); cur = []; };
  // short clauses ("bei Instagram:") join the next one; a card that already reads as a
  // phrase (18+ chars) is closed at its clause boundary
  for (const c of clauses) {
    if (cur.length && (txt(cur).length >= 18 || txt([...cur, ...c]).length > MAX)) flush();
    cur = [...cur, ...c];
  }
  flush();
  // timings, absolute
  const mine = cards.filter((c) => c.id === id);
  mine.forEach((c, i) => {
    c.start = f.start + c.words[0].start;
    const next = mine[i + 1];
    c.end = next ? f.start + next.words[0].start : Math.min(f.start + c.words.at(-1).end + 0.35, holdEnd);
    c.text = c.words.map((x) => x.t).join(" ");
  });
});

const ts = (s) => {
  const ms = Math.round(s * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60;
  const sec = Math.floor(ms / 1000) % 60, r = ms % 1000;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")},${String(r).padStart(3, "0")}`;
};
if (SRT) {
  writeFileSync(SRT, cards.map((c, i) => `${i + 1}\n${ts(c.start)} --> ${ts(c.end)}\n${c.text}\n`).join("\n"));
  console.log(`✓ ${SRT}: ${cards.length} cards, longest ${Math.max(...cards.map((c) => c.text.length))} chars`);
}

if (BURN) {
  const OPEN = "<!-- captions:start -->", CLOSE = "<!-- captions:end -->";
  html = html.replace(new RegExp(`\\n?[ \\t]*${OPEN}[\\s\\S]*?${CLOSE}`, "g"), "");
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const items = cards.map((c, i) =>
    `    <div id="cap-${String(i).padStart(2, "0")}" class="clip cap" data-start="${c.start.toFixed(3)}" data-duration="${(c.end - c.start).toFixed(3)}" data-track-index="970"><span>${esc(c.text)}</span></div>`);
  const block = `
    ${OPEN}
    <style>
      @font-face { font-family: "Montserrat"; src: url("assets/fonts/montserrat-variable-latin.woff2") format("woff2-variations"); font-weight: 100 900; font-display: block; }
      /* Captions sit above the platform's bottom chrome (bottom ~20%), in the film's face,
         on an ink plate: legible on both registers, never over the plate or a figure. */
      .cap { position: absolute; left: 0; width: ${W}px; top: ${Y}px; z-index: 8000; text-align: center; pointer-events: none; }
      .cap span { display: inline-block; max-width: ${Math.round(W * 0.82)}px; padding: 14px 26px; border-radius: 14px;
        background: rgba(32, 32, 30, 0.86); color: #fff4e7; font-family: "Montserrat", sans-serif;
        font-size: 40px; line-height: 52px; font-weight: 700; }
    </style>
${items.join("\n")}
    ${CLOSE}`;
  const anchor = html.lastIndexOf("</body>");
  writeFileSync(INDEX, html.slice(0, anchor) + block + "\n  " + html.slice(anchor));
  console.log(`✓ burned ${cards.length} caption cards into ${INDEX} at y=${Y}`);
}
for (const c of cards) console.log(`  ${c.start.toFixed(2).padStart(6)}–${c.end.toFixed(2).padEnd(6)} ${c.text}`);
