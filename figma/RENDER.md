# Rendering — one page, four modules

The plan on this file caps it at three pages and there are four modules that used to want eight
each. **Every frame now renders onto one page**, and each module lays out in its own band so
they do not land on top of each other.

| | Band starts at | Frames |
|---|---:|---:|
| Member | y = 0 | 158 |
| Doctor | y = 60,000 | 275 |
| Organisation | y = 120,000 | 262 |
| Auth | y = 180,000 | 70 |

The page is called **`Medra`**. If you would rather use a page you already have, change
`ONE_PAGE` in `tools/figma/shell.py` and re-run the builders — it is one constant, and both the
render script and the linker read it.

---

## Before you render anything

**Your canvas is stale.** Every desktop screen changed when the three old shells were replaced
with one, so what is in Figma now is the old design. Re-rendering **appends** rather than
replaces, so rendering on top of it gives you two of everything.

Delete the old frames first. On the page holding them:

```powershell
figma-cli eval "(async()=>{const p=figma.currentPage;const n=p.children.length;for(const f of [...p.children]) f.remove();return 'removed '+n;})()"
```

That empties the current page. Check you are on the right one first — it does not ask.

**`fix-layout.js` is no longer needed for anything you re-render.** It repairs frames drawn
before `normalise.py` existed; everything rendered from these bundles is already correct. Keep it
only for frames you are not re-rendering.

## Rendering

Figma Desktop open, the file open, `figma-cli` connected. From inside each bundle folder, in this
order — the modules cross-link, and the linker resolves what is in the file at the time it runs:

```powershell
cd medra-auth   ; .\render-auth.ps1
cd ..\medra-member ; .\render-member.ps1
cd ..\medra-doctor ; .\render-doctor.ps1
cd ..\medra-org    ; .\render-org.ps1
```

Each script primes the icon cache, imports the tokens, selects the one page, renders its frames
in flow order, and then runs its linker. The linker wires the prototype, lays that module's band
out, and sets its flow starting points.

**765 frames is a lot to render in one sitting.** If a script stops part-way, re-run it — but
delete that module's frames first, or you will get duplicates of everything it already drew.

## Afterwards

Each linker returns a report. The one field worth reading is `missing`: a non-empty list means a
transition names a frame that is not in the file yet, which usually means a module has not been
rendered. Render it and re-run the linker; the linkers are safe to re-run on their own.

Verify before and after:

```bash
python3 tools/figma/proto_check.py figma/medra-member link-member.js
```

All four currently report **PROTOTYPE COMPLETE** — 765 frames, 678 screens, every one reachable,
no broken hotspots.

## What you will see on the page

Each band is one module. Within a band, each section is a horizontal row of desktop frames with
its mobile frames directly beneath, and the next section starts below that. The flow starting
points are named `<Section> · Desktop` and `<Section> · Mobile`, so the presentation picker lists
them in journey order rather than making you hunt for a frame.
