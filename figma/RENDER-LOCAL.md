# Rendering from your own machine

Rendering has to happen where Figma Desktop is. `figcli` is a bridge to the running app over
localhost, so it only exists on the machine you are sitting at — a Claude session in a container
has no Figma Desktop to talk to, and `--dangerously-skip-permissions` only removes permission
prompts, it does not conjure one.

So the render is yours to run. This is everything it needs.

---

## The short version

```powershell
figcli                     # in one terminal, leave it running
```

```powershell
cd <wherever you keep Medra-24>
git pull
cd figma
.\render-all.ps1
```

That is it. 839 frames, four modules, all four prototypes wired.

**It deletes before it draws.** Re-rendering *appends* in Figma, so this clears the frames it is
about to replace first — scoped by frame name (`Member · `, `Doctor · `, `Org · `, `Auth · `,
`cmp/`), never by page, so anything else on that page survives.

If it stops part way, re-run just that module — it clears only that module's frames:

```powershell
.\render-all.ps1 -Only org
```

---

## If you are working from the zips instead of the repo

Put the four `.zip` files in one folder together with `render-all.ps1` and run it. It expands any
bundle it does not already find unpacked, so pasting zips still works:

```
somewhere\
  render-all.ps1
  medra-auth.zip
  medra-member.zip
  medra-doctor.zip
  medra-org.zip
```

```powershell
.\render-all.ps1
```

---

## Pasting this to a local Claude session

If you would rather have Claude drive it, this is the whole instruction — nothing else needs
explaining, because the script carries the ordering, the deleting and the linking:

> Run `figma/render-all.ps1` from the Medra-24 checkout, with figcli already running and Figma
> Desktop open on the Medra file. It renders all four modules and wires the prototypes. If it
> stops part way, re-run only the module it stopped on with `-Only <module>` — do not re-run the
> whole thing, and do not run the per-module `render-*.ps1` scripts directly, because those do
> not delete and Figma appends. When it finishes, tell me the `missing` list from each of the
> four linker reports.

---

## What to check when it finishes

Each linker prints a report. The one field worth reading is **`missing`** — a non-empty list
means a transition names a frame that is not in the file, which normally means a module did not
finish rendering. Render that module and re-run its linker; the linkers are safe to re-run on
their own.

Then, in the repo:

```bash
python3 tools/figma/proto_check.py figma/medra-org link-org.js
```

All four report **PROTOTYPE COMPLETE** against the built bundles today — 839 frames, 751 screens,
every one reachable, no broken hotspots. If Figma disagrees with that, the difference is
something that happened during the render rather than something wrong with the bundle.

---

## What you will see on the page

One page, `Medra`, with each module in its own band:

| | Band starts at | Frames |
|---|---:|---:|
| Member | y = 0 | 158 |
| Doctor | y = 60,000 | 275 |
| Organisation | y = 120,000 | 316 |
| Auth | y = 180,000 | 90 |

Within a band each section is a row of desktop frames with its mobile frames directly beneath.
The flow starting points are named `<Section> · Desktop` and `<Section> · Mobile`, so the
presentation picker lists them in journey order instead of making you hunt for a frame.
