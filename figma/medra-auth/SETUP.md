# Medra — Authentication Module (figma-ds-cli)

**56 frames · 4 Figma pages · Desktop 1440×900 + Mobile 390×844 · Editorial Light+**

Each persona renders onto **its own Figma page**:
`Medra Auth — Entry` · `Medra Auth — Patient` · `Medra Auth — Doctor` · `Medra Auth — Institution`

Covers every requirement, no dead ends:
- Patient registration (phone + OTP), onboarding, login, can't-get-code help, success → home
- Doctor registration (phone + MDCN), OTP, set password, **MDCN verification pending**, profile, login + **2-factor**, forgot/reset, success → dashboard
- Institution registration, **document/licence upload**, plan selection, verify + password, **application pending**, **Facility Admin login**, forgot/reset, success → admin portal
- Role selection routes new users; role-based redirect shown on each success screen

Offline validation: **ALL 56 CLEAN, FULLY OFFLINE ✓** (`node validate.js`).

## Assumptions (baked in — change if you disagree)
- **Patients are passwordless** — OTP each login. **Doctors & admins use password + OTP (2-factor).**
- Copy is inclusive & Nigeria-specific (₦, +234, MDCN, NDPR, languages: English/Hausa/Yoruba/Igbo/Pidgin).
- Imagery is **on-brand generated placeholders** (this environment blocks stock-photo hosts). Swap the
  files in `assets/img/` (`panel-*.png`, `band-*.png`, `success.png`) with licensed photos of Nigerian
  healthcare — same names, similar aspect — and re-render. Nothing else changes.

## Render (Figma Desktop open + connected)
```powershell
# once per machine — prime the offline icon cache
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force

# creates all four pages, renders every frame, then wires + arranges the prototype
.\render-auth.ps1
```
`render-auth.ps1` runs `link-auth.js` at the end, which:
- **wires the clickable prototype** across pages — 176 links (every desktop + mobile hotspot),
- **arranges** each page (desktop row on top, matching mobile row below, in flow order),
- **sets the flow start** for each page.

It returns `{ linked, framesFound, missing }`. A non-empty `missing` entry means that frame is a
stale render — re-render just that `.jsx` and re-run `figma-cli run .\link-auth.js`.

## Tokens & styles
Uses the same `DESIGN.md` tokens as the design system. To also create the Figma **Variables &
Styles**, run `styles-medra.js` from the `medra-ds` bundle once (shared across the file).

## Preview without Figma
`preview.html` renders all 56 frames in a browser (approximate). `medra-auth-overview.png` is the
contact sheet.
