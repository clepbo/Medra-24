# Medra — Organisation module

**217 frames · 8 Figma pages · Desktop 1440 + mobile 390 · organisation-module only**

57 desktop screens covering PRD v2.0 Modules 10–13. On mobile each is a hub with its own sections
and sheets — 141 mobile frames — plus 19 component-state frames.

Offline validation
- `node validate.js` → **ALL 217 CLEAN, FULLY OFFLINE ✓** (222 icons, 41 tokens, 0 warnings)
- headless measurement → **0 horizontal overflow** at 390 and 1440; mobile median 844px, max 1,437px
- `python3 tools/figma/proto_check.py figma/medra-org link-org.js` → **PROTOTYPE COMPLETE ✓**,
  197/197 screens reachable, 699 explicit links, no broken hotspots

## 1. It is a third product, not a re-skin

| | Member | Doctor | Organisation |
|---|---|---|---|
| Ground | soft blue mesh | soft blue, white floating card | **warm graphite on off-white** |
| Navigation | 262px navy sidebar | 206px navy sidebar + light rail | **88px icon rail + persistent context bar** |
| Context | none needed | the patient | **branch × department switcher, always visible** |
| Accent | teal | navy + coral | **amber** |
| Density | one thing at a time | a clinic day | **a board — queues, tables, allocation** |
| Mobile | light appbar, 5 tabs | gradient header, 5 tabs | graphite header, **role-aware tabs** |

The context bar is the piece that makes it an organisation console. An admin's first question is
never "which page" but **"which branch, which department"**, and every number on every screen is
relative to that answer — so it never scrolls away.

**The mobile tab bar changes with the role.** An admin, a nurse and a front desk do not want the
same five destinations, so there are three bars over one shell: admin (Today · Bookings · People ·
Referrals · More), staff (My queue · Members · Referrals · Alerts · More) and front desk
(Front desk · Bookings · Walk-in · Members · More).

## 2. Screens

### 1 · Setup & verification
A1 Setup checklist · A2 Verification (RC + licence + documents + contact person) · A3 Branches ·
A4 Plan & seats · A5 Public profile

### 2 · Today & bookings
B1 Today across the organisation · B2 Bookings & allocation · B3 Find a member

### 3 · Departments & people
C1 Departments · C2 Department detail · C3 Add a department · C4 People · C5 Invite someone ·
C6 Person detail · C7 Roles & permissions

### 4 · The clinical chain
**Nursing** D1 My queue · D2 Record vitals · D3 Administer & record · D4 Escalate
**Laboratory** D5 Order queue · D6 Order · D7 Enter structured result · D8 Sample problem
**Pharmacy** D9 Prescription queue · D10 Dispense · D11 Cannot dispense
**Front desk** D12 The day · D13 Register a walk-in · D14 Check in & payment

### 5 · Referrals & external access
E1 Referred out · E2 Refer someone · E3 Referral sent · E4 Referred to us · E5 Referral detail ·
E6 Single-use links · **E7–E11 the external party's own screens** (privacy notice → the task →
upload → done → expired)

### 6 · Access, money & reports
F1 Who has access · F2 Audit log · F3 Privacy & compliance · F4 Reports · F5 Settings ·
F6 Subscription

### 7 · States
X1 Seats full · X2 Not verified · X3 Locked · X4 Nothing booked · X5 Offline · X6 Error ·
X7 Loading

## 3. Three things worth reviewing carefully

**The external party's five screens (E7–E11)** have no navigation at all. Nobody there has an
account, has been trained, or will come back. They are a page on a stranger's phone — privacy
notice, what you are asked to do, a short structured upload, done. The link dies when they finish.

**The two hard denials** are visible product, not a settings page: front desk cannot read clinical
content, and a lab technician cannot release a result. `C7` states both with the reasoning.

**`unverified()`** is a component with two states and it appears wherever a self-reported value
does — including inside a nurse's view and an external party's. The label is part of the datum.

## 4. Render — organisation module only

See `CLI-PROMPT.md`. `.\render-org.ps1` creates the eight `Medra Org —` pages and touches nothing
else. Re-rendering **appends** — delete old frames first if a page already has them.
