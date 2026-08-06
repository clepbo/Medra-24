(async () => {
  // Medra Doctor — turn the cmp/* frames on the doctor components page into component sets.
  // Doctor-module only: it looks at one page and removes only the sets it owns.
  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();
  const PAGE = 'Medra Doctor — 8 Components';
  let page = figma.root.children.find(n => n.name === PAGE);
  if (!page) return { error: `page "${PAGE}" not found — render the cmp/* frames first` };
  await figma.setCurrentPageAsync(page);

  const re = /^cmp\/(.+?)\/(.+?)=(.+)$/;
  const groups = {};
  for (const node of [...page.children]) {
    if (node.type !== 'FRAME') continue;
    const m = re.exec((node.name || '').trim());
    if (!m) continue;
    const [, comp, prop, value] = m;
    groups[comp] = groups[comp] || { prop, variants: {} };
    groups[comp].variants[value] = node;
  }
  if (!Object.keys(groups).length) return { error: 'no cmp/* frames found on the page' };

  const OWNED = new Set(Object.keys(groups).map(c => `Medra Doctor/${c}`));
  for (const node of [...page.children]) {
    if (node.type === 'COMPONENT_SET' && OWNED.has(node.name)) node.remove();
  }

  const REST = { 'Slot':'Open', 'Queue Row':'Waiting', 'Share Toggle':'Shared', 'Scope Line':'Granted',
                 'Drug Result':'Default', 'Stat Tile':'Info', 'Checklist Row':'Todo',
                 'Outcome':'Default', 'Rail Item':'Inactive' };
  const WIRING = {
    'Slot':          [['ON_CLICK','Booked']],
    'Queue Row':     [['ON_HOVER','Now']],
    'Share Toggle':  [['ON_CLICK','Withheld']],
    'Checklist Row': [['ON_CLICK','Done']],
    'Outcome':       [['ON_CLICK','Selected']],
    'Rail Item':     [['ON_HOVER','Active']],
  };
  const BACK = {
    'Slot':          [['ON_CLICK','Open']],
    'Queue Row':     [['ON_HOVER','Waiting']],
    'Share Toggle':  [['ON_CLICK','Shared']],
    'Outcome':       [['ON_CLICK','Default']],
    'Rail Item':     [['ON_HOVER','Inactive']],
  };
  const smart = (d = 0.16) => ({ type:'SMART_ANIMATE', easing:{type:'GENTLE'}, duration:d });
  const changeTo = id => ({ type:'NODE', destinationId:id, navigation:'CHANGE_TO', transition:smart() });

  const report = { sets:0, variants:0, reactions:0, components:[], notes:[] };
  let cursorX = 0, cursorY = 0, rowH = 0;

  for (const [comp, { prop, variants }] of Object.entries(groups)) {
    try {
      const comps = [];
      for (const [value, frame] of Object.entries(variants)) {
        const c = figma.createComponentFromNode(frame);
        c.name = `${prop}=${value}`;
        comps.push([value, c]);
      }
      const set = figma.combineAsVariants(comps.map(([, c]) => c), page);
      set.name = `Medra Doctor/${comp}`;
      set.layoutMode = 'HORIZONTAL';
      set.itemSpacing = 24;
      set.paddingLeft = set.paddingRight = set.paddingTop = set.paddingBottom = 24;
      set.primaryAxisSizingMode = 'AUTO';
      set.counterAxisSizingMode = 'AUTO';
      set.x = cursorX; set.y = cursorY;
      cursorX += set.width + 80;
      rowH = Math.max(rowH, set.height);
      if (cursorX > 2600) { cursorX = 0; cursorY += rowH + 80; rowH = 0; }

      const byValue = Object.fromEntries(comps);
      const rest = REST[comp];
      if (rest && byValue[rest]) {
        for (const [trigger, target] of (WIRING[comp] || [])) {
          if (!byValue[target]) continue;
          const existing = byValue[rest].reactions ? [...byValue[rest].reactions] : [];
          existing.push({ trigger:{ type:trigger }, actions:[changeTo(byValue[target].id)] });
          await byValue[rest].setReactionsAsync(existing);
          report.reactions++;
        }
        for (const [value, node] of comps) {
          if (value === rest) continue;
          for (const [trigger, target] of (BACK[comp] || [])) {
            if (!byValue[target] || value === target) continue;
            const existing = node.reactions ? [...node.reactions] : [];
            existing.push({ trigger:{ type:trigger }, actions:[changeTo(byValue[target].id)] });
            await node.setReactionsAsync(existing);
            report.reactions++;
          }
        }
      }
      report.sets++; report.variants += comps.length;
      report.components.push(`Medra Doctor/${comp} (${comps.map(([v]) => v).join(', ')})`);
    } catch (e) { report.notes.push(`${comp}: ${e.message}`); }
  }
  return report;
})();
