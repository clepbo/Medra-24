# Medra Doctor app — render + wire (Figma Desktop open + connected).
# Render the auth bundle first if you want the sign-out link to resolve.
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
figma-cli tokens import-design-md .\DESIGN.md

# ---- Medra Doctor — Today & Schedule ----
figma-cli eval "(async()=>{const t='Medra Doctor — Today & Schedule';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('K1-today-d.jsx', 'K1-today-m.jsx', 'K2-appointments-d.jsx', 'K2-appointments-m.jsx', 'K3-appointment-d.jsx', 'K3-appointment-m.jsx', 'K4-availability-d.jsx', 'K4-availability-m.jsx', 'K5-timeoff-d.jsx', 'K5-timeoff-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — Consultation ----
figma-cli eval "(async()=>{const t='Medra Doctor — Consultation';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('C1-room-d.jsx', 'C1-room-m.jsx', 'C2-templates-d.jsx', 'C2-templates-m.jsx', 'C3-prescribe-d.jsx', 'C3-prescribe-m.jsx', 'C4-tests-d.jsx', 'C4-tests-m.jsx', 'C5-upload-d.jsx', 'C5-upload-m.jsx', 'C6-sign-d.jsx', 'C6-sign-m.jsx', 'C7-done-d.jsx', 'C7-done-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — Patients ----
figma-cli eval "(async()=>{const t='Medra Doctor — Patients';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('T1-patients-d.jsx', 'T1-patients-m.jsx', 'T2-record-d.jsx', 'T2-record-m.jsx', 'T3-access-d.jsx', 'T3-access-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — Practice & Earnings ----
figma-cli eval "(async()=>{const t='Medra Doctor — Practice & Earnings';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('S1-profile-d.jsx', 'S1-profile-m.jsx', 'S2-fees-d.jsx', 'S2-fees-m.jsx', 'S3-meeting-d.jsx', 'S3-meeting-m.jsx', 'S4-contact-d.jsx', 'S4-contact-m.jsx', 'S5-earnings-d.jsx', 'S5-earnings-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — States ----
figma-cli eval "(async()=>{const t='Medra Doctor — States';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('X1-verifying-d.jsx', 'X1-verifying-m.jsx', 'X2-empty-d.jsx', 'X2-empty-m.jsx', 'X3-notifications-d.jsx', 'X3-notifications-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Doctor — Components ----
figma-cli eval "(async()=>{const t='Medra Doctor — Components';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('CMP-Slot-State-Open.jsx', 'CMP-Slot-State-Booked.jsx', 'CMP-Slot-State-Blocked.jsx', 'CMP-Slot-State-Break.jsx', 'CMP-ShareToggle-State-Shared.jsx', 'CMP-ShareToggle-State-Withheld.jsx', 'CMP-QueueRow-State-Waiting.jsx', 'CMP-QueueRow-State-Now.jsx', 'CMP-ScopeLine-State-Granted.jsx', 'CMP-ScopeLine-State-Locked.jsx', 'CMP-DrugResult-State-Default.jsx', 'CMP-DrugResult-State-Blocked.jsx')) { figma-cli render (Get-Content $f -Raw) }

# Wire the prototype with motion and arrange the canvas
figma-cli run .\link-doctor.js