# Incremental render for the Medra design system.
# Usage:
#   .\render-changes.ps1                 # render every .jsx (first run / full refresh)
#   .\render-changes.ps1 15-*.jsx        # render only matching frames (after editing a few)
# Name-based prototype linking means rearranging the canvas never breaks links,
# so you can safely re-render single frames without touching the rest.

param([string[]]$Only)

if ($Only) {
    $files = @()
    foreach ($pat in $Only) { $files += Get-ChildItem -Path $pat -ErrorAction SilentlyContinue }
} else {
    $files = Get-ChildItem .\*.jsx | Sort-Object Name
}

if (-not $files) { Write-Host "No matching .jsx files."; exit 1 }

foreach ($f in $files) {
    Write-Host "Rendering $($f.Name) ..."
    figma-cli render (Get-Content $f.FullName -Raw)
}
Write-Host "Rendered $($files.Count) frame(s). Now re-run the linker:  figma-cli run .\link-medra.js"

# Retired frames to remove from the canvas (none in v1.0):
#   (add stale frame names here when you rename/remove a screen)
