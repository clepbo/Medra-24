# Medra — Authentication Module (figma-ds-cli)

**90 frames (45 screens × desktop + mobile) · 5 Figma pages · "Soft Clinical" direction**

Each persona renders onto **its own Figma page**:
`Medra Auth — Entry` · `Medra Auth — Member` · `Medra Auth — Doctor` · `Medra Auth — Institution` ·
`Medra Auth — Staff`

Covers every requirement, no dead ends:
- **Onboarding story** — 3 photographic intro slides → welcome → role selection
- **Member** sign-up — **phone _or_ email**, plus **Continue with Google / Apple**; verify **once**,
  then the device is trusted (**no OTP every login**); **quick unlock** with biometrics on return;
  3-step guided onboarding (name/photo → about you → health basics); login; can't-get-code help
- Doctor registration (**name + work email + phone + MDCN**), OTP, set password, **MDCN verification pending**, profile; **log in with email, phone _or_ MDCN**; 2-factor only on a **new** device; forgot/reset
- Institution registration, **document/licence upload**, **organisation sizing** (practitioners · branches · seats · volume) → **recommended plan with real pricing, editable inline**, verify + password, **application pending**, **Facility Admin login**, forgot/reset
- Role selection routes new users; role-based redirect shown on each success screen
- **Staff joining an organisation (S1–S10)** — the person an admin invited on the console's `C5`.
  Invitation → prove it is you → your details → your registration (MDCN / NMCN / MLSCN / PCN, or
  None for front desk and billing) → the undertaking → password → waiting for the seat → in.
  Two entrances: `S1` for somebody new to Medra, **`S9` for somebody who already has an account**,
  where nothing is re-verified because the licence was already theirs. Two honest stops: `S7`
  while a person checks the register, and `S10` when the seven-day link has died.

Offline validation: **ALL 90 CLEAN, FULLY OFFLINE ✓** (`node validate.js`) · **PROTOTYPE COMPLETE ✓**, 90/90 screens reachable, no broken hotspots.

## Nomenclature
People using Medra for their own care are **members**, not "patients". "Patient" is kept only for
the *clinical* context (a doctor's patient list, a consultation note). The role card reads
**"I'm here for my own care."** Alternatives considered: *individual*, *care seeker*, *client*.

## Pricing model (institutions)
| Plan | Price | Includes |
|---|---|---|
| Starter | **₦45,000/mo** | 1 practitioner · 1 branch · core booking & records |
| Practice | **₦120,000/mo** | up to 10 practitioners · 1 branch · staff roles & allocation |
| Group | **₦280,000/mo** | up to 30 practitioners · up to 3 branches · analytics |
| Enterprise | **Custom** | unlimited practitioners & branches · SSO · dedicated support |

Add-ons: **+₦8,000** per extra practitioner/mo · **+₦25,000** per extra branch/mo.
**Annual billing = 2 months free.** Every plan starts with a **30-day free trial, no card**.
Worked example on screen I4: 8 practitioners × 2 branches → Practice ₦120,000 + 1 extra branch
₦25,000 = **₦145,000/mo**. Figures are indicative — validate with the pilot clinics.

## Assumptions (baked in — change if you disagree)
- **Members never need a password.** Verify once → device trusted 30 days → biometric quick unlock.
  A code is only requested on a **new/untrusted device**, or on request.
- **Doctors & admins:** password + 2-factor, but 2FA is **step-up only** (new device), with
  "keep me signed in for 30 days".
- **MDCN** is the doctor identifier. Other cadres use different councils (nurses **NMCN**,
  lab scientists **MLSCN**, pharmacists **PCN**) — add those when staff roles beyond doctors land.
- Copy is inclusive & Nigeria-specific (₦, +234, MDCN, NDPR, languages: English/Hausa/Yoruba/Igbo/Pidgin).
- Imagery is **real licensed Unsplash photography**, chosen for Nigerian/African representation,
  auto-graded with a baked text scrim — see `assets/img/ATTRIBUTION.md`. Regenerate or swap any
  photo with `python3 tools/figma/auth_assets.py`.

## Render (Figma Desktop open + connected)
```powershell
# once per machine — prime the offline icon cache
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force

# creates all four pages, renders every frame, then wires + arranges the prototype
.\render-auth.ps1
```
`render-auth.ps1` runs `link-auth.js` at the end, which:
- **wires the clickable prototype** across pages — 262 links (every desktop + mobile hotspot),
- **arranges** each page (desktop row on top, matching mobile row below, in flow order),
- **sets the flow start** for each page.

It returns `{ linked, framesFound, missing }`. A non-empty `missing` entry means that frame is a
stale render — re-render just that `.jsx` and re-run `figma-cli run .\link-auth.js`.

## Tokens & styles
Uses the same `DESIGN.md` tokens as the design system. To also create the Figma **Variables &
Styles**, run `styles-medra.js` from the `medra-ds` bundle once (shared across the file).

## Preview without Figma
`preview.html` renders all 66 frames in a browser (approximate). `medra-auth-overview.png` is the
contact sheet.
