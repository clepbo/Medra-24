# Medra — Member App (batch 2: Visits · Records · Medicines · Profile)

**108 frames · 6 Figma pages · Desktop 1440×900 + Mobile 390×844 · "Soft Clinical"**

This batch closes the bottom nav. Before it, three of the five mobile tabs went nowhere and
"Visits" pointed at the booking-confirmed screen as a stand-in. Now every tab lands on a real
screen, on both breakpoints, and so does the desktop sidebar.

| Figma page | Screens | Frames |
|---|---|---|
| `Medra Member — Visits & Virtual Care` | W0, V1–V7, W1–W4 (12) | 24 |
| `Medra Member — Records` | R1–R10 (10) | 20 |
| `Medra Member — Medicines` | M1–M5 (5) | 10 |
| `Medra Member — Profile & Settings` | P0–P9 + P3b, P9b (11) | 22 |
| `Medra Member — Alerts & States` | N0–N2, X1–X3 (6) | 12 |
| `Medra — Interactive Components · Care` | 6 component sets | 20 |

Offline validation: **ALL 108 CLEAN, FULLY OFFLINE ✓** (`node validate.js`)

## Render (Figma Desktop open + connected)

```powershell
# 1. batch 1 first — the nav map links these screens back to Home and Find care
cd ..\medra-member ; .\render-member.ps1

# 2. then this batch
cd ..\medra-member-2 ; .\render-member2.ps1
```

`render-member2.ps1` creates the six pages, renders every frame, then runs:
1. `components-member2.js` — converts the `cmp/*` frames into **interactive components**
   (it only removes the sets it owns, so the batch-1 component page is untouched)
2. `link-member2.js` — wires the prototype, closes the nav **across both batches**, arranges

`link-member2.js` returns `{ linked, navLinked, stayOnScreen, framesFound, missing }`.
A non-empty `missing` means that frame is a stale render — re-render just that `.jsx` and re-run.

> **Re-render batch 1.** Its four mobile frames changed in this pass: the bottom nav went from
> four tabs to five (Medicines was desktop-only), and three mobile screens were trimmed to fit
> 844 (see below). If you skip step 1, batch-1 mobile frames will still show the old 4-tab nav.

## Layout rules that matter for Figma

- **No `wrap="wrap"`.** figma-ds-cli ignores auto-layout wrapping, so wrapped rows ran
  off-canvas. Every multi-item row is chunked explicitly with `rows_of()`. Verified: widest
  content in every frame is exactly its frame width — nothing overflows horizontally.
- **No `items="stretch"`.** The CLI rejects it, so nothing depends on a stretched child. Two
  places where the obvious solution needed it were designed differently instead:
  the records timeline uses a **date gutter + connector stubs** rather than a stretched rail,
  and the video call places its self-view with `justify`/`align` rather than absolute position.
- **`grow` is a row property.** `grow={1}` on a child of a *column* stretches it vertically —
  that is what inflated the in-call quick actions. `mini_btn(..., full=True)` emits `w="fill"`
  instead, for use inside columns.
- **Mobile content fits 390 × 844.** Measured, not assumed: `tools/figma/preview_bundle.py`
  renders the bundle and a Playwright pass measures the bottom-most element in every frame
  against the 844 budget. Both bundles are at **0 overflows**.

  This pass also caught **three batch-1 screens that were over** (P1 profile 902 px,
  S1 results 862 px, H2 empty home 852 px) — my earlier "tallest 736 px" claim came from a
  weaker measurement that only read the clipped frame height, not the content extent.
  All three are fixed.

## Screens

### Visits & virtual care
| # | Screen | Notes |
|---|---|---|
| V1 | **Upcoming visits** | Tabs, next visit with Join/Reschedule/Cancel, a visit booked for a dependant, "get ready" checklist, directions |
| V2 | **Past visits** | Completed with "View summary" + "Book again"; a cancelled one with its reason; year filters; spend to date |
| V3 | **No visits** | Empty state + what you get on every Medra visit |
| V4 | **Visit detail** | Status, fee, reason, reminders, how to join, share-records nudge, full action set |
| V5 | **Reschedule** | Current slot shown as "will be released", new day + open times, the ₦2,000 late-change rule stated up front |
| V6 | **Cancel visit** | Reason (used only to improve Medra, not shown to the doctor), free-text, what happens, destructive confirm vs "Keep my visit" |
| V7 | **Cancelled** | Confirmation, SMS sent, nothing charged, rebook suggestion |
| W1 | **Pre-call check** | Self-view, camera/mic/connection checks, mic meter, low-data mode, **"call me on the phone instead"**, waiting-room note |
| W2 | **In call** | Doctor feed, self-view PiP, encrypted + timer plate, live captions, control bar; desktop adds a rail showing exactly what the doctor can see right now |
| W3 | **Visit summary** | Duration, what the doctor recorded, links into the note/prescription/tests/follow-up, anonymous rating |
| W4 | **Connection lost** | Attempt counter, "your visit is saved", switch to audio, ask the clinic to ring you |

### Records — the part that makes Medra more than a booking site
| # | Screen | Notes |
|---|---|---|
| R1 | **Timeline** | Month groups with a date gutter, six record types, who-has-access banner, health summary, "bring in older records" |
| R2 | **Consultation note** | Why you came / examination / assessment / plan, everything that came out of the visit, and a **signature block: MDCN number, timestamp, "cannot be edited"** |
| R3 | **Lab result** | Values with reference ranges and flags, the original scan, the accredited lab, a plain-language explainer, trend comparison |
| R4 | **Vitals trend** | Six-month blood-pressure chart, other measurements, add a reading. Self-measured readings are **labelled as such** so no clinician mistakes them for clinic results |
| R5 | **Share records** | Who (doctor, search, or a QR for a walk-in) · what (six scopes; allergies and medicines are locked on) · how long (this visit / 24 h / 7 d / 30 d) · NDPA 2023 consent statement |
| R6 | **Who has access** | Active shares with expiry and instant revoke, ended shares, and an **append-only view log** — "who opened what, when", which neither you nor Medra can edit |
| R7 | **Add a record** | Camera or file, type, date, clinic, note; scanning tips; auto-read fields you can correct |
| R8 | **Record added** | What we read from the photo, every field editable, labelled "added by you" |
| R9 | **No records** | Three ways the history fills up |

### Medicines
| # | Screen | Notes |
|---|---|---|
| M1 | **My medicines** | Today's doses with mark-taken, adherence dots, refill nudge, allergy warning |
| M2 | **Medicine detail** | How to take it, when to call a doctor, where it came from (linked to the note), 14-day adherence, reminders |
| M3 | **Request a refill** | Which medicine, days needed, clinic pharmacy / nearby / delivery, note to the doctor, what happens next — and that approval is **not** automatic |
| M4 | **Reminders** | Per-medicine times, push/SMS/voice channels, quiet hours with an urgent-override |
| M5 | **No medicines** | Why adding them yourself is still worth it |

### Profile & settings
| # | Screen | Notes |
|---|---|---|
| P0 | **Profile** | Health snapshot, Medra ID + QR for reception. Mobile uses a **two-up tile hub** so all six destinations fit one screen |
| P2 | **Personal details** | Name must match your ID for check-in; verified phone; emergency contact; medical basics |
| P3 | **Dependants** | A child and an older parent, with "book for" and "manage" |
| P4 | **Add a dependant** | Relationship, details, guardian consent, and the **handover at 18** |
| P5 | **Devices & security** | Trusted devices with an unrecognised one flagged, unlock method, step-up checks, sign-in activity |
| P6 | **Notifications** | Per-event push/SMS matrix, quiet hours. Visit confirmations always go by SMS |
| P7 | **Language & accessibility** | English/Hausa/Yorùbá/Igbo/Pidgin, text size, contrast, reduced motion, screen-reader hints, data saver, offline records |
| P8 | **Privacy & data** | Who can see what, download/print/export your copy, how Medra uses data, data residency |
| P9 | **Delete account** | What disappears **and what we must keep** — clinic-held notes, payment records, the anonymised access log — 30-day grace, plus smaller alternatives |

### Alerts & system states
| # | Screen | Notes |
|---|---|---|
| N1 | **Notifications** | Today / earlier, unread markers, a "needs you" rail |
| N2 | **No notifications** | Plus a route to the preferences |
| X1 | **Loading** | Skeletons for the dashboard and the mobile home |
| X2 | **Offline** | Last-saved timestamp, and an explicit split of **what still works** vs **what has to wait** |
| X3 | **Error** | Says plainly it is Medra's fault, gives a copyable reference, and tells you to go to the clinic if you need care now |

## No dead ends — how it is guaranteed

`link-member2.js` wires in three passes:

1. **382 explicit screen-to-screen links** from the table above.
2. **The nav map** — `Nav Home · Nav Find · Nav Visits · Nav Records · Nav Meds · Nav Profile ·
   Notifications` applied to **every frame in both batches**, desktop→desktop and mobile→mobile.
3. **A sweep**: anything still named `Btn …` with no reaction gets an `ON_CLICK` that stays on
   its own screen (10 ms Smart Animate — visually nothing). Toggles, radios, chips and filters
   land here. Nothing in the file is a dead hotspot, and the pass reports its count as
   `stayOnScreen` so you can see exactly how many are placeholders for real state.

Cross-module links: `Sign out`, `Sign out everywhere` and `Confirm delete` go to
**Auth · Member — M6 Log In**; `Book a visit`, `Book again` and `Book follow-up` go to the
batch-1 search and booking screens.

## Known stand-ins (deliberate, not oversights)
- **Uploaded documents open R3.** A scanned NHIS card opens the lab-result detail, which is the
  closest real document view. A dedicated "uploaded document" detail screen is worth adding when
  upload gets built for real.
- **"Add a medicine" opens R7.** Adding one by hand means photographing the pack or the
  prescription, which is what R7 does — but a manual-entry form is the more direct answer.
- **M3 returns to M1** rather than to a "refill pending" screen. The nudge on M1 carries the
  pending state; a separate confirmation screen would be the fuller treatment.

## Assumptions baked in (change them if you disagree)
- **Nothing is shared by default.** Allergies and current medicines are the only exception, and
  they are shared with any doctor treating you, because the alternative is unsafe prescribing.
- **The access log is append-only** — for you, for the clinic, and for Medra. It is the member's
  evidence, so it cannot be a thing we can quietly clean up.
- **Deleting your account cannot delete the clinic's copy** of a note a doctor wrote. Nigerian
  medical-records retention applies to the clinic, not to Medra. P9 says so on the screen.
- **SMS is the floor, not a fallback.** Visit confirmations always go out by SMS even with every
  other channel off, and Medra pays for the messages.
- **Refills need a human.** A doctor approves or declines; they can require a visit first.
- **A child's account transfers to them at 18.**

Figures, ranges and timings on screen are indicative — validate them with the pilot clinics.

## Preview without Figma
```bash
python3 tools/figma/preview_bundle.py figma/medra-member-2   # writes preview.html
```
`medra-member-2-overview.png` is the contact sheet for all 108 frames.

See `MOTION.md` for the animation spec.


## Added after the 1 August product review

| # | Screen | Why |
|---|---|---|
| W0 | **Join by link** | The MVP video path: the doctor's own Google Meet or Zoom link, embedded in the Join button, with phone and WhatsApp fallbacks. W1/W2/W4 (in-app video) stay in the file, badged **PHASE 2** |
| R10 | **One-page summary** | "What would the print one-page summary look like? Can they select what to print?" — blood group and allergies always on, everything else opt-in, live preview, QR code |
| N0 | **Notification panel** | The bell now opens an overlay with the five most recent and a "View all", instead of jumping straight to the full page |
| P3b | **Family plan** | Two dependants free, then ₦3,000/month for up to six people or ₦1,500 per extra person — "they taste the service before" |
| P9b | **Confirm deletion** | Deleting now takes four steps: a reason, typing DELETE, a code to your phone, and an acknowledgement |

Changed in place: the Medra ID sits under the member's name on the profile; WhatsApp is a first
class notification and reminder channel everywhere; who-has-access is a selectable list with
revoke-selected and revoke-everything.
