/* btv.js: the film's shared vocabulary. Loaded by every frame (idempotent).

   Everything here is a pure function of its arguments and of timeline time: no
   Math.random, no Date, no CSS transitions (Law 3). Frames call these with absolute
   positions on their OWN paused timeline, so a seek to T reproduces frame T.

   The plate is the logo's O, drawn from the traced geometry in btv-brand.js. */
(function () {
  if (window.BTV) return;
  var B = window.BTV_BRAND;
  var NS = "http://www.w3.org/2000/svg";

  /* Icons: stroke paths copied verbatim from bontrivo.de's own markup (24-unit grid,
     round caps), except `bag`, which is drawn in the same idiom for Vorbestellung because
     the supplied HTML has no pickup icon. STORYBOARD.md records that distinction. */
  var ICONS = {
    // site icon (kept for reference): reads as the letters "PF" at film scale, so the
    // frames use `cutlery` below, drawn in the same idiom (24 grid, round caps, 1.8 stroke)
    cutlerySite: '<path d="M6 3v18M6 3c3 0 5 1.5 5 4.5S9 12 6 12M18 3v18M14 3h4v9M14 8h4"/>',
    cutlery: '<path d="M6 3v5.5a2.5 2.5 0 0 0 5 0V3M8.5 3v18M17.5 21V3c-2 1.6-3 4.4-3 8.5h3"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M8.5 14.5l2 2 4-4.5"/>',
    bag: '<path d="M5 8h14l-1.2 13H6.2L5 8Z"/><path d="M9 10V6.5a3 3 0 0 1 6 0V10"/>',
    bistro: '<path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13.5" r="3.3"/>',
    bar: '<path d="M4 4h16l-6.5 8v6.5h3.5V21H8.5v-2.5H12V12L4 4Z"/>',
    hotel: '<path d="M4 21V6.5a1 1 0 0 1 1-1h4v15.5M14 21v-6h4M4 12h16M14 21V6.5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1V21M8 8h.01M8 12h.01"/>',
    cafe: '<path d="M4 8h13v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V8Z"/><path d="M17 9h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M7 3.5c0 1-1 1-1 2s1 1 1 2M11 3.5c0 1-1 1-1 2s1 1 1 2"/>',
    beer: '<path d="M6 21V9a3 3 0 0 1 3-3h1V4h4v2h1a3 3 0 0 1 3 3v12"/><path d="M6 13h12M9 21v-4M15 21v-4"/>',
    cloche: '<path d="M3 12a9 9 0 0 1 18 0Z"/><path d="M3 12h18M12 3v2"/>',
    check: '<path d="M5 12.5l4.2 4.2L19 7"/>',
    arrow: '<path d="M5 12h13M13 6l6 6-6 6"/>'
  };

  function icon(name, size, color, stroke) {
    return '<svg xmlns="' + NS + '" viewBox="0 0 24 24" width="' + size + '" height="' + size +
      '" fill="none" stroke="' + (color || "#20201E") + '" stroke-width="' + (stroke || 1.8) +
      '" stroke-linecap="round" stroke-linejoin="round">' + ICONS[name] + "</svg>";
  }

  /* The O-plate. `opts.bean` adds the bean group (id <prefix>-bean) so it can drop in on
     its own; `opts.fill` paints the plate's well (used by the iris, whose cream inside
     becomes the next ground). The SVG's viewBox is centred on the fitted ring centre, so
     an element of size S placed at (cx − S/2, cy − S/2) has the ring centred on (cx, cy). */
  function plate(el, prefix, opts) {
    opts = opts || {};
    var b = B.oBox, g = B.geo;
    var well = opts.fill
      ? '<circle cx="' + g.cx + '" cy="' + g.cy + '" r="' + (g.r_in + 1.2) + '" fill="' + opts.fill + '"/>'
      : "";
    el.innerHTML =
      '<svg xmlns="' + NS + '" viewBox="' + b.join(" ") + '" width="100%" height="100%" overflow="visible">' +
      well +
      '<g id="' + prefix + '-ring" fill="' + B.colors.ring + '">' + B.ring + "</g>" +
      (opts.bean ? '<g id="' + prefix + '-bean" fill="' + B.colors.bean + '">' + B.bean + "</g>" : "") +
      "</svg>";
  }

  /* Where the bean sits, in plate-local percent, so it can scale about its own centre. */
  function beanOrigin() {
    var b = B.oBox;
    var bx = 154.5, by = 71.6; // measured bean centroid in the source PNG (SOURCES.md)
    return ((bx - b[0]) / b[2] * 100).toFixed(2) + "% " + ((by - b[1]) / b[3] * 100).toFixed(2) + "%";
  }

  /* Contact shadows. An object resting on the table casts a tight, darker shadow; lifted,
     the shadow spreads, softens and drops away. The serve gesture tweens between the two,
     so depth comes from light, not from perspective (DIRECTION: flat, top-down). */
  var REST = "drop-shadow(0px 14px 16px rgba(32,32,30,0.20))";
  var LIFT = "drop-shadow(0px 46px 40px rgba(32,32,30,0.10))";

  /* serve(): the signature gesture. The object travels in from `from` (px offsets),
     slightly lifted (scale `lift`, spread shadow), and LANDS at `at`: travel ends exactly
     on the word, the shadow tightens over the last third, a 0.05 s squash reads as weight.
     Nothing bounces: power3.out, then still. */
  function serve(tl, el, at, o) {
    o = o || {};
    var dur = o.dur || 0.42;
    var start = at - dur;
    var from = o.from || { x: 0, y: -40 };
    // immediateRender:false: the from-state (opacity 1 at the start offset) must not be
    // painted before the serve begins. With it, a plate sat visibly at its start position
    // from frame 0 wherever that position was inside the canvas (found in the 9:16 cut).
    tl.fromTo(el, { x: from.x, y: from.y, scale: o.lift || 1.05, opacity: o.fade ? 0 : 1, filter: LIFT },
      { x: 0, y: 0, scale: 1, opacity: 1, filter: REST, duration: dur, ease: "power3.out", immediateRender: false }, start);
    tl.fromTo(el, { scaleY: 1 }, { scaleY: 0.985, duration: 0.05, ease: "power1.out", immediateRender: false }, at + 0.01);
    tl.to(el, { scaleY: 1, duration: 0.16, ease: "power2.out" }, at + 0.07);
  }

  /* drop(): something set INTO the plate from above: the course on the plate, the bean.
     Starts larger (nearer the overhead camera) with a soft distant shadow, lands on `at`. */
  function drop(tl, el, at, o) {
    o = o || {};
    var dur = o.dur || 0.34;
    // SVG children (the bean) take no CSS filter: they inherit their plate's shadow.
    var a = { scale: o.from || 1.55, opacity: 0 }, b = { scale: 1, opacity: 1, duration: dur, ease: "power3.out" };
    if (o.shadow !== false) { a.filter = LIFT; b.filter = REST; }
    if (o.origin) { a.transformOrigin = o.origin; b.transformOrigin = o.origin; }
    tl.fromTo(el, a, b, at - dur);
  }

  /* clear(): a course taken off the plate before the next one arrives (the "Abräumen").
     A relocation is an exit with intent: power2.in, short, to one side. */
  function clear(tl, el, at, o) {
    o = o || {};
    tl.to(el, { x: o.x == null ? 180 : o.x, y: o.y || 0, opacity: 0, scale: 1.08, filter: LIFT,
      duration: o.dur || 0.26, ease: "power2.in" }, at);
  }

  /* Line reveal from the baseline: the line's mask is its wrapper (overflow hidden).
     135%, not ~108%: umlaut dots sit above cap height, and with a wrapper only a few px
     taller than the line box they peek out before the cue (found in 04, "ÜBER"). */
  function rise(tl, el, at, o) {
    o = o || {};
    tl.fromTo(el, { yPercent: o.from == null ? 135 : o.from, opacity: 1 },
      { yPercent: 0, duration: o.dur || 0.34, ease: "power3.out" }, at - (o.lead || 0.02));
  }

  /* Plain arrival: opacity + a short travel with meaning (references/04, §2). */
  function arrive(tl, el, at, o) {
    o = o || {};
    tl.fromTo(el, { opacity: 0, x: o.x || 0, y: o.y == null ? 18 : o.y },
      { opacity: 1, x: 0, y: 0, duration: o.dur || 0.3, ease: o.ease || "power3.out" }, at - (o.lead || 0.02));
  }

  window.BTV = { icon: icon, plate: plate, beanOrigin: beanOrigin, serve: serve, drop: drop,
    clear: clear, rise: rise, arrive: arrive, REST: REST, LIFT: LIFT };
})();
