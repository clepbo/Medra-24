# Medra Design System — Terminal Setup (for terminal-Claude / figma-ds-cli)

This bundle renders into **Figma Desktop** with `figma-ds-cli` — no API key, no internet.
Run everything **from inside this unzipped folder**, with Figma Desktop open and connected.

- **21 frames** (`*.jsx`) · **75 icons** (offline cache) · **1 linker** (`link-medra.js`)
- Tokens: `DESIGN.md` (single-mode LIGHT) · Font: **Inter** (ships with Figma)
- Offline validation: **ALL 21 CLEAN, FULLY OFFLINE ✓** (run `node validate.js` to re-check)

> **No client patch needed.** Icon colours use hex values (not `var:token`), so the
> `<Icon>`/`/`-in-colour parser bug does not apply — you do **not** need a patched
> `figma-client.js` for this bundle. If your global cache is empty, step 1 primes it.

---

## 1. Prime the offline icon cache (once per machine)
```powershell
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
```

## 2. Create / activate the target page
```powershell
figma-cli eval "(async()=>{const t='Medra — Design System';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return figma.currentPage.name;})()"
```

## 3. Import design tokens (single-mode) — skip if already imported
```powershell
figma-cli tokens import-design-md .\DESIGN.md
```

## 4a. FULL render (first time)
```powershell
Get-ChildItem .\*.jsx | Sort-Object Name | ForEach-Object { figma-cli render (Get-Content $_.FullName -Raw) }
```

## 4b. OR incremental (only changed frames; keeps your layout)
```powershell
.\render-changes.ps1                 # all
.\render-changes.ps1 15-*.jsx        # just the buttons frame, etc.
```

## 5. Wire the prototype **and arrange the canvas**
```powershell
figma-cli run .\link-medra.js
```
This does two things: (a) **arranges all 21 frames into grouped section rows** —
Brand · Identity · Foundations · Components · Expression — so the canvas reads top-to-bottom
by section instead of one long line; and (b) wires navigation. It returns
`{ linked, framesFound, missingHotspots }`. **If `missingHotspots` is non-empty**, that frame
is a stale render — re-render just that `.jsx` (step 4b) and re-run the linker. Flow start is
set to **00 Cover**.

> Re-running the linker re-arranges the grid. If you later hand-arrange frames yourself,
> just don't re-run it — name-based linking means your layout is preserved regardless.

---

## Preview without Figma
`preview.html` is a self-contained browser preview of all 21 frames (approximate — the real
render is Figma). Open it in any browser. `medra-ds-overview.png` is the contact sheet.

## Notes
- One `.jsx` = one editable Figma frame. Rearranging frames on the canvas is safe —
  linking is by **frame name + button text**, not position.
- Images are local under `assets/` and embedded at render time (no remote URLs).
- To embed the **3D hero logo**, drop your PNG at `assets/logo/hero-white.png`
  (transparent, ~1600px wide) and re-render `00-cover.jsx` and `20-contact.jsx`.
