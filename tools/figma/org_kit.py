#!/usr/bin/env python3
"""Medra — Organisation console design system.

**Three products, three structures.** A member opens Medra monthly; a doctor uses it between
patients; a front desk stares at it for eight hours. So the organisation console is the only
one whose chrome is dark-first and whose navigation is *contextual* rather than sectional —
an org admin's first question is never "which page", it is **"which branch, which department"**.

| | Member | Doctor | Organisation |
|---|---|---|---|
| Ground | soft blue mesh | soft blue, white card | warm graphite on off-white |
| Navigation | 262px navy sidebar | 206px navy sidebar + light rail | 88px icon rail + a persistent context bar |
| Context | none needed | the patient | branch x department switcher, always visible |
| Accent | teal | navy + coral | amber (seats, counts, anything the admin owns) |
| Density | one thing at a time | a clinic day | a board: queues, tables, allocation |
| Mobile | light appbar, 5 tabs | gradient header card, 5 tabs | graphite header, role-aware tabs |

House rules carried over: no wrap="wrap", no items="stretch", grow is a row property, numeric
props keep their braces, every Text needs a font.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from shell import app_desk, title_from
from member2_kit import (hr, tabs, status_pill, prep_step, radio_row, consent_row, audit_row,
                         notif_row, empty_state, skel, skel_card, note_section, lab_line, kv, PILL)
from doctor_kit import (dcard, dgroup, drow, dtoggle, dbtn, dcta, eyerow, dhead, stat_tile,
                        alert_strip, kpi_line, bar, progress_row, see_all, capped, checklist_row,
                        patient_row, request_row, level_chip, file_row, month_cal, task_row,
                        rail_section, outcome_choice, field_chips)

AMBER_IC = "#B8801F"; GRAPH_IC = "#2A313A"; DIM_IC = "#8A94A0"

RAIL = [("layout-dashboard", "Today",       "Nav Today"),
        ("calendar-check",   "Bookings",    "Nav Bookings"),
        ("users",            "People",      "Nav People"),
        ("building-2",       "Departments", "Nav Departments"),
        ("share-2",          "Referrals",   "Nav Referrals"),
        ("shield-check",     "Access",      "Nav Access"),
        ("chart-column",     "Reports",     "Nav Reports"),
        ("settings",         "Settings",    "Nav Settings")]


def icon_rail(active=0, badges=None):
    """88px, icon over label. An org admin learns eight destinations in a day; after that the
    labels are noise and the width is better spent on the board."""
    badges = badges or {}
    cells = ""
    for i, (ic, label, nm) in enumerate(RAIL):
        on = i == active
        chip = ''
        if badges.get(label):
            chip = (f'<Frame flex="row" px={{6}} py={{1}} rounded={{999}} image="assets/img/btn-amber.jpg" '
                    f'overflow="hidden">{T(9,"bold","var:text/on-dark",str(badges[label]))}</Frame>')
        st = 'bg="#2E3640"' if on else ''
        cells += (f'<Frame name="Btn {nm}" w="fill" flex="col" gap={{4}} items="center" py={{10}} '
                  f'rounded={{14}} {st}>'
                  f'<Frame flex="row" gap={{4}} items="center">{I(ic,19,"#FFFFFF" if on else "#8A94A0")}{chip}</Frame>'
                  f'{T(9,"semibold" if on else "regular","var:text/on-dark" if on else "#8A94A0",label)}</Frame>')
    return (f'<Frame w={{88}} h="fill" flex="col" gap={{4}} px={{8}} pt={{18}} pb={{16}} '
            f'image="assets/img/rail-org.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="col" gap={{5}} items="center" pb={{14}}>'
            f'<Image image="assets/logo/appicon.png" w={{34}} h={{34}} rounded={{11}} />'
            f'{T(8,"semibold","#D6942E","ORG")}</Frame>'
            f'{cells}<Frame grow={{1}} />'
            f'<Frame name="Btn Open help" w="fill" flex="col" gap={{4}} items="center" py={{10}}>'
            f'{I("circle-help",18,"#8A94A0")}{T(9,"regular","#8A94A0","Help")}</Frame>'
            f'<Frame name="Btn Sign out" w="fill" flex="col" gap={{4}} items="center" py={{10}}>'
            f'{I("log-out",18,"#8A94A0")}{T(9,"regular","#8A94A0","Log out")}</Frame></Frame>')


def ctx_bar(branch="Garki Medical Centre", dept="All departments", crumbs=("Today",), urgent=0,
            right=None, who=("Mrs. Adaeze Nwosu", "Organisation admin")):
    """The piece of chrome that makes this an organisation console: which branch, which
    department. It never scrolls away, because every number on every screen is relative to it."""
    ug = (f'<Frame name="Btn Nav Today" flex="row" gap={{7}} items="center" px={{11}} py={{7}} '
          f'rounded={{10}} bg="#3A2A20">{I("triangle-alert",13,"#E8A24A")}'
          f'{T(12,"semibold","#F0C179",f"{urgent} need you")}</Frame>') if urgent else ''
    trail = " · ".join(crumbs)
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{14}} px={{20}} py={{12}} '
            f'image="assets/img/ctxbar.jpg" overflow="hidden">'
            f'<Frame flex="row" gap={{9}} items="center">'
            f'<Frame name="Btn Switch branch" flex="row" gap={{9}} items="center" px={{12}} py={{8}} '
            f'rounded={{11}} bg="#1B2027">{I("building-2",15,"#D6942E")}'
            f'<Frame flex="col" gap={{1}}>{T(9,"semibold","#8A94A0","BRANCH")}'
            f'{T(12,"semibold","var:text/on-dark",branch)}</Frame>{I("chevron-down",14,"#8A94A0")}</Frame>'
            f'<Frame name="Btn Switch dept" flex="row" gap={{9}} items="center" px={{12}} py={{8}} '
            f'rounded={{11}} bg="#1B2027">{I("layers",15,"#8A94A0")}'
            f'<Frame flex="col" gap={{1}}>{T(9,"semibold","#8A94A0","DEPARTMENT")}'
            f'{T(12,"semibold","var:text/on-dark",dept)}</Frame>{I("chevron-down",14,"#8A94A0")}</Frame>'
            f'<Frame flex="row" px={{10}}>{T(11,"regular","#8A94A0",trail)}</Frame></Frame>'
            f'<Frame flex="row" gap={{10}} items="center">{ug}'
            f'<Frame name="Btn Search member" w={{210}} flex="row" gap={{9}} items="center" px={{12}} py={{9}} '
            f'rounded={{11}} bg="#1B2027">{I("search",15,"#8A94A0")}'
            f'{T(12,"regular","#8A94A0","Name or Medra ID",w="fill")}</Frame>'
            f'<Frame name="Btn Notifications" flex="row" px={{10}} py={{10}} rounded={{11}} bg="#1B2027">'
            f'{I("bell",16,"#8A94A0")}</Frame>'
            f'<Frame name="Btn Nav Settings" flex="row" gap={{9}} items="center">'
            f'<Frame w={{118}} flex="col" gap={{1}} items="end">'
            f'{T(12,"semibold","var:text/on-dark",who[0])}{T(9,"regular","#8A94A0",who[1])}</Frame>'
            f'<Image image="assets/img/avatar-3.jpg" w={{34}} h={{34}} rounded={{999}} /></Frame>'
            f'{right or ""}</Frame></Frame>')


# The pill has to name the person actually looking at the screen. An org frame says which
# department it belongs to in its own name — "Org · Pharmacy — D9 …" — so read it from there
# rather than making every call site remember to pass it.
SECTION_PERSONA = {
    "front desk": "desk", "nursing": "nurse", "laboratory": "lab", "lab": "lab",
    "pharmacy": "pharm", "imaging": "imaging", "radiology": "imaging", "billing": "billing",
    "doctor": "orgdoc",
}


def persona_of(name):
    head = name.split("—")[0]
    section = head.split("·")[-1].strip().lower() if "·" in head else ""
    return SECTION_PERSONA.get(section, "admin")


def o_desk(name, crumbs, children, active=0, branch="Garki Medical Centre", dept="All departments",
           urgent=0, aside=None, who=("Mrs. Adaeze Nwosu", "Organisation admin"), badges=None,
           persona=None):
    """Delegates to the one shell. The branch x department context that used to need its own
    bar is now the subtitle — it is context, not navigation, and it was taking a whole band of
    the screen to say so."""
    nav = [(ic, nm, label) for ic, label, nm in RAIL]
    bad = {("Nav " + k) for k in (badges or {}) if (badges or {}).get(k)}
    title = crumbs[-1] if crumbs else title_from(name)
    return app_desk(name, persona or persona_of(name), title,
                    f'<Frame w="fill" flex="col" gap={{16}}>{children}</Frame>',
                    nav, active, sub=f"{branch} · {dept}", side=aside, badges=bad, who=who,
                    search="Btn Search member")

def o_tabs(items, active=0):
    cells = ""
    for i, (ic, label, nm) in enumerate(items):
        on = i == active
        cells += (f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{5}} items="center" pt={{6}}>'
                  f'{I(ic,20,GRAPH_IC if on else M_IC)}'
                  f'{T(9,"semibold" if on else "regular","var:text/strong" if on else "var:text/muted",label)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{4}} items="center" px={{12}} pt={{9}} pb={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}} rounded={{22}}>{cells}</Frame>')


def o_head(title, sub=None, back=True, right=None, stats=None, chips=None, ctx=None):
    left = (f'<Frame name="Btn Back" w={{36}} h={{36}} rounded={{12}} bg="#2E3640" flex="col" '
            f'justify="center" items="center">{I("arrow-left",17,W_IC)}</Frame>' if back else
            f'<Image image="assets/logo/appicon.png" w={{36}} h={{36}} rounded={{11}} />')
    _bell = (f'<Frame name="Btn Notifications" w={{36}} h={{36}} rounded={{12}} bg="#2E3640" flex="col" '
             f'justify="center" items="center">{I("bell",16,W_IC)}</Frame>')
    _search = (f'<Frame name="Btn Search member" w={{36}} h={{36}} rounded={{12}} bg="#2E3640" flex="col" '
               f'justify="center" items="center">{I("search",16,W_IC)}</Frame>')
    if right is not None: rt = right
    elif back: rt = _bell
    else: rt = f'<Frame flex="row" gap={{8}} items="center">{_search}{_bell}</Frame>'
    ctxrow = ''
    if ctx:
        ctxrow = (f'<Frame name="Btn Switch branch" w="fill" flex="row" gap={{8}} items="center" '
                  f'px={{12}} py={{9}} rounded={{12}} bg="#1B2027">{I("building-2",14,"#D6942E")}'
                  f'{T(11,"semibold","var:text/on-dark",ctx,w="fill")}{I("chevron-down",14,"#8A94A0")}</Frame>')
    subline = T(12, "regular", "#A9B2BC", sub, w="fill") if sub else ""
    statrow = ''
    if stats:
        cells = ""
        for v, l in stats:
            cells += (f'<Frame grow={{1}} flex="col" gap={{2}} px={{11}} py={{10}} rounded={{13}} bg="#2E3640">'
                      f'{T(16,"bold","var:text/on-dark",v)}{T(10,"regular","#A9B2BC",l)}</Frame>')
        statrow = f'<Frame w="fill" flex="row" gap={{8}} pt={{2}}>{cells}</Frame>'
    chiprow = ''
    if chips:
        cc = ""
        for label, nm, on in chips:
            st = ('image="assets/img/btn-amber.jpg" overflow="hidden"' if on else 'bg="#2E3640"')
            cc += (f'<Frame name="Btn {nm}" flex="row" px={{12}} py={{7}} rounded={{999}} {st}>'
                   f'{T(12,"semibold","var:text/on-dark",label)}</Frame>')
        chiprow = f'<Frame w="fill" flex="row" gap={{8}} pt={{2}}>{cc}</Frame>'
    return (f'<Frame w="fill" flex="col" gap={{11}} px={{18}} pt={{16}} pb={{18}} rounded={{24}} '
            f'image="assets/img/head-org-m.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="row" justify="between" items="center">{left}'
            f'<Frame grow={{1}} flex="col" gap={{1}} px={{12}}>{T(17,"bold","var:text/on-dark",title)}{subline}</Frame>'
            f'{rt}</Frame>{ctxrow}{statrow}{chiprow}</Frame>')


def o_mob(name, head, children, tab_items=None, tab=None):
    tabrow = (f'<Frame w="fill" px={{12}} pb={{8}}>{o_tabs(tab_items, tab)}</Frame>'
              if tab_items and tab is not None else '')
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/canvas-org-m.jpg" '
            f'overflow="hidden">{statusbar()}'
            f'<Frame w="fill" px={{14}} pt={{2}}>{head}</Frame>'
            f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{14}} pt={{14}} pb={{10}}>{children}</Frame>'
            f'{tabrow}</Frame>')


O_PEEK = (f'{statusbar(dark=True)}'
          f'<Frame w="fill" flex="col" gap={{11}} px={{26}} pt={{18}}>'
          f'<Frame w="fill" h={{92}} rounded={{22}} bg="#2A313A" />'
          f'<Frame w="fill" flex="row" gap={{9}}>'
          f'<Frame grow={{1}} h={{54}} rounded={{14}} bg="#2A313A" />'
          f'<Frame grow={{1}} h={{54}} rounded={{14}} bg="#2A313A" /></Frame>'
          f'<Frame w="fill" h={{74}} rounded={{16}} bg="#2A313A" /></Frame>')


def o_sheet(name, title, sub, body, actions=None):
    acts = (f'<Frame w="fill" flex="col" gap={{9}} pt={{4}}>{actions}</Frame>') if actions else ''
    card_ = (f'<Frame w="fill" flex="col" gap={{14}} px={{18}} pt={{12}} pb={{22}} rounded={{26}} bg="var:bg/base">'
             f'<Frame w="fill" flex="row" justify="center"><Rect w={{40}} h={{4}} rounded={{999}} '
             f'bg="var:neutral/300" /></Frame>'
             f'<Frame w="fill" flex="row" justify="between" items="start" gap={{12}}>'
             f'<Frame grow={{1}} flex="col" gap={{3}}>{T(18,"bold","var:text/strong",title)}'
             + (T(12, "regular", "var:text/muted", sub, w="fill") if sub else '')
             + f'</Frame><Frame name="Btn Close sheet" w={{32}} h={{32}} rounded={{999}} bg="var:bg/muted" '
             f'flex="col" justify="center" items="center">{I("x",16,N_IC)}</Frame></Frame>{body}{acts}</Frame>')
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" bg="#242A31" overflow="hidden">'
            f'<Frame name="Btn Close sheet" w="fill" grow={{1}} flex="col" bg="#242A31" overflow="hidden">'
            f'{O_PEEK}</Frame>{card_}</Frame>')


def o_sec_row(ic, label, summary, name, value=None, tone=None):
    return drow(ic, label, value=value, name=name, sub=summary, tone=tone)


def o_hub_list(rows, title="More on this screen"):
    return dgroup(title, rows, p=14)


def sheet_pick(ic, label, sub, name, tone=None):
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


# =====================================================================================
# CONSOLE PARTS — a board, not a page
# =====================================================================================
DEPT = {"nursing": ("dept-nursing.jpg", "syringe", "Nursing"),
        "lab": ("dept-lab.jpg", "flask-conical", "Laboratory"),
        "pharmacy": ("dept-pharmacy.jpg", "pill", "Pharmacy"),
        "desk": ("dept-desk.jpg", "concierge-bell", "Front desk"),
        "clinic": ("dept-clinic.jpg", "stethoscope", "Consulting")}


def dept_badge(key, size=34):
    img, ic, _ = DEPT[key]
    return (f'<Frame w={{{size}}} h={{{size}}} rounded={{11}} image="assets/img/{img}" overflow="hidden" '
            f'flex="col" justify="center" items="center">{I(ic,int(size*0.5),W_IC)}</Frame>')


def dept_card(key, seats_used, seats_total, waiting, name, sub=None):
    img, ic, label = DEPT[key]
    pct = int(seats_used * 100 / max(1, seats_total))
    return (f'<Frame name="Btn {name}" grow={{1}} flex="col" gap={{12}} p={{16}} rounded={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">{dept_badge(key)}'
            f'<Frame flex="row" gap={{6}} items="center" px={{9}} py={{5}} rounded={{8}} bg="var:bg/muted">'
            f'{T(11,"semibold","var:text/default",f"{waiting} waiting")}</Frame></Frame>'
            f'<Frame w="fill" flex="col" gap={{3}}>{T(14,"semibold","var:text/strong",label)}'
            + (T(11, "regular", "var:text/muted", sub, w="fill") if sub else '')
            + f'</Frame>{bar(pct,"amber",7)}'
            f'{T(11,"regular","var:text/muted",f"{seats_used} of {seats_total} seats used")}</Frame>')


def board_col(title, count, rows, name, tone=None):
    """A column of the day board. Front desk lives here."""
    tint = {"warn": "var:state/warning-bg", "err": "var:state/error-bg",
            "ok": "var:state/success-bg", None: "var:bg/muted"}[tone]
    return (f'<Frame grow={{1}} flex="col" gap={{10}} p={{13}} rounded={{16}} bg="var:bg/subtle" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(12,"semibold","var:text/strong",title)}'
            f'<Frame flex="row" px={{8}} py={{3}} rounded={{999}} bg="{tint}">'
            f'{T(11,"semibold","var:text/default",str(count))}</Frame></Frame>'
            f'<Frame w="fill" flex="col" gap={{8}}>{rows}</Frame>'
            f'<Frame name="Btn {name}" w="fill" flex="row" justify="center" py={{8}} rounded={{10}} '
            f'bg="var:bg/base">{T(11,"semibold","var:text/accent","See all")}</Frame></Frame>')


def board_card(who, meta, name, tag=None, avatar="avatar-2.jpg", tone=None):
    pill = status_pill(tag, size=10) if tag else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{8}} p={{11}} rounded={{12}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{9}} items="center">'
            f'<Image image="assets/img/{avatar}" w={{30}} h={{30}} rounded={{9}} />'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(12,"semibold","var:text/strong",who)}'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame></Frame>{pill}</Frame>')


def seat_row(avatar, who, role, dept, meta, name, state="active"):
    tone = {"active": "ok", "invited": "warn", "suspended": "err"}[state]
    label = {"active": "Active", "invited": "Invited", "suspended": "Suspended"}[state]
    bg = {"ok": "var:state/success-bg", "warn": "var:state/warning-bg", "err": "var:state/error-bg"}[tone]
    col = {"ok": "var:state/success", "warn": "var:state/warning", "err": "var:state/error"}[tone]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Image image="assets/img/{avatar}" w={{36}} h={{36}} rounded={{11}} />'
            f'{T(13,"semibold","var:text/strong",who,w=150)}'
            f'{T(12,"regular","var:text/muted",role,w=124)}'
            f'{T(12,"regular","var:text/muted",dept,w=112)}'
            f'{T(11,"regular","var:text/faint",meta,w="fill")}'
            f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="{bg}">'
            f'{T(10,"semibold",col,label)}</Frame>{I("chevron-right",15,M_IC)}</Frame>')


def seat_row_m(avatar, who, role, dept, name, state="active"):
    tone = {"active": "ok", "invited": "warn", "suspended": "err"}[state]
    bg = {"ok": "var:state/success-bg", "warn": "var:state/warning-bg", "err": "var:state/error-bg"}[tone]
    col = {"ok": "var:state/success", "warn": "var:state/warning", "err": "var:state/error"}[tone]
    label = {"active": "Active", "invited": "Invited", "suspended": "Suspended"}[state]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" py={{10}}>'
            f'<Image image="assets/img/{avatar}" w={{34}} h={{34}} rounded={{11}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(10,"regular","var:text/muted",f"{role} · {dept}",w="fill")}</Frame>'
            f'<Frame flex="row" px={{8}} py={{3}} rounded={{7}} bg="{bg}">{T(10,"semibold",col,label)}</Frame>'
            f'{I("chevron-right",14,M_IC)}</Frame>')


def perm_row(label, allowed, why=None):
    ic, c, bg = (("check", OK_IC, "var:state/success-bg") if allowed
                 else ("x", ERR_IC, "var:state/error-bg"))
    return (f'<Frame w="fill" flex="row" gap={{11}} items="start" py={{9}}>'
            f'<Frame w={{24}} h={{24}} rounded={{8}} bg="{bg}" flex="col" justify="center" '
            f'items="center">{I(ic,13,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(12,"medium","var:text/strong",label)}'
            + (T(11, "regular", "var:text/muted", why, w="fill") if why else "") + '</Frame></Frame>')


# The verification component lives in medra_ui so the member, doctor and organisation
# modules all render it identically. `unverified` is kept as the org-local alias.
unverified = health_fact


def branch_row_m(name_, addr, staff, open_h, nm, main=False):
    tag = (f'<Frame flex="row" px={{8}} py={{3}} rounded={{6}} bg="var:state/info-bg">'
           f'{T(10,"semibold","var:text/accent","Main")}</Frame>') if main else ''
    return (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{11}} items="center" py={{11}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="var:bg/muted" flex="col" justify="center" '
            f'items="center">{I("building-2",16,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>'
            f'<Frame flex="row" gap={{7}} items="center">{T(13,"semibold","var:text/strong",name_)}{tag}</Frame>'
            f'{T(10,"regular","var:text/muted",addr,w="fill")}'
            f'{T(10,"regular","var:text/faint",f"{staff} · {open_h}",w="fill")}</Frame>'
            f'{I("chevron-right",14,M_IC)}</Frame>')


def link_row_m(who, what, state, when, nm):
    tone = {"open": ("warn", "Open"), "used": ("ok", "Used and expired"),
            "expired": ("muted", "Expired unused"), "revoked": ("err", "Revoked")}[state]
    bg = {"warn": "var:state/warning-bg", "ok": "var:state/success-bg",
          "muted": "var:bg/muted", "err": "var:state/error-bg"}[tone[0]]
    col = {"warn": "var:state/warning", "ok": "var:state/success",
           "muted": "var:text/muted", "err": "var:state/error"}[tone[0]]
    return (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{11}} items="center" py={{11}}>'
            f'<Frame w={{32}} h={{32}} rounded={{10}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I("link",15,ERR_IC if tone[0]=="err" else A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(10,"regular","var:text/muted",what,w="fill")}'
            f'<Frame flex="row" gap={{6}} items="center">'
            f'<Frame flex="row" px={{7}} py={{2}} rounded={{6}} bg="{bg}">{T(9,"semibold",col,tone[1])}</Frame>'
            f'{T(10,"regular","var:text/faint",when)}</Frame></Frame>'
            f'{I("chevron-right",14,M_IC)}</Frame>')


def board_stack(title, count, rows, name, tone=None):
    """The day board, one column at a time. Four columns side by side is a desktop idea."""
    tint = {"warn": "var:state/warning-bg", "err": "var:state/error-bg",
            "ok": "var:state/success-bg", None: "var:bg/muted"}[tone]
    return (f'<Frame w="fill" flex="col" gap={{9}} p={{13}} rounded={{16}} bg="var:bg/subtle" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(13,"semibold","var:text/strong",title)}'
            f'<Frame flex="row" px={{9}} py={{3}} rounded={{999}} bg="{tint}">'
            f'{T(11,"semibold","var:text/default",str(count))}</Frame></Frame>'
            f'<Frame w="fill" flex="col" gap={{8}}>{rows}</Frame>'
            f'<Frame name="Btn {name}" w="fill" flex="row" justify="center" py={{9}} rounded={{10}} '
            f'bg="var:bg/base">{T(11,"semibold","var:text/accent","See all")}</Frame></Frame>')


def alloc_row_m(time, who, meta, reason, nm, assigned=None):
    """The allocation card at 390. Desktop puts time, name, status and the button on one
    line; that line does not exist on a phone."""
    tag = (f'<Frame flex="row" gap={{6}} items="center" px={{9}} py={{4}} rounded={{7}} bg="var:state/success-bg">'
           f'{I("user-check",11,OK_IC)}{T(10,"semibold","var:state/success",assigned)}</Frame>' if assigned else
           f'<Frame flex="row" gap={{6}} items="center" px={{9}} py={{4}} rounded={{7}} bg="var:state/error-bg">'
           f'{I("user-x",11,ERR_IC)}{T(10,"semibold","var:state/error","Nobody assigned")}</Frame>')
    act = (dbtn("Change", "Change " + nm, "repeat", "ghost", full=True, size="sm") if assigned
           else dbtn("Assign someone", "Assign " + nm, "user-plus", "navy", full=True, size="sm"))
    return (f'<Frame name="Btn {nm}" w="fill" flex="col" gap={{9}} p={{12}} rounded={{14}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{10}} items="center">'
            f'{T(14,"bold","var:text/strong",time)}'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame></Frame>'
            f'<Frame w="fill" flex="row">{tag}</Frame>'
            f'<Frame w="fill" flex="row" gap={{8}} items="center" px={{10}} py={{8}} rounded={{10}} '
            f'bg="var:neutral/50">{I("file-text",11,M_IC)}'
            f'{T(10,"regular","var:text/muted",reason,w="fill")}</Frame>{act}</Frame>')
