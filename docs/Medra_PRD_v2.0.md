# Medra — Product Requirements Document (PRD)

**A unified medical records & consultation-booking platform for Nigeria**

| | |
|---|---|
| **Product** | Medra |
| **Document type** | Product Requirements Document (PRD) |
| **Version** | **v2.0** |
| **Status** | Draft for review |
| **Owner** | Godwin Okwor (Product) |
| **Contributors** | Israel Oni (UI/UX Design) |
| **Launch market** | Abuja, Nigeria (pilot) |
| **Date** | 10 August 2026 |
| **Supersedes** | v1.0 (23 July 2026) |
| **Related docs** | UI/UX Design Brief (10 Jul 2026) · Product review (1 Aug 2026) · **Second product review (9 Aug 2026)** · UI/UX Design Scope · Medra MVP Feature Set |

---

## 0. Version history

| Version | Date | What changed |
|---|---|---|
| v1.0 | 23 Jul 2026 | First full PRD. Three roles in practice — member, doctor, institution admin. Booking loop, records, subscription. |
| **v2.0** | **10 Aug 2026** | **The 9 August review changed the shape of the product, not just the screens.** Five changes carry structural weight: (1) the **clinical chain** — nurses, lab technicians and pharmacists are first-class roles, because a doctor consumes work other people produce; (2) the **organisation module** is specified, with departments rather than individuals as the unit of onboarding and billing; (3) **self-reported health data is marked unverified** and stays marked until a clinician or lab vets it; (4) **external parties reach a record through a scoped, single-use link**, so a lab that is not on Medra can still return a result; (5) **identity widens** — NIN, mandatory date of birth, NHIS and private insurance. §24 records the decisions and the questions still open. |

### What v2.0 does *not* change

The member-owned record was already the spine of v1.0 and the review ratified it: the member is
the connector between institutions, not the institution. Booking, availability, consultation
notes, consent-scoped sharing, the subscription model and the design language all stand. The
existing 439 rendered frames are extended and retrofitted, not discarded — §15.7 lists exactly
what has to change and what does not.

---

## 1. Executive Summary

Medra is a mobile-responsive web platform that digitises how Nigerians find care, book consultations, and carry their medical history. Today most private hospitals in Nigeria run on paper filing and WhatsApp/phone booking. There is no shared medical database, so a patient's history lives on paper they must physically carry between doctors — creating avoidable risks such as clashing drug prescriptions, and wasted trips to unavailable doctors.

Medra solves this in four layers:

1. **A member-facing booking experience** — find a verified doctor or institution, see real availability, and book (in-person or virtual) before leaving home.
2. **A hospital/clinic operating system** — a shared database that institutions use internally to manage bookings, allocate work across departments, hold records, and communicate between staff.
3. **The clinical chain** — nurses, lab technicians and pharmacists enter the work they actually do, so the doctor reads a prepared record instead of typing one. A platform that models only doctors either loses that data or turns the doctor into a data-entry clerk; both destroy the reason to use it.
4. **A portable medical history** — each member owns a continuous, structured record (diagnoses, prescriptions, results, recommendations) that any authorised clinician can read to make safer decisions, with every fact carrying whether it has been **medically verified** or merely self-reported.

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

**Nine roles.** v1.0 had five and flagged the gap as an open item; the 9 August review closed it.
RBAC is a core, security-sensitive requirement because of medical-data sensitivity.

| Role | What it is | Why it exists |
|---|---|---|
| **Member** | A person using Medra for their own care and their dependants' | Owns the record; the connector between institutions |
| **Doctor / Medical practitioner** | Consults, diagnoses, prescribes, refers, signs | The clinical decision |
| **Nurse** | Vitals, injections, dressings, observations, prep before and after a consultation | Produces most of what a doctor reads. Without this role, either the data is lost or the doctor types it |
| **Lab technician** | Runs ordered tests and returns structured results | Results are the second-largest thing in a record after notes |
| **Pharmacist / dispensary** | Dispenses against a prescription, records what was actually given | Closes the loop between prescribed and taken |
| **Front desk / receptionist** | Registers walk-ins, checks people in, manages the day's queue, takes payment | The first and last person a patient meets |
| **Organisation admin** | Onboards the organisation, its branches, departments and staff; manages seats and billing | The buyer |
| **Independent practitioner** | A doctor with no institution behind them | §11.4 — a large share of the Abuja pilot |
| **Platform admin** | Verifies organisations and practitioners, configures plans | Medra's own back office |

### 6.1 Permission matrix

| Capability | Member | Doctor | Nurse | Lab tech | Pharmacist | Front desk | Org admin | Platform admin |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Browse providers, book, cancel own visit | ✅ | — | — | — | — | ✅ (on behalf) | — | — |
| View **own** record | ✅ | — | — | — | — | — | — | — |
| View a member's record | — | ✅ scoped | ✅ scoped | ⚠️ order only | ⚠️ prescription only | ❌ | ❌ | — |
| Write consultation note, diagnose, prescribe, refer, **sign** | — | ✅ | — | — | — | — | — | — |
| Record vitals and observations | — | ✅ | ✅ | — | — | — | — | — |
| Administer and record an injection or procedure | — | ✅ | ✅ | — | — | — | — | — |
| Receive a test order; enter a **structured result** | — | — | — | ✅ | — | — | — | — |
| Release a result to the member | — | ✅ | — | ❌ | — | — | — | — |
| Dispense against a prescription; record what was given | — | — | — | — | ✅ | — | — | — |
| Register a walk-in, check in, take payment | — | — | — | — | — | ✅ | ✅ | — |
| Allocate a booking to a practitioner | — | — | — | — | — | ✅ | ✅ | — |
| Create a **scoped external-access link** | — | ✅ | — | — | — | — | ✅ | — |
| Manage departments, seats and staff | — | — | — | — | — | — | ✅ | — |
| Manage subscription and billing | — | ✅ (own) | — | — | — | — | ✅ | — |
| Verify organisations and practitioners | — | — | — | — | — | — | — | ✅ |
| Platform-wide analytics | — | — | — | — | — | — | — | ✅ |

Legend: ✅ full · ⚠️ limited to the task in hand · ❌ explicitly denied · — not applicable.

Two denials are deliberate and worth stating plainly, because they are the ones a clinic will
push back on:

- **Front desk cannot read clinical content.** They register, schedule, check in and take money.
  Giving the busiest, highest-turnover seat in the building a window into diagnoses is the
  fastest way to lose a member's trust and breach the NDPA.
- **A lab technician cannot release a result to a member.** They enter it; a doctor releases it.
  An out-of-range value arriving on a phone with nobody to explain it is a harm, not a feature.

### 6.2 Scope of access, and how it ends

Access is granted **per episode of care**, not per person and not forever. A nurse assigned to
today's clinic sees today's patients; access ends when the visit is marked complete. Every read
is logged and visible to the member (§12).

---

## 7. Scope Overview — MVP vs. Future

Medra's full vision spans four portals. The **MVP** ships a mobile-responsive web app focused on the patient booking loop plus the minimum records and clinic tooling to be useful.

| Area | MVP | Phase 2 | Phase 3+ |
|---|---|---|---|
| Patient booking | ✅ Full core flow | Rescheduling, waitlists | — |
| Doctor availability & dashboard | ✅ | Analytics | — |
| Medical records | ✅ Basic structured note | Attachments, lab results, ICD codes | Interoperability/exports |
| Telemedicine | ✅ Virtual type + manual link via SMS | Automated Daily.co link generation | In-app video UI |
| **Organisation portal** | ✅ Onboarding, verification, departments, seats, allocation, billing | Multi-branch analytics, internal messaging | Enterprise SSO |
| **Clinical chain** (nurse, lab, pharmacy) | ✅ Task-scoped apps for each | Inventory, rostering | Device integration |
| **External access link** | ✅ Scoped, single-use, consent-gated | Two-way messaging with the external party | Partner API |
| **Verification state** on health data | ✅ Marked everywhere it appears | Bulk verification at a visit | Automated lab attestation |
| **Insurance** | ✅ NHIS and private insurer captured on the profile | Eligibility check with partners | Claims submission |
| Subscription & payments | ✅ Clinic pays via Paystack, 30-day trial | Tiered/enterprise plans, employer sponsors | Patient-to-institution payments |
| Platform admin | ⚠️ Manual/back-office at MVP | Self-serve plan config, analytics | — |
| Drug-interaction checks | Manual (doctor reads history) | Assisted flags | Automated interaction warnings |

Legend: ✅ in scope · ⚠️ partial/minimum · — later.

---

## 8. MVP Functional Requirements (by Module)

The MVP is organised into **thirteen** modules. Modules 1–9 come from the original MVP Feature Set; **Modules 10–13 were added in v2.0** after the 9 August review and are the reason this version exists.

### Module 1 — Authentication & identity *(foundation)* — **revised in v2.0**
- Member registration (phone or email + OTP, or Google).
- Doctor registration (phone + **MDCN** number + **NIN**).
- **Organisation registration** — see Module 10.
- Staff registration — invited into an organisation by its admin, never self-serve into a
  clinical role (Module 10.3).
- Login and onboarding for all user types; forgot password (OTP reset).
- Role-based redirect after login.

**v2.0 identity changes.** Nigeria's population makes name collisions common, and a medical
record attached to the wrong person is the worst failure this product can have. So:

| Field | Who | Rule |
|---|---|---|
| **NIN** | Doctors **and** members | Captured at onboarding. Second identifier alongside MDCN for a doctor, and the strongest one a member has |
| **Date of birth** | Members | **Mandatory, full date.** An age-only fallback was proposed and rejected — age is not an identifier and decays |
| **Medra ID** | Members | Fixed minimum length so IDs cannot collide as the population grows; short enough to read aloud over a phone |
| **NHIS number** | Members | Optional. Used where a partner institution accepts it |
| **Private insurance** | Members | Optional: insurer + policy number |
| **RC number + organisation licence** | Organisations | **Both.** See Module 10.1 |

**Data-privacy clause.** Doctors and organisations must accept an explicit data-privacy
undertaking during onboarding — not a link in a footer, a step they cannot skip, recorded with
a timestamp and the version of the text they accepted. This is what makes a later breach a
breach of something they signed, and it is a condition of the NDPA 2023 posture in §12.

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

### Module 10 — Organisation onboarding & administration *(new in v2.0)*

**10.1 Registration and verification**
- Organisation name, type (hospital · clinic · diagnostic laboratory · pharmacy · multi-service).
- **RC number** (CAC) **and** **organisation practice licence number** — both are required. An RC
  number alone proves a company exists, not that it may practise medicine; anyone determined
  enough can register a company. The licence is the clinical credential.
- Documents uploaded for review: CAC certificate, organisation practice licence, and any further
  registration a medical organisation of that type must hold. *(Open: the definitive document
  list per organisation type — §24.)*
- **A named contact person signs up on behalf of the organisation** — typically the admin or the
  front-desk lead. Their own details are captured and they are verified as an individual too,
  because they will hold the most privileged seat in the account.
- Verification is by a person at Medra, as with practitioners. Until it completes, the
  organisation can continue filling in details but cannot receive bookings.

**10.2 Sizing, which drives the plan**
Asked once, at onboarding, and editable afterwards: number of practitioners · number of branches
or locations · number of front-desk staff · average patients per month. These size the plan
rather than gate the product; every input stays adjustable on the pricing screen and the price
recalculates live.

**10.3 Departments are the unit, not individuals**
A hospital does not want to onboard a lab technician; it wants to onboard **the laboratory**.
An organisation creates **departments** — laboratory, pharmacy, nursing, front desk, and one per
clinical specialty — and buys **seats** within them. Staff are invited into a department and
inherit its role and permissions. This matters commercially as well as structurally: the price
follows practitioners, branches and seats, so the unit of billing and the unit of administration
are the same thing.

A **standalone laboratory or pharmacy** registers as an organisation whose only department is
that one. Nigeria has high-quality independent labs that are not attached to a hospital, and a
doctor referring out to one is a normal event, not an edge case.

**10.4 What the admin does day to day**
Allocate bookings to practitioners · add, suspend and remove staff · move a seat between people ·
see the day across branches · manage the subscription and invoices · hold the organisation's
public profile.

### Module 11 — The clinical chain *(new in v2.0)*

A doctor consumes work other people produce. The vitals were taken by a nurse, the blood drawn
and run by a laboratory, the drug handed over by a pharmacist. v1.0 modelled only the doctor,
which left two bad options: lose that data, or make the doctor type it. Neither is acceptable —
"you cannot jump one, two, three and just do the doctors."

Each role gets a **task-scoped app**, not a copy of the doctor's:

| Role | Sees | Does |
|---|---|---|
| **Nurse** | Today's assigned patients, the reason for each visit, standing orders | Record vitals · administer and record injections and procedures · pre-consultation prep · post-consultation observations · flag anything urgent to the doctor |
| **Lab technician** | Only the orders addressed to their department, and only the clinical detail attached to each | Accept an order · enter a **structured result** · attach the raw report · mark done |
| **Pharmacist** | Only prescriptions directed to them | Dispense · record what was actually given and when · flag a substitution or a stock-out back to the prescriber |

**11.1 Structured results, not prose**
A result is entered against a **template per test**: analyte, value, unit, reference range. The
technician fills numbers into a form, not a paragraph. This is what makes a value trendable, what
lets Medra flag out-of-range without reading English, and what makes a result from Lab A
comparable with one from Lab B. Free text is available for a comment, never for the values.

**11.2 The order is the unit of work**
A doctor raises an order (test, injection, dispense). It appears in exactly one department's
queue, carries only the clinical detail that department needs, and is closed by the person who
does it. The record shows who ordered, who performed, and when — which is also the audit trail.

### Module 12 — External access: the scoped, single-use link *(new in v2.0)*

Most Nigerian labs and clinics will not be on Medra on day one, and a referral to one must not
force the member back to carrying paper. So a doctor (or an organisation admin) can generate a
**scoped public link or QR code** for a single external party.

- **The member consents before it exists.** No link is created without it.
- **The creator selects exactly what the other side may see** — the reason for the referral, the
  tests to run, and nothing else. The default is the minimum.
- **On opening, the external party sees a privacy notice** naming the member, what they are being
  given access to, and the undertaking they are accepting. They continue only by accepting it.
- **They can upload the result** against the same structured template a Medra lab would use.
- **The link expires the moment they mark it done** — single-use, not a standing door. It also
  expires on a timer if nothing happens.
- **The address is short and typable** — of the form `medra.ng/s/<random token>` — so it can be
  read over a phone or written on a referral slip. A link nobody can type is a link nobody uses,
  and the whole point is that it must be easier than the paper route it replaces. **The token is
  random and never the member's Medra ID**; an earlier draft used the ID, which made every link
  guessable by counting. See §15.1.

This is also the acquisition path for the labs themselves: an organisation that keeps receiving
these links can onboard properly and stop using them.

### Module 13 — Verification state on health data *(new in v2.0)*

Members may enter their own blood group, genotype, weight, allergies and long-term conditions.
Many people in Nigeria have been told their blood group rather than tested for it.

- Self-entered clinical facts are labelled **"Not medically verified"** — on the member's own
  dashboard, and everywhere the value travels, including into another hospital's view.
- The label is **part of the datum**, not a badge on one screen. A value that arrives somewhere
  without its provenance is worse than no value.
- Only a **clinician or a lab result** flips it to verified, and the record keeps who verified it
  and when.
- These fields stay **optional** at onboarding, with an explicit "I'll do this later" — a large
  share of members genuinely do not know their genotype, and forcing a guess manufactures exactly
  the false data this rule exists to prevent.

The reasoning is worth preserving verbatim from the review: if a member says group A because a
parent once told them so, and Medra shows that to a surgical team as fact, the harm and the
liability are Medra's. **Medra must never project unverified data as verified.**

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

- **User** (base) → specialises into **Member**, **Doctor**, **Nurse**, **LabTechnician**,
  **Pharmacist**, **FrontDesk**, **OrgAdmin**, **PlatformAdmin**. Identity carries **NIN**;
  members also carry **date of birth** (required) and **Medra ID**.
- **Organisation** ── has many ──> **Branch**, **Department**, **Seat**, **StaffMembership**;
  ── has one ──> **Subscription**; ── holds ──> **RC number**, **licence number**, **documents**,
  **verification status**.
- **Department** (laboratory · pharmacy · nursing · front desk · a clinical specialty) ── has
  many ──> **Seat**. A **StaffMembership** binds a User to a Department and carries the role. It
  is the membership that grants permission, never the person.
- **Order** (test · injection/procedure · dispense): raised by a Doctor → routed to one
  Department → performed by a StaffMembership. Carries only the clinical detail that department
  needs. Status: raised → accepted → done, with actor and timestamp at each step.
- **LabResult**: order → **ResultTemplate** (analyte, unit, reference range) → values, plus an
  optional attachment and comment. Released to the member only by a Doctor.
- **HealthFact** (blood group, genotype, weight, allergy, long-term condition): value +
  **VerificationState** (self-reported | verified) + verifier + verified-at. The state travels
  with the value into every view, internal or external.
- **Insurance**: member → NHIS number and/or private insurer + policy number.
- **ExternalAccessGrant**: created by a Doctor or OrgAdmin, consented to by the Member, scoped to
  a named set of records and one task; short public URL; accepted-privacy-notice record;
  single-use; expiry on completion and on a timer.
- **PrivacyUndertaking**: user or organisation → text version, accepted-at, IP. Required at
  onboarding for doctors and organisations.
- **PractitionerProfile** (doctor or private practitioner): specialisation, bio, photo, fee, MDCN, **NIN**, verification status.
- **Availability**: practitioner → weekly schedule → **Slot** (date/time, duration, open/booked).
- **Appointment**: patient × practitioner × slot; type (in-person/virtual); status (pending/confirmed/declined/complete/no-show/cancelled); booking reference.
- **MedicalRecord / ConsultationNote**: appointment → complaint, diagnosis, treatment plan, **Prescription**(s), follow-up date, doctor's comment, private notes.
- **Subscription**: institution/practitioner → plan, trial end, status (trial/active/expired), Paystack references.
- **Notification / Message**: SMS log + in-app notifications; internal staff messages.
- **AuditLog**: actor, action, target record, timestamp.

> A stated design goal is that the **UI itself communicates this data model to developers** — annotated handoff specs should map screens/fields to entities.

---

## 14. Information Architecture (Sitemap Overview)

- **Member app:** Onboarding/Auth · Home/Search · Filters · Provider Profile · Booking Flow (slot → type → confirm) · Visits (upcoming/past) · Records (timeline → detail, with verification state) · Medicines · Profile/Settings/Insurance/Notifications.
- **Doctor app:** Auth/Enrolment · Today's queue · Patient record (read + write) · Consultation (note, prescribe, order, refer, sign) · Availability · Practice & money · Growth · Settings.
- **Organisation portal *(new)*:** Registration (RC + licence + documents + contact person) · Verification · Sizing & plan · Branches · **Departments & seats** · Staff invitations & roles · Booking allocation · Day view across branches · Subscription & invoices · Organisation public profile.
- **Department apps *(new)*:** **Nursing** (today's patients, vitals, injections, observations) · **Laboratory** (order queue, structured result entry, attachments) · **Pharmacy** (prescription queue, dispense, substitutions) · **Front desk** (walk-in registration, check-in, queue, payment).
- **External party *(new)*:** the scoped link — privacy notice → what to do → structured result upload → done, link expires.
- **Platform Admin:** Organisation & practitioner approval · Plan configuration · (Phase 2) Analytics.

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
| Member app — the whole module | 57 | 158 | 8 | Done · prototype audited complete |
| Doctor app — full module (rebuilt) | 52 | 270 | 8 | Done · prototype audited complete |
| Organisation console — admin, clinical chain, external parties | 55 | 217 | 8 | Done · not yet rendered into Figma |
| Platform admin | — | — | — | Not started |

The member app was built and reviewed in two batches. They are now **one bundle** — one builder,
one prototype, one render script — which is what made the module auditable end to end for the
first time. That audit found 21 unreachable screens and, more seriously, that **a member could
not sign out on a phone**: the control existed on the desktop screens only. Both are fixed.

### 15.1a The clinical chain now crosses module boundaries

Until August the three modules stopped at their own edges: a doctor could write an order but not
send it anywhere, and could intend to share a record but not actually ask the member. Eight
screens close both loops.

**An order leaving the building.** `C4 Order tests` → `C11 Send the order` picks who runs it —
the doctor's own laboratory or imaging room, a Medra partner, a single-use link to somewhere
that is not on Medra, or paper. `C12` tracks it through the five steps of its life. The result
comes back either as a photograph (`C5`, which already existed) or **as data** (`P8`), and the
difference is clinical, not cosmetic: structured values carry the laboratory's own reference
ranges, can be trended against the patient's own history, and name the scientist and the
analyser that produced them. A photographed report carries a doctor's transcription, and a
transcription error becomes part of the record silently.

**A share that does not exist until the member agrees.** `C13` picks the recipient and the
scope; `C14` waits; `R11` on the member's phone shows her exactly what was ticked, in the same
words, and states plainly that declining does not affect her care; `R12` gives her the handle on
it afterwards — opened or not, when it dies, revoke, narrow, and an append-only log. Only then
does `C15` produce a link.

Two rules are now visible on the screens rather than assumed in a document:

1. **Two lines always travel and cannot be switched off** — who the member is, and what they are
   allergic to. A radiographer does not need a medicine list to photograph a spine, but nobody
   should ever be handed a patient without their allergies.
2. **A link's address is a random token, never the member's Medra ID.** The earlier draft used
   `medra.ng/<Medra ID>`, which made every link guessable by counting. This was a defect and is
   corrected in both the doctor and organisation modules. **It must survive into build.**

Every screen is drawn at **1440 desktop and 390 mobile**, wired into a clickable prototype with a
motion spec, and validated offline (tokens, icons, images, DSL rules) before rendering.

### 15.2 Product decisions settled by the Member designs

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

### 15.7 What v2.0 does to the design already built

525 frames are rendered across four bundles: design system 27 · authentication 70 · member 158 ·
doctor 270, with the organisation console's 217 built and awaiting a render. The review reads as "alter the design from the beginning", and for the **product**
that is fair — but it is not a rebuild of the file. Most of the work survives; three kinds of
change land on it.

**A. Retrofit — small, mechanical, across existing screens**

| Change | Where | Size |
|---|---|---|
| NIN field | Auth: doctor sign-up, member sign-up | 4 frames |
| Date of birth mandatory, age-only fallback removed | Auth: member details | 2 frames |
| Data-privacy undertaking as a step | Auth: doctor and organisation onboarding | 4 frames |
| NHIS and private insurance | Member: profile, personal details | 4 frames |
| **"Not medically verified" state** on blood group, genotype, weight, allergies, conditions | Member home, records, profile; doctor's patient file and consultation room | ~18 frames + one new component with two variants |

> **Applied 10 August 2026.** All of row A is done. `health_fact()` is a shared primitive in
> `medra_ui.py`, so the member, doctor and organisation modules render provenance identically and
> the label genuinely travels with the value rather than being re-implemented per screen.

The verification state is the only one of these with teeth. It is a **component state**, so it is
drawn once and applied — but it has to appear everywhere the value does, including inside the
doctor's view of someone else's record, which is precisely the place a badge is most often
dropped.

**B. Extend — existing modules gain screens**

| Addition | Module | Est. screens |
|---|---|---|
| Raise an order to a department (test, injection, dispense) | Doctor consultation | 2 |
| Generate a scoped external link + consent | Doctor, member | 3 |
| Structured result template — the doctor's view of one | Doctor | 1 |
| Member-side consent to an external share, and its receipt | Member records | 2 |

**C. New — the modules that do not exist yet**

| Module | Est. screens | Notes |
|---|---|---|
| **Organisation portal** | 18–22 | Registration with RC + licence + documents · contact person · verification · sizing · plan · branches · **departments & seats** · staff invitations · allocation · day view · billing · public profile |
| **Nursing app** | 6–8 | Today's patients · vitals · injections and procedures · observations · escalate |
| **Laboratory app** | 6–8 | Order queue · accept · structured result entry · attach · done |
| **Pharmacy app** | 5–6 | Prescription queue · dispense · substitution · stock-out |
| **Front desk app** | 6–8 | Walk-in registration · check-in · queue · payment · allocation |
| **External party flow** | 4–5 | Privacy notice · what to do · structured upload · done and expired |

Roughly **45–57 new screens**, which at both breakpoints and with the mobile hub pattern is the
largest single block of design work remaining — comparable to the doctor module. The department
apps share one shell and one component set, so they cost less than their screen count suggests.

**What does not change:** the member-owned record, the booking loop, consent-scoped sharing, the
subscription model, the design language, the hub → section → sheet mobile pattern, and the
generation-and-audit pipeline. The order of work in §21 changes; the foundation does not.

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
- **Sizing before pricing:** onboarding asks for **practitioners, branches, front-desk staff and
  monthly patient volume**, then recommends a plan. Every input stays editable on the pricing
  screen, and the price recalculates live.
- **Departments and seats (v2.0):** an organisation buys seats inside departments, not licences
  for named individuals. A seat can be reassigned when a technician leaves. Non-clinical seats
  (front desk) and clinical support seats (nursing, laboratory, pharmacy) are priced below a
  practitioner seat — they are numerous and they are what makes the record complete, so pricing
  them like a consultant would defeat the point of having them.

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

**Revised in v2.0.** The clinical chain moved from "later" into the MVP, because without it the
record is incomplete and the doctor becomes a typist — which removes the reason to buy.

- **Phase 1 — MVP (this PRD):** Modules 1–13. Member booking loop · doctor consultation and
  records · **organisation portal with departments and seats** · **nursing, laboratory and
  pharmacy apps** · **front desk** · **scoped external-access link** · **verification state on
  health data** · identity (NIN, DOB, insurance) · manual telemedicine link · Paystack
  trial→paid · Abuja pilot.
- **Phase 2:** Automated Daily.co links; rescheduling and waitlists; multi-branch analytics;
  internal staff messaging; doctor analytics; assisted drug-interaction flags; tiered and
  enterprise plans; insurance eligibility checks with partners.
- **Phase 3+:** In-app video UI; employer-sponsored plans; claims submission; ICD coding;
  ratings and reviews; multi-language; offline; interoperability and exports; partner API to
  replace the external link for high-volume labs.

> The MVP is now materially larger than v1.0's. If the pilot date is fixed, the honest lever is
> **breadth of the clinical chain**, not its existence: ship nursing and laboratory, and let
> pharmacy and front desk follow. Dropping the chain entirely returns the product to the thing
> the review said would not work.

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

## 23. Second Review — 9 August 2026 · decisions and open questions

Participants: Godwin Okwor, Israel Oni. The review covered authentication and onboarding for
doctors, organisations and members, and stopped partway through the member dashboard; it
continues Friday.

### 23.1 Decisions taken

| # | Decision | Where it lands |
|---|---|---|
| 1 | A platform that models only doctors cannot work. Nurses, lab technicians and pharmacists are first-class roles | §6, Module 11 |
| 2 | Organisations onboard **departments**, not individuals; seats are bought within them | Module 10.3, §18 |
| 3 | Organisation identity needs **RC number and practice licence** — an RC number alone proves nothing clinical | Module 10.1 |
| 4 | A named contact person registers on behalf of the organisation and is verified as an individual | Module 10.1 |
| 5 | A standalone laboratory or pharmacy is a valid organisation type | Module 10.3 |
| 6 | The **member is the connector** between institutions — records are member-based, not institution-based *(ratifies v1.0)* | §1, §13 |
| 7 | External parties reach a record by a **scoped, single-use, consent-gated link**, short enough to read aloud | Module 12 |
| 8 | Lab results are entered against a **structured template** — analyte, value, unit, range — never as prose | Module 11.1 |
| 9 | Self-reported health data is marked **"Not medically verified"** and stays marked until a clinician or lab vets it | Module 13 |
| 10 | Those fields stay **optional** at onboarding, with an explicit "I'll do this later" | Module 13 |
| 11 | **NIN** for doctors and members; **date of birth mandatory** — the age-only shortcut is rejected | Module 1 |
| 12 | **NHIS and private insurance** captured on the member profile | Module 1, §13 |
| 13 | A **data-privacy undertaking** is an unskippable onboarding step for doctors and organisations | Module 1, §12 |
| 14 | Free trial then paid at launch; price follows practitioners, branches and seats | §18 |
| 15 | The people using Medra for their own care are **members**, not "patients" | Throughout |

### 23.2 Open questions — these block design, and are worth answering before Friday

1. **Is a nurse a distinct role, or a practitioner variant?** The review said both at different
   moments — that nurses are "presented as a doctor", and that nursing is as important as
   medicine and needs its own place. This PRD assumes a **distinct role with its own task-scoped
   app**, because a nurse's screen is a work queue and a doctor's is a decision surface. Confirm.
2. **Who creates staff accounts?** Assumed: the organisation admin invites, the person completes
   their own identity and credential check. The alternative — staff self-register and request to
   join — is friendlier but lets an unverified person sit in a clinical queue.
3. **What is the definitive document list per organisation type?** CAC certificate and practice
   licence are settled. A diagnostic laboratory and a pharmacy will each have their own
   regulator's registration; naming them is a prerequisite for the upload screen.
4. **Who can flip a health fact to verified?** Assumed: any doctor at the point of care, or a lab
   result that measures it directly. Should a nurse-recorded weight count as verified?
5. **Is insurance storage only, or eligibility and claims?** Assumed **storage only** at MVP —
   the number sits on the profile and a partner institution uses it. Claims submission is a large
   integration and is not in this scope.
6. **Does the front desk take payment inside Medra, or record one taken elsewhere?** This decides
   whether the payment rail is one-sided (member pays before booking) or two-sided.
7. **The subscription contradiction from v1.0 is still open.** §4 says practitioners pay a
   subscription and members pay providers directly; the 1 August review added payment before
   booking, which means Medra collects and pays out. Both are designed. It needs deciding before
   build, because "both" means two charges on the same transaction.

### 23.3 Sequencing recommendation

The organisation module is the buyer's module and the department apps hang off it, so it comes
first. But the **verification-state retrofit is small, safety-critical and touches screens that
already exist** — it should be done immediately rather than queued behind a new module, because
every day the design shows unverified data as fact is a day that assumption spreads into build.

Suggested order: verification-state retrofit → identity and privacy-clause retrofit →
organisation portal → laboratory app (it unlocks the external link and the result template) →
nursing → front desk → pharmacy → external party flow.

---

## 24. Glossary

- **MDCN** — Medical and Dental Council of Nigeria (doctor licensing/identity).
- **NDPA / NDPR** — Nigeria Data Protection Act 2023 / Regulation.
- **Paystack** — payment processor for the clinic subscription.
- **Daily.co** — video infrastructure (Phase 2 telemedicine automation).
- **RBAC** — Role-Based Access Control.
- **Institution / Enterprise** — a clinic/hospital; enterprise = multi-branch billed as one.
- **Verified badge** — visible marker that Medra confirmed a provider's MDCN/licence.
- **NIN** — National Identification Number (Nigeria); a second identifier for members and doctors.
- **RC number** — company registration number issued by the CAC. Proves a company exists, not that it may practise medicine.
- **NHIS** — National Health Insurance Scheme.
- **Department** — the unit an organisation onboards and buys seats in (laboratory, pharmacy, nursing, front desk, a clinical specialty).
- **Order** — a unit of work a doctor raises for a department: a test, an injection or procedure, or a dispense.
- **Not medically verified** — the state of a health fact a member entered themselves, which travels with the value until a clinician or lab confirms it.
- **External access grant** — a scoped, single-use, consent-gated link that lets a party who is not on Medra read what they need and return a result.

---

