# Medra Member — the prototype

Everything is wired by `link-member.js`. Nothing needs to be connected by hand in Figma.

**502 explicit transitions · 770 navigation links · 746 controls that stay on their own
screen · 110 of 110 screens reachable · 0 broken hotspots.**

Verify it before rendering, and again after:

```bash
python3 tools/figma/proto_check.py figma/medra-member link-member.js
```

---

## 1. How the wiring works

Three passes, in this order.

**1 — Explicit transitions.** A hand-written table of `(screen, hotspot, destination)`. The
table describes a **screen**, and a screen is two frames — desktop and mobile — so each entry is
attached to whichever frames actually carry the control, found by scanning the generated frames
at build time rather than guessed. A transition naming a hotspot that exists on neither is a
**build error**, not a silent skip; `proto_check.py` fails on it.

A hotspot prefixed `~` in the table is **breakpoint-optional**. That is not a way to silence the
check — it is a statement that the two breakpoints legitimately differ, and there are three
recurring reasons: a desktop dashboard has no `Btn Back` because it has a sidebar; a phone
booking screen has no tab bar because you are mid-flow; and a list shows as many rows as it has
room for, so the fourth doctor card exists on a 1440 panel and not on a 390 one.

**2 — Navigation sweep.** Seven global hotspots — the six sidebar items plus notifications —
applied to every frame that carries them. A frame that does not carry one (a phone tab bar has
five of the six destinations) is simply skipped. This is why the audit reports "NAV NOT PRESENT"
separately from "BROKEN LINKS": the first is expected, the second is a defect.

**3 — Dead-hotspot sweep.** Anything still named `Btn …` and not yet wired gets a 10 ms
navigate-to-self. Toggles, radios, filter chips and segmented controls behave like state in the
build; in a click-through they must at least respond rather than feel broken.

## 2. Flow starting points

Each of the seven screen pages declares **two** — `… · Desktop` and `… · Mobile`. With one, the
mobile row is not a prototype at all; you have to hand-pick a frame every time you present it.

| Page | Desktop start | Mobile start |
|---|---|---|
| 1 Find & Book | H2 First Visit | H2 First Visit · Mobile |
| 2 Visits & Virtual Care | V1 Upcoming | V1 Upcoming · Mobile |
| 3 Records | R1 Timeline | R1 Timeline · Mobile |
| 4 Medicines | M1 My Medicines | M1 My Medicines · Mobile |
| 5 Profile & Settings | P0 Profile | P0 Profile · Mobile |
| 6 Alerts | N1 Notifications | N1 Notifications · Mobile |
| 7 System States | X1 Loading | X1 Loading · Mobile |

The canvas is arranged to match: the desktop row on top, the mobile row directly beneath, both
in flow order.

## 3. The flows worth clicking

### The spine — signing up to a booked visit
`H2 First Visit` → **Find a doctor** → `S1 Results` → a doctor card → `P1 Profile` →
**Book** → `B1 Choose a Time` → **Review** → `B3` → **Pay** → `B4 Payment` →
**Confirm** → `C1 Confirmed` → **View my visits** → `H1 Home`, now with a visit on it.

This is the loop the whole app exists for. The doctor's avatar, name and fee keep the same layer
names the whole way, so Smart Animate tweens them across every step.

### The new member's app
The prototype opens on `H2`, and from there the tab bar leads to `V3 No Visits`,
`R9 No Records` and `M5 No Medicines` — because that is what a member who signed up a minute ago
has. Each of those has a "Find a doctor" that crosses into the populated app. It is the only
honest way to reach the first-run screens, and it is the state every real member starts in.

### Booking going wrong
`B1` → the 10:00 slot → `B2 Slot Taken` → **Book the alternative** → `B3`, or **Another day**
→ `B1`. `S1` → **Near me** → `S3 No Results`: filtering to nothing is a real outcome, and `S3`
offers to widen the search or notify you when a slot opens.

### A visit, end to end
`V1 Upcoming` → **Join** → `W0 Join by Link` → **Join the visit** → `W3 Visit Summary` →
**Open the note** → `R2`. `W0` → **Coming later: video inside Medra** → `W1 Pre-call Check` →
**Join** → `W2 In Call` → **End** → `W3`.
`V1` → **Reschedule** → `V5` · **Cancel** → `V6` → `V7 Cancelled`.

### Records and consent
`R1 Timeline` → any record → `R2` / `R3` / `R4`. `R2` → **Share** → `R5 Share Records` →
`R6 Who Has Access`, where a share can be revoked and the append-only view log lists who opened
what. `R1` → **Add a record** → `R7` → `R8 Record Added`.

### Medicines
`M1` → a medicine → `M2` → **Where this came from** → `R2`. `M1` → **Request a refill** → `M3`.

### Profile
`P0` → any settings screen → `Btn Back` → `P0`. `P0` → **Delete my account** → `P9` →
**Continue to delete** → `P9b Confirm Deletion`. `P0` → **Sign out** and `P5` → **Sign out
everywhere** leave for the auth bundle.

### States
`X1` ⇄ `X2` ⇄ `X3` ⇄ `W4`, via a switcher strip labelled **"state — for review, not a real
control"**, because these screens are reached by condition and not by tapping. `X2 Offline` →
**Retry** → `R1` and `X3 Error` → **Try again** → `H1`. `W4 Connection Lost` → **Retry** →
`W2`, → **End** → `V1`.

## 4. Motion

`MOTION.md` has the full table. In summary: 280 ms Smart Animate by default; 260 ms Move In from
the left for pushing into a detail; 220 ms Move Out to the right for every `Btn Back`; 320 ms
Move In from the bottom for sheets; 10 ms for controls that only change state.

## 5. What leaves this bundle

Six links point at the authentication bundle — **Sign out** from `P0`, **Sign out everywhere**
from `P5`, and **Confirm delete** from `P9b`, at both breakpoints — targeting
`Auth · Member — M6 Log In`. If that page is in the file they resolve; if not, the linker
reports them in `missing` and skips them. Nothing else crosses a module boundary.

## 6. What is deliberately not wired

- **Toggles, radios and filter chips** stay on their own screen. Drawing a second frame for
  every switch would triple the file and teach a reviewer nothing.
- **`Consent Scope / Locked`** is inert by design. Allergies and current medicines cannot be
  unshared; a control that looks tappable and then silently refuses is worse than one that
  reads as locked.
- **Destructive confirmations** beyond `P9 → P9b` are single-step here. The build needs more
  steps; the design file does not need a frame for each.
