# Medra Doctor — the prototype

Everything is wired by `link-doctor.js`. Nothing needs to be connected by hand in Figma.

**906 explicit transitions · 2,795 navigation links · 1,444 controls that stay on their own
screen · 215 of 215 screens reachable · 0 broken hotspots.**

Verify it before rendering, and again after:

```bash
python3 tools/figma/proto_check.py figma/medra-doctor link-doctor.js
```

---

## 1. How the wiring works

Three passes, in this order.

**1 — Explicit transitions.** A hand-written table of `(screen, hotspot, destination)`. The
table describes a **screen**, and on mobile a screen is a hub plus its sections and sheets, so
each entry is attached to whichever frame of that family actually carries the control — found by
scanning the generated frames at build time, not guessed. A transition naming a hotspot that
exists nowhere in the family is a **build error**, not a silent skip; `proto_check.py` fails on
it. A hotspot prefixed `~` in the table is breakpoint-optional: mobile carries a per-row action
that the capped desktop list does not, and its absence there is expected rather than broken.

**1b — Hub ⇄ section ⇄ sheet.** These are generated, never hand-written. Declaring a section on
a screen emits the section frame, the row that opens it (`Btn Sec <screen> <key>`, push), and its
`Btn Back` (pop). Declaring a sheet emits the sheet frame, the row that opens it
(`Btn Sheet <screen> <key>`, slide up from the bottom), and two ways out — the X and tapping the
scrim.

**2 — Navigation sweep.** Twelve global hotspots — the eight sidebar items, notifications,
patient search, start-consult and help — applied to every frame that carries them. A frame that
does not carry one (a phone tab bar has five of the eight destinations) is simply skipped. This
is why the audit reports "NAV NOT PRESENT" separately from "BROKEN LINKS": the first is
expected, the second is a defect.

**3 — Dead-hotspot sweep.** Anything still named `Btn …` and not yet wired gets a 10 ms
navigate-to-self. Toggles, radios, filter chips and segmented controls behave like state in the
build; in a click-through they must at least respond rather than feel broken.

## 2. Flow starting points

Each of the seven screen pages declares **two** — `… · Desktop` and `… · Mobile`. With one, the
mobile row is not a prototype at all; you have to hand-pick a frame every time you present it.

| Page | Desktop start | Mobile start |
|---|---|---|
| 1 Getting Started | G1 Setup Checklist | G1 · Mobile |
| 2 Today & Schedule | K1 Queue | K1 · Mobile |
| 3 Consultation | C1 In Progress | C1 · Mobile |
| 4 Patients | P1 Find a Patient | P1 · Mobile |
| 5 Practice & Money | S1 Public Profile | S1 · Mobile |
| 6 Growth | R1 Insights | R1 · Mobile |
| 7 States & Edge Cases | X1 Subscription Locked | X1 · Mobile |

The canvas is arranged to match: the desktop row on top, the mobile row directly beneath, both
in flow order.

## 3. The flows worth clicking

### The spine — a patient from queue to signed note
`K1 Queue` → **Read the file** → `K4` → **Start consultation** → `C1 In Progress` →
**Prescription** → `C3` → **Tests** → `C4` → **Finish and review** → `C7 Review & Sign` →
**Sign and send** → `C8 Signed` → **Start the next consultation** → `C1`.

This is the loop the whole app exists for. The patient's avatar, name and Medra ID keep the same
layer names the whole way, so Smart Animate tweens them across every step.

### Booking requests
`K1` → **Requests** → `K2` → **Accept** → back to `K1`. Decline stays on `K2` (a confirmation in
the build); **Another time** goes to `K6 Week`.

### The day going wrong
`K1` → **I am running late** → `K3` → **Send** → `K1`.
`K1` → the no-show row → `K5 Appointment Outcome` → **Mark as did not arrive** → `K1`.
`K6 Week` → **Block time off** → `K8` → **Offer everyone my next open slot** → `K6`.

### A result, from arrival to release
`K1` → **3 results to release** → `P7 Results` → **Release** → `C5 Result` → **Save to her
record** → `C7`. `Hold` stays on `P7`, which is the point: holding is a decision, not a dead end.

### Consent
`K4 Read the file` → **Ask for more history** → `P3` → **Send the request** → `P2 Record`.
`P2` shows what she shared; what she has not is listed as explicitly locked and is inert.

### Virtual
`K4` → **Send the meeting link** → `C10 Virtual Visit` → **Join the call** → `C1`.
`C10` → **Refund this visit** → `K5`.

### Money and the trial
Sidebar **Money** → `S5 Earnings` → **Subscription and billing** → `S6`. The trial card in the
sidebar footer goes to `S6` from every desktop screen. `X1 Subscription Locked` → **Add a card**
→ `S6`.

### Growth (AARRR)
`R1 Insights` → **Fix my hours** → `K7 Availability`; → **My booking link** → `R3`;
→ **Invite a colleague** → `G3`. `S1` → **Ratings** → `R2` → **My public profile** → `S1`.

### Mobile: the hub pattern
Every mobile screen opens as a hub. Tap a row and you get that subject on its own screen with a
back arrow; tap a sheet row and it slides up over a dimmed hub. Worth clicking:
`K1 Queue` → **Waiting** → back → **Quick actions** (sheet) → **I am running late** → `K3`.
`C1 In Progress` → **The consultation note** → back → **Add to this visit** (sheet) →
**Prescription** → `C3`. `S1 Public Profile` → **Practice settings** → any settings screen.

### Mobile-only: the More tab
The fifth tab is `K9 Everything`, not Settings. It is the only mobile route to Schedule,
Consults, Money and Growth, and it also reaches results, refills, unsigned notes, verification,
billing, every settings page, help and sign out. On desktop the app-grid button in the top bar
opens the same screen.

### States
The six States screens carry a switcher strip so the page can be clicked through: `X1` ⇄ `X2` ⇄
`X3` ⇄ `X4` ⇄ `X5` ⇄ `X6`. It is labelled **"state — for review, not a real control"** because
it is a review affordance, not product. `X4 Offline` → **Retry** and `X5 Error` → **Try again**
both land on `K1`.

## 4. Motion

`MOTION.md` has the full table. In summary: 260 ms Smart Animate by default; 240 ms Move In from
the left for pushing into a detail; 200 ms Move Out to the right for every `Btn Back`; 300 ms
Move In from the bottom for anything attached to a visit (prescribe, tests, upload, refer,
templates, running late, outcome); 10 ms for controls that only change state.

## 5. What leaves this bundle

Eight links point at the authentication bundle — **Sign out** from `S1`, and **Sign out
everywhere** / **Close account** from `S8`, at both breakpoints — targeting
`Auth · Doctor — D6 Log In`. If that page is in the file they resolve; if not, the linker
reports them in `missing` and skips them. Nothing else crosses a module boundary.

## 6. What is deliberately not wired

- **Toggles, radios and filter chips** stay on their own screen. Drawing a second frame for every
  switch would triple the file and teach a reviewer nothing.
- **`Drug Result / Blocked`** and **`Scope Line / Locked`** are inert by design. A control that
  looks tappable and then silently refuses is worse than one that reads as blocked — in a
  prescribing screen that is a safety property, not a style choice.
- **Destructive confirmations** (discard a draft, close an account) are single-step here. The
  build needs a confirmation step; the design file does not need a frame for it.
