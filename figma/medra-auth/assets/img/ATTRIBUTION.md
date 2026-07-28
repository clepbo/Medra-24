# Imagery — credits & licence

Photography is **real, licensed stock from [Unsplash](https://unsplash.com)**, chosen for
Nigerian / African representation in healthcare. The Unsplash Licence permits free commercial
use; attribution is not required but is good practice, so it is recorded here.

| File(s) | Unsplash photo ID | Subject |
|---|---|---|
| `d-panel-patient.jpg`, `m-hero-patient.jpg` | `photo-1531123897727-8f129e1688ce` | Woman portrait — patient |
| `d-panel-doctor.jpg`, `m-hero-doctor.jpg`, `onb-1.jpg`, `avatar-1.jpg` | `photo-1622253692010-333f2da6031d` | Doctor in scrubs with stethoscope |
| `onb-2.jpg`, `proof-phone.jpg` | `photo-1576091160399-112ba8d25d1d` | Doctor booking on a phone |
| `d-panel-institution.jpg`, `m-hero-institution.jpg` | `photo-1666214280557-f1b5022eb634` | Clinical team at work |
| `onb-3.jpg`, `proof-lab.jpg` | `photo-1609188076864-c35269136b09` | Laboratory / diagnostics |
| `success.jpg`, `avatar-2.jpg` | `photo-1573497019940-1c28c88b4f3e` | Professional portrait |
| `avatar-3.jpg` | `photo-1594824476967-48c8b964273f` | Clinician in teal scrubs |

View any photo at `https://unsplash.com/photos/<id>`.

## Processing applied (see `tools/figma/auth_assets.py`)
1. Cropped to the target aspect with face-aware cropping.
2. Subtle cool **brand grade** so photography sits with the navy→teal palette.
3. A baked **bottom-up scrim** so white headline/body text is always legible (WCAG-safe).

## Generated (not photographic)
`surface-mobile.jpg`, `surface-desktop.jpg` (soft mesh grounds), `btn-teal.jpg`,
`btn-navy.jpg` (gradient CTA pills), `pulse-teal.png`, `pulse-white.png` (the ECG motif).

To swap in your own photography: replace a file with the same name and similar aspect ratio,
then re-render the affected frames. Re-running `auth_assets.py` re-downloads and re-processes.
