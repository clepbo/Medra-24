(async () => {
  // ============================================================
  // Medra — turn rendered `cmp/<Component>/<Prop>=<Value>` frames into REAL Figma
  // interactive components: one component set per component, variant properties,
  // and wired hover / press / click interactions with Smart Animate.
  // Run:  figma-cli run .\components-medra.js
  // Idempotent: existing "Medra/<Component>" sets are removed first.
  // ============================================================
  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();

  const PAGE = 'Medra — Interactive Components';
  let page = figma.root.children.find(n => n.name === PAGE);
  if (!page) return { error: `page "${PAGE}" not found — render the cmp/* frames first` };
  await figma.setCurrentPageAsync(page);

  // ---- collect cmp frames -------------------------------------------------
  const re = /^cmp\/(.+?)\/(.+?)=(.+)$/;
  const groups = {};                       // component -> { prop, variants: {value: frame} }
  for (const node of [...page.children]) {
    if (node.type !== 'FRAME') continue;
    const m = re.exec((node.name || '').trim());
    if (!m) continue;
    const [, comp, prop, value] = m;
    groups[comp] = groups[comp] || { prop, variants: {} };
    groups[comp].variants[value] = node;
  }
  if (!Object.keys(groups).length) return { error: 'no cmp/* frames found on the page' };

  // ---- clean previous runs ------------------------------------------------
  for (const node of [...page.children]) {
    if (node.type === 'COMPONENT_SET' && node.name.startsWith('Medra/')) node.remove();
  }

  // ---- interaction map ----------------------------------------------------
  // For each component: which variant is the resting state, and what each trigger goes to.
  const REST = {
    'Button Primary': 'Default', 'Input': 'Default', 'Time Slot': 'Available',
    'Specialty Chip': 'Default', 'Toggle': 'Off', 'Checkbox': 'Unchecked',
    'Nav Item': 'Inactive', 'Doctor Card': 'Default',
  };
  const WIRING = {                      // rest -> [ [trigger, targetVariant], ... ]
    'Button Primary': [['ON_HOVER', 'Hover'], ['ON_PRESS', 'Pressed']],
    'Input':          [['ON_HOVER', 'Focus'], ['ON_PRESS', 'Focus']],
    'Time Slot':      [['ON_HOVER', 'Hover'], ['ON_CLICK', 'Selected']],
    'Specialty Chip': [['ON_HOVER', 'Hover'], ['ON_CLICK', 'Selected']],
    'Toggle':         [['ON_CLICK', 'On']],
    'Checkbox':       [['ON_CLICK', 'Checked']],
    'Nav Item':       [['ON_CLICK', 'Active']],
    'Doctor Card':    [['ON_HOVER', 'Hover']],
  };
  const BACK = {                        // non-rest variant -> back to rest on release/leave
    'Button Primary': [['ON_HOVER', 'Default'], ['ON_PRESS', 'Default']],
    'Time Slot':      [['ON_CLICK', 'Available']],
    'Specialty Chip': [['ON_CLICK', 'Default']],
    'Toggle':         [['ON_CLICK', 'Off']],
    'Checkbox':       [['ON_CLICK', 'Unchecked']],
    'Doctor Card':    [['ON_HOVER', 'Default']],
  };

  const smart = (d = 0.16) => ({ type: 'SMART_ANIMATE', easing: { type: 'GENTLE' }, duration: d });
  const changeTo = (id, d) => ({ type: 'NODE', destinationId: id, navigation: 'CHANGE_TO', transition: smart(d) });

  const report = { sets: 0, variants: 0, reactions: 0, components: [], notes: [] };
  let cursorX = 0, cursorY = 0, rowH = 0;

  for (const [comp, { prop, variants }] of Object.entries(groups)) {
    try {
      // frame -> component, named "Prop=Value" so Figma derives the variant property
      const comps = [];
      for (const [value, frame] of Object.entries(variants)) {
        const c = figma.createComponentFromNode(frame);
        c.name = `${prop}=${value}`;
        comps.push([value, c]);
      }
      const set = figma.combineAsVariants(comps.map(([, c]) => c), page);
      set.name = `Medra/${comp}`;
      set.layoutMode = 'HORIZONTAL';
      set.itemSpacing = 24;
      set.paddingLeft = set.paddingRight = set.paddingTop = set.paddingBottom = 24;
      set.primaryAxisSizingMode = 'AUTO';
      set.counterAxisSizingMode = 'AUTO';

      // lay the sets out in a tidy grid
      set.x = cursorX; set.y = cursorY;
      cursorX += set.width + 80;
      rowH = Math.max(rowH, set.height);
      if (cursorX > 2600) { cursorX = 0; cursorY += rowH + 80; rowH = 0; }

      // ---- wire interactions ----
      const byValue = Object.fromEntries(comps);
      const rest = REST[comp];
      if (rest && byValue[rest]) {
        for (const [trigger, target] of (WIRING[comp] || [])) {
          if (!byValue[target]) continue;
          const existing = byValue[rest].reactions ? [...byValue[rest].reactions] : [];
          existing.push({ trigger: { type: trigger }, actions: [changeTo(byValue[target].id)] });
          await byValue[rest].setReactionsAsync(existing);
          report.reactions++;
        }
        for (const [value, node] of comps) {
          if (value === rest) continue;
          for (const [trigger, target] of (BACK[comp] || [])) {
            if (!byValue[target] || value === target) continue;
            const existing = node.reactions ? [...node.reactions] : [];
            existing.push({ trigger: { type: trigger }, actions: [changeTo(byValue[target].id)] });
            await node.setReactionsAsync(existing);
            report.reactions++;
          }
        }
      }
      report.sets++; report.variants += comps.length;
      report.components.push(`Medra/${comp} (${comps.map(([v]) => v).join(', ')})`);
    } catch (e) {
      report.notes.push(`${comp}: ${e.message}`);
    }
  }
  return report;
})();
