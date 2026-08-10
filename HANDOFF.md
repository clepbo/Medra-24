# Medra — project handoff

**Everything needed to pick this project up cold**, in one file: what Medra is, what has been
designed, how the design is produced, how to instruct the CLI that renders it into Figma, and
what is left. Kept current — it is updated in the same commit as the work it describes.

| | |
|---|---|
| **Document version** | **v1.0** |
| **Last updated** | 10 August 2026 |
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

Six rendered bundles, **707 frames**, all validated clean and fully offline.

| Bundle | Frames | Pages | Status |
|---|---:|---:|---|
| `figma/medra-ds` — design system + journeys | 27 | 1 | Done |
| `figma/medra-auth` — authentication, 4 roles | 70 | 4 | Done · needs v2.0 retrofit |
| `figma/medra-member` — batch 1, find & book | 46 | 2 | Done · needs v2.0 retrofit |
| `figma/medra-member-2` — visits, records, medicines, profile | 108 | 6 | Done · needs v2.0 retrofit |
| `figma/medra-doctor` — full doctor module | 239 | 8 | Done |
| `figma/medra-org` — organisation + clinical chain + external | 217 | 8 | **New — not yet rendered into Figma** |

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
the machinery is in place (`addx()` in both member builders) but no screen has been converted.

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
| `tools/figma/doctor_kit.py` | Doctor chrome: navy sidebar, right rail, clinical components |
| `tools/figma/org_kit.py` | Organisation console: icon rail, context bar, board, seats, `unverified()` |
| `tools/figma/build_*.py` | One per bundle. Screens, transition table, linker, render script |
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

### A. Retrofit to existing modules (small, mechanical, safety-critical)

| Change | Where | Size |
|---|---|---|
| **"Not medically verified" state** | Member home/records/profile; doctor's patient file and consultation | ~18 frames + one component, two variants |
| NIN field | Auth: doctor and member sign-up | 4 frames |
| Date of birth mandatory | Auth: member details | 2 frames |
| Data-privacy undertaking step | Auth: doctor and organisation onboarding | 4 frames |
| NHIS + private insurance | Member profile and personal details | 4 frames |

**Do this first.** It is small, it touches screens that already exist, and every day the design
shows unverified data as fact is a day that assumption spreads into build.

### B. Extend the doctor module

Raise an order to a department (2) · generate a scoped external link + consent (3) · the doctor's
view of a structured result (1) · member-side consent to an external share (2).

### C. Member mobile hub → section conversion

Machinery is in place; 55 screens unconverted. Evidence says it is not needed (see §3); the
product owner asked for it anyway.

### D. Not started

Platform admin portal · imaging department · insurance eligibility checks · in-app video.

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

Read `docs/Medra_PRD_v2.0.md` first, then this file, then the `SETUP.md` of whichever bundle you
are touching. If a designer sends an exported `.fig`, `tools/figma/figkiwi.py` will read it.
