# Review — 18 September 2026 (platform admin + product corrections)

**Who:** Godwin (Product) → Israel (UI/UX). **Where the work landed:** Figma file
`QCHjeHd3quYt5HXWUpCBFp` (*Medra-24*), page *Medra – Design Canvas*. Everything below was applied
**directly in Figma** through the figma-cli daemon (not through the JSX bundles), so read the
warning in §4 before you re-render any bundle.

Every screen that changed carries a yellow **CHANGE NOTE** sticky beside it on the canvas,
written for developers in plain language: what changed, and why. This document is the index of
those notes plus the decisions behind them.

---

## 1. Decisions (these override earlier documents)

| # | Decision | Replaces |
|---|---|---|
| D1 | **Doctors do not accept booking requests.** A member pays at booking, against the availability the doctor already published. The booking is confirmed on payment. The doctor is *notified* of a new booking and can only **reschedule** or **cancel with a full refund**. | PRD v2.0 §4 "doctor accepts/declines a request"; doctor screens K2 *Requests* and the auto-accept rules |
| D2 | **Private practice pays 1.5 % per consultation, not a subscription.** Medra takes 1.5 % of each consultation fee at the moment the member pays. The rest is paid out on the doctor's schedule. **The bank transfer charge on each payout is borne by the doctor, not Medra.** Organisations stay on plans (G1/G2). | HANDOFF §1 "independent practitioners pay a subscription"; open question §9.7 — **now closed** |
| D3 | **The doctor's schedule is a calendar**, in the Google Calendar idiom: hours down the side, days across, bookings as blocks. Clicking a day opens a **day drawer** (bookings, free slots, add booking, block the day). Clicking a booking opens an **appointment drawer** (reschedule / cancel & refund). | K6 *Week* list layout |
| D4 | **Addresses are collected at onboarding** for members (M4 *About you*) and doctors (D5 *Profile setup*): street, state, city/LGA. Street stays private; state and city drive "near me" and every region breakdown in the admin. | Region/state analytics that had no source data |
| D5 | **MFA is mandatory for every platform-admin sign-in** — no skip, no "remember this device". | PA2 copy |
| D6 | **Verification is manual.** Platform admins check MDCN / NMCN / PCN / CAC by hand and record what they found. There is no automatic register lookup. Nurses and pharmacists are verified in the same queue as doctors and organisations. | "Awaiting your decision" KPI on H1 with nowhere to go |
| D7 | **Escalations are tracked, not phoned.** Every escalation and privacy incident has a status tracker and an updates log. Medra does not make phone calls; it notifies, records and follows up in-app. | L2 "escalation ladder" |
| D8 | **Every table paginates.** No admin list is shown as an unbounded scroll. | R6 and others |
| D9 | **No unnecessary copy on auth screens.** Filler sentences removed; do not re-add them. | PA1/PA2 |

---

## 2. What changed, screen by screen

### Platform admin (new persona, `Platform · …` frames)

| Correction | Screen(s) | What changed |
|---|---|---|
| 6 · Payment history + retry | R2 *Organisation Detail* (+mobile) | PAYMENT HISTORY table (date, invoice, description, amount, method, status), paginated; a **Retry charge** action on a failed row and in the BILLING card. Admins can trigger a retry; the result lands in the audit log. |
| 7 · MFA | PA2 *Two-Factor*, PA1 *Log In* | Enforced-MFA copy, filler removed. |
| 8 · Performance by doctor | R3 *Practitioners* | Side column is now PERFORMANCE BY DOCTOR (bars) — the by-specialty breakdown was unreliable. |
| 9 · Revenue as a chart | R4 *Practitioner Detail* | 12-month revenue **line chart**; KPI shows *Medra fee 1.5 %*; RECENT ACTIVITY includes "rescheduled by doctor" and "cancelled — member refunded". |
| 10 · Member state / datasets | R5 *Members*, R6 *Member Detail*, all tables | State/region now sourced from onboarding (D4). Every table paginated, including R6 activity and consent tables. |
| 11 · Addresses | M4, D5 (+mobile) | See D4. |
| 12 · Privacy incidents | F2 *Privacy Incidents* → **F3 *Privacy Incident Detail*** (new, +mobile) | Rows in F2 open F3: what happened, status tracker, updates log, owner, next steps; *Log an update / Suspend the account / Close incident*. |
| 13 · Escalation ladder | L2 *Event Detail*, E2 *Escalation Detail* | "Escalation ladder" replaced by ESCALATION STATUS tracker + UPDATES LOG + "what Medra does here" (no calls). |
| 15 · Usage heatmap | N3 *Usage* | Density calendar uses the same colours as VISITS BY CHANNEL, with a legend. PEAK card follows the view filter (hour / day / date / month). |
| 16 · Custom pricing | G2 *Edit Plan* → **G3 *Subscriber Pricing*** (new, +mobile) | Per-organisation discount or fixed price, valid-from/until, reason; over 10 % needs a second admin. Existing overrides listed. |
| 17 · Legal content | V3 *Legal & Consent Documents* → **V4 *Publish Legal Document*** (new, +mobile) | Upload a PDF, paste a URL or text; version + effective date; who must accept; publish. |
| 18 · Verification queue | H1 *Control Center* → **Q1 *Verification Queue*** + **Q2 *Verification Detail*** (new, +mobile) | "Awaiting your decision" opens Q1: organisations, doctors, nurses, pharmacists, oldest first. Q2: manual register check form, documents submitted, Approve / Reject / Ask for more. **Verification** added to the sidebar and the mobile *More* menu. |
| 19 · Manual MDCN check | R4 *Practitioner Detail* | MDCN VERIFICATION card with *Verify MDCN number* (opens Q2) and *Mark as failed*. |

### Doctor module (`Doctor · …` frames — edited in place)

| Correction | Screen(s) | What changed |
|---|---|---|
| 2 · No accept step | K2 *Requests* (+mobile, sub-sheet *A booking*) | Rebuilt as **New bookings**: paid bookings, soonest first, with *Reschedule* and *Cancel & refund* per row; cancellation rules card. Auto-accept sheet deleted. **"Requests" renamed "Bookings" in the sidebar/tab bar of every doctor frame** (287 text nodes). K1 "3 booking requests" → "3 new bookings, all paid". |
| 3 · Calendar | K6 *Week* (+mobile), **K6 · Day drawer**, **K6 · Appointment drawer** (new), mobile sheets *Appointment* and *Block a day* (new) | Week grid 08:00–18:00, today tinted, red now-line, Day/Week/Month switch, *+ Add booking*, *Block a day*. Mobile is a day view with a date strip. |
| 4 · 1.5 % fee | S6 *Subscription* → **S6 *Fees & Payouts*** (+mobile, sub-sheet *Payout account*); X1 *Subscription Locked* → **X1 *Payout Account Needed*** (+mobile sheets); S2 *Types & Fees*; S5 *Earnings*; the sidebar "Free trial" card on every doctor frame; K9 | Payout table (fees, Medra 1.5 %, bank charge, paid to you), payout account + schedule, worked example. X1 now covers "earning but no bank account on file" — nothing is hidden or paused, only payouts are held. S2/S5 deduction line is *Medra fee · 1.5 %*. Plans/subscription sheets deleted. |

### Support — 25 September (new, nothing existed before)

Medra had no support screen anywhere: every persona had a **Help** button in the sidebar that led
nowhere, and the platform admin had no way to answer anyone. Both halves of the loop are now designed.

| Side | Screens | What it does |
|---|---|---|
| Members, doctors, organisations | `<Persona> · Support — T1 Help & Support`, `T2 New Ticket`, `T3 My Ticket` (each +mobile, 18 frames) | Search, common topics for that persona, and the tickets they already raised. The form attaches the booking / payout / seat the ticket is about, so it arrives with a reference. The ticket screen is a plain conversation with Medra, plus "this is sorted — close it" and "it is still wrong". |
| Platform admin | `Platform · Support — S1 Ticket Queue`, `S2 Ticket Detail` (+mobile) | One queue across all personas, oldest waiting first, with the reply promise, topic mix and who is carrying what. The detail screen holds the conversation, internal notes the member never sees, the reply box, and the booking or refund the ticket is about. `Escalate` hands it to E1. |

**Support** is now in the platform sidebar (32 frames) and the mobile *More* menu; every persona's
**Help** button opens its own T1. 378 interactions wired. Two rules are stated on the screens
themselves: Medra answers in the app and never rings you, and Medra never asks for a password,
card PIN or one-time code.

### Two-factor — 25 September (corrected and completed)

The old PA2 said *"We sent a 6-digit code to the authenticator app"* and *"Code not arriving?"*.
**Medra does not send this code** — Google Authenticator generates it on the admin's phone. PA2 now
says so, and three screens were added for the part that was missing (PA2 only ever showed the state
*after* an app was connected):

* `Auth · Platform — PA5 Set Up Authenticator` — install **Google Authenticator** (the only app
  supported at launch), scan the QR or type the setup key, confirm with a code.
* `Auth · Platform — PA6 Recovery Codes` — ten single-use codes, shown once, must be confirmed saved.
* `Auth · Platform — PA7 Use a Recovery Code` — the way back in when the phone is lost.

### Marketing (new, `Marketing · …` frames)

* **W1 Coming Soon** (waitlist) — desktop + mobile. Photo dissolves into a solid navy band so the Medra mark and wordmark read; email pill; socials. Awaiting a final hero image (brief: health-record subject, composition on the outer thirds so the centre copy is not covered).
* **P1 Home** (landing) — desktop, from the video reference, now with the six final photos. **21 Sep:** copy rewritten for all three personas (members, doctors at 1.5 % per consultation, hospitals/labs); 'Join the waitlist' removed from the landing (W1 has its own page); fixed header; persona buttons in the hero; per-card CTAs; contact form with name + 'I am' fields; interactive footer with the fading Medra watermark; responsive to 390 px. Figma prototype: nav/footer links scroll to their section, CTAs go to W1 / M6, and the *Marketing · Landing* flow opens on three *Enter* frames that stage the hero in. **Live HTML:** https://clepbo.github.io/Medra-24/site/landing-prototype.html The scroll animation (cream sheets sliding up over the gradient, staggered reveals, hover lifts) is delivered as an **HTML prototype**, not in Figma: `docs/site/landing-prototype.html`. Illustration placeholders are labelled; prompts are in §3.

---

## 3. Illustration briefs for the landing page

Style for all six: flat line-art with two-tone fills, teal `#2F8BAC` line, peach `#F1C4AD` and
mint `#5FD3C7` fills, navy `#0F2233` accents, no gradients, no faces in photographic detail,
transparent background, 4:3 unless stated. Nigerian subjects, contemporary dress.

1. **Hero** — a member holding a phone that shows a health record card (Medra ID `MDR-8842-19`,
   a result, a prescription). On the far left a doctor at a small desk; on the far right a
   reception counter. The phone is the centre of gravity; the two sides are outer-third.
2. **How it works** — a seated doctor with a laptop, a dotted path curling from a search
   (magnifier) → a calendar with a paid tick → a record card. 4:3.
3. **For members** — a parent and child, the parent's phone showing two record cards. 16:10.
4. **For doctors** — a doctor at a desk with a diary that fills itself (three bookings sliding
   into a calendar), an e-prescription pad beside. 16:10.
5. **For hospitals & labs** — a front desk, a lab bench with three tubes and a pharmacy shelf,
   all connected by one line to a single record card. 16:10.
6. **Questions** — a speech bubble with a real person's silhouette behind it (not a robot), a
   small clock showing "one working day". 4:3.

---

## 4. Warning for whoever re-renders a bundle

The doctor and auth changes in §2 were made **on the Figma canvas, not in `figma/medra-doctor`
or `figma/medra-auth`**. `render-all.ps1` deletes and replaces frames by module prefix, so a
re-render of either bundle will **silently undo** K2, K6, S6, X1, M4, D5 and the
"Requests → Bookings" rename. Before re-rendering:

1. port the changes into the JSX (K2, K6 + drawers, S6, X1, M4/D5 address fields, sidebar label),
2. or exclude those frames from the render scope.

The platform-admin persona, Q1/Q2/G3/V4/F3 and the marketing frames have **no JSX source**; they
exist only in Figma and in the builder scripts kept with the figma-cli session.

---

## 5. Prototype coverage after this review

* Platform admin: 80 frames, 963 wired interactions, **0 dead ends**; only the six state
  screens (Loading / Offline / Error, desktop + mobile) are unreachable by design — they are flow
  starting points.
* Doctor: 121 new interactions wired for the calendar drawers, booking sheets, payout screens.
* Canvas (19 Sep): **every screen now shows its full content** — 253 frames whose content ran past the 900 / 844 floor (mostly org, member, doctor consult and auth mobile screens) were expanded to their content height instead of clipping. The whole canvas was then re-flowed row by row: 200 px between screen rows, 360 px before a function banner, 720 px before a persona banner; 0 overlapping frames; every change note sits clear of its neighbours. Frames are taller than the device viewport on purpose — the prototype still scrolls inside 1440×900 / 390×844.
