# Rendering — one page, four modules

The plan on this file caps it at three pages and there are four modules that used to want eight
each. **Every frame now renders onto one page**, and each module lays out in its own band so
they do not land on top of each other.

| | Band starts at | Frames |
|---|---:|---:|
| Member | y = 0 | 158 |
| Doctor | y = 60,000 | 275 |
| Organisation | y = 120,000 | 316 |
| Auth | y = 180,000 | 90 |

The page is called **`Medra`**. If you would rather use a page you already have, change
`ONE_PAGE` in `tools/figma/shell.py` and re-run the builders — it is one constant, and both the
render script and the linker read it.

---

## Rendering

Figma Desktop open on the target file, `figma-cli` connected, then from this folder:

```powershell
cd figma
.\render-all.ps1
```

That is the whole thing. It selects (or creates) the page, **deletes the frames it is about to
replace**, renders all four modules in dependency order, and runs the four linkers.

**Why one script rather than four.** The per-module scripts each work, but none of them deletes,
and re-rendering **appends**. That is the one way an 870-frame render goes wrong: it stops half
way, somebody re-runs it, and now there are two of everything with no way to tell which is
which. `render-all.ps1` deletes first and says how many frames it removed.

**The delete is scoped by frame name, not by page.** Every Medra frame is named for its module —
`Member · …`, `Doctor · …`, `Org · …`, `Auth · …`, plus the component frames under `cmp/`.
Nothing else on the page is touched, so a page you are also using for something else survives.

### If it stops part way

Re-run the module it stopped on. That deletes only that module's frames and redraws them:

```powershell
.\render-all.ps1 -Only org
```

Other flags: `-Page "Some other page"` to render somewhere else, `-KeepOld` to skip the delete
(you will get duplicates — it exists for the case where you are deliberately rendering a second
copy alongside the first).

### Running the four by hand

Still supported, and still in the same order — the modules cross-link, and each linker resolves
what is in the file at the time it runs:

```powershell
cd medra-auth   ; .\render-auth.ps1
cd ..\medra-member ; .\render-member.ps1
cd ..\medra-doctor ; .\render-doctor.ps1
cd ..\medra-org    ; .\render-org.ps1
```

Each script primes the icon cache, imports the tokens, selects the one page, renders its frames
in flow order, and then runs its linker. **None of them deletes**, so clear the old frames first
if you go this way.

## Afterwards

Each linker returns a report. The one field worth reading is `missing`: a non-empty list means a
transition names a frame that is not in the file yet, which usually means a module has not been
rendered. Render it and re-run the linker; the linkers are safe to re-run on their own.

Verify before and after:

```bash
python3 tools/figma/proto_check.py figma/medra-member link-member.js
```

All four currently report **PROTOTYPE COMPLETE** — 839 frames, 751 screens, every one reachable,
no broken hotspots.

## What you will see on the page

Each band is one module. Within a band, each section is a horizontal row of desktop frames with
its mobile frames directly beneath, and the next section starts below that. The flow starting
points are named `<Section> · Desktop` and `<Section> · Mobile`, so the presentation picker lists
them in journey order rather than making you hunt for a frame.
