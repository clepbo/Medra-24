#!/usr/bin/env python3
"""Medra — Doctor app design system.

**This is deliberately not the member app.** A member opens Medra once a month; a doctor lives
in it between patients. The first pass made that difference *cold* — graph paper and a dark
command strip — which read as technical rather than warm. This version takes the structure from
the reference dashboard the product owner liked instead: a white card floating on a soft blue
canvas, three columns, pastel code chips, a donut, progress bars and a month calendar.

| | Member app | Doctor app |
|---|---|---|
| Page | full-bleed soft mesh gradient | **white card floating on a soft blue canvas**, 24px inset |
| Columns | two — sidebar + main | **three** — navy sidebar + main + light right rail |
| Navigation | one 262px navy sidebar | **206px labelled navy sidebar**, white left notch, coral badges |
| Right rail | none | **292px light column** — month calendar, next up, done today |
| Corners | 24–28px | 14–18px inside a 28px card |
| Density | generous, one thing at a time | dense — a whole queue on one screen |
| Accent | teal only | teal **plus warm coral/amber** for counts, attention and progress |
| Mobile chrome | light appbar | **floating brand-gradient header card** with the day's numbers |
| Mobile nav | 5 flat tabs | 5 tabs, raised centre Consult, fifth tab is **More** (K9) |
| Primary action | teal | **navy**, teal reserved for live/active state |

House rules carried over: no wrap="wrap", no items="stretch", grow is a row property,
numeric props keep their braces.
"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from member2_kit import (hr, tabs, status_pill, prep_step, radio_row, consent_row, audit_row, notif_row,
                         empty_state, skel, skel_card, note_section, provenance, lab_line,
                         kv, kv_pair, timeline, tl_item, PILL)
from member_kit import date_strip
from shell import app_desk, title_from, tool_btn

RAIL_DIM = "#7FA3BE"; RAIL_ON = "#FFFFFF"; INK = "#09141F"

# =====================================================================================
# PRIMITIVES — squarer and denser than the member kit
# =====================================================================================
def dcard(children, p=18, gap=13, r=16, bg="var:bg/base", stroke="var:border/subtle", sw=1):
    st = f' stroke="{stroke}" strokeWidth={{{sw}}}' if stroke else ''
    return (f'<Frame w="fill" flex="col" gap={{{gap}}} p={{{p}}} rounded={{{r}}} bg="{bg}"{st}>'
            f'{children}</Frame>')

def dgroup(title, rows, footer=None, p=18, action=None):
    body = hr().join(rows) if isinstance(rows, list) else rows
    head = ''
    if title:
        head = (f'<Frame w="fill" flex="row" justify="between" items="center" pb={{2}}>'
                f'{T(11,"semibold","var:text/accent",title.upper())}{action or ""}</Frame>')
    ft = (f'{hr()}<Frame name="Group footer" w="fill" flex="row" gap={{8}} items="start" pt={{2}}>'
          f'{I("info",13,M_IC)}'
          f'{T(11,"regular","var:text/muted",footer,w="fill")}</Frame>') if footer else ''
    return dcard(f'{head}{body}{ft}', p=p, gap=6)

def drow(ic, label, value=None, name=None, sub=None, chevron=True, tone=None, right=None, strong=False):
    tint = {"warn": "var:state/warning-bg", "err": "var:state/error-bg", "ok": "var:state/success-bg",
            "info": "var:state/info-bg", None: "var:bg/muted"}[tone]
    hexc = {"warn": WARN_IC, "err": ERR_IC, "ok": OK_IC, "info": A_IC, None: A_IC}[tone]
    tail = right if right is not None else (
        f'<Frame flex="row" gap={{8}} items="center">'
        f'{T(13,"semibold" if strong else "regular","var:text/strong" if strong else "var:text/muted",value) if value else ""}'
        f'{I("chevron-right",16,M_IC) if chevron else ""}</Frame>')
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame name="Btn {name or label}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{32}} h={{32}} rounded={{10}} bg="{tint}" flex="col" justify="center" items="center">'
            f'{I(ic,16,hexc)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"medium","var:text/strong",label)}{s}</Frame>{tail}</Frame>')

def dtoggle(ic, label, sub=None, on=True, name=None):
    sw = (f'<Frame name="Btn {name or label}" w={{44}} h={{25}} rounded={{999}} image="assets/img/btn-teal.jpg" '
          f'overflow="hidden" flex="row" justify="end" items="center" px={{3}}><Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame>'
          if on else
          f'<Frame name="Btn {name or label}" w={{44}} h={{25}} rounded={{999}} bg="var:neutral/300" '
          f'flex="row" justify="start" items="center" px={{3}}><Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame>')
    return drow(ic, label, sub=sub, name=(name or label) + " row", chevron=False, right=sw)

def dbtn(label, name, icon=None, kind="ghost", grow=True, full=False, size="md"):
    g = ' w="fill"' if full else (' grow={1}' if grow else '')
    px, py, fs, ics = {"sm": (12, 8, 12, 13), "md": (15, 11, 13, 15), "lg": (20, 14, 15, 17)}[size]
    if kind == "navy":   st = 'image="assets/img/btn-navy.jpg" overflow="hidden"'; col = "var:text/on-dark"; ic = W_IC
    elif kind == "teal": st = 'image="assets/img/btn-teal.jpg" overflow="hidden"'; col = "var:text/on-dark"; ic = W_IC
    elif kind == "danger": st = 'bg="var:state/error-bg"'; col = "var:state/error"; ic = ERR_IC
    elif kind == "ok":     st = 'bg="var:state/success-bg"'; col = "var:state/success"; ic = OK_IC
    elif kind == "warn":   st = 'bg="var:state/warning-bg"'; col = "var:state/warning"; ic = WARN_IC
    elif kind == "dark":   st = 'bg="var:bg/band-2"'; col = "var:text/on-dark"; ic = W_IC
    elif kind == "rail":   st = 'bg="#173049" stroke="#24486B" strokeWidth={1}'; col = "var:text/on-dark"; ic = T_IC
    else: st = 'bg="var:bg/base" stroke="var:border/default" strokeWidth={1}'; col = "var:text/default"; ic = N_IC
    return (f'<Frame name="Btn {name}"{g} flex="row" gap={{7}} justify="center" items="center" '
            f'px={{{px}}} py={{{py}}} rounded={{12}} {st}>'
            f'{I(icon,ics,ic) if icon else ""}{T(fs,"semibold",col,label)}</Frame>')

def dcta(label, name, icon="arrow-right", kind="navy"):
    return dbtn(label, name, icon, kind, full=True, size="lg")

def eyerow(title, action=None):
    return (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(11,"semibold","var:text/accent",title.upper())}{action or ""}</Frame>')

def dhead(parts, size=26):
    return head_chip(parts, size)

def stat_tile(ic, value, label, sub=None, tone="info", name=None, delta=None):
    """`delta` is (direction, text) — "up" or "down" and what it is against. Abraham asked for
    money to read as a movement rather than a number: "their earnings, like a regression against
    previous, an arrow down means less than what they..." A figure with nothing to compare it to
    tells a doctor whether they are busy, not whether they are doing better."""
    tint = {"info": "tint-blue.jpg", "ok": "tint-mint.jpg", "warn": "tint-amber.jpg",
            "err": "tint-red.jpg", "teal": "tint-teal.jpg", "slate": "tint-slate.jpg",
            "navy": "tint-navy.jpg", "ocean": "tint-ocean.jpg"}[tone]
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    d = ''
    if delta:
        up = delta[0] == "up"
        d = (f'<Frame flex="row" gap={{4}} items="center" px={{8}} py={{3}} rounded={{999}} '
             f'bg="{"var:state/success-bg" if up else "var:state/error-bg"}">'
             f'{I("trending-up" if up else "trending-down", 12, OK_IC if up else ERR_IC)}'
             f'{T(10,"semibold","var:state/success" if up else "var:state/error",delta[1])}</Frame>')
    head = (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame w={{34}} h={{34}} rounded={{11}} image="assets/img/{tint}" overflow="hidden" '
            f'flex="col" justify="center" items="center">{I(ic,17,W_IC)}</Frame>{d}</Frame>')
    return (f'<Frame name="Btn {name or label}" grow={{1}} flex="col" gap={{10}} p={{16}} rounded={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>{head}'
            f'<Frame w="fill" flex="col" gap={{2}}>{T(24,"bold","var:text/strong",value)}'
            f'{T(12,"semibold","var:text/default",label,w="fill")}{s}</Frame></Frame>')

def alert_strip(ic, title, body, tone="warn", action=None):
    bg = {"warn": "var:state/warning-bg", "err": "var:state/error-bg", "ok": "var:state/success-bg",
          "info": "var:state/info-bg"}[tone]
    c = {"warn": WARN_IC, "err": ERR_IC, "ok": OK_IC, "info": A_IC}[tone]
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center" p={{14}} rounded={{14}} bg="{bg}">{I(ic,17,c)}'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",title)}'
            f'{T(12,"regular","var:text/default",body,w="fill")}</Frame>{action or ""}</Frame>')

def kpi_line(label, value, tone="default"):
    c = {"default": "var:text/strong", "ok": "var:state/success", "warn": "var:state/warning",
         "err": "var:state/error", "muted": "var:text/muted"}[tone]
    return (f'<Frame w="fill" flex="row" justify="between" items="center" py={{7}}>'
            f'{T(12,"regular","var:text/muted",label,w="fill")}{T(13,"semibold",c,value)}</Frame>')

def bar(pct, tone="teal", h=8):
    """`pct` is 0–100. The fill uses grow ratios, not a pixel width — a fixed-width fill
    overflowed the 390 frame the moment the same component was reused on mobile."""
    img = {"teal": "btn-teal.jpg", "navy": "btn-navy.jpg", "amber": "tint-amber.jpg",
           "red": "tint-red.jpg", "mint": "tint-mint.jpg"}[tone]
    p = max(1, min(100, int(pct))); rest = 100 - p
    fill = f'<Frame grow={{{p}}} h={{{h}}} rounded={{999}} image="assets/img/{img}" overflow="hidden" />'
    tail = f'<Frame grow={{{rest}}} h={{{h}}} />' if rest > 0 else ''
    return (f'<Frame w="fill" h={{{h}}} rounded={{999}} bg="var:neutral/200" flex="row">'
            f'{fill}{tail}</Frame>')

def progress_row(label, value, pct, tone="teal"):
    return (f'<Frame w="fill" flex="col" gap={{7}} py={{7}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(12,"medium","var:text/default",label)}{T(12,"semibold","var:text/strong",value)}</Frame>'
            f'{bar(pct,tone)}</Frame>')

# =====================================================================================
# SHELL — a white app card floating on a soft blue canvas, three columns:
# navy sidebar · main · light right rail. Distinct from the member app by structure
# (member is full-bleed and two columns), warm rather than clinical.
# =====================================================================================
RAIL = [("layout-dashboard", "Today",    "Nav Today"),
        ("inbox",            "Requests", "Nav Requests"),
        ("calendar-days",    "Schedule", "Nav Schedule"),
        ("users",            "Patients", "Nav Patients"),
        ("notebook-pen",     "Consults", "Nav Consults"),
        ("banknote",         "Money",    "Nav Money"),
        ("trending-up",      "Growth",   "Nav Growth"),
        ("settings",         "Settings", "Nav Settings")]

def sidebar(active=0, badges=None):
    badges = badges or {}
    cells = ""
    for i, (ic, label, nm) in enumerate(RAIL):
        on = i == active
        chip = ''
        if badges.get(label):
            chip = (f'<Frame flex="row" px={{7}} py={{2}} rounded={{999}} bg="#F07A52">'
                    f'{T(9,"bold","var:text/on-dark",str(badges[label]))}</Frame>')
        notch = ('<Rect w={4} h={22} rounded={999} bg="#FFFFFF" />' if on
                 else '<Frame w={4} h={22} />')
        row = (f'<Frame grow={{1}} flex="row" gap={{12}} items="center" px={{14}} py={{12}} rounded={{14}} '
               f'{"bg=" + chr(34) + "#17324D" + chr(34) if on else ""}>'
               f'{I(ic,18,"#FFFFFF" if on else "#7FA3BE")}'
               f'{T(13,"semibold" if on else "regular","var:text/on-dark" if on else "#9FBED6",label,w="fill")}'
               f'{chip}</Frame>')
        cells += (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{8}} items="center">{notch}{row}</Frame>')
    return (f'<Frame w={{206}} h="fill" flex="col" gap={{6}} pl={{10}} pr={{16}} pt={{22}} pb={{18}} '
            f'image="assets/img/sidebar-dr.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="row" gap={{11}} items="center" px={{14}} pb={{18}}>'
            f'<Image image="assets/logo/appicon.png" w={{36}} h={{36}} rounded={{11}} />'
            f'<Frame flex="col" gap={{1}}>{T(16,"bold","var:text/on-dark","Medra")}'
            f'{T(9,"semibold","var:brand/teal","FOR DOCTORS")}</Frame></Frame>'
            f'{cells}<Frame grow={{1}} />'
            f'<Frame w="fill" flex="col" gap={{9}} px={{8}}>'
            f'<Frame w="fill" flex="col" gap={{9}} p={{14}} rounded={{16}} bg="#17324D">'
            f'<Frame flex="row" gap={{8}} items="center">{I("sparkles",15,T_IC)}'
            f'{T(12,"semibold","var:text/on-dark","Free trial")}</Frame>'
            f'{T(11,"regular","#9FBED6","12 days left. Add a card to keep your dashboard after 26 August.",w="fill")}'
            f'<Frame name="Btn Open billing S6" w="fill" flex="row" justify="center" px={{12}} py={{8}} rounded={{10}} bg="#FFFFFF">'
            f'{T(11,"semibold","var:text/strong","See plans")}</Frame></Frame>'
            f'<Frame name="Btn Sign out" w="fill" flex="row" gap={{11}} items="center" px={{14}} py={{11}}>'
            f'{I("log-out",17,"#7FA3BE")}{T(13,"regular","#9FBED6","Log out")}</Frame></Frame></Frame>')

def topbar(crumbs, right=None, urgent=2):
    # A breadcrumb laid out horizontally squeezed the page title onto two lines once the
    # right-hand group was in place. Parents go above the title instead.
    parents = " · ".join(crumbs[:-1])
    trail = (f'<Frame flex="col" gap={{2}}>'
             + (T(11, "semibold", "var:text/accent", parents.upper()) if parents else "")
             + T(20, "bold", "var:text/strong", crumbs[-1]) + '</Frame>')
    ug = (f'<Frame name="Btn Nav Requests" flex="row" gap={{7}} items="center" px={{12}} py={{8}} rounded={{12}} '
          f'bg="var:state/error-bg">{I("triangle-alert",14,ERR_IC)}'
          f'{T(12,"semibold","var:state/error",f"{urgent} need you")}</Frame>') if urgent else ''
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{16}}>'
            f'<Frame grow={{1}} flex="row" gap={{9}} items="center">{trail}</Frame>'
            f'<Frame flex="row" gap={{10}} items="center">{ug}'
            f'<Frame name="Btn Search patient" w={{230}} flex="row" gap={{9}} items="center" px={{13}} py={{10}} '
            f'rounded={{12}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>{I("search",15,M_IC)}'
            f'{T(12,"regular","var:text/faint","Search or Medra ID",w="fill")}</Frame>'
            f'<Frame name="Btn Nav More" flex="row" px={{10}} py={{10}} rounded={{12}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{I("layout-grid",16,N_IC)}</Frame>'
            f'<Frame name="Btn Notifications" flex="row" px={{10}} py={{10}} rounded={{12}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{I("bell",16,N_IC)}</Frame>'
            f'<Frame name="Btn Nav Settings" flex="row" gap={{10}} items="center">'
            f'<Frame w={{112}} flex="col" gap={{1}} items="end">'
            f'{T(13,"semibold","var:text/strong","Dr. Okafor")}'
            f'{T(10,"regular","var:text/muted","Cardiology")}</Frame>'
            f'<Image image="assets/img/avatar-4.jpg" w={{38}} h={{38}} rounded={{999}} /></Frame>'
            f'{right or ""}</Frame></Frame>')

def panel(title, body, foot=None):
    """The right rail. Same idea as before — always holds what this section needs next —
    but light, like the reference's calendar column, instead of a second dark band."""
    ft = (f'<Frame grow={{1}} /><Frame w="fill" flex="col" gap={{9}}>{foot}</Frame>'
          if foot else '<Frame grow={1} />')
    return (f'<Frame w={{292}} h="fill" flex="col" gap={{14}} px={{18}} pt={{24}} pb={{20}} bg="var:bg/subtle" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{T(11,"semibold","var:text/accent",title.upper())}{body}{ft}</Frame>')

def dr_desk(name, crumbs, children, active=0, panel_block=None, urgent=2, cmd_right=None, badges=None):
    """Delegates to the one shell. `crumbs` still supplies the title; `panel_block` still
    supplies the right rail; `badges` still marks a rail item. Nothing at a call site moved.

    The workplace control appears because a doctor is a person, not a seat: this account also
    exists at Garki Medical Centre, and which one you are in decides the roster, the money and
    who you answer to — not what a consultation looks like."""
    nav = [(ic, nm, label) for ic, label, nm in RAIL]
    bad = {("Nav " + k) for k in (badges or {}) if (badges or {}).get(k)}
    title = crumbs[-1] if crumbs else title_from(name)
    sub = " · ".join(crumbs[:-1]) if crumbs and len(crumbs) > 1 else None
    return app_desk(name, "doctor", title,
                    f'<Frame w="fill" flex="col" gap={{16}}>{children}</Frame>',
                    nav, active, sub=sub, side=panel_block, badges=bad,
                    search="Btn Search patient", extra=tool_btn("layout-grid", "Nav More"),
                    place=("Private practice", "Garki Medical Centre"))

# ---------------------------------------------------------------- mobile
# The sidebar carries eight destinations; a phone tab bar cannot. The fifth tab is a real
# screen (K9) that holds the four the tab bar drops — Schedule, Consults, Money, Growth —
# plus search, help and settings, so nothing on desktop is unreachable on mobile.
MTABS = [("layout-dashboard", "Today", "Nav Today"), ("inbox", "Requests", "Nav Requests"),
         ("stethoscope", "Consult", "Start consult"), ("users", "Patients", "Nav Patients"),
         ("ellipsis", "More", "Nav More")]

def dr_tabbar(active=0):
    cells = ""
    for i, (ic, label, nm) in enumerate(MTABS):
        if i == 2:
            cells += (f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{4}} items="center">'
                      f'<Frame w={{46}} h={{46}} rounded={{16}} image="assets/img/btn-navy.jpg" overflow="hidden" '
                      f'flex="col" justify="center" items="center">{I(ic,21,W_IC)}</Frame>'
                      f'{T(9,"semibold","var:text/strong",label)}</Frame>')
            continue
        on = i == active
        cells += (f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{5}} items="center" pt={{6}}>'
                  f'{I(ic,20,T_IC if on else M_IC)}'
                  f'{T(9,"semibold" if on else "regular","var:text/accent" if on else "var:text/muted",label)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{4}} items="center" px={{12}} pt={{9}} pb={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}} rounded={{22}}>{cells}</Frame>')

def dr_head(title, sub=None, back=True, right=None, stats=None, chips=None, illo=False):
    """A floating brand-gradient card, not a full-bleed navy block — the mobile equivalent of
    the desktop welcome banner."""
    left = (f'<Frame name="Btn Back" w={{36}} h={{36}} rounded={{12}} bg="#17324D" flex="col" justify="center" '
            f'items="center">{I("arrow-left",17,W_IC)}</Frame>' if back else
            f'<Image image="assets/logo/appicon.png" w={{36}} h={{36}} rounded={{11}} />')
    # Top-level screens carry search as well as notifications; the desktop top bar has both and
    # without it a phone has no way into a patient record except the Patients tab.
    _bell = (f'<Frame name="Btn Notifications" w={{36}} h={{36}} rounded={{12}} bg="#17324D" flex="col" '
             f'justify="center" items="center">{I("bell",16,W_IC)}</Frame>')
    _search = (f'<Frame name="Btn Search patient" w={{36}} h={{36}} rounded={{12}} bg="#17324D" flex="col" '
               f'justify="center" items="center">{I("search",16,W_IC)}</Frame>')
    if right is not None:
        rt = right
    elif back:
        rt = _bell
    else:
        rt = f'<Frame flex="row" gap={{8}} items="center">{_search}{_bell}</Frame>'
    subline = T(12, "regular", "var:text/on-dark-muted", sub, w="fill") if sub else ""
    art = (f'<Frame w="fill" flex="row" justify="end" pt={{2}}>'
           f'<Image image="assets/img/illo-welcome-m.png" w={{190}} h={{132}} /></Frame>') if illo else ''
    statrow = ''
    if stats:
        cells = ""
        for v, l in stats:
            cells += (f'<Frame grow={{1}} flex="col" gap={{2}} px={{11}} py={{10}} rounded={{13}} bg="#17324D">'
                      f'{T(16,"bold","var:text/on-dark",v)}{T(10,"regular","#9FBED6",l)}</Frame>')
        statrow = f'<Frame w="fill" flex="row" gap={{8}} pt={{2}}>{cells}</Frame>'
    chiprow = ''
    if chips:
        cc = ""
        for label, nm, on in chips:
            st = ('image="assets/img/btn-teal.jpg" overflow="hidden"' if on else 'bg="#17324D"')
            cc += (f'<Frame name="Btn {nm}" flex="row" px={{12}} py={{7}} rounded={{999}} {st}>'
                   f'{T(12,"semibold","var:text/on-dark",label)}</Frame>')
        chiprow = f'<Frame w="fill" flex="row" gap={{8}} pt={{2}}>{cc}</Frame>'
    return (f'<Frame w="fill" flex="col" gap={{11}} px={{18}} pt={{16}} pb={{18}} rounded={{24}} '
            f'image="assets/img/head-m.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="row" justify="between" items="center">{left}'
            f'<Frame grow={{1}} flex="col" gap={{1}} px={{12}}>{T(17,"bold","var:text/on-dark",title)}{subline}</Frame>'
            f'{rt}</Frame>{art}{statrow}{chiprow}</Frame>')

def dr_mob(name, head, children, tab=None):
    tabrow = f'<Frame w="fill" px={{12}} pb={{8}}>{dr_tabbar(tab)}</Frame>' if tab is not None else ''
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/canvas-m.jpg" '
            f'overflow="hidden">{statusbar()}'
            f'<Frame w="fill" px={{14}} pt={{2}}>{head}</Frame>'
            f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{14}} pt={{14}} pb={{10}}>{children}</Frame>'
            f'{tabrow}</Frame>')

# ---------------------------------------------------------------- reference-flavoured parts
def welcome(title_plain, title_bold, sub, actions="", stats=None):
    """The hero from the reference: greeting, one line of progress, illustration on the right."""
    st = ''
    if stats:
        cells = ""
        for v, l, tone in stats:
            bgc = {"teal": "var:state/info-bg", "ok": "var:state/success-bg",
                   "warn": "var:state/warning-bg", "coral": "#FDEBE4"}[tone]
            cells += (f'<Frame flex="col" gap={{2}} px={{14}} py={{10}} rounded={{13}} bg="{bgc}">'
                      f'{T(18,"bold","var:text/strong",v)}{T(10,"medium","var:text/muted",l)}</Frame>')
        st = f'<Frame w="fill" flex="row" gap={{9}} pt={{2}}>{cells}</Frame>'
    act = f'<Frame w="fill" flex="row" gap={{10}} pt={{4}}>{actions}</Frame>' if actions else ''
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{18}} p={{24}} rounded={{22}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame grow={{1}} flex="col" gap={{9}}>'
            f'{head_chip([(title_plain,False),(title_bold,True)],26)}'
            f'{T(14,"regular","var:text/muted",sub,w="fill")}{st}{act}</Frame>'
            f'<Image image="assets/img/illo-welcome.png" w={{300}} h={{182}} /></Frame>')

def donut_card(pct, title, legend, note=None, size=168):
    lg = ""
    for label, tone in legend:
        col = {"teal": "#39B0CF", "navy": "#1B3A5B", "amber": "#E0A32E", "coral": "#F07A52",
               "grey": "#CBD6DF"}[tone]
        lg += (f'<Frame flex="row" gap={{7}} items="center"><Ellipse w={{9}} h={{9}} bg="{col}" />'
               f'{T(11,"regular","var:text/muted",label)}</Frame>')
    n = T(11, "regular", "var:text/muted", note, w="fill", align="center") if note else ""
    return (f'<Frame w="fill" flex="col" gap={{12}} items="center" p={{18}} rounded={{18}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(13,"semibold","var:text/strong",title)}'
            f'<Frame name="Btn Donut range" flex="row" gap={{6}} items="center" px={{11}} py={{6}} rounded={{999}} '
            f'bg="#FDEBE4">{T(11,"semibold","#C2521F","Today")}{I("chevron-down",12,"#C2521F")}</Frame></Frame>'
            f'<Frame w={{{size}}} h={{{size}}} flex="col" justify="center" items="center" '
            f'image="assets/img/donut-{pct}.png" overflow="hidden">'
            f'{T(28,"bold","var:text/strong",f"{pct}%")}</Frame>'
            f'<Frame w="fill" flex="row" gap={{18}} justify="center">{lg}</Frame>{n}</Frame>')

def level_chip(code, tone="blue"):
    bg = {"blue": "assets/img/pale-blue.jpg", "mint": "assets/img/pale-mint.jpg",
          "amber": "assets/img/pale-amber.jpg", "coral": "assets/img/pale-coral.jpg",
          "lilac": "assets/img/pale-lilac.jpg"}[tone]
    col = {"blue": "var:text/accent", "mint": "var:state/success", "amber": "var:state/warning",
           "coral": "#C2521F", "lilac": "#4A54A8"}[tone]
    return (f'<Frame w={{38}} h={{38}} rounded={{12}} image="{bg}" overflow="hidden" flex="col" '
            f'justify="center" items="center">{T(12,"bold",col,code)}</Frame>')

def person_progress(avatar, who, pct, tone="teal", name=None):
    """The reference's student list: avatar, name, a bar, a percentage."""
    col = {"teal": "btn-teal.jpg", "coral": "tint-coral.jpg", "navy": "btn-navy.jpg",
           "amber": "tint-amber.jpg"}[tone]
    return (f'<Frame name="Btn {name or who}" w="fill" flex="row" gap={{12}} items="center" py={{10}}>'
            f'<Image image="assets/img/{avatar}" w={{36}} h={{36}} rounded={{999}} />'
            f'{T(13,"medium","var:text/strong",who,w=136)}'
            f'<Frame grow={{1}} h={{7}} rounded={{999}} bg="var:neutral/200" flex="row">'
            f'<Frame grow={{{max(1,min(100,pct))}}} h={{7}} rounded={{999}} image="assets/img/{col}" overflow="hidden" />'
            f'<Frame grow={{{max(1,100-pct)}}} h={{7}} /></Frame>'
            f'{T(13,"semibold","var:text/strong",f"{pct}%")}</Frame>')

def file_row(code, tone, title, filename, status, status_tone, members, size, name, mobile=False):
    """The reference's media table. The fixed columns only work at desktop width, so the
    mobile variant stacks instead of squeezing — that is what pushed K1 past 390."""
    sc = {"ok": "var:state/success", "warn": "var:state/warning", "muted": "var:text/muted"}[status_tone]
    if mobile:
        return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" py={{10}}>'
                f'{level_chip(code, tone)}'
                f'<Frame grow={{1}} flex="col" gap={{2}}>{T(12,"semibold","var:text/strong",title)}'
                f'{T(10,"regular","var:text/muted",filename,w="fill")}'
                f'<Frame flex="row" gap={{6}} items="center">'
                f'<Ellipse w={{5}} h={{5}} bg="#CBD6DF" />{T(10,"medium",sc,status)}'
                f'{T(10,"regular","var:text/faint","· "+size)}</Frame></Frame>'
                f'{I("chevron-right",14,M_IC)}</Frame>')
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{13}} items="center" py={{11}}>'
            f'{level_chip(code, tone)}'
            f'{T(13,"semibold","var:text/strong",title,w=132)}'
            f'{T(12,"regular","var:text/muted",filename,w="fill")}'
            f'<Frame flex="row" gap={{7}} items="center" w={{110}}>'
            f'<Ellipse w={{6}} h={{6}} bg="#CBD6DF" />{T(11,"medium",sc,status)}</Frame>'
            f'{T(11,"regular","var:text/muted",members,w=84)}'
            f'{T(11,"regular","var:text/muted",size,w=56)}</Frame>')

MONTH = [("Mon", ["27", "4", "11", "18", "25"]), ("Tue", ["28", "5", "12", "19", "26"]),
         ("Wed", ["29", "6", "13", "20", "27"]), ("Thu", ["30", "7", "14", "21", "28"]),
         ("Fri", ["1", "8", "15", "22", "29"]), ("Sat", ["2", "9", "16", "23", "30"]),
         ("Sun", ["3", "10", "17", "24", "31"])]

def month_cal(today="14", busy=("6", "7", "8", "13", "20", "21", "27"), full=("9", "22")):
    cols = ""
    for day, nums in MONTH:
        cells = f'{T(10,"medium","var:text/muted",day)}'
        for n in nums:
            faint = n in ("27", "28", "29", "30") and nums.index(n) == 0
            if n == today:
                cells += (f'<Frame name="Btn Day {n}" w="fill" flex="col" gap={{2}} items="center" py={{5}} '
                          f'rounded={{9}} image="assets/img/btn-navy.jpg" overflow="hidden">'
                          f'{T(11,"bold","var:text/on-dark",n)}<Frame h={{4}} /></Frame>')
            elif n in full:
                cells += (f'<Frame name="Btn Day {n}" w="fill" flex="col" gap={{2}} items="center" py={{5}} '
                          f'rounded={{9}} bg="#F07A52">{T(11,"bold","var:text/on-dark",n)}'
                          f'<Frame h={{4}} /></Frame>')
            else:
                dot = ('<Ellipse w={4} h={4} bg="#F07A52" />' if n in busy else '<Frame h={4} />')
                cells += (f'<Frame name="Btn Day {n}" w="fill" flex="col" gap={{2}} items="center" py={{5}}>'
                          f'{T(11,"medium","var:text/faint" if faint else "var:text/default",n)}{dot}</Frame>')
        cols += f'<Frame grow={{1}} flex="col" gap={{4}} items="center">{cells}</Frame>'
    return (f'<Frame w="fill" flex="col" gap={{10}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(14,"bold","var:text/strong","August 2026")}'
            f'<Frame flex="row" gap={{7}} items="center">'
            f'<Frame name="Btn Month prev" w={{24}} h={{24}} rounded={{8}} flex="col" justify="center" items="center">'
            f'{I("chevron-left",14,M_IC)}</Frame>'
            f'<Frame name="Btn Month next" w={{24}} h={{24}} rounded={{8}} image="assets/img/btn-navy.jpg" '
            f'overflow="hidden" flex="col" justify="center" items="center">{I("chevron-right",14,W_IC)}</Frame>'
            f'</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{2}}>{cols}</Frame></Frame>')

def upcoming_card(title, when, avatars, name, tone="teal", action="plus"):
    bar_col = {"teal": "#39B0CF", "coral": "#F07A52", "navy": "#1B3A5B"}[tone]
    av = ""
    for a in avatars:
        av += f'<Image image="assets/img/{a}" w={{26}} h={{26}} rounded={{999}} />'
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="center" p={{14}} rounded={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Rect w={{4}} h={{44}} rounded={{999}} bg="{bar_col}" />'
            f'<Frame grow={{1}} flex="col" gap={{6}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(13,"semibold","var:text/strong",title)}{I("ellipsis-vertical",15,M_IC)}</Frame>'
            f'{T(11,"regular","var:text/muted",when)}'
            f'<Frame flex="row" gap={{4}} items="center">{av}</Frame></Frame>'
            f'<Frame name="Btn Add {name}" w={{30}} h={{30}} rounded={{999}} image="assets/img/btn-navy.jpg" '
            f'overflow="hidden" flex="col" justify="center" items="center">{I(action,15,W_IC)}</Frame></Frame>')

def task_row(ic, tone, title, meta, name):
    bg = {"blue": "assets/img/pale-blue.jpg", "mint": "assets/img/pale-mint.jpg",
          "amber": "assets/img/pale-amber.jpg", "coral": "assets/img/pale-coral.jpg"}[tone]
    col = {"blue": A_IC, "mint": OK_IC, "amber": WARN_IC, "coral": "#C2521F"}[tone]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" p={{12}} rounded={{14}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{32}} h={{32}} rounded={{10}} image="{bg}" overflow="hidden" flex="col" '
            f'justify="center" items="center">{I(ic,15,col)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(12,"semibold","var:text/strong",title)}'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame>'
            f'{I("chevron-right",14,M_IC)}</Frame>')

def rail_section(title, body, action="View all", action_name=None):
    act = (f'<Frame name="Btn {action_name or title}" flex="row">'
           f'{T(11,"semibold","var:text/accent",action)}</Frame>') if action else ''
    return (f'<Frame w="fill" flex="col" gap={{10}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(13,"bold","var:text/strong",title)}{act}</Frame>{body}</Frame>')

# =====================================================================================
# CLINICAL COMPONENTS
# =====================================================================================
def queue_row(time, avatar, who, meta, reason, kind, vtype, name, now=False, flags=None, mobile=False):
    edge = ('stroke="var:border/accent" strokeWidth={2}' if now else 'stroke="var:border/subtle" strokeWidth={1}')
    tic = "video" if vtype == "Virtual" else "hospital"
    flagrow = ''
    if flags:
        ff = ""
        for ic, label, tone in flags:
            bg = {"err": "var:state/error-bg", "warn": "var:state/warning-bg",
                  "info": "var:state/info-bg", "ok": "var:state/success-bg"}[tone]
            c = {"err": ERR_IC, "warn": WARN_IC, "info": A_IC, "ok": OK_IC}[tone]
            ff += (f'<Frame flex="row" gap={{5}} items="center" px={{8}} py={{4}} rounded={{7}} bg="{bg}">'
                   f'{I(ic,11,c)}{T(10,"semibold","var:text/default",label)}</Frame>')
        flagrow = f'<Frame w="fill" flex="row" gap={{6}}>{ff}</Frame>'
    msg = (f'<Frame name="Btn Msg {name}" flex="row" px={{9}} py={{7}} rounded={{9}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>{I("message-circle",14,M_IC)}</Frame>')
    action = msg + (dbtn("Start", "Start " + name, "stethoscope", "navy", grow=False, size="sm") if now
                    else dbtn("Open", "Open " + name, "chevron-right", "ghost", grow=False, size="sm"))
    mact = (dbtn("Start consultation", "Start " + name, "stethoscope", "navy", full=True, size="sm") if now
            else (dbtn("Open the file", "Open " + name, "clipboard-list", "ghost", full=True, size="sm")
                  + dbtn("Message", "Msg " + name, "message-circle", "ghost", full=True, size="sm")))
    if mobile:
        return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{9}} p={{13}} rounded={{14}} '
                f'bg="var:bg/base" {edge}>'
                f'<Frame w="fill" flex="row" gap={{10}} items="center">'
                f'<Frame w={{46}} flex="col" gap={{1}} items="center">'
                f'{T(14,"bold","var:text/strong",time)}{T(9,"regular","var:text/muted","30m")}</Frame>'
                f'<Image image="assets/img/{avatar}" w={{36}} h={{36}} rounded={{11}} />'
                f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
                f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame>'
                f'<Frame flex="row" gap={{5}} items="center">{I(tic,12,A_IC)}{status_pill(kind,size=10)}</Frame></Frame>'
                f'{flagrow}'
                f'<Frame w="fill" flex="row" gap={{8}} items="center" px={{10}} py={{8}} rounded={{10}} bg="var:neutral/50">'
                f'{I("file-text",11,M_IC)}{T(11,"regular","var:text/muted",reason,w="fill")}</Frame>'
                # Desktop puts Start/Open at the end of the header row; at 390 that row is already
                # full, so the same action gets its own line rather than being dropped.
                f'<Frame w="fill" flex="row" gap={{8}}>{mact}</Frame></Frame>')
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{10}} p={{14}} rounded={{14}} bg="var:bg/base" {edge}>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Frame w={{54}} flex="col" gap={{1}} items="center">'
            f'{T(15,"bold","var:text/strong",time)}{T(10,"regular","var:text/muted","30 min")}</Frame>'
            f'<Rect w={{1}} h={{40}} bg="var:border/subtle" />'
            f'<Image image="assets/img/{avatar}" w={{40}} h={{40}} rounded={{12}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            # w="fill" on the row and the name: the column this sits in shrinks when a screen
            # also carries a context rail, and a hugging row inside a shrinking column overflows
            # it rather than wrapping.
            f'<Frame w="fill" flex="row" gap={{8}} items="center">'
            f'{T(14,"semibold","var:text/strong",who,w="fill")}{status_pill(kind,size=10)}</Frame>'
            f'{T(11,"regular","var:text/muted",meta,w="fill")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{9}} py={{5}} rounded={{8}} bg="var:bg/muted">'
            f'{I(tic,11,A_IC)}{T(10,"medium","var:text/default",vtype)}</Frame>{action}</Frame>'
            f'{flagrow}'
            f'<Frame w="fill" flex="row" gap={{8}} items="center" px={{11}} py={{8}} rounded={{10}} bg="var:neutral/50">'
            f'{I("file-text",12,M_IC)}{T(11,"regular","var:text/muted",reason,w="fill")}</Frame></Frame>')

def now_card(avatar, who, meta, reason, when, mobile=False):
    sz = (48, 16, 12) if mobile else (56, 18, 13)
    return (f'<Frame w="fill" flex="col" gap={{13}} p={{18}} rounded={{18}} image="assets/img/btn-navy.jpg" '
            f'overflow="hidden">'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{7}} items="center">{I("circle-dot",14,T_IC)}'
            f'{T(11,"semibold","var:brand/teal","NEXT · IN 6 MIN")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{10}} py={{5}} rounded={{8}} bg="#17324D">'
            f'{I("video",12,T_IC)}{T(10,"medium","var:text/on-dark","Virtual")}</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Image image="assets/img/{avatar}" w={{{sz[0]}}} h={{{sz[0]}}} rounded={{15}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(sz[1],"bold","var:text/on-dark",who)}'
            f'{T(sz[2],"regular","var:text/on-dark-muted",meta,w="fill")}</Frame>'
            f'{T(15,"semibold","var:text/on-dark",when)}</Frame>'
            f'<Frame w="fill" flex="row" gap={{8}} items="start" px={{12}} py={{10}} rounded={{11}} bg="#17324D">'
            f'{I("file-text",13,T_IC)}{T(12,"regular","var:text/on-dark",reason,w="fill")}</Frame>'
            f'<Frame w="fill" flex="row" gap={{9}}>'
            f'<Frame name="Btn Open prep" grow={{1}} flex="row" gap={{7}} justify="center" items="center" '
            f'px={{13}} py={{11}} rounded={{11}} bg="#17324D">{I("clipboard-list",14,W_IC)}'
            f'{T(12,"semibold","var:text/on-dark","Read the file")}</Frame>'
            f'<Frame name="Btn Start consult" grow={{1}} flex="row" gap={{7}} justify="center" items="center" '
            f'px={{13}} py={{11}} rounded={{11}} bg="var:bg/base">{I("stethoscope",14,N_IC)}'
            f'{T(12,"semibold","var:text/strong","Start")}</Frame></Frame></Frame>')

def request_row(ic, who, what, when, name, tone="info", actions=None):
    bg = {"info": "var:state/info-bg", "warn": "var:state/warning-bg", "err": "var:state/error-bg",
          "ok": "var:state/success-bg"}[tone]
    c = {"info": A_IC, "warn": WARN_IC, "err": ERR_IC, "ok": OK_IC}[tone]
    acts = rows_of(actions, 2, 8) if actions else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{10}} p={{14}} rounded={{14}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{11}} items="start">'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,16,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(11,"regular","var:text/muted",what,w="fill")}</Frame>'
            f'{T(10,"regular","var:text/faint",when)}</Frame>{acts}</Frame>')

def note_field(label, ic, value, name, lines=3, ph=False, helper=None, template=True, private=False):
    col = "var:text/faint" if ph else "var:text/strong"
    h = 18 + lines * 19
    sub = T(11, "regular", "var:text/muted", helper, w="fill") if helper else ""
    tpl = (f'<Frame name="Btn Template {name}" flex="row" gap={{5}} items="center" px={{9}} py={{4}} rounded={{7}} '
           f'bg="var:bg/muted">{I("files",11,M_IC)}{T(10,"medium","var:text/muted","Template")}</Frame>') if template else ''
    lock = (f'<Frame flex="row" gap={{5}} items="center" px={{9}} py={{4}} rounded={{7}} bg="var:neutral/100">'
            f'{I("eye-off",11,M_IC)}{T(10,"medium","var:text/muted","Private")}</Frame>') if private else ''
    fill = 'bg="var:neutral/100"' if private else 'bg="var:neutral/50"'
    return (f'<Frame w="fill" flex="col" gap={{6}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{7}} items="center">{I(ic,14,A_IC)}'
            f'{T(12,"semibold","var:text/default",label)}</Frame>'
            f'<Frame flex="row" gap={{7}} items="center">{lock}{tpl}</Frame></Frame>'
            f'<Frame name="Btn Field {name}" w="fill" minH={{{h}}} flex="col" px={{14}} py={{12}} rounded={{12}} '
            f'{fill} stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{T(13,"regular",col,value,w="fill")}</Frame>{sub}</Frame>')

def share_toggle(label, name, on=True, sub=None):
    sw = (f'<Frame name="Btn {name}" w={{42}} h={{24}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden" '
          f'flex="row" justify="end" items="center" px={{3}}><Ellipse w={{18}} h={{18}} bg="#FFFFFF" /></Frame>' if on else
          f'<Frame name="Btn {name}" w={{42}} h={{24}} rounded={{999}} bg="var:neutral/300" '
          f'flex="row" justify="start" items="center" px={{3}}><Ellipse w={{18}} h={{18}} bg="#FFFFFF" /></Frame>')
    s = T(10, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center" py={{8}}>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(12,"medium","var:text/default",label)}{s}</Frame>{sw}</Frame>')

def drug_result(name, form, note_txt, btn, blocked=False):
    tint = "var:state/error-bg" if blocked else "var:state/success-bg"
    c = ERR_IC if blocked else OK_IC
    tail = (f'<Frame flex="row" gap={{5}} items="center" px={{8}} py={{4}} rounded={{7}} bg="var:state/error-bg">'
            f'{I("ban",11,ERR_IC)}{T(10,"semibold","var:state/error","Blocked")}</Frame>' if blocked
            else I("plus", 15, A_IC))
    return (f'<Frame name="Btn {btn}" w="fill" flex="row" gap={{11}} items="center" p={{12}} rounded={{12}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{32}} h={{32}} rounded={{10}} bg="{tint}" flex="col" justify="center" items="center">'
            f'{I("pill",15,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",name)}'
            f'{T(10,"regular","var:text/muted",form,w="fill")}</Frame>'
            f'{T(10,"regular","var:text/faint",note_txt)}{tail}</Frame>')

def rx_line(name, dose, freq, days, btn):
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center" py={{10}}>'
            f'<Frame w={{30}} h={{30}} rounded={{10}} bg="var:state/success-bg" flex="col" justify="center" items="center">'
            f'{I("pill",14,OK_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"semibold","var:text/strong",name)}'
            f'{T(10,"regular","var:text/muted",dose+" · "+freq+" · "+days,w="fill")}</Frame>'
            f'<Frame name="Btn Edit {btn}" flex="row">{I("pencil",14,M_IC)}</Frame>'
            f'<Frame name="Btn Remove {btn}" flex="row">{I("x",15,ERR_IC)}</Frame></Frame>')

def patient_row(avatar, who, mid, meta, last, name, tag=None, compact=False):
    p = status_pill(tag, size=10) if tag else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" py={{11}}>'
            f'<Image image="assets/img/{avatar}" w={{38}} h={{38}} rounded={{12}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{8}} items="center">{T(13,"semibold","var:text/strong",who)}{p}</Frame>'
            f'<Frame flex="row" gap={{8}} items="center">'
            f'<Frame flex="row" px={{7}} py={{2}} rounded={{6}} bg="var:bg/muted">'
            f'{T(10,"semibold","var:text/accent",mid)}</Frame>'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame></Frame>'
            f'{T(10,"regular","var:text/muted",last)}{I("chevron-right",15,M_IC)}</Frame>')

def scope_line(label, granted=True, detail=None):
    ic, c = ("circle-check", OK_IC) if granted else ("lock", M_IC)
    sub = T(10, "regular", "var:text/muted", detail, w="fill") if detail else ""
    return (f'<Frame w="fill" flex="row" gap={{10}} items="start" py={{7}}>{I(ic,15,c)}'
            f'<Frame grow={{1}} flex="col" gap={{1}}>'
            f'{T(12,"medium","var:text/strong" if granted else "var:text/faint",label)}{sub}</Frame></Frame>')

def slot_chip(t, state="open", name=None, w=None):
    conf = {"open":    ('bg="var:bg/base" stroke="var:border/default" strokeWidth={1}', "var:text/default"),
            "booked":  ('image="assets/img/btn-navy.jpg" overflow="hidden"', "var:text/on-dark"),
            "blocked": ('bg="var:neutral/100"', "var:text/faint"),
            "hold":    ('bg="var:state/warning-bg"', "var:state/warning"),
            "break":   ('bg="var:bg/muted"', "var:text/muted")}[state]
    ww = f' w={{{w}}}' if w else ' grow={1}'
    return (f'<Frame name="Btn {name or ("Slot "+t)}"{ww} flex="row" justify="center" py={{9}} rounded={{10}} '
            f'{conf[0]}>{T(12,"semibold",conf[1],t)}</Frame>')

def day_col(day, date, items, today=False):
    bg = ('image="assets/img/btn-teal.jpg" overflow="hidden"' if today else 'bg="var:bg/muted"')
    head = (f'<Frame w="fill" flex="col" gap={{1}} items="center" py={{9}} rounded={{11}} {bg}>'
            f'{T(10,"medium","var:text/on-dark-muted" if today else "var:text/muted",day)}'
            f'{T(15,"bold","var:text/on-dark" if today else "var:text/strong",date)}</Frame>')
    return f'<Frame grow={{1}} flex="col" gap={{7}}>{head}{"".join(items)}</Frame>'

def earn_row(label, sub, amount, tone="default"):
    c = {"default": "var:text/strong", "ok": "var:state/success", "muted": "var:text/muted",
         "err": "var:state/error"}[tone]
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{10}}>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"medium","var:text/strong",label)}'
            f'{T(10,"regular","var:text/muted",sub,w="fill")}</Frame>'
            f'{T(14,"bold",c,amount)}</Frame>')

def review_row(stars, quote, who, when, reply=None):
    st = "".join(I("star", 12, "#E0A32E") for _ in range(stars))
    r = (f'<Frame w="fill" flex="row" gap={{9}} items="start" px={{12}} py={{10}} rounded={{10}} bg="var:neutral/50">'
         f'{I("corner-down-right",13,M_IC)}{T(11,"regular","var:text/muted",reply,w="fill")}</Frame>') if reply else ''
    return (f'<Frame w="fill" flex="col" gap={{9}} py={{12}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{3}} items="center">{st}</Frame>'
            f'{T(10,"regular","var:text/faint",when)}</Frame>'
            f'{T(13,"regular","var:text/default",quote,w="fill")}'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(11,"regular","var:text/muted",who)}'
            f'{dbtn("Reply","Reply "+who,"corner-down-right","ghost",grow=False,size="sm")}</Frame>{r}</Frame>')

def msg_row(avatar, who, preview, when, name, unread=False, channel="whatsapp"):
    ic = {"whatsapp": "message-circle", "email": "mail", "inapp": "message-square-text"}[channel]
    dot = '<Ellipse w={7} h={7} bg="#39B0CF" />' if unread else '<Frame w={7} />'
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" py={{11}}>'
            f'<Image image="assets/img/{avatar}" w={{38}} h={{38}} rounded={{12}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{7}} items="center">{T(13,"semibold","var:text/strong",who)}{I(ic,12,M_IC)}</Frame>'
            f'{T(10,"regular","var:text/faint",when)}</Frame>'
            f'{T(11,"regular","var:text/muted",preview,w="fill")}</Frame>{dot}</Frame>')

def checklist_row(done, label, sub, name, action=None):
    box = (f'<Frame w={{24}} h={{24}} rounded={{8}} bg="var:brand/teal" flex="col" justify="center" items="center">'
           f'{I("check",14,W_IC)}</Frame>' if done else
           '<Rect w={24} h={24} rounded={8} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />')
    col = "var:text/muted" if done else "var:text/strong"
    act = action or (dbtn("Do it", "Do " + name, "arrow-right", "ghost", grow=False, size="sm") if not done else
                     T(11, "medium", "var:state/success", "Done"))
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>{box}'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"semibold",col,label)}'
            f'{T(11,"regular","var:text/muted",sub,w="fill")}</Frame>{act}</Frame>')

def outcome_choice(ic, title, desc, name, sel=False, tone="info"):
    bd = "var:border/accent" if sel else "var:border/subtle"
    bw = 2 if sel else 1
    bg = {"info": "var:state/info-bg", "ok": "var:state/success-bg", "warn": "var:state/warning-bg",
          "err": "var:state/error-bg"}[tone]
    c = {"info": A_IC, "ok": OK_IC, "warn": WARN_IC, "err": ERR_IC}[tone]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="start" p={{14}} rounded={{13}} '
            f'bg="var:bg/base" stroke="{bd}" strokeWidth={{{bw}}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,16,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",title)}'
            f'{T(11,"regular","var:text/muted",desc,w="fill")}</Frame>'
            f'{I("circle-check",18,T_IC) if sel else ""}</Frame>')

def timeline_entry(day, mon, ic, title, meta, name, tone="info", tag=None):
    bg = {"info": "var:state/info-bg", "ok": "var:state/success-bg", "warn": "var:state/warning-bg",
          "muted": "var:bg/muted"}[tone]
    c = {"info": A_IC, "ok": OK_IC, "warn": WARN_IC, "muted": N_IC}[tone]
    p = status_pill(tag, size=10) if tag else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" py={{10}}>'
            f'<Frame w={{42}} flex="col" gap={{0}} items="center">'
            f'{T(15,"bold","var:text/strong",day)}{T(9,"medium","var:text/muted",mon)}</Frame>'
            f'<Frame w={{30}} h={{30}} rounded={{10}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,14,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",title,w="fill")}'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame>'
            f'{p}{I("chevron-right",15,M_IC)}</Frame>')

def chart(series, h=140, unit=""):
    cols = ""
    for label, val, px, tone in series:
        img = {"ok": "btn-teal.jpg", "warn": "tint-amber.jpg", "bad": "tint-red.jpg",
               "navy": "btn-navy.jpg", "slate": "tint-slate.jpg"}[tone]
        cols += (f'<Frame grow={{1}} h={{{h}}} flex="col" gap={{6}} justify="end" items="center">'
                 f'{T(10,"semibold","var:text/default",val)}'
                 f'<Frame w="fill" h={{{px}}} rounded={{8}} image="assets/img/{img}" overflow="hidden" />'
                 f'{T(9,"regular","var:text/muted",label)}</Frame>')
    u = T(10, "regular", "var:text/faint", unit) if unit else ""
    return (f'<Frame w="fill" flex="col" gap={{7}}>'
            f'<Frame w="fill" flex="row" gap={{7}} items="end">{cols}</Frame>{u}</Frame>')

def field_dr(label, ic, value, ph=True, helper=None, prefix=None, trailing=None, focus=False):
    return field(label, ic, value, ph=ph, helper=helper, prefix=prefix, trailing=trailing, focus=focus)


# =====================================================================================
# DENSITY — the third pass.
#
# The screens were complete but overloaded: the average mobile screen was two full
# viewports of stacked cards and the busiest was five. Completeness is not the same as
# legibility, and a doctor between patients reads the first screenful or nothing.
#
# Mobile is now **hub → section → sheet**:
#   hub      what is happening now, plus a short list of ways in
#   section  one subject per screen, reached by tapping a row on the hub
#   sheet    one decision, over a dimmed hub — the "dialogue" case
#
# Desktop keeps its three columns but obeys a budget: at most two groups per column,
# lists capped at four rows, and a "See all N" row pointing at whichever screen owns
# the full list. Nothing is deleted; it moves to where it belongs.
# =====================================================================================

def see_all(label, name, count=None):
    """The disclosure that replaces rows five and beyond. It is a row, not a link, because
    it has to look like the thing it continues."""
    txt = f"See all {count} {label}" if count else label
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{9}} justify="center" items="center" '
            f'py={{11}} rounded={{11}} bg="var:bg/subtle">'
            f'{T(12,"semibold","var:text/accent",txt)}{I("arrow-right",14,A_IC)}</Frame>')

def capped(rows, keep, label, name, footer=None):
    """A dgroup that shows `keep` rows and sends the rest to the screen that owns them."""
    total = len(rows)
    body = hr().join(rows[:keep])
    tail = (hr() + see_all(label, name, total)) if total > keep else ''
    return body + tail

def sec_row(ic, label, summary, name, value=None, tone=None):
    """A way into a section. Carries a count so the hub still tells you the shape of the
    day without unrolling it."""
    return drow(ic, label, value=value, name=name, sub=summary, tone=tone)

def hub_sections(rows, title="More on this screen"):
    return dgroup(title, rows, p=14)

def mob_hub(name, head, pinned, sections, tab=None, foot=None, sec_title="More on this screen"):
    """The mobile landing for a desktop screen. Header, the one thing you act on now, and
    a short list of ways in. Everything else lives one tap away."""
    body = (pinned or '') + (hub_sections(sections, sec_title) if sections else '') + (foot or '')
    return dr_mob(name, head, body, tab)

def mob_section(name, title, sub, body, tab=None, stats=None, foot=None, right=None):
    """One subject, one screen. Back always returns to the hub that opened it."""
    return dr_mob(name, dr_head(title, sub, back=True, stats=stats, right=right),
                  body + (foot or ''), tab)

def dr_sheet(name, title, sub, body, actions=None, behind=None, peek=None):
    """A bottom sheet over a dimmed hub — the "opens like a dialogue" case. Used only for a
    single decision; anything with its own scroll is a section, not a sheet.

    `peek` is the strip of the screen underneath that stays visible. The DSL has no opacity,
    so the dim is a flat slate fill rather than a translucent one; in build it is 55% black.
    """
    # Tapping the scrim closes the sheet, the same as the X.
    top = (f'<Frame name="Btn Close sheet" w="fill" grow={{1}} flex="col" bg="#2A3948" '
           f'overflow="hidden">{peek or ""}</Frame>')
    acts = (f'<Frame w="fill" flex="col" gap={{9}} pt={{4}}>{actions}</Frame>') if actions else ''
    card = (f'<Frame w="fill" flex="col" gap={{14}} px={{18}} pt={{12}} pb={{22}} rounded={{26}} '
            f'bg="var:bg/base">'
            f'<Frame w="fill" flex="row" justify="center"><Rect w={{40}} h={{4}} rounded={{999}} '
            f'bg="var:neutral/300" /></Frame>'
            f'<Frame w="fill" flex="row" justify="between" items="start" gap={{12}}>'
            f'<Frame grow={{1}} flex="col" gap={{3}}>{T(18,"bold","var:text/strong",title)}'
            + (T(12, "regular", "var:text/muted", sub, w="fill") if sub else '')
            + f'</Frame><Frame name="Btn Close sheet" w={{32}} h={{32}} rounded={{999}} '
            f'bg="var:bg/muted" flex="col" justify="center" items="center">{I("x",16,N_IC)}</Frame></Frame>'
            f'{body}{acts}</Frame>')
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" bg="#2A3948" overflow="hidden">'
            f'{top}{card}</Frame>')

def sheet_pick(ic, label, sub, name, tone=None):
    """A row inside a sheet. Bigger tap target than a list row — a sheet is a decision."""
    tint = {"warn": "var:state/warning-bg", "err": "var:state/error-bg", "ok": "var:state/success-bg",
            "info": "var:state/info-bg", None: "var:bg/muted"}[tone]
    hexc = {"warn": WARN_IC, "err": ERR_IC, "ok": OK_IC, "info": A_IC, None: A_IC}[tone]
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{13}} items="center" p={{13}} '
            f'rounded={{14}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{38}} h={{38}} rounded={{12}} bg="{tint}" flex="col" justify="center" '
            f'items="center">{I(ic,18,hexc)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",label)}{s}</Frame>'
            f'{I("chevron-right",15,M_IC)}</Frame>')

# ---------------------------------------------------------------- routing an order outward
def dept_choice(ic, label, desc, name, sel=False, tone="info", meta=None):
    """Where an order goes. Wider than outcome_choice because the deciding information is
    the third line — how busy they are, how long they take, what they cannot do."""
    tint = {"info": "var:state/info-bg", "ok": "var:state/success-bg", "warn": "var:state/warning-bg",
            "err": "var:state/error-bg", "muted": "var:neutral/100"}[tone]
    c = {"info": A_IC, "ok": OK_IC, "warn": WARN_IC, "err": ERR_IC, "muted": M_IC}[tone]
    bd = "var:border/accent" if sel else "var:border/subtle"
    bw = 2 if sel else 1
    m = (f'<Frame w="fill" flex="row" gap={{7}} items="center" px={{10}} py={{6}} rounded={{8}} '
         f'bg="var:neutral/50">{I("info",12,M_IC)}'
         f'{T(11,"regular","var:text/muted",meta,w="fill")}</Frame>') if meta else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{9}} p={{14}} rounded={{14}} '
            f'bg="var:bg/base" stroke="{bd}" strokeWidth={{{bw}}}>'
            f'<Frame w="fill" flex="row" gap={{12}} items="start">'
            f'<Frame w={{36}} h={{36}} rounded={{12}} bg="{tint}" flex="col" justify="center" items="center">'
            f'{I(ic,17,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",label)}'
            f'{T(11,"regular","var:text/muted",desc,w="fill")}</Frame>'
            f'{I("circle-check",18,T_IC) if sel else I("circle",18,M_IC)}</Frame>{m}</Frame>')

def track_step(label, when, done=False, current=False, sub=None):
    """One step of an order's life. Three states — done, happening, not yet — because a
    doctor's question is never "where is it" but "should I be chasing it"."""
    if done:
        dot = (f'<Frame w={{26}} h={{26}} rounded={{999}} bg="var:brand/teal" flex="col" justify="center" '
               f'items="center">{I("check",14,W_IC)}</Frame>')
        col, wcol = "var:text/muted", "var:text/faint"
    elif current:
        dot = (f'<Frame w={{26}} h={{26}} rounded={{999}} bg="var:state/warning-bg" flex="col" justify="center" '
               f'items="center">{I("loader",14,WARN_IC)}</Frame>')
        col, wcol = "var:text/strong", "var:state/warning"
    else:
        dot = '<Rect w={26} h={26} rounded={999} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />'
        col, wcol = "var:text/faint", "var:text/faint"
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame w="fill" flex="row" gap={{12}} items="start" py={{9}}>{dot}'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold",col,label)}{s}</Frame>'
            f'{T(11,"semibold" if current else "regular",wcol,when)}</Frame>')

def link_row_dr(who, what, state, when, name):
    """A single-use link in the doctor's own list. The state pill is the whole point of the
    row: open, used and expired need three different reactions from a doctor."""
    conf = {"open":    ("var:state/warning-bg", "var:state/warning", "Open", WARN_IC),
            "used":    ("var:state/success-bg", "var:state/success", "Used", OK_IC),
            "expired": ("var:neutral/100", "var:text/muted", "Expired", M_IC),
            "revoked": ("var:state/error-bg", "var:state/error", "Revoked", ERR_IC)}[state]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="{conf[0]}" flex="col" justify="center" items="center">'
            f'{I("link",16,conf[3])}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(11,"regular","var:text/muted",what,w="fill")}</Frame>'
            f'<Frame flex="col" gap={{3}} items="end">'
            f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="{conf[0]}">'
            f'{T(10,"semibold",conf[1],conf[2])}</Frame>'
            f'{T(10,"regular","var:text/faint",when)}</Frame>{I("chevron-right",15,M_IC)}</Frame>')


def range_cal(month="August 2026", ranges=(), booked=(), name="Off"):
    """A month you select on, not two dropdowns you type into.

    Godwin, 14 Aug — "instead of selecting from 22nd August to 26th, and I still want to select
    from 30th, I need to do that multiple times. I can just pick the dates on the calendar and
    it is easier that way." Abraham: "a single calendar where you can click and it highlights
    the range for you… you need a single calendar to do that."

    `ranges` is a list of (start, end, label) day numbers; a day inside one is filled, the ends
    are rounded, and a day carrying an appointment keeps its marker so you can see what you are
    about to cancel before you select it, not after.
    """
    inside, starts, ends, solo = set(), set(), set(), set()
    for a, b, _ in ranges:
        a, b = int(a), int(b)
        if a == b:
            solo.add(str(a)); continue
        starts.add(str(a)); ends.add(str(b))
        for d in range(a + 1, b):
            inside.add(str(d))

    cols = ""
    for day, nums in MONTH:
        cells = f'{T(10,"semibold","var:text/faint",day)}'
        for n in nums:
            # the first row carries the tail of the previous month, and those numbers repeat
            # later in the grid — 30 July and 30 August are both "30". A selection must never
            # land on the leading ones.
            faint = n in ("27", "28", "29", "30") and nums.index(n) == 0
            sel = (not faint) and (n in inside or n in starts or n in ends or n in solo)
            if sel:
                r = ("rounded={10}" if n in solo else
                     "roundedTopLeft={10} roundedBottomLeft={10}" if n in starts else
                     "roundedTopRight={10} roundedBottomRight={10}" if n in ends else "")
                cells += (f'<Frame name="Btn {name} {n}" w="fill" flex="col" gap={{2}} items="center" '
                          f'py={{7}} {r} image="assets/img/btn-navy.jpg" overflow="hidden">'
                          f'{T(12,"bold","var:text/on-dark",n)}'
                          + ('<Ellipse w={4} h={4} bg="#FFFFFF" />' if n in booked
                             else '<Frame h={4} w={4} />') + '</Frame>')
            else:
                dot = ('<Ellipse w={4} h={4} bg="#2F8BAC" />' if n in booked else '<Frame h={4} w={4} />')
                cells += (f'<Frame name="Btn {name} {n}" w="fill" flex="col" gap={{2}} items="center" py={{7}} '
                          f'rounded={{10}}>{T(12,"medium","var:text/faint" if faint else "var:text/default",n)}'
                          f'{dot}</Frame>')
        cols += f'<Frame grow={{1}} flex="col" gap={{3}} items="center">{cells}</Frame>'

    chips = ""
    for a, b, label in ranges:
        chips += (f'<Frame name="Btn Range {a}" flex="row" gap={{7}} items="center" px={{11}} py={{6}} '
                  f'rounded={{999}} bg="var:state/info-bg">'
                  f'{T(11,"semibold","var:text/accent",label)}{I("x",12,A_IC)}</Frame>')
    legend = (f'<Frame w="fill" flex="row" gap={{16}} items="center" pt={{2}}>'
              f'<Frame flex="row" gap={{6}} items="center">'
              f'<Frame w={{10}} h={{10}} rounded={{3}} image="assets/img/btn-navy.jpg" overflow="hidden" />'
              f'{T(10,"regular","var:text/muted","Not available")}</Frame>'
              f'<Frame flex="row" gap={{6}} items="center"><Ellipse w={{6}} h={{6}} bg="#2F8BAC" />'
              f'{T(10,"regular","var:text/muted","Somebody is booked")}</Frame></Frame>')
    return (f'<Frame w="fill" flex="col" gap={{12}} p={{18}} rounded={{16}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(15,"bold","var:text/strong",month)}'
            f'<Frame flex="row" gap={{8}} items="center">'
            f'<Frame name="Btn Prev month" flex="row">{I("chevron-left",17,M_IC)}</Frame>'
            f'<Frame name="Btn Next month" flex="row">{I("chevron-right",17,M_IC)}</Frame></Frame></Frame>'
            f'{T(11,"regular","var:text/muted","Drag across the days you will not be here.",w="fill")}'
            f'<Frame w="fill" flex="row" gap={{4}}>{cols}</Frame>'
            + (f'<Frame w="fill" flex="row" gap={{8}}>{chips}</Frame>' if chips else '')
            + f'{legend}</Frame>')


# =====================================================================================
# THE STRUCTURED EXAMINATION TEMPLATE
#
# Godwin, third review: "Blood pressure this over this, and the doctor just puts in the
# numbers… sometimes you are rushing with a patient and you forget some of the things you
# needed to do, but if you see a template of what you need to fill in, then you know."
#
# He is describing a checklist that prevents omission under time pressure, not a data-entry
# convenience — which is why the empty fields are drawn as visibly empty rather than hidden.
#
# **The field list is taken from published convention, not invented, and still needs a
# clinician's sign-off before build.** Sources, all in `docs/Clinical_Templates.md`:
#
#   · the five conventional vital signs — temperature, pulse, respiratory rate, blood
#     pressure, oxygen saturation — plus height, weight and a **computed** BMI, which is how
#     every vital-signs template and the CDISC VS domain define the set;
#   · blood pressure **recorded twice**, because the WHO HEARTS protocol — the one running in
#     60 primary-care centres in the FCT under the Hypertension Treatment in Nigeria
#     programme, which is Medra's own pilot geography — defines hypertension on two readings,
#     not one. A template that takes a single reading cannot express the diagnosis it is for;
#   · BMI computed rather than typed, which is Godwin's explicit ask and also the thing that
#     stops a busy clinic recording height and weight and never doing anything with them.
#
# What the template deliberately does NOT do is score, warn or diagnose. It colours a value
# that is outside the reference range and stops there.
# =====================================================================================
VITAL_TONE = {"ok": ("var:state/success-bg", "var:state/success"),
              "warn": ("var:state/warning-bg", "var:state/warning"),
              "err": ("var:state/error-bg", "var:state/error"),
              None: ("var:neutral/50", "var:text/strong"),
              "empty": ("var:neutral/50", "var:text/faint")}


def vital(label, value, unit, name, tone=None, ref=None, computed=False):
    """One measurement. An empty one still draws its box and its unit, because the point of the
    template is that you can see what you have not done yet."""
    empty = not value
    bg, col = VITAL_TONE["empty" if empty else tone]
    # Three tiles across a 410px column leaves about 100px inside each one, and "136/86 mmHg"
    # does not fit on one line in it — the first version broke the number itself, which on a
    # blood-pressure field is worse than useless. Label above, value and unit on their own
    # line at a size that fits, and the "Calculated" marker moves to the reference line where
    # it does not compete with the label for width.
    r = ref or ("Calculated" if computed else None)
    foot = (f'<Frame w="fill" flex="row" gap={{4}} items="center">'
            + (I("calculator", 9, M_IC) if computed else '')
            + T(9, "regular", "var:text/faint", r, w="fill") + '</Frame>') if r else ''
    return (f'<Frame name="Btn Vital {name}" grow={{1}} flex="col" gap={{5}} p={{11}} rounded={{12}} '
            f'bg="{bg}" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{T(10,"semibold","var:text/muted",label,w="fill")}'
            f'<Frame w="fill" flex="row" gap={{3}} items="end">'
            f'{T(17,"bold",col,value or "—")}'
            f'{T(9,"regular","var:text/muted",unit)}</Frame>{foot}</Frame>')


def vitals_grid(rows, title="Examination", action=None, foot=None):
    """`rows` is a list of lists of `vital()` — you control the shape, because a paediatric
    template and an antenatal one do not want the same grid."""
    head = (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{7}} items="center">{I("stethoscope",14,A_IC)}'
            f'{T(12,"semibold","var:text/default",title)}</Frame>{action or ""}</Frame>')
    body = "".join(f'<Frame w="fill" flex="row" gap={{9}}>{"".join(r)}</Frame>' for r in rows)
    ft = T(10, "regular", "var:text/muted", foot, w="fill") if foot else ''
    return f'<Frame w="fill" flex="col" gap={{9}}>{head}{body}{ft}</Frame>'
