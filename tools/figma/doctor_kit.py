#!/usr/bin/env python3
"""Medra — Doctor app design system.

**This is deliberately not the member app.** A member opens Medra once a month; a doctor lives
in it between patients. So the doctor app is built as a clinical workstation, and it should be
recognisable as a different product from three metres away:

| | Member app | Doctor app |
|---|---|---|
| Navigation | one 262px navy sidebar | **88px icon rail + 236px contextual panel** |
| Ground | soft mesh gradient | **graph paper** — the ruled sheet a clinic already runs on |
| Corners | 24–28px | **14–18px** |
| Density | generous, one thing at a time | dense — a whole queue on one screen |
| Top bar | light search bar | **dark command strip** with the day's progress and urgent count |
| Mobile chrome | light appbar | **navy header block** with the day's numbers in it |
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
    ft = (f'{hr()}<Frame w="fill" flex="row" gap={{8}} items="start" pt={{2}}>{I("info",13,M_IC)}'
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

def stat_tile(ic, value, label, sub=None, tone="info", name=None):
    tint = {"info": "tint-blue.jpg", "ok": "tint-mint.jpg", "warn": "tint-amber.jpg",
            "err": "tint-red.jpg", "teal": "tint-teal.jpg", "slate": "tint-slate.jpg",
            "navy": "tint-navy.jpg", "ocean": "tint-ocean.jpg"}[tone]
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame name="Btn {name or label}" grow={{1}} flex="col" gap={{10}} p={{16}} rounded={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} image="assets/img/{tint}" overflow="hidden" '
            f'flex="col" justify="center" items="center">{I(ic,17,W_IC)}</Frame>'
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
# DESKTOP SHELL — icon rail + contextual panel + command strip
# =====================================================================================
RAIL = [("layout-dashboard", "Today",    "Nav Today"),
        ("inbox",            "Requests", "Nav Requests"),
        ("calendar-days",    "Schedule", "Nav Schedule"),
        ("users",            "Patients", "Nav Patients"),
        ("notebook-pen",     "Consults", "Nav Consults"),
        ("banknote",         "Money",    "Nav Money"),
        ("trending-up",      "Growth",   "Nav Growth"),
        ("settings",         "Settings", "Nav Settings")]

def rail(active=0, badges=None):
    badges = badges or {}
    cells = ""
    for i, (ic, label, nm) in enumerate(RAIL):
        on = i == active
        chip = ''
        if badges.get(label):
            chip = (f'<Frame flex="row" px={{6}} py={{1}} rounded={{999}} bg="#D14343">'
                    f'{T(9,"bold","var:text/on-dark",str(badges[label]))}</Frame>')
        box = ('bg="#17324D" stroke="#2B5B85" strokeWidth={1}' if on else '')
        cells += (f'<Frame name="Btn {nm}" w="fill" flex="col" gap={{5}} items="center" py={{10}} '
                  f'rounded={{13}} {box}>'
                  f'<Frame flex="row" gap={{4}} items="start">{I(ic,20,RAIL_ON if on else RAIL_DIM)}{chip}</Frame>'
                  f'{T(9,"semibold" if on else "medium","var:text/on-dark" if on else "#7FA3BE",label)}</Frame>')
    return (f'<Frame w={{88}} h="fill" flex="col" gap={{6}} px={{9}} pt={{18}} pb={{16}} '
            f'image="assets/img/rail.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="col" gap={{4}} items="center" pb={{10}}>'
            f'<Image image="assets/logo/appicon.png" w={{40}} h={{40}} rounded={{11}} />'
            f'<Frame flex="row" px={{7}} py={{2}} rounded={{999}} bg="#17324D">'
            f'{T(8,"bold","var:brand/teal","CLINIC")}</Frame></Frame>'
            f'{cells}<Frame grow={{1}} />'
            f'<Frame name="Btn Open help" w="fill" flex="col" gap={{5}} items="center" py={{9}} rounded={{13}}>'
            f'{I("circle-help",19,RAIL_DIM)}{T(9,"medium","#7FA3BE","Help")}</Frame>'
            f'<Frame name="Btn Nav Settings" w="fill" flex="col" items="center" pt={{6}}>'
            f'<Image image="assets/img/avatar-4.jpg" w={{36}} h={{36}} rounded={{999}} /></Frame></Frame>')

def panel(title, body, foot=None):
    """The 236px contextual column. Every section fills it with what that section needs next —
    it is the main reason the doctor app can be dense without being cluttered."""
    ft = f'<Frame grow={{1}} /><Frame w="fill" flex="col" gap={{9}}>{foot}</Frame>' if foot else '<Frame grow={1} />'
    return (f'<Frame w={{236}} h="fill" flex="col" gap={{14}} px={{16}} pt={{20}} pb={{18}} '
            f'image="assets/img/panel.jpg" overflow="hidden" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{T(11,"semibold","var:text/accent",title.upper())}{body}{ft}</Frame>')

def command(crumbs, right=None, urgent=2):
    trail = ""
    for i, c in enumerate(crumbs):
        last = i == len(crumbs) - 1
        trail += T(13, "semibold" if last else "regular",
                   "var:text/on-dark" if last else "var:text/on-dark-muted", c)
        if not last:
            trail += I("chevron-right", 13, "#7FA3BE")
    ug = (f'<Frame name="Btn Nav Requests" flex="row" gap={{7}} items="center" px={{11}} py={{7}} rounded={{10}} bg="#3A1E22" '
          f'stroke="#7A3238" strokeWidth={{1}}>{I("triangle-alert",13,"#F08A8A")}'
          f'{T(12,"semibold","#F5B5B5",f"{urgent} need you")}</Frame>') if urgent else ''
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{24}} py={{13}} '
            f'image="assets/img/command.jpg" overflow="hidden">'
            f'<Frame flex="row" gap={{9}} items="center">{trail}</Frame>'
            f'<Frame flex="row" gap={{11}} items="center">{ug}'
            f'<Frame name="Btn Search patient" flex="row" gap={{9}} items="center" px={{13}} py={{8}} rounded={{10}} '
            f'bg="#17324D" stroke="#24486B" strokeWidth={{1}}>{I("search",14,"#7FA3BE")}'
            f'{T(12,"regular","#9FBED6","Search patient or Medra ID")}'
            f'<Frame flex="row" px={{6}} py={{2}} rounded={{6}} bg="#0F2233">'
            f'{T(10,"semibold","#7FA3BE","⌘K")}</Frame></Frame>'
            f'<Frame name="Btn Notifications" flex="row" px={{9}} py={{8}} rounded={{10}} bg="#17324D">'
            f'{I("bell",15,"#9FBED6")}</Frame>'
            f'{right or ""}</Frame></Frame>')

def dr_desk(name, crumbs, children, active=0, panel_block=None, urgent=2, cmd_right=None, badges=None):
    p = panel_block if panel_block is not None else ''
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="row" image="assets/img/surface-clinic.jpg" '
            f'overflow="hidden">{rail(active,badges)}{p}'
            f'<Frame grow={{1}} h="fill" flex="col">'
            f'{command(crumbs,cmd_right,urgent)}'
            f'<Frame grow={{1}} w="fill" flex="col" gap={{16}} px={{28}} py={{22}}>{children}</Frame></Frame></Frame>')

# =====================================================================================
# MOBILE SHELL — navy header block, then graph paper, then a tab bar with a raised action
# =====================================================================================
MTABS = [("layout-dashboard", "Today", "Nav Today"), ("inbox", "Requests", "Nav Requests"),
         ("stethoscope", "Consult", "Start consult"), ("users", "Patients", "Nav Patients"),
         ("ellipsis", "More", "Nav Settings")]

def dr_tabbar(active=0):
    cells = ""
    for i, (ic, label, nm) in enumerate(MTABS):
        if i == 2:
            cells += (f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{4}} items="center">'
                      f'<Frame w={{46}} h={{46}} rounded={{15}} image="assets/img/btn-navy.jpg" overflow="hidden" '
                      f'flex="col" justify="center" items="center">{I(ic,21,W_IC)}</Frame>'
                      f'{T(9,"semibold","var:text/strong",label)}</Frame>')
            continue
        on = i == active
        cells += (f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{5}} items="center" pt={{6}}>'
                  f'{I(ic,20,T_IC if on else M_IC)}'
                  f'{T(9,"semibold" if on else "regular","var:text/accent" if on else "var:text/muted",label)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{4}} items="center" px={{12}} pt={{9}} pb={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}} rounded={{20}}>{cells}</Frame>')

def dr_head(title, sub=None, back=True, right=None, stats=None, chips=None):
    """Navy header block — the single strongest signal that this is not the member app."""
    left = (f'<Frame name="Btn Back" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" '
            f'items="center">{I("arrow-left",18,W_IC)}</Frame>' if back else
            f'<Image image="assets/logo/appicon.png" w={{38}} h={{38}} rounded={{11}} />')
    rt = right if right is not None else (
        f'<Frame name="Btn Notifications" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" '
        f'justify="center" items="center">{I("bell",17,W_IC)}</Frame>')
    subline = T(12, "regular", "var:text/on-dark-muted", sub, w="fill") if sub else ""
    statrow = ''
    if stats:
        cells = ""
        for v, l in stats:
            cells += (f'<Frame grow={{1}} flex="col" gap={{2}} px={{11}} py={{10}} rounded={{12}} bg="#17324D">'
                      f'{T(17,"bold","var:text/on-dark",v)}{T(10,"regular","#9FBED6",l)}</Frame>')
        statrow = f'<Frame w="fill" flex="row" gap={{8}} pt={{2}}>{cells}</Frame>'
    chiprow = ''
    if chips:
        cc = ""
        for label, nm, on in chips:
            st = ('image="assets/img/btn-teal.jpg" overflow="hidden"' if on else 'bg="#17324D"')
            cc += (f'<Frame name="Btn {nm}" flex="row" px={{12}} py={{7}} rounded={{999}} {st}>'
                   f'{T(12,"semibold","var:text/on-dark",label)}</Frame>')
        chiprow = f'<Frame w="fill" flex="row" gap={{8}} pt={{2}}>{cc}</Frame>'
    return (f'<Frame w="fill" flex="col" gap={{11}} px={{18}} pt={{8}} pb={{18}} '
            f'image="assets/img/head-m.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="row" justify="between" items="center">{left}'
            f'<Frame grow={{1}} flex="col" gap={{1}} px={{12}}>{T(17,"bold","var:text/on-dark",title)}{subline}</Frame>'
            f'{rt}</Frame>{statrow}{chiprow}</Frame>')

def dr_mob(name, head, children, tab=None):
    tabrow = f'<Frame w="fill" px={{12}} pb={{8}}>{dr_tabbar(tab)}</Frame>' if tab is not None else ''
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/surface-clinic-m.jpg" '
            f'overflow="hidden">{statusbar(dark=True)}{head}'
            f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{16}} pt={{14}} pb={{10}}>{children}</Frame>'
            f'{tabrow}</Frame>')

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
    action = (dbtn("Start", "Start " + name, "stethoscope", "navy", grow=False, size="sm") if now
              else dbtn("Open", "Open " + name, "chevron-right", "ghost", grow=False, size="sm"))
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
                f'{I("file-text",11,M_IC)}{T(11,"regular","var:text/muted",reason,w="fill")}</Frame></Frame>')
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{10}} p={{14}} rounded={{14}} bg="var:bg/base" {edge}>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Frame w={{54}} flex="col" gap={{1}} items="center">'
            f'{T(15,"bold","var:text/strong",time)}{T(10,"regular","var:text/muted","30 min")}</Frame>'
            f'<Rect w={{1}} h={{40}} bg="var:border/subtle" />'
            f'<Image image="assets/img/{avatar}" w={{40}} h={{40}} rounded={{12}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{8}} items="center">{T(14,"semibold","var:text/strong",who)}{status_pill(kind,size=10)}</Frame>'
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
