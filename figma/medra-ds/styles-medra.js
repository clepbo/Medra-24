(async () => {
  // ============================================================
  // Medra — create Figma Variables + Styles (colour, type, effect)
  // Run:  figma-cli run .\styles-medra.js
  // Idempotent: removes any existing "Medra/…" styles + Medra collections first.
  // ============================================================
  const hexRGB = h => {
    h = h.replace('#', '');
    return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 };
  };
  const rgba = (h, a) => Object.assign(hexRGB(h), { a });

  // ---- palette (mirrors DESIGN.md) ----
  const COLORS = {
    'bg/base': '#FFFFFF', 'bg/subtle': '#F4F6F8', 'bg/muted': '#EAF1F5', 'bg/band': '#0F2233', 'bg/band-2': '#143352',
    'brand/navy-deep': '#0F2233', 'brand/navy': '#1B3A5B', 'brand/blue': '#245F88', 'brand/blue-light': '#2F8BAC', 'brand/teal': '#39B0CF', 'brand/teal-bright': '#3BB6D2',
    'text/strong': '#0F2233', 'text/default': '#1B3A5B', 'text/muted': '#5B6B7A', 'text/faint': '#91A2B0', 'text/on-dark': '#FFFFFF', 'text/on-dark-muted': '#A9C2D4', 'text/accent': '#2F8BAC',
    'border/subtle': '#E6ECF1', 'border/default': '#D3DEE7', 'border/strong': '#B4C4D1', 'border/accent': '#39B0CF',
    'state/success': '#2FA36B', 'state/success-bg': '#E6F5EE', 'state/warning': '#E0A32E', 'state/warning-bg': '#FBF1DD',
    'state/error': '#D14343', 'state/error-bg': '#FBE9E9', 'state/info': '#2F8BAC', 'state/info-bg': '#E4F0F5',
    'neutral/50': '#F7F9FB', 'neutral/100': '#EEF2F6', 'neutral/200': '#E1E8EE', 'neutral/300': '#CBD6DF', 'neutral/400': '#A7B6C2',
    'neutral/500': '#7E8F9D', 'neutral/600': '#5B6B7A', 'neutral/700': '#3E4C59', 'neutral/800': '#26323D', 'neutral/900': '#0F2233'
  };
  const SPACING = { '4': 4, '8': 8, '12': 12, '16': 16, '24': 24, '32': 32, '48': 48, '64': 64, '96': 96 };
  const RADIUS = { 'sm': 8, 'md': 12, 'lg': 16, 'xl': 24, 'pill': 999 };
  const TYPE = [
    ['Display', 'Bold', 72, 120], ['H1', 'Bold', 48, 120], ['H2', 'Bold', 32, 125], ['H3', 'Semi Bold', 24, 130],
    ['Title', 'Semi Bold', 18, 140], ['Body', 'Regular', 16, 150], ['Small', 'Regular', 14, 150], ['Caption', 'Medium', 12, 140]
  ];
  const EFFECTS = [
    ['Elevation/E1 Card', [{ type: 'DROP_SHADOW', color: rgba('#0F2233', 0.06), offset: { x: 0, y: 2 }, radius: 8, spread: 0, visible: true, blendMode: 'NORMAL' }]],
    ['Elevation/E2 Popover', [{ type: 'DROP_SHADOW', color: rgba('#0F2233', 0.12), offset: { x: 0, y: 8 }, radius: 24, spread: 0, visible: true, blendMode: 'NORMAL' }]],
    ['Focus Ring', [{ type: 'DROP_SHADOW', color: rgba('#39B0CF', 0.9), offset: { x: 0, y: 0 }, radius: 0, spread: 3, visible: true, blendMode: 'NORMAL' }]]
  ];

  const report = { variables: 0, paintStyles: 0, textStyles: 0, effectStyles: 0, notes: [] };

  // ---- clean up previous Medra styles / collections ----
  (await figma.getLocalPaintStylesAsync()).filter(s => s.name.startsWith('Medra/')).forEach(s => s.remove());
  (await figma.getLocalTextStylesAsync()).filter(s => s.name.startsWith('Medra/')).forEach(s => s.remove());
  (await figma.getLocalEffectStylesAsync()).filter(s => s.name.startsWith('Medra/')).forEach(s => s.remove());
  for (const c of await figma.variables.getLocalVariableCollectionsAsync()) {
    if (c.name.startsWith('Medra')) c.remove();
  }

  // ---- VARIABLES: colour collection (single mode) ----
  try {
    const col = figma.variables.createVariableCollection('Medra Colour');
    col.renameMode(col.modes[0].modeId, 'Light');
    const mode = col.modes[0].modeId;
    for (const [name, hex] of Object.entries(COLORS)) {
      const v = figma.variables.createVariable(name, col, 'COLOR');
      v.setValueForMode(mode, hexRGB(hex));
      report.variables++;
    }
    // number scale collection
    const num = figma.variables.createVariableCollection('Medra Scale');
    num.renameMode(num.modes[0].modeId, 'Value');
    const nmode = num.modes[0].modeId;
    for (const [k, val] of Object.entries(SPACING)) { const v = figma.variables.createVariable('spacing/' + k, num, 'FLOAT'); v.setValueForMode(nmode, val); report.variables++; }
    for (const [k, val] of Object.entries(RADIUS)) { const v = figma.variables.createVariable('radius/' + k, num, 'FLOAT'); v.setValueForMode(nmode, val); report.variables++; }
  } catch (e) { report.notes.push('variables: ' + e.message); }

  // ---- PAINT STYLES (colour styles) ----
  for (const [name, hex] of Object.entries(COLORS)) {
    try {
      const ps = figma.createPaintStyle();
      ps.name = 'Medra/' + name;
      ps.paints = [{ type: 'SOLID', color: hexRGB(hex) }];
      report.paintStyles++;
    } catch (e) { report.notes.push('paint ' + name + ': ' + e.message); }
  }

  // ---- TEXT STYLES ----
  const fonts = ['Regular', 'Medium', 'Semi Bold', 'Bold'];
  for (const style of fonts) {
    try { await figma.loadFontAsync({ family: 'Inter', style }); }
    catch (e) { report.notes.push('font Inter ' + style + ' missing — install Inter in Figma'); }
  }
  for (const [name, weight, size, lh] of TYPE) {
    try {
      const ts = figma.createTextStyle();
      ts.name = 'Medra/' + name;
      ts.fontName = { family: 'Inter', style: weight };
      ts.fontSize = size;
      ts.lineHeight = { value: lh, unit: 'PERCENT' };
      report.textStyles++;
    } catch (e) { report.notes.push('text ' + name + ': ' + e.message); }
  }

  // ---- EFFECT STYLES ----
  for (const [name, effects] of EFFECTS) {
    try {
      const es = figma.createEffectStyle();
      es.name = 'Medra/' + name;
      es.effects = effects;
      report.effectStyles++;
    } catch (e) { report.notes.push('effect ' + name + ': ' + e.message); }
  }

  return report;
})();
