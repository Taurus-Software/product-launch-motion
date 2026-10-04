/* split.js: film 3's stage. The frame is split for the whole film: the guest's side
   (cream) and the team's side (ink), the seam between them is the counter.

   Orientation decides the axis: 16:9 splits left | right at x = 960, 9:16 splits
   top / bottom at y = 760 (the team's half is the taller one, because the burned captions
   sit in it at y ≈ 1352). Frames place everything with CSS (two blocks: the frame's own
   and the 9:16 block that tools/make-vertical.mjs appends); the few numbers a timeline
   needs (a travel distance, a clip formula) come from SP.geo(), keyed on the orientation
   the root declares, so the same frame file is correct in both cuts.

   Two-colourway objects: anything that sits ON the seam (the clock, the travelling bag,
   the price's small print, the URL, the logo) exists twice, once in a layer clipped to the
   guest's half (drawn ink) and once in a layer clipped to the team's half (drawn cream),
   moved by one tween through a shared class. It reads as one object that changes colour
   exactly at the counter. Deterministic: no layout reads, no randomness. */
(function () {
  if (window.SP) return;
  var NS = "http://www.w3.org/2000/svg";
  var INK = "#20201E", CREAM = "#FFF4E7", TOMATO = "#E65F3C";

  function portrait(id) {
    var r = document.querySelector('[data-composition-id="' + id + '"]');
    return !!r && r.getAttribute("data-width") === "1080";
  }

  /* Stage numbers per orientation. seam: the counter's coordinate on its axis. */
  function geo(id) {
    return portrait(id)
      ? { P: true, W: 1080, H: 1920, seam: 760, axis: "y" }
      : { P: false, W: 1920, H: 1080, seam: 960, axis: "x" };
  }

  /* clip-path of the team's half as the seam opens: p = 0 closed (all guest), 1 open */
  function openClip(g, p) {
    var q = (1 - p) * 100;
    return g.P ? "inset(0% 0% " + q.toFixed(3) + "% 0%)" : "inset(0% " + q.toFixed(3) + "% 0% 0%)";
  }

  /* The clock: viewBox centred on its axle, ring r 150, 12 ticks outside it, one hand.
     `col` is the stroke colour of this copy (ink in the guest layer, cream in the team
     layer). The hand group carries `handClass` so both copies turn with one tween. */
  function clock(el, col, handClass) {
    var ticks = "";
    for (var i = 0; i < 12; i++) {
      var a = i * Math.PI / 6, s = Math.sin(a), c = -Math.cos(a), r0 = i % 3 === 0 ? 160 : 163, r1 = 172;
      ticks += '<line x1="' + (s * r0).toFixed(2) + '" y1="' + (c * r0).toFixed(2) + '" x2="' + (s * r1).toFixed(2) +
        '" y2="' + (c * r1).toFixed(2) + '" stroke-width="' + (i % 3 === 0 ? 5 : 3) + '"/>';
    }
    el.innerHTML =
      '<svg xmlns="' + NS + '" viewBox="-180 -180 360 360" width="100%" height="100%" overflow="visible">' +
      '<g fill="none" stroke="' + col + '" stroke-linecap="round">' +
      '<circle r="150" stroke-width="5"/>' + ticks + "</g>" +
      '<g class="' + handClass + '"><line x1="0" y1="14" x2="0" y2="-122" stroke="' + col +
      '" stroke-width="7" stroke-linecap="round"/></g>' +
      '<circle r="9" fill="' + col + '"/></svg>';
  }

  /* The pickup time: a tomato arc on the ring, 32° wide, drawn at 12 o'clock; its group
     (class arcClass) is rotated to the time. Tomato reads on both halves, so one copy. */
  function arc(el, arcClass) {
    var a = 16 * Math.PI / 180, r = 150;
    var x = (Math.sin(a) * r).toFixed(2), y = (-Math.cos(a) * r).toFixed(2);
    el.innerHTML =
      '<svg xmlns="' + NS + '" viewBox="-180 -180 360 360" width="100%" height="100%" overflow="visible">' +
      '<g class="' + arcClass + '"><path d="M-' + x + " " + y + " A" + r + " " + r + " 0 0 1 " + x + " " + y +
      '" fill="none" stroke="' + TOMATO + '" stroke-width="16" stroke-linecap="round"/></g></svg>';
  }

  /* The order: a tomato disc with the receipt glyph (no text on it: no order UI exists to
     show). The same tag stands for the order on both sides of the counter. */
  function tag(el) {
    el.innerHTML = '<svg xmlns="' + NS + '" viewBox="0 0 88 88" width="100%" height="100%">' +
      '<circle cx="44" cy="44" r="44" fill="' + TOMATO + '"/>' +
      '<g transform="translate(20 20) scale(2)" fill="none" stroke="' + CREAM + '" stroke-width="1.7" ' +
      'stroke-linecap="round" stroke-linejoin="round">' + window.BTV.ICONS.receipt + "</g></svg>";
  }
  /* a ring the size of the tag, expanded once at the real-time moment */
  function pulse(el) {
    el.innerHTML = '<svg xmlns="' + NS + '" viewBox="0 0 88 88" width="100%" height="100%" overflow="visible">' +
      '<circle cx="44" cy="44" r="42" fill="none" stroke="' + TOMATO + '" stroke-width="3"/></svg>';
  }
  /* The wordmark in one SVG (traced groups share the source PNG's 577 × 186 grid); the
     letters take this copy's colour, ring and bean keep the brand's. */
  function logo(el, letters) {
    var BR = window.BTV_BRAND;
    el.innerHTML = '<svg xmlns="' + NS + '" viewBox="0 0 577 186" width="100%" height="100%">' +
      '<g fill="' + letters + '">' + BR.letters + '</g><g fill="' + BR.colors.ring + '">' + BR.ring +
      '</g><g fill="' + BR.colors.bean + '">' + BR.bean + "</g></svg>";
  }

  window.SP = { portrait: portrait, geo: geo, openClip: openClip, clock: clock, arc: arc,
    tag: tag, pulse: pulse, logo: logo,
    INK: INK, CREAM: CREAM, TOMATO: TOMATO };
})();
