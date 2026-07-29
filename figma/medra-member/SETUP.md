# Medra — Member App (batch 1: Find & Book)

**44 frames · 2 Figma pages · Desktop 1440×900 + Mobile 390×844 · "Soft Clinical"**

- `Medra Member — Find & Book` — 10 screens × desktop + mobile (20 frames)
- `Medra — Interactive Components` — 24 component state frames → real component sets

Offline validation: **ALL 44 CLEAN, FULLY OFFLINE ✓** (`node validate.js`)

## Screens
| # | Screen | Notes |
|---|---|---|
| H1 | **Home** (returning) | Next-visit card, search, specialties, available-today |
| H2 | **Home** (new member) | Empty state — "No visits booked yet" |
| S1 | **Search results** | Filter chips, sort, 24 verified doctors |
| S2 | **Filters** | Bottom sheet on mobile: specialty, availability, type, distance, price, language |
| S3 | **No results** | Widen search + "notify me when a slot opens" |
| P1 | **Doctor profile** | Stats, about, languages, fee, availability |
| B1 | **Choose a time** | Date strip, slot grid (taken slots disabled), in-person vs virtual |
| B2 | **Slot just taken** | Concurrency edge case → nearest open times |
| B3 | **Review & confirm** | Full summary, reason for visit, data-sharing note, SMS opt-in |
| C1 | **Booking confirmed** | Reference number, details, SMS note, add to calendar |

No dead ends: every screen has a back path, a home path, and bottom-nav/sidebar escape.
`link-member.js` also **closes the auth dead-end** — auth success and quick-unlock now land on
the member home.

## Render (Figma Desktop open + connected)
```powershell
.\render-member.ps1
```
This creates both pages, renders every frame, then runs:
1. `components-medra.js` — converts `cmp/*` frames into **interactive components**
2. `link-member.js` — wires the **prototype with motion** and arranges the canvas

## Interactive components
`components-medra.js` turns each `cmp/<Component>/State=<Value>` frame into a Figma
**component set** named `Medra/<Component>` with a `State` variant property, then wires
interactions **inside** the component with Smart Animate (160 ms, gentle):

| Component | Variants | Interactions |
|---|---|---|
| `Medra/Button Primary` | Default · Hover · Pressed · Loading · Disabled | hover → Hover, press → Pressed, release → Default |
| `Medra/Input` | Default · Focus · Filled · Error | hover/press → Focus |
| `Medra/Time Slot` | Available · Hover · Selected · Taken | hover → Hover, click ⇄ Selected |
| `Medra/Specialty Chip` | Default · Hover · Selected | hover → Hover, click ⇄ Selected |
| `Medra/Toggle` | On · Off | click ⇄ |
| `Medra/Checkbox` | Checked · Unchecked | click ⇄ |
| `Medra/Nav Item` | Active · Inactive | click → Active |
| `Medra/Doctor Card` | Default · Hover | hover ⇄ |

Drop any of these into a screen and it animates on its own — no prototype wiring needed.
The script is idempotent (it removes previous `Medra/*` sets first) and returns
`{ sets, variants, reactions, components, notes }`.

See `MOTION.md` for the animation spec.
