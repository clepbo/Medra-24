#!/usr/bin/env python3
"""Medra Member app, batch 2 — component vocabulary for Visits, Records, Medicines,
Profile & Settings, Notifications and the system states.

House rules that this file obeys everywhere (they are the ones that bit us in Figma):
  · never `wrap="wrap"` — the CLI ignores it; chunk with rows_of()
  · never `items="stretch"` — the CLI rejects it, so nothing relies on a stretched child
    (the records timeline uses a date gutter + connector instead of a stretched rail, and the
     video call places its self-view with justify/align rather than absolute positioning)
  · numeric props always keep their braces — doubled inside f-strings
"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from member_kit import *

INK = "#0A1622"; DIM = "#8FB3CA"

def hr(c="var:border/subtle"):
    return f'<Rect w="fill" h={{1}} bg="{c}" />'

def vspace(h):
    return f'<Frame h={{{h}}} />'

# ---------------------------------------------------------------- tabs
def tabs(options, sel=0, name="Tab", size=15):
    """Underlined editorial tabs — used for Upcoming/Past and the record filters."""
    out = ""
    for i, o in enumerate(options):
        on = i == sel
        bar = ('<Rect w="fill" h={3} rounded={999} bg="var:brand/teal" />' if on
               else '<Rect w="fill" h={3} rounded={999} bg="var:border/subtle" />')
        out += (f'<Frame name="Btn {name} {o}" grow={{1}} flex="col" gap={{9}} items="center">'
                f'{T(size,"semibold" if on else "medium","var:text/strong" if on else "var:text/muted",o)}'
                f'{bar}</Frame>')
    return f'<Frame w="fill" flex="row" gap={{18}}>{out}</Frame>'

# ---------------------------------------------------------------- status pills
PILL = {
  "confirmed": ("circle-check", "Confirmed",  "var:state/success-bg", "var:state/success", OK_IC),
  "soon":      ("clock",        "In 2 days",  "var:state/info-bg",    "var:state/info",    A_IC),
  "today":     ("clock",        "Today",      "var:state/success-bg", "var:state/success", OK_IC),
  "completed": ("check-check",  "Completed",  "var:bg/muted",         "var:text/default",  N_IC),
  "cancelled": ("circle-x",     "Cancelled",  "var:state/error-bg",   "var:state/error",   ERR_IC),
  "missed":    ("circle-slash", "Missed",     "var:state/warning-bg", "var:state/warning", WARN_IC),
  "pending":   ("hourglass",    "Pending",    "var:state/warning-bg", "var:state/warning", WARN_IC),
  "live":      ("video",        "Live now",   "var:state/error-bg",   "var:state/error",   ERR_IC),
  "shared":    ("share-2",      "Shared",     "var:state/info-bg",    "var:state/info",    A_IC),
  "new":       ("sparkles",     "New",        "var:state/info-bg",    "var:state/info",    A_IC),
}
def status_pill(kind, text=None, size=11):
    ic, label, bg, fg, hexc = PILL[kind]
    return (f'<Frame flex="row" gap={{6}} items="center" px={{11}} py={{6}} rounded={{999}} bg="{bg}">'
            f'{I(ic,12,hexc)}{T(size,"semibold",fg,text or label)}</Frame>')

# ---------------------------------------------------------------- small buttons
def mini_btn(label, name, icon=None, kind="ghost", grow=True, full=False):
    # `grow` only makes sense inside a row — in a column it stretches the button vertically,
    # which is what happened to the in-call quick actions. Use full=True in columns.
    g = ' w="fill"' if full else (' grow={1}' if grow else '')
    if kind == "teal":
        st = 'image="assets/img/btn-teal.jpg" overflow="hidden"'; col = "var:text/on-dark"; ic = W_IC
    elif kind == "navy":
        st = 'image="assets/img/btn-navy.jpg" overflow="hidden"'; col = "var:text/on-dark"; ic = W_IC
    elif kind == "danger":
        st = 'bg="var:state/error-bg"'; col = "var:state/error"; ic = ERR_IC
    elif kind == "dark":
        st = 'bg="var:bg/band-2"'; col = "var:text/on-dark"; ic = W_IC
    elif kind == "onpanel":          # readable on top of a var:bg/band-2 panel
        st = 'bg="#1C4066" stroke="#27567F" strokeWidth={1}'; col = "var:text/on-dark"; ic = T_IC
    else:
        st = 'bg="var:bg/base" stroke="var:border/default" strokeWidth={1}'; col = "var:text/default"; ic = N_IC
    return (f'<Frame name="Btn {name}"{g} flex="row" gap={{7}} justify="center" items="center" '
            f'px={{14}} py={{10}} rounded={{999}} {st}>'
            f'{I(icon,14,ic) if icon else ""}{T(13,"semibold",col,label)}</Frame>')

def fab(label, name, icon="plus"):
    return (f'<Frame name="Btn {name}" flex="row" gap={{9}} items="center" px={{18}} py={{14}} rounded={{999}} '
            f'image="assets/img/btn-teal.jpg" overflow="hidden">{I(icon,17,W_IC)}'
            f'{T(14,"semibold","var:text/on-dark",label)}</Frame>')

# ---------------------------------------------------------------- visits
def visit_card(avatar, doctor, spec, place, when, vtype, kind, actions, name, reason=None, dim=False):
    """One appointment. `actions` is a list of (label, icon, kind, btn-name)."""
    tint = "var:state/info-bg" if vtype == "Virtual" else "var:bg/muted"
    tic = "video" if vtype == "Virtual" else "hospital"
    # two actions per row: three "Join / Reschedule / Cancel" buttons in one 390px row
    # wrapped the labels mid-word in Figma, so chunk them.
    acts = rows_of([mini_btn(l, n, i, k) for l, i, k, n in actions], 2, 9)
    rsn = (f'{hr()}<Frame w="fill" flex="row" gap={{9}} items="start">{I("file-text",14,M_IC)}'
           f'{T(12,"regular","var:text/muted",reason,w="fill")}</Frame>') if reason else ''
    name_col = "var:text/faint" if dim else "var:text/strong"
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{13}} p={{18}} rounded={{24}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{status_pill(kind)}'
            f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{6}} rounded={{999}} bg="{tint}">'
            f'{I(tic,12,A_IC)}{T(11,"medium","var:text/default",vtype)}</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Image image="assets/img/{avatar}" w={{54}} h={{54}} rounded={{18}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>{T(16,"semibold",name_col,doctor)}'
            f'{T(13,"regular","var:text/muted",spec,w="fill")}'
            f'<Frame flex="row" gap={{6}} items="center">{I("map-pin",12,M_IC)}'
            f'{T(12,"regular","var:text/muted",place,w="fill")}</Frame></Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{14}} py={{12}} rounded={{16}} bg="var:neutral/50">'
            f'{I("calendar-days",15,A_IC)}{T(13,"semibold","var:text/default",when,w="fill")}</Frame>'
            f'{rsn}'
            f'{acts}</Frame>')

def prep_step(n, title, body, done=False):
    mark = (f'<Frame w={{26}} h={{26}} rounded={{999}} bg="var:brand/teal" flex="col" justify="center" items="center">'
            f'{I("check",14,W_IC)}</Frame>' if done else
            f'<Frame w={{26}} h={{26}} rounded={{999}} bg="var:bg/muted" flex="col" justify="center" items="center">'
            f'{T(12,"bold","var:text/default",str(n))}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{12}} items="start">{mark}'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",title)}'
            f'{T(12,"regular","var:text/muted",body,w="fill")}</Frame></Frame>')

# ---------------------------------------------------------------- virtual visit
def call_plate(doctor, spec, timer="12:04", secure=True):
    sec = (f'<Frame flex="row" gap={{6}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:bg/band-2">'
           f'{I("lock",12,T_IC)}{T(11,"medium","var:text/on-dark","Encrypted")}</Frame>') if secure else ''
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{18}} py={{14}}>'
            f'<Frame flex="row" gap={{11}} items="center" px={{12}} py={{9}} rounded={{999}} bg="var:bg/band-2">'
            f'<Ellipse w={{8}} h={{8}} bg="#2FA36B" />'
            f'<Frame flex="col" gap={{1}}>{T(13,"semibold","var:text/on-dark",doctor)}'
            f'{T(10,"regular","var:text/on-dark-muted",spec)}</Frame></Frame>'
            f'<Frame flex="row" gap={{8}} items="center">{sec}'
            f'<Frame flex="row" gap={{7}} items="center" px={{12}} py={{8}} rounded={{999}} bg="var:bg/band-2">'
            f'{I("timer",13,T_IC)}{T(12,"semibold","var:text/on-dark",timer)}</Frame></Frame></Frame>')

def call_pip(label="You", w=104, h=138):
    return (f'<Frame w={{{w}}} h={{{h}}} rounded={{18}} image="assets/img/call-self.jpg" overflow="hidden" '
            f'flex="col" justify="end" p={{7}}>'
            f'<Frame flex="row" gap={{5}} items="center" px={{8}} py={{4}} rounded={{999}} bg="var:bg/band-2">'
            f'{I("mic",10,W_IC)}{T(10,"medium","var:text/on-dark",label)}</Frame></Frame>')

def call_btn(icon, name, kind="dark", size=56, label=None):
    if kind == "end":
        bg = 'bg="#D14343"'; ic = W_IC
    elif kind == "on":
        bg = 'bg="var:bg/base"'; ic = N_IC
    elif kind == "off":
        bg = 'bg="#3E4C59"'; ic = W_IC
    else:
        bg = 'bg="var:bg/band-2"'; ic = W_IC
    btn = (f'<Frame w={{{size}}} h={{{size}}} rounded={{999}} {bg} flex="col" justify="center" items="center">'
           f'{I(icon,int(size*0.40),ic)}</Frame>')
    cap = T(10, "medium", "var:text/on-dark-muted", label) if label else ""
    return (f'<Frame name="Btn {name}" flex="col" gap={{7}} items="center">{btn}{cap}</Frame>')

def call_controls(items, gap=14):
    cells = "".join(call_btn(*a) for a in items)
    return (f'<Frame w="fill" flex="row" gap={{{gap}}} justify="center" items="center" px={{16}} py={{18}}>'
            f'{cells}</Frame>')

def check_line(label, state="ok", detail=None):
    ic, col, hexc = {"ok": ("circle-check", "var:state/success", OK_IC),
                     "warn": ("triangle-alert", "var:state/warning", WARN_IC),
                     "bad": ("circle-x", "var:state/error", ERR_IC),
                     "wait": ("loader", "var:text/muted", M_IC)}[state]
    sub = T(11, "regular", "var:text/on-dark-muted", detail) if detail else ""
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center">{I(ic,17,hexc)}'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"medium","var:text/on-dark",label)}{sub}</Frame></Frame>')

def level_meter(bars=7, active=4):
    out = ""
    for i in range(bars):
        h = 8 + i * 4
        out += f'<Rect w={{6}} h={{{h}}} rounded={{3}} bg="{"#39B0CF" if i < active else "#3E4C59"}" />'
    return f'<Frame flex="row" gap={{5}} items="end">{out}</Frame>'

# ---------------------------------------------------------------- records timeline
KIND = {
  "visit":        ("stethoscope",   "Consultation", "var:state/info-bg",    A_IC),
  "lab":          ("flask-conical", "Lab result",   "var:state/info-bg",    A_IC),
  "prescription": ("pill",          "Prescription", "var:state/success-bg", OK_IC),
  "imaging":      ("scan",          "Imaging",      "var:bg/muted",         N_IC),
  "vitals":       ("activity",      "Vitals",       "var:state/warning-bg", WARN_IC),
  "upload":       ("file-plus",     "You uploaded", "var:bg/muted",         N_IC),
  "vaccine":      ("syringe",       "Immunisation", "var:state/success-bg", OK_IC),
}
def tl_item(day, mon, kind, title, meta, name, tag=None, thumb=None, gutter=52):
    ic, label, tint, hexc = KIND[kind]
    tagpill = status_pill(tag) if tag else ''
    th = (f'<Image image="assets/img/{thumb}" w={{46}} h={{46}} rounded={{12}} />') if thumb else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="start">'
            f'<Frame w={{{gutter}}} flex="col" gap={{1}} items="center" pt={{16}}>'
            f'{T(19,"bold","var:text/strong",day)}{T(11,"medium","var:text/muted",mon)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{11}} p={{16}} rounded={{22}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{8}} items="center" px={{10}} py={{6}} rounded={{999}} bg="{tint}">'
            f'{I(ic,13,hexc)}{T(11,"semibold","var:text/default",label)}</Frame>{tagpill}</Frame>'
            f'<Frame w="fill" flex="row" gap={{12}} items="center">'
            f'<Frame grow={{1}} flex="col" gap={{3}}>{T(15,"semibold","var:text/strong",title,w="fill")}'
            f'{T(12,"regular","var:text/muted",meta,w="fill")}</Frame>{th}'
            f'{I("chevron-right",17,M_IC)}</Frame></Frame></Frame>')

def tl_link(gutter=52):
    return (f'<Frame w="fill" flex="row" gap={{12}}><Frame w={{{gutter}}} flex="row" justify="center">'
            f'<Rect w={{2}} h={{16}} rounded={{999}} bg="var:border/default" /></Frame>'
            f'<Frame grow={{1}} /></Frame>')

def tl_month(label, gutter=52):
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" pt={{4}}>'
            f'<Frame w={{{gutter}}} flex="row" justify="center">{I("circle-dot",16,T_IC)}</Frame>'
            f'<Frame grow={{1}} flex="row" gap={{12}} items="center">{eyebrow(label)}'
            f'<Rect grow={{1}} h={{1}} bg="var:border/subtle" /></Frame></Frame>')

def timeline(entries, gutter=52):
    """entries: list of ("month", label) or ("item", kwargs-tuple)."""
    out = []
    for i, e in enumerate(entries):
        if e[0] == "month":
            out.append(tl_month(e[1], gutter))
        else:
            if out and entries[i-1][0] == "item":
                out.append(tl_link(gutter))
            out.append(tl_item(*e[1], gutter=gutter))
    return f'<Frame w="fill" flex="col" gap={{0}}>{"".join(out)}</Frame>'

# ---------------------------------------------------------------- record detail
def kv(label, value, ic=None, w="fill"):
    icn = f'{I(ic,15,M_IC)}' if ic else ''
    return (f'<Frame w="fill" flex="col" gap={{4}}>'
            f'<Frame flex="row" gap={{7}} items="center">{icn}{T(12,"medium","var:text/muted",label)}</Frame>'
            f'{T(15,"regular","var:text/strong",value,w="fill")}</Frame>')

def kv_pair(a, b):
    return f'<Frame w="fill" flex="row" gap={{16}} items="start">{a}{b}</Frame>'

def note_section(title, body, ic="file-text"):
    """A section of somebody's consultation note. Named "Btn Field …" for the same reason a
    note_field is: what a clinician wrote is content, and the prose budget must not count a
    doctor's own words against the screen showing them."""
    return (f'<Frame w="fill" flex="col" gap={{8}}>'
            f'<Frame flex="row" gap={{8}} items="center">{I(ic,15,A_IC)}'
            f'{T(13,"semibold","var:text/default",title)}</Frame>'
            f'<Frame name="Btn Field note {title}" w="fill" flex="col">'
            f'{T(14,"regular","var:text/muted",body,w="fill")}</Frame></Frame>')

def provenance(who, council, when):
    return (f'<Frame w="fill" flex="row" gap={{11}} items="start" p={{14}} rounded={{16}} bg="var:neutral/50">'
            f'{I("shield-check",16,OK_IC)}'
            f'<Frame grow={{1}} flex="col" gap={{2}}>'
            f'{T(12,"semibold","var:text/default","Signed by "+who)}'
            f'{T(11,"regular","var:text/muted",council+" · "+when+" · this note cannot be edited",w="fill")}</Frame></Frame>')

def lab_line(test, value, ref, flag=None):
    fl = ''
    if flag:
        c = {"High": ("var:state/error-bg", "var:state/error"), "Low": ("var:state/warning-bg", "var:state/warning")}[flag]
        fl = (f'<Frame flex="row" px={{9}} py={{4}} rounded={{999}} bg="{c[0]}">'
              f'{T(10,"semibold",c[1],flag)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{10}} items="center" py={{10}}>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"medium","var:text/strong",test)}'
            f'{T(11,"regular","var:text/muted","Normal "+ref)}</Frame>'
            f'{T(15,"bold","var:text/strong",value)}{fl}</Frame>')

def chart(series, h=150, unit=""):
    """series: list of (label, value_text, bar_px, tone) — tone: 'ok' | 'warn' | 'bad'."""
    cols = ""
    for label, val, px, tone in series:
        img = {"ok": "btn-teal.jpg", "warn": "tint-amber.jpg", "bad": "tint-navy.jpg"}[tone]
        cols += (f'<Frame grow={{1}} h={{{h}}} flex="col" gap={{7}} justify="end" items="center">'
                 f'{T(11,"semibold","var:text/default",val)}'
                 f'<Frame w="fill" h={{{px}}} rounded={{10}} image="assets/img/{img}" overflow="hidden" />'
                 f'{T(10,"regular","var:text/muted",label)}</Frame>')
    u = T(11, "regular", "var:text/faint", unit) if unit else ""
    return (f'<Frame w="fill" flex="col" gap={{8}}>'
            f'<Frame w="fill" flex="row" gap={{8}} items="end">{cols}</Frame>{u}</Frame>')

# ---------------------------------------------------------------- sharing & consent
def consent_row(ic, title, desc, name, on=True, locked=False):
    box = (f'<Frame w={{24}} h={{24}} rounded={{8}} bg="var:neutral/200" flex="col" justify="center" items="center">'
           f'{I("lock",13,M_IC)}</Frame>' if locked else
           (f'<Frame w={{24}} h={{24}} rounded={{8}} bg="var:brand/teal" flex="col" justify="center" items="center">'
            f'{I("check",15,W_IC)}</Frame>' if on else
            '<Rect w={24} h={24} rounded={8} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />'))
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{13}} items="start" py={{4}}>{box}'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="var:bg/muted" flex="col" justify="center" items="center">'
            f'{I(ic,16,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",title)}'
            f'{T(12,"regular","var:text/muted",desc,w="fill")}</Frame></Frame>')

def share_row(avatar, who, what, expires, name):
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{12}}>'
            f'<Image image="assets/img/{avatar}" w={{42}} h={{42}} rounded={{14}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",who)}'
            f'{T(12,"regular","var:text/muted",what,w="fill")}'
            f'<Frame flex="row" gap={{6}} items="center">{I("clock",11,WARN_IC)}'
            f'{T(11,"medium","var:state/warning",expires)}</Frame></Frame>'
            f'{mini_btn("Revoke",name,"circle-slash","danger",grow=False)}</Frame>')

def audit_row(who, what, when):
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center" py={{9}}>'
            f'<Frame w={{30}} h={{30}} rounded={{10}} bg="var:neutral/50" flex="col" justify="center" items="center">'
            f'{I("eye",14,M_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"medium","var:text/strong",who)}'
            f'{T(11,"regular","var:text/muted",what,w="fill")}</Frame>'
            f'{T(11,"regular","var:text/faint",when)}</Frame>')

def qr_card(label="Medra ID  MDR-8842-19", sub="Show this at reception"):
    return (f'<Frame w="fill" flex="col" gap={{12}} items="center" p={{20}} rounded={{24}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{120}} h={{120}} rounded={{18}} bg="var:neutral/50" flex="col" justify="center" items="center">'
            f'{I("qr-code",68,N_IC)}</Frame>'
            f'{T(14,"semibold","var:text/strong",label)}{T(12,"regular","var:text/muted",sub)}</Frame>')

# ---------------------------------------------------------------- medicines
def dots_week(pattern, size=11):
    """pattern: 7 chars — y taken, n missed, . not due yet."""
    out = ""
    for ch in pattern:
        if ch == "y":
            out += f'<Ellipse w={{{size}}} h={{{size}}} bg="#2FA36B" />'
        elif ch == "n":
            out += f'<Ellipse w={{{size}}} h={{{size}}} bg="#E0A32E" />'
        else:
            out += f'<Ellipse w={{{size}}} h={{{size}}} bg="#E1E8EE" />'
    return f'<Frame flex="row" gap={{5}} items="center">{out}</Frame>'

def med_card(name, dose, purpose, schedule, refills, adherence, pattern, btn, taken_today=None):
    action = ''
    if taken_today is not None:
        action = (mini_btn("Mark as taken", "Take " + name, "check", "teal", full=True) if not taken_today else
                  f'<Frame grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{10}} '
                  f'rounded={{999}} bg="var:state/success-bg">{I("check-check",14,OK_IC)}'
                  f'{T(13,"semibold","var:state/success","Taken today")}</Frame>')
    return (f'<Frame name="Btn {btn}" w="fill" flex="col" gap={{13}} p={{18}} rounded={{24}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Frame w={{48}} h={{48}} rounded={{16}} bg="var:state/success-bg" flex="col" justify="center" items="center">'
            f'{I("pill",22,OK_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(16,"semibold","var:text/strong",name)}'
            f'{T(12,"regular","var:text/muted",dose+" · "+purpose,w="fill")}</Frame>'
            f'{I("chevron-right",18,M_IC)}</Frame>'
            f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{13}} py={{11}} rounded={{16}} bg="var:neutral/50">'
            f'{I("clock",14,A_IC)}{T(12,"medium","var:text/default",schedule,w="fill")}'
            f'{T(11,"regular","var:text/muted",refills)}</Frame>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="col" gap={{6}}>{T(11,"medium","var:text/muted","Last 7 days")}{dots_week(pattern)}</Frame>'
            f'<Frame flex="col" gap={{2}} items="end">{T(17,"bold","var:text/strong",adherence)}'
            f'{T(10,"regular","var:text/muted","taken on time")}</Frame></Frame>'
            f'{action}</Frame>')

def dose_row(time, name, dose, state="due", name_btn=None):
    """state: taken | due | upcoming | missed"""
    conf = {"taken":   ("check-check", OK_IC, "var:state/success-bg", "Taken 08:04"),
            "due":     ("clock",       A_IC,  "var:state/info-bg",    "Due now"),
            "upcoming":("clock",       M_IC,  "var:neutral/50",       "Later today"),
            "missed":  ("circle-alert",WARN_IC,"var:state/warning-bg","Missed")}[state]
    right = (mini_btn("Take", name_btn or ("Take " + name), "check", "teal", grow=False)
             if state in ("due", "missed") else
             f'<Frame flex="row" gap={{6}} items="center">{I(conf[0],14,conf[1])}'
             f'{T(11,"semibold","var:text/muted",conf[3])}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{13}} rounded={{18}} bg="{conf[2]}">'
            f'<Frame flex="col" gap={{1}} items="center" w={{46}}>{T(14,"bold","var:text/strong",time)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"semibold","var:text/strong",name)}'
            f'{T(11,"regular","var:text/muted",dose)}</Frame>{right}</Frame>')

def adherence_grid(days=14, missed=(4, 9)):
    cells = []
    for i in range(days):
        c = "#E0A32E" if i in missed else "#2FA36B"
        cells.append(f'<Frame grow={{1}} h={{34}} rounded={{9}} bg="{c}" />')
    return rows_of(cells, 7, 6)

# ---------------------------------------------------------------- settings / lists
def list_row(ic, label, value=None, name=None, sub=None, chevron=True, danger=False, right=None, tint=None):
    col = "var:state/error" if danger else "var:text/strong"
    hexc = ERR_IC if danger else A_IC
    bg = tint or ("var:state/error-bg" if danger else "var:bg/muted")
    tail = right if right is not None else (
        f'<Frame flex="row" gap={{9}} items="center">'
        f'{T(13,"regular","var:text/muted",value) if value else ""}'
        f'{I("chevron-right",17,M_IC) if chevron else ""}</Frame>')
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame name="Btn {name or label}" w="fill" flex="row" gap={{13}} items="center" py={{13}}>'
            f'<Frame w={{36}} h={{36}} rounded={{12}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,17,hexc)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"medium",col,label)}{s}</Frame>{tail}</Frame>')

def toggle_row(ic, label, sub=None, on=True, name=None):
    sw = (f'<Frame name="Btn {name or label}" w={{50}} h={{29}} rounded={{999}} image="assets/img/btn-teal.jpg" '
          f'overflow="hidden" flex="row" justify="end" items="center" px={{4}}><Ellipse w={{21}} h={{21}} bg="#FFFFFF" /></Frame>'
          if on else
          f'<Frame name="Btn {name or label}" w={{50}} h={{29}} rounded={{999}} bg="var:neutral/300" '
          f'flex="row" justify="start" items="center" px={{4}}><Ellipse w={{21}} h={{21}} bg="#FFFFFF" /></Frame>')
    return list_row(ic, label, sub=sub, name=(name or label) + " row", chevron=False, right=sw)

def radio_row(label, sub=None, on=False, name=None):
    dot = (f'<Frame w={{24}} h={{24}} rounded={{999}} bg="var:brand/teal" flex="col" justify="center" items="center">'
           f'<Ellipse w={{9}} h={{9}} bg="#FFFFFF" /></Frame>' if on else
           '<Rect w={24} h={24} rounded={999} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />')
    s = T(12, "regular", "var:text/muted", sub, w="fill") if sub else ""
    return (f'<Frame name="Btn {name or label}" w="fill" flex="row" gap={{13}} items="center" py={{12}}>{dot}'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"medium","var:text/strong",label)}{s}</Frame></Frame>')

def tile(ic, label, sub, name, tint="var:bg/muted"):
    """Compact two-up destination tile — the mobile profile hub uses these instead of a long
    list of rows, which keeps every destination on one screen."""
    return (f'<Frame name="Btn {name}" grow={{1}} flex="col" gap={{9}} p={{15}} rounded={{20}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{38}} h={{38}} rounded={{13}} bg="{tint}" flex="col" justify="center" items="center">'
            f'{I(ic,18,A_IC)}</Frame>'
            f'<Frame w="fill" flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",label,w="fill")}'
            f'{T(11,"regular","var:text/muted",sub,w="fill")}</Frame></Frame>')

def group_card(title, rows, footer=None, p=18):
    body = hr().join(rows) if isinstance(rows, list) else rows
    ft = (f'{hr()}<Frame name="Group footer" w="fill" flex="row" gap={{9}} items="start" pt={{4}}>'
          f'{I("info",14,M_IC)}'
          f'{T(11,"regular","var:text/muted",footer,w="fill")}</Frame>') if footer else ''
    head = f'{eyebrow(title)}' if title else ''
    return (f'<Frame w="fill" flex="col" gap={{6}} p={{{p}}} rounded={{24}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{head}{body}{ft}</Frame>')

def device_row(ic, device, meta, name, current=False):
    tail = (f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:state/success-bg">'
            f'{I("check",12,OK_IC)}{T(11,"semibold","var:state/success","This device")}</Frame>' if current
            else mini_btn("Sign out", name, "log-out", "ghost", grow=False))
    return list_row(ic, device, sub=meta, name=name + " row", chevron=False, right=tail)

def dependant_row(avatar, who, meta, name):
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{12}}>'
            f'<Image image="assets/img/{avatar}" w={{44}} h={{44}} rounded={{999}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",who)}'
            f'{T(12,"regular","var:text/muted",meta,w="fill")}</Frame>'
            f'{mini_btn("Book","Book for "+name,"calendar-plus","ghost",grow=False)}'
            f'{mini_btn("Manage","Manage "+name,None,"ghost",grow=False)}</Frame>')

# ---------------------------------------------------------------- notifications
def notif_row(ic, title, body, when, name, unread=False, tone="info"):
    bg = {"info": "var:state/info-bg", "ok": "var:state/success-bg",
          "warn": "var:state/warning-bg", "muted": "var:bg/muted"}[tone]
    hexc = {"info": A_IC, "ok": OK_IC, "warn": WARN_IC, "muted": N_IC}[tone]
    dot = '<Ellipse w={8} h={8} bg="#39B0CF" />' if unread else '<Frame w={8} />'
    card_bg = "var:bg/base" if unread else "var:neutral/50"
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{12}} items="start" p={{15}} rounded={{20}} '
            f'bg="{card_bg}" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{38}} h={{38}} rounded={{13}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,18,hexc)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(14,"semibold","var:text/strong",title)}{dot}</Frame>'
            f'{T(12,"regular","var:text/muted",body,w="fill")}'
            f'{T(11,"regular","var:text/faint",when)}</Frame></Frame>')

# ---------------------------------------------------------------- states
def empty_state(ic, title, body, primary=None, secondary=None, tone="info", pad=26):
    bg = {"info": "var:state/info-bg", "ok": "var:state/success-bg", "warn": "var:state/warning-bg"}[tone]
    hexc = {"info": A_IC, "ok": OK_IC, "warn": WARN_IC}[tone]
    acts = ""
    if primary: acts += primary
    if secondary: acts += secondary
    return (f'<Frame w="fill" flex="col" gap={{14}} items="center" p={{{pad}}} rounded={{26}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{80}} h={{80}} rounded={{999}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,36,hexc)}</Frame>'
            f'{T(19,"bold","var:text/strong",title)}'
            f'{T(14,"regular","var:text/muted",body,w="fill",align="center")}{acts}</Frame>')

def skel(w="fill", h=16, r=8, grow=None):
    g = f' grow={{{grow}}}' if grow else ''
    ww = f' w="{w}"' if isinstance(w, str) else f' w={{{w}}}'
    return f'<Rect{ww}{g} h={{{h}}} rounded={{{r}}} bg="var:neutral/200" />'

def skel_card(lines=3, p=18, avatar=True):
    av = '<Rect w={54} h={54} rounded={18} bg="var:neutral/200" />' if avatar else ''
    body = "".join(skel(h=13, w="fill") for _ in range(lines))
    return (f'<Frame w="fill" flex="row" gap={{13}} items="start" p={{{p}}} rounded={{24}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{av}'
            f'<Frame grow={{1}} flex="col" gap={{9}}>{body}</Frame></Frame>')

def banner(img, eyebrow_t, head, sub, actions="", h=None, r=28):
    hh = f' h={{{h}}}' if h else ''
    return (f'<Frame w="fill"{hh} flex="row" justify="between" items="center" gap={{24}} p={{28}} rounded={{{r}}} '
            f'image="assets/img/{img}" overflow="hidden">'
            f'<Frame grow={{1}} flex="col" gap={{9}}>'
            f'{eyebrow(eyebrow_t,"var:brand/teal")}'
            f'{T(28,"bold","var:text/on-dark",head)}'
            f'{T(15,"regular","var:text/on-dark-muted",sub,w="fill")}</Frame>'
            f'<Frame flex="row" gap={{11}} items="center">{actions}</Frame></Frame>')

def light_banner(img, eyebrow_t, head, sub, actions=""):
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{24}} p={{26}} rounded={{28}} '
            f'image="assets/img/{img}" overflow="hidden">'
            f'<Frame grow={{1}} flex="col" gap={{8}}>{eyebrow(eyebrow_t)}'
            f'{T(26,"bold","var:text/strong",head)}'
            f'{T(15,"regular","var:text/muted",sub,w="fill")}</Frame>'
            f'<Frame flex="row" gap={{11}} items="center">{actions}</Frame></Frame>')

def sheet_wrap(title, body, actions, close="Btn Close sheet"):
    return (f'<Frame grow={{1}} w="fill" flex="col" justify="end">'
            f'<Frame w="fill" flex="col" gap={{16}} px={{22}} pt={{14}} pb={{24}} rounded={{32}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="center"><Rect w={{44}} h={{5}} rounded={{999}} bg="var:neutral/300" /></Frame>'
            f'<Frame w="fill" flex="row" justify="between" items="center">{T(19,"bold","var:text/strong",title)}'
            f'<Frame name="{close}" flex="row">{I("x",21,N_IC)}</Frame></Frame>'
            f'{body}{actions}</Frame></Frame>')

def mob_sub(text):
    """A one-line subtitle sitting under the mobile appbar."""
    return f'<Frame w="fill" px={{20}} pb={{2}}>{T(13,"regular","var:text/muted",text,w="fill")}</Frame>'


# =====================================================================================
# HUB → SECTION → SHEET  (mobile only)
#
# The doctor module proved the pattern out and the product owner asked for it here too.
# A phone screen becomes:
#   hub      what the screen is about, the one thing you act on, and a short list of ways in
#   section  one subject per screen, reached by tapping a row on the hub
#   sheet    one decision, over a dimmed hub — the "dialogue" case
#
# These use the member chrome (light appbar, five-tab bottom nav), not the doctor's, so the
# two apps stay visually distinct while behaving the same way.
# =====================================================================================

def m_sec_row(ic, label, summary, name, value=None, tint=None):
    """A way into a section. Carries a count so the hub still describes the screen without
    unrolling it."""
    return list_row(ic, label, value=value, name=name, sub=summary, tint=tint)


def m_hub_list(rows, title="More on this screen"):
    return group_card(title, rows, p=16)


def m_sheet(name, title, sub, body, actions=None, peek=None):
    """A bottom sheet over a dimmed screen. The DSL has no opacity, so the dim is painted
    rather than composited — in build it is the screen behind at 55% black.
    Tapping the scrim closes it, the same as the X."""
    top = (f'<Frame name="Btn Close sheet" w="fill" grow={{1}} flex="col" bg="#2A3948" '
           f'overflow="hidden">{peek or ""}</Frame>')
    acts = (f'<Frame w="fill" flex="col" gap={{10}} pt={{4}}>{actions}</Frame>') if actions else ''
    card_ = (f'<Frame w="fill" flex="col" gap={{15}} px={{20}} pt={{12}} pb={{24}} rounded={{30}} '
             f'bg="var:bg/base">'
             f'<Frame w="fill" flex="row" justify="center"><Rect w={{42}} h={{4}} rounded={{999}} '
             f'bg="var:neutral/300" /></Frame>'
             f'<Frame w="fill" flex="row" justify="between" items="start" gap={{12}}>'
             f'<Frame grow={{1}} flex="col" gap={{3}}>{T(19,"bold","var:text/strong",title)}'
             + (T(13, "regular", "var:text/muted", sub, w="fill") if sub else '')
             + f'</Frame><Frame name="Btn Close sheet" w={{34}} h={{34}} rounded={{999}} '
             f'bg="var:bg/muted" flex="col" justify="center" items="center">{I("x",17,N_IC)}</Frame></Frame>'
             f'{body}{acts}</Frame>')
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" bg="#2A3948" overflow="hidden">'
            f'{top}{card_}</Frame>')


def m_sheet_pick(ic, label, sub, name, tint=None):
    """A row inside a sheet. Bigger tap target than a list row — a sheet is a decision."""
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{14}} items="center" p={{14}} '
            f'rounded={{18}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{40}} h={{40}} rounded={{14}} bg="{tint or "var:bg/muted"}" flex="col" '
            f'justify="center" items="center">{I(ic,19,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",label)}'
            + (T(11, "regular", "var:text/muted", sub, w="fill") if sub else '')
            + f'</Frame>{I("chevron-right",16,M_IC)}</Frame>')


# The strip of the screen that stays visible behind a sheet.
M_SHEET_PEEK = (f'{statusbar(dark=True)}'
                f'<Frame w="fill" flex="col" gap={{12}} px={{26}} pt={{20}}>'
                f'<Frame w="fill" h={{86}} rounded={{26}} bg="#22303E" />'
                f'<Frame w="fill" flex="row" gap={{10}}>'
                f'<Frame grow={{1}} h={{58}} rounded={{18}} bg="#22303E" />'
                f'<Frame grow={{1}} h={{58}} rounded={{18}} bg="#22303E" /></Frame>'
                f'<Frame w="fill" h={{80}} rounded={{20}} bg="#22303E" /></Frame>')
