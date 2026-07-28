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

