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

## v1.1 — Clean logo + canvas arrangement
- **Logo:** replaced the glowing 3D treatment with the **clean vector mark** plus a
  **subtle soft glow** (the 3D render's bloom is baked into its brightest pixels and can't be
  cleanly separated). Cover uses the gradient mark on a light panel; Contact uses the reverse
  mark on navy; Variations gains a "Soft glow (hero)" tile. New assets:
  `logo-primary-glow.png`, `hero-white-glow.png`. Removed `logo-3d.png`.
- **Canvas layout:** `link-medra.js` now **arranges the 21 frames into grouped section rows**
  (Brand · Identity · Foundations · Components · Expression) instead of one horizontal line.

## v1.2 — Official logos + Variables & Styles
- All logo art swapped to the **official Medra SVG set** (Gradient, Navy, Teal, White,
  Inverse, Stroke) across cover, logo pages, variations + lockups, contact and sidebar;
  glow / app-icon / favicon / lockups regenerated from the real mark.
- Added **`styles-medra.js`** — creates Figma **Variables** (Medra Colour collection +
  Medra Scale spacing/radius) and **Styles** (paint, text `Medra/Display…Caption`, and
  effect `Medra/Elevation/E1, E2, Focus Ring`). Run via `figma-cli run .\styles-medra.js`
  (see SETUP step 3b). Idempotent.

### Known / next
- Hero uses the vector Medra mark as a placeholder — swap `assets/logo/hero-white.png`
  with the 3D render to embed it (re-render 00 + 20).
- Candidate v1.1 additions: Data tables · Empty/Loading/Error states · Navigation
  (sidebar/topbar/tabbar) · Booking flow walkthrough · Motion & the ECG pulse loader.
