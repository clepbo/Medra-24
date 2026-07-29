# Medra Member app — render + wire (Figma Desktop open + connected).
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
figma-cli tokens import-design-md .\DESIGN.md

# ---- Medra Member — Find & Book ----
figma-cli eval "(async()=>{const t='Medra Member — Find & Book';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('H1-home-d.jsx', 'H1-home-m.jsx', 'H2-home-empty-d.jsx', 'H2-home-empty-m.jsx', 'S1-results-d.jsx', 'S1-results-m.jsx', 'S2-filters-d.jsx', 'S2-filters-m.jsx', 'S3-empty-d.jsx', 'S3-empty-m.jsx', 'P1-profile-d.jsx', 'P1-profile-m.jsx', 'B1-slot-d.jsx', 'B1-slot-m.jsx', 'B2-taken-d.jsx', 'B2-taken-m.jsx', 'B3-review-d.jsx', 'B3-review-m.jsx', 'C1-confirmed-d.jsx', 'C1-confirmed-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra — Interactive Components ----
figma-cli eval "(async()=>{const t='Medra — Interactive Components';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('CMP-ButtonPrimary-State-Default.jsx', 'CMP-ButtonPrimary-State-Hover.jsx', 'CMP-ButtonPrimary-State-Pressed.jsx', 'CMP-ButtonPrimary-State-Loading.jsx', 'CMP-ButtonPrimary-State-Disabled.jsx', 'CMP-Input-State-Default.jsx', 'CMP-Input-State-Focus.jsx', 'CMP-Input-State-Filled.jsx', 'CMP-Input-State-Error.jsx', 'CMP-TimeSlot-State-Available.jsx', 'CMP-TimeSlot-State-Hover.jsx', 'CMP-TimeSlot-State-Selected.jsx', 'CMP-TimeSlot-State-Taken.jsx', 'CMP-SpecialtyChip-State-Default.jsx', 'CMP-SpecialtyChip-State-Hover.jsx', 'CMP-SpecialtyChip-State-Selected.jsx', 'CMP-Toggle-State-On.jsx', 'CMP-Toggle-State-Off.jsx', 'CMP-Checkbox-State-Checked.jsx', 'CMP-Checkbox-State-Unchecked.jsx', 'CMP-NavItem-State-Active.jsx', 'CMP-NavItem-State-Inactive.jsx', 'CMP-DoctorCard-State-Default.jsx', 'CMP-DoctorCard-State-Hover.jsx')) { figma-cli render (Get-Content $f -Raw) }

# Turn the cmp/* frames into real interactive components (variants + hover/press)
figma-cli run .\components-medra.js

# Wire the prototype with motion + arrange the canvas
figma-cli run .\link-member.js