# Arranging the Figma page by function

The page is laid out by **module** — member, doctor, organisation, auth — because that is how it
was built. That is a producer's order. It answers *"where does this screen live"* and not the
question anybody actually arrives with, which is **"show me how somebody books a visit"**.

This re-lays it out by what a person can **do**: a banner for each persona, a banner for each
function under it, and beneath each function the screens that carry it end to end, in the order
somebody meets them.

**12 personas · 70 functions · 234 screens · 27 of them copied into a second function.**

The full inventory is `docs/Functions.md`. Both it and the script are generated from
`tools/figma/functions.py`, so they cannot drift apart.

> **This has been run — 20 August 2026.** File `QCHjeHd3quYt5HXWUpCBFp`, page `64:49`. Read back
> from the live file: **12 persona banners, 70 function banners, 839 screen frames** (767 unique
> plus 72 marked `(copy)`), with the 87 `cmp/…` component frames on the design-system page
> `15:2`. The banners were drawn `◆ Persona: …` and `◇ Function: …`.
>
> The instructions below stand for the next run. It is idempotent, so re-running after any
> re-render is the normal thing to do, not a repair.

---

## Run it

```powershell
figcli                                  # bridge running, Figma Desktop open on the file

cd figma
figma-cli run .\arrange-by-function.js
```

It returns a JSON report. **These are the numbers a correct run produces** — they come from a
dry run of the same matching against the built bundles, so anything different is worth
explaining before you go further:

| field | expected | means |
|---|---:|---|
| `personas` | 12 | persona banners drawn |
| `functions` | 70 | function banners drawn |
| `moved` | 752 | original frames repositioned |
| `copied` | 87 | clones made — 27 screens, counted as all their frames |
| `missing` | 0 | screens the map wants that the page does not have |
| `strays` | 0 | frames on the page no function claims (`cmp/…` are not counted) |
| `cleared` | 0 first time | banners and clones removed from a previous run |

`moved + copied` should be **839** — every frame in the file.

---

## Order matters, and getting it wrong costs you the arrangement

```
1.  .\render-all.ps1          renders every frame and runs the four linkers
2.  read the linker reports   'missing' must be empty on all four
3.  arrange-by-function.js    ← only now
```

**Running a linker after the arrangement undoes it.** The linkers lay each module's band out
from scratch; that is their job. If you re-render or re-link anything afterwards, run the
arrangement again — it is idempotent and cheap.

---

## What the script does to your file

| | |
|---|---|
| **Moves originals** | Each screen keeps exactly one original — the frame carrying the prototype wiring — and it is moved into the function that owns it |
| **Clones copies** | A screen doing two jobs is cloned into the second one, **with its reactions stripped**. Two frames answering the same click is how a prototype quietly becomes untrustworthy, so copies are inert. They are there to read, not to click |
| **Draws banners** | One per persona (large) and one per function, in the navy→blue gradient |
| **Is idempotent** | Re-running removes the banners and clones it made last time, then rebuilds. Copies do not multiply |
| **Deletes nothing else** | A frame it cannot find is reported, not invented. A frame it does not know about is left exactly where it is |

---

## What to look out for

Seven things, in the order they are likely to bite.

**1. `missing` should be empty.** Every entry is a screen the map expects and the page does not
have. One or two means that module did not finish rendering. A whole block of them from one
persona means a module was never rendered at all.

**2. `strays` should be small, and every one should be explainable.** These are frames on the
page that no function claims. Expect the component frames (`cmp/…`) and nothing else. A stray
that is a real screen means the map in `tools/figma/functions.py` is out of date — a screen was
added and never assigned a function. That is a map bug, not a Figma bug: fix the map, regenerate,
re-run.

**3. `copied` should be 87** — that is 27 screens counted as all their frames, desktop plus
mobile plus mobile sections. Higher means clones from an earlier run were not cleared; check
nothing was renamed, because the cleanup finds them by the ` (copy)` suffix.

**4. The prototype must still work from the originals.** Open any flow starting point and click
through. If a click lands on a copy, a clone kept its reactions — report it, do not fix it by
hand, because the next run would reintroduce it.

**5. Watch the ampersand screens.** Thirteen frames have `&` in their name — `Review & Sign`,
`Review & Confirm`, `Devices & Security`, `Lab Results & Diagnostics`, `Types & Fees`,
`Account & Security`, `Language & Accessibility`, `Privacy & Data`, `Privacy & Compliance`,
`Administer & Record`, `Roles & Permissions`, `Plan & Seats`, `Bookings & Allocation`. The
script normalises `&amp;` before matching, but if any of those turn up in `missing`, that
normalisation is the first place to look, not the render.

**6. Two screens have mobile frames that do not follow the naming convention** —
`H2 First Visit (empty state)` has a mobile called `H2 First Visit · Mobile`, and
`R3 Lab Results & Diagnostics` has `R3 Lab Result · Mobile`. The script matches on an exact
frame list rather than on a name prefix precisely because of these two, so they should be fine.
If either turns up in `missing`, that is why.

**7. Nothing should overlap.** Each function's screens are laid out left to right, each screen as
a column with its desktop frame on top and its mobile frames beneath. If two functions collide
vertically, a screen family is taller than the layout expected — say which one and by how much.

---

## Write this report when you are done

Short, and in this shape. It is the thing that gets read, not the JSON.

```
ARRANGEMENT REPORT — <date>

Ran against: <file name> / page <page name>
Script report: personas <n>, functions <n>, moved <n>, copied <n>,
               missing <n>, strays <n>, cleared <n>

MISSING          <list them, or "none">
                 For each: which persona and function expected it, and your best guess
                 at why it is not on the page.

STRAYS           <count, and what they are>
                 Component frames are expected. Name any real screen that appears here —
                 it means the function map does not know about it.

PROTOTYPE        Clicked through <n> flows from the starting points. <worked / what broke>

OVERLAPS         <none, or which two functions and by how much>

READABILITY      The part a script cannot check. Walking the page top to bottom as somebody
                 who has never seen it:
                   · does each function read as one complete job, or does a story stop
                     half way and continue three banners later?
                   · is any function so large it should be two? (over about ten screens,
                     ask whether it is really one job)
                   · is any function a single screen that would be better folded into
                     its neighbour?
                   · do the copies help, or do they make the page feel repetitive?

RECOMMEND        Concrete changes to tools/figma/functions.py — which screen should move
                 to which function, which functions should split or merge. Do not edit the
                 generated files; edit the map and regenerate.
```

---

## Changing the grouping

Edit `PERSONAS` in `tools/figma/functions.py`, then:

```bash
python3 tools/figma/functions.py --check     # every id resolves? nothing orphaned?
python3 tools/figma/functions.py             # regenerate both artefacts
```

`--check` fails loudly on a screen id that does not exist and lists any screen no function
claims. A map that silently skips a screen is worse than no map, so it will not generate until
both are clean.
