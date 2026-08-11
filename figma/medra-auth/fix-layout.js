(async () => {
  // Medra Auth — repair pass. Fixes two things in place; renders nothing, deletes nothing.
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
  // Scoped by frame name, not by page — this file's frames are not all on the pages the render
  // script names, because the plan caps the file at three. Set DRY to true to count only.
  const DRY = false;
  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();
  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
  const OWN = new Set(["Auth \u00b7 Doctor \u2014 D1 Create Account", "Auth \u00b7 Doctor \u2014 D1 Create Account \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D10 Success", "Auth \u00b7 Doctor \u2014 D10 Success \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D2 Verify Code", "Auth \u00b7 Doctor \u2014 D2 Verify Code \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D3 Set Password", "Auth \u00b7 Doctor \u2014 D3 Set Password \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D4 Verification Pending", "Auth \u00b7 Doctor \u2014 D4 Verification Pending \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D5 Profile Setup", "Auth \u00b7 Doctor \u2014 D5 Profile Setup \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D6 Log In", "Auth \u00b7 Doctor \u2014 D6 Log In \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D7 Two-Factor", "Auth \u00b7 Doctor \u2014 D7 Two-Factor \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D8 Forgot Password", "Auth \u00b7 Doctor \u2014 D8 Forgot Password \u00b7 Mobile", "Auth \u00b7 Doctor \u2014 D9 New Password", "Auth \u00b7 Doctor \u2014 D9 New Password \u00b7 Mobile", "Auth \u00b7 Entry \u2014 E1 Onboarding 1", "Auth \u00b7 Entry \u2014 E1 Onboarding 1 \u00b7 Mobile", "Auth \u00b7 Entry \u2014 E2 Onboarding 2", "Auth \u00b7 Entry \u2014 E2 Onboarding 2 \u00b7 Mobile", "Auth \u00b7 Entry \u2014 E3 Onboarding 3", "Auth \u00b7 Entry \u2014 E3 Onboarding 3 \u00b7 Mobile", "Auth \u00b7 Entry \u2014 E4 Welcome", "Auth \u00b7 Entry \u2014 E4 Welcome \u00b7 Mobile", "Auth \u00b7 Entry \u2014 E5 Role Selection", "Auth \u00b7 Entry \u2014 E5 Role Selection \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I1 Register", "Auth \u00b7 Institution \u2014 I1 Register \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I10 New Password", "Auth \u00b7 Institution \u2014 I10 New Password \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I11 Success", "Auth \u00b7 Institution \u2014 I11 Success \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I2 Verify Documents", "Auth \u00b7 Institution \u2014 I2 Verify Documents \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I3 Organisation Size", "Auth \u00b7 Institution \u2014 I3 Organisation Size \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I4 Your Plan", "Auth \u00b7 Institution \u2014 I4 Your Plan \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I5 Verify Admin", "Auth \u00b7 Institution \u2014 I5 Verify Admin \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I6 Set Password", "Auth \u00b7 Institution \u2014 I6 Set Password \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I7 Application Submitted", "Auth \u00b7 Institution \u2014 I7 Application Submitted \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I8 Facility Admin Log In", "Auth \u00b7 Institution \u2014 I8 Facility Admin Log In \u00b7 Mobile", "Auth \u00b7 Institution \u2014 I9 Forgot Password", "Auth \u00b7 Institution \u2014 I9 Forgot Password \u00b7 Mobile", "Auth \u00b7 Member \u2014 M1 Create Account", "Auth \u00b7 Member \u2014 M1 Create Account \u00b7 Mobile", "Auth \u00b7 Member \u2014 M2 Verify Once", "Auth \u00b7 Member \u2014 M2 Verify Once \u00b7 Mobile", "Auth \u00b7 Member \u2014 M3 Your Name", "Auth \u00b7 Member \u2014 M3 Your Name \u00b7 Mobile", "Auth \u00b7 Member \u2014 M4 About You", "Auth \u00b7 Member \u2014 M4 About You \u00b7 Mobile", "Auth \u00b7 Member \u2014 M5 Health Basics", "Auth \u00b7 Member \u2014 M5 Health Basics \u00b7 Mobile", "Auth \u00b7 Member \u2014 M6 Log In", "Auth \u00b7 Member \u2014 M6 Log In \u00b7 Mobile", "Auth \u00b7 Member \u2014 M7 Quick Unlock", "Auth \u00b7 Member \u2014 M7 Quick Unlock \u00b7 Mobile", "Auth \u00b7 Member \u2014 M8 Cannot Get Code", "Auth \u00b7 Member \u2014 M8 Cannot Get Code \u00b7 Mobile", "Auth \u00b7 Member \u2014 M9 Success", "Auth \u00b7 Member \u2014 M9 Success \u00b7 Mobile"].map(norm));

  // every top-level frame in the file that belongs to this module, wherever it sits
  const roots = [], onPages = {};
  for (const pg of figma.root.children) {
    if (pg.type !== 'PAGE') continue;
    for (const f of pg.children) {
      if (f.type === 'FRAME' && OWN.has(norm(f.name))) {
        roots.push(f); onPages[pg.name] = (onPages[pg.name] || 0) + 1;
      }
    }
  }
  if (!roots.length) return { error: 'no frames from this module found in this file',
                              expectedFrames: OWN.size,
                              pagesInFile: figma.root.children.filter(n=>n.type==='PAGE').map(p=>p.name) };

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
  roots.forEach(collect);
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
  roots.forEach(walk);

  return { dryRun: DRY, framesRepaired: roots.length, framesExpected: OWN.size,
           foundOnPages: onPages, spacersCollapsed: spacers, textCentred: texts,
           nodesScanned: scanned, failed, examples: samples, notes };
})();
