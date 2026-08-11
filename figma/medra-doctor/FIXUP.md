# Repairing the canvas without re-rendering it

Two defects were being generated at scale. Both are now fixed in the generator, so **any page
rendered from today onward is clean** — but a page already in Figma still carries them, and
re-rendering means deleting the page and losing anything changed by hand since.

`fix-layout.js` repairs them in place. It renders nothing, deletes nothing, and moves nothing.

---

## What it fixes

**1 · Empty space that will not close.** `<Frame grow={1} />` is a spacer — "push the next thing
to the far end of this row". It has no height, and **Figma gives a new frame 100×100 by
default**, so a 34px-tall row became 100px tall with a hole in it. In the layers panel it reads
as *W Fill × H 100 Hug*, which is exactly the frame you selected inside `Btn Doctor Dr. Ngozi
Okafor`. The same thing happens on the other axis: `<Frame w={7} />` inside a row is 100px tall,
and `<Frame h={4} />` inside a column is 100px wide.

The repair sets the spacer to **FILL on its parent's cross axis** — your own diagnosis, and the
right one. A spacer should take the size of the row it sits in, never dictate it.

**2 · Text left-aligned inside a centred card.** `items="center"` centres the text *node*; it
does not centre the text *inside* the node. Wherever the node ends up wider than the glyphs, the
label reads as left-aligned in a visibly centred card — the **Browse by specialty** grid is the
clearest case. The repair sets `textAlignHorizontal = CENTER` on any text whose container is
centred.

## What it will change

| Bundle | Spacers | Text nodes |
|---|---:|---:|
| `medra-member` | 108 | 635 |
| `medra-doctor` | 286 | 1,821 |
| `medra-org` | 48 | 1,469 |
| `medra-auth` | 88 | 190 |
| **Total** | **530** | **4,115** |

## How to run it

Figma Desktop open, the file open, `figma-cli` connected. From inside the bundle folder:

```powershell
figma-cli run .\fix-layout.js
```

It returns a report:

```json
{ "pages": [...], "spacersCollapsed": 108, "textCentred": 635,
  "nodesScanned": 41207, "failed": 0, "examples": [...] }
```

**To see what it would do without touching anything**, open `fix-layout.js` and set
`const DRY = true;` on the first line of the body, run it, then set it back.

Each bundle has its own copy, and each is **scoped to that module's own pages** — the member
script names the eight `Medra Member —` pages and will not touch a doctor or organisation page
even if they are in the same file. It is **idempotent**: running it twice reports 0 the second
time, because it skips anything already correct.

## The prompt, if you would rather ask than type

> Run the layout repair pass on this bundle. Figma Desktop is open and connected.
>
> ```powershell
> figma-cli run .\fix-layout.js
> ```
>
> It fixes two things in place on frames that are already rendered — empty spacer frames that
> are holding rows open at Figma's default 100px, and text that is left-aligned inside a centred
> container. It renders nothing and deletes nothing, and it only touches this module's own
> pages. Report back the `spacersCollapsed` and `textCentred` counts and anything in `failed`
> or `notes`. If `failed` is not 0, paste the `notes` array — do not re-run it or try to fix
> the nodes by hand.
>
> Do not re-render any page. Do not run `render-*.ps1`.

## Why this will not come back

`tools/figma/normalise.py` runs over every frame at build time, inside each `build_*.py`, before
anything is written to disk. Rule 1 fills the cross axis of every empty frame; rule 2 adds
`align="center"` to every text in a centred container. Both are applied to the parsed tree, not
to the string, so a tag is only rewritten when its parent actually says so.

You can confirm it on any bundle:

```bash
grep -c '<Frame grow={1} />' figma/medra-member/*.jsx    # 0
```

If either defect reappears, that is a bug in `normalise.py`, not something to fix by hand in
Figma again.
