#!/usr/bin/env node
// check-durations.mjs: trap 4 (root and clip durations disagree → a frame blanks before its
// cut). Compares every frame's #root data-duration, each of its .clip data-durations and its
// timeline's explicit length against the wrapper duration assemble.mjs wrote into index.html.
import { readFileSync } from "node:fs";
const index = readFileSync("index.html", "utf8");
let bad = 0;
for (const m of index.matchAll(/data-composition-id="([^"]+)"\s+data-composition-src="([^"]+)"\s+data-start="([\d.]+)"\s+data-duration="([\d.]+)"/g)) {
  const [, id, src, , dur] = m;
  const html = readFileSync(src, "utf8");
  const root = html.match(/data-composition-id="[^"]+"[^>]*data-duration="([\d.]+)"/)?.[1];
  const clips = [...html.matchAll(/class="clip[^"]*"[^>]*data-duration="([\d.]+)"/g)].map((x) => x[1]);
  const anchor = html.match(/tl\.to\(\{\}, \{ duration: ([\d.]+) \}, 0\)/)?.[1];
  const all = [root, ...clips, anchor];
  const ok = all.every((v) => v === dur);
  if (!ok) bad++;
  console.log(`${ok ? "✓" : "✗"} ${id.padEnd(18)} wrapper ${dur}  root ${root}  clips ${[...new Set(clips)].join(",")}  anchor ${anchor}`);
}
process.exit(bad ? 1 : 0);
