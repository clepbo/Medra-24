(async () => {
  // Medra Organisation — repair pass. Fixes two things in place; renders nothing, deletes nothing.
  //
  //  1. Empty spacer frames. `<Frame grow={1} />` means "push the next thing to the far end".
  //     It has no height, and Figma gives a new frame 100×100 by default, so a 34px row became
  //     100px tall with a hole in it. The frame is set to FILL on the parent's cross axis: a
  //     spacer should take the size of the row it sits in, never dictate it.
  //
  //  2. Text left-aligned inside a centred container. `items="center"` centres the text *node*;
  //     it does not centre the text *inside* the node, so a label reads as left-aligned in a
  //     visibly centred card. Any text in a centred container gets textAlignHorizontal CENTER.
  //
  // Set DRY to true to count without changing anything.
  const DRY = false;
  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();
  const PAGES = ["Medra Org \u2014 1 Setup & Verification", "Medra Org \u2014 2 Today & Bookings", "Medra Org \u2014 3 Departments & People", "Medra Org \u2014 4 The Clinical Chain", "Medra Org \u2014 5 Referrals & External Access", "Medra Org \u2014 6 Access, Money & Reports", "Medra Org \u2014 7 States & Edge Cases", "Medra Org \u2014 8 Components"];
  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
  const pages = figma.root.children.filter(n => n.type==='PAGE' && PAGES.some(p => norm(p)===norm(n.name)));
  if (!pages.length) return { error: 'none of this module\u2019s pages are in this file', lookedFor: PAGES };

  // A spacer is empty AND invisible. A frame with a fill or a stroke is a drawn block, and
  // resizing one of those would be a design change, not a repair.
  const invisible = n => {
    const f = n.fills, s = n.strokes;
    const hasFill = Array.isArray(f) && f.some(p => p.visible !== false && p.opacity !== 0);
    const hasStroke = Array.isArray(s) && s.length > 0;
    return !hasFill && !hasStroke;
  };

  // Text properties cannot be touched until every font on the node is loaded.
  const seen = new Set(), fonts = [];
  const collect = n => {
    if (n.type === 'TEXT') {
      let fs; try { fs = n.getRangeAllFontNames(0, n.characters.length); } catch (e) { fs = []; }
      for (const f of fs) { const k = f.family + '|' + f.style;
        if (!seen.has(k)) { seen.add(k); fonts.push(f); } }
    }
    if ('children' in n) n.children.forEach(collect);
  };
  for (const pg of pages) pg.children.forEach(collect);
  for (const f of fonts) { try { await figma.loadFontAsync(f); } catch (e) {} }

  let spacers = 0, texts = 0, scanned = 0, failed = 0;
  const notes = [], samples = [];

  const walk = n => {
    scanned++;
    const auto = 'layoutMode' in n && n.layoutMode && n.layoutMode !== 'NONE';
    if (auto && n.children.length > 1) {
      const row = n.layoutMode === 'HORIZONTAL';
      for (const kid of n.children) {
        if (kid.type === 'FRAME' && kid.children.length === 0 && invisible(kid)) {
          const prop = row ? 'layoutSizingVertical' : 'layoutSizingHorizontal';
          if (kid[prop] !== 'FILL') {
            if (samples.length < 8) samples.push((n.name||'Frame') + ' \u2192 ' + (row?'height':'width') + ' was ' + Math.round(row?kid.height:kid.width));
            if (!DRY) {
              try { kid[prop] = 'FILL'; spacers++; }
              catch (e) {
                // FILL refused (a fixed-size parent, usually) \u2014 collapse it instead, same result
                try { kid.resize(row ? Math.max(kid.width,0.01) : 0.01, row ? 0.01 : Math.max(kid.height,0.01)); spacers++; }
                catch (e2) { failed++; if (notes.length < 10) notes.push((n.name||'?') + ': ' + e2.message); }
              }
            } else spacers++;
          }
        }
        if (kid.type === 'TEXT') {
          const centred = (!row && n.counterAxisAlignItems === 'CENTER')
                       || ( row && n.primaryAxisAlignItems === 'CENTER');
          if (centred && kid.textAlignHorizontal !== 'CENTER') {
            if (!DRY) {
              try { kid.textAlignHorizontal = 'CENTER'; texts++; }
              catch (e) { failed++; if (notes.length < 10) notes.push('text \u201c' + (kid.characters||'').slice(0,24) + '\u201d: ' + e.message); }
            } else texts++;
          }
        }
      }
    }
    if ('children' in n) n.children.forEach(walk);
  };
  for (const pg of pages) pg.children.forEach(walk);

  return { dryRun: DRY, pages: pages.map(p => p.name), spacersCollapsed: spacers,
           textCentred: texts, nodesScanned: scanned, failed, examples: samples, notes };
})();
