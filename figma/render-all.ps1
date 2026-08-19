# Medra — render every module into Figma, in one command.
#
#   .\render-all.ps1              # all four modules, from scratch
#   .\render-all.ps1 -Only org    # just one module — deletes only that module's frames
#   .\render-all.ps1 -KeepOld     # render without deleting first (you will get duplicates)
#
# Run it from this folder, with Figma Desktop open on the target file and figma-cli connected.
#
# WHY THIS EXISTS. The four render-*.ps1 scripts each work, but none of them deletes, and
# re-rendering APPENDS. That is the one way an 870-frame render goes wrong: it stops half way,
# somebody re-runs it, and now there are two of everything with no way to tell which is which.
# This deletes first, scoped to the module being rendered, and says how many it removed.
#
# THE DELETE IS SCOPED BY FRAME NAME, NOT BY PAGE. Every Medra frame is named for its module —
# "Member · …", "Doctor · …", "Org · …", "Auth · …" — plus the component frames under "cmp/".
# Nothing else on the page is touched, so a page you are also using for something else survives.

param(
  [ValidateSet('all','auth','member','doctor','org')] [string]$Only = 'all',
  [switch]$KeepOld,
  [string]$Page = 'Medra'
)

$ErrorActionPreference = 'Stop'
$order = if ($Only -eq 'all') { @('auth','member','doctor','org') } else { @($Only) }

# The name prefixes each module owns. The linkers use the same convention, so if you rename a
# module's frames you have to change it in both places.
$owns = @{
  auth   = @('Auth · ')
  member = @('Member · ')
  doctor = @('Doctor · ')
  org    = @('Org · ')
}

Write-Host ""
Write-Host "Medra → Figma   page '$Page'   modules: $($order -join ', ')" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------------- 1. select or create the page
$esc = $Page.Replace("'", "''")
figma-cli eval "(async()=>{const t='$esc';let p=figma.root.children.find(n=>n.name===t);if(!p){p=figma.createPage();p.name=t;}await figma.setCurrentPageAsync(p);return p.name;})()"

# ---------------------------------------------------------------- 2. delete what we are replacing
if (-not $KeepOld) {
  foreach ($m in $order) {
    $prefixes = ($owns[$m] | ForEach-Object { "'" + $_.Replace("'", "''") + "'" }) -join ','
    # Components are shared: only clear them when the whole file is being rebuilt, because one
    # module's re-render must not remove another module's component set.
    $alsoCmp = if ($Only -eq 'all' -and $m -eq $order[0]) { 'true' } else { 'false' }
    Write-Host "  clearing $m …" -NoNewline
    figma-cli eval "(async()=>{const p=figma.currentPage;const pre=[$prefixes];const cmp=$alsoCmp;let n=0;for(const f of [...p.children]){const nm=f.name||'';if(pre.some(x=>nm.startsWith(x))||(cmp&&nm.startsWith('cmp/'))){f.remove();n++;}}return n;})()"
  }
  Write-Host ""
}

# ---------------------------------------------------------------- 3. render, in dependency order
# Auth first, then member, doctor, org: the linkers resolve cross-module transitions against
# whatever is in the file at the time they run, so the module that others point *at* goes first.
foreach ($m in $order) {
  $dir = Join-Path $PSScriptRoot "medra-$m"
  if (-not (Test-Path $dir)) { Write-Host "  skipped $m (no folder)" -ForegroundColor Yellow; continue }
  Write-Host ""
  Write-Host "── $m ──────────────────────────────────────────" -ForegroundColor Cyan
  Push-Location $dir
  try { & ".\render-$m.ps1" } finally { Pop-Location }
}

Write-Host ""
Write-Host "Done. Each linker printed a report; the field worth reading is 'missing' —" -ForegroundColor Green
Write-Host "a non-empty list means a transition names a frame that is not in the file." -ForegroundColor Green
Write-Host "The linkers are safe to re-run on their own once everything is rendered." -ForegroundColor Green
