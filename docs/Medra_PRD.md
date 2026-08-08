# Medra — Product Requirements Document (PRD)

**A unified medical records & consultation-booking platform for Nigeria**

| | |
|---|---|
| **Product** | Medra |
| **Document type** | Product Requirements Document (PRD) v1.0 |
| **Status** | Draft for review |
| **Owner** | Godwin Okwor (Product) |
| **Contributors** | Israel Oni (UI/UX Design) |
| **Launch market** | Abuja, Nigeria (pilot) |
| **Date** | 23 July 2026 |
| **Related docs** | UI/UX Design Brief (call transcript, 10 Jul 2026) · UI/UX Design Scope · Medra MVP Feature Set |

---

## 1. Executive Summary

Medra is a mobile-responsive web platform that digitises how Nigerians find care, book consultations, and carry their medical history. Today most private hospitals in Nigeria run on paper filing and WhatsApp/phone booking. There is no shared medical database, so a patient's history lives on paper they must physically carry between doctors — creating avoidable risks such as clashing drug prescriptions, and wasted trips to unavailable doctors.

Medra solves this in three layers:

1. **A patient-facing booking experience** — find a verified doctor or institution, see real availability, and book (in-person or virtual) before leaving home.
2. **A hospital/clinic operating system** — a shared database that institutions use internally to manage bookings, allocate doctors, hold patient records, and communicate between staff.
3. **A portable medical history** — each patient owns a continuous, structured record (diagnoses, prescriptions, results, recommendations) that any authorised doctor can read to make safer decisions.

**Business model:** Institutions and independent practitioners pay a subscription to be on the platform (priced by size, with enterprise/multi-branch plans). Patients use the platform for free and pay institutions directly for services rendered.

**MVP thesis:** The MVP must answer one question — *"Can a patient see if a doctor is available and book before leaving home?"* — while capturing just enough medical record data to make the platform clinically useful.

---

## 2. Problem Statement & Background

### 2.1 Current state
- Private healthcare in Nigeria relies on **paper filing** and **WhatsApp/phone diaries** for booking.
- There is **no unified medical database** — records are siloed per hospital, mostly on paper.
- Patients **physically carry printed results** between doctors and often cannot interpret them.
- **No cross-visit continuity:** a new doctor has no view of prior diagnoses or current medication.

### 2.2 Consequences
- **Wasted trips:** a patient travels to a clinic only to find the doctor unavailable.
- **Clinical risk:** a new prescription can clash with existing medication the new doctor is unaware of.
- **Lost history:** paper is lost, damaged, or simply not brought to the visit.
- **Operational drag:** clinics manage bookings and internal communication manually.

### 2.3 Opportunity
A single system that unifies **booking + records + internal hospital operations**, sold to institutions as a subscription while remaining free for patients, positioned to become the medical database standard for private care in Nigeria — starting with Abuja.

> **Positioning note (from the client):** Medra is *not* "just a booking site." Booking is the entry point; the durable value is the **unified medical database** institutions use internally and the **portable patient history** that follows the patient across providers.

---

## 3. Goals & Objectives

### 3.1 Product goals
- Give patients **one place** to find institutions/practitioners, book consultations, and access their own medical history.
- Give institutions a **paid, subscription-based system** to manage bookings, staff, and patient records internally.
- Support **independent private practitioners** as first-class service providers.
- Design a UI that **clearly communicates the underlying data model** to developers, given the volume and sensitivity of medical data.

### 3.2 Business objectives
- Validate willingness-to-pay with **3–5 pilot clinics in Abuja**.
- Prove the core loop: **search → see real availability → book → attend → record written → history readable**.
- Establish a repeatable **institution onboarding + MDCN verification** process.

### 3.3 Non-goals (for MVP)
Full video-calling UI, doctor analytics, patient ratings/reviews, multi-language support, offline mode, and patient-side platform fees are explicitly **out of MVP scope** (see §9).

---

## 4. Success Metrics (KPIs)

| Category | Metric | MVP target (directional) |
|---|---|---|
| Activation | % of registered patients who complete a first booking | ≥ 40% |
| Core value | % of bookings where the doctor writes a consultation note | ≥ 80% |
| Reliability | Booking flow completion rate (start → confirmed) | ≥ 90% |
| No-show reduction | No-show rate for booked appointments (SMS-reminded) | Trend down vs. clinic baseline |
| Availability accuracy | Bookings against slots that turn out unavailable | < 2% |
| Monetisation | Pilot clinics converting from free trial to paid | ≥ 50% |
| Retention | Weekly active doctors during pilot | Trend up |

> Targets are placeholders to be confirmed against pilot-clinic baselines during Discovery.

---

## 5. Target Market & Personas

**Launch market:** Abuja private hospitals/clinics and independent practitioners; patients within reach of those providers. Nationwide/enterprise (multi-branch) follows.

### 5.1 Personas

> **Nomenclature:** people who use Medra for their own care are **members**, not "patients".
> "Patient" is reserved for the *clinical* context — a doctor's patient list, a consultation note.
> This keeps the product respectful of people who are simply managing their health, not sick.


**Member ("patient" only in clinical context) — "Amara", 31, Abuja**
Wants to see the right doctor without wasted trips, and to stop carrying paper results between doctors. Needs a simple phone-based sign-up, clear availability, and a readable history.

**Institution Admin — "Mr. Bello", clinic administrator**
Runs bookings and staff for a private clinic. Wants incoming bookings routed to the right doctor, staff managed, and one bill for the whole institution (including branches).

**Doctor / Staff — "Dr. Ngozi", 38**
Needs a clean daily schedule, the patient's relevant history at the point of consultation, and a fast way to record diagnosis, prescriptions, and follow-up.

**Private Practitioner — "Dr. Femi", independent**
Operates without an institution. Wants to enrol as a service provider, set availability, and manage his own bookings and patient notes.

**Platform Admin — Medra operations**
Approves institutions, verifies MDCN numbers, configures subscription plans, and oversees platform activity. *(Role assumed in scope doc — confirm.)*

**Organisation / Employer sponsor (future) — HR at a company**
Wants to cover employee medical costs like a corporate health plan by enrolling staff against an institution. *(Raised on the call as feasible; parked for a later phase.)*

---

## 6. User Roles & Permissions

Five roles. RBAC is a core, security-sensitive requirement because of medical-data sensitivity.

| Capability | Patient | Doctor / Staff | Institution Admin | Private Practitioner | Platform Admin |
|---|:--:|:--:|:--:|:--:|:--:|
| Browse institutions/practitioners | ✅ | — | — | — | ✅ |
| Book / cancel own appointment | ✅ | — | — | — | — |
| View **own** medical history | ✅ | — | — | — | — |
| View **assigned patient** history | — | ✅ | ✅ (manage) | ✅ | — |
| Write consultation note / prescription | — | ✅ | — | ✅ | — |
| Set availability / calendar | — | ✅ | ✅ (for staff) | ✅ | — |
| Confirm/decline/complete/no-show booking | — | ✅ | ✅ | ✅ | — |
| Allocate booking to a doctor | — | — | ✅ | — | — |
| Manage staff (roles & permissions) | — | — | ✅ | — | — |
| Manage subscription/billing | — | — | ✅ | ✅ | — |
| Internal staff messaging | — | ✅ | ✅ | — | — |
| Approve institutions / verify MDCN | — | — | — | — | ✅ |
| Configure subscription plans | — | — | — | — | ✅ |
| Platform-wide analytics | — | — | — | — | ✅ |

> **Open item:** institution staff roles beyond "doctor" — nurses, receptionists, lab techs — may need distinct permission sets. Confirm before finalising the RBAC matrix (see §17).

---

## 7. Scope Overview — MVP vs. Future

Medra's full vision spans four portals. The **MVP** ships a mobile-responsive web app focused on the patient booking loop plus the minimum records and clinic tooling to be useful.

| Area | MVP | Phase 2 | Phase 3+ |
|---|---|---|---|
| Patient booking | ✅ Full core flow | Rescheduling, waitlists | — |
| Doctor availability & dashboard | ✅ | Analytics | — |
| Medical records | ✅ Basic structured note | Attachments, lab results, ICD codes | Interoperability/exports |
| Telemedicine | ✅ Virtual type + manual link via SMS | Automated Daily.co link generation | In-app video UI |
| Institution admin portal | ⚠️ Minimum (login, allocate, staff basics) | Full staff mgmt, multi-branch, internal messaging | Enterprise SSO |
| Subscription & payments | ✅ Clinic pays via Paystack, 30-day trial | Tiered/enterprise plans, employer sponsors | Patient-to-institution payments |
| Platform admin | ⚠️ Manual/back-office at MVP | Self-serve plan config, analytics | — |
| Drug-interaction checks | Manual (doctor reads history) | Assisted flags | Automated interaction warnings |

Legend: ✅ in scope · ⚠️ partial/minimum · — later.

---

## 8. MVP Functional Requirements (by Module)

The MVP is organised into nine modules (source: Medra MVP Feature Set).

### Module 1 — Authentication *(foundation)*
- Patient registration (phone number + OTP).
- Institution registration (with document verification — practice licences).
- Doctor registration (phone + **MDCN** number).
- Facility admin login.
- Login and onboarding for all user types.
- Forgot password (OTP reset).
- Role-based redirect after login (patient → home, doctor → dashboard, admin → portal).

### Module 2 — Doctor / Institution Profile & Availability *(the product core)*
- Doctor profile setup: name, specialisation, bio, photo, fee, MDCN.
- Set weekly availability: days, hours, slot duration.
- **Verified badge** — manual process at MVP (Medra verifies MDCN before approving).
- Public doctor/institution profile page (what patients see before booking).

### Module 3 — Patient Search & Booking *(core conversion flow)*
- Search institutions and doctors by specialisation.
- Filter by availability (Today / This Week) and location.
- Doctor profile detail view (photo, bio, fee, verified badge, availability).
- Real-time availability calendar (date picker shows only genuinely open slots).
- Select time slot; select type (in-person or virtual); confirm booking.
- Booking confirmation screen with a **booking reference number**.
- SMS confirmation to patient; in-app notification to doctor of new booking.

### Module 4 — Appointment Management
- **Patient:** view upcoming, view past, cancel (with confirmation step).
- **Doctor / Institution:** dashboard of today's appointments; confirm or decline pending bookings; mark complete; mark no-show. (Institution admin additionally **allocates** a booking to a doctor.)

### Module 5 — SMS Reminders *(biggest no-show reducer)*
- SMS on booking confirmed.
- SMS reminder 24 hours before and 2 hours before.
- SMS on appointment cancelled.

### Module 6 — Basic Medical Record
- **Doctor writes:** presenting complaint, diagnosis (free text, no ICD codes yet), treatment plan, prescriptions (drug, dose, frequency, duration), follow-up date, doctor's comment, and **private notes** (not patient-visible).
- **Patient reads:** timeline of past visits; full record detail view (everything except private notes).

### Module 7 — Telemedicine (Minimal)
- Patient selects "Virtual" as consultation type when booking.
- Confirmation states "Video link will be sent via SMS before your appointment."
- Doctor manually sends the room link via SMS (automated in Phase 2 via Daily.co).

### Module 8 — Subscription & Payments
- 30-day free trial, no card required to start.
- Trial countdown visible in doctor/clinic dashboard.
- **Paystack** subscription (₦___/month, auto-charge after trial).
- Subscription-expired state: doctor/clinic dashboard **locked**; patient side keeps working.
- Payment-confirmation SMS to clinic.

### Module 9 — Settings (Bare Minimum)
- Edit profile (all user types), change password, logout.

---

## 9. Explicitly Out of MVP Scope

| Left out | Reason |
|---|---|
| Full in-app video interface | Daily.co link via SMS works; ship first, automate later. |
| Doctor analytics | No data worth showing at pilot scale. |
| Patient ratings/reviews | No review pool at 3–5 pilot clinics. |
| Multi-language support | English sufficient for Abuja pilot. |
| Offline mode | Complex; unnecessary at this scale. |
| Patient platform fees | Patients pay institutions directly, not the platform, at this stage. |

---

## 10. User Stories & Acceptance Criteria

Format: *As a [role], I want [capability], so that [benefit].* Each story carries acceptance criteria (AC).

### 10.1 Patient
- **P1 — Register:** *As a patient, I want to register with my phone number and an OTP, so that I can access the platform quickly.*
  - AC: Valid Nigerian phone accepted; OTP delivered via SMS; expired/incorrect OTP handled; account created on success; role-redirect to patient home.
- **P2 — Search:** *As a patient, I want to search doctors/institutions by specialisation, location, and availability, so that I find relevant care fast.*
  - AC: Results filter by specialty, location, and Today/This Week; each result shows verified badge, fee, next available slot; empty state when no matches.
- **P3 — View profile:** *As a patient, I want to view a doctor's/institution's profile, so that I can decide before booking.*
  - AC: Profile shows photo, bio, specialisation, fee, verified badge, and real availability.
- **P4 — Book:** *As a patient, I want to pick a real open slot and consultation type, so that I can book before leaving home.*
  - AC: Only genuinely open slots shown; in-person/virtual selectable; confirmation screen shows booking reference; double-booking of the same slot is prevented.
- **P5 — Confirmation & reminders:** *As a patient, I want SMS confirmation and reminders, so that I don't forget or miss my appointment.*
  - AC: SMS on confirm; reminders at 24h and 2h; SMS on cancellation.
- **P6 — Manage appointments:** *As a patient, I want to see upcoming/past appointments and cancel with a confirmation step, so that I stay in control.*
  - AC: Upcoming and past lists; cancel requires explicit confirm; cancellation triggers SMS and frees the slot.
- **P7 — Medical history:** *As a patient, I want a timeline of past visits and full record detail, so that I carry my history without paper.*
  - AC: Chronological timeline; detail view shows complaint, diagnosis, treatment, prescriptions, follow-up, doctor's comment; **private notes never shown**.

### 10.2 Doctor / Private Practitioner
- **D1 — Register & verify:** *As a doctor, I want to register with my MDCN number, so that I can be verified and listed.*
  - AC: MDCN captured at registration; account stays **unverified/hidden** until Platform Admin approves; verified badge appears on approval.
- **D2 — Profile & availability:** *As a doctor, I want to set my profile and weekly availability, so that patients see accurate open slots.*
  - AC: Profile fields (name, specialisation, bio, photo, fee, MDCN); weekly schedule with slot duration; changes reflect in patient-facing calendar.
- **D3 — Daily dashboard:** *As a doctor, I want today's appointment queue, so that I can run my day.*
  - AC: Today's list with patient name, time, type, status; confirm/decline pending; mark complete; mark no-show.
- **D4 — Record at point of care:** *As a doctor, I want the patient's relevant history during consultation and a fast way to write a note, so that I make safe decisions.*
  - AC: Prior visits/prescriptions visible during consult; note captures complaint, diagnosis, treatment, prescriptions, follow-up, comment, private notes; saved to the patient's timeline.
- **D5 — Virtual link:** *As a doctor, I want to send a video link for virtual bookings, so that the consultation can happen remotely.*
  - AC: Virtual bookings flagged; doctor can send room link via SMS (MVP: manual).

### 10.3 Institution Admin
- **A1 — Register & subscribe:** *As an admin, I want to register my institution and choose a plan (single-practice / multi-doctor / multi-branch), so that my clinic can operate on Medra.*
  - AC: Document/licence upload; plan selection by institution size; multi-branch billed as **one** institution; 30-day trial starts without a card.
- **A2 — Allocate bookings:** *As an admin, I want to route incoming bookings to the right doctor (or honour a patient's requested doctor), so that patients are seen appropriately.*
  - AC: Incoming bookings visible; assign to a doctor; patient's doctor preference surfaced; doctor notified.
- **A3 — Manage staff:** *As an admin, I want to add staff with roles/permissions, so that the right people access the right data.*
  - AC: Add/remove staff; assign role; permissions enforced per §6.
- **A4 — Records & messaging:** *As an admin, I want oversight of patient records and internal staff messaging, so that the clinic coordinates internally.*
  - AC: Records management view; internal messaging between staff (form TBD — see §17).
- **A5 — Billing:** *As an admin, I want to see trial countdown and manage subscription/billing, so that service continues uninterrupted.*
  - AC: Trial countdown visible; Paystack subscription; expired state locks staff dashboards while patient side still works; payment-confirmation SMS.

### 10.4 Platform Admin
- **X1 — Approve & verify:** *As a platform admin, I want to approve institutions and verify MDCN numbers, so that only legitimate providers are listed.*
  - AC: Approval queue; MDCN verification step; verified badge granted on approval.
- **X2 — Configure plans:** *As a platform admin, I want to configure subscription plans, so that pricing matches institution size.*
- **X3 — Oversight:** *As a platform admin, I want platform-wide visibility, so that I can monitor activity.* *(Analytics = Phase 2.)*

---

## 11. Key User Journeys

### 11.1 Patient — first booking (the core loop)
1. Register (phone + OTP) → onboarding.
2. Search by specialisation → filter Today/This Week → browse results.
3. Open a verified doctor's profile → review fee, bio, availability.
4. Pick an open slot → choose in-person or virtual → confirm.
5. See confirmation with booking reference → receive SMS.
6. Receive 24h and 2h reminders.
7. Attend (or join virtually via SMS link) → doctor writes note.
8. Read the visit in personal medical history timeline.

### 11.2 Institution — onboarding to first patient
1. Admin registers institution → uploads practice licence → selects plan → 30-day trial starts.
2. Platform Admin verifies documents/MDCN → approves → institution goes live.
3. Admin adds doctors/staff → doctors set availability.
4. Patient books → admin allocates to a doctor (or patient's requested doctor).
5. Doctor sees it on today's dashboard → confirms → consults → records note.
6. Near trial end, admin sees countdown → subscribes via Paystack → payment SMS confirms.

### 11.3 Doctor — a consultation day
1. Log in → land on today's queue.
2. Confirm/decline pending bookings.
3. For each patient: open record → read relevant history → consult → write note (incl. prescriptions & follow-up) → mark complete (or no-show).

### 11.4 Private practitioner — independent enrolment
1. Register (phone + MDCN) → set up profile → set availability → get verified.
2. Appear in patient search as an independent provider.
3. Manage own bookings and patient notes without an institution.

*(Sitemap and per-role flow diagrams are a design deliverable — see §14 and §15.)*

---

## 12. Non-Functional Requirements

### 12.1 Security & privacy *(critical — medical data)*
- **Data protection compliance:** align with the **Nigeria Data Protection Act (NDPA) 2023 / NDPR** — lawful basis, consent capture, data-subject rights, and breach handling. UI must reflect consent and access where required.
- **Access control:** strict RBAC (§6); patients see only their own records; doctors see only assigned patients; private notes never exposed to patients.
- **Access logging / audit trail:** who viewed/edited which record and when (surfaced in UI where relevant).
- **Encryption:** in transit (TLS) and at rest for sensitive fields.
- **Authentication:** OTP-based; session management; password reset via OTP.
- **Consent:** explicit patient consent for record creation/sharing across providers.

### 12.2 Performance & reliability
- Booking flow must feel instant; availability must be **accurate in real time** (no booking of unavailable slots).
- Graceful handling of empty, loading, error, and success states across all screens.

### 12.3 Usability & accessibility
- **Mobile-responsive web** first; designed for low-friction phone use.
- Clear information hierarchy given data density; readable typography; sensible color/contrast (accessibility).

### 12.4 Reliability of integrations
- SMS, payments, and (later) video must fail gracefully with retries and user-visible status.

### 12.5 Scalability
- Data model designed for volume and multi-branch/enterprise growth from day one, even if enterprise features ship later.

---

## 13. Data Model (Conceptual)

Core entities and key relationships (to be detailed in developer-handoff specs):

- **User** (base) → specialises into **Patient**, **Doctor/Staff**, **InstitutionAdmin**, **PlatformAdmin**.
- **Institution** ── has many ──> **Branch**, **Staff (Doctor/Admin)**; ── has one ──> **Subscription**.
- **PractitionerProfile** (doctor or private practitioner): specialisation, bio, photo, fee, MDCN, verification status.
- **Availability**: practitioner → weekly schedule → **Slot** (date/time, duration, open/booked).
- **Appointment**: patient × practitioner × slot; type (in-person/virtual); status (pending/confirmed/declined/complete/no-show/cancelled); booking reference.
- **MedicalRecord / ConsultationNote**: appointment → complaint, diagnosis, treatment plan, **Prescription**(s), follow-up date, doctor's comment, private notes.
- **Subscription**: institution/practitioner → plan, trial end, status (trial/active/expired), Paystack references.
- **Notification / Message**: SMS log + in-app notifications; internal staff messages.
- **AuditLog**: actor, action, target record, timestamp.

> A stated design goal is that the **UI itself communicates this data model to developers** — annotated handoff specs should map screens/fields to entities.

---

## 14. Information Architecture (Sitemap Overview)

- **Patient app:** Onboarding/Auth · Home/Search · Filters · Provider Profile · Booking Flow (slot → type → confirm) · Dashboard (upcoming/past) · Medical History (timeline → detail) · Profile/Settings/Notifications.
- **Doctor/Practitioner view:** Auth/Enrolment · Daily Dashboard/Queue · Patient Record (read + write) · Availability/Calendar · Profile/Settings.
- **Institution Admin portal:** Registration/Plan selection · Admin Dashboard · Booking Management/Allocation · Staff Management · Patient Records · Internal Messaging · Multi-branch view · Subscription/Billing.
- **Platform Admin:** Institution Approval/Onboarding · Plan Configuration · (Phase 2) Analytics.

---

## 15. Design Deliverables

Screen groups expand into individual screens plus states (empty, loading, error, success). Exact counts confirmed once scope is locked.

**Screen groups**
- Patient app/web (auth, search/browse, profile, booking, dashboard, history, settings).
- Institution Admin portal (registration/plans, dashboard, booking/allocation, staff, records, messaging, multi-branch, billing).
- Doctor/Practitioner view (daily dashboard, record view, availability, enrolment).
- Platform Admin (approval/onboarding, plan config, analytics — pending confirmation).

**Supporting deliverables**
- Sitemap & core user-flow diagrams (per role).
- Low-fidelity wireframes (all four roles).
- **Design system** — colors, typography, components, built for reuse across roles (aligned to Medra brand: blue-gradient wordmark + heartbeat-cross mark).
- High-fidelity UI screens.
- Clickable prototype for key flows (booking, admin allocation, patient history).
- Developer-handoff documentation — annotated specs reflecting backend/data structure.

**Indicative design process & timeline** (subject to scope confirmation):

| Phase | Focus | Output | Est. |
|---|---|---|---|
| 1. Discovery & IA | Confirm scope/flows per role; structure IA | Sitemap, user flows | 1–1.5 wks |
| 2. Wireframes | Low-fi layouts, all four roles | Reviewed wireframe set | 1–2 wks |
| 3. UI Design | Design system + hi-fi screens | Full hi-fi screen set | 2–3 wks |
| 4. Prototype & Handoff | Clickable prototype, dev-ready specs | Prototype + handoff doc | ~1 wk |

**Total: ~5–7 weeks** for an MVP-scope first release.

### 15.1 Design progress (as built in Figma)

| Module | Screens | Frames | Figma pages | Status |
|---|---|---|---|---|
| Design system + user journeys | — | 27 | 1 | Done |
| Authentication (all four roles) | 35 | 70 | 4 | Done |
| Member app, batch 1 — Find & Book | 11 | 46 | 2 | Done |
| Member app, batch 2 — Visits · Records · Medicines · Profile | 44 | 108 | 6 | Done |
| Doctor app — full module (rebuilt) | 46 | 239 | 8 | Done |
| Institution admin portal | — | — | — | Not started |
| Platform admin | — | — | — | Not started |

Every screen is drawn at **1440 desktop and 390 mobile**, wired into a clickable prototype with a
motion spec, and validated offline (tokens, icons, images, DSL rules) before rendering.

### 15.2 Product decisions settled by the Member batch-2 designs

These were open questions before the screens existed. They are now decided **on the screen**, and
they need a build and a legal sign-off, not just a design review.

1. **Nothing is shared by default.** A doctor sees a member's history only through an explicit,
   scoped, time-boxed grant: who · what (six categories) · how long (this visit / 24 h / 7 d /
   30 d). Revocation is immediate. Consent is recorded with a timestamp under **NDPA 2023**.
2. **Allergies and current medicines are the one exception** — always visible to any doctor
   treating the member, because the alternative is unsafe prescribing. The consent control for
   them reads as locked rather than pretending to be optional.
3. **The record-access log is append-only.** Every open is logged with who and when, and neither
   the member, the clinic, nor Medra can edit or delete it. It is the member's evidence.
4. **Provenance is on every clinical record.** A consultation note carries the doctor's name,
   **MDCN number**, timestamp and "cannot be edited". Member-uploaded records are labelled
   "added by you", and member-taken vitals are labelled "self-measured", so a clinician can always
   tell what the record is worth.
5. **Account deletion cannot delete clinic-held notes.** Nigerian medical-records retention binds
   the clinic, not Medra. The delete screen states plainly what disappears (profile, uploads,
   preferences, shares) and what is kept (clinic copies, payment records, the anonymised access
   log), with a 30-day grace period and a "pause instead" alternative.
6. **SMS is the floor, not a fallback.** Visit confirmations always go out by SMS even with every
   other channel disabled, and **Medra pays for the messages**. Medicine reminders offer SMS for
   days with no data. This has a real unit cost — model it per active member per month.
7. **Every video visit has a no-data escape hatch.** Pre-call and connection-lost both offer
   "ask the clinic to call my phone", plus a low-data mode (~12 MB per 20 minutes) and
   audio-only. A dropped call never loses the appointment.
8. **Refills need a human.** A doctor approves or declines a refill request and may require a
   visit first. Requests carry a supply length, a collection choice (clinic pharmacy, nearby
   pharmacy, delivery) and an estimated cost.
9. **Dependants are first-class.** One member can hold records and bookings for a child or an
   older relative. A child's account **transfers to them at 18**; an adult must confirm by SMS
   before someone else can manage theirs.
10. **Offline is a designed state, not an error.** Records, reminders and the Medra ID keep
    working from local storage; booking and video explicitly do not, because a stale slot is worse
    than no slot. Queued actions sync on reconnect.

Open items for the pilot clinics: the ₦2,000 late-change fee on reschedules, refill turnaround
(designed as "within a day"), the ₦1,500 delivery fee, and whether plain-language result
explainers are acceptable to the clinical partners as written.

### 15.3 Product review — 1 August 2026 (Godwin Okwor, Abraham Peter, Israel Oni)

Two sessions: a 69-minute walkthrough of the design system, authentication and the member app,
and a 9-minute review of the member profile. Everything raised is now in the designs.

**Authentication and onboarding**
1. **WhatsApp is a verification channel**, offered before SMS — "not a lot of people are using
   SMS ... WhatsApp is faster actually". Member, doctor and institution OTP screens all lead with
   it, and "send it on WhatsApp" is an option on the can't-get-a-code screen.
2. **Name is mandatory**, not skippable — "you don't want to say dear +234 801...".
3. **Age can replace a date of birth.** People often do not know the exact date; the system works
   the year back from an age.
4. **Every member gets a Medra ID** (`MDR-8842-19`). Shown at the end of onboarding with copy and
   QR actions, printed under their name on their profile, on the one-page summary, and accepted as
   a **log-in method**. A doctor can search a card by it when the patient remembers nothing else.
5. **Onboarding captures genotype, height and weight** alongside blood group, allergies and
   long-term conditions — relevant in Nigeria and cheap to ask once.
6. **Doctor specialisation is a platform-managed list** with an "add another" for second
   specialities, wired so the platform admin can extend it.
7. **Doctors choose how patients reach them** — WhatsApp, work email, phone — set during profile
   setup and changeable later.
8. **Institutions**: contact person grouped as its own block (name, role, email, phone), the
   institution type expanded to a managed list, RC number captured for the CAC check, and setup
   can continue while verification is pending.
9. **The institution flow leads with a free month**, everything unlocked, and shows the plan that
   would apply afterwards — with an option to skip the trial and pay now.

**Member app**
10. **Payment happens before the booking is confirmed.** New screen B4: card, transfer, USSD or
    wallet, held by Paystack, refunded in full if the doctor cancels or does not show.
11. **Search around an address you type**, not only your live location — "some people would not
    want to use their live address ... to look for care around their house while at work".
12. **The undisclosed-history question is asked at booking** and again by the doctor in the
    consultation. What was asked and what was answered is stored with the visit, so it is never
    later unclear what the doctor did and did not know.
13. **Reminder channels are in-app, WhatsApp, SMS and email**, chosen per event.
14. **Virtual visits use the doctor's own meeting link for the MVP** — Google Meet or Zoom,
    embedded in the Join button. The in-app video screens stay in the file, marked **PHASE 2**.
15. **Who-has-access is a selectable list** — revoke one, revoke selected, or revoke everything.
16. **The one-page summary is a printable log the member composes**: blood group and allergies
    always on, everything else opt-in, with a QR code back to the full record.
17. **Deleting an account takes four steps** — a reason, typing DELETE, a code to your phone, and
    an explicit acknowledgement — because "people prefer to just leave their account" and the
    ones who do delete should mean it.
18. **The notification bell opens a panel** with the five most recent, and a "View all" into the
    full screen.
19. **Dependants: two free, then a family plan.** ₦3,000/month for up to six people, or ₦1,500 per
    extra person — "they can book for two people first for free, then from the third they pay",
    so the value is felt before it is charged. Figures are indicative.

**Also fixed in this round, found while measuring rather than in the review:** every one of the
70 authentication frames and 5 design-system frames still used `wrap="wrap"`, which figma-ds-cli
ignores — the same defect that made the member module render badly in Figma. All 297 frames across
the five bundles are now clean, and the validator rejects it permanently.

**Still open, by agreement:** a medical doctor reviews the clinical screens before build; legal
opinion on what an institution must supply at verification; a drug-reference API for prescribing;
and confirmation of the commission and family-plan prices with the pilot clinics.

### 15.4 Doctor module — second pass

The first doctor build was judged too basic, with mobile screens carrying less than desktop and
a look too close to the member app. It was rebuilt rather than patched.

**A separate visual system.** The doctor app is structurally a different product: the whole app
is a **white card floating on a soft blue canvas** with **three columns** — a 206px labelled navy
sidebar, the main column, and a **292px light right rail** holding a month calendar, what is next
and what is already done — against the member app's full-bleed two columns. Corners are 14–18px
inside a 28px card, the palette adds a **warm coral/amber** alongside the brand teal for counts
and attention, and on mobile the chrome is a **floating brand-gradient header card** with a
raised centre action in the tab bar. It is recognisable as a different product at a glance, on
the same brand.

**Mobile parity.** Every mobile screen now carries the same cards as its desktop twin, with the
desktop side-rail folded in underneath and the panel's key numbers absorbed into the header.
They are scrolling frames; what is guaranteed is no horizontal overflow at 390 and the primary
action inside the first viewport.

**Requirements this pass closed that the first build had missed:**
- **Confirm or decline a booking request** (§7 Module 4, §10.2 D3) — screen K2.
- **Mark complete or no-show** (§7 Module 4) — screen K5, with the fee, slot and record
  consequences stated.
- **The PRD's exact note fields** (§7 Module 6): presenting complaint, examination, diagnosis,
  treatment plan, doctor's comment and **private notes** — screen C1, with per-field share
  switches on C7.
- **Send the room link for a virtual booking** (§7 Module 7, D5) — screen C10, with proof of
  delivery on three channels and four fallbacks.
- **Subscription, 30-day trial countdown, Paystack, and the expired-locked state**
  (§7 Module 8) — screens S6 and X1.
- **The independent practitioner who has no institution** (§11.4) — screen S7.

**AARRR on the supply side**, which had no representation at all before: acquisition (booking
link, waiting-room QR poster, patient import, colleague invitations), activation (a setup
checklist with a real "you are not bookable yet" gate), retention (recall and follow-up lists,
messages, insights, reviews), referral (invite a colleague, refer a patient onward), and revenue
(fees, payouts, subscription).

**Edge cases now designed:** running late · no-show with a fee split · doctor cancels · video
fails · unpaid slot released · booking declined with a refund · time off with patients already
booked · handing patients to a colleague · an allergy blocking a prescription · an out-of-range
result held back · a refill that should be a visit · an unsigned note · a note recovered after a
crash · offline with queued writes · a service error mid-consultation · trial expiry and lock ·
a shared clinic machine left signed in · a patient declining an access request.

**One contradiction this surfaced, needing a decision before build.** §4 of this document says
practitioners pay a **subscription** and patients pay providers **directly**. The 1 August review
added **payment before booking**, which means Medra collects the fee and pays the doctor out.
Both are now designed — S6 for the subscription and trial, S5 for payouts — and S2 states that
Medra earns from the subscription rather than a commission. If the answer is "both", that needs
justifying to doctors, because it is two charges on the same transaction.

Still open by agreement: a medical doctor reviews every clinical string before build; the 50%
no-show split is a pilot policy; referral rewards are indicative; the institution admin portal
and a lab technician's own screen are separate modules.

### 15.5 Doctor module — third pass: the reference direction, and a prototype that holds

The product owner approved the second pass's structure and asked for the warmth of a reference
dashboard, and for the screens to be prototyped rather than merely drawn.

**The reference direction.** The floating card, the pastel two-letter code chips (`Rx` `Lab`
`Ref` `Note`), the donut, the per-patient progress bars, the media table and the month calendar
in the right rail all come from it. The structure — three columns, a floating card — is what
keeps the doctor app distinct from the member app; the reference supplied the warmth, not the
information architecture.

**The prototype is now audited, not assumed.** A new offline check (`tools/figma/proto_check.py`)
reads the frames off disk, walks the transition table and reports unreachable screens, broken
hotspots and unwired controls. Its first run found real defects, all now fixed:

- **45 transitions pointed at hotspots that did not exist** — mostly on mobile, where the
  affordance had simply not been drawn. That is the same "mobile carries less than desktop"
  complaint, showing up as broken links rather than as missing content.
- **Four of the eight sidebar destinations had no mobile route at all.** A phone tab bar carries
  five; Schedule, Consults, Money and Growth had none. A new screen, **K9 "Everything"**, is the
  fifth tab and now the only mobile route to them; on desktop the same directory is what the
  app-grid button in the top bar opens.
- **S8 Account & Security was unreachable** — nothing linked to it. So were four of the six
  States screens, which happen because of a condition rather than a tap; each now carries a
  small state switcher, explicitly labelled as a review control rather than product.
- **Every page had one flow starting point, on desktop only**, so the mobile row was not a
  prototype at all. Each page now declares two.

Current state: **116 frames, 46 screens at both breakpoints, 92 of 92 reachable, 626 explicit
transitions and 1,196 navigation links, no broken hotspots, no horizontal overflow at 390 or
1440.** The flows are documented in `figma/medra-doctor/PROTOTYPE.md`.

**One judgement made in the process.** Where a desktop right-rail section would only repeat what
the mobile main column already said — "Next up" on a screen that already lists the queue — it is
left out rather than folded in. Parity means the same information is reachable, not that every
desktop container is duplicated; the difference is roughly 900px of scroll on the busiest screen.

Nothing outside the doctor module was created, edited or re-rendered; the design-system,
authentication and member pages are untouched, and `CLI-PROMPT.md` states that constraint to the
terminal that renders into Figma.

### 15.6 Doctor module — fourth pass: density

The product owner accepted the coverage and the direction, and raised the remaining problem:
the screens were overloaded, mobile especially. That was true and measurable — the average
mobile screen was two full viewports of stacked cards and the busiest was five, because every
desktop card had been folded into one column. Completeness is not legibility.

**Mobile is now hub → section → sheet.**

| | What it is |
|---|---|
| **Hub** | The header numbers, the one thing you act on now, and a short list of ways in. Nothing else. |
| **Section** | One subject, one screen, opened by tapping a row on the hub. Back always returns to the hub. |
| **Sheet** | One decision, over a dimmed hub — quick actions, *Add to this visit*, *Change this week*. Anything with its own scroll is a section, not a sheet. |

Nothing was removed. Every card is still in the bundle, one tap away, with a count on the hub row
so the hub still tells you the shape of the day without unrolling it. The pattern is generated
rather than hand-assembled: a screen declares its sections and sheets and the builder emits the
frames, the rows that open them, the way back and the motion class — which is why 169 mobile
frames carry no hand-written wiring.

**Desktop got a budget, not a rewrite:** at most two groups per column, lists capped at four rows
with a *See all N* row pointing at the screen that owns the full list, and anything beyond that
moved to the right rail or to where it belongs.

| | Third pass | Fourth pass |
|---|---|---|
| Tallest mobile screen | 4,096px (≈5 viewports) | **1,467px** |
| Median mobile screen | ~1,750px | **844px — one viewport** |
| Tallest desktop screen | 1,691px | **1,365px** |
| Frames | 116 | **239** (46 desktop screens, 169 mobile frames, 24 component states) |
| Prototype | 92/92 reachable | **215/215 reachable**, 906 explicit links, 0 broken hotspots |

The prototype audit was extended with it: the transition table now describes a *screen* rather
than a frame, and each entry is attached to whichever frame of a mobile family actually carries
the control, found by scanning the generated frames at build time. A hotspot that exists nowhere
in the family fails the build.

---

## 16. Brand & Design Direction

- **Name:** Medra. **Logo:** stylised "M" script paired with a **heartbeat/cross** medical mark; **blue gradient** (deep navy → teal) as the primary identity color.
- Deliver a reusable design system (colors, typography, components) consistent across all four portals.
- Tone: trustworthy, clinical-yet-approachable; clarity prioritised over decoration given data density and sensitivity.

---

## 17. Integrations & Technical Considerations

| Concern | MVP approach | Notes / Phase 2 |
|---|---|---|
| **SMS** (OTP, confirmations, reminders, video links) | SMS gateway (e.g. Termii/Twilio — confirm provider) | Single biggest no-show reducer; needs delivery-status handling. |
| **Payments** | **Paystack** subscription; auto-charge after 30-day trial | Tiered/enterprise plans; possibly employer-sponsored billing later; patient-to-institution payments later. |
| **Telemedicine** | Manual room link via SMS | Automate **Daily.co** link generation in Phase 2; in-app video later. |
| **MDCN verification** | Manual verification by Platform Admin before approval | Explore automated MDCN lookup later. |
| **Platform** | Mobile-responsive web | Native apps to confirm as a later decision. |
| **Data/compliance** | NDPA/NDPR-aligned storage, audit logging, consent | See §12.1. |

---

## 18. Monetisation & Pricing Model

- **Who pays:** Institutions and independent practitioners (subscription). **Members** (people
  using Medra for their own care) use the platform **free**; they pay institutions directly for
  services rendered.
- **Sizing before pricing:** onboarding asks for **practitioners, branches, admin seats and
  monthly patient volume**, then recommends a plan. Every input stays editable on the pricing
  screen, and the price recalculates live.

### 18.1 Plans (indicative — validate with pilot clinics)

| Plan | Price / month | Includes |
|---|---|---|
| **Starter** | **₦45,000** | 1 practitioner · 1 branch · core booking & records |
| **Practice** | **₦120,000** | Up to 10 practitioners · 1 branch · staff roles & allocation |
| **Group** | **₦280,000** | Up to 30 practitioners · up to 3 branches · analytics |
| **Enterprise** | **Custom** | Unlimited practitioners & branches · SSO · dedicated support |

- **Add-ons:** +₦8,000 per extra practitioner/month · +₦25,000 per extra branch/month.
- **Annual billing:** pay for 10 months, get 12 (**2 months free**).
- **Trial:** 30-day free trial on every plan, **no card required**; countdown visible in the portal.
- **Worked example:** 8 practitioners across 2 branches → Practice (₦120,000) + 1 extra branch
  (₦25,000) = **₦145,000/month**.
- **Expired state:** staff/clinic dashboards lock; the member side keeps working.
- **Multi-branch** is billed as **one institution**, never per branch account.
- **Future revenue:** paid add-ons, employer-sponsored plans, automated telemedicine.

> Prices are a starting point for the Abuja pilot and should be tested against willingness-to-pay
> before launch; the plan **structure** (size-based tiers + per-practitioner/branch add-ons) is the
> durable decision.

## 19. Assumptions, Dependencies & Constraints

**Assumptions**
- Pilot is **3–5 private clinics in Abuja**; English-only; mobile-responsive web is sufficient for MVP.
- Platform Admin role exists and performs manual verification/approvals.
- Institutions accept manual MDCN verification during MVP.

**Dependencies**
- Reliable SMS delivery in Nigeria; Paystack availability; Daily.co (Phase 2); MDCN as the doctor-identity source of truth.

**Constraints**
- Budget/timeline still being finalised (team being assembled); scope must stay MVP-tight.
- Medical-data sensitivity imposes security/compliance overhead from day one.

---

## 20. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Availability data is stale** → patients book unavailable slots | Erodes core value | Real-time slot locking; single source of truth for availability; conflict prevention on booking. |
| **Data breach / privacy failure** | Severe (legal + trust) | NDPA/NDPR alignment, RBAC, encryption, audit logging, consent capture from MVP. |
| **SMS undelivered** | Missed reminders, no-shows | Delivery-status tracking, retries, in-app fallback notifications. |
| **Low clinic adoption after trial** | Revenue risk | Tight onboarding, visible value (no-show reduction), consultative pricing. |
| **Scope creep beyond MVP** | Slips launch | Enforce §9 "out of scope"; phase the roadmap. |
| **MDCN verification bottleneck** | Slow onboarding | Clear manual SOP now; automate later. |
| **Ambiguous staff-role permissions** | Wrong data access | Resolve nurse/receptionist/lab-tech roles before finalising RBAC. |

---

## 21. Roadmap (Phased)

- **Phase 1 — MVP (this PRD):** Modules 1–9; manual telemedicine link; Paystack trial→paid; basic records; Abuja pilot.
- **Phase 2:** Automated Daily.co links; rescheduling/waitlists; fuller admin portal (staff mgmt, multi-branch, internal messaging); doctor analytics; assisted drug-interaction flags; tiered/enterprise plans.
- **Phase 3+:** In-app video UI; employer-sponsored plans; patient-to-institution payments; record attachments/lab results/ICD codes; ratings/reviews; multi-language; offline; interoperability/exports.

---

## 22. What You Might Be Missing — Gaps & Recommendations

A candid list of things not fully addressed in the brief/scope/MVP that typically bite medical platforms. Prioritised.

**A. Compliance & legal (highest priority)**
- **NDPA 2023 / NDPR compliance** and a written data-protection/privacy policy, patient consent flows, and data-subject rights (access, deletion). Medical data is high-risk; build this into MVP, not later.
- **Terms of Service, provider agreements, and liability/disclaimer** language — especially around telemedicine and clinical decisions made using Medra records. Consider professional-indemnity implications.
- **Data residency & retention policy** — where records are stored and for how long.

**B. Clinical safety**
- The **drug-interaction goal from the brief is currently manual** (doctor reads history). Flag explicitly that automated interaction checking is a later phase, and ensure the record UI makes current medications prominent so a doctor *can* catch clashes.
- **Allergies and chronic conditions** aren't in the basic record fields — consider adding an "allergies / known conditions / current medications" summary block, as it's the highest-value safety data at a glance.
- **Emergency/critical info** — blood group, emergency contact.

**C. Product/UX gaps**
- **Rescheduling** (not just cancel) — patients will want it; currently Phase 2. Confirm that's acceptable for pilot.
- **Overlap/double-booking prevention** and slot-locking under concurrency — call it out as an explicit requirement, not an assumption.
- **Time zones / clock source** — trivial for Abuja-only, but define now to avoid reminder bugs.
- **No-show and cancellation policy** — who bears the cost, and does it affect the patient's ability to rebook?
- **Notifications beyond SMS** — email and in-app; SMS-only is fragile if delivery fails.
- **Search when nothing matches** — empty-state and "notify me when available" behavior.
- **Patient identity uniqueness** — one person, one medical record across institutions; how do you de-duplicate patients (phone number as key has edge cases — shared phones, changed numbers)?

**D. Operations & trust**
- **MDCN verification SOP** — a documented manual process (who, SLA, evidence stored) so onboarding isn't a bottleneck and the "verified badge" is trustworthy.
- **Institution offboarding / subscription-expiry data handling** — what happens to patient records when a clinic leaves? (Patients arguably own their history — clarify.)
- **Support & feedback channel** — how patients/clinics report problems during pilot.
- **Backups & disaster recovery** for medical data.

**E. Commercial**
- **Pricing is undefined** (₦___). Pilot needs at least a working number and a plan-by-size matrix to test willingness-to-pay.
- **Employer-sponsored plans** (raised on the call) — decide in/out for pilot; likely Phase 2.
- **Virtual-consultation payment reconciliation** — some clinics charge for online consults up front; that conflicts with "patients pay institutions directly" and may force an early payment touchpoint.

**F. Analytics & measurement**
- Even if doctor-facing analytics are out, **instrument the product** from day one (funnel events, no-show rates, activation) so you can prove the MVP thesis and price confidently. This is measurement infrastructure, not a user-facing feature.

**G. Design-system & handoff**
- The stated goal that **"the UI communicates the data model to developers"** should be an explicit handoff deliverable: annotated specs mapping each screen/field to a data entity, plus all screen **states** (empty/loading/error/success). Make sure this is scoped and estimated.

---

## 23. Glossary

- **MDCN** — Medical and Dental Council of Nigeria (doctor licensing/identity).
- **NDPA / NDPR** — Nigeria Data Protection Act 2023 / Regulation.
- **Paystack** — payment processor for the clinic subscription.
- **Daily.co** — video infrastructure (Phase 2 telemedicine automation).
- **RBAC** — Role-Based Access Control.
- **Institution / Enterprise** — a clinic/hospital; enterprise = multi-branch billed as one.
- **Verified badge** — visible marker that Medra confirmed a provider's MDCN/licence.

---

