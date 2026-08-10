# Medra Member app — render + wire (Figma Desktop open + connected).
# Member-module only: it creates and fills the eight 'Medra Member —' pages and nothing else.

# 1. prime the offline icon cache (safe to re-run)
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force

# 2. tokens — the same 41 tokens as every other Medra bundle, so this is a no-op
figma-cli tokens import-design-md .\DESIGN.md

# ---- Medra Member — 1 Find & Book ----
figma-cli eval "(async()=>{const t='Medra Member — 1 Find & Book';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('H1-home-d.jsx', 'H1-home-m.jsx', 'H2-home-empty-d.jsx', 'H2-home-empty-m.jsx', 'S1-results-d.jsx', 'S1-results-m.jsx', 'S2-filters-d.jsx', 'S2-filters-m.jsx', 'S3-empty-d.jsx', 'S3-empty-m.jsx', 'P1-profile-d.jsx', 'P1-profile-m.jsx', 'B1-slot-d.jsx', 'B1-slot-m.jsx', 'B2-taken-d.jsx', 'B2-taken-m.jsx', 'B3-review-d.jsx', 'B3-review-m.jsx', 'B4-payment-d.jsx', 'B4-payment-m.jsx', 'C1-confirmed-d.jsx', 'C1-confirmed-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 2 Visits & Virtual Care ----
figma-cli eval "(async()=>{const t='Medra Member — 2 Visits & Virtual Care';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('V1-visits-d.jsx', 'V1-visits-m.jsx', 'V2-past-d.jsx', 'V2-past-m.jsx', 'V3-visits-empty-d.jsx', 'V3-visits-empty-m.jsx', 'V4-visit-d.jsx', 'V4-visit-m.jsx', 'V5-reschedule-d.jsx', 'V5-reschedule-m.jsx', 'V6-cancel-d.jsx', 'V6-cancel-m.jsx', 'V7-cancelled-d.jsx', 'V7-cancelled-m.jsx', 'W1-precall-d.jsx', 'W1-precall-m.jsx', 'W2-incall-d.jsx', 'W2-incall-m.jsx', 'W3-callend-d.jsx', 'W3-callend-m.jsx', 'W4-lost-d.jsx', 'W4-lost-m.jsx', 'W0-join-d.jsx', 'W0-join-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 3 Records ----
figma-cli eval "(async()=>{const t='Medra Member — 3 Records';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('R1-records-d.jsx', 'R1-records-m.jsx', 'R2-note-d.jsx', 'R2-note-m.jsx', 'R3-lab-d.jsx', 'R3-lab-m.jsx', 'R4-vitals-d.jsx', 'R4-vitals-m.jsx', 'R5-share-d.jsx', 'R5-share-m.jsx', 'R6-access-d.jsx', 'R6-access-m.jsx', 'R7-upload-d.jsx', 'R7-upload-m.jsx', 'R8-added-d.jsx', 'R8-added-m.jsx', 'R9-records-empty-d.jsx', 'R9-records-empty-m.jsx', 'R10-summary-d.jsx', 'R10-summary-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 4 Medicines ----
figma-cli eval "(async()=>{const t='Medra Member — 4 Medicines';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('M1-meds-d.jsx', 'M1-meds-m.jsx', 'M2-med-d.jsx', 'M2-med-m.jsx', 'M3-refill-d.jsx', 'M3-refill-m.jsx', 'M4-reminders-d.jsx', 'M4-reminders-m.jsx', 'M5-meds-empty-d.jsx', 'M5-meds-empty-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 5 Profile & Settings ----
figma-cli eval "(async()=>{const t='Medra Member — 5 Profile & Settings';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('P0-profile-d.jsx', 'P0-profile-m.jsx', 'P2-details-d.jsx', 'P2-details-m.jsx', 'P3-dependants-d.jsx', 'P3-dependants-m.jsx', 'P4-add-dependant-d.jsx', 'P4-add-dependant-m.jsx', 'P5-security-d.jsx', 'P5-security-m.jsx', 'P6-notifs-d.jsx', 'P6-notifs-m.jsx', 'P7-language-d.jsx', 'P7-language-m.jsx', 'P8-privacy-d.jsx', 'P8-privacy-m.jsx', 'P9-delete-d.jsx', 'P9-delete-m.jsx', 'P3b-family-d.jsx', 'P3b-family-m.jsx', 'P9b-delete-confirm-d.jsx', 'P9b-delete-confirm-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 6 Alerts ----
figma-cli eval "(async()=>{const t='Medra Member — 6 Alerts';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('N1-notifs-d.jsx', 'N1-notifs-m.jsx', 'N2-notifs-empty-d.jsx', 'N2-notifs-empty-m.jsx', 'N0-panel-d.jsx', 'N0-panel-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 7 System States ----
figma-cli eval "(async()=>{const t='Medra Member — 7 System States';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('X1-loading-d.jsx', 'X1-loading-m.jsx', 'X2-offline-d.jsx', 'X2-offline-m.jsx', 'X3-error-d.jsx', 'X3-error-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Member — 8 Components ----
figma-cli eval "(async()=>{const t='Medra Member — 8 Components';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('CMP-ButtonPrimary-State-Default.jsx', 'CMP-ButtonPrimary-State-Hover.jsx', 'CMP-ButtonPrimary-State-Pressed.jsx', 'CMP-ButtonPrimary-State-Loading.jsx', 'CMP-ButtonPrimary-State-Disabled.jsx', 'CMP-Input-State-Default.jsx', 'CMP-Input-State-Focus.jsx', 'CMP-Input-State-Filled.jsx', 'CMP-Input-State-Error.jsx', 'CMP-TimeSlot-State-Available.jsx', 'CMP-TimeSlot-State-Hover.jsx', 'CMP-TimeSlot-State-Selected.jsx', 'CMP-TimeSlot-State-Taken.jsx', 'CMP-SpecialtyChip-State-Default.jsx', 'CMP-SpecialtyChip-State-Hover.jsx', 'CMP-SpecialtyChip-State-Selected.jsx', 'CMP-Toggle-State-On.jsx', 'CMP-Toggle-State-Off.jsx', 'CMP-Checkbox-State-Checked.jsx', 'CMP-Checkbox-State-Unchecked.jsx', 'CMP-NavItem-State-Active.jsx', 'CMP-NavItem-State-Inactive.jsx', 'CMP-DoctorCard-State-Default.jsx', 'CMP-DoctorCard-State-Hover.jsx', 'CMP-Tab-State-Active.jsx', 'CMP-Tab-State-Inactive.jsx', 'CMP-StatusPill-State-Confirmed.jsx', 'CMP-StatusPill-State-Completed.jsx', 'CMP-StatusPill-State-Cancelled.jsx', 'CMP-StatusPill-State-Pending.jsx', 'CMP-StatusPill-State-Live.jsx', 'CMP-CallControl-State-On.jsx', 'CMP-CallControl-State-Off.jsx', 'CMP-CallControl-State-Idle.jsx', 'CMP-CallControl-State-End.jsx', 'CMP-ListRow-State-Default.jsx', 'CMP-ListRow-State-Hover.jsx', 'CMP-ListRow-State-Pressed.jsx', 'CMP-ConsentScope-State-On.jsx', 'CMP-ConsentScope-State-Off.jsx', 'CMP-ConsentScope-State-Locked.jsx', 'CMP-Dose-State-Due.jsx', 'CMP-Dose-State-Taken.jsx', 'CMP-Dose-State-Missed.jsx')) { figma-cli render (Get-Content $f -Raw) }

# 3. turn the cmp/* frames into real interactive component sets
figma-cli run .\components-member.js

# 4. wire the prototype, close the nav, arrange the canvas
figma-cli run .\link-member.js