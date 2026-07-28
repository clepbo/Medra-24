# CHANGES — Medra Auth

## v3.0 — Review feedback: access, nomenclature, pricing, imagery
- **More ways in.** Members sign up/in with **phone or email**, or **Continue with Google / Apple**.
- **No code every time.** Verify **once**, then the device is trusted for 30 days; returning
  members get a **biometric quick-unlock** screen. Doctors/admins get "keep me signed in", and
  2-factor is **step-up only** on a new device.
- **Nomenclature.** "Patient" → **member** for people using Medra for their own care ("I'm here
  for my own care"). "Patient" is retained only for clinical contexts.
- **Doctors.** Registration now captures **name + work email + phone + MDCN**; sign-in accepts
  **email, phone or MDCN**.
- **Institution pricing.** New **organisation-sizing** step (practitioners · branches · admin
  seats · monthly volume) feeds a **recommended plan with real ₦ pricing**, a line-by-line
  breakdown, monthly/annual toggle, and **inline steppers** so everything stays editable.
- **Imagery.** The member flow now shows **care in action** (a practitioner attending to a
  patient) instead of a headshot; success uses a bright, hopeful portrait.
- **Tooling.** `validate.js` now catches collapsed numeric props (`w=390` vs `w={390}`).

**70 frames · 35 screens · 4 pages · 318 prototype links · ALL 70 CLEAN, FULLY OFFLINE ✓**

## v2.0 — "Soft Clinical" redesign + real photography
Real licensed photography (Nigerian/African representation), soft mesh grounds, floating cards,
gradient CTAs, ECG-pulse motif, highlight-chip headlines; onboarding reworked into a 3-slide
story plus a guided profile setup capturing health basics.

## v1.0 — Authentication module (Editorial Light+)
Initial 56-frame build across Entry, Patient, Doctor and Institution pages.
