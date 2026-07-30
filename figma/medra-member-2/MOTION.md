# Medra — Motion spec (Member batch 2)

Same principles as batch 1: motion explains where something came from, stays under ~330 ms, and
uses one easing family so the whole app feels like one hand made it. Batch 2 adds a
**hierarchy direction** — settings and detail screens push in from the side, which is what makes
a deep tree like Profile → Devices → sign-out legible without a breadcrumb.

## Screen transitions (wired by `link-member2.js`)

| Transition | Type | Direction | Duration | Used for |
|---|---|---|---|---|
| Default navigation | Smart Animate | — | **280 ms** | Everything not listed below. Shared layers (doctor avatar, name, date) tween between screens. |
| Push into detail | Move In | Left | **260 ms** | Opening a settings page, a record, a medicine, the access list |
| Pop back | Move Out | Right | **220 ms** | Every `Btn Back` |
| Sheet open | Move In | Bottom | **320 ms** | Share records, request a refill, cancel a visit, add a record, add a reading |
| Sheet close | Move Out | Bottom | **240 ms** | Cancel share, "keep my visit", back from a confirmation |
| Stay on screen | Smart Animate | — | **10 ms** | The sweep for controls whose real behaviour is state, not navigation (toggles, radios, chips) |

Because the doctor's avatar and name keep the same layer names from a visit card → visit detail →
pre-call → in-call → summary, Figma tweens them across the whole telemedicine flow instead of
hard-cutting. That continuity is the point: the member should never wonder whether they are still
in the right appointment.

## Component micro-interactions (in-component, 160 ms Smart Animate)

`components-member2.js` builds six sets on `Medra — Interactive Components · Care`:

| Component | Variants | Interactions |
|---|---|---|
| `Medra/Tab` | Active · Inactive | click → Active, click ⇄ back |
| `Medra/Status Pill` | Confirmed · Completed · Cancelled · Pending · Live | display only — the state comes from data |
| `Medra/Call Control` | On · Off · Idle · End | click ⇄ Off (mute/unmute), hover → Idle |
| `Medra/List Row` | Default · Hover · Pressed | hover → Hover, press → Pressed, release → Default |
| `Medra/Consent Scope` | On · Off · Locked | click ⇄ Off; Locked has no interaction, on purpose |
| `Medra/Dose` | Due · Taken · Missed | click Due → Taken |

`Medra/Consent Scope`'s **Locked** variant is deliberately inert. Allergies and current medicines
are always shared, and a control that looks tappable but silently refuses is worse than one that
reads as locked.

## Motion that belongs in build, not in Figma

- **Skeleton shimmer** — X1's blocks pulse `neutral/200 → neutral/100 → neutral/200` over 1.2 s.
- **Mark-as-taken** — the dose row fills green from the left (220 ms) and the adherence dot pops
  (scale 1 → 1.25 → 1, 180 ms). Optimistic: it reverts with a shake if the write fails.
- **Vitals chart** — bars grow from the baseline, staggered 40 ms apart, once per screen entry.
- **Revoke access** — the row collapses its height to 0 (200 ms) rather than vanishing, so the
  member sees which one went.
- **Reconnecting (W4)** — the wifi-off glyph breathes at 1 s intervals; nothing spins, because a
  spinner implies progress we cannot actually promise.
- **Call controls** — auto-hide after 4 s of no touch, return on tap (fade 160 ms).
- **Live captions** — new lines slide up 8 px and fade in over 140 ms.
- **Haptics** — a light tap on mark-as-taken and on mute; a heavier one on end-call and on
  granting a share, because those two are consequential.

## Reduced motion

P7 has a **Reduce motion** switch. When it is on, every transition above drops to a 120 ms
cross-fade, the skeleton shimmer becomes a static block, and the chart, dose and revoke
animations are removed entirely. In build, default it to on whenever the OS reports
`prefers-reduced-motion`, and let the switch override in either direction.
