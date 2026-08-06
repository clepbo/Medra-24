# Medra Doctor — motion spec

The doctor app is used between patients, so motion here is shorter than the member app's:
**260 ms default rather than 280 ms**, and nothing decorative. A doctor with someone waiting
should never be watching an animation finish.

## Screen transitions (wired by `link-doctor.js`)

| Transition | Type | Direction | Duration | Used for |
|---|---|---|---|---|
| Default | Smart Animate | — | **260 ms** | Sidebar, tab bar, top bar, right rail, everything not listed below |
| Push into detail | Move In | Left | **240 ms** | Opening a patient record, a settings page, the file before a consultation |
| Pop back | Move Out | Right | **200 ms** | Every `Btn Back` |
| Attach to a visit | Move In | Bottom | **300 ms** | Prescribe, order tests, upload a result, refer, templates, running late, outcome |
| Stay on screen | Smart Animate | — | **10 ms** | Toggles, radios, filters — controls whose real behaviour is state, not navigation |

The state switcher on the States page uses the default 260 ms Smart Animate. It is a review
control, not a real one — it exists so the page can be clicked through.

The patient's avatar, name and Medra ID keep the same layer names from the queue → the file →
the consultation room → review → signed, so Figma tweens them across the whole spine. That
continuity is the point: a doctor must never wonder which patient a screen belongs to.

## In-component (160 ms Smart Animate)

| Component | Variants | Interaction |
|---|---|---|
| `Medra Doctor/Slot` | Open · Booked · Held · Break · Away | click ⇄ Booked |
| `Medra Doctor/Queue Row` | Waiting · Now · Unpaid | hover ⇄ Now |
| `Medra Doctor/Share Toggle` | Shared · Withheld | click ⇄ |
| `Medra Doctor/Scope Line` | Granted · Locked | display only — Locked is inert on purpose |
| `Medra Doctor/Drug Result` | Default · Blocked | display only — Blocked must not look tappable |
| `Medra Doctor/Stat Tile` | Info · Warning · Danger · Good | display only |
| `Medra Doctor/Checklist Row` | Todo · Done | click → Done |
| `Medra Doctor/Outcome` | Default · Selected | click ⇄ |
| `Medra Doctor/Rail Item` | Inactive · Active | hover ⇄ |

`Drug Result / Blocked` and `Scope Line / Locked` are deliberately inert. A control that looks
tappable and then silently refuses is worse than one that reads as blocked — and in a
prescribing screen that difference is a safety property, not a style choice.

## Belongs in build, not in Figma

- **Autosave pulse** — the "Autosaved" chip fades in for 900 ms whenever the note is written.
  A doctor mid-consultation needs to know their typing is safe without being told twice.
- **Elapsed timer** — counts in real time; the digits turn amber at the booked length and red at
  1.5×, so overrunning is visible without a modal.
- **Queue re-order** — when a patient is marked complete, their row collapses (200 ms) and the
  next row lifts into the "Now" state. Never a full-page refresh.
- **Allergy block** — the blocked drug row shakes 4 px twice (180 ms). It is the one place a
  jolt is warranted.
- **Signing** — the button fills left to right over the network round trip, then the note card
  settles with the signature block fading in. Signing is irreversible; it should feel like it.
- **Offline** — an amber bar slides down 32 px beneath the top bar and stays. Queued items count
  up in place.
- **Right rail** — the month calendar and "Next up" cards cross-fade (200 ms) when the section
  changes; they never slide, because the rail is a fixed column and sliding reads as navigation.
- **Progress bars and the donut** (K1) — animate from 0 on first paint of the day only, 600 ms,
  then never again. A bar that re-animates on every return is noise.
- **Skeletons** — pulse `neutral/200 → neutral/100` over 1.2 s.
- **Reduce motion** — everything above drops to a 120 ms cross-fade; the shake and the timer
  colour change stay, because they are information rather than decoration.
