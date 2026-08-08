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
foreach ($f in @('G1-checklist-d.jsx', 'G1-checklist-m.jsx', 'G1-checklist-m-steps.jsx', 'G1-checklist-m-why.jsx', 'G2-verification-d.jsx', 'G2-verification-m.jsx', 'G2-verification-m-steps.jsx', 'G2-verification-m-docs.jsx', 'G2-verification-m-meanwhile.jsx', 'G2-verification-m-faq.jsx', 'G3-invite-d.jsx', 'G3-invite-m.jsx', 'G3-invite-m-sent.jsx', 'G3-invite-m-how.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 2 Today & Schedule ----
figma-cli eval "(async()=>{const t='Medra Doctor — 2 Today & Schedule';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('K1-today-d.jsx', 'K1-today-m.jsx', 'K1-today-m-waiting.jsx', 'K1-today-m-also.jsx', 'K1-today-m-rest.jsx', 'K1-today-m-files.jsx', 'K1-today-m-quick-sheet.jsx', 'K2-requests-d.jsx', 'K2-requests-m.jsx', 'K2-requests-m-bookings.jsx', 'K2-requests-m-other.jsx', 'K2-requests-m-rules.jsx', 'K3-late-d.jsx', 'K3-late-m.jsx', 'K3-late-m-msg.jsx', 'K3-late-m-who.jsx', 'K4-file-d.jsx', 'K4-file-m.jsx', 'K4-file-m-why.jsx', 'K4-file-m-shared.jsx', 'K4-file-m-last.jsx', 'K4-file-m-prep.jsx', 'K4-file-m-reach-sheet.jsx', 'K5-outcome-d.jsx', 'K5-outcome-m.jsx', 'K5-outcome-m-means.jsx', 'K5-outcome-m-note.jsx', 'K6-week-d.jsx', 'K6-week-m.jsx', 'K6-week-m-day.jsx', 'K6-week-m-week.jsx', 'K6-week-m-edit-sheet.jsx', 'K7-availability-d.jsx', 'K7-availability-m.jsx', 'K7-availability-m-days.jsx', 'K7-availability-m-rules.jsx', 'K7-availability-m-breaks.jsx', 'K7-availability-m-where.jsx', 'K8-timeoff-d.jsx', 'K8-timeoff-m.jsx', 'K8-timeoff-m-impact.jsx', 'K8-timeoff-m-who.jsx', 'K8-timeoff-m-cover.jsx', 'K9-more-d.jsx', 'K9-more-m.jsx', 'K9-more-m-clinical.jsx', 'K9-more-m-business.jsx', 'K9-more-m-account.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 3 Consultation ----
figma-cli eval "(async()=>{const t='Medra Doctor — 3 Consultation';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('C1-room-d.jsx', 'C1-room-m.jsx', 'C1-room-m-note.jsx', 'C1-room-m-side.jsx', 'C1-room-m-flagged.jsx', 'C1-room-m-add-sheet.jsx', 'C2-templates-d.jsx', 'C2-templates-m.jsx', 'C2-templates-m-preview.jsx', 'C2-templates-m-settings.jsx', 'C3-prescribe-d.jsx', 'C3-prescribe-m.jsx', 'C3-prescribe-m-builder.jsx', 'C3-prescribe-m-current.jsx', 'C3-prescribe-m-checks.jsx', 'C4-tests-d.jsx', 'C4-tests-m.jsx', 'C4-tests-m-order.jsx', 'C4-tests-m-where.jsx', 'C4-tests-m-note.jsx', 'C5-upload-d.jsx', 'C5-upload-m.jsx', 'C5-upload-m-read.jsx', 'C5-upload-m-explain.jsx', 'C5-upload-m-queue.jsx', 'C6-refer-d.jsx', 'C6-refer-m.jsx', 'C6-refer-m-letter.jsx', 'C6-refer-m-what.jsx', 'C7-sign-d.jsx', 'C7-sign-m.jsx', 'C7-sign-m-share.jsx', 'C7-sign-m-also.jsx', 'C7-sign-m-preview.jsx', 'C8-signed-d.jsx', 'C8-signed-m.jsx', 'C9-drafts-d.jsx', 'C9-drafts-m.jsx', 'C9-drafts-m-why.jsx', 'C9-drafts-m-stop.jsx', 'C10-virtual-d.jsx', 'C10-virtual-m.jsx', 'C10-virtual-m-sent.jsx', 'C10-virtual-m-trouble.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 4 Patients ----
figma-cli eval "(async()=>{const t='Medra Doctor — 4 Patients';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('P1-patients-d.jsx', 'P1-patients-m.jsx', 'P1-patients-m-access.jsx', 'P1-patients-m-cant.jsx', 'P2-record-d.jsx', 'P2-record-m.jsx', 'P2-record-m-timeline.jsx', 'P2-record-m-vitals.jsx', 'P2-record-m-locked.jsx', 'P2-record-m-actions.jsx', 'P3-access-d.jsx', 'P3-access-m.jsx', 'P3-access-m-why.jsx', 'P3-access-m-how.jsx', 'P3-access-m-asked.jsx', 'P4-followups-d.jsx', 'P4-followups-m.jsx', 'P4-followups-m-due.jsx', 'P4-followups-m-tests.jsx', 'P4-followups-m-send.jsx', 'P4-followups-m-result.jsx', 'P5-messages-d.jsx', 'P5-messages-m.jsx', 'P5-messages-m-quick.jsx', 'P5-messages-m-rules.jsx', 'P6-refills-d.jsx', 'P6-refills-m.jsx', 'P6-refills-m-context.jsx', 'P6-refills-m-rules.jsx', 'P7-results-d.jsx', 'P7-results-m.jsx', 'P7-results-m-trend.jsx', 'P7-results-m-why.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 5 Practice & Money ----
figma-cli eval "(async()=>{const t='Medra Doctor — 5 Practice & Money';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('S1-profile-d.jsx', 'S1-profile-m.jsx', 'S1-profile-m-edit.jsx', 'S1-profile-m-public.jsx', 'S1-profile-m-links.jsx', 'S2-fees-d.jsx', 'S2-fees-m.jsx', 'S2-fees-m-money.jsx', 'S2-fees-m-rules.jsx', 'S3-virtual-d.jsx', 'S3-virtual-m.jsx', 'S3-virtual-m-provider.jsx', 'S3-virtual-m-setup.jsx', 'S3-virtual-m-later.jsx', 'S4-contact-d.jsx', 'S4-contact-m.jsx', 'S4-contact-m-limits.jsx', 'S4-contact-m-preview.jsx', 'S5-earnings-d.jsx', 'S5-earnings-m.jsx', 'S5-earnings-m-breakdown.jsx', 'S5-earnings-m-payouts.jsx', 'S5-earnings-m-billing.jsx', 'S6-billing-d.jsx', 'S6-billing-m.jsx', 'S6-billing-m-plans.jsx', 'S6-billing-m-invoices.jsx', 'S6-billing-m-what.jsx', 'S7-practice-d.jsx', 'S7-practice-m.jsx', 'S7-practice-m-places.jsx', 'S7-practice-m-facility.jsx', 'S8-security-d.jsx', 'S8-security-m.jsx', 'S8-security-m-security.jsx', 'S8-security-m-audit.jsx', 'S8-security-m-danger.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 6 Growth ----
figma-cli eval "(async()=>{const t='Medra Doctor — 6 Growth';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('R1-insights-d.jsx', 'R1-insights-m.jsx', 'R1-insights-m-why.jsx', 'R1-insights-m-when.jsx', 'R1-insights-m-grow.jsx', 'R2-reviews-d.jsx', 'R2-reviews-m.jsx', 'R2-reviews-m-reviews.jsx', 'R2-reviews-m-themes.jsx', 'R2-reviews-m-rules.jsx', 'R2-reviews-m-grow.jsx', 'R3-link-d.jsx', 'R3-link-m.jsx', 'R3-link-m-qr.jsx', 'R3-link-m-import.jsx', 'R3-link-m-perf.jsx', 'R3-link-m-grow.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 7 States & Edge Cases ----
figma-cli eval "(async()=>{const t='Medra Doctor — 7 States & Edge Cases';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('X1-locked-d.jsx', 'X1-locked-m.jsx', 'X1-locked-m-still.jsx', 'X1-locked-m-stopped.jsx', 'X2-empty-d.jsx', 'X2-empty-m.jsx', 'X2-empty-m-week.jsx', 'X2-empty-m-why.jsx', 'X3-notifications-d.jsx', 'X3-notifications-m.jsx', 'X3-notifications-m-earlier.jsx', 'X3-notifications-m-channels.jsx', 'X4-offline-d.jsx', 'X4-offline-m.jsx', 'X4-offline-m-works.jsx', 'X4-offline-m-waits.jsx', 'X5-error-d.jsx', 'X5-error-m.jsx', 'X5-error-m-safe.jsx', 'X5-error-m-help.jsx', 'X6-loading-d.jsx', 'X6-loading-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — 8 Components ----
figma-cli eval "(async()=>{const t='Medra Doctor — 8 Components';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('CMP-Slot-State-Open.jsx', 'CMP-Slot-State-Booked.jsx', 'CMP-Slot-State-Held.jsx', 'CMP-Slot-State-Break.jsx', 'CMP-Slot-State-Away.jsx', 'CMP-QueueRow-State-Waiting.jsx', 'CMP-QueueRow-State-Now.jsx', 'CMP-QueueRow-State-Unpaid.jsx', 'CMP-ShareToggle-State-Shared.jsx', 'CMP-ShareToggle-State-Withheld.jsx', 'CMP-ScopeLine-State-Granted.jsx', 'CMP-ScopeLine-State-Locked.jsx', 'CMP-DrugResult-State-Default.jsx', 'CMP-DrugResult-State-Blocked.jsx', 'CMP-StatTile-State-Info.jsx', 'CMP-StatTile-State-Warning.jsx', 'CMP-StatTile-State-Danger.jsx', 'CMP-StatTile-State-Good.jsx', 'CMP-ChecklistRow-State-Done.jsx', 'CMP-ChecklistRow-State-Todo.jsx', 'CMP-Outcome-State-Selected.jsx', 'CMP-Outcome-State-Default.jsx', 'CMP-RailItem-State-Active.jsx', 'CMP-RailItem-State-Inactive.jsx')) { figma-cli render (Get-Content $f -Raw) }

# 3. turn the cmp/* frames into interactive component sets (doctor page only)
figma-cli run .\components-doctor.js

# 4. wire the prototype, close the navigation, arrange the canvas
figma-cli run .\link-doctor.js

# Expected: link-doctor.js returns { linked, navLinked, stayOnScreen, framesFound, missing }.
# A non-empty 'missing' means that frame did not render — re-render that one .jsx and re-run step 4.