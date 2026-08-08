# Instruction for the terminal (figma-ds-cli)

Copy everything between the lines into the terminal session that has Figma Desktop connected.

---

You are rendering **the Medra Doctor module only**. Do not create, edit, rename, re-render or
delete anything on any page that does not begin with `Medra Doctor —`. The design-system,
authentication and member pages in this file are finished and signed off — leave them alone.

**Working directory:** the unzipped `medra-doctor` folder. Confirm you can see
`render-doctor.ps1`, `link-doctor.js`, `components-doctor.js`, `DESIGN.md`, `pages.json`,
239 `.jsx` files and an `assets/` folder before you start.

**Run, in this order:**

1. Prime the offline icon cache (safe to re-run, it only copies files):
   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
   Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
   ```

2. Everything else:
   ```powershell
   .\render-doctor.ps1
   ```

**What that script does, so you can verify it is behaving:**
- imports `DESIGN.md` — the same 41 tokens already in the file, so it is a no-op; it never
  removes or renames a token;
- creates (or reuses) exactly eight pages: `Medra Doctor — 1 Getting Started` through
  `Medra Doctor — 8 Components`;
- renders 215 screen frames and 24 `cmp/*` frames into those pages
  (46 desktop screens; on mobile each is a hub plus its section and sheet frames);
- runs `components-doctor.js`, which touches **only** page 8 and removes only component sets it
  owns (`Medra Doctor/…`);
- runs `link-doctor.js`, which wires the prototype, closes the navigation, gives each page two
  flow starting points (`… · Desktop` and `… · Mobile`) and arranges each page with the desktop
  row on top and the matching mobile row beneath.

**Report back with:**
- the object `link-doctor.js` returns — `{ linked, navLinked, stayOnScreen, framesFound, missing }`;
- the object `components-doctor.js` returns — `{ sets, variants, reactions, components, notes }`;
- any frame that failed to render, by filename.

**If `missing` is not empty:** that frame did not render. Re-render just that one file —
`figma-cli render (Get-Content <name>.jsx -Raw)` on the right page — then re-run
`figma-cli run .\link-doctor.js`. Do not re-run the whole script.

**If a render errors:** paste the exact CLI error and the filename. Do not attempt to fix the
`.jsx` yourself — the generator is the source of truth and the fix belongs upstream.

**Do not:** run any other `link-*.js` or `components-*.js` from another bundle in this session,
reorder or delete existing pages, or "tidy up" frames on pages you did not create.

---

## Expected result

| | |
|---|---|
| Pages created | 8, all prefixed `Medra Doctor —` |
| Frames rendered | 239 (215 screens + 24 component states) |
| Component sets | 10, named `Medra Doctor/…` |
| Prototype links | 906 explicit + 2,795 navigation, plus a sweep so no `Btn` node is dead |
| Pages touched outside the doctor module | **0** |
