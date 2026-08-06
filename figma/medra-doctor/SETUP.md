# Medra — Doctor / Medical Practitioner module

**114 frames · 8 Figma pages · Desktop 1440×900 + Mobile 390 · doctor-module only**

45 screens, every one drawn at both breakpoints, plus 24 component-state frames that become
10 interactive component sets.

Offline validation: **ALL 114 CLEAN, FULLY OFFLINE ✓** (`node validate.js`) · **0 horizontal overflow**

---

## 1. It no longer looks like the member app

That was the first thing asked for, so it is structural rather than cosmetic.

| | Member app | Doctor app |
|---|---|---|
| Navigation | one 262px navy sidebar | **88px icon rail + 236px contextual panel** |
| Ground | soft mesh gradient | **graph paper** — the ruled sheet a clinic already runs on |
| Corners | 24–28px | **14–18px** |
| Density | generous, one thing at a time | dense — the whole queue on one screen |
| Top bar | light search bar | **dark command strip**: breadcrumb, "2 need you", ⌘K patient search |
| Mobile chrome | light appbar | **navy header block** with the day's numbers inside it |
| Mobile nav | 5 flat tabs | 5 tabs with a **raised centre Consult action** |
| Primary action | teal | **navy**; teal is reserved for live/active |

The **contextual panel** is the important one. It is why the app can be dense without being
cluttered: it always holds what that section needs next. Today shows clinic progress and the
"needs you" counts; Requests shows the inbox split; Consultation shows who you are with, the
elapsed timer and what you can attach; Money shows the next payout and the trial countdown.

## 2. Mobile carries the same information as desktop

The previous version trimmed mobile, which was the second complaint. It no longer does. Every
mobile screen contains the same cards as its desktop twin, laid out vertically, with the desktop
side-rail content folded in underneath. The header block absorbs the panel's key numbers so
nothing is lost.

These are **scrolling frames** — `minH={844}`, so Figma grows them rather than clipping. The
tallest is C1 (the consultation room) at about 2,500px, which is a genuinely long screen on a
phone. What is guaranteed is that **nothing overflows horizontally** at 390 and that the primary
action of each screen sits in the first viewport.

## 3. Screens

### 1 · Getting started — activation and acquisition
| # | Screen | Why it exists |
|---|---|---|
| G1 | **Setup checklist** | Seven steps, three of them required, with an explicit "you are not bookable yet" gate. Activation is a doctor's first-booking moment, and this is what stands between them and it |
| G2 | **Verification** | Four-step progress with real timestamps, documents held, a median time, and everything worth doing while waiting — none of which needs redoing after approval |
| G3 | **Invite a colleague** | Referral. The message, the tracked invitations, and what both sides get |

### 2 · Today & schedule
| # | Screen | Why it exists |
|---|---|---|
| K1 | **Today's queue** | Next patient with the reason in their words, four stats, the waiting list with clinical flags (paediatric, possible cardiac, unpaid), what is left of the day, and who has already been seen |
| K2 | **Requests** | **PRD D3: confirm or decline.** Three booking requests with accept / another time / decline, plus auto-accept rules and everything else waiting |
| K3 | **Running late** | How late, who is affected, what they are told, on which channel. The single cheapest thing a clinic can do for its rating |
| K4 | **Read the file first** | Allergy banner, why they came in their words, what they flagged as missing, what they shared and what they did not, last visit, and a pre-flight checklist |
| K5 | **Appointment outcome** | **PRD D3: mark complete / no-show.** Four outcomes, what a no-show does to the fee, the slot and their record, and a "do not count this against her" override |
| K6 | **The week** | Six-day grid with booked / open / held-for-payment / break / away, the day list, and the week's counts including no-shows |
| K7 | **Availability** | Working days, slot length, buffer, horizon, same-day cutoff, daily cap, unpaid-hold, breaks, travel buffer, and where each type can be booked |
| K8 | **Time off** | Blocks the days, shows who is already booked and how much is refundable, offers to message them, and offers to hand them to a named colleague |

### 3 · Consultation — the spine
| # | Screen | Why it exists |
|---|---|---|
| C1 | **In progress** | The six PRD note fields by name — presenting complaint, examination, diagnosis, treatment plan, doctor's comment, **private notes** — plus the "something is missing from her record" prompt and a live rail of allergies, adherence, BP trend and outstanding tests |
| C2 | **Templates** | Five templates with a live preview, auto-suggest, and clinic-shared sets |
| C3 | **Prescribe** | Drug search, dose builder, refills, patient-facing instructions, reminder — and a **hard block on a penicillin prescription for a penicillin-allergic patient**, overridable only with a written reason. Five safety checks, including "kidney function unknown" |
| C4 | **Order tests** | Test search with prices, where she should go, clinical details for the lab, urgent flag, and a nudge if it is not done in 7 days |
| C5 | **Result** | Photograph it, we read the values, **you check them before release**, one line in plain language, hold-until-spoken, and the other results waiting |
| C6 | **Refer onward** | Named colleagues with next slots, a referral letter, urgency, what to share — and the loop that brings their reply back to you |
| C7 | **Review & sign** | Nine per-section switches for what the patient sees, a live preview of her phone, and an immutable signature block |
| C8 | **Signed** | Where everything went, what was released, the next patient |
| C9 | **Unsigned notes** | Two drafts, what an unsigned note costs the patient, the pharmacy and your payout, a recovered note, and reminders to stop it happening |
| C10 | **Virtual visit** | **PRD D5.** Your link, proof it reached her by three routes, the waiting room, and four fallbacks when the video fails |

### 4 · Patients
| # | Screen | Why it exists |
|---|---|---|
| P1 | **Find a patient** | Search by **Medra ID**, name or phone; QR scan; walk-in creation; access replies |
| P2 | **Patient record** | Consent-scoped. What she shared is shown; what she has not is listed as **explicitly locked**, so absence is never mistaken for nothing. Patient-added records and self-measured readings are labelled |
| P3 | **Ask for more** | Categories, why, for how long, on which channel, and everything you have already asked |
| P4 | **Follow-ups and recalls** | Retention. Seven reviews due, five tests never done, a recall message with your open slots, and how recalls have performed |
| P5 | **Messages** | Four unread across WhatsApp, email and in-app, with a symptom-flagged message surfaced, quick replies, and your boundaries |
| P6 | **Refills** | Approve / change / ask them in / decline, with the context that makes it a clinical decision rather than a blind renewal |
| P7 | **Results** | Three waiting, with a trend chart for the abnormal one, and why a doctor releases results at all |

### 5 · Practice & money
| # | Screen | Why it exists |
|---|---|---|
| S1 | **Public profile** | Bio, specialisation from the platform list, second specialities, languages, years, location, and a completeness meter tied to bookings |
| S2 | **Types & fees** | Four types with length, price and per-mode availability, what you actually receive, and every fee rule the member is also shown |
| S3 | **Virtual visits** | Provider choice, new-link-per-visit, lobby, phone fallback, connection warning, and the phase-2 note |
| S4 | **How patients reach you** | WhatsApp / email / phone / in-app switches, available hours, do-not-disturb, auto-reply, and the member-side preview |
| S5 | **Earnings** | Month to date, six-month chart, full breakdown including a no-show and a refund, payout account, hold period, statements, tax summary |
| S6 | **Subscription** | **PRD §7 Module 8.** Trial countdown, three plans, invoices, and exactly what a lock does — and does not — touch |
| S7 | **Where I practise** | Independent / facility / both, multiple locations, what the facility can and cannot see, and cover arrangements. **PRD §11.4** |
| S8 | **Account & security** | Devices including a shared clinic machine, 2FA, idle timeout, an audit trail, and leaving Medra |

### 6 · Growth (AARRR)
| # | Screen | Why it exists |
|---|---|---|
| R1 | **Insights** | The search → profile → booking → attended → signed funnel, and the four fixable settings costing bookings |
| R2 | **Ratings** | Distribution, recurring themes pulled from comments, replies, and how ratings work |
| R3 | **Booking link** | The link, a printable waiting-room QR poster, patient import, and where bookings actually came from |

### 7 · States & edge cases
| # | Screen | Why it exists |
|---|---|---|
| X1 | **Subscription locked** | What stops, what keeps working, and the rule that **a doctor's unpaid invoice never costs a patient their records** |
| X2 | **Nothing booked** | Empty state plus what actually gets a doctor booked |
| X3 | **Notifications** | Today / earlier, what is blocking a patient, per-channel delivery, quiet hours |
| X4 | **Offline** | Writing a note works offline; signing, prescribing and releasing do not — and three queued items are listed by name |
| X5 | **Error** | Says plainly it is Medra's fault, gives a copyable reference with the failing service, lists what is safe, and tells you to write on paper if a patient is in front of you |
| X6 | **Loading** | Skeletons for both breakpoints |

### 8 · Components
`Medra Doctor/Slot` (5) · `Queue Row` (3) · `Share Toggle` (2) · `Scope Line` (2) ·
`Drug Result` (2) · `Stat Tile` (4) · `Checklist Row` (2) · `Outcome` (2) · `Rail Item` (2)

## 4. Coverage

### From the PRD
| Requirement | Where |
|---|---|
| §7 M2 · profile, specialisation, bio, photo, fee, MDCN | S1 |
| §7 M2 · weekly availability, slot duration | K7 |
| §7 M2 · verified badge, manual MDCN check | G2, S1 |
| §7 M4 · today's dashboard | K1 |
| §7 M4 · confirm / decline pending bookings | **K2** |
| §7 M4 · mark complete / mark no-show | **K5** |
| §7 M6 · complaint, diagnosis, plan, prescriptions, follow-up, comment, **private notes** | **C1, C7** |
| §7 M7 · virtual flagged, doctor sends the room link | **C10** |
| §7 M8 · 30-day trial, countdown, Paystack, expired = locked | **S6, X1** |
| §10.2 D1–D5 | G2, S1, K7, K1, C1, C10 |
| §11.4 · independent practitioner without an institution | **S7** |

### From the 1 August review
MDCN log-in and **Medra ID search** (P1, command strip) · specialisation from a
platform-managed list with "add another" (S1) · **patient contact via WhatsApp / email / phone**
(S4) · doctor writes the note during the consultation (C1) · **doctor picks what the patient
sees** (C7) · asks about undisclosed history (C1) · uploads and releases lab results (C5, P7) ·
**drug search rather than free typing** (C3) · sets the meeting link, which is embedded in the
member's Join button (C10, S3) · transcription marked phase 2 (C1, S3).

### AARRR
| Stage | Screens |
|---|---|
| Acquisition | G2 verification · R3 booking link, QR poster, patient import · G3 invite a colleague |
| Activation | G1 checklist with a real gate · X2 first-week empty state · S1 completeness meter |
| Retention | K1 queue · P4 follow-ups and recalls · P5 messages · R1 insights · R2 reviews · X3 notifications |
| Referral | G3 invite a colleague · C6 refer a patient onward · R3 share your link |
| Revenue | S2 fees · S5 earnings and payouts · S6 subscription and trial · X1 locked |

### Scenarios covered beyond the happy path
Running late · no-show with a fee split · doctor cancels · video fails · unpaid slot released ·
booking declined with a refund · time off with patients already booked · handing patients to a
colleague · allergy blocks a prescription · result out of range held back · refill that should be
a visit instead · unsigned note · note recovered after a crash · offline with queued writes ·
service error mid-consultation · trial expiry and lock · shared clinic machine signed in ·
a patient declining an access request.

## 5. Open, and deliberately so

- **A medical doctor has not reviewed this.** Every clinical string — the note structure, the
  drug fields, the reference ranges, the safety checks — is a placeholder until they do.
- **Two money models are in the file.** The PRD says practitioners pay a **subscription** and
  patients pay providers directly (§4). The 1 August review added **payment before booking**,
  which means Medra collects and pays out. Both are designed (S6 subscription, S5 payouts) and
  S2 states that Medra earns from the subscription, not a commission. **Confirm which is true
  before build** — if it is both, someone has to justify charging twice.
- **The 50% no-show split** (K5, S2) is a pilot policy, not a decision.
- **Referral rewards** (G3) are indicative.
- **Institution-employed doctors** are represented in S7, but the facility admin's own portal
  (staff, seats, allocation, supervisor privileges) is a separate module.
- **A lab technician's own screen** does not exist; C5 covers a doctor uploading a result.

## 6. Render — doctor module only

See `CLI-PROMPT.md` for the exact instruction to hand to the terminal.

```powershell
.\render-doctor.ps1
```

It creates the eight `Medra Doctor —` pages, renders 114 frames into them, builds the component
sets on the doctor components page only, then wires the prototype. **It does not touch the
design-system, authentication or member pages.** The one cross-module link is Sign out, which
points at `Auth · Doctor — D6 Log In` if that frame exists and is skipped if it does not.

`link-doctor.js` returns `{ linked, navLinked, stayOnScreen, framesFound, missing }`.
A non-empty `missing` means that frame did not render — re-render that one `.jsx` and re-run step 4.

## 7. Preview without Figma
```bash
python3 tools/figma/preview_bundle.py figma/medra-doctor
```
`medra-doctor-overview.png` is the contact sheet for all 114 frames.
