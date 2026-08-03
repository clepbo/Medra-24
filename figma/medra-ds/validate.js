#!/usr/bin/env node
/* Offline validator for the Medra design-system bundle.
   Checks the figma-ds-cli DSL hard rules against every .jsx, with network assumed off.
   Rules: colours are #RRGGBB or var:token (no rgba/rgb) · no NaN · every <Text> has font=
   · no items="stretch" · no <b>/<strike> · every var: token exists in DESIGN.md
   · every <Icon> resolves in assets/icon-cache · every image= resolves on disk. */
const fs = require('fs'), path = require('path');
const ROOT = __dirname;
const ICON_DIR = path.join(ROOT, 'assets/icon-cache');

// --- collect valid tokens from DESIGN.md ---
const design = fs.readFileSync(path.join(ROOT, 'DESIGN.md'), 'utf8');
const tokenSet = new Set();
for (const m of design.matchAll(/^\|\s*([a-z0-9]+\/[a-z0-9-]+)\s*\|\s*(#[0-9A-Fa-f]{6})/gm)) tokenSet.add(m[1]);
// also allow type-scale / radius names referenced only in docs (not as var:)

const jsxFiles = fs.readdirSync(ROOT).filter(f => f.endsWith('.jsx')).sort();
let errors = 0, warnings = 0;
const iconCache = new Set(fs.readdirSync(ICON_DIR));

function iconFile(name) {           // lucide:heart-pulse -> lucide_heart_pulse.svg
  const bare = name.replace(/^lucide:/, '');
  return 'lucide_' + bare.replace(/[^a-z0-9]/gi, '_') + '.svg';
}

for (const file of jsxFiles) {
  const src = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const report = msg => { console.log(`  ✗ ${file}: ${msg}`); errors++; };

  // 1. no rgba()/rgb()
  if (/\brgba?\(/.test(src)) report('uses rgb()/rgba() — colours must be #hex or var:token');
  // 2. no NaN
  if (/\bNaN\b/.test(src)) report('contains NaN');
  // 3. items="stretch"
  if (/items="stretch"/.test(src)) report('uses items="stretch" (rejected by CLI)');
  // 4. no <b>/<strike>
  if (/<\/?b>|<strike/i.test(src)) report('uses <b>/<strike> — use weight="bold"');
  // 5. every <Text ...> has font=
  for (const m of src.matchAll(/<Text\b([^>]*)>/g)) {
    if (!/\bfont=/.test(m[1])) report('a <Text> is missing font=');
  }
  // 6. colour values: every color=/bg=/stroke= must be #RRGGBB or var:token
  for (const m of src.matchAll(/\b(?:color|bg|stroke)="([^"]+)"/g)) {
    const v = m[1];
    if (v.startsWith('var:')) {
      const tok = v.slice(4);
      if (!tokenSet.has(tok)) report(`unknown var token: ${v}`);
    } else if (!/^#[0-9A-Fa-f]{6}$/.test(v)) {
      report(`bad colour value: ${v}`);
    }
  }
  // 7. icons resolve
  for (const m of src.matchAll(/<Icon\b[^>]*name="([^"]+)"/g)) {
    const f = iconFile(m[1]);
    if (!iconCache.has(f)) report(`icon not in cache: ${m[1]} (${f})`);
  }
  // 8. images resolve on disk
  for (const m of src.matchAll(/image="([^"]+)"/g)) {
    const p = m[1];
    if (/^https?:/.test(p)) report(`remote image not allowed: ${p}`);
    else if (!fs.existsSync(path.join(ROOT, p))) report(`missing image: ${p}`);
  }
  // 11. wrap="wrap" is NOT honoured by figma-ds-cli — rows must be chunked explicitly
  if (/wrap="wrap"/.test(src)) report('uses wrap="wrap" — the CLI ignores it, chunk rows with rows_of()');

  // 9. exactly one root <Frame> with a name
  const roots = src.match(/^<Frame\b[^>]*name="/);
  if (!roots) { console.log(`  ! ${file}: root frame has no name=`); warnings++; }
}

console.log('');
if (errors === 0)
  console.log(`ALL ${jsxFiles.length} CLEAN, FULLY OFFLINE ✓  (icons: ${iconCache.size}, tokens: ${tokenSet.size}, warnings: ${warnings})`);
else
  console.log(`${errors} error(s) across ${jsxFiles.length} files — fix before delivery.`);
process.exit(errors === 0 ? 0 : 1);
