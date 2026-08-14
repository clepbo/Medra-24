# Medra Auth — render + wire (Figma Desktop open + connected).
# Everything goes on ONE page: 'Medra'. Rename it here and in link-*.js if you
# use a different one. Re-rendering APPENDS — delete this module's old frames first.

# 1. prime the offline icon cache (safe to re-run)
New-Item -ItemType Directory -Force "$HOME\.figma-ds-cli\icon-cache" | Out-Null
Copy-Item .\assets\icon-cache\*.svg "$HOME\.figma-ds-cli\icon-cache\" -Force

# 2. tokens — the same 41 tokens as every other Medra bundle, so this is a no-op
figma-cli tokens import-design-md .\DESIGN.md

# 3. select the one page (creates it only if it is genuinely absent)
figma-cli eval "(async()=>{const t='Medra';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"

# 4. render every frame — 70 of them, in flow order
foreach ($f in @('E1-onb1-d.jsx', 'E1-onb1-m.jsx', 'E2-onb2-d.jsx', 'E2-onb2-m.jsx', 'E3-onb3-d.jsx', 'E3-onb3-m.jsx', 'E4-welcome-d.jsx', 'E4-welcome-m.jsx', 'E5-role-d.jsx', 'E5-role-m.jsx', 'M1-create-d.jsx', 'M1-create-m.jsx', 'M2-otp-d.jsx', 'M2-otp-m.jsx', 'M3-name-d.jsx', 'M3-name-m.jsx', 'M4-about-d.jsx', 'M4-about-m.jsx', 'M5-health-d.jsx', 'M5-health-m.jsx', 'M6-login-d.jsx', 'M6-login-m.jsx', 'M7-unlock-d.jsx', 'M7-unlock-m.jsx')) { figma-cli render (Get-Content $f -Raw) }
foreach ($f in @('M8-help-d.jsx', 'M8-help-m.jsx', 'M9-success-d.jsx', 'M9-success-m.jsx', 'D1-create-d.jsx', 'D1-create-m.jsx', 'D2-otp-d.jsx', 'D2-otp-m.jsx', 'D3-password-d.jsx', 'D3-password-m.jsx', 'D4-pending-d.jsx', 'D4-pending-m.jsx', 'D5-profile-d.jsx', 'D5-profile-m.jsx', 'D6-login-d.jsx', 'D6-login-m.jsx', 'D7-2fa-d.jsx', 'D7-2fa-m.jsx', 'D8-forgot-d.jsx', 'D8-forgot-m.jsx', 'D9-reset-d.jsx', 'D9-reset-m.jsx', 'D10-success-d.jsx', 'D10-success-m.jsx')) { figma-cli render (Get-Content $f -Raw) }
foreach ($f in @('I1-register-d.jsx', 'I1-register-m.jsx', 'I2-documents-d.jsx', 'I2-documents-m.jsx', 'I3-orgsize-d.jsx', 'I3-orgsize-m.jsx', 'I4-plan-d.jsx', 'I4-plan-m.jsx', 'I5-otp-d.jsx', 'I5-otp-m.jsx', 'I6-password-d.jsx', 'I6-password-m.jsx', 'I7-pending-d.jsx', 'I7-pending-m.jsx', 'I8-admin-login-d.jsx', 'I8-admin-login-m.jsx', 'I9-forgot-d.jsx', 'I9-forgot-m.jsx', 'I10-reset-d.jsx', 'I10-reset-m.jsx', 'I11-success-d.jsx', 'I11-success-m.jsx')) { figma-cli render (Get-Content $f -Raw) }

# 6. wire the prototype and lay the canvas out in bands, one per section
figma-cli run .\link-auth.js