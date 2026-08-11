# Medra — project handoff

**Everything needed to pick this project up cold**, in one file: what Medra is, what has been
designed, how the design is produced, how to instruct the CLI that renders it into Figma, and
what is left. Kept current — it is updated in the same commit as the work it describes.

| | |
|---|---|
| **Document version** | **v1.4** |
| **Last updated** | 11 August 2026 (spacer and text-alignment defects fixed at source · in-place repair pass added) |
| **Repo** | `clepbo/Medra-24` |
| **Working branch** | `claude/new-project-prd-stories-ss2qlr` |
| **Current PRD** | `docs/Medra_PRD_v2.0.md` (v1.0 kept, marked superseded) |
| **Owner** | Godwin Okwor (Product) · Israel Oni (UI/UX) |

---

## 1. What Medra is

A unified medical records and consultation-booking platform for Nigeria, piloting in Abuja.
Private healthcare there runs on paper files and WhatsApp diaries: records are siloed per
hospital, patients physically carry printed results, and a new doctor sees no prior history.

Medra is four layers:

1. **Member booking** — find a verified doctor or organisation, see real availability, book and
   pay before leaving home.
2. **An organisation operating system** — bookings, allocation across departments, staff, seats.
3. **The clinical chain** — nurses, lab technicians and pharmacists enter the work they do, so
   the doctor reads a prepared record instead of typing one.
4. **A portable record** — owned by the member, carried between institutions, with every clinical
   fact marked as verified or self-reported.

**Business model:** organisations and independent practitioners pay a subscription priced by
practitioners, branches and seats. Members are never charged. *(Open: whether Medra also collects
consultation fees — see §9.)*

**The one-line thesis:** *can a member see whether a doctor is free and book before leaving home*,
while capturing enough record to be clinically useful.

---

## 2. Vocabulary that matters

| Term | Meaning |
|---|---|
| **Member** | A person using Medra for their own care. **Never say "patient"** — decided at the 9 Aug review. |
| **Medra ID** | `MDR-8842-19`. The member's identifier, on their phone and any printed summary. |
| **Organisation** | A hospital, clinic, diagnostic lab or pharmacy. Identified by **RC number AND practice licence** — RC alone proves a company exists, not that it may practise. |
| **Department** | The unit an organisation onboards and buys **seats** in: laboratory, pharmacy, nursing, front desk, a clinical specialty. Permissions follow the department, not the person. |
| **Order** | A unit of work a doctor raises for a department — a test, an injection, a dispense. |
| **Not medically verified** | The state of any health fact a member entered themselves. Travels with the value into every view, including another hospital's. |
| **External access grant** | A scoped, single-use, consent-gated link (`medra.ng/<Medra ID>`) letting a party not on Medra read what they need and return a result. |
| **Episode of care** | The scope of access. Never per person, never permanent. |

---

## 3. Where the design is now

Five rendered bundles, **742 frames**, all validated clean and fully offline.

| Bundle | Frames | Pages | Status |
|---|---:|---:|---|
| `figma/medra-ds` — design system + journeys | 27 | 1 | Done |
| `figma/medra-auth` — authentication, 4 roles | 70 | 4 | Done · **v2.0 retrofit applied** |
| `figma/medra-member` — the whole member app | 158 | 8 | Done · **prototype complete** |
| `figma/medra-doctor` — full doctor module | 270 | 8 | Done · **prototype complete** |
| `figma/medra-org` — organisation + clinical chain + external | 217 | 8 | Done · **not yet rendered into Figma** |

`medra-member` was two bundles until the merge (`medra-member` for find & book,
`medra-member-2` for everything the bottom nav led to). The split existed because batch 1 was
already rendered and signed off when batch 2 started; it cost a real thing — batch 2 read
batch-1's frame names off disk to build its own tab bar, and no single audit could see the whole
app — so it is now one bundle, one builder (`tools/figma/build_member.py`), one prototype and
one render script. **If you have the old two-page member render in Figma, delete those pages
before re-rendering**: the page names changed and re-rendering appends rather than replaces.

Each bundle is a folder of `.jsx` frames plus `render-*.ps1`, `link-*.js`, `validate.js`,
`DESIGN.md`, `pages.json`, `assets/`, and a `.zip` beside it in `figma/`.

### Three products, three structures

Deliberately distinct so a reviewer can tell them apart from three metres away.

| | Member | Doctor | Organisation |
|---|---|---|---|
| Ground | soft blue mesh | soft blue, white floating card | **warm graphite on off-white** |
| Navigation | 262px navy sidebar | 206px navy sidebar + light right rail | **88px icon rail + persistent context bar** |
| Context | none needed | the patient | **branch × department switcher, always visible** |
| Accent | teal | navy + coral | **amber** |
| Mobile chrome | light appbar, 5 tabs | gradient header card, 5 tabs | graphite header, **role-aware tabs** (admin / staff / front desk) |

### The mobile pattern: hub → section → sheet

Applied to the doctor and organisation modules. A phone screen is:

- **Hub** — header numbers, the one thing you act on now, a short list of ways in.
- **Section** — one subject on its own screen, opened from a hub row; `Btn Back` returns to the hub.
- **Sheet** — one decision over a dimmed hub. Anything with its own scroll is a section, not a sheet.

Generated, never hand-assembled: a screen declares its sections and sheets and the builder emits
the frames, the rows that open them, the way back and the motion class.

**The member module has NOT been converted to this pattern.** Measured against the exported
`.fig`, its mobile screens already fit one viewport (median 845px, max 895px), so the restructure
would add taps without removing scroll. The product owner asked for the full treatment anyway;
the machinery is in place (`addx()` in `tools/figma/build_member.py`) but no screen has been
converted. One caution for whoever does it: `preview_bundle.py` cannot measure this. Flex
children shrink in the preview, so every mobile frame reads back as exactly 844px whatever it
contains. The numbers above came from the exported `.fig`; use that, or a Figma render, as
ground truth.

---

## 4. How the design is produced

**Nothing is drawn by hand.** Python generates a JSX dialect; a CLI renders it into Figma.

```
tools/figma/*.py  ──►  figma/<bundle>/*.jsx  ──►  figma-ds-cli  ──►  Figma
                       + link-*.js (prototype)
                       + render-*.ps1
```

### The pipeline

| Step | Command | What it does |
|---|---|---|
| 1. Assets | `python3 tools/figma/org_assets.py` | Generates gradients, tints, donuts, illustrations into `assets/img` |
| 2. Build | `python3 tools/figma/build_org.py` | Writes every `.jsx`, `link-org.js`, `render-org.ps1`, `pages.json` |
| 3. Validate | `cd figma/medra-org && node validate.js` | Tokens exist, icons cached, images present, DSL rules obeyed |
| 4. Preview | `python3 tools/figma/preview_bundle.py figma/medra-org figma/medra-org/preview.html` | JSX → HTML for offline QA |
| 5. Measure | headless Chromium over the preview | Horizontal overflow and content height |
| 6. Audit | `python3 tools/figma/proto_check.py figma/medra-org link-org.js` | Reachability, broken hotspots, wiring coverage |
| 7. Render | terminal-Claude runs `render-org.ps1` in Figma Desktop | The only step not run in this repo |

### Files

| File | Purpose |
|---|---|
| `tools/figma/medra_ui.py` | Shared vocabulary: `T`, `I`, `card`, `field`, `cta`, `rows_of`, `statusbar` |
| `tools/figma/member_kit.py`, `member2_kit.py` | Member chrome + hub/sheet primitives |
| `tools/figma/build_member.py` | The **whole** member app — one builder for all 8 pages |
| `tools/figma/doctor_kit.py` | Doctor chrome: navy sidebar, right rail, clinical components |
| `tools/figma/org_kit.py` | Organisation console: icon rail, context bar, board, seats, `unverified()` |
| `tools/figma/build_*.py` | One per bundle. Screens, transition table, linker, render script |
| `tools/figma/normalise.py` | Fixes the two structural defects above in every frame at build time |
| `tools/figma/fixups.py` | Emits `fix-layout.js` — the same two fixes, applied **in place** to a canvas already rendered |
| `tools/figma/preview_bundle.py` | JSX → HTML approximate renderer |
| `tools/figma/proto_check.py` | Offline prototype audit |
| `tools/figma/figkiwi.py` | **Reads an exported `.fig`** so a designer's corrections can be read out rather than guessed |
| `tools/docx_build.js` | Markdown → styled `.docx` for the PRD |

### The JSX dialect — rules that bite

Elements: `<Frame> <Text> <Icon> <Rect> <Ellipse> <Image>`. One `.jsx` = one Figma frame.

1. **`wrap="wrap"` is NOT honoured.** Chunk rows with `rows_of(items, per_row, gap)`. This silently
   broke 75 frames once; `validate.js` rule 11 now fails the build on it.
2. **`items="stretch"` is rejected.**
3. **`grow` is a row property.** `grow={1}` on a column child stretches it vertically. Use
   `w="fill"` (i.e. `full=True` on button helpers) instead.
4. **Numeric props keep their braces:** `w={390}`, `rounded={12}`.
5. **Colours must be `#RRGGBB` or `var:token`.** `rgba()` renders as NaN.
6. **Every `<Text>` needs a font.** The helpers do this; hand-written text does not.
7. **`minH` frames grow, they do not clip.** Mobile frames use `minH={844}`.
8. **No shadow or effect support.** Depth comes from fills and borders.
9. **Icons must be in `assets/icon-cache/` as `lucide_<name_with_underscores>.svg`.** Fetch from
   `https://cdn.jsdelivr.net/npm/lucide-static@1.26.0/icons/<name>.svg`.
10. **Python f-strings:** no backslashes in expressions, `{{n}}` for literal braces. Hoist long
    strings to module level rather than nesting f-strings.
11. **An empty frame keeps Figma's 100×100 default on whatever axis you did not set.**
    `<Frame grow={1} />` is a spacer with no height, so it renders 100px tall and holds a 34px
    row open — 530 of them were in the file. `tools/figma/normalise.py` now fills the cross axis
    of every empty frame at build time. Do not write a spacer without a cross-axis size.
12. **`items="center"` centres the text node, not the text inside it.** A label ends up
    left-aligned in a visibly centred card. `normalise.py` adds `align="center"` to any text in
    a centred container; 4,115 nodes needed it.

### How the prototype is wired

Three passes in `link-*.js`:

1. **Explicit transitions** — a hand-written `(screen, hotspot, destination)` table. The table
   describes a *screen*; on mobile a screen is a hub plus its sections, so each entry attaches to
   whichever frame of that family actually carries the control, found by scanning generated frames
   at build time. A hotspot that exists nowhere in the family **fails the build**. A `~` prefix
   marks a control that is legitimately breakpoint-specific.
2. **Navigation sweep** — global hotspots (rail, tab bar, context bar) applied to every frame that
   carries them. Frames that do not are skipped; the audit reports this separately from breakage.
3. **Dead-hotspot sweep** — anything still named `Btn …` gets a 10 ms navigate-to-self, so no
   control feels broken in a click-through.

Every page declares **two flow starting points**, `· Desktop` and `· Mobile`.

---

## 5. Instructing the CLI (the terminal that renders into Figma)

A second Claude runs in a terminal with Figma Desktop connected. Each bundle ships a
`CLI-PROMPT.md` to paste. The pattern that matters:

```
You are rendering **the Medra <module> module only**. Do not create, edit, rename, re-render or
delete anything on any page that does not begin with `Medra <Module> —`. The other pages in this
file are finished and signed off — leave them alone.

Working directory: the unzipped bundle. Confirm you can see render-*.ps1, link-*.js, DESIGN.md,
pages.json, N .jsx files and an assets/ folder before you start.

Run, in this order:
1. New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
   Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
2. .\render-<module>.ps1

Report back with: the object link-*.js returns ({ linked, navLinked, stayOnScreen, framesFound,
missing }), and any frame that failed to render, by filename.

If `missing` is not empty, re-render just that file and re-run the linker. Do not attempt to fix
the .jsx yourself — the generator is the source of truth and the fix belongs upstream.
```

**Known behaviour: re-rendering appends, it does not replace.** The exported `.fig` showed 215
doctor mobile frames where the bundle has 169 — the old row was still there beside the new one.
Either delete the old frames first, or render to new pages.

---

## 6. What has been decided (and why)

Decisions that are expensive to reverse, with the reasoning, so nobody re-litigates them blind.

| Decision | Why |
|---|---|
| **Records are member-owned; the member is the connector** | An institution-owned record recreates the silo Medra exists to remove |
| **Nurses, lab techs and pharmacists are first-class roles** | A doctor consumes work others produce. Model only doctors and you either lose that data or turn the doctor into a typist — either kills the product |
| **Departments, not individuals, are the unit** | Seats stay when people leave; permissions never travel with a person; work routes to a queue rather than an absent individual |
| **Self-reported health data is marked unverified, everywhere** | A wrong blood group shown as fact to a surgical team is the worst failure this product can have, and the liability is Medra's |
| **Front desk cannot read clinical content** | Busiest, highest-turnover seat in the building. A window into diagnoses there is the fastest route to a breach |
| **A lab technician cannot release a result** | An out-of-range value on a phone with nobody to explain it is a harm, not a feature |
| **External access is a scoped single-use link, not an account** | Most Nigerian labs will not sign up to run one test, and a member should not carry paper because of that |
| **Lab results use structured templates** | Prose cannot be trended, flagged or compared between labs |
| **Payment before booking** | Cut no-shows from ~11% to ~7% in the pilot narrative |
| **Mandatory date of birth, plus NIN** | Large population, duplicate names and birthdays. Age is not an identifier and decays |
| **Access is per episode of care** | The only rule that makes a shared record safe to pass around a hospital |

---

## 7. Review history

| Date | Who | What changed |
|---|---|---|
| 10 Jul 2026 | Design brief | Original scope |
| 1 Aug 2026 | Godwin, Abraham, Israel | Payment before booking; MDCN login; Medra ID search; doctor picks what the member sees; drug search not free text; doctor sets the meeting link; transcription is Phase 2 |
| **9 Aug 2026** | **Godwin, Israel** | **The clinical chain; the organisation module; departments as the unit; RC + licence; unverified health data; single-use external links; structured results; NIN and mandatory DOB; NHIS and private insurance; data-privacy undertaking; "members" not "patients"** — recorded in PRD v2.0 §23 |
| Friday (planned) | Godwin, Israel | Review continues from the member dashboard onward |

---

## 8. What is left

### A. Retrofit to existing modules — **DONE (10 Aug)**

`health_fact()`, `verify_tag()` and `unverified_note()` live in `tools/figma/medra_ui.py` so
every module renders provenance identically. `org_kit.unverified` is an alias of the same thing.

| Change | Where it landed |
|---|---|
| **"Not medically verified"** | Member: H1 health card, H1 stat tile, R1 health summary, P0 profile tiles, P2 details, P4 dependant, R10 printed summary (asterisk + legend). Doctor: K4 read-the-file, P2 record (with an explicit "do not act on these as fact — order a group and screen" note), C1 side rail. Organisation: D2 nursing vitals |
| NIN | Auth M3 (member) and D1 (doctor); member P2 personal details |
| Date of birth mandatory | Auth M3 — the "Just my age" toggle is **removed**, not hidden |
| Data-privacy undertaking | Auth D1 (doctor) and I2 (institution): three clauses visible, a required checkbox, version-stamped |
| NHIS + private insurance | Auth M5, member P2 |
| RC **and** practice licence | Auth I1; regulator registration upload added to I2 |

Verified after: every bundle validates clean, zero horizontal overflow at 390 and 1440, and the
doctor and organisation prototypes still audit complete.

### A2. Merge the two member bundles — **DONE (10 Aug)**

One bundle, one builder, one prototype, one render script. The merge also made the member module
auditable end to end for the first time, and that first audit found real defects, all now fixed:

| Found | Fix |
|---|---|
| 21 screens unreachable — every empty state, all three system states, half the video chain, and the delete confirmation | The prototype now **opens on H2 First Visit**, a member who signed up a minute ago; their tab bar leads to the empty Visits, Records and Medicines, because that is what they have. `S1 → Near me → S3 No Results`. A switcher strip on X1–X3 reaches each other and W4 |
| **A member could not sign out on a phone.** `Sign out` was on desktop P0 only, `Sign out everywhere` on desktop P5 only | Both added to the mobile screens |
| Mobile P9 had no way to reach the deletion confirmation | "Continue to delete" added |
| Mobile W0 had no route into the phase-2 call preview | The phase-2 card added to the mobile screen |
| 124 transitions named a hotspot that did not exist — mostly one breakpoint's control claimed on both | Marked `~` (breakpoint-optional) where the difference is real and intended, fixed where it was not |

Result: **110/110 screens reachable, 0 broken hotspots, ALL 154 CLEAN**.

The system-state screens moved to their own page (`7 System States`), so the page numbering
changed — `6 Alerts`, `7 System States`, `8 Components`. **Delete the old member pages in Figma
before re-rendering**; re-rendering appends rather than replaces.

### B. Extend the doctor module — **DONE (10 Aug)**

Eight screens that close the loop between the three modules. Until this pass, an order stopped
at the doctor's screen and a share stopped at the doctor's intention; neither reached the
department that does the work or the member who has to agree.

| Screen | What it is |
|---|---|
| **C11 Send the order** | Where an order actually goes: your own laboratory, your imaging room, a Medra partner, a single-use link, or paper. Each option carries the deciding information — how busy they are, how long they take, what they cannot do |
| **C12 Order status** | Five steps, what the member sees while it runs, what to do if it stalls, and the doctor's other open orders sorted by what is closest to going wrong |
| **C13 Send to someone not on Medra** | Recipient, a seven-item scope with two lines locked on, how long the link lives |
| **C14 Waiting on consent** | Nothing exists until the member says yes. Four honest ways forward if she declines |
| **C15 The link is ready** | The token, how to send it, what the recipient sees, the doctor's open links, the member's audit trail |
| **P8 Structured result** | A result that arrived as data rather than as a photograph: the laboratory's values and ranges, the delta against the patient's own history, and full provenance — laboratory, scientist, analyser, verified when |
| **R11 Approve a share** (member) | Item by item, in the same words the doctor ticked, plus that saying no does not affect care |
| **R12 Shared outside Medra** (member) | Whether it has been opened, when it dies, revoke, narrow, and the append-only log |

Two chains now run end to end across modules: **C4 → C11 → C12 → P8** (an order reaching a
department and a result coming back), and **C13 → C14 → R11 → R12 → C15** (a share that does
not exist until the member agrees to it).

**A security defect was fixed in the same pass.** A single-use link's address was
`medra.ng/<the member's Medra ID>` — enumerable, so anyone holding one link could reach others
by counting. It is now `medra.ng/s/<random token>` in both the doctor and organisation modules.
This one is worth carrying into build as a requirement, not a detail.

### C. Member mobile hub → section conversion

Machinery is in place (`addx()` in `tools/figma/build_member.py`); 55 screens unconverted.
Evidence says it is not needed (see §3); the product owner asked for it anyway.

### D. Not started

Platform admin portal · imaging department · insurance eligibility checks · in-app video.

### D2. Repair the canvas that is already in Figma — **script ready, not yet run**

`figma/FIXUP.md` and a per-bundle `fix-layout.js`. Run it once per module; it is idempotent and
touches only that module's own pages. See §4 rules 11 and 12 for what it fixes and why.

### E. Render the organisation module into Figma

`figma/medra-org` is built, validated and audited but has never been rendered. It creates its
own eight `Medra Organisation —` pages and touches nothing else.

---

## 9. Open questions

These block design or build. Numbers 1–7 are from PRD v2.0 §23.2.

1. **Is a nurse a distinct role or a practitioner variant?** Assumed **distinct, with its own
   task-scoped app** — a nurse's screen is a work queue, a doctor's is a decision surface.
2. **Who creates staff accounts?** Assumed: the admin invites, the person proves their own
   identity and registration number. A clinical seat is never active on trust alone.
3. **The definitive document list per organisation type.** CAC certificate and practice licence
   are settled; a diagnostic lab and a pharmacy each have their own regulator's registration.
4. **Who can flip a health fact to verified?** Assumed: any doctor at the point of care, or a lab
   result that measures it directly.
5. **Insurance — storage only, or eligibility and claims?** Assumed **storage only** at MVP.
6. **Does the front desk take payment inside Medra, or record one taken elsewhere?** Assumed
   **record only** — the current design captures method and reference; Medra never touches the
   money at the counter.
7. **Subscription vs payment-before-booking.** §4 says practitioners pay a subscription and
   members pay providers directly; the 1 Aug review added payment before booking, which means
   Medra collects and pays out. Both are designed. **"Both" means two charges on one relationship
   and doctors will ask why.**
8. **Emergency "break-glass" access.** Assumed **yes, with loud audit** — a clinician can open a
   record without consent, must give a reason, and the member and admin are both told afterwards.
   Without it, staff share logins, which makes the audit log meaningless. `B3 Find a member` and
   `F2 Audit log` both show it; it has not been confirmed.

---

## 10. Conventions

- **Voice:** plain, specific, never cute. Copy explains consequence — "your fee is held until you
  sign", not "please sign". Reasons appear next to rules.
- **Nigerian specifics:** ₦, +234, MDCN, MLSCN, PCN, CAC/RC, NHIS, NDPA 2023, Paystack,
  WhatsApp-first messaging, Abuja place names (Garki, Maitama, Wuse, Kubwa, Asokoro).
- **Names in mock data are consistent across modules** — Amara Okeke `MDR-8842-19` is the same
  person in the member, doctor and organisation bundles, and her dependants Chidi and Grace share
  the `8842` family stem. Keep it that way; it is what makes a walkthrough legible.
- **Commits:** one per coherent change, describing the reasoning, not the file list.
- **Every design change is validated, measured and audited before it is committed.** No exceptions
  — the three checks are cheap and have caught real defects every single time.

---

## 11. Quick start for a new session

```bash
git checkout claude/new-project-prd-stories-ss2qlr
python3 tools/figma/build_org.py                     # regenerate a bundle
cd figma/medra-org && node validate.js               # must say ALL N CLEAN
cd ../.. && python3 tools/figma/proto_check.py figma/medra-org link-org.js   # must say COMPLETE
python3 tools/figma/preview_bundle.py figma/medra-org figma/medra-org/preview.html
```

`preview_bundle.py` is for *looking*, not for measuring. Its flex children shrink, so every
mobile frame measures back as exactly 844px whatever it holds — use a Figma render or an
exported `.fig` when you need a real height.

Read `docs/Medra_PRD_v2.0.md` first, then this file, then the `SETUP.md` of whichever bundle you
are touching. If a designer sends an exported `.fig`, `tools/figma/figkiwi.py` will read it.
