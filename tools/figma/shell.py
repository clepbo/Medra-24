#!/usr/bin/env python3
"""One desktop shell for every persona.

Three visual systems was my call and it was the wrong one: a reviewer had to relearn the
furniture three times, and a shared component had to be drawn three ways. This replaces them
with a single shell — the organisation module's icon rail, the doctor module's floating card,
one accent — and moves the identity into a **persona pill** in the top bar, which is the thing
that actually needs to be legible from three metres.

    ground (flat, calm)  →  inset 20  →  white card, radius 28
    ├── 76px icon rail — logo, destinations, help, avatar
    └── main column — top bar (title · persona pill · search · alerts · you)
                      content
        └── optional 340px right rail — what this section needs next

Nothing here uses coral or amber any more. Navy carries structure, teal is the only accent, and
green / amber / red are reserved for state, so a colour on screen always means something.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *

RAIL_W  = 76          # collapsed — icons only
RAIL_WX = 248         # expanded — icons with their labels
GROUND = "var:bg/subtle"

# The pill is the only place a persona is named. Everything else is identical across modules,
# which is the point — one design, and you always know whose screen you are looking at.
PERSONAS = {
    "member": ("circle-user", "Member"),
    "doctor": ("stethoscope", "Doctor"),
    "admin":  ("building-2", "Organisation · Admin"),
    "desk":   ("concierge-bell", "Organisation · Front desk"),
    "nurse":  ("heart-pulse", "Organisation · Nursing"),
    "lab":    ("flask-conical", "Organisation · Laboratory"),
    "pharm":  ("pill", "Organisation · Pharmacy"),
    "imaging":("scan", "Organisation · Imaging"),
    "billing":("receipt", "Organisation · Billing"),
    "orgdoc": ("stethoscope", "Organisation · Doctor"),
}


# Who is signed in, per persona — so the rail footer never says "Member" on a doctor's screen.
DEFAULT_WHO = {
    "member": ("Amara Okeke", "Member"),
    "doctor": ("Dr. Ngozi Okafor", "Cardiologist"),
    "orgdoc": ("Dr. Chuka Eze", "General practice · Garki"),
    "admin":  ("Mrs. Adaeze Nwosu", "Organisation admin"),
    "desk":   ("Blessing Ade", "Front desk"),
    "nurse":  ("Ifeoma Nwachukwu", "Nurse · Outpatient"),
    "lab":    ("Samuel Adeoye", "Lab scientist"),
    "pharm":  ("Kemi Balogun", "Pharmacist"),
    "imaging":("Tunde Alabi", "Radiographer"),
    "billing":("Grace Umeh", "Cashier"),
}


def persona_pill(key, size=12):
    ic, label = PERSONAS[key]
    return (f'<Frame name="Btn Persona" flex="row" gap={{7}} items="center" px={{12}} py={{7}} '
            f'rounded={{999}} bg="var:state/info-bg">'
            f'{I(ic, size + 2, "#2F8BAC")}'
            f'{T(size,"semibold","var:text/accent",label)}</Frame>')


def workplace(current, other=None, name="Btn Switch workplace"):
    """One account, two workplaces.

    A doctor is a person, not a seat: the MDCN number is theirs, not the hospital's. When an
    organisation invites them it adds a workplace to an account that already exists, so the
    same clinician is one record whether they are at Garki on Tuesday or in their own rooms on
    Saturday. This is the control that says which one you are working in — and the reason the
    money, the roster and the governance on screen differ without the consultation differing.
    Without a second workplace it renders as a plain label, not a control."""
    if not other:
        return (f'<Frame flex="row" gap={{8}} items="center" px={{12}} py={{7}} rounded={{999}} '
                f'bg="var:neutral/50">{I("briefcase-medical",14,"#7E8F9D")}'
                f'{T(12,"medium","var:text/muted",current)}</Frame>')
    return (f'<Frame name="{name}" flex="row" gap={{8}} items="center" px={{12}} py={{7}} rounded={{999}} '
            f'bg="var:neutral/50" stroke="var:border/default" strokeWidth={{1}}>'
            f'{I("briefcase-medical",14,"#2F8BAC")}'
            f'{T(12,"semibold","var:text/strong",current)}'
            f'{I("chevrons-up-down",14,"#7E8F9D")}</Frame>')


def rail_item(ic, name, label=None, on=False, badge=None, wide=False):
    """Collapsed: a 44px icon square. Expanded: the same square with its label beside it, so
    the active state and the hit area are identical in both — only the label appears."""
    box = ('bg="var:state/info-bg"' if on else '')
    col = "#2F8BAC" if on else "#7E8F9D"
    dot = ('<Frame w={7} h={7} rounded={999} bg="var:state/error" />') if badge else ''
    if not wide:
        return (f'<Frame name="Btn {name}" w={{44}} h={{44}} rounded={{14}} {box} '
                f'flex="row" justify="center" items="center">{I(ic, 20, col)}{dot}</Frame>')
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="center" px={{12}} py={{11}} '
            f'rounded={{14}} {box}>{I(ic, 20, col)}'
            f'{T(14,"semibold" if on else "regular","var:text/strong" if on else "var:text/muted",label or name,w="fill")}'
            f'{dot}</Frame>')


def rail(items, active=0, badges=(), expanded=False, who=("Amara Okeke", "Member")):
    """items: (icon, hotspot-name, label). Collapsed by default; expanded shows the labels.

    The two states are the same list, the same order and the same hotspot names, so every
    transition in the prototype works in either — the rail is a view of one thing, not two
    navigations that have to be kept in step."""
    cells = "".join(rail_item(ic, nm, lb, i == active, nm in badges, expanded)
                    for i, (ic, nm, lb) in enumerate(items))
    w = RAIL_WX if expanded else RAIL_W
    toggle_ic = "panel-left-close" if expanded else "panel-left-open"
    if expanded:
        head = (f'<Frame w="fill" flex="row" justify="between" items="center">'
                f'<Frame flex="row" gap={{10}} items="center">'
                f'<Image image="assets/logo/appicon.png" w={{36}} h={{36}} rounded={{12}} />'
                f'{T(16,"bold","var:text/strong","Medra")}</Frame>'
                f'<Frame name="Btn Collapse rail" flex="row">{I(toggle_ic,18,"#A7B6C2")}</Frame></Frame>')
        foot = (f'<Frame w="fill" flex="col" gap={{4}}>'
                f'{rail_item("circle-help","Open help","Help",wide=True)}'
                f'<Frame name="Btn Nav Profile" w="fill" flex="row" gap={{11}} items="center" p={{10}} '
                f'rounded={{14}} bg="var:neutral/50">'
                f'<Image image="assets/img/me.jpg" w={{34}} h={{34}} rounded={{999}} />'
                f'<Frame grow={{1}} flex="col" gap={{1}}>'
                f'{T(13,"semibold","var:text/strong",who[0])}'
                f'{T(11,"regular","var:text/muted",who[1])}</Frame>'
                f'<Frame name="Btn Sign out" flex="row">{I("log-out",16,"#A7B6C2")}</Frame></Frame></Frame>')
        pad = 'px={16} py={20}'
        align = ''
    else:
        head = (f'<Frame w="fill" flex="col" gap={{14}} items="center">'
                f'<Image image="assets/logo/appicon.png" w={{40}} h={{40}} rounded={{13}} />'
                f'<Frame name="Btn Expand rail" flex="row">{I(toggle_ic,18,"#A7B6C2")}</Frame></Frame>')
        foot = (f'{rail_item("circle-help","Open help")}'
                f'<Image image="assets/img/me.jpg" w={{38}} h={{38}} rounded={{999}} />'
                f'<Frame name="Btn Sign out" flex="row">{I("log-out",18,"#A7B6C2")}</Frame>')
        pad = 'px={16} py={22}'
        align = ' items="center"'
    return (f'<Frame w={{{w}}} h="fill" flex="col" gap={{18}}{align} {pad} '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{head}'
            f'<Frame w="fill" flex="col" gap={{6}}{align}>{cells}</Frame>'
            f'<Frame grow={{1}} w="fill" />{foot}</Frame>')


def topbar(title, persona, sub=None, right=None, search="Btn Search", place=None, extra=""):
    subline = T(12, "regular", "var:text/muted", sub) if sub else ""
    tools = right if right is not None else (
        (f'<Frame name="{search}" w={{300}} flex="row" gap={{10}} items="center" px={{15}} py={{11}} '
         f'rounded={{999}} bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={{1}}>'
         f'{I("search",17,"#7E8F9D")}{T(13,"regular","var:text/faint","Search",w="fill")}</Frame>'
         if search else '')
        + extra
        + f'<Frame name="Btn Notifications" w={{40}} h={{40}} rounded={{999}} bg="var:neutral/50" '
          f'stroke="var:border/subtle" strokeWidth={{1}} flex="row" justify="center" items="center">'
          f'{I("bell",18,"#1B3A5B")}</Frame>')
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{18}} pb={{4}}>'
            f'<Frame flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{11}} items="center">'
            f'{T(20,"bold","var:text/strong",title)}{persona_pill(persona)}</Frame>'
            f'{subline}</Frame>'
            f'<Frame flex="row" gap={{10}} items="center">{tools}</Frame></Frame>')


def tool_btn(ic, name):
    return (f'<Frame name="Btn {name}" w={{40}} h={{40}} rounded={{999}} bg="var:neutral/50" '
            f'stroke="var:border/subtle" strokeWidth={{1}} flex="row" justify="center" '
            f'items="center">{I(ic,18,"#1B3A5B")}</Frame>')


def app_desk(name, persona, title, children, items, active=0, sub=None,
             side=None, badges=(), right=None, expanded=False, who=None, place=None,
             search="Btn Search", extra=""):
    """One shell, every persona. `side` is the optional 340px context rail.

    `expanded` swaps the icon rail for the labelled one. Both states carry the same hotspot
    names, so a screen drawn in either is wired by the same transition table."""
    rail_block = (f'<Frame w={{340}} h="fill" flex="col" gap={{14}} px={{20}} py={{22}} '
                  f'bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={{1}}>'
                  f'{side}</Frame>') if side else ''
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="col" p={{20}} bg="{GROUND}" '
            f'overflow="hidden">'
            f'<Frame w="fill" grow={{1}} flex="row" rounded={{28}} bg="var:bg/base" overflow="hidden" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{rail(items, active, badges, expanded, who or DEFAULT_WHO.get(persona, ("Amara Okeke","Member")))}'
            f'<Frame grow={{1}} h="fill" flex="col" gap={{20}} px={{30}} py={{24}}>'
            f'{topbar(title, persona, sub, right, search, place, extra)}{children}</Frame>'
            f'{rail_block}</Frame></Frame>')


# ---------------------------------------------------------------- the pieces inside it
def stat(ic, value, label, sub=None, filled=False, name=None):
    """The tile row. One filled tile per screen, never more — it is the thing you are meant to
    look at first, and two of them is none."""
    if filled:
        return (f'<Frame name="Btn {name or label}" grow={{1}} flex="col" gap={{13}} p={{20}} rounded={{20}} '
                f'image="assets/img/btn-navy.jpg" overflow="hidden">'
                f'<Frame w={{40}} h={{40}} rounded={{13}} bg="var:bg/band-2" flex="row" justify="center" '
                f'items="center">{I(ic,19,"#FFFFFF")}</Frame>'
                f'<Frame flex="col" gap={{2}}>{T(26,"bold","var:text/on-dark",value)}'
                f'{T(13,"semibold","var:text/on-dark",label)}'
                f'{T(11,"regular","#A9C2D4",sub) if sub else ""}</Frame></Frame>')
    return (f'<Frame name="Btn {name or label}" grow={{1}} flex="col" gap={{13}} p={{20}} rounded={{20}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{40}} h={{40}} rounded={{13}} bg="var:neutral/50" flex="row" justify="center" '
            f'items="center">{I(ic,19,"#2F8BAC")}</Frame>'
            f'<Frame flex="col" gap={{2}}>{T(26,"bold","var:text/strong",value)}'
            f'{T(13,"semibold","var:text/default",label)}'
            f'{T(11,"regular","var:text/muted",sub) if sub else ""}</Frame></Frame>')


def panel(title, body, action=None, name=None, p=20):
    head = (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(15,"bold","var:text/strong",title)}'
            + (f'<Frame name="Btn {name}" flex="row" gap={{5}} items="center">'
               f'{T(12,"semibold","var:text/accent",action)}{I("chevron-right",14,"#2F8BAC")}</Frame>'
               if action else '') + '</Frame>')
    return (f'<Frame w="fill" flex="col" gap={{13}} p={{{p}}} rounded={{20}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{head}{body}</Frame>')


def row(ic, label, sub=None, value=None, name=None, tone=None, chevron=True):
    tint = {"ok": "var:state/success-bg", "warn": "var:state/warning-bg",
            "err": "var:state/error-bg", None: "var:neutral/50"}[tone]
    col = {"ok": "#2FA36B", "warn": "#E0A32E", "err": "#D14343", None: "#2F8BAC"}[tone]
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    v = T(13, "semibold", "var:text/strong", value) if value else ""
    ch = I("chevron-right", 15, "#A7B6C2") if chevron else ""
    return (f'<Frame name="Btn {name or label}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="{tint}" flex="row" justify="center" '
            f'items="center">{I(ic,16,col)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",label)}{s}</Frame>'
            f'{v}{ch}</Frame>')


# =====================================================================================
# ADAPTERS
# Every screen in the three modules already calls its own module's shell. Rather than
# rewrite ~150 call sites — the risky, churn-heavy way to do this — each old shell now
# delegates here. The call sites are untouched, the look changes everywhere at once, and
# the three old bodies are gone rather than left to rot beside the new one.
# =====================================================================================
def title_from(name):
    """'Member · Records — R6 Who Has Access' -> 'Who Has Access'. The screen code belongs in
    the layer name, where a linker and an audit can find it, not in the heading a user reads."""
    tail = name.split("—")[-1].strip() if "—" in name else name.split("·")[-1].strip()
    parts = tail.split(" ", 1)
    if parts and len(parts) == 2 and any(c.isdigit() for c in parts[0]) and len(parts[0]) <= 4:
        return parts[1]
    return tail


NAV_MEMBER = [("house", "Nav Home", "Home"), ("search", "Nav Find", "Find care"),
              ("calendar-days", "Nav Visits", "My visits"), ("clipboard-list", "Nav Records", "Records"),
              ("pill", "Nav Meds", "Medicines"), ("circle-user", "Nav Profile", "Profile")]


# =====================================================================================
# ONE PAGE
# The Figma plan on this project caps the file at three pages, and there are four modules
# wanting eight each. So every frame in every module renders onto one page, and the layout
# pass stacks each logical group in its own band rather than starting all of them at x=0
# and piling them on top of each other. Change this in one place if the page is renamed.
# =====================================================================================
ONE_PAGE = "Medra"

# Four modules share the page, and each linker runs on its own, so each needs to know where
# its own territory starts. Without this they all lay out from y=0 and land on top of one
# another — which is exactly what happened the first time the page cap forced this.
BAND_Y0 = {"member": 0, "doctor": 60000, "org": 120000, "auth": 180000}


def one_page_ps1(module, files_in_order, link_script, components=None):
    """The render script: prime icons, import tokens, select the single page, render every
    frame in flow order, then wire. It never creates a second page."""
    esc = ONE_PAGE.replace("'", "\\'")
    ps = [f"# Medra {module} — render + wire (Figma Desktop open + connected).",
          f"# Everything goes on ONE page: '{ONE_PAGE}'. Rename it here and in link-*.js if you",
          "# use a different one. Re-rendering APPENDS — delete this module's old frames first.",
          "",
          "# 1. prime the offline icon cache (safe to re-run)",
          'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
          'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
          "",
          "# 2. tokens — the same 41 tokens as every other Medra bundle, so this is a no-op",
          "figma-cli tokens import-design-md .\\DESIGN.md",
          "",
          f"# 3. select the one page (creates it only if it is genuinely absent)",
          f'figma-cli eval "(async()=>{{const t=\'{esc}\';let p=figma.root.children.find(n=>n.name===t);'
          f'if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"',
          "",
          f"# 4. render every frame — {len(files_in_order)} of them, in flow order"]
    for i in range(0, len(files_in_order), 24):
        chunk = ", ".join("'" + f + "'" for f in files_in_order[i:i + 24])
        ps.append(f"foreach ($f in @({chunk})) {{ figma-cli render (Get-Content $f -Raw) }}")
    ps.append("")
    if components:
        ps += [f"# 5. turn the cmp/* frames into real interactive component sets",
               f"figma-cli run .\\{components}", ""]
    ps += ["# 6. wire the prototype and lay the canvas out in bands, one per section",
           f"figma-cli run .\\{link_script}"]
    return "\n".join(ps)


LAYOUT_JS = (
 "  // One page, so each section gets its own horizontal band and the next one starts below it.\n"
 "  // Laying every section out from y=0 would stack four modules on top of each other.\n"
 "  const GX=170, GY=140, BAND=300;\n"
 "  const page = figma.root.children.find(n => n.type==='PAGE' && norm(n.name)===norm(ONE_PAGE))\n"
 "             || figma.currentPage;\n"
 "  let y = Y0;\n"
 "  for (const key of Object.keys(ORDER)){ const ord=ORDER[key]; if(!ord) continue;\n"
 "    let x=0, rowH=0;\n"
 "    for (const dn of (ord.d||[])){ const df=F(dn); if(df){ df.x=x; df.y=y; x+=df.width+GX;\n"
 "      rowH=Math.max(rowH,df.height); } }\n"
 "    let mx=0, mH=0;\n"
 "    for (const mn of (ord.m||[])){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=y+rowH+GY;\n"
 "      mx+=mf.width+GX; mH=Math.max(mH,mf.height); } }\n"
 "    y += rowH + GY + mH + BAND; }\n"
 "  // Every section's two starting points live on the one page.\n"
 "  const pts=[];\n"
 "  for (const [key,s] of Object.entries(STARTS)){\n"
 "    if(!s) continue;\n"
 "    if(F(s[0])) pts.push({ nodeId:F(s[0]).id, name:key+' \\u00b7 Desktop' });\n"
 "    if(F(s[1])) pts.push({ nodeId:F(s[1]).id, name:key+' \\u00b7 Mobile' }); }\n"
 "  if(pts.length) page.flowStartingPoints=pts;\n")
