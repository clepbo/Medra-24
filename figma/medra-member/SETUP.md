# Medra — the Member app

**154 frames · 8 Figma pages · Desktop 1440×900 + Mobile 390×844 · "Soft Clinical"**

55 screens, drawn at both breakpoints, plus 44 interactive component states. This was two
bundles — `medra-member` (Find & Book) and `medra-member-2` (everything the bottom nav leads
to) — because batch 1 was already rendered and signed off when batch 2 started. That reason
expired; the split cost real things (batch 2 read batch-1's frame names off disk to build its
own tab bar, and a member-app change meant deciding which of two files owned it), so there is
now **one bundle, one builder, one prototype, one render script**.

| Figma page | Screens | Frames |
|---|---|---|
| `Medra Member — 1 Find & Book` | H1, H2, S1–S3, P1, B1–B4, C1 (11) | 22 |
| `Medra Member — 2 Visits & Virtual Care` | V1–V7, W0–W4 (12) | 24 |
| `Medra Member — 3 Records` | R1–R10 (10) | 20 |
| `Medra Member — 4 Medicines` | M1–M5 (5) | 10 |
| `Medra Member — 5 Profile & Settings` | P0, P2–P9, P3b, P9b (11) | 22 |
| `Medra Member — 6 Alerts` | N0–N2 (3) | 6 |
| `Medra Member — 7 System States` | X1–X3 (3) | 6 |
| `Medra Member — 8 Components` | 14 component sets | 44 |

Offline validation: **ALL 154 CLEAN, FULLY OFFLINE ✓** (`node validate.js`)
Prototype audit: **PROTOTYPE COMPLETE ✓ — 110/110 screens reachable, 0 broken hotspots**
(`python3 tools/figma/proto_check.py figma/medra-member link-member.js`)

## Build and render

```bash
python3 tools/figma/build_member.py        # rewrites every .jsx, the linker and the render script
```

```powershell
# Figma Desktop open + connected
.\render-member.ps1
```

The script primes the icon cache, imports the tokens, creates the eight pages, renders every
frame, then runs:

1. `components-member.js` — turns the `cmp/*` frames into **interactive component sets**
   (it removes only the sets it is about to rebuild, so nothing else on the page is touched)
2. `link-member.js` — wires the **prototype with motion**, closes the nav, arranges the canvas

`link-member.js` returns `{ linked, navLinked, stayOnScreen, framesFound, missing }`. A
non-empty `missing` means that frame is a stale render — re-render just that `.jsx` and re-run.

> **Re-rendering appends, it does not replace.** If a page already holds a previous render,
> delete its frames first or you get two of everything.

## Where the prototype starts

Every page declares **two** flow starting points, `… · Desktop` and `… · Mobile`. With one, the
mobile row is not a prototype at all — you have to hand-pick a frame each time you present it.

Page 1 starts on **H2 First Visit**, not on the populated home. That is deliberate: H2 is a
member who signed up a minute ago, and it is the only entry point from which the first-run
screens are reachable at all. Their tab bar leads to the *empty* Visits, Records and Medicines,
because that is what they have; "Find a doctor" from any of those crosses into the populated
app, and the booking flow ends on a home with a visit on it. It is the same arc a real member
walks in their first week.

## Layout rules that matter for Figma

- **No `wrap="wrap"`.** figma-ds-cli ignores auto-layout wrapping, so wrapped rows ran
  off-canvas. Every multi-item row is chunked explicitly with `rows_of()`.
- **No `items="stretch"`.** The CLI rejects it. Two places that wanted it were designed
  differently instead: the records timeline uses a date gutter + connector stubs rather than a
  stretched rail, and the video call places its self-view with `justify`/`align`.
- **`grow` is a row property.** `grow={1}` on a child of a *column* stretches it vertically.
  Inside a column use `w="fill"` (`mini_btn(..., full=True)`).
- **Mobile frames are `minH={844}`, not fixed.** They grow rather than clip, so a screen that
  runs long scrolls — it does not lose content. Screens are still designed to the 844 budget
  (S1 shows two result cards instead of three, H2 drops its second doctor block).

  A caution for whoever picks this up: `tools/figma/preview_bundle.py` measures the *frame*,
  and because flex children shrink in the preview every mobile frame measures exactly 844.
  It cannot tell you whether a screen overflows. Treat a Figma render as the ground truth for
  density, not the preview.

## Screens

### Find & book
| # | Screen | Notes |
|---|---|---|
| H1 | **Home** (returning) | Next-visit card, search, specialties, available-today |
| H2 | **Home** (new member) | The flow start. Empty state — "No visits booked yet" |
| S1 | **Search results** | Filter chips (2-up mobile / 4-up desktop), sort, 24 verified doctors |
| S2 | **Filters** | Bottom sheet on mobile. Opens with **an address to search around**, so you can look for care near your house while you are at work |
| S3 | **No results** | Reached by filtering to nothing. Widen search + "notify me when a slot opens" |
| P1 | **Doctor profile** | Stats, about, languages, fee, availability |
| B1 | **Choose a time** | Date strip, slot grid (taken slots disabled), in-person vs virtual |
| B2 | **Slot just taken** | Concurrency edge case → nearest open times |
| B3 | **Review & confirm** | Full summary, reason for visit, the "anything not in your records?" question, data-sharing note, reminder channels including WhatsApp |
| B4 | **Payment** | Payment happens *before* the booking is confirmed. Card, transfer, USSD or wallet, held by Paystack, refunded in full if the doctor cancels |
| C1 | **Booking confirmed** | Reference number, receipt, WhatsApp + SMS note, add to calendar |

### Visits & virtual care
| # | Screen | Notes |
|---|---|---|
| V1 | **Upcoming visits** | Tabs, next visit with Join/Reschedule/Cancel, a visit booked for a dependant, "get ready" checklist, directions |
| V2 | **Past visits** | Completed with "View summary" + "Book again"; a cancelled one with its reason; year filters; spend to date |
| V3 | **No visits** | Empty state + what you get on every Medra visit |
| V4 | **Visit detail** | Status, fee, reason, reminders, how to join, share-records nudge |
| V5 | **Reschedule** | Current slot shown as "will be released", the ₦2,000 late-change rule stated up front |
| V6 | **Cancel visit** | Reason (used only to improve Medra, never shown to the doctor), what happens, destructive confirm vs "Keep my visit" |
| V7 | **Cancelled** | Confirmation, SMS sent, nothing charged, rebook suggestion |
| W0 | **Join by link** | The MVP video path: the doctor's own Meet/Zoom link embedded in the Join button, with phone and WhatsApp fallbacks |
| W1 | **Pre-call check** | Self-view, camera/mic/connection checks, low-data mode, "call me on the phone instead" |
| W2 | **In call** | Doctor feed, self-view PiP, encrypted + timer plate, live captions; desktop adds a rail showing exactly what the doctor can see right now |
| W3 | **Visit summary** | Duration, what the doctor recorded, links into the note/prescription/tests/follow-up, anonymous rating |
| W4 | **Connection lost** | Attempt counter, "your visit is saved", switch to audio, ask the clinic to ring you |

W1, W2 and W4 are in-app video — badged **PHASE 2**. W0 is what ships.

### Records — the part that makes Medra more than a booking site
| # | Screen | Notes |
|---|---|---|
| R1 | **Timeline** | Month groups with a date gutter, six record types, who-has-access banner, health summary |
| R2 | **Consultation note** | Why you came / examination / assessment / plan, and a **signature block: MDCN number, timestamp, "cannot be edited"** |
| R3 | **Lab result** | Values with reference ranges and flags, the original scan, the accredited lab, a plain-language explainer |
| R4 | **Vitals trend** | Six-month chart. Self-measured readings are **labelled as such** so no clinician mistakes them for clinic results |
| R5 | **Share records** | Who · what (six scopes; allergies and medicines locked on) · how long · NDPA 2023 consent statement |
| R6 | **Who has access** | Active shares with expiry and instant revoke, and an **append-only view log** |
| R7 | **Add a record** | Camera or file, type, date, clinic, note; auto-read fields you can correct |
| R8 | **Record added** | What we read from the photo, every field editable, labelled "added by you" |
| R9 | **No records** | Three ways the history fills up |
| R10 | **One-page summary** | Blood group and allergies always on, everything else opt-in, live preview, QR code |

### Medicines
| # | Screen | Notes |
|---|---|---|
| M1 | **My medicines** | Today's doses with mark-taken, adherence dots, refill nudge, allergy warning |
| M2 | **Medicine detail** | How to take it, when to call a doctor, where it came from, 14-day adherence |
| M3 | **Request a refill** | Which medicine, days needed, pharmacy choice, and that approval is **not** automatic |
| M4 | **Reminders** | Per-medicine times, push/SMS/voice, quiet hours with an urgent override |
| M5 | **No medicines** | Why adding them yourself is still worth it |

### Profile & settings
| # | Screen | Notes |
|---|---|---|
| P0 | **Profile** | Health snapshot, Medra ID + QR for reception. Mobile uses a two-up tile hub so all six destinations fit one screen |
| P2 | **Personal details** | Name must match your ID for check-in; verified phone; NIN, never shown to a doctor; emergency contact |
| P3 | **Dependants** | A child and an older parent, with "book for" and "manage" |
| P3b | **Family plan** | Two dependants free, then ₦3,000/month for up to six people |
| P4 | **Add a dependant** | Relationship, guardian consent, and the handover at 18 |
| P5 | **Devices & security** | Trusted devices with an unrecognised one flagged, unlock method, sign-in activity, sign out everywhere |
| P6 | **Notifications** | Per-event push/SMS matrix, quiet hours. Visit confirmations always go by SMS |
| P7 | **Language & accessibility** | English/Hausa/Yorùbá/Igbo/Pidgin, text size, contrast, reduced motion, data saver |
| P8 | **Privacy & data** | Who can see what, download/print/export your copy, data residency |
| P9 | **Delete account** | What disappears **and what we must keep** — clinic-held notes, payment records, the anonymised access log |
| P9b | **Confirm deletion** | Four steps: a reason, typing DELETE, a code to your phone, an acknowledgement |

### Alerts and system states
| # | Screen | Notes |
|---|---|---|
| N0 | **Notification panel** | The bell opens an overlay with the five most recent and a "View all" |
| N1 | **Notifications** | Today / earlier, unread markers, a "needs you" rail |
| N2 | **No notifications** | Plus a route to the preferences |
| X1 | **Loading** | Skeletons for the dashboard and the mobile home |
| X2 | **Offline** | Last-saved timestamp, and an explicit split of **what still works** vs **what has to wait** |
| X3 | **Error** | Says plainly it is Medra's fault, gives a copyable reference, and tells you to go to the clinic if you need care now |

X1–X3 appear because of a condition, never because someone tapped something, so each carries a
switcher strip labelled **"state — for review, not a real control"**. It also reaches
`W4 Connection Lost`, which has the same problem for the same reason.

## Known stand-ins (deliberate, not oversights)

- **Uploaded documents open R3.** A scanned NHIS card opens the lab-result detail, the closest
  real document view. A dedicated uploaded-document screen is worth adding when upload is built.
- **"Add a medicine" opens R7.** Adding one by hand means photographing the pack or the
  prescription, which is what R7 does — but a manual-entry form is the more direct answer.
- **M3 returns to M1** rather than to a "refill pending" screen. The nudge on M1 carries the
  pending state.

## Assumptions baked in (change them if you disagree)

- **Nothing is shared by default.** Allergies and current medicines are the only exception, and
  they go to any doctor treating you, because the alternative is unsafe prescribing.
- **The access log is append-only** — for you, for the clinic, and for Medra. It is the member's
  evidence, so it cannot be something we can quietly clean up.
- **Deleting your account cannot delete the clinic's copy** of a note a doctor wrote. Nigerian
  retention rules apply to the clinic, not to Medra. P9 says so on the screen.
- **SMS is the floor, not a fallback.** Visit confirmations go out by SMS even with every other
  channel off, and Medra pays for the messages.
- **Refills need a human.** A doctor approves or declines; they can require a visit first.
- **A child's account transfers to them at 18.**

Figures, ranges and timings on screen are indicative — validate them with the pilot clinics.

## Preview without Figma

```bash
python3 tools/figma/preview_bundle.py figma/medra-member   # writes preview.html
```

`medra-member-overview.png` is the contact sheet. See `PROTOTYPE.md` for how the wiring works
and `MOTION.md` for the animation spec.
