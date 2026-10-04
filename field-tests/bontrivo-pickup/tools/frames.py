#!/usr/bin/env python3
"""frames.py: writes compositions/frames/*.html for film 3. EDIT HERE, not in the frames.

Why a generator: the film is one locked stage (DIRECTION: a split frame, hard cuts only).
Grounds, side labels, icons, order tags, the clock and the bag persist across cuts, and a
hard cut only stays invisible if the persisted parts are drawn identically on both sides of
it. Writing them once, here, makes that true by construction; each frame then adds only its
own copy and its own timeline. The output is ordinary HyperFrames HTML (one template, one
paused GSAP timeline per frame), readable and committed.

Both formats live in each frame: the 16:9 layout is the default CSS, the 9:16 layout is
the same selectors under `#root[data-width="1080"]`. tools/make-vertical.mjs only swaps the
root's declared size; nothing is string-patched.

Durations come from the assembled index (run assemble.mjs first, then this, then the chain
again): a frame's root/clip durations must equal its wrapper's (trap 4).

usage: python3 tools/frames.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = json.loads((ROOT / "audio_meta.json").read_text())
INDEX = (ROOT / "index.html").read_text()
DUR = {m[1]: m[2] for m in re.finditer(
    r'data-composition-id="([^"]+)"\s+data-composition-src="[^"]+"\s+data-start="[\d.]+"\s+data-duration="([\d.]+)"', INDEX)}

PORT = '#root[data-width="1080"]'


def stage_css(p):
    """The stage both formats share. 16:9: guest | team at x 960. 9:16: guest / team at y 760."""
    return f"""
    @font-face {{
      font-family: "Montserrat";
      src: url("assets/fonts/montserrat-variable-latin.woff2") format("woff2-variations");
      font-weight: 100 900;
      font-display: block;
    }}
    #root {{
      position: relative; width: 1920px; height: 1080px; overflow: hidden;
      font-family: "Montserrat", sans-serif; -webkit-font-smoothing: antialiased; color: #20201e;
    }}
    {PORT} {{ width: 1080px; height: 1920px; }}
    /* grounds: the guest's side cream, the team's side ink */
    .{p}-cream {{ position: absolute; inset: 0; background: #fff4e7; }}
    .{p}-ink {{ position: absolute; left: 960px; top: 0; width: 960px; height: 1080px; background: #20201e; }}
    {PORT} .{p}-ink {{ left: 0; top: 760px; width: 1080px; height: 1160px; }}
    /* two-colourway layers: the same object drawn ink (guest half) and cream (team half) */
    .{p}-gh {{ position: absolute; inset: 0; clip-path: inset(0px 960px 0px 0px); }}
    .{p}-th {{ position: absolute; inset: 0; clip-path: inset(0px 0px 0px 960px); }}
    {PORT} .{p}-gh {{ clip-path: inset(0px 0px 1160px 0px); }}
    {PORT} .{p}-th {{ clip-path: inset(760px 0px 0px 0px); }}
    /* side labels */
    .{p}-eb {{ position: absolute; top: 150px; font-size: 26px; line-height: 32px; font-weight: 700;
      letter-spacing: 0.14em; text-transform: uppercase; white-space: nowrap; }}
    .{p}-eg {{ right: 1020px; text-align: right; color: #85817a; }}
    .{p}-et {{ left: 1020px; color: #a69f97; }}
    {PORT} .{p}-eg {{ right: auto; left: 82px; top: 200px; text-align: left; }}
    {PORT} .{p}-et {{ left: 82px; top: 1030px; }}
    /* copy slots, mirror-set: guest copy flush right to the seam, team copy flush left */
    .{p}-m {{ position: absolute; overflow: hidden; white-space: nowrap; }}
    .{p}-m span {{ display: inline-block; }}
    .{p}-h {{ height: 84px; font-size: 64px; line-height: 72px; font-weight: 900; letter-spacing: 0.005em; }}
    .{p}-g {{ right: 1020px; text-align: right; }}
    .{p}-t {{ left: 1020px; color: #fff4e7; }}
    .{p}-r1 {{ top: 220px; }} .{p}-r2 {{ top: 296px; }}
    .{p}-sub {{ position: absolute; top: 304px; font-size: 34px; line-height: 42px; font-weight: 500; white-space: nowrap; }}
    .{p}-sub.{p}-g {{ color: #55534c; }} .{p}-sub.{p}-t {{ color: #a69f97; }}
    {PORT} .{p}-h {{ height: 74px; font-size: 56px; line-height: 62px; }}
    {PORT} .{p}-g {{ right: auto; left: 80px; text-align: left; }}
    {PORT} .{p}-t {{ left: 80px; }}
    {PORT} .{p}-g.{p}-r1 {{ top: 250px; }} {PORT} .{p}-g.{p}-r2 {{ top: 312px; }}
    {PORT} .{p}-t.{p}-r1 {{ top: 1074px; }} {PORT} .{p}-t.{p}-r2 {{ top: 1136px; }}
    {PORT} .{p}-sub.{p}-g {{ top: 322px; left: 82px; }} {PORT} .{p}-sub.{p}-t {{ top: 1146px; left: 82px; }}
    /* the cast: guest, team, the order on both sides, the clock on the seam, the bag */
    .{p}-gi {{ position: absolute; left: 255px; top: 545px; width: 150px; height: 150px; }}
    .{p}-ti {{ position: absolute; left: 1515px; top: 545px; width: 150px; height: 150px; }}
    .{p}-tag {{ position: absolute; top: 576px; width: 88px; height: 88px; }}
    .{p}-gtag {{ left: 516px; }} .{p}-ttag {{ left: 1316px; }}
    .{p}-clk {{ position: absolute; left: 780px; top: 440px; width: 360px; height: 360px; }}
    .{p}-bag {{ position: absolute; left: 1535px; top: 805px; width: 110px; height: 110px; }}
    .{p}-bag.{p}-at-guest {{ left: 275px; }}
    .{p}-ok {{ position: absolute; left: 352px; top: 790px; width: 46px; height: 46px; }}
    {PORT} .{p}-gi {{ left: 135px; top: 535px; width: 130px; height: 130px; }}
    {PORT} .{p}-ti {{ left: 135px; top: 855px; width: 130px; height: 130px; }}
    {PORT} .{p}-tag {{ width: 80px; height: 80px; }}
    {PORT} .{p}-gtag {{ left: 320px; top: 560px; }} {PORT} .{p}-ttag {{ left: 320px; top: 880px; }}
    {PORT} .{p}-clk {{ left: 656px; top: 616px; width: 288px; height: 288px; }}
    {PORT} .{p}-bag {{ left: 465px; top: 945px; }}
    {PORT} .{p}-bag.{p}-at-guest {{ left: 465px; top: 465px; }}
    {PORT} .{p}-ok {{ left: 542px; top: 450px; }}
    /* centred copy (price, CTA) */
    .{p}-cen {{ position: absolute; left: 0; width: 1920px; text-align: center; white-space: nowrap; }}
    {PORT} .{p}-cen {{ width: 1080px; }}"""


def cues(fid):
    w = META[fid]["words"]
    s = "  ".join(f'"{x["w"]}"@{x["start"]:.2f}' for x in w)
    lines, cur = [], ""
    for part in s.split("  "):
        if len(cur) + len(part) > 84:
            lines.append(cur.rstrip()); cur = ""
        cur += part + "  "
    lines.append(cur.rstrip())
    return "\n         ".join(lines)


def frame(fid, comment, markup, js, css="", vo=""):
    p = "f" + fid[:2]
    D = DUR[fid]
    return f"""<!--
{comment.strip()}
  (Generated by tools/frames.py; edit there.)
-->
<template>
  <script src="vendor/gsap.min.js"></script>
  <script src="compositions/lib/btv-brand.js"></script>
  <script src="compositions/lib/btv.js"></script>
  <script src="compositions/lib/split.js"></script>
  <style>{stage_css(p)}{css.replace("{p}", p).replace("{PORT}", PORT)}
  </style>

  <div id="root" data-composition-id="{fid}" data-width="1920" data-height="1080" data-duration="{D}">
    <div class="clip {p}-cream" id="{p}-cream" data-start="0" data-duration="{D}" data-track-index="0"></div>
    <div id="{p}-layer-1" class="clip" data-start="0" data-duration="{D}" data-track-index="1" style="position:absolute;inset:0">
      <div class="{p}-ink" id="{p}-ink"></div>
{markup.replace("{p}", p).rstrip()}
    </div>
  </div>

  <script>
    (function () {{
      /* VO: "{vo}"
         {cues(fid)}
         duration {META[fid]["duration"]:.3f}s · hold {D} · hard cut out */
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
      var B = window.BTV, S = window.SP, G = S.geo("{fid}");
{js.replace("{p}", p).rstrip()}

      tl.to({{}}, {{ duration: {D} }}, 0);
      window.__timelines["{fid}"] = tl;
    }})();
  </script>
</template>
"""


# ── persistent pieces (markup + the JS that fills them) ─────────────────────────────────
EYEBROWS = """      <div class="{p}-eb {p}-eg" id="{p}-eg">Gast</div>
      <div class="{p}-eb {p}-et" id="{p}-et">Ihr Team</div>"""
ICONS = """      <div class="{p}-gi" id="{p}-gi"></div>
      <div class="{p}-ti" id="{p}-ti"></div>"""
ICONS_JS = """      document.getElementById("{p}-gi").innerHTML = B.icon("guest", "100%", S.INK, 1.5);
      document.getElementById("{p}-ti").innerHTML = B.icon("cloche", "100%", S.CREAM, 1.5);"""
TAGS = """      <div class="{p}-tag {p}-gtag" id="{p}-gtag"></div>
      <div class="{p}-tag {p}-ttag" id="{p}-ttag"></div>"""
TAGS_JS = """      S.tag(document.getElementById("{p}-gtag"));
      S.tag(document.getElementById("{p}-ttag"));"""


def two(inner_g, inner_t):
    """the two-colourway layer pair, then the single-colour arc layer goes above it.
    Text copies in the team layer carry data-layout-allow-overlap: the auditor sees two text
    boxes at the same place, but each copy is clipped to its own half (clip-path), so on
    screen they never overlap; the auditor does not model clip-path (as in film 2's wipe)."""
    return f"""      <div class="{{p}}-gh" id="{{p}}-gh">
{inner_g}
      </div>
      <div class="{{p}}-th" id="{{p}}-th">
{inner_t}
      </div>"""


CLOCK_G = """        <div class="{p}-clk" id="{p}-clk-g"></div>"""
CLOCK_T = """        <div class="{p}-clk" id="{p}-clk-t"></div>"""
ARC = """      <div class="{p}-clk" id="{p}-arc"></div>"""
CLOCK_JS = """      S.clock(document.getElementById("{p}-clk-g"), S.INK, "{p}-hand");
      S.clock(document.getElementById("{p}-clk-t"), S.CREAM, "{p}-hand");
      S.arc(document.getElementById("{p}-arc"), "{p}-arcg");"""
BAG_G = """        <div class="{p}-bag{cls}" id="{p}-bag-g"></div>"""
BAG_T = """        <div class="{p}-bag{cls}" id="{p}-bag-t"></div>"""
BAG_JS = """      document.getElementById("{p}-bag-g").innerHTML = B.icon("bag", "100%", S.INK, 1.5);
      document.getElementById("{p}-bag-t").innerHTML = B.icon("bag", "100%", S.CREAM, 1.5);"""
OK = """        <div class="{p}-ok" id="{p}-ok"></div>"""
OK_JS = """      document.getElementById("{p}-ok").innerHTML = '<svg viewBox="0 0 46 46" width="100%" height="100%">' +
        '<circle cx="23" cy="23" r="23" fill="#B7CF4A"/><path d="M13 23.5l6.5 6.5L33 16.5" fill="none" stroke="#20201E" ' +
        'stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>';"""

ARC_AT = 105  # the pickup time the team sets (degrees clockwise from 12): on the team's side

FRAMES = {}

# ── 01 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["01-split"] = dict(
    vo="Vorbestellen und abholen, ganz einfach.",
    comment="""
  01-split: the opening. The frame is one cream field; the team's side opens from the seam
  outwards (16:9: rightwards, 9:16: downwards) and stays open for the whole film. The
  headline is set ACROSS the counter: „VORBESTELLEN“ flush right on the guest's side,
  „UND ABHOLEN.“ flush left on the team's; under them „ganz | einfach.“
  16:9: 92 px, „VORBESTELLEN“ = 789 px → 111–900, „UND ABHOLEN.“ = 773 px → 1020–1793.""",
    css="""
    .{p}-ink { clip-path: inset(0% 100% 0% 0%); }
    {PORT} .{p}-ink { clip-path: inset(0% 0% 100% 0%); }
    .{p}-eb { opacity: 0; }
    .{p}-big { height: 112px; font-size: 92px; line-height: 104px; font-weight: 900; letter-spacing: 0.005em; top: 420px; }
    .{p}-small { position: absolute; top: 548px; font-size: 44px; line-height: 54px; font-weight: 500; white-space: nowrap; opacity: 0; }
    .{p}-small.{p}-t { color: #fff4e7; }
    {PORT} .{p}-big.{p}-g { top: 520px; } {PORT} .{p}-small.{p}-g { top: 646px; left: 82px; }
    {PORT} .{p}-big.{p}-t { top: 790px; } {PORT} .{p}-small.{p}-t { top: 916px; left: 82px; }""",
    markup=EYEBROWS + """
      <div class="{p}-m {p}-big {p}-g" id="{p}-mg"><span id="{p}-wg">VORBESTELLEN</span></div>
      <div class="{p}-m {p}-big {p}-t" id="{p}-mt"><span id="{p}-wt">UND ABHOLEN.</span></div>
      <div class="{p}-small {p}-g" id="{p}-sg">ganz</div>
      <div class="{p}-small {p}-t" id="{p}-st">einfach.</div>""",
    js="""
      // the team's side opens from the seam (0 → 0.55), one sound on the right (open-r)
      var ink = document.getElementById("{p}-ink"), st = { p: 0 };
      tl.fromTo(st, { p: 0 }, { p: 1, duration: 0.55, ease: "power3.inOut", immediateRender: false,
        onUpdate: function () { ink.style.clipPath = S.openClip(G, st.p); } }, 0.0);
      tl.fromTo(["#{p}-eg", "#{p}-et"], { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 0.5);
      // "Vorbestellen"@0.24 · "und abholen"@1.01 · "ganz"@1.82 · "einfach."@2.02
      B.rise(tl, "#{p}-wg", 0.24);
      B.rise(tl, "#{p}-wt", 1.01);
      B.arrive(tl, "#{p}-sg", 1.82, { y: 10, dur: 0.28 });
      B.arrive(tl, "#{p}-st", 2.02, { y: 10, dur: 0.28 });""")

# ── 02 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["02-gast"] = dict(
    vo="Ihre Gäste bestellen vor, direkt über Ihre Website.",
    comment="""
  02-gast: hard cut, the stage holds. The guest's side only: the guest arrives on „Gäste“,
  the copy on „bestellen“, and on „vor“ the order appears beside the guest (a tomato tag,
  no interface: none is described, BRIEF). The team's side stays empty and dark: it has not
  heard of the order yet. Sound: tap-l, panned to the guest's side.""",
    css="""
    .{p}-gi, .{p}-gtag, #{p}-sg { opacity: 0; }""",
    markup=EYEBROWS + """
      <div class="{p}-gi" id="{p}-gi"></div>
      <div class="{p}-tag {p}-gtag" id="{p}-gtag"></div>
      <div class="{p}-m {p}-h {p}-g {p}-r1"><span id="{p}-w1">BESTELLEN VOR.</span></div>
      <div class="{p}-sub {p}-g" id="{p}-sg">direkt über Ihre Website</div>""",
    js="""
      document.getElementById("{p}-gi").innerHTML = B.icon("guest", "100%", S.INK, 1.5);
      S.tag(document.getElementById("{p}-gtag"));
      // "Gäste"@0.31 · "bestellen"@0.63 · "vor,"@1.02 (the order) · "direkt"@1.52
      B.arrive(tl, "#{p}-gi", 0.31, { y: 16, dur: 0.3 });
      B.rise(tl, "#{p}-w1", 0.63);
      tl.fromTo("#{p}-gtag", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power3.out" }, 1.0);
      B.arrive(tl, "#{p}-sg", 1.52, { y: 10, dur: 0.3 });""")

# ── 03 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["03-echtzeit"] = dict(
    vo="Ihr Team sieht die Bestellung in Echtzeit.",
    comment="""
  03-echtzeit: hard cut; the guest's side holds (guest, order, copy). The team arrives on
  „Team“, its line on „sieht“, and on „Echtzeit“ the same order appears on the team's side,
  mirrored across the counter, in the same frame; both tags pulse once together. Real time
  is shown as simultaneity, not as travel: nothing crosses the seam. Sound: tap-r, the same
  tap as the guest's, now on the right.""",
    css="""
    .{p}-ti, .{p}-ttag, #{p}-ts, .{p}-pulse { opacity: 0; }
    .{p}-pulse { position: absolute; }""",
    markup=EYEBROWS + ICONS + TAGS + """
      <div class="{p}-tag {p}-gtag {p}-pulse" id="{p}-pg"></div>
      <div class="{p}-tag {p}-ttag {p}-pulse" id="{p}-pt"></div>
      <div class="{p}-m {p}-h {p}-g {p}-r1"><span>BESTELLEN VOR.</span></div>
      <div class="{p}-sub {p}-g">direkt über Ihre Website</div>
      <div class="{p}-sub {p}-t" id="{p}-ts">Ihr Team sieht die Bestellung</div>
      <div class="{p}-m {p}-h {p}-t {p}-r1"><span id="{p}-w1">IN ECHTZEIT.</span></div>""",
    js=ICONS_JS + "\n" + TAGS_JS + """
      S.pulse(document.getElementById("{p}-pg"));
      S.pulse(document.getElementById("{p}-pt"));
      // "Team"@0.24 · "sieht"@0.49 · "in"@1.22 · "Echtzeit."@1.37: the order, on both sides at once
      B.arrive(tl, "#{p}-ti", 0.24, { y: 16, dur: 0.3 });
      B.arrive(tl, "#{p}-ts", 0.49, { y: 10, dur: 0.3 });
      B.rise(tl, "#{p}-w1", 1.22);
      tl.fromTo("#{p}-ttag", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power3.out" }, 1.35);
      // immediateRender:false: the from-state (opacity 0.8) must not paint before 1.37 (v1 showed
      // the team-side ring from the cut on, before the order had arrived)
      tl.fromTo(["#{p}-pg", "#{p}-pt"], { opacity: 0.8, scale: 1 },
        { opacity: 0, scale: 1.9, duration: 0.6, ease: "power2.out", immediateRender: false }, 1.37);""")

# ── 04 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["04-abholzeit"] = dict(
    vo="Und steuert die Abholzeit.",
    comment=f"""
  04-abholzeit: hard cut; cast and orders hold, the copy is cleared. One clock appears ON the
  counter, half on each side (drawn twice: ink in the guest's half, cream in the team's,
  turned by one tween). On „steuert“ the team sets the pickup time: the tomato arc turns
  from 12 o'clock to {ARC_AT}° (the team's side of the dial) and locks; a short ratchet on
  the right. The dial has no numerals: the time is a position, not a claim (BRIEF).""",
    css="""
    .{p}-clk { opacity: 0; }""",
    markup=EYEBROWS + ICONS + TAGS + "\n" + two(CLOCK_G, CLOCK_T) + "\n" + ARC + """
      <div class="{p}-m {p}-h {p}-t {p}-r1"><span id="{p}-w1">STEUERT DIE</span></div>
      <div class="{p}-m {p}-h {p}-t {p}-r2"><span id="{p}-w2">ABHOLZEIT.</span></div>""",
    js=ICONS_JS + "\n" + TAGS_JS + "\n" + CLOCK_JS + f"""
      // "Und"@0.05: the clock; "steuert"@0.23: the arc turns to the pickup time and locks
      tl.fromTo(["#{{p}}-clk-g", "#{{p}}-clk-t", "#{{p}}-arc"], {{ opacity: 0, scale: 0.94 }},
        {{ opacity: 1, scale: 1, duration: 0.32, ease: "power3.out" }}, 0.03);
      tl.fromTo(".{{p}}-arcg", {{ rotation: 0, svgOrigin: "0 0" }},
        {{ rotation: {ARC_AT}, svgOrigin: "0 0", duration: 0.52, ease: "power2.inOut", immediateRender: false }}, 0.27);
      B.rise(tl, "#{{p}}-w1", 0.23);
      B.rise(tl, "#{{p}}-w2", 0.68);""")

# ── 05 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["05-puenktlich"] = dict(
    vo="So holen Ihre Gäste pünktlich ab.",
    comment=f"""
  05-puenktlich: THE SIGNATURE. Hard cut; everything holds, the team's copy too. The bag is
  ready on the team's side („So“). The hand sweeps from 12 into the pickup arc and lands on
  „pünktlich“; at the same instant the bag is halfway across the counter (its travel is
  symmetric about 1.31, so the seam crossing IS the word). The bag exists twice (ink on the
  guest's half, cream on the team's), so it changes colour exactly at the counter. It
  arrives at the guest, an olive check: picked up. The order tags retire. Sound: swish-rl
  travels right → left with it, the service bell rings once on „pünktlich“.
  Travel: 16:9 x −1260 (1590 → 330 at y 860); 9:16 y −480 (1000 → 520 at x 520).""",
    css="""
    .{p}-bag, .{p}-ok { opacity: 0; }""",
    markup=EYEBROWS + ICONS + TAGS + "\n" + two(
        CLOCK_G + "\n" + BAG_G.replace("{cls}", "") + "\n" + OK,
        CLOCK_T + "\n" + BAG_T.replace("{cls}", "")) + "\n" + ARC + """
      <div class="{p}-m {p}-h {p}-g {p}-r1"><span id="{p}-w1">HOLEN</span></div>
      <div class="{p}-m {p}-h {p}-g {p}-r2"><span id="{p}-w2">PÜNKTLICH AB.</span></div>
      <div class="{p}-m {p}-h {p}-t {p}-r1"><span>STEUERT DIE</span></div>
      <div class="{p}-m {p}-h {p}-t {p}-r2"><span>ABHOLZEIT.</span></div>""",
    js=ICONS_JS + "\n" + TAGS_JS + "\n" + CLOCK_JS + "\n" + BAG_JS + "\n" + OK_JS + f"""
      gsap.set(".{{p}}-arcg", {{ rotation: {ARC_AT}, svgOrigin: "0 0" }});
      var bags = ["#{{p}}-bag-g", "#{{p}}-bag-t"];
      var trip = G.P ? {{ y: -480 }} : {{ x: -1260 }};
      // "So"@0.22: the bag is ready on the team's side
      tl.fromTo(bags, {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.26, ease: "power3.out" }}, 0.20);
      // the hand: 12 → the arc, landing on "pünktlich"@1.31
      tl.fromTo(".{{p}}-hand", {{ rotation: 0, svgOrigin: "0 0" }},
        {{ rotation: {ARC_AT}, svgOrigin: "0 0", duration: 1.06, ease: "power2.inOut", immediateRender: false }}, 0.25);
      // the handover: symmetric travel 1.06 → 1.56, the seam crossing at 1.31
      tl.to(bags, Object.assign({{ duration: 0.5, ease: "power2.inOut" }}, trip), 1.06);
      tl.fromTo("#{{p}}-ok", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.24, ease: "power3.out" }}, 1.60);
      tl.to(["#{{p}}-gtag", "#{{p}}-ttag"], {{ opacity: 0, scale: 0.8, duration: 0.3, ease: "power2.in" }}, 1.74);
      // "holen"@0.43 · "pünktlich ab."@1.31
      B.rise(tl, "#{{p}}-w1", 0.43);
      B.rise(tl, "#{{p}}-w2", 1.31);""")

# ── 06 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["06-weniger"] = dict(
    vo="Weniger Wartezeit, mehr zufriedene Gäste.",
    comment=f"""
  06-weniger: hard cut; the stage after the handover holds (the hand in the pickup arc, the
  bag with the guest, checked). The copy pairs across the counter: the guest's gain on the
  left, the team's on the right. No figure: „weniger“ is the site's word, not a number.""",
    markup=EYEBROWS + ICONS + "\n" + two(
        CLOCK_G + "\n" + BAG_G.replace("{cls}", " {p}-at-guest") + "\n" + OK,
        CLOCK_T + "\n" + BAG_T.replace("{cls}", " {p}-at-guest")) + "\n" + ARC + """
      <div class="{p}-m {p}-h {p}-g {p}-r1"><span id="{p}-w1">WENIGER</span></div>
      <div class="{p}-m {p}-h {p}-g {p}-r2"><span id="{p}-w2">WARTEZEIT.</span></div>
      <div class="{p}-m {p}-h {p}-t {p}-r1"><span id="{p}-w3">MEHR ZUFRIEDENE</span></div>
      <div class="{p}-m {p}-h {p}-t {p}-r2"><span id="{p}-w4">GÄSTE.</span></div>""",
    js=ICONS_JS + "\n" + CLOCK_JS + "\n" + BAG_JS + "\n" + OK_JS + f"""
      gsap.set(".{{p}}-arcg", {{ rotation: {ARC_AT}, svgOrigin: "0 0" }});
      gsap.set(".{{p}}-hand", {{ rotation: {ARC_AT}, svgOrigin: "0 0" }});
      // "Weniger"@0.26 · "Wartezeit,"@0.64 · "mehr zufriedene"@1.52 · "Gäste."@2.30
      B.rise(tl, "#{{p}}-w1", 0.26);
      B.rise(tl, "#{{p}}-w2", 0.64);
      B.rise(tl, "#{{p}}-w3", 1.52);
      B.rise(tl, "#{{p}}-w4", 2.30);""")

# ── 07 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["07-einfach"] = dict(
    vo="Einfach für Gäste. Einfach für Ihr Team.",
    comment="""
  07-einfach: THE CLAIM. Hard cut to the bare stage: only the two grounds and their labels.
  The site's sentence is set across the counter, each half on its own side, each landing
  with a tick on its own side (tick-l, tick-r). The split IS the claim.
  16:9: 92 px, „FÜR IHR TEAM.“ = 748 px → 1020–1768; „FÜR GÄSTE.“ = 588 px → 312–900.""",
    css="""
    .{p}-big { height: 112px; font-size: 92px; line-height: 104px; font-weight: 900; letter-spacing: 0.005em; }
    .{p}-b1 { top: 420px; } .{p}-b2 { top: 516px; }
    {PORT} .{p}-g.{p}-b1 { top: 530px; } {PORT} .{p}-g.{p}-b2 { top: 626px; }
    {PORT} .{p}-t.{p}-b1 { top: 800px; } {PORT} .{p}-t.{p}-b2 { top: 896px; }""",
    markup=EYEBROWS + """
      <div class="{p}-m {p}-big {p}-g {p}-b1"><span id="{p}-w1">EINFACH</span></div>
      <div class="{p}-m {p}-big {p}-g {p}-b2"><span id="{p}-w2">FÜR GÄSTE.</span></div>
      <div class="{p}-m {p}-big {p}-t {p}-b1"><span id="{p}-w3">EINFACH</span></div>
      <div class="{p}-m {p}-big {p}-t {p}-b2"><span id="{p}-w4">FÜR IHR TEAM.</span></div>""",
    js="""
      // "Einfach"@0.05 · "für Gäste."@0.42 · "Einfach"@1.30 · "für Ihr Team."@1.70
      B.rise(tl, "#{p}-w1", 0.05);
      B.rise(tl, "#{p}-w2", 0.42);
      B.rise(tl, "#{p}-w3", 1.30);
      B.rise(tl, "#{p}-w4", 1.70);""")

# ── 08 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["08-live"] = dict(
    vo="Wir richten die Vorbestellung für Sie ein. In wenigen Tagen live.",
    comment="""
  08-live: hard cut, bare stage. The setup belongs to the restaurant's side (right: „WIR
  RICHTEN DIE VORBESTELLUNG EIN.“), going live is what the guests see (left: „IN WENIGEN
  TAGEN LIVE.“). The right half is spoken first and rises first; reading follows motion.""",
    css="""
    .{p}-c1 { top: 456px; } .{p}-c2 { top: 532px; }
    {PORT} .{p}-g.{p}-c1 { top: 560px; } {PORT} .{p}-g.{p}-c2 { top: 622px; }
    {PORT} .{p}-t.{p}-c1 { top: 820px; } {PORT} .{p}-t.{p}-c2 { top: 882px; }""",
    markup=EYEBROWS + """
      <div class="{p}-m {p}-h {p}-t {p}-c1"><span id="{p}-w1">WIR RICHTEN DIE</span></div>
      <div class="{p}-m {p}-h {p}-t {p}-c2"><span id="{p}-w2">VORBESTELLUNG EIN.</span></div>
      <div class="{p}-m {p}-h {p}-g {p}-c1"><span id="{p}-w3">IN WENIGEN</span></div>
      <div class="{p}-m {p}-h {p}-g {p}-c2"><span id="{p}-w4">TAGEN LIVE.</span></div>""",
    js="""
      // "richten"@0.21 · "Vorbestellung"@0.67 · "In wenigen"@2.41 · "Tagen live."@3.01
      B.rise(tl, "#{p}-w1", 0.21);
      B.rise(tl, "#{p}-w2", 0.67);
      B.rise(tl, "#{p}-w3", 2.41);
      B.rise(tl, "#{p}-w4", 3.01);""")

# ── 09 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["09-preis"] = dict(
    vo="Vorbestellung inklusive. Neunundzwanzig Euro im Monat, bei jährlicher Zahlung.",
    comment="""
  09-preis: hard cut; the side labels go (the price is for the house, both sides). The
  price sits ON the counter: tomato reads on cream and on ink, so it needs one copy; the
  lines under it straddle the seam and exist twice (ink | cream). 29,00 € always with its
  billing condition and the yearly total (BRIEF).
  16:9: „29,00 €“ 150 px = 613 px centred on 960; 9:16: centred on x 540, ON the seam y 760.""",
    css="""
    .{p}-lab { position: absolute; top: 330px; font-size: 26px; line-height: 32px; font-weight: 700;
      letter-spacing: 0.14em; text-transform: uppercase; white-space: nowrap; opacity: 0; }
    .{p}-lab.{p}-g { color: #85817a; } .{p}-lab.{p}-t { color: #a69f97; }
    .{p}-pm { top: 380px; height: 180px; }
    .{p}-pm span { font-size: 150px; line-height: 176px; font-weight: 900; color: #e65f3c; }
    .{p}-per { top: 590px; font-size: 44px; line-height: 54px; font-weight: 700; opacity: 0; }
    .{p}-fine { top: 662px; font-size: 24px; line-height: 32px; font-weight: 500; opacity: 0; }
    {PORT} .{p}-lab.{p}-g { left: 0; width: 1080px; text-align: center; top: 600px; }
    {PORT} .{p}-lab.{p}-t { left: 0; width: 1080px; text-align: center; top: 880px; }
    {PORT} .{p}-pm { top: 672px; }
    {PORT} .{p}-per { top: 930px; } {PORT} .{p}-fine { top: 1000px; }""",
    markup="""      <div class="{p}-lab {p}-g" id="{p}-lg">Vorbestellung</div>
      <div class="{p}-lab {p}-t" id="{p}-lt">inklusive</div>
      <div class="{p}-m {p}-cen {p}-pm"><span id="{p}-price">29,00&nbsp;€</span></div>
""" + two(
        """        <div class="{p}-cen {p}-per" style="color:#20201e">/ Monat</div>
        <div class="{p}-cen {p}-fine" style="color:#55534c">Jährliche Zahlweise — 348,00 € / Jahr, im Voraus fällig</div>""",
        """        <div class="{p}-cen {p}-per" style="color:#fff4e7" data-layout-allow-overlap>/ Monat</div>
        <div class="{p}-cen {p}-fine" style="color:#a69f97" data-layout-allow-overlap>Jährliche Zahlweise — 348,00 € / Jahr, im Voraus fällig</div>"""),
    js="""
      // "Vorbestellung"@0.02 · "inklusive."@0.67 · "Neunundzwanzig"@1.92 · "Monat,"@3.25 · "jährlicher"@3.96
      B.arrive(tl, "#{p}-lg", 0.04, { y: 10, dur: 0.28 });
      B.arrive(tl, "#{p}-lt", 0.67, { y: 10, dur: 0.28 });
      B.rise(tl, "#{p}-price", 1.92);
      B.arrive(tl, ".{p}-per", 3.25, { y: 10, dur: 0.28 });
      B.arrive(tl, ".{p}-fine", 3.96, { y: 8, dur: 0.3 });""")

# ── 10 ───────────────────────────────────────────────────────────────────────────────────
FRAMES["10-anfragen"] = dict(
    vo="Jetzt Website anfragen. Auf bontrivo.de.",
    comment="""
  10-anfragen: the resolution, with no transformation (films 1 and 2 ended by turning
  something into the O; law 10). The wordmark exists twice, clipped to each half: letters
  ink on the guest's side, cream on the team's; ring and bean keep the brand colours. The
  guest's copy slides in from its outer edge, the team's from the other, and the two halves
  meet in register on „bontrivo“ with the brand chord (films 1-2): one mark across both
  sides. The CTA button sits on the counter (tomato reads on both).
  Each copy is also clipped to ITS part of the mark (16:9: local x 550 = the seam; 9:16:
  local y 148.3): v1 clipped only by the half-layers, so while sliding, each copy showed the
  other half's letters („TRIVO … BONT“, swapped) from the frame's first instant.
  16:9: lockup width 1100 at (410, 252.7); button 586 px → left 667, top 690; URL top 800.
  9:16: lockup width 920 at (80, 611.7), centred ON the seam; button top 1010; URL top 1120.""",
    css="""
    .{p}-logo { position: absolute; left: 410px; top: 252.7px; width: 1100px; height: 354.6px; }
    #{p}-logo-g { clip-path: inset(0px 550px 0px 0px); } #{p}-logo-t { clip-path: inset(0px 0px 0px 550px); }
    {PORT} #{p}-logo-g { clip-path: inset(0px 0px 148.3px 0px); } {PORT} #{p}-logo-t { clip-path: inset(148.3px 0px 0px 0px); }
    .{p}-btn { position: absolute; left: 667px; top: 690px; height: 78px; padding: 0 44px 0 48px; border-radius: 20px;
      background: #e65f3c; color: #20201e; display: flex; align-items: center; gap: 16px; box-sizing: border-box;
      font-size: 30px; font-weight: 700; letter-spacing: 0.02em; text-transform: uppercase; white-space: nowrap; opacity: 0; }
    .{p}-url { top: 800px; font-size: 34px; line-height: 42px; font-weight: 700; opacity: 0; }
    {PORT} .{p}-logo { left: 80px; top: 611.7px; width: 920px; height: 296.6px; }
    {PORT} .{p}-btn { left: 247px; top: 1010px; }
    {PORT} .{p}-url { top: 1120px; }""",
    markup=two(
        """        <div class="{p}-logo" id="{p}-logo-g"></div>
        <div class="{p}-cen {p}-url" style="color:#20201e">bontrivo.de</div>""",
        """        <div class="{p}-logo" id="{p}-logo-t"></div>
        <div class="{p}-cen {p}-url" style="color:#fff4e7" data-layout-allow-overlap>bontrivo.de</div>""") + """
      <div class="{p}-btn" id="{p}-btn"><span>Jetzt Website anfragen</span><span id="{p}-arrow"></span></div>""",
    js="""
      S.logo(document.getElementById("{p}-logo-g"), window.BTV_BRAND.colors.letters);
      S.logo(document.getElementById("{p}-logo-t"), S.CREAM);
      document.getElementById("{p}-arrow").innerHTML = B.icon("arrow", 30, S.INK, 2.4);
      // "anfragen."@0.70: the one action
      tl.fromTo("#{p}-btn", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.68);
      // the two halves of the mark meet in register on "bontrivo"@2.15
      // each part starts just outside the frame: 16:9 BONT (screen 410–960) from x −960,
      // RIVO (960–1510) from +960; 9:16 the top part from y −760, the bottom part from +1160
      var gIn = G.P ? { y: -760 } : { x: -960 }, tIn = G.P ? { y: 1160 } : { x: 960 };
      tl.fromTo("#{p}-logo-g", gIn, Object.assign({ duration: 0.55, ease: "power3.out" }, G.P ? { y: 0 } : { x: 0 }), 1.60);
      tl.fromTo("#{p}-logo-t", tIn, Object.assign({ duration: 0.55, ease: "power3.out" }, G.P ? { y: 0 } : { x: 0 }), 1.60);
      // "."@2.77: the address
      B.arrive(tl, ".{p}-url", 2.77, { y: 10, dur: 0.28 });""")


out = ROOT / "compositions" / "frames"
out.mkdir(parents=True, exist_ok=True)
for fid, f in FRAMES.items():
    (out / f"{fid}.html").write_text(frame(fid, f["comment"], f["markup"], f["js"], f.get("css", ""), f["vo"]))
print(f"✓ {len(FRAMES)} frames written to compositions/frames/")
