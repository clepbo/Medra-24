# Medra — Motion spec

Motion is applied two ways: **screen transitions** (wired by `link-member.js`) and
**component micro-interactions** (baked into the interactive components).

## Principles
1. **Motion explains, it doesn't perform.** Every animation shows where something came from.
2. **Fast enough to feel instant** — 160–320 ms. Nothing over ~330 ms.
3. **One easing family** — `GENTLE` (a soft ease-out) so the whole app feels like one hand made it.
4. **Respect reduced motion** — in build, honour `prefers-reduced-motion` by dropping to a cross-fade.

## Screen transitions
| Transition | Type | Direction | Duration | Used for |
|---|---|---|---|---|
| Default navigation | Smart Animate | — | **280 ms** | Home → results → profile → booking. Shared elements (doctor avatar, name, fee) glide between screens. |
| Sheet open | Move In | Bottom | **320 ms** | Filters, sort |
| Sheet close | Move Out | Bottom | **240 ms** | Apply, reset, close |

Smart Animate is deliberate: because the doctor avatar/name/fee keep the same layer names
across Home → Results → Profile → Review → Confirmed, Figma **tweens them between screens**
instead of hard-cutting. That's what makes the booking flow feel continuous.

## Component micro-interactions (in-component, 160 ms Smart Animate)
- **Buttons** lift on hover, compress on press.
- **Time slots** tint on hover, fill navy on select — the core booking gesture.
- **Specialty chips** outline on hover, fill on select.
- **Toggles / checkboxes** slide and fill.
- **Nav items** shift muted → teal.
- **Doctor cards** raise their border on hover.

## Recommended additions for build (beyond Figma's capability)
- **Skeleton loaders** on search results and availability (shimmer, 1.2 s loop).
- **Success pulse** on booking confirmation — the ECG motif drawing once (~600 ms).
- **Optimistic slot lock** — the slot animates to Selected immediately, reverting with a shake if the server says it's taken (that's the B2 screen).
- **Haptic tap** on slot select and confirm (mobile).
