# ============================================================================
# Medra — DOCTOR MODULE ONLY.
# Renders the eight 'Medra Doctor —' pages and nothing else. It does not touch the
# design-system, authentication or member pages: it creates its own pages, renders
# into them, and wires only frames whose names begin with 'Doctor · '.
# Requires: Figma Desktop open, the file open, figma-ds-cli connected.
# ============================================================================

# 1. prime the offline icon cache (safe to re-run)
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force

# 2. tokens — the same 41 tokens as every other Medra bundle, so this is a no-op
#    if you have already imported them. It never removes or renames anything.
figma-cli tokens import-design-md .\DESIGN.md

# ---- Medra Doctor — 1 Getting Started ----
figma-cli eval "(async()=>{const t='Medra Doctor — 1 Getting Started';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('G1-checklist-d.jsx', 'G1-checklist-m.jsx', 'G2-verification-d.jsx', 'G2-verification-m.jsx', 'G3-invite-d.jsx', 'G3-invite-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 2 Today & Schedule ----
figma-cli eval "(async()=>{const t='Medra Doctor — 2 Today & Schedule';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('K1-today-d.jsx', 'K1-today-m.jsx', 'K2-requests-d.jsx', 'K2-requests-m.jsx', 'K3-late-d.jsx', 'K3-late-m.jsx', 'K4-file-d.jsx', 'K4-file-m.jsx', 'K5-outcome-d.jsx', 'K5-outcome-m.jsx', 'K6-week-d.jsx', 'K6-week-m.jsx', 'K7-availability-d.jsx', 'K7-availability-m.jsx', 'K8-timeoff-d.jsx', 'K8-timeoff-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 3 Consultation ----
figma-cli eval "(async()=>{const t='Medra Doctor — 3 Consultation';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('C1-room-d.jsx', 'C1-room-m.jsx', 'C2-templates-d.jsx', 'C2-templates-m.jsx', 'C3-prescribe-d.jsx', 'C3-prescribe-m.jsx', 'C4-tests-d.jsx', 'C4-tests-m.jsx', 'C5-upload-d.jsx', 'C5-upload-m.jsx', 'C6-refer-d.jsx', 'C6-refer-m.jsx', 'C7-sign-d.jsx', 'C7-sign-m.jsx', 'C8-signed-d.jsx', 'C8-signed-m.jsx', 'C9-drafts-d.jsx', 'C9-drafts-m.jsx', 'C10-virtual-d.jsx', 'C10-virtual-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 4 Patients ----
figma-cli eval "(async()=>{const t='Medra Doctor — 4 Patients';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('P1-patients-d.jsx', 'P1-patients-m.jsx', 'P2-record-d.jsx', 'P2-record-m.jsx', 'P3-access-d.jsx', 'P3-access-m.jsx', 'P4-followups-d.jsx', 'P4-followups-m.jsx', 'P5-messages-d.jsx', 'P5-messages-m.jsx', 'P6-refills-d.jsx', 'P6-refills-m.jsx', 'P7-results-d.jsx', 'P7-results-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 5 Practice & Money ----
figma-cli eval "(async()=>{const t='Medra Doctor — 5 Practice & Money';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('S1-profile-d.jsx', 'S1-profile-m.jsx', 'S2-fees-d.jsx', 'S2-fees-m.jsx', 'S3-virtual-d.jsx', 'S3-virtual-m.jsx', 'S4-contact-d.jsx', 'S4-contact-m.jsx', 'S5-earnings-d.jsx', 'S5-earnings-m.jsx', 'S6-billing-d.jsx', 'S6-billing-m.jsx', 'S7-practice-d.jsx', 'S7-practice-m.jsx', 'S8-security-d.jsx', 'S8-security-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 6 Growth ----
figma-cli eval "(async()=>{const t='Medra Doctor — 6 Growth';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('R1-insights-d.jsx', 'R1-insights-m.jsx', 'R2-reviews-d.jsx', 'R2-reviews-m.jsx', 'R3-link-d.jsx', 'R3-link-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 7 States & Edge Cases ----
figma-cli eval "(async()=>{const t='Medra Doctor — 7 States & Edge Cases';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('X1-locked-d.jsx', 'X1-locked-m.jsx', 'X2-empty-d.jsx', 'X2-empty-m.jsx', 'X3-notifications-d.jsx', 'X3-notifications-m.jsx', 'X4-offline-d.jsx', 'X4-offline-m.jsx', 'X5-error-d.jsx', 'X5-error-m.jsx', 'X6-loading-d.jsx', 'X6-loading-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 8 Components ----
figma-cli eval "(async()=>{const t='Medra Doctor — 8 Components';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('CMP-Slot-State-Open.jsx', 'CMP-Slot-State-Booked.jsx', 'CMP-Slot-State-Held.jsx', 'CMP-Slot-State-Break.jsx', 'CMP-Slot-State-Away.jsx', 'CMP-QueueRow-State-Waiting.jsx', 'CMP-QueueRow-State-Now.jsx', 'CMP-QueueRow-State-Unpaid.jsx', 'CMP-ShareToggle-State-Shared.jsx', 'CMP-ShareToggle-State-Withheld.jsx', 'CMP-ScopeLine-State-Granted.jsx', 'CMP-ScopeLine-State-Locked.jsx', 'CMP-DrugResult-State-Default.jsx', 'CMP-DrugResult-State-Blocked.jsx', 'CMP-StatTile-State-Info.jsx', 'CMP-StatTile-State-Warning.jsx', 'CMP-StatTile-State-Danger.jsx', 'CMP-StatTile-State-Good.jsx', 'CMP-ChecklistRow-State-Done.jsx', 'CMP-ChecklistRow-State-Todo.jsx', 'CMP-Outcome-State-Selected.jsx', 'CMP-Outcome-State-Default.jsx', 'CMP-RailItem-State-Active.jsx', 'CMP-RailItem-State-Inactive.jsx')) { figma-cli render (Get-Content $f -Raw) }

# 3. turn the cmp/* frames into interactive component sets (doctor page only)
figma-cli run .\components-doctor.js

# 4. wire the prototype, close the navigation, arrange the canvas
figma-cli run .\link-doctor.js

# Expected: link-doctor.js returns { linked, navLinked, stayOnScreen, framesFound, missing }.
# A non-empty 'missing' means that frame did not render — re-render that one .jsx and re-run step 4.