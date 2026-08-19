# Medra — project handoff

**Everything needed to pick this project up cold**, in one file: what Medra is, what has been
designed, how the design is produced, how to instruct the CLI that renders it into Figma, and
what is left. Kept current — it is updated in the same commit as the work it describes.

| | |
|---|---|
| **Document version** | **v1.5** |
| **Last updated** | 11 August 2026 (one desktop shell · one doctor account, two workplaces · critical-value alerting) |
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

Five rendered bundles, **839 frames**, all validated clean and fully offline.

| Bundle | Frames | Pages | Status |
|---|---:|---:|---|
| `figma/medra-ds` — design system + journeys | 27 | 1 | Done |
| `figma/medra-auth` — authentication, 4 roles + staff joining an organisation | 90 | 5 | Done · **v2.0 retrofit applied** · **prototype complete** |
| `figma/medra-member` — the whole member app | 158 | 8 | Done · **prototype complete** |
| `figma/medra-doctor` — full doctor module | 275 | 8 | Done · **prototype complete** |
| `figma/medra-org` — organisation: eight personas, each with its own navigation | 316 | 9 | Done · **prototype complete** · **not yet rendered into Figma** |

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
13. **A `<` in prose makes the file un-parseable.** "Normal < 5.7" and "<1h" are both real Medra
    copy. `T()` in `medra_ui.py` now escapes `<`, `>` and bare `&`, leaving existing entities
    alone. Four org frames and one doctor frame were silently unmeasurable before this — and one
    of them, `D7-lab-result-m`, turned out to overflow its phone by 77px the moment it could be
    measured, which is exactly the class of defect the escape hides.
14. **`{{n}}` only becomes `{n}` inside an f-string.** Concatenating a plain `'…gap={{12}}…'`
    onto an f-string emits the literal double braces. Three of them shipped. Grep the built
    bundle for `={{` after any change to a builder — validate.js does not catch it.
15. **Keep the icon cache in step with the JSX.** `render-*.ps1` copies `assets/icon-cache/*.svg`
    into figma-ds-cli's own cache before rendering, so an icon that is missing fails quietly
    part-way through a run. `python3 tools/figma/icons.py` scans every bundle for the
    `lucide:<name>` it actually uses and fetches whatever is absent. Run it after every build.

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
| **14 Aug 2026** | **Godwin, Abraham Peter, Israel** | **Doctor module only.** Consultation length set by the practice not the patient · block dates on a month calendar · a structured examination template · lab results renamed to include instrumental diagnostics · earnings against the previous period · the clinic-progress donut belongs to the admin, not the doctor · **and a reversal: Godwin wants the member to see the consultation note, private notes included, except in psychiatry and psychology** — recorded in `docs/Review_14Aug2026.md` |
| Next (planned) | Godwin, Abraham, Israel | **The organisation dashboards** — asked for directly |

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

### A4. Critical-value alerting — **DONE (11 Aug)**

The one item in the content audit that was a safety defect rather than a gap. A potassium of 7.2
kills people while a result sits in an inbox; every laboratory runs a critical list for exactly
this reason, and Medra had no path for it.

| Screen | What it does |
|---|---|
| **D15 Critical Value** (lab) | The value cannot be "sent". It has to reach a named human by voice, with a read-back recorded — who you spoke to, what they read back, at what time |
| **K10 Critical Result** (doctor) | Interrupts. Acknowledge with your name and the time, then say what you are doing — and both go on the record. "Handed to the on-call" is a real answer; ignoring it is not one the screen offers |
| **F7 Critical Results** (governance) | The escalation ladder — requester, on-call at 15 minutes, medical director at 30 — and a board of what is unacknowledged. It never times out |

**Result acknowledgement came with it.** Before this, "released" and "somebody read it" were the
same fact. K10's acknowledgement is what separates them, and F7 shows the difference between
acknowledged and acted on — a result that was heard and then forgotten is the failure that
reaches a coroner.

Entry points are on `K1` (the only thing allowed above a doctor's welcome), `P7`, `D5` and `D7`.

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

### B2. Every persona in the organisation gets a dashboard — **DONE (17 Aug)**

Godwin's request after the second review, and the subject of the next one: *"an admin view,
front desk/receptionist view, doctors view, nurses, lab technician, pharmacy including any
other department that is important in a medical organization… what do they each see?…
including how they communicate with each other."* Nursing, laboratory, pharmacy and the front
desk already had theirs. This pass added the three that were missing.

**Imaging / radiology — D16, D17, D18.** The third review asked for instrumental diagnostics
(ECG, echo, CT, MRI, gastroscopy) alongside blood and urine. They do not behave like blood: a
specimen leaves the patient, an image does not, so the person has to be present, prepared and
safe before anything happens, and the result is a radiologist's sentence rather than a number
against a range.

| Screen | What it is |
|---|---|
| **D16 Worklist** | Six studies ordered by appointment rather than by request time, because an image needs the person, the room and the machine at once. A rooms-and-machines panel, and a count of what has been acquired but not yet read |
| **D17 Safety check** | The only screen in Medra that refuses to move. Identity said aloud, metal, pregnancy, claustrophobia, and what the patient was told. Two unanswered here, so the start button is off. Dose and operator are recorded on every study, not only abnormal ones |
| **D18 Report a study** | The radiologist's screen: findings, impression, urgency, and a critical-finding switch that routes into the D15 pathway. Signed by a named person, amendable only by a second version that says so |

**Billing / cashier — D19, D20, D21.** The front desk takes money at check-in; running the
money is a different job. In a Nigerian clinic the leak is the claim that was submitted,
queried and never resubmitted.

| Screen | What it is |
|---|---|
| **D19 The money today** | Taken, outstanding, sitting with HMOs, unreconciled — and how it came in, because cash is the only line Medra cannot verify by itself. Closing the till needs two named people and cannot be turned off |
| **D20 Take a payment** | An itemised bill, part payment as a first-class case, method and reference, receipt to her phone. Append-only: a wrong amount is corrected by a second entry, never by editing the first |
| **D21 Insurance claims** | Fourteen claims with HMOs and NHIS by state, an ageing profile, and the four causes of a query — three of which are fixed at the front desk before the person is seen |

**The doctor inside a hospital — G1 to G4**, on a new `Clinic` page. One account, two
workplaces: Dr. Eze's MDCN number is his, so the hospital inviting him added a workplace to an
account that already existed. The consultation is identical to his private one; four things
differ and the screens say which.

| Screen | What it is |
|---|---|
| **G1 My day** | A list he did not build — the front desk booked it and the admin allocated it. Beside it, the four things this workplace owns and he does not: who fills his day, who sets the slot length, whose money it is, who supervises him |
| **G2 My roster** | The hospital's roster, not his availability. He cannot open or close a session; he asks, and a named person answers. Overbooking is visible as a fact somebody decided |
| **G3 Messages** | Godwin asked for this directly. A message goes to a **department** and whoever is on shift picks it up — sending it to a named person is how a question waits until Monday because that person went home |
| **G4 A conversation** | Attached to the visit, so the next doctor can see why the order of the day changed. Nothing clinical is decided here; an order, a result and a referral each keep their own screen and their own record |

### B3. The rail is expanded by default, and the admin has real reports — **DONE (17 Aug)**

Two things from the same sitting.

**The sidebar now opens labelled.** `expanded=True` is the default on `rail()` and `app_desk()`;
collapsed is still there and still carries the same hotspot names, so it is a state of one rail
rather than a second navigation. Making it the default cost 172px of main column and that
turned up three fits that had been passing only because the rail was 76px wide: `K1` and `K6`
in the doctor module both put a fixed inner column beside a context rail, and a hugging row
inside a shrinking column overflows rather than wraps. Fixed by capping the expanded rail at
208px, narrowing those two inner columns to 300, and giving `queue_row`'s name line `w="fill"`.
The persona pill lost its "Organisation · " prefix — at 208px "Organisation · Laboratory" was
two lines in a pill — and the rail's profile block puts the role on its own line for the same
reason.

**Reports became four screens instead of one.** The old `F4` was a bar chart and five ratios,
which is a summary rather than an answer. An administrator's questions are four:

| Screen | What it answers |
|---|---|
| **F4 Reports** | The overview: 1,412 seen, six months of volume, a day × hour grid of when the place is actually busy, and the way into the other three |
| **F8 Patients** | New against returning, where the visits came from, why people came, who they were by age, and who did not turn up — with the finding that a phone booking is three times more likely to be a no-show than one made in Medra |
| **F9 Clinicians** | The number Godwin asked for by name: **hours actually spent consulting**, per doctor, against hours rostered. Plus median consultation length, notes signed same day, criticals acknowledged, and where a clinical hour goes — 62 hours a month spent waiting for somebody to walk in |
| **F10 Departments** | Seven departments side by side, transactions per person, turnaround against each department's own target, and who is on shift right now |

**The charts are generated, not drawn** — `col_chart`, `rank_bars`, `heat_grid`, `part_bar`,
`data_table`, `hero_stat` in `org_kit.py`. Four rules hold across all of them and are written
at the top of that section:

1. **One blue ramp, light to dark.** Magnitude is the job on every chart here, so colour
   carries size and nothing else. Four steps, because that is where adjacent pairs still clear
   ΔE 15 for normal vision and 13 under protanopia.
2. **Green, amber and red never appear inside a chart.** They mean *state* everywhere else in
   this file, and a bar that is red because it is fourth is a bar somebody reads as a problem.
3. **Every mark carries its number.** The pale steps do not reach 3:1 against white; the label
   is what makes them readable, not decoration.
4. **A table once there are more than about seven things.** Seven departments is past the point
   where colour can carry identity, and the admin came for the number anyway.

There are no line charts: the renderer has no path primitive, so a month-by-month column chart
is the honest substitute. `rank_bars` sorts its own rows — on a ranked chart the order *is* the
message — and pins a residual "everything else" bucket to the bottom in the de-emphasis gray,
because it is often the largest number and never the story.

**Builders now prune their own folders.** A renamed section used to leave its `.jsx` behind;
the render script drew it, the linker never wired it, and the audit reported an unreachable
screen. Two of those were live in this bundle.

### B4. Staff onboarding — **DONE (17 Aug)**

The gap that stopped the organisation story running end to end: an admin could invite somebody
on `C5`, and nothing existed for the person who received it. Ten screens on a new `Staff` page
in the auth bundle, `S1`–`S10`.

Deliberately shorter than the doctor's own registration, and for a reason worth keeping: the
organisation has already been verified and is vouching for the person, so what Medra still has
to establish is only that the human holding the link is the human the admin invited, and that a
clinical seat is held by somebody on a register. That is Abraham's caution — *"even with new
features you have KYC for that feature… before you know it, it gets too complicated"* — and
Godwin's answer in the same breath: *"all they need to do now is set up an account, put and
verify information."*

| | Screen | What it does |
|---|---|---|
| | **S1 The invitation** | Who invited you, which department, which branch, when it expires — all of it typed by the admin on `C5`, which is exactly why it is shown back. Under it, what the seat lets you do and the two things it never will |
| 1 | **S2 Prove it is you** | One code. The screen says out loud that it went to the address *the admin typed*, and that if that address is not yours you should stop |
| 2 | **S3 Your details** | Name, NIN, date of birth, and your own phone rather than the department's — it is how you get back in when you no longer work there. "Your admin typed your name when she invited you. Correct anything she got wrong; from here it is your account, not hers" |
| 3 | **S4 Your registration** | MDCN / NMCN / MLSCN / PCN, the number, the licence. Front desk and billing choose None and the step is one tap. Until the register confirms it, the account can see the building and nothing clinical |
| 4 | **S5 The undertaking** | Five lines, no schedule of definitions: everything you open is logged, you may open a record only while that person is in your care, break-glass is reported the same day, and looking up a colleague or yourself is never allowed. Signed by name |
| 5 | **S6 Set a password** | With the line that matters in a shared clinic: a computer eight people use is one device, which is why you never leave yourself logged in on it |
| | **S7 Waiting for your seat** | Three steps, one still running, and an honest admission that there is nothing useful to do here until it finishes. No invented task |
| | **S8 You are in** | Seat active, seven samples waiting — and the point of the whole model: the registration now sits on the person's Medra account rather than on Garki's |
| | **S9 Add this workplace** | The second entrance. Somebody who already uses Medra logs in and confirms; nothing is re-verified, because the MDCN number was theirs the first time. What changes and what does not, in five lines |
| | **S10 Invitation expired** | Seven days, then the link dies — the same rule as the single-use links Medra sends to laboratories. Withdrawn and already-used land here too |

`S1` and `S9` are the two entrances, `S7` and `S10` the two places a person legitimately stops.
The flow is entered from a link in an email or WhatsApp, not from a screen in the console, so
nothing in the organisation module navigates into it.

**One thing to leave alone.** The auth bundle's headlines wrap — the plain half of a
`head_chip` breaks over two lines with the teal chip beside it. That is the house style of this
bundle and has been since the first render; it is not a layout defect and does not want fixing.

### B5. The content cut, and the two blocked clinical items — **DONE (17 Aug)**

**The cut.** Godwin's objection was *"there are too much of irrelevant information been added
to the screen while some major functions are been left out."* The rule applied is **one
explanation per screen**: a screen may say *why* once, and every other group on it either says
nothing or states a fact. A sentence that carries a rule — who may see this, what cannot be
undone, what is charged, what is logged — is the product speaking and stays; a sentence that
re-narrates the rows above it is what goes, and it was usually the longest one on the screen.

**Explanation across the four bundles fell from 70,770 characters to 59,123 — down 16%**, over
about 150 rewritten strings. `tools/figma/prose_budget.py` now measures it and every builder
reports it, so drift shows up on the next build rather than at the next review.

Two things the tool had to learn before its number meant anything:

- **What a person authors is content, not chrome.** A consultation note is supposed to be a
  paragraph. `note_field` and `note_section` bodies are excluded, or the tool would be telling
  a doctor their own note is too long.
- **A row subtitle is data, not prose.** The first version named `C11 Send the order` as one of
  the worst screens in the file — but its longest line is 99 characters and the other thirty-two
  are things like "Open now · 3 samples in the queue · median 4 hours". That is six destinations
  each carrying the fact you choose between them on: the opposite of the reported problem.
  Prose is now a line that is long enough to be a sentence **and punctuated like one**.

**Screens whose job is to explain get a wider budget** — consent, revocation, deletion, the
critical-value pathway, the MRI safety stop, the undertaking. A consent screen that does not say
what saying no costs you is not a shorter screen, it is a worse one. They are named individually
in `prose_budget.py` so "this screen is special" stays a decision somebody made.

**The two blocked items are now designed rather than blank**, from published convention, and
sourced in `docs/Clinical_Templates.md`. Neither should reach build without a clinician.

**The examination template** (`C1`) — nine measurements: the five conventional vital signs plus
height, weight and a **computed** BMI. Blood pressure is taken **twice**, because the WHO HEARTS
protocol defines hypertension on two readings — and HEARTS is what runs in 60 primary-care
centres in the FCT under the Hypertension Treatment in Nigeria programme, which is Medra's own
pilot geography. An unfilled field stays visibly unfilled: Godwin was describing a checklist
that prevents omission under time pressure, not a data-entry convenience. The template does not
score, warn or diagnose — it tints a value outside the reference range and stops.

**Private notes → withholding on stated grounds** (`C7`, `R2`). The blanket private note is
gone. The member sees the note by default; a clinician may withhold **one item** and must pick a
ground, and there are three: **serious harm** (explicitly not "she may find it upsetting"),
**somebody else's information** (a colleague is never a third party), and a **psychotherapy
note** (psychiatry and psychology only, kept apart from the record). The member is told *which
ground* — not the old "a private note exists", which tells somebody that something is being kept
from them and nothing else. This lands where Godwin did while keeping the two grounds a
clinician genuinely needs and that a transcript line would have removed.

### B6. Eight personas, eight navigations — **DONE (17 Aug)**

> **Godwin:** "these personas are different entities but they are just contained under the
> organisation module and of course they won't be seeing the same things… the items on each of
> their navigation bar has to be different."

He was right, and the module was wrong in one specific way: **every screen wore the
administrator's eight destinations.** A pharmacist logging in was offered Referrals, Access and
Reports — none of which they can open — and was not offered stock, which is half their job. A
navigation bar is the clearest statement a product makes about whose screen this is, and it was
making the same statement to eight different people.

There are now eight rails in `NAV_BY_PERSONA`. The admin's is the only long one, because the
admin is the only persona whose job is the whole building.

| Persona | Their rail |
|---|---|
| **Admin** | Today · Bookings · People · Departments · Referrals · Access · Reports · Settings |
| **Front desk** | The day · Bookings · Walk-in · Members · Payments · Messages |
| **Doctor** | My day · Patients · Results · Roster · Messages |
| **Nursing** | My queue · Record vitals · Standing orders · Members · Messages |
| **Laboratory** | Order queue · Enter result · Critical · Sample problems · Messages |
| **Pharmacy** | Prescriptions · Stock · Substitutions · Messages |
| **Imaging** | Worklist · Reporting · Rooms · Messages |
| **Billing** | The money · Owing · Claims · Messages |

Two rules hold across all of them, both enforced rather than trusted:

- **Every destination is a real screen.** `build_org.py` asserts every rail item resolves before
  the build finishes — a rail item that leads nowhere is worse than a missing one.
- **Hotspot names are unique per destination**, never per position: `Nav Lab Queue`, not a second
  `Nav Today`. The prototype's navigation sweep is global by name, so two personas sharing one
  would send a nurse to the pharmacist's screen.

**Twelve new screens**, because seven rails needed destinations the module did not have:
a **Messages screen for every department** rather than only the doctor's (H1–H6, each with its
own address book — you message a department and whoever is on shift picks it up); the doctor's
own **Patients** (H7) and **Results** (H8), which an administrator never sees; nursing's
**Standing orders** (H9); pharmacy's **Stock** (H10); and imaging's **Rooms** (H11), where a
machine out of service is visible as an organisation problem rather than a departmental one.

**The phone matches the desktop.** `TAB_STAFF` and `TAB_DESK` are gone — two hand-written bars
covering eight personas was the mobile half of the same mistake. `o_tabs_for()` generates the
tab bar from the persona's own rail: three destinations, then **Messages**, then More. On a
phone, being reachable by the rest of the building beats a second list you can open from More.

**The admin got what the admin is for.** Onboarding — invite someone, add a department, chase
the two people invited who never joined, see that the front desk has no spare seat — is now a
block on the administrator's own Today rather than two rows deep in People. It appears on
nobody else's screen, because only an administrator can create a seat.

### B7. The member mobile calm register — **DONE (17 Aug)**

> "Look at how subtle and calm the interface looks, the use of cards and icons to illustrate
> functions, and also the glass effects… not too much colours/gradients, just subtle, calm and
> minimal."

All fifty-seven member mobile screens are in the register. The work was done in the kit rather
than screen by screen, so it lands everywhere at once and stays consistent as screens change.

**The gap was not layout.** A contact sheet of all fifty-seven showed it plainly: nearly every
icon in the app sat in the same pale blue-grey square. That is what makes a list of rows read
as a list of rows rather than as a set of things you recognise.

| Change | Where | Effect |
|---|---|---|
| **The icon's meaning owns its colour** | `TONE_OF` + `soft_icon_box()` | A pill is always mint, a record always blue, money always sand, sharing always lilac — on every screen. Six soft tints, none of them a state colour, so green/amber/red still only mean good/warning/bad |
| **Strokeless cards** | `card()`, `group_card()` override `medra_ui` | On a pale ground a hairline border is what makes an interface feel busy before anything is on it |
| **A calmer primary** | `btn-calm.jpg`, `cta()` override | Deep ocean into navy instead of the bright teal gradient that was the most saturated object on every screen |
| **Function tiles** | `func_tile()`, `func_grid()` | Icon in a soft tinted square over a short label — the CliniQ pattern. On `H1`, `H2`, `P0` and all four empty states |
| **One chart, one colour** | `chart()` | The blood-pressure history painted bars amber and navy by value, which turns a trend into a verdict on a phone with nobody there to explain it. Now one quiet tone with the latest reading in the accent — emphasis, not a scale |
| **Red only where it belongs** | `R6 Who has access` | Three red *Revoke* buttons made a member exercising a right look like a destructive act. Red is now on "revoke everything" and nowhere else |
| **A quieter selected chip** | `S1`, `S2` | The filled navy pill was the heaviest object on a screen whose job is to narrow a list |

**The empty states earn their keep now.** `M5`, `R9`, `V3` and `N2` each end in a three-tile
grid of what you can do from here — the screen a member reaches by having nothing is the screen
most worth teaching on.

**Still not converted, and deliberately:** the hub → section machinery (`addx()` in
`build_member.py`) is unused. Measured against the exported `.fig`, the member's mobile screens
already fit one viewport, so splitting them adds taps without removing scroll. The doctor and
organisation modules use it because their screens genuinely overflow; the member's do not.

### D. Not started

Platform admin portal · insurance eligibility checks · in-app video · shift handover · duty
roster as an admin tool · what happens to work in flight when a staff member is removed ·
deceased/inactive record state.

### A3. The auth prototype — **DONE (11 Aug)**

It had never been audited. 35 of its 70 screens — every mobile frame — were unreachable, because
the page declared **one** flow starting point and it was the desktop frame. Fixed to the dual
`· Desktop` / `· Mobile` convention the other three use. Also fixed in the same pass:

- **Eight transitions named a hotspot that did not exist.** Three were breakpoint-asymmetric and
  are now marked `~` (the phone's hero draws a bare `Btn Skip`, the desktop names its own;
  correcting an MDCN number is a desktop job). One was stale — M3 lost its skip button when the
  v2.0 review made the legal name mandatory, and the transition stayed. One was a name mismatch,
  `Btn Login method Phone number` against an actual `Btn Login method Phone`.
- **No dead-hotspot sweep.** 193 controls — language pickers, blood-group chips, consent boxes —
  had no reaction at all and did nothing when clicked. Auth now sweeps like the other three.
- **`render-auth.ps1` emitted curly quotes** (`const t=’…’`) inside a JavaScript string. That is
  a syntax error, so every page-creation line in the auth render script silently failed.

**70/70 reachable, 0 broken hotspots.**

### D0b. One command to render the lot — **(17 Aug)**

`figma/render-all.ps1`. Selects the page, **deletes the frames it is about to replace**, renders
all four modules in dependency order, runs the four linkers.

The four per-module scripts each work, but none of them deletes and re-rendering **appends**.
That is the one way an 870-frame render goes wrong: it stops half way, somebody re-runs it, and
now there are two of everything with no way to tell which is which. `-Only org` re-does a single
module after a failure, deleting only that module's frames.

**The delete is scoped by frame name, not by page** — `Member · `, `Doctor · `, `Org · `,
`Auth · ` and `cmp/`. Nothing else on the page is touched.

**Rendering cannot be driven from a Claude session.** `figma-cli` is a local CLI that talks to
Figma Desktop over a plugin bridge; there is no Figma Desktop in a container, and the Figma MCP
server writes through the *Plugin API* rather than through this project's JSX dialect — porting
870 frames and every image asset through it would mean rewriting a renderer that already works.
Rendering is a thing somebody runs on the machine that has the file open.

### D0. Render it — **the blocker, now cleared (11 Aug)**

Nothing built since the shell conversion has ever been through figma-ds-cli, and it could not
be: the render scripts created eight pages per module and the plan on this file allows three.

Every module now renders onto **one page**, `ONE_PAGE` in `tools/figma/shell.py`, with a per
module y-offset (`BAND_Y0`) so four linkers running independently do not lay their frames on
top of each other. `figma/RENDER.md` has the order and the delete-first warning.

**The canvas in Figma is stale.** Every desktop screen changed when the three shells became one.
Re-rendering appends, so the old frames have to go first or there will be two of everything.

### D2. Repair the canvas that is already in Figma — **script ready, not yet run**

`figma/FIXUP.md` and a per-bundle `fix-layout.js`. Run it once per module; it is idempotent.
See §4 rules 11 and 12 for what it fixes and why.

**It is scoped by frame name, not by page.** The Figma plan on this project caps the file at
three pages, so modules share pages rather than sitting on the ones `render-*.ps1` names. Any
script in this repo that filters by page name will find nothing here — scope by frame name
instead, and report `framesRepaired` against `framesExpected` so an empty result cannot be
mistaken for a clean one.

### E. Render the organisation module into Figma

`figma/medra-org` is built, validated, audited and prototype-complete — 262 frames, 243 screens,
all reachable — but it has never been rendered. It lays out in the `120,000` band on the one
shared page; see `figma/RENDER.md` for the order and the delete-first warning.

---

## 9. Open questions

These block design or build. Numbers 1–7 are from PRD v2.0 §23.2; 8 and 9 are from the 14 August review.

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
8. **Do private notes stay private?** The design says never patient-visible; the 14 Aug review
   asked for the opposite — the member sees everything except in psychiatry and psychology. This
   is clinical governance, not a design preference, and it needs a doctor. **Do not apply it from
   the transcript.** See `docs/Review_14Aug2026.md` §1.1.
9. **Is there a place for advice that is not a drug?** Diet, exercise, salt, when to come back,
   what to watch for — most of what a hypertension review produces. Nothing in the file holds it.
10. **Emergency "break-glass" access.** Assumed **yes, with loud audit** — a clinician can open a
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
