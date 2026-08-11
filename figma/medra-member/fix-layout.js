(async () => {
  // Medra Member — repair pass. Fixes two things in place; renders nothing, deletes nothing.
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
  const OWN = new Set(["Member \u00b7 Alerts \u2014 N0 Notification Panel", "Member \u00b7 Alerts \u2014 N0 Notification Panel \u00b7 Mobile", "Member \u00b7 Alerts \u2014 N1 Notifications", "Member \u00b7 Alerts \u2014 N1 Notifications \u00b7 Mobile", "Member \u00b7 Alerts \u2014 N2 No Notifications", "Member \u00b7 Alerts \u2014 N2 No Notifications \u00b7 Mobile", "Member \u00b7 Booking \u2014 B1 Choose a Time", "Member \u00b7 Booking \u2014 B1 Choose a Time \u00b7 Mobile", "Member \u00b7 Booking \u2014 B2 Slot Taken", "Member \u00b7 Booking \u2014 B2 Slot Taken \u00b7 Mobile", "Member \u00b7 Booking \u2014 B3 Review & Confirm", "Member \u00b7 Booking \u2014 B3 Review & Confirm \u00b7 Mobile", "Member \u00b7 Booking \u2014 B4 Payment", "Member \u00b7 Booking \u2014 B4 Payment \u00b7 Mobile", "Member \u00b7 Booking \u2014 C1 Confirmed", "Member \u00b7 Booking \u2014 C1 Confirmed \u00b7 Mobile", "Member \u00b7 Doctor \u2014 P1 Profile", "Member \u00b7 Doctor \u2014 P1 Profile \u00b7 Mobile", "Member \u00b7 Home \u2014 H1 Home", "Member \u00b7 Home \u2014 H1 Home \u00b7 Mobile", "Member \u00b7 Home \u2014 H2 First Visit (empty state)", "Member \u00b7 Home \u2014 H2 First Visit \u00b7 Mobile", "Member \u00b7 Medicines \u2014 M1 My Medicines", "Member \u00b7 Medicines \u2014 M1 My Medicines \u00b7 Mobile", "Member \u00b7 Medicines \u2014 M2 Medicine Detail", "Member \u00b7 Medicines \u2014 M2 Medicine Detail \u00b7 Mobile", "Member \u00b7 Medicines \u2014 M3 Request a Refill", "Member \u00b7 Medicines \u2014 M3 Request a Refill \u00b7 Mobile", "Member \u00b7 Medicines \u2014 M4 Reminders", "Member \u00b7 Medicines \u2014 M4 Reminders \u00b7 Mobile", "Member \u00b7 Medicines \u2014 M5 No Medicines", "Member \u00b7 Medicines \u2014 M5 No Medicines \u00b7 Mobile", "Member \u00b7 Profile \u2014 P0 Profile", "Member \u00b7 Profile \u2014 P0 Profile \u00b7 Mobile", "Member \u00b7 Profile \u2014 P2 Personal Details", "Member \u00b7 Profile \u2014 P2 Personal Details \u00b7 Mobile", "Member \u00b7 Profile \u2014 P3 Dependants", "Member \u00b7 Profile \u2014 P3 Dependants \u00b7 Mobile", "Member \u00b7 Profile \u2014 P3b Family Plan", "Member \u00b7 Profile \u2014 P3b Family Plan \u00b7 Mobile", "Member \u00b7 Profile \u2014 P4 Add a Dependant", "Member \u00b7 Profile \u2014 P4 Add a Dependant \u00b7 Mobile", "Member \u00b7 Profile \u2014 P5 Devices & Security", "Member \u00b7 Profile \u2014 P5 Devices & Security \u00b7 Mobile", "Member \u00b7 Profile \u2014 P6 Notification Preferences", "Member \u00b7 Profile \u2014 P6 Notification Preferences \u00b7 Mobile", "Member \u00b7 Profile \u2014 P7 Language & Accessibility", "Member \u00b7 Profile \u2014 P7 Language & Accessibility \u00b7 Mobile", "Member \u00b7 Profile \u2014 P8 Privacy & Data", "Member \u00b7 Profile \u2014 P8 Privacy & Data \u00b7 Mobile", "Member \u00b7 Profile \u2014 P9 Delete Account", "Member \u00b7 Profile \u2014 P9 Delete Account \u00b7 Mobile", "Member \u00b7 Profile \u2014 P9b Confirm Deletion", "Member \u00b7 Profile \u2014 P9b Confirm Deletion \u00b7 Mobile", "Member \u00b7 Records \u2014 R1 Timeline", "Member \u00b7 Records \u2014 R1 Timeline \u00b7 Mobile", "Member \u00b7 Records \u2014 R10 One-page Summary", "Member \u00b7 Records \u2014 R10 One-page Summary \u00b7 Mobile", "Member \u00b7 Records \u2014 R11 Approve a Share", "Member \u00b7 Records \u2014 R11 Approve a Share \u00b7 Mobile", "Member \u00b7 Records \u2014 R12 Shared Outside Medra", "Member \u00b7 Records \u2014 R12 Shared Outside Medra \u00b7 Mobile", "Member \u00b7 Records \u2014 R2 Consultation Note", "Member \u00b7 Records \u2014 R2 Consultation Note \u00b7 Mobile", "Member \u00b7 Records \u2014 R3 Lab Result", "Member \u00b7 Records \u2014 R3 Lab Result \u00b7 Mobile", "Member \u00b7 Records \u2014 R4 Vitals Trend", "Member \u00b7 Records \u2014 R4 Vitals Trend \u00b7 Mobile", "Member \u00b7 Records \u2014 R5 Share Records", "Member \u00b7 Records \u2014 R5 Share Records \u00b7 Mobile", "Member \u00b7 Records \u2014 R6 Who Has Access", "Member \u00b7 Records \u2014 R6 Who Has Access \u00b7 Mobile", "Member \u00b7 Records \u2014 R7 Add a Record", "Member \u00b7 Records \u2014 R7 Add a Record \u00b7 Mobile", "Member \u00b7 Records \u2014 R8 Record Added", "Member \u00b7 Records \u2014 R8 Record Added \u00b7 Mobile", "Member \u00b7 Records \u2014 R9 No Records", "Member \u00b7 Records \u2014 R9 No Records \u00b7 Mobile", "Member \u00b7 Search \u2014 S1 Results", "Member \u00b7 Search \u2014 S1 Results \u00b7 Mobile", "Member \u00b7 Search \u2014 S2 Filters", "Member \u00b7 Search \u2014 S2 Filters \u00b7 Mobile", "Member \u00b7 Search \u2014 S3 No Results", "Member \u00b7 Search \u2014 S3 No Results \u00b7 Mobile", "Member \u00b7 States \u2014 X1 Loading", "Member \u00b7 States \u2014 X1 Loading \u00b7 Mobile", "Member \u00b7 States \u2014 X2 Offline", "Member \u00b7 States \u2014 X2 Offline \u00b7 Mobile", "Member \u00b7 States \u2014 X3 Something Went Wrong", "Member \u00b7 States \u2014 X3 Something Went Wrong \u00b7 Mobile", "Member \u00b7 Virtual \u2014 W0 Join by Link", "Member \u00b7 Virtual \u2014 W0 Join by Link \u00b7 Mobile", "Member \u00b7 Virtual \u2014 W1 Pre-call Check", "Member \u00b7 Virtual \u2014 W1 Pre-call Check \u00b7 Mobile", "Member \u00b7 Virtual \u2014 W2 In Call", "Member \u00b7 Virtual \u2014 W2 In Call \u00b7 Mobile", "Member \u00b7 Virtual \u2014 W3 Visit Summary", "Member \u00b7 Virtual \u2014 W3 Visit Summary \u00b7 Mobile", "Member \u00b7 Virtual \u2014 W4 Connection Lost", "Member \u00b7 Virtual \u2014 W4 Connection Lost \u00b7 Mobile", "Member \u00b7 Visits \u2014 V1 Upcoming", "Member \u00b7 Visits \u2014 V1 Upcoming \u00b7 Mobile", "Member \u00b7 Visits \u2014 V2 Past", "Member \u00b7 Visits \u2014 V2 Past \u00b7 Mobile", "Member \u00b7 Visits \u2014 V3 No Visits", "Member \u00b7 Visits \u2014 V3 No Visits \u00b7 Mobile", "Member \u00b7 Visits \u2014 V4 Visit Detail", "Member \u00b7 Visits \u2014 V4 Visit Detail \u00b7 Mobile", "Member \u00b7 Visits \u2014 V5 Reschedule", "Member \u00b7 Visits \u2014 V5 Reschedule \u00b7 Mobile", "Member \u00b7 Visits \u2014 V6 Cancel Visit", "Member \u00b7 Visits \u2014 V6 Cancel Visit \u00b7 Mobile", "Member \u00b7 Visits \u2014 V7 Cancelled", "Member \u00b7 Visits \u2014 V7 Cancelled \u00b7 Mobile", "cmp/Button Primary/State=Default", "cmp/Button Primary/State=Disabled", "cmp/Button Primary/State=Hover", "cmp/Button Primary/State=Loading", "cmp/Button Primary/State=Pressed", "cmp/Call Control/State=End", "cmp/Call Control/State=Idle", "cmp/Call Control/State=Off", "cmp/Call Control/State=On", "cmp/Checkbox/State=Checked", "cmp/Checkbox/State=Unchecked", "cmp/Consent Scope/State=Locked", "cmp/Consent Scope/State=Off", "cmp/Consent Scope/State=On", "cmp/Doctor Card/State=Default", "cmp/Doctor Card/State=Hover", "cmp/Dose/State=Due", "cmp/Dose/State=Missed", "cmp/Dose/State=Taken", "cmp/Input/State=Default", "cmp/Input/State=Error", "cmp/Input/State=Filled", "cmp/Input/State=Focus", "cmp/List Row/State=Default", "cmp/List Row/State=Hover", "cmp/List Row/State=Pressed", "cmp/Nav Item/State=Active", "cmp/Nav Item/State=Inactive", "cmp/Specialty Chip/State=Default", "cmp/Specialty Chip/State=Hover", "cmp/Specialty Chip/State=Selected", "cmp/Status Pill/State=Cancelled", "cmp/Status Pill/State=Completed", "cmp/Status Pill/State=Confirmed", "cmp/Status Pill/State=Live", "cmp/Status Pill/State=Pending", "cmp/Tab/State=Active", "cmp/Tab/State=Inactive", "cmp/Time Slot/State=Available", "cmp/Time Slot/State=Hover", "cmp/Time Slot/State=Selected", "cmp/Time Slot/State=Taken", "cmp/Toggle/State=Off", "cmp/Toggle/State=On"].map(norm));

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
