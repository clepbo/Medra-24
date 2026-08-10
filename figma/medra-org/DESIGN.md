# Medra — Design Tokens (DESIGN.md)

Single-mode **LIGHT** token set for the Medra design system (Editorial Light direction).
Import with: `figma-cli tokens import-design-md .\DESIGN.md`

> One mode only (Figma Starter allows one). Colours are `#RRGGBB`. Reference in JSX as `var:group/name`.

## Colour

### bg
| Token | Value | Use |
|---|---|---|
| bg/base | #FFFFFF | Page / canvas background |
| bg/subtle | #F4F6F8 | Section panels, muted surfaces |
| bg/muted | #EAF1F5 | Chips, wells, code blocks |
| bg/band | #0F2233 | Navy editorial side band / dark panels |
| bg/band-2 | #143352 | Secondary dark panel |
| bg/inverse | #0F2233 | Dark surfaces |

### brand
| Token | Value | Use |
|---|---|---|
| brand/navy-deep | #0F2233 | Deepest navy, dark backgrounds |
| brand/navy | #1B3A5B | Primary navy, ribbon start, headings |
| brand/blue | #245F88 | Gradient midpoint |
| brand/blue-light | #2F8BAC | Gradient |
| brand/teal | #39B0CF | Primary accent, ribbon end, cross |
| brand/teal-bright | #3BB6D2 | Highlight teal |

### text
| Token | Value | Use |
|---|---|---|
| text/strong | #0F2233 | Headlines |
| text/default | #1B3A5B | Body on light |
| text/muted | #5B6B7A | Secondary / captions |
| text/faint | #91A2B0 | Placeholder, disabled |
| text/on-dark | #FFFFFF | Text on navy/teal |
| text/on-dark-muted | #A9C2D4 | Secondary on navy |
| text/accent | #2F8BAC | Links / accent text |

### border
| Token | Value | Use |
|---|---|---|
| border/subtle | #E6ECF1 | Hairlines, dividers |
| border/default | #D3DEE7 | Card borders, inputs |
| border/strong | #B4C4D1 | Emphasis borders |
| border/accent | #39B0CF | Focus ring / active |

### state
| Token | Value | Use |
|---|---|---|
| state/success | #2FA36B | Confirmed, verified |
| state/success-bg | #E6F5EE | Success surface |
| state/warning | #E0A32E | Pending, trial ending |
| state/warning-bg | #FBF1DD | Warning surface |
| state/error | #D14343 | Cancelled, no-show, errors |
| state/error-bg | #FBE9E9 | Error surface |
| state/info | #2F8BAC | Info, virtual |
| state/info-bg | #E4F0F5 | Info surface |

### neutral
| Token | Value |
|---|---|
| neutral/50 | #F7F9FB |
| neutral/100 | #EEF2F6 |
| neutral/200 | #E1E8EE |
| neutral/300 | #CBD6DF |
| neutral/400 | #A7B6C2 |
| neutral/500 | #7E8F9D |
| neutral/600 | #5B6B7A |
| neutral/700 | #3E4C59 |
| neutral/800 | #26323D |
| neutral/900 | #0F2233 |

## Type scale (reference — apply as size/weight in JSX)
| Token | Size | Weight | Use |
|---|---|---|---|
| display | 72 | bold | Cover / section hero |
| h1 | 48 | bold | Page titles |
| h2 | 32 | bold | Section headers |
| h3 | 24 | semibold | Sub-sections |
| title | 18 | semibold | Card titles |
| body | 16 | regular | Body copy |
| small | 14 | regular | Secondary |
| caption | 12 | medium | Labels, captions (tracked) |

Primary typeface: **Inter** (headings + body). Fallback: system sans.

## Radius
| Token | Value |
|---|---|
| radius/sm | 8 |
| radius/md | 12 |
| radius/lg | 16 |
| radius/xl | 24 |
| radius/pill | 999 |

## Spacing (4-pt base)
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96
