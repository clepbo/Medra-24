<p align="center">
  <img src="brand/png/medra-logo-primary.png" alt="Medra" width="240" />
</p>

<h1 align="center">Medra</h1>

**A unified medical records & consultation-booking platform for Nigeria.**

Private healthcare in Abuja runs on paper files and WhatsApp diaries: records are siloed per
hospital, people physically carry printed results, and a new doctor sees no prior history. Medra
replaces that with one system for records, bookings, staff work and institutional data. Members
find verified doctors and organisations, see real availability, book and pay before leaving home,
and carry a portable record between institutions. Organisations pay a subscription; **members are
never charged.**

- **Launch market:** Abuja (pilot: 3–5 private clinics)
- **Platform:** mobile-responsive web (MVP) — every screen designed at 1440 and 390
- **Business model:** organisation/practitioner subscription, priced by practitioners, branches
  and seats; free for members
- **Vocabulary:** a person using Medra for their own care is a **member**, never a "patient"
  (decided at the 9 August 2026 review)

---

## Where the design is

**Complete and in Figma.** 839 frames across five bundles — authentication, the member app, the
doctor module, the organisation (eight personas, each with its own navigation) and the design
system — all wired into clickable prototypes and arranged on the canvas by **what a person can
do** rather than by which module built it.

| | |
|---|---:|
| Personas | 12 |
| Functions | 70 |
| Screen frames in Figma | 839 |
| Components | 87 |

**Start here: [the flow map](docs/site/index.html)** — every function, each one a link straight
into Figma playback at its first screen. It is a standalone page; open it from disk, or read it
served once GitHub Pages is enabled on this branch's `/docs` folder.

## Documentation

- 🩺 [**Flow map**](docs/site/index.html) — what the product does, function by function, each
  linking into the prototype. The fastest way in.
- 📄 [**PRD v2.0**](docs/Medra_PRD_v2.0.md) — the current spec: goals, personas, roles and
  permissions, MVP modules, user stories, security and data requirements, data model, roadmap and
  open questions. ([v1.0](docs/Medra_PRD.md) is kept and marked superseded.)
- 🛠 [**HANDOFF.md**](HANDOFF.md) — everything needed to pick the project up cold: what is
  designed, how the design is produced, how it is rendered into Figma, and what is left.
- 📋 [**Functions.md**](docs/Functions.md) — the readable inventory behind the flow map, generated
  from `tools/figma/functions.py`.
- 🧪 [**Clinical_Templates.md**](docs/Clinical_Templates.md) — the examination template and the
  private-notes grounds, with sources. **Both are waiting on a clinician**, not on a designer.
- 🗒 [**Review_14Aug2026.md**](docs/Review_14Aug2026.md) — the doctor-module review and what it
  changed.

## MVP in one paragraph

Medra MVP is a mobile-responsive web app where a member registers with their phone number,
searches for a verified doctor in Abuja, sees their real availability, books an appointment
(in-person or virtual), pays before the visit, receives an SMS confirmation and reminders, and
reads the consultation note the doctor writes afterwards. The doctor gets a dashboard of today's
schedule, confirms or declines bookings, and writes a structured note against a prepared record —
prepared because the nurse, the laboratory and the pharmacy enter their own work into the same
episode. The organisation admin sees all of it, onboards departments and staff, and buys seats.
The clinic pays a monthly subscription after a 30-day free trial.
