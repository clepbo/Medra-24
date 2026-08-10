# Instruction for the terminal (figma-ds-cli)

Copy everything between the lines into the terminal session that has Figma Desktop connected.

---

You are rendering **the Medra Organisation module only**. Do not create, edit, rename, re-render
or delete anything on any page that does not begin with `Medra Org —`. The design-system,
authentication, member and doctor pages in this file are finished — leave them alone.

**Working directory:** the unzipped `medra-org` folder. Confirm you can see `render-org.ps1`,
`link-org.js`, `DESIGN.md`, `pages.json`, 217 `.jsx` files and an `assets/` folder before starting.

**Run, in this order:**

1. Prime the offline icon cache (safe to re-run, it only copies files):
   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
   Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
   ```

2. Everything else:
   ```powershell
   .\render-org.ps1
   ```

**What that script does, so you can verify it is behaving:**
- imports `DESIGN.md` — the same 41 tokens already in the file, so it is a no-op;
- creates (or reuses) exactly eight pages, `Medra Org — 1 Setup & Verification` through
  `Medra Org — 8 Components`;
- renders 217 frames into them;
- runs `link-org.js`, which wires the prototype, closes the navigation, gives each page two flow
  starting points and arranges the desktop row above the matching mobile row.

**Report back with:**
- the object `link-org.js` returns — `{ linked, navLinked, stayOnScreen, framesFound, missing }`;
- any frame that failed to render, by filename.

**If `missing` is not empty:** that frame did not render. Re-render just that one file —
`figma-cli render (Get-Content <name>.jsx -Raw)` on the right page — then re-run
`figma-cli run .\link-org.js`. Do not re-run the whole script.

**If a render errors:** paste the exact CLI error and the filename. Do not fix the `.jsx`
yourself — the generator is the source of truth and the fix belongs upstream.

**Note on re-rendering:** the CLI *appends*. If a `Medra Org —` page already has frames from a
previous run, delete them first or the page will end up with two of everything.

---

## Expected result

| | |
|---|---|
| Pages created | 8, all prefixed `Medra Org —` |
| Frames rendered | 217 (57 desktop screens + 141 mobile + 19 component states) |
| Prototype links | 699 explicit + 3,384 navigation, plus a sweep so no `Btn` node is dead |
| Pages touched outside the organisation module | **0** |
