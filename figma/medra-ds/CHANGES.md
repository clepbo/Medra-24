# CHANGES

## v1.0 — Initial delivery (Editorial Light)
Full Medra design system: brand foundations → production-ready UI components.
Aesthetic: white canvas, deep-navy editorial side band, oversized faint section numerals,
teal hairlines, generous whitespace. Grounded in the Medra PRD (roles, booking flow, records).

**21 frames**

| # | Frame | Group |
|---|---|---|
| 00 | Cover | Brand |
| 01 | Contents | Brand |
| 02 | Brand Story | Brand |
| 03 | Brand Goals | Brand |
| 04 | Logo — Primary | Identity |
| 05 | Logo — Construction & Clear Space | Identity |
| 06 | Logo — Variations | Identity |
| 07 | Logo — Misuse | Identity |
| 08 | Colour — Primary | Foundations |
| 09 | Colour — Semantic & Neutrals | Foundations |
| 10 | Gradient & Elevation | Foundations |
| 11 | Typography — Typeface | Foundations |
| 12 | Typography — Scale | Foundations |
| 13 | Iconography | Foundations |
| 14 | Layout — Grid, Spacing & Radius | Foundations |
| 15 | Components — Buttons | Components |
| 16 | Components — Forms & Inputs | Components |
| 17 | Components — Cards | Components |
| 18 | Components — Badges, Status & Alerts | Components |
| 19 | Imagery | Expression |
| 20 | Contact | Brand |

**Prototype:** Cover → Contents → each section; every section has Next + Back-to-Contents;
Contents index rows deep-link to their sections; flow start = Cover. No dead-ends.

**Assets:** 75 Lucide icons (offline), Medra logo set (gradient/reverse/mono/lockups/app-icon),
gradient panels, duotone imagery placeholders, doctor avatars.

**Validation:** ALL 21 CLEAN, FULLY OFFLINE ✓ (0 prop warnings · 0 unknown tokens · no NaN ·
all icons + images resolve).

### Known / next
- Hero uses the vector Medra mark as a placeholder — swap `assets/logo/hero-white.png`
  with the 3D render to embed it (re-render 00 + 20).
- Candidate v1.1 additions: Data tables · Empty/Loading/Error states · Navigation
  (sidebar/topbar/tabbar) · Booking flow walkthrough · Motion & the ECG pulse loader.
