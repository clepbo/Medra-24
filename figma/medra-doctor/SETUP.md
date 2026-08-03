# Medra — Doctor App (batch 1)

**58 frames · 6 Figma pages · Desktop 1440×900 + Mobile 390×844 · "Soft Clinical", navy-led**

Built from the 1 August review, where the doctor flow was asked to be "much more robust".

The spine is one sentence: **see today's queue → read the file before you start → consult and
write the note as you go → decide what the patient sees → sign it.** Schedule, fees, meeting
links, contact channels and earnings all exist to serve that spine.

| Figma page | Screens | Frames |
|---|---|---|
| `Medra Doctor — Today & Schedule` | K1–K5 (5) | 10 |
| `Medra Doctor — Consultation` | C1–C7 (7) | 14 |
| `Medra Doctor — Patients` | T1–T3 (3) | 6 |
| `Medra Doctor — Practice & Earnings` | S1–S5 (5) | 10 |
| `Medra Doctor — States` | X1–X3 (3) | 6 |
| `Medra Doctor — Components` | 6 component sets | 12 |

Offline validation: **ALL 58 CLEAN, FULLY OFFLINE ✓** (`node validate.js`) · **0 mobile overflows**

## Two deliberate differences from the member app

1. **Navy is the primary action colour**, not teal. This is a tool used all day between patients;
   the teal stays with the member-facing product so the two never feel like the same screen.
2. **Higher density.** A member books once a month and gets air. A doctor scanning a queue
   between patients needs the whole queue on one screen.

## Render

```powershell
# render the auth bundle first if you want the sign-out link to resolve
.\render-doctor.ps1
```

`link-doctor.js` returns `{ linked, navLinked, stayOnScreen, framesFound, missing }`.

## Screens

### Today & schedule
| # | Screen | Notes |
|---|---|---|
| K1 | **Today's queue** | Next patient with the reason for coming, the waiting list, four stats, and a **Needs you** rail — results to release, refills waiting, unsigned notes. Everything in that rail is blocking a patient |
| K2 | **The week** | Six-day grid with booked / open / break / blocked, day list underneath, and this week's counts including no-shows |
| K3 | **Read the file first** | The screen the review asked for by implication: allergy banner, why they came **in their words**, what they have shared and what they have not, and what happened last time — before you say hello |
| K4 | **Availability** | Working days, slot length, buffer, booking horizon, same-day cutoff, daily cap, breaks. These rules are what makes "real availability" true on the member side |
| K5 | **Time off** | Blocks the days, shows exactly who is already booked, and offers to message them — Medra never cancels a patient on the doctor's behalf without them choosing it |

### Consultation
| # | Screen | Notes |
|---|---|---|
| C1 | **In progress** | Patient strip with a live timer, tabbed note / prescription / tests / files, four note fields with template buttons, the **"something is missing from her record"** prompt, and a live rail of allergies, adherence, BP trend and outstanding tests |
| C2 | **Note templates** | Four templates with a preview. Templates fill structure only — nothing is submitted for you |
| C3 | **Prescribe** | Drug search against the essential-medicines and NAFDAC lists, dose builder, refills, plain-language instructions the member sees — and a **hard block on penicillin for a penicillin-allergic patient**, overridable only with a written reason |
| C4 | **Order tests** | Test search, where she should go, price shown, clinical details for the lab, urgent flag |
| C5 | **Upload a result** | Photograph it, we read the values, **you check them before release** — plus a plain-language line and a switch to hold the result until you have spoken |
| C6 | **Review & sign** | Per-section switches for what the patient sees, a live preview of her phone, and the signature block. Private working notes are off by default; she is told a private note exists, not what it says |
| C7 | **Signed** | What went where, what you earned, and the next patient |

### Patients
| # | Screen | Notes |
|---|---|---|
| T1 | **Find a patient** | Search by **Medra ID**, name or phone — the review's point that a doctor should be able to pull up a card when the patient remembers nothing else. Plus QR scan and walk-in creation |
| T2 | **Patient record** | Consent-scoped. What she shared is shown; what she has not is listed as **explicitly locked**, so a doctor never mistakes absence for "nothing there" |
| T3 | **Ask for more** | Pick the categories, write why, choose the window. She can accept, part-accept or decline — and every ask and answer is logged |

### Practice & earnings
| # | Screen | Notes |
|---|---|---|
| S1 | **Public profile** | Bio, specialisation (from the platform-managed list), languages, where you practise, and the numbers members judge you on |
| S2 | **Types & fees** | Per-type length and price, and an honest **what you actually receive** breakdown: fee − 12% commission − processing = payout |
| S3 | **Virtual visits** | The MVP decision made concrete: pick Google Meet / Zoom / Teams / paste-your-own, new link per appointment, lobby, phone fallback. Medra does not host the call — it hands over a working link at the right moment |
| S4 | **How patients reach you** | WhatsApp, email, phone, in-app — each a switch, with available hours, do-not-disturb and an explicit "this is not for emergencies" line the patient sees |
| S5 | **Earnings** | Month to date, breakdown by type, refunds, commission, Friday payouts, statements and a tax summary |

### States
| # | Screen | Notes |
|---|---|---|
| X1 | **Verification pending** | Four-step progress with timestamps, and everything you can usefully set up while you wait — none of it needs redoing after approval |
| X2 | **Nothing booked** | Empty state plus what actually gets a doctor booked, marked as pilot observations rather than promises |
| X3 | **Notifications** | Today / earlier, a rail of what is blocking a patient right now, and per-channel delivery including WhatsApp |

## Decisions baked in (from the review)

- **Search by Medra ID.** Members get `MDR-8842-19` at the end of onboarding, it sits under their
  name on their profile, and it is on their printed summary and QR code.
- **The doctor sets the meeting link.** In-app video is designed but marked **PHASE 2** on the
  member screens; the MVP hands over a Google Meet or Zoom link embedded in the Join button.
- **Transcription is phase 2** and is shown as such, with the note that nothing is recorded
  without the patient agreeing first.
- **The doctor chooses what the patient sees** — per section, with a live preview, and with the
  patient told that a private note exists.
- **The undisclosed-history prompt is a first-class field**, not a free-text afterthought. What
  the doctor asked and what they were told is stored with the consultation.
- **Prescribing is drug-search based**, not free typing, so allergy and interaction checks can
  actually fire. The specialisation list is platform-managed, as asked.
- **Commission is 12%** during the pilot, stated on screen where the doctor can see it. Change it
  with the pilot doctors, not silently.

## Known gaps for the next batch

- **Institution-employed doctors.** This batch assumes an independent practitioner. A doctor who
  belongs to a facility needs a facility switcher, shared templates, and rules the admin sets.
- **Lab technician role.** The review said a hospital can have a technician enter results; C5
  covers the doctor uploading, not a technician's own screen.
- **Referrals to another doctor** are not designed yet.
- **A medical doctor has not reviewed this.** The review scheduled exactly that. Treat every
  clinical string — the note structure, the drug fields, the reference ranges — as a placeholder
  until then.

## Preview without Figma
```bash
python3 tools/figma/preview_bundle.py figma/medra-doctor
```
`medra-doctor-overview.png` is the contact sheet for all 58 frames.
