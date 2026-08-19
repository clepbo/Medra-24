# What you can do on Medra

Every function in the product, grouped by the person who performs it, with the screens that
carry it end to end. Generated from `tools/figma/functions.py` — edit the map there, not this
file.

**12 personas · 70 functions · 234 screens**, every one
placed. 27 screens appear in more than one function, because they genuinely do two
jobs — a lab result is part of *order a test and get it back* for the doctor and part of *see
what happened* for the member. Those are marked **·copy** below; the first function to claim a
screen owns the original.

Screens are listed in the order a person meets them, not alphabetically. That ordering is the
point of this index — keep it right when screens are added.

---

## Contents

- [Member](#member) — 12 functions
- [Doctor — own practice](#doctor--own-practice) — 11 functions
- [Organisation admin](#organisation-admin) — 8 functions
- [Front desk](#front-desk) — 5 functions
- [Doctor — inside an organisation](#doctor--inside-an-organisation) — 5 functions
- [Nurse](#nurse) — 6 functions
- [Laboratory](#laboratory) — 5 functions
- [Pharmacy](#pharmacy) — 5 functions
- [Imaging](#imaging) — 5 functions
- [Billing](#billing) — 4 functions
- [Referrals](#referrals) — 3 functions
- [Outside party](#outside-party) — 1 functions

---

## Member

*A person using Medra for their own care, and their family's*

### Join Medra

From never having heard of it to a working account. Verify once; the device is trusted after that.

| # | Screen | |
|---:|---|---|
| 1 | Auth · Entry — E1 Onboarding 1 | `auth/E1-onb1` |
| 2 | Auth · Entry — E2 Onboarding 2 | `auth/E2-onb2` |
| 3 | Auth · Entry — E3 Onboarding 3 | `auth/E3-onb3` |
| 4 | Auth · Entry — E4 Welcome | `auth/E4-welcome` |
| 5 | Auth · Entry — E5 Role Selection | `auth/E5-role` |
| 6 | Auth · Member — M1 Create Account | `auth/M1-create` |
| 7 | Auth · Member — M2 Verify Once | `auth/M2-otp` |
| 8 | Auth · Member — M3 Your Name | `auth/M3-name` |
| 9 | Auth · Member — M4 About You | `auth/M4-about` |
| 10 | Auth · Member — M5 Health Basics | `auth/M5-health` |
| 11 | Auth · Member — M9 Success | `auth/M9-success` |
| 12 | Auth · Member — M6 Log In | `auth/M6-login` |
| 13 | Auth · Member — M7 Quick Unlock | `auth/M7-unlock` |
| 14 | Auth · Member — M8 Cannot Get Code | `auth/M8-help` |

### Find a doctor

Search, narrow, and read a profile well enough to choose. The first-run home screen is here because an empty home is where finding starts.

| # | Screen | |
|---:|---|---|
| 1 | Member · Home — H2 First Visit (empty state) | `member/H2-home-empty` |
| 2 | Member · Home — H1 Home | `member/H1-home` |
| 3 | Member · Search — S1 Results | `member/S1-results` |
| 4 | Member · Search — S2 Filters | `member/S2-filters` |
| 5 | Member · Search — S3 No Results | `member/S3-empty` |
| 6 | Member · Doctor — P1 Profile | `member/P1-profile` |

### Book a visit

Pick a time, see the price before agreeing to it, pay, and get a confirmation you can show at a desk.

| # | Screen | |
|---:|---|---|
| 1 | Member · Doctor — P1 Profile | `member/P1-profile` **·copy** |
| 2 | Member · Booking — B1 Choose a Time | `member/B1-slot` |
| 3 | Member · Booking — B2 Slot Taken | `member/B2-taken` |
| 4 | Member · Booking — B3 Review & Confirm | `member/B3-review` |
| 5 | Member · Booking — B4 Payment | `member/B4-payment` |
| 6 | Member · Booking — C1 Confirmed | `member/C1-confirmed` |

### Attend a visit

What happens between booking and being seen — including the video path and the two ways a visit does not happen.

| # | Screen | |
|---:|---|---|
| 1 | Member · Visits — V1 Upcoming | `member/V1-visits` |
| 2 | Member · Visits — V4 Visit Detail | `member/V4-visit` |
| 3 | Member · Visits — V3 No Visits | `member/V3-visits-empty` |
| 4 | Member · Virtual — W0 Join by Link | `member/W0-join` |
| 5 | Member · Virtual — W1 Pre-call Check | `member/W1-precall` |
| 6 | Member · Virtual — W2 In Call | `member/W2-incall` |
| 7 | Member · Virtual — W4 Connection Lost | `member/W4-lost` |
| 8 | Member · Virtual — W3 Visit Summary | `member/W3-callend` |
| 9 | Member · Visits — V5 Reschedule | `member/V5-reschedule` |
| 10 | Member · Visits — V6 Cancel Visit | `member/V6-cancel` |
| 11 | Member · Visits — V7 Cancelled | `member/V7-cancelled` |

### See what happened

Everything a visit produces, from the member's side: the note, the results, the trend.

| # | Screen | |
|---:|---|---|
| 1 | Member · Visits — V2 Past | `member/V2-past` |
| 2 | Member · Records — R2 Consultation Note | `member/R2-note` |
| 3 | Member · Records — R3 Lab Results & Diagnostics | `member/R3-lab` |
| 4 | Member · Records — R4 Vitals Trend | `member/R4-vitals` |
| 5 | Member · Records — R10 One-page Summary | `member/R10-summary` |

### Keep my records

The record is the member's, travels with them, and can be added to by hand — most Nigerian history is on paper.

| # | Screen | |
|---:|---|---|
| 1 | Member · Records — R1 Timeline | `member/R1-records` |
| 2 | Member · Records — R9 No Records | `member/R9-records-empty` |
| 3 | Member · Records — R7 Add a Record | `member/R7-upload` |
| 4 | Member · Records — R8 Record Added | `member/R8-added` |
| 5 | Member · Records — R10 One-page Summary | `member/R10-summary` **·copy** |

### Share my records, and take it back

Consent, in both directions. Every screen here is one a member has to be able to act on under pressure.

| # | Screen | |
|---:|---|---|
| 1 | Member · Records — R5 Share Records | `member/R5-share` |
| 2 | Member · Records — R11 Approve a Share | `member/R11-approve` |
| 3 | Member · Records — R6 Who Has Access | `member/R6-access` |
| 4 | Member · Records — R12 Shared Outside Medra | `member/R12-shared` |

### Take my medicines

What to take, when, and how to get more without a trip to the clinic for a piece of paper.

| # | Screen | |
|---:|---|---|
| 1 | Member · Medicines — M1 My Medicines | `member/M1-meds` |
| 2 | Member · Medicines — M2 Medicine Detail | `member/M2-med` |
| 3 | Member · Medicines — M4 Reminders | `member/M4-reminders` |
| 4 | Member · Medicines — M3 Request a Refill | `member/M3-refill` |
| 5 | Member · Medicines — M5 No Medicines | `member/M5-meds-empty` |

### Care for my family

A child's records until they are eighteen, and an adult's only with their say-so.

| # | Screen | |
|---:|---|---|
| 1 | Member · Profile — P3 Dependants | `member/P3-dependants` |
| 2 | Member · Profile — P4 Add a Dependant | `member/P4-add-dependant` |
| 3 | Member · Profile — P3b Family Plan | `member/P3b-family` |

### Manage my account

Identity, devices, what Medra is allowed to send, and the two screens that end the relationship.

| # | Screen | |
|---:|---|---|
| 1 | Member · Profile — P0 Profile | `member/P0-profile` |
| 2 | Member · Profile — P2 Personal Details | `member/P2-details` |
| 3 | Member · Profile — P5 Devices & Security | `member/P5-security` |
| 4 | Member · Profile — P6 Notification Preferences | `member/P6-notifs` |
| 5 | Member · Profile — P7 Language & Accessibility | `member/P7-language` |
| 6 | Member · Profile — P8 Privacy & Data | `member/P8-privacy` |
| 7 | Member · Profile — P9 Delete Account | `member/P9-delete` |
| 8 | Member · Profile — P9b Confirm Deletion | `member/P9b-delete-confirm` |

### Be told things

Notifications, and the preference screen that decides which of them ever arrive.

| # | Screen | |
|---:|---|---|
| 1 | Member · Alerts — N0 Notification Panel | `member/N0-panel` |
| 2 | Member · Alerts — N1 Notifications | `member/N1-notifs` |
| 3 | Member · Alerts — N2 No Notifications | `member/N2-notifs-empty` |
| 4 | Member · Profile — P6 Notification Preferences | `member/P6-notifs` **·copy** |

### When something breaks

The three states every screen can fall into. Kept together because they are reviewed together.

| # | Screen | |
|---:|---|---|
| 1 | Member · States — X1 Loading | `member/X1-loading` |
| 2 | Member · States — X2 Offline | `member/X2-offline` |
| 3 | Member · States — X3 Something Went Wrong | `member/X3-error` |

## Doctor — own practice

*A clinician working for themselves, not inside an organisation*

### Join and get verified

MDCN is checked by a person, which is the slowest thing Medra does and the reason anybody trusts it.

| # | Screen | |
|---:|---|---|
| 1 | Auth · Doctor — D1 Create Account | `auth/D1-create` |
| 2 | Auth · Doctor — D2 Verify Code | `auth/D2-otp` |
| 3 | Auth · Doctor — D3 Set Password | `auth/D3-password` |
| 4 | Auth · Doctor — D4 Verification Pending | `auth/D4-pending` |
| 5 | Auth · Doctor — D5 Profile Setup | `auth/D5-profile` |
| 6 | Auth · Doctor — D10 Success | `auth/D10-success` |
| 7 | Auth · Doctor — D6 Log In | `auth/D6-login` |
| 8 | Auth · Doctor — D7 Two-Factor | `auth/D7-2fa` |
| 9 | Auth · Doctor — D8 Forgot Password | `auth/D8-forgot` |
| 10 | Auth · Doctor — D9 New Password | `auth/D9-reset` |
| 11 | Doctor · Start — G1 Setup Checklist | `doctor/G1-checklist` |
| 12 | Doctor · Start — G2 Verification | `doctor/G2-verification` |

### Run my day

The queue, the person in front of you, and the four things that go wrong in a clinic day.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Today — K1 Queue | `doctor/K1-today` |
| 2 | Doctor · Today — K9 Everything | `doctor/K9-more` |
| 3 | Doctor · Today — K2 Requests | `doctor/K2-requests` |
| 4 | Doctor · Today — K3 Running Late | `doctor/K3-late` |
| 5 | Doctor · Today — K5 Appointment Outcome | `doctor/K5-outcome` |
| 6 | Doctor · Today — K10 Critical Result | `doctor/K10-critical` |
| 7 | Doctor · States — X2 Nothing Booked | `doctor/X2-empty` |

### See a patient

Read the file, hold the consultation, and sign it. Nothing reaches the member until it is signed.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Today — K4 Read the File | `doctor/K4-file` |
| 2 | Doctor · Consult — C1 In Progress | `doctor/C1-room` |
| 3 | Doctor · Consult — C2 Templates | `doctor/C2-templates` |
| 4 | Doctor · Consult — C10 Virtual Visit | `doctor/C10-virtual` |
| 5 | Doctor · Consult — C7 Review & Sign | `doctor/C7-sign` |
| 6 | Doctor · Consult — C8 Signed | `doctor/C8-signed` |
| 7 | Doctor · Consult — C9 Unsigned Notes | `doctor/C9-drafts` |

### Prescribe

Including the interaction check, which is the one place the software is allowed to stop a doctor.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Consult — C3 Prescribe | `doctor/C3-prescribe` |
| 2 | Doctor · Patients — P6 Refills | `doctor/P6-refills` |

### Order a test and get it back

The longest chain in the product: order, route it, watch it, read it, release it.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Consult — C4 Order Tests | `doctor/C4-tests` |
| 2 | Doctor · Consult — C11 Send the Order | `doctor/C11-route` |
| 3 | Doctor · Consult — C12 Order Status | `doctor/C12-order` |
| 4 | Doctor · Consult — C5 Result | `doctor/C5-upload` |
| 5 | Doctor · Patients — P7 Results | `doctor/P7-results` |
| 6 | Doctor · Patients — P8 Structured Result | `doctor/P8-result` |
| 7 | Doctor · Today — K10 Critical Result | `doctor/K10-critical` **·copy** |

### Send a member somewhere else

A referral inside Medra, and the single-use link for the laboratory that is not on it.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Consult — C6 Refer | `doctor/C6-refer` |
| 2 | Doctor · Consult — C13 Send to Someone Not on Medra | `doctor/C13-link` |
| 3 | Doctor · Consult — C14 Waiting on Consent | `doctor/C14-consent` |
| 4 | Doctor · Consult — C15 The Link Is Ready | `doctor/C15-links` |

### Look after my patients between visits

The work that happens when nobody is in the room.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Patients — P1 Find a Patient | `doctor/P1-patients` |
| 2 | Doctor · Patients — P2 Record | `doctor/P2-record` |
| 3 | Doctor · Patients — P3 Ask for More | `doctor/P3-access` |
| 4 | Doctor · Patients — P4 Follow-ups | `doctor/P4-followups` |
| 5 | Doctor · Patients — P5 Messages | `doctor/P5-messages` |
| 6 | Doctor · Patients — P6 Refills | `doctor/P6-refills` **·copy** |

### Manage my schedule

Availability is a promise: if a slot shows on Medra it is genuinely open.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Schedule — K6 Week | `doctor/K6-week` |
| 2 | Doctor · Schedule — K7 Availability | `doctor/K7-availability` |
| 3 | Doctor · Schedule — K8 Time Off | `doctor/K8-timeoff` |

### Run my practice

Fees, channels, where I practise, what I am paid, and what I pay.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Practice — S1 Public Profile | `doctor/S1-profile` |
| 2 | Doctor · Practice — S2 Types & Fees | `doctor/S2-fees` |
| 3 | Doctor · Practice — S3 Virtual Visits | `doctor/S3-virtual` |
| 4 | Doctor · Practice — S4 Contact Channels | `doctor/S4-contact` |
| 5 | Doctor · Practice — S7 Where I Practise | `doctor/S7-practice` |
| 6 | Doctor · Practice — S5 Earnings | `doctor/S5-earnings` |
| 7 | Doctor · Practice — S6 Subscription | `doctor/S6-billing` |
| 8 | Doctor · Practice — S8 Account & Security | `doctor/S8-security` |
| 9 | Doctor · States — X1 Subscription Locked | `doctor/X1-locked` |

### Grow my practice

The three screens that decide whether a doctor stays on the platform.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Growth — R1 Insights | `doctor/R1-insights` |
| 2 | Doctor · Growth — R2 Ratings | `doctor/R2-reviews` |
| 3 | Doctor · Growth — R3 Booking Link | `doctor/R3-link` |
| 4 | Doctor · Start — G3 Invite a Colleague | `doctor/G3-invite` |

### When something breaks

| # | Screen | |
|---:|---|---|
| 1 | Doctor · States — X6 Loading | `doctor/X6-loading` |
| 2 | Doctor · States — X4 Offline | `doctor/X4-offline` |
| 3 | Doctor · States — X5 Error | `doctor/X5-error` |
| 4 | Doctor · States — X3 Notifications | `doctor/X3-notifications` |

## Organisation admin

*The person who owns the whole building — and the only one who can create a seat*

### Register the organisation

RC number, practice licence, size, plan. Checked by a person before it can take a public booking.

| # | Screen | |
|---:|---|---|
| 1 | Auth · Institution — I1 Register | `auth/I1-register` |
| 2 | Auth · Institution — I2 Verify Documents | `auth/I2-documents` |
| 3 | Auth · Institution — I3 Organisation Size | `auth/I3-orgsize` |
| 4 | Auth · Institution — I4 Your Plan | `auth/I4-plan` |
| 5 | Auth · Institution — I5 Verify Admin | `auth/I5-otp` |
| 6 | Auth · Institution — I6 Set Password | `auth/I6-password` |
| 7 | Auth · Institution — I7 Application Submitted | `auth/I7-pending` |
| 8 | Auth · Institution — I11 Success | `auth/I11-success` |
| 9 | Auth · Institution — I8 Facility Admin Log In | `auth/I8-admin-login` |
| 10 | Auth · Institution — I9 Forgot Password | `auth/I9-forgot` |
| 11 | Auth · Institution — I10 New Password | `auth/I10-reset` |

### Set the organisation up

Branches, seats and the public profile — everything that has to be true before anybody works.

| # | Screen | |
|---:|---|---|
| 1 | Org · Setup — A1 Setup Checklist | `org/A1-setup` |
| 2 | Org · Setup — A2 Verification | `org/A2-verify` |
| 3 | Org · Setup — A3 Branches | `org/A3-branches` |
| 4 | Org · Setup — A4 Plan & Seats | `org/A4-plan` |
| 5 | Org · Setup — A5 Public Profile | `org/A5-profile` |
| 6 | Org · States — X2 Not Yet Verified | `org/X2-unverified` |

### Onboard a department or a member of staff

The admin's defining job. A department is the unit; permissions follow it, never the person.

| # | Screen | |
|---:|---|---|
| 1 | Org · People — C1 Departments | `org/C1-departments` |
| 2 | Org · People — C3 Add a Department | `org/C3-add-dept` |
| 3 | Org · People — C2 Department | `org/C2-department` |
| 4 | Org · People — C4 People | `org/C4-people` |
| 5 | Org · People — C5 Invite Someone | `org/C5-invite` |
| 6 | Org · People — C6 Person | `org/C6-person` |
| 7 | Org · People — C7 Roles & Permissions | `org/C7-roles` |
| 8 | Org · States — X1 Seats Full | `org/X1-seats` |

### Run the day across the organisation

Every department, every branch, and the four bookings nobody has been allocated to.

| # | Screen | |
|---:|---|---|
| 1 | Org · Today — B1 Today | `org/B1-today` |
| 2 | Org · Today — B2 Bookings & Allocation | `org/B2-bookings` |
| 3 | Org · Today — B3 Find a Member | `org/B3-find` |
| 4 | Org · States — X4 Nothing Booked | `org/X4-empty` |

### Read the numbers

The four questions an administrator actually arrives with, one screen each.

| # | Screen | |
|---:|---|---|
| 1 | Org · Reports — F4 Reports | `org/F4-reports` |
| 2 | Org · Reports — F8 Patients | `org/F8-patients` |
| 3 | Org · Reports — F9 Clinicians | `org/F9-clinicians` |
| 4 | Org · Reports — F10 Departments | `org/F10-departments` |

### Govern who sees what

Access is per episode of care. This is the group that makes a shared record safe to hand around a hospital.

| # | Screen | |
|---:|---|---|
| 1 | Org · Access — F1 Who Has Access | `org/F1-access` |
| 2 | Org · Access — F2 Audit Log | `org/F2-audit` |
| 3 | Org · Access — F3 Privacy & Compliance | `org/F3-compliance` |
| 4 | Org · People — C7 Roles & Permissions | `org/C7-roles` **·copy** |
| 5 | Org · Governance — F7 Critical Results | `org/F7-critical` |

### Settings and money

| # | Screen | |
|---:|---|---|
| 1 | Org · Settings — F5 Organisation Settings | `org/F5-settings` |
| 2 | Org · Settings — F6 Subscription | `org/F6-billing` |
| 3 | Org · States — X3 Subscription Locked | `org/X3-locked` |

### When something breaks

| # | Screen | |
|---:|---|---|
| 1 | Org · States — X7 Loading | `org/X7-loading` |
| 2 | Org · States — X5 Offline | `org/X5-offline` |
| 3 | Org · States — X6 Error | `org/X6-error` |

## Front desk

*Registration, check-in and payment — the busiest seat in the building*

### Join the organisation as staff

Shared by every organisation persona: the invitation an admin sent, through to a working seat.

| # | Screen | |
|---:|---|---|
| 1 | Auth · Staff — S1 The Invitation | `auth/S1-invite` |
| 2 | Auth · Staff — S2 Prove It Is You | `auth/S2-verify` |
| 3 | Auth · Staff — S3 Your Details | `auth/S3-details` |
| 4 | Auth · Staff — S4 Your Registration | `auth/S4-registration` |
| 5 | Auth · Staff — S5 The Undertaking | `auth/S5-undertaking` |
| 6 | Auth · Staff — S6 Set A Password | `auth/S6-password` |
| 7 | Auth · Staff — S7 Waiting For Your Seat | `auth/S7-pending` |
| 8 | Auth · Staff — S8 You Are In | `auth/S8-ready` |
| 9 | Auth · Staff — S9 Add This Workplace | `auth/S9-workplace` |
| 10 | Auth · Staff — S10 Invitation Expired | `auth/S10-expired` |

### Run the front desk day

Who is here, who is late, who has not paid.

| # | Screen | |
|---:|---|---|
| 1 | Org · Front Desk — D12 The Day | `org/D12-desk` |
| 2 | Org · Today — B2 Bookings & Allocation | `org/B2-bookings` **·copy** |
| 3 | Org · States — X5 Offline | `org/X5-offline` **·copy** |

### Register somebody who just walked in

Most Nigerian clinic visits start this way, not with a booking.

| # | Screen | |
|---:|---|---|
| 1 | Org · Front Desk — D13 Register a Walk-in | `org/D13-walkin` |
| 2 | Org · Today — B3 Find a Member | `org/B3-find` **·copy** |

### Check in and take payment

| # | Screen | |
|---:|---|---|
| 1 | Org · Front Desk — D14 Check In | `org/D14-checkin` |

### Talk to the rest of the building

| # | Screen | |
|---:|---|---|
| 1 | Org · Front Desk — H1 Messages | `org/H1-desk-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` |

## Doctor — inside an organisation

*The same clinician, in a workplace they do not own*

### Add a workplace to my account

One account, two workplaces. The MDCN number is the doctor's, so nothing is re-verified.

| # | Screen | |
|---:|---|---|
| 1 | Auth · Staff — S9 Add This Workplace | `auth/S9-workplace` **·copy** |
| 2 | Auth · Staff — S1 The Invitation | `auth/S1-invite` **·copy** |
| 3 | Auth · Staff — S8 You Are In | `auth/S8-ready` **·copy** |

### My day here

A list the doctor did not build — reception booked it and the admin allocated it.

| # | Screen | |
|---:|---|---|
| 1 | Org · Doctor — G1 My Day | `org/G1-orgdoc` |
| 2 | Org · Doctor — H7 My Patients | `org/H7-dr-patients` |

### Results waiting on me

| # | Screen | |
|---:|---|---|
| 1 | Org · Doctor — H8 Results | `org/H8-dr-results` |
| 2 | Org · Laboratory — D15 Critical Value | `org/D15-critical` |

### The roster I am on

The hospital's roster, not the doctor's availability. They ask; a named person answers.

| # | Screen | |
|---:|---|---|
| 1 | Org · Doctor — G2 My Roster | `org/G2-roster` |

### Talk to the team

A message goes to a department, and whoever is on shift picks it up.

| # | Screen | |
|---:|---|---|
| 1 | Org · Doctor — G3 Messages | `org/G3-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` **·copy** |

## Nurse

*Vitals, injections, observations — and the escalation that must never wait*

### Work my queue

Ordered by when the doctor needs them, not by when they arrived.

| # | Screen | |
|---:|---|---|
| 1 | Org · Nursing — D1 My Queue | `org/D1-nursing` |

### Record vitals

| # | Screen | |
|---:|---|---|
| 1 | Org · Nursing — D2 Record Vitals | `org/D2-vitals` |

### Administer and record

Five rights, shortened to the four a queue actually gets wrong.

| # | Screen | |
|---:|---|---|
| 1 | Org · Nursing — D3 Administer & Record | `org/D3-administer` |

### Escalate something out of range

Two minutes to the first doctor, then the duty doctor automatically. Never a message that waits.

| # | Screen | |
|---:|---|---|
| 1 | Org · Nursing — D4 Escalate | `org/D4-escalate` |

### Standing orders

A doctor's instruction that repeats, and the four things nursing may do without asking.

| # | Screen | |
|---:|---|---|
| 1 | Org · Nursing — H9 Standing Orders | `org/H9-nurse-orders` |

### Talk to the team

| # | Screen | |
|---:|---|---|
| 1 | Org · Nursing — H2 Messages | `org/H2-nurse-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` **·copy** |

## Laboratory

*Samples in, structured results out — and the value that has to be phoned*

### Work the order queue

| # | Screen | |
|---:|---|---|
| 1 | Org · Laboratory — D5 Order Queue | `org/D5-lab-queue` |
| 2 | Org · Laboratory — D6 Order | `org/D6-lab-order` |

### Enter a result

A form rather than a paragraph, because prose cannot be trended or compared.

| # | Screen | |
|---:|---|---|
| 1 | Org · Laboratory — D7 Enter Result | `org/D7-lab-result` |

### Reject a bad sample

In a paper laboratory this happens silently. Here it always tells somebody.

| # | Screen | |
|---:|---|---|
| 1 | Org · Laboratory — D8 Sample Problem | `org/D8-lab-problem` |

### Handle a critical value

The one result that cannot be sent. It reaches a named human by voice, with a read-back.

| # | Screen | |
|---:|---|---|
| 1 | Org · Laboratory — D15 Critical Value | `org/D15-critical` **·copy** |
| 2 | Org · Governance — F7 Critical Results | `org/F7-critical` **·copy** |
| 3 | Doctor · Today — K10 Critical Result | `doctor/K10-critical` **·copy** |

### Talk to the team

| # | Screen | |
|---:|---|---|
| 1 | Org · Laboratory — H3 Messages | `org/H3-lab-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` **·copy** |

## Pharmacy

*Dispensing against a prescription, and what happens when you cannot*

### Work the prescription queue

Somebody standing at the counter comes first, whatever order they arrived in.

| # | Screen | |
|---:|---|---|
| 1 | Org · Pharmacy — D9 Prescription Queue | `org/D9-pharmacy` |

### Dispense

| # | Screen | |
|---:|---|---|
| 1 | Org · Pharmacy — D10 Dispense | `org/D10-dispense` |

### When you cannot dispense

A substitution is a proposal, never a decision — it goes back to the prescriber.

| # | Screen | |
|---:|---|---|
| 1 | Org · Pharmacy — D11 Cannot Dispense | `org/D11-substitute` |

### Watch the shelf

A count you keep, not a warehouse system: so you can tell a member before they queue.

| # | Screen | |
|---:|---|---|
| 1 | Org · Pharmacy — H10 Stock | `org/H10-pharm-stock` |

### Talk to the team

| # | Screen | |
|---:|---|---|
| 1 | Org · Pharmacy — H4 Messages | `org/H4-pharm-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` **·copy** |

## Imaging

*The department where the patient has to be present, prepared and safe*

### Work the worklist

Ordered by appointment, because an image needs the person, the room and the machine at once.

| # | Screen | |
|---:|---|---|
| 1 | Org · Imaging — D16 Worklist | `org/D16-imaging` |

### Check it is safe to scan

The only screen in Medra that refuses to move.

| # | Screen | |
|---:|---|---|
| 1 | Org · Imaging — D17 Safety Check | `org/D17-prepare` |

### Report a study

A radiologist's sentence, not a picture. Signed by name, amendable only by a second version.

| # | Screen | |
|---:|---|---|
| 1 | Org · Imaging — D18 Report a Study | `org/D18-report` |

### Rooms and machines

| # | Screen | |
|---:|---|---|
| 1 | Org · Imaging — H11 Rooms | `org/H11-img-rooms` |

### Talk to the team

| # | Screen | |
|---:|---|---|
| 1 | Org · Imaging — H5 Messages | `org/H5-img-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` **·copy** |

## Billing

*Running the money, which is a different job from taking it at the desk*

### The money today

Cash is the only line Medra cannot verify itself, so it is the one counted against a drawer.

| # | Screen | |
|---:|---|---|
| 1 | Org · Billing — D19 The Money Today | `org/D19-billing` |

### Take a payment

Part payment is a first-class case. Entries are append-only.

| # | Screen | |
|---:|---|---|
| 1 | Org · Billing — D20 Take a Payment | `org/D20-payment` |

### Chase an insurance claim

Where the revenue actually leaks: submitted, queried, never resubmitted.

| # | Screen | |
|---:|---|---|
| 1 | Org · Billing — D21 Insurance Claims | `org/D21-claims` |

### Talk to the team

| # | Screen | |
|---:|---|---|
| 1 | Org · Billing — H6 Messages | `org/H6-bill-messages` |
| 2 | Org · Doctor — G4 A Conversation | `org/G4-thread` **·copy** |

## Referrals

*Sending a member elsewhere and receiving one — it spans several personas, so it is its own group*

### Refer a member out

| # | Screen | |
|---:|---|---|
| 1 | Org · Referrals — E1 Referred Out | `org/E1-outbound` |
| 2 | Org · Referrals — E2 Refer Someone | `org/E2-create` |
| 3 | Org · Referrals — E3 Referral Sent | `org/E3-sent` |
| 4 | Doctor · Consult — C6 Refer | `doctor/C6-refer` **·copy** |

### Receive a referral

Accepting books it and tells them both. Declining tells them too — silence is not available.

| # | Screen | |
|---:|---|---|
| 1 | Org · Referrals — E4 Referred To Us | `org/E4-inbound` |
| 2 | Org · Referrals — E5 Referral Detail | `org/E5-inbound-detail` |

### Send work to somebody not on Medra

A scoped, single-use, consent-gated link. The address is a random token, never a Medra ID.

| # | Screen | |
|---:|---|---|
| 1 | Doctor · Consult — C13 Send to Someone Not on Medra | `doctor/C13-link` **·copy** |
| 2 | Doctor · Consult — C14 Waiting on Consent | `doctor/C14-consent` **·copy** |
| 3 | Doctor · Consult — C15 The Link Is Ready | `doctor/C15-links` **·copy** |
| 4 | Org · Referrals — E6 Single-use Links | `org/E6-links` |
| 5 | Member · Records — R11 Approve a Share | `member/R11-approve` **·copy** |
| 6 | Member · Records — R12 Shared Outside Medra | `member/R12-shared` **·copy** |

## Outside party

*Somebody with no Medra account, doing one job from a link that dies after it*

### Do one job from a single-use link

Four screens, no account, no training, no way back in. Finishable on a phone in a waiting room.

| # | Screen | |
|---:|---|---|
| 1 | Org · External — E7 Privacy Notice | `org/E7-ext-notice` |
| 2 | Org · External — E8 What You Are Asked To Do | `org/E8-ext-task` |
| 3 | Org · External — E9 Upload the Report | `org/E9-ext-upload` |
| 4 | Org · External — E10 Done | `org/E10-ext-done` |
| 5 | Org · External — E11 Link Expired | `org/E11-ext-expired` |

---

## The screens that do two jobs

These are the ones that will be duplicated when the Figma page is arranged this way. Each is
listed under the function that owns the original first, then everywhere it is copied to.

| Screen | Original lives under | Also copied into |
|---|---|---|
| Auth · Staff — S1 The Invitation | Front desk → Join the organisation as staff | Doctor — inside an organisation → Add a workplace to my account |
| Auth · Staff — S8 You Are In | Front desk → Join the organisation as staff | Doctor — inside an organisation → Add a workplace to my account |
| Auth · Staff — S9 Add This Workplace | Front desk → Join the organisation as staff | Doctor — inside an organisation → Add a workplace to my account |
| Doctor · Consult — C13 Send to Someone Not on Medra | Doctor — own practice → Send a member somewhere else | Referrals → Send work to somebody not on Medra |
| Doctor · Consult — C14 Waiting on Consent | Doctor — own practice → Send a member somewhere else | Referrals → Send work to somebody not on Medra |
| Doctor · Consult — C15 The Link Is Ready | Doctor — own practice → Send a member somewhere else | Referrals → Send work to somebody not on Medra |
| Doctor · Consult — C6 Refer | Doctor — own practice → Send a member somewhere else | Referrals → Refer a member out |
| Doctor · Patients — P6 Refills | Doctor — own practice → Prescribe | Doctor — own practice → Look after my patients between visits |
| Doctor · Today — K10 Critical Result | Doctor — own practice → Run my day | Doctor — own practice → Order a test and get it back · Laboratory → Handle a critical value |
| Member · Doctor — P1 Profile | Member → Find a doctor | Member → Book a visit |
| Member · Profile — P6 Notification Preferences | Member → Manage my account | Member → Be told things |
| Member · Records — R10 One-page Summary | Member → See what happened | Member → Keep my records |
| Member · Records — R11 Approve a Share | Member → Share my records, and take it back | Referrals → Send work to somebody not on Medra |
| Member · Records — R12 Shared Outside Medra | Member → Share my records, and take it back | Referrals → Send work to somebody not on Medra |
| Org · Doctor — G4 A Conversation | Front desk → Talk to the rest of the building | Doctor — inside an organisation → Talk to the team · Nurse → Talk to the team · Laboratory → Talk to the team · Pharmacy → Talk to the team · Imaging → Talk to the team · Billing → Talk to the team |
| Org · Governance — F7 Critical Results | Organisation admin → Govern who sees what | Laboratory → Handle a critical value |
| Org · Laboratory — D15 Critical Value | Doctor — inside an organisation → Results waiting on me | Laboratory → Handle a critical value |
| Org · People — C7 Roles & Permissions | Organisation admin → Onboard a department or a member of staff | Organisation admin → Govern who sees what |
| Org · States — X5 Offline | Organisation admin → When something breaks | Front desk → Run the front desk day |
| Org · Today — B2 Bookings & Allocation | Organisation admin → Run the day across the organisation | Front desk → Run the front desk day |
| Org · Today — B3 Find a Member | Organisation admin → Run the day across the organisation | Front desk → Register somebody who just walked in |
