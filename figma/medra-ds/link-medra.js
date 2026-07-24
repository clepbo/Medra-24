(async () => {
  const page = figma.currentPage;
  const norm = s => (s || "").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim();
  const frames = page.children.filter(n => n.type === "FRAME");
  const byName = {};
  frames.forEach(f => { byName[norm(f.name)] = f; });
  const F = name => byName[norm(name)];

  // ---- arrange frames into grouped section rows (readable grid, not one long line) ----
  const layoutRows = [
    ["Medra DS — 00 Cover", "Medra DS — 01 Contents", "Medra DS — 02 Brand Story", "Medra DS — 03 Brand Goals"],
    ["Medra DS — 04 Logo Primary", "Medra DS — 05 Logo Construction", "Medra DS — 06 Logo Variations", "Medra DS — 07 Logo Misuse"],
    ["Medra DS — 08 Colour Primary", "Medra DS — 09 Colour Semantic", "Medra DS — 10 Gradient Elevation", "Medra DS — 11 Typography Typeface", "Medra DS — 12 Typography Scale", "Medra DS — 13 Iconography", "Medra DS — 14 Layout Grid"],
    ["Medra DS — 15 Components Buttons", "Medra DS — 16 Components Forms", "Medra DS — 17 Components Cards", "Medra DS — 18 Components Badges"],
    ["Medra DS — 19 Imagery", "Medra DS — 20 Contact"]
  ];
  const GAPX = 140, GAPY = 220;
  let ay = 0;
  for (const row of layoutRows) {
    let ax = 0, rowH = 0;
    for (const name of row) {
      const f = F(name);
      if (!f) continue;
      f.x = ax; f.y = ay;
      ax += f.width + GAPX;
      rowH = Math.max(rowH, f.height);
    }
    ay += rowH + GAPY;
  }

  // canonical frame order (drives "Next")
  const order = [
    "Medra DS — 00 Cover", "Medra DS — 01 Contents", "Medra DS — 02 Brand Story",
    "Medra DS — 03 Brand Goals", "Medra DS — 04 Logo Primary", "Medra DS — 05 Logo Construction",
    "Medra DS — 06 Logo Variations", "Medra DS — 07 Logo Misuse", "Medra DS — 08 Colour Primary",
    "Medra DS — 09 Colour Semantic", "Medra DS — 10 Gradient Elevation", "Medra DS — 11 Typography Typeface",
    "Medra DS — 12 Typography Scale", "Medra DS — 13 Iconography", "Medra DS — 14 Layout Grid",
    "Medra DS — 15 Components Buttons", "Medra DS — 16 Components Forms", "Medra DS — 17 Components Cards",
    "Medra DS — 18 Components Badges", "Medra DS — 19 Imagery", "Medra DS — 20 Contact"
  ];

  // Contents index rows -> destination section
  const navMap = {
    "Nav Brand Story": "Medra DS — 02 Brand Story",
    "Nav Brand Goals": "Medra DS — 03 Brand Goals",
    "Nav Logo System": "Medra DS — 04 Logo Primary",
    "Nav Colour": "Medra DS — 08 Colour Primary",
    "Nav Gradient & Elevation": "Medra DS — 10 Gradient Elevation",
    "Nav Typography": "Medra DS — 11 Typography Typeface",
    "Nav Iconography": "Medra DS — 13 Iconography",
    "Nav Layout": "Medra DS — 14 Layout Grid",
    "Nav Components": "Medra DS — 15 Components Buttons",
    "Nav Imagery & Contact": "Medra DS — 19 Imagery"
  };

  // find first descendant whose (normalised) name matches
  const findNamed = (root, target) => {
    let hit = null;
    const t = norm(target);
    const walk = n => {
      if (hit) return;
      if (n.name && norm(n.name) === t) { hit = n; return; }
      if ("children" in n) n.children.forEach(walk);
    };
    walk(root);
    return hit;
  };

  const transition = { type: "SMART_ANIMATE", easing: { type: "EASE_OUT" }, duration: 0.3 };
  const jobs = [];          // collect, then await sequentially (never fire-and-forget in a walk)
  const missingHotspots = [];

  const queue = (frameName, hotspotName, destName) => {
    const frame = F(frameName);
    const dest = F(destName);
    if (!frame) return;
    if (!dest) return;
    const node = hotspotName === "*self*" ? frame : findNamed(frame, hotspotName);
    if (!node) { missingHotspots.push(`${frameName} → "${hotspotName}"`); return; }
    jobs.push([node, dest]);
  };

  // 1. Next / Contents chrome on every content frame
  order.forEach((name, i) => {
    if (i === 0) { queue(name, "*self*", "Medra DS — 01 Contents"); return; } // cover → contents
    if (i < order.length - 1) queue(name, "Btn Next", order[i + 1]);
    queue(name, "Btn Contents", "Medra DS — 01 Contents");
  });

  // 2. Contents index rows
  Object.entries(navMap).forEach(([row, dest]) => queue("Medra DS — 01 Contents", row, dest));

  // 3. a few in-context CTAs (no dead-ends)
  queue("Medra DS — 17 Components Cards", "Btn Book Ngozi", "Medra DS — 18 Components Badges");

  // apply
  let linked = 0;
  for (const [node, dest] of jobs) {
    await node.setReactionsAsync([{ trigger: { type: "ON_CLICK" }, actions: [{ type: "NODE", destinationId: dest.id, navigation: "NAVIGATE", transition }] }]);
    linked++;
  }

  // flow start = cover
  const cover = F("Medra DS — 00 Cover");
  if (cover) page.flowStartingPoints = [{ nodeId: cover.id, name: "Medra Design System" }];

  return { linked, framesFound: frames.length, missingHotspots };
})();
