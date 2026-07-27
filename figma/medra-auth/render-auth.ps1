# Medra Auth — render each persona onto its own Figma page (Figma Desktop open + connected).
# Run from inside this folder. Installs client cache first (once per machine).
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force
figma-cli tokens import-design-md .\DESIGN.md

# ---- Medra Auth — Entry ----
figma-cli eval "(async()=>{const t='Medra Auth — Entry';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('E1-splash-d.jsx', 'E1-splash-m.jsx', 'E2-role-d.jsx', 'E2-role-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Auth — Patient ----
figma-cli eval "(async()=>{const t='Medra Auth — Patient';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('P1-create-d.jsx', 'P1-create-m.jsx', 'P2-otp-d.jsx', 'P2-otp-m.jsx', 'P3-onboard-d.jsx', 'P3-onboard-m.jsx', 'P4-login-d.jsx', 'P4-login-m.jsx', 'P5-help-d.jsx', 'P5-help-m.jsx', 'P6-success-d.jsx', 'P6-success-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Auth — Doctor ----
figma-cli eval "(async()=>{const t='Medra Auth — Doctor';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('D1-create-d.jsx', 'D1-create-m.jsx', 'D2-otp-d.jsx', 'D2-otp-m.jsx', 'D3-password-d.jsx', 'D3-password-m.jsx', 'D4-pending-d.jsx', 'D4-pending-m.jsx', 'D5-profile-d.jsx', 'D5-profile-m.jsx', 'D6-login-d.jsx', 'D6-login-m.jsx', 'D7-2fa-d.jsx', 'D7-2fa-m.jsx', 'D8-forgot-d.jsx', 'D8-forgot-m.jsx', 'D9-reset-d.jsx', 'D9-reset-m.jsx', 'D10-success-d.jsx', 'D10-success-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# ---- Medra Auth — Institution ----
figma-cli eval "(async()=>{const t='Medra Auth — Institution';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"
foreach ($f in @('I1-register-d.jsx', 'I1-register-m.jsx', 'I2-documents-d.jsx', 'I2-documents-m.jsx', 'I3-plan-d.jsx', 'I3-plan-m.jsx', 'I4-otp-d.jsx', 'I4-otp-m.jsx', 'I5-password-d.jsx', 'I5-password-m.jsx', 'I6-pending-d.jsx', 'I6-pending-m.jsx', 'I7-admin-login-d.jsx', 'I7-admin-login-m.jsx', 'I8-forgot-d.jsx', 'I8-forgot-m.jsx', 'I9-reset-d.jsx', 'I9-reset-m.jsx', 'I10-success-d.jsx', 'I10-success-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# Wire the clickable prototype + arrange every page
figma-cli run .\link-auth.js