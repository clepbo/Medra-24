#!/usr/bin/env python3
"""Medra Member app — shared chrome and cards.

The chrome and cards the member app shares across every page: the bottom nav, the dashboard
sidebar, the doctor card, the slot grid. Kept out of build_member.py so the builder reads as
screens rather than plumbing. Import after medra_ui — `desk()` here deliberately shadows the
auth `desk()`.
"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from shell import app_desk, title_from, NAV_MEMBER

# ---------------------------------------------------------------- member-specific parts
def appbar(title=None, back=True, right=None, dark=False):
    left = (circle_btn("arrow-left","Back") if back else
            '<Image image="assets/logo/appicon.png" w={38} h={38} rounded={10} />')
    mid = T(17,"semibold","var:text/strong",title) if title else '<Frame />'
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{20}} pt={{10}} pb={{8}}>'
            f'{left}{mid}{right or circle_btn("bell","Notifications")}</Frame>')

def greet_bar():
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{20}} pt={{10}} pb={{6}}>'
            f'<Frame flex="row" gap={{12}} items="center">'
            f'<Image image="assets/img/me.jpg" w={{46}} h={{46}} rounded={{999}} />'
            f'<Frame flex="col" gap={{1}}>{T(13,"regular","var:text/muted","Good morning")}'
            f'{T(17,"bold","var:text/strong","Amara")}</Frame></Frame>'
            f'<Frame flex="row" gap={{9}} items="center">{circle_btn("bell","Notifications")}</Frame></Frame>')

def searchbar(placeholder="Search doctors, clinics or symptoms", name="Search"):
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="center" px={{18}} py={{15}} rounded={{999}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>{I("search",19,T_IC)}'
            f'{T(15,"regular","var:text/faint",placeholder,w="fill")}'
            f'<Frame name="Btn Filters" flex="row">{I("sliders-horizontal",19,N_IC)}</Frame></Frame>')

def next_visit_card(compact=False):
    return (f'<Frame name="Btn Upcoming visit" w="fill" flex="col" gap={{14}} p={{20}} rounded={{26}} '
            f'image="assets/img/btn-navy.jpg" overflow="hidden">'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="row" gap={{8}} items="center">{I("calendar-check",15,T_IC)}'
            f'{T(12,"semibold","var:brand/teal","NEXT VISIT · IN 2 DAYS")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{11}} py={{6}} rounded={{999}} bg="var:bg/band-2">'
            f'{I("video",13,T_IC)}{T(11,"medium","var:text/on-dark","Virtual")}</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Image image="assets/img/avatar-4.jpg" w={{52}} h={{52}} rounded={{999}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(17,"bold","var:text/on-dark","Dr. Ngozi Okafor")}'
            f'{T(13,"regular","var:text/on-dark-muted","Cardiologist · Garki Medical Centre")}</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{8}} items="center" px={{14}} py={{11}} rounded={{16}} bg="var:bg/band-2">'
            f'{I("clock",15,T_IC)}{T(13,"medium","var:text/on-dark","Tue, 12 Aug · 10:30 AM",w="fill")}</Frame>'
            f'<Frame w="fill" flex="row" gap={{10}}>'
            f'<Frame name="Btn Reschedule" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{12}} rounded={{999}} bg="var:bg/band-2">'
            f'{I("calendar-days",15,W_IC)}{T(13,"semibold","var:text/on-dark","Reschedule")}</Frame>'
            f'<Frame name="Btn Join visit" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{12}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden">'
            f'{I("video",15,W_IC)}{T(13,"semibold","var:text/on-dark","Join")}</Frame></Frame></Frame>')

SPECIALTIES=[("heart-pulse","Cardiology"),("brain","Neurology"),("baby","Paediatrics"),
             ("stethoscope","General"),("bone","Orthopaedics"),("syringe","Vaccines")]
def specialty_row(limit=6, per_row=3):
    cells=[]
    for ic,label in SPECIALTIES[:limit]:
        cells.append(f'<Frame name="Btn Specialty {label}" grow={{1}} flex="col" gap={{8}} items="center" py={{14}} px={{6}} rounded={{20}} '
                f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
                f'<Frame w={{42}} h={{42}} rounded={{14}} bg="var:bg/muted" flex="col" justify="center" items="center">{I(ic,20,A_IC)}</Frame>'
                f'{T(12,"medium","var:text/default",label)}</Frame>')
    return rows_of(cells, per_row, 10)

def section_head(title, action="See all", name="See all"):
    return (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(17,"bold","var:text/strong",title)}'
            f'<Frame name="Btn {name}" flex="row" gap={{5}} items="center">{T(13,"semibold","var:text/accent",action)}'
            f'{I("chevron-right",15,T_IC)}</Frame></Frame>')

def doctor_card(avatar, name, spec, clinic, fee, rating, slot, tag="Today", nm=None, verified=True):
    vb=I("badge-check",16,T_IC) if verified else ""
    return (f'<Frame name="Btn {nm or ("Doctor "+name)}" w="fill" flex="col" gap={{13}} p={{16}} rounded={{24}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{13}} items="center">'
            f'<Image image="assets/img/{avatar}" w={{58}} h={{58}} rounded={{20}} />'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{7}} items="center">{T(16,"semibold","var:text/strong",name)}{vb}</Frame>'
            f'{T(13,"regular","var:text/muted",spec+" · "+clinic,w="fill")}'
            f'<Frame flex="row" gap={{12}} items="center">'
            f'<Frame flex="row" gap={{4}} items="center">{I("star",13,"#E0A32E")}{T(12,"semibold","var:text/default",rating)}</Frame>'
            f'<Frame flex="row" gap={{4}} items="center">{I("map-pin",13,M_IC)}{T(12,"regular","var:text/muted","2.4 km")}</Frame>'
            f'</Frame></Frame>'
            f'<Frame flex="col" gap={{3}} items="end">{T(15,"bold","var:text/strong",fee)}'
            f'{T(11,"regular","var:text/muted","per visit")}</Frame></Frame>'
            f'<Frame w="fill" flex="row" gap={{8}} items="center">'
            f'<Frame flex="row" gap={{6}} items="center" px={{11}} py={{7}} rounded={{999}} bg="var:state/success-bg">'
            f'{I("clock",12,OK_IC)}{T(11,"semibold","var:state/success",tag+" · "+slot)}</Frame>'
            f'<Frame grow={{1}} />'
            f'<Frame name="Btn Book {name}" flex="row" gap={{7}} items="center" px={{16}} py={{9}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden">'
            f'{T(13,"semibold","var:text/on-dark","Book")}{I("arrow-right",14,W_IC)}</Frame></Frame></Frame>')

def bottom_nav(active=0):
    # Five tabs, matching the desktop sidebar minus "Find care" (which lives in the search bar).
    # Every tab is wired — see link-member.js; nothing here is decorative.
    items=[("house","Home","Nav Home"),("calendar-days","Visits","Nav Visits"),
           ("clipboard-list","Records","Nav Records"),("pill","Medicines","Nav Meds"),
           ("circle-user","Profile","Nav Profile")]
    cells=""
    for i,(ic,label,nm) in enumerate(items):
        on=i==active
        cells+=(f'<Frame name="Btn {nm}" grow={{1}} flex="col" gap={{4}} items="center">'
                f'{I(ic,21,T_IC if on else M_IC)}'
                f'{T(10,"semibold" if on else "regular","var:text/accent" if on else "var:text/muted",label)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{4}} items="center" px={{16}} pt={{12}} pb={{20}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}} rounded={{28}}>{cells}</Frame>')

def date_strip(sel=2):
    days=[("Mon","19"),("Tue","20"),("Wed","21"),("Thu","22"),("Fri","23"),("Sat","24")]
    cells=""
    for i,(d,n) in enumerate(days):
        on=i==sel
        st='image="assets/img/btn-teal.jpg" overflow="hidden"' if on else 'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}'
        cells+=(f'<Frame name="Btn Date {d}{n}" grow={{1}} flex="col" gap={{5}} items="center" py={{13}} rounded={{18}} {st}>'
                f'{T(11,"medium","var:text/on-dark-muted" if on else "var:text/muted",d)}'
                f'{T(17,"bold","var:text/on-dark" if on else "var:text/strong",n)}</Frame>')
    return f'<Frame w="fill" flex="row" gap={{8}}>{cells}</Frame>'

def slot_grid(sel="10:30"):
    slots=[("09:00",True),("09:30",True),("10:00",False),("10:30",True),
           ("11:00",True),("11:30",False),("14:00",True),("14:30",True),("15:00",True)]
    cells=[]
    for t,ok in slots:
        if not ok:
            st='bg="var:neutral/100"'; col="var:text/faint"
        elif t==sel:
            st='image="assets/img/btn-navy.jpg" overflow="hidden"'; col="var:text/on-dark"
        else:
            st='bg="var:bg/base" stroke="var:border/default" strokeWidth={1}'; col="var:text/default"
        cells.append(f'<Frame name="Btn Slot {t}" grow={{1}} flex="row" justify="center" py={{13}} rounded={{16}} {st}>'
                f'{T(14,"semibold",col,t)}</Frame>')
    return rows_of(cells, 3, 9)

def summary_row(ic,label,value):
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center">'
            f'<Frame w={{38}} h={{38}} rounded={{12}} bg="var:bg/muted" flex="col" justify="center" items="center">{I(ic,17,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(12,"regular","var:text/muted",label)}'
            f'{T(15,"semibold","var:text/strong",value)}</Frame></Frame>')


# ---------------------------------------------------------------- desktop dashboard parts
def stat_card(ic, value, label, sub, tint="tint-teal.jpg"):
    return (f'<Frame grow={{1}} flex="col" gap={{12}} p={{20}} rounded={{24}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame w={{44}} h={{44}} rounded={{14}} image="assets/img/{tint}" overflow="hidden" flex="col" justify="center" items="center">{I(ic,20,W_IC)}</Frame>'
            f'{I("arrow-up-right",17,M_IC)}</Frame>'
            f'<Frame flex="col" gap={{2}}>{T(28,"bold","var:text/strong",value)}'
            f'{T(13,"semibold","var:text/default",label)}{T(12,"regular","var:text/muted",sub)}</Frame></Frame>')

def hero_banner():
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{24}} p={{28}} rounded={{28}} '
            f'image="assets/img/hero-banner.jpg" overflow="hidden">'
            f'<Frame grow={{1}} flex="col" gap={{9}}>'
            f'<Frame flex="row" gap={{9}} items="center">{I("sparkles",17,T_IC)}'
            f'{T(12,"semibold","var:brand/teal","GOOD MORNING, AMARA")}</Frame>'
            f'{T(28,"bold","var:text/on-dark","How are you feeling today?")}'
            f'{T(15,"regular","var:text/on-dark-muted","Book a verified doctor in under a minute — in person or by video.",w="fill")}</Frame>'
            f'<Frame flex="row" gap={{11}} items="center">'
            f'<Frame name="Btn Book now" flex="row" gap={{9}} items="center" px={{20}} py={{14}} rounded={{999}} bg="var:bg/base">'
            f'{I("calendar-plus",17,N_IC)}{T(14,"semibold","var:text/strong","Book a visit")}</Frame>'
            f'<Frame name="Btn Talk now" flex="row" gap={{9}} items="center" px={{20}} py={{14}} rounded={{999}} bg="var:bg/band-2">'
            f'{I("video",17,W_IC)}{T(14,"semibold","var:text/on-dark","Talk to a doctor")}</Frame></Frame></Frame>')

def med_row(name, dose, time, taken=True):
    pill=(f'<Frame flex="row" gap={{6}} items="center" px={{11}} py={{6}} rounded={{999}} bg="var:state/success-bg">'
          f'{I("check",12,OK_IC)}{T(11,"semibold","var:state/success","Taken")}</Frame>' if taken else
          f'<Frame name="Btn Take {name}" flex="row" gap={{6}} items="center" px={{13}} py={{6}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden">'
          f'{T(11,"semibold","var:text/on-dark","Mark taken")}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{38}} h={{38}} rounded={{12}} bg="var:bg/muted" flex="col" justify="center" items="center">{I("pill",17,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"semibold","var:text/strong",name)}'
            f'{T(12,"regular","var:text/muted",dose)}</Frame>'
            f'{T(13,"medium","var:text/default",time)}{pill}</Frame>')

def record_row(date, title, doctor):
    return (f'<Frame name="Btn Record {date}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{38}} h={{38}} rounded={{12}} bg="var:state/info-bg" flex="col" justify="center" items="center">{I("file-text",17,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"semibold","var:text/strong",title)}'
            f'{T(12,"regular","var:text/muted",doctor)}</Frame>'
            f'{T(12,"regular","var:text/muted",date)}{I("chevron-right",16,M_IC)}</Frame>')

# ---------------------------------------------------------------- shells
def mob(name, children, nav=None):
    navrow=f'<Frame w="fill" px={{14}} pb={{10}}>{nav}</Frame>' if nav else ''
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/surface-mobile.jpg" overflow="hidden">'
            f'{statusbar()}{children}{navrow}</Frame>')

def desk(name, children, sidebar_active=0, topbar=True):
    """Delegates to the one shell. The signature is unchanged, so not one screen had to move."""
    return app_desk(name, "member", title_from(name),
                    f'<Frame w="fill" flex="col" gap={{16}}>{children}</Frame>',
                    NAV_MEMBER, sidebar_active)
