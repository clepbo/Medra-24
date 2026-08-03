#!/usr/bin/env python3
"""Medra — Doctor app chrome and clinical components.

Same "Soft Clinical" language as the member app, with two deliberate differences:
  · the primary action colour is **navy**, not teal — the doctor app is a work tool used all
    day, and the teal is reserved for the member-facing product
  · density is higher: a doctor scanning a queue between patients needs more on screen than a
    member booking once a month

House rules carried over: no wrap="wrap", no items="stretch", grow is a row property,
mobile content fits 390x844.
"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from member_kit import (stat_card, date_strip, slot_grid, summary_row, section_head)
from member2_kit import (hr, tabs, status_pill, mini_btn, prep_step, list_row, toggle_row,
                         radio_row, group_card, consent_row, audit_row, notif_row, empty_state,
                         skel, skel_card, banner, light_banner, kv, kv_pair, note_section,
                         provenance, lab_line, chart, tile, dots_week, adherence_grid,
                         dose_row, med_card, timeline, tl_item, share_row, qr_card, PILL)

DIM = "#8FB3CA"

# ---------------------------------------------------------------- shells
DR_NAV = [("layout-dashboard", "Today", "Nav Today"),
          ("calendar-days", "Schedule", "Nav Schedule"),
          ("users", "Patients", "Nav Patients"),
          ("notebook-pen", "Notes", "Nav Notes"),
          ("banknote", "Earnings", "Nav Earnings"),
          ("settings", "Settings", "Nav Settings")]

def dr_desk(name, children, active=0, topbar=True, search_ph="Search a patient by name, phone or Medra ID"):
    navs = ""
    for i, (ic, label, nm) in enumerate(DR_NAV):
        on = i == active
        if on:
            navs += (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{12}} items="center" px={{14}} py={{13}} '
                     f'rounded={{16}} bg="var:bg/base">{I(ic,19,A_IC)}'
                     f'{T(14,"semibold","var:text/strong",label,w="fill")}'
                     f'<Rect w={{5}} h={{5}} rounded={{999}} bg="var:brand/teal" /></Frame>')
        else:
            navs += (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{12}} items="center" px={{14}} py={{13}} '
                     f'rounded={{16}}>{I(ic,19,"#8FB3CA")}'
                     f'{T(14,"regular","var:text/on-dark-muted",label,w="fill")}</Frame>')
    side = (f'<Frame w={{262}} h="fill" flex="col" gap={{22}} p={{20}} image="assets/img/sidebar.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="row" gap={{11}} items="center" pt={{6}} pb={{2}}>'
            f'<Image image="assets/logo/logo-white.png" w={{86}} h={{64}} />'
            f'<Frame flex="row" px={{9}} py={{4}} rounded={{999}} bg="var:bg/band-2">'
            f'{T(10,"semibold","var:brand/teal","DOCTOR")}</Frame></Frame>'
            f'<Frame w="fill" flex="col" gap={{5}}>{T(11,"semibold","#6E93AE","MENU")}{navs}</Frame>'
            f'<Frame grow={{1}} />'
            f'<Frame w="fill" flex="col" gap={{11}} p={{17}} rounded={{22}} bg="var:bg/band-2">'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(11,"semibold","var:text/on-dark-muted","TAKING BOOKINGS")}'
            f'<Frame name="Btn Toggle availability" w={{44}} h={{25}} rounded={{999}} image="assets/img/btn-teal.jpg" '
            f'overflow="hidden" flex="row" justify="end" items="center" px={{3}}>'
            f'<Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame></Frame>'
            f'{T(11,"regular","var:text/on-dark-muted","Turn this off and your open slots stop being bookable — existing appointments are untouched.",w="fill")}</Frame>'
            f'<Frame name="Btn Nav Settings" w="fill" flex="row" gap={{11}} items="center" p={{11}} rounded={{18}} bg="var:bg/band-2">'
            f'<Image image="assets/img/avatar-4.jpg" w={{38}} h={{38}} rounded={{999}} />'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"semibold","var:text/on-dark","Dr. Ngozi Okafor")}'
            f'{T(11,"regular","var:text/on-dark-muted","Cardiologist")}</Frame>'
            f'{I("chevron-right",16,"#8FB3CA")}</Frame></Frame>')
    top = (f'<Frame w="fill" flex="row" gap={{16}} items="center">'
           f'<Frame name="Btn Search patient" grow={{1}} flex="row" gap={{11}} items="center" px={{18}} py={{15}} '
           f'rounded={{999}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
           f'{I("search",19,M_IC)}{T(15,"regular","var:text/faint",search_ph,w="fill")}'
           f'<Frame flex="row" gap={{6}} items="center" px={{9}} py={{4}} rounded={{8}} bg="var:bg/muted">'
           f'{T(11,"medium","var:text/muted","Medra ID")}</Frame></Frame>'
           f'{circle_btn("bell","Notifications")}'
           f'<Frame name="Btn Start consult" flex="row" gap={{9}} items="center" px={{18}} py={{14}} rounded={{999}} '
           f'image="assets/img/btn-navy.jpg" overflow="hidden">{I("stethoscope",17,W_IC)}'
           f'{T(14,"semibold","var:text/on-dark","Start next consultation")}</Frame></Frame>') if topbar else ''
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="row" image="assets/img/surface-desktop.jpg" '
            f'overflow="hidden">{side}'
            f'<Frame grow={{1}} h="fill" flex="col" gap={{20}} px={{36}} py={{28}}>{top}{children}</Frame></Frame>')

DR_TABS = [("layout-dashboard", "Today", "Nav Today"), ("calendar-days", "Schedule", "Nav Schedule"),
           ("users", "Patients", "Nav Patients"), ("banknote", "Earnings", "Nav Earnings"),
           ("settings", "Settings", "Nav Settings")]

def dr_bottom_nav(active=0):
    cells = ""
    for i, (ic, label, nm) in enumerate(DR_TABS):
        on = i == active
        cells += (f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{4}} items="center">'
                  f'{I(ic,21,T_IC if on else M_IC)}'
                  f'{T(10,"semibold" if on else "regular","var:text/accent" if on else "var:text/muted",label)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{4}} items="center" px={{16}} pt={{12}} pb={{20}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}} rounded={{28}}>{cells}</Frame>')

def dr_mob(name, children, nav=None, bg="surface-mobile.jpg"):
    navrow = f'<Frame w="fill" px={{14}} pb={{10}}>{nav}</Frame>' if nav else ''
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/{bg}" overflow="hidden">'
            f'{statusbar()}{children}{navrow}</Frame>')

def dr_appbar(title=None, back=True, right=None):
    left = (circle_btn("arrow-left", "Back") if back else
            '<Image image="assets/logo/appicon.png" w={38} h={38} rounded={10} />')
    mid = T(17, "semibold", "var:text/strong", title) if title else '<Frame />'
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{20}} pt={{10}} pb={{8}}>'
            f'{left}{mid}{right or circle_btn("bell","Notifications")}</Frame>')

def dr_greet():
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{20}} pt={{10}} pb={{6}}>'
            f'<Frame flex="row" gap={{12}} items="center">'
            f'<Image image="assets/img/avatar-4.jpg" w={{46}} h={{46}} rounded={{999}} />'
            f'<Frame flex="col" gap={{1}}>{T(13,"regular","var:text/muted","Thursday, 14 August")}'
            f'{T(17,"bold","var:text/strong","Dr. Okafor")}</Frame></Frame>'
            f'<Frame flex="row" gap={{9}} items="center">{circle_btn("bell","Notifications")}</Frame></Frame>')

# ---------------------------------------------------------------- doctor CTA (navy)
def dcta(label, name, icon="arrow-right"):
    return cta(label, name, icon, "btn-navy.jpg")

# ---------------------------------------------------------------- queue
def queue_row(time, avatar, who, meta, reason, kind, vtype, name, now=False):
    edge = ('stroke="var:border/accent" strokeWidth={2}' if now
            else 'stroke="var:border/subtle" strokeWidth={1}')
    tic = "video" if vtype == "Virtual" else "hospital"
    action = (mini_btn("Start", "Start " + name, "stethoscope", "navy", grow=False) if now
              else mini_btn("Open", "Open " + name, "chevron-right", "ghost", grow=False))
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{14}} items="center" p={{16}} rounded={{22}} '
            f'bg="var:bg/base" {edge}>'
            f'<Frame w={{58}} flex="col" gap={{2}} items="center">'
            f'{T(15,"bold","var:text/strong",time)}{T(10,"regular","var:text/muted","30 min")}</Frame>'
            f'<Rect w={{1}} h={{44}} bg="var:border/subtle" />'
            f'<Image image="assets/img/{avatar}" w={{44}} h={{44}} rounded={{14}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{9}} items="center">{T(15,"semibold","var:text/strong",who)}'
            f'{status_pill(kind)}</Frame>'
            f'{T(12,"regular","var:text/muted",meta,w="fill")}'
            f'<Frame flex="row" gap={{7}} items="center">{I("file-text",12,M_IC)}'
            f'{T(12,"regular","var:text/muted",reason,w="fill")}</Frame></Frame>'
            f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:bg/muted">'
            f'{I(tic,12,A_IC)}{T(11,"medium","var:text/default",vtype)}</Frame>'
            f'{action}</Frame>')

def now_card(avatar, who, meta, reason, when, name="Now"):
    return (f'<Frame w="fill" flex="col" gap={{15}} p={{22}} rounded={{28}} image="assets/img/btn-navy.jpg" '
            f'overflow="hidden">'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{8}} items="center">{I("circle-dot",15,T_IC)}'
            f'{T(12,"semibold","var:brand/teal","NEXT PATIENT · STARTS IN 6 MINUTES")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{11}} py={{6}} rounded={{999}} bg="var:bg/band-2">'
            f'{I("video",13,T_IC)}{T(11,"medium","var:text/on-dark","Virtual")}</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{14}} items="center">'
            f'<Image image="assets/img/{avatar}" w={{56}} h={{56}} rounded={{18}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>{T(18,"bold","var:text/on-dark",who)}'
            f'{T(13,"regular","var:text/on-dark-muted",meta,w="fill")}</Frame>'
            f'{T(15,"semibold","var:text/on-dark",when)}</Frame>'
            f'<Frame w="fill" flex="row" gap={{9}} items="start" px={{14}} py={{12}} rounded={{16}} bg="var:bg/band-2">'
            f'{I("file-text",15,T_IC)}{T(13,"regular","var:text/on-dark",reason,w="fill")}</Frame>'
            f'<Frame w="fill" flex="row" gap={{10}}>'
            f'<Frame name="Btn Open prep" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{13}} '
            f'rounded={{999}} bg="var:bg/band-2">{I("clipboard-list",15,W_IC)}'
            f'{T(13,"semibold","var:text/on-dark","Read the file first")}</Frame>'
            f'<Frame name="Btn Start consult" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{13}} '
            f'rounded={{999}} bg="var:bg/base">{I("stethoscope",15,N_IC)}'
            f'{T(13,"semibold","var:text/strong","Start consultation")}</Frame></Frame></Frame>')

# ---------------------------------------------------------------- clinical note
def note_field(label, ic, value, name, lines=3, ph=False, helper=None):
    col = "var:text/faint" if ph else "var:text/strong"
    h = 20 + lines * 20
    sub = T(11, "regular", "var:text/muted", helper, w="fill") if helper else ""
    return (f'<Frame w="fill" flex="col" gap={{7}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{8}} items="center">{I(ic,15,A_IC)}'
            f'{T(13,"semibold","var:text/default",label)}</Frame>'
            f'<Frame name="Btn Template {name}" flex="row" gap={{6}} items="center" px={{10}} py={{5}} rounded={{999}} '
            f'bg="var:bg/muted">{I("files",12,M_IC)}{T(11,"medium","var:text/muted","Template")}</Frame></Frame>'
            f'<Frame name="Btn Field {name}" w="fill" minH={{{h}}} flex="col" px={{16}} py={{14}} rounded={{16}} '
            f'bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{T(14,"regular",col,value,w="fill")}</Frame>{sub}</Frame>')

def share_toggle(label, name, on=True):
    sw = (f'<Frame name="Btn {name}" w={{44}} h={{25}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden" '
          f'flex="row" justify="end" items="center" px={{3}}><Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame>' if on else
          f'<Frame name="Btn {name}" w={{44}} h={{25}} rounded={{999}} bg="var:neutral/300" '
          f'flex="row" justify="start" items="center" px={{3}}><Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame>')
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center" py={{9}}>'
            f'{T(13,"medium","var:text/default",label,w="fill")}{sw}</Frame>')

def drug_result(name, form, note_txt, btn):
    return (f'<Frame name="Btn {btn}" w="fill" flex="row" gap={{12}} items="center" p={{13}} rounded={{16}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{36}} h={{36}} rounded={{12}} bg="var:state/success-bg" flex="col" justify="center" items="center">'
            f'{I("pill",17,OK_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",name)}'
            f'{T(11,"regular","var:text/muted",form,w="fill")}</Frame>'
            f'{T(11,"regular","var:text/faint",note_txt)}{I("plus",16,A_IC)}</Frame>')

def rx_line(name, dose, freq, days, btn):
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{12}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="var:state/success-bg" flex="col" justify="center" items="center">'
            f'{I("pill",16,OK_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",name)}'
            f'{T(11,"regular","var:text/muted",dose+" · "+freq+" · "+days,w="fill")}</Frame>'
            f'<Frame name="Btn Edit {btn}" flex="row">{I("pencil",15,M_IC)}</Frame>'
            f'<Frame name="Btn Remove {btn}" flex="row">{I("x",16,ERR_IC)}</Frame></Frame>')

def alert_strip(ic, title, body, tone="warn"):
    bg = {"warn": "var:state/warning-bg", "err": "var:state/error-bg", "ok": "var:state/success-bg",
          "info": "var:state/info-bg"}[tone]
    c = {"warn": WARN_IC, "err": ERR_IC, "ok": OK_IC, "info": A_IC}[tone]
    return (f'<Frame w="fill" flex="row" gap={{11}} items="start" p={{15}} rounded={{18}} bg="{bg}">{I(ic,17,c)}'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",title)}'
            f'{T(12,"regular","var:text/default",body,w="fill")}</Frame></Frame>')

# ---------------------------------------------------------------- patients
def patient_row(avatar, who, mid, meta, last, name, tag=None):
    pill = status_pill(tag) if tag else ''
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{13}} items="center" py={{13}}>'
            f'<Image image="assets/img/{avatar}" w={{44}} h={{44}} rounded={{14}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{9}} items="center">{T(14,"semibold","var:text/strong",who)}{pill}</Frame>'
            f'<Frame flex="row" gap={{9}} items="center">'
            f'<Frame flex="row" gap={{5}} items="center" px={{8}} py={{3}} rounded={{7}} bg="var:bg/muted">'
            f'{T(10,"semibold","var:text/accent",mid)}</Frame>'
            f'{T(11,"regular","var:text/muted",meta,w="fill")}</Frame></Frame>'
            f'<Frame flex="col" gap={{2}} items="end">{T(11,"regular","var:text/muted","Last seen")}'
            f'{T(12,"medium","var:text/default",last)}</Frame>'
            f'{I("chevron-right",17,M_IC)}</Frame>')

def scope_line(label, granted=True, detail=None):
    ic, c = ("circle-check", OK_IC) if granted else ("lock", M_IC)
    sub = T(11, "regular", "var:text/muted", detail, w="fill") if detail else ""
    return (f'<Frame w="fill" flex="row" gap={{11}} items="start" py={{8}}>{I(ic,16,c)}'
            f'<Frame grow={{1}} flex="col" gap={{1}}>'
            f'{T(13,"medium","var:text/strong" if granted else "var:text/faint",label)}{sub}</Frame></Frame>')

# ---------------------------------------------------------------- schedule
def slot_chip(t, state="open", name=None):
    conf = {"open":   ('bg="var:bg/base" stroke="var:border/default" strokeWidth={1}', "var:text/default"),
            "booked": ('image="assets/img/btn-navy.jpg" overflow="hidden"', "var:text/on-dark"),
            "blocked":('bg="var:neutral/100"', "var:text/faint"),
            "break":  ('bg="var:state/warning-bg"', "var:state/warning")}[state]
    return (f'<Frame name="Btn {name or ("Slot "+t)}" grow={{1}} flex="row" justify="center" py={{11}} rounded={{14}} '
            f'{conf[0]}>{T(13,"semibold",conf[1],t)}</Frame>')

def day_col(day, date, items, today=False):
    head = (f'<Frame w="fill" flex="col" gap={{2}} items="center" py={{10}} rounded={{14}} '
            f'{"image=" + chr(34) + "assets/img/btn-teal.jpg" + chr(34) + " overflow=" + chr(34) + "hidden" + chr(34) if today else "bg=" + chr(34) + "var:bg/muted" + chr(34)}>'
            f'{T(11,"medium","var:text/on-dark-muted" if today else "var:text/muted",day)}'
            f'{T(16,"bold","var:text/on-dark" if today else "var:text/strong",date)}</Frame>')
    return (f'<Frame grow={{1}} flex="col" gap={{8}}>{head}{"".join(items)}</Frame>')

def earn_row(label, sub, amount, tone="default"):
    c = {"default": "var:text/strong", "ok": "var:state/success", "muted": "var:text/muted"}[tone]
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{12}}>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"medium","var:text/strong",label)}'
            f'{T(11,"regular","var:text/muted",sub,w="fill")}</Frame>'
            f'{T(15,"bold",c,amount)}</Frame>')

def queue_row_m(time, avatar, who, meta, reason, kind, vtype, name, now=False):
    """Compact queue row for 390 — the desktop row wraps badly at this width."""
    edge = ('stroke="var:border/accent" strokeWidth={2}' if now
            else 'stroke="var:border/subtle" strokeWidth={1}')
    tic = "video" if vtype == "Virtual" else "hospital"
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{10}} p={{14}} rounded={{20}} '
            f'bg="var:bg/base" {edge}>'
            f'<Frame w="fill" flex="row" gap={{11}} items="center">'
            f'<Image image="assets/img/{avatar}" w={{40}} h={{40}} rounded={{13}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",who)}'
            f'{T(11,"regular","var:text/muted",meta,w="fill")}</Frame>'
            f'<Frame flex="col" gap={{2}} items="end">{T(14,"bold","var:text/strong",time)}'
            f'<Frame flex="row" gap={{5}} items="center">{I(tic,11,A_IC)}'
            f'{T(10,"medium","var:text/muted",vtype)}</Frame></Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{11}} py={{9}} rounded={{13}} bg="var:neutral/50">'
            f'{I("file-text",12,M_IC)}{T(11,"regular","var:text/muted",reason,w="fill")}</Frame></Frame>')

def patient_strip_m(timer="12:04"):
    return (f'<Frame w="fill" flex="row" gap={{11}} items="center" p={{13}} rounded={{18}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Image image="assets/img/avatar-2.jpg" w={{38}} h={{38}} rounded={{13}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Amara Okeke")}'
            f'{T(10,"regular","var:text/muted","MDR-8842-19 · penicillin allergy",w="fill")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:state/error-bg">'
            f'<Ellipse w={{7}} h={{7}} bg="#D14343" />{T(11,"semibold","var:state/error",timer)}</Frame></Frame>')

def head_stats_m(cells):
    """Two-up stat cells — four across 390 wraps every label."""
    return rows_of(cells, 2, 10)
