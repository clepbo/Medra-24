#!/usr/bin/env python3
"""Medra — Member app, batch 1: Home → Search → Doctor profile → Booking → Confirmation.
Also emits interactive-component state frames (cmp/…) that components-medra.js turns into
real Figma component sets with variants + hover/press interactions."""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *          # shared "Soft Clinical" vocabulary

OUT = "/home/user/Medra-24/figma/medra-member"
os.makedirs(OUT, exist_ok=True)

from member_kit import *     # member chrome: nav, dashboard shell, cards


frames=[]; NAMES={}; ORDER={}
def add(page,fid,d,m):
    frames.append((page,f"{fid}-d.jsx",d)); frames.append((page,f"{fid}-m.jsx",m))
    NAMES[fid]=(re.search(r'name="([^"]+)"',d).group(1), re.search(r'name="([^"]+)"',m).group(1))
    ORDER.setdefault(page,[]).append(fid)

DOCTORS=[("avatar-4.jpg","Dr. Ngozi Okafor","Cardiologist","Garki Medical Centre","₦15,000","4.9","10:30"),
         ("avatar-1.jpg","Dr. Chuka Eze","General practice","Wuse Clinic","₦8,000","4.8","11:00"),
         ("avatar-3.jpg","Dr. Kemi Adeyemi","Paediatrician","Maitama Hospital","₦12,000","4.9","14:00"),
         ("avatar-5.jpg","Dr. Tunde Bello","Neurologist","Asokoro Specialist","₦25,000","4.7","09:30")]

# ============================================================ H1 HOME (returning)
HEALTH_CARD=card(section_head("Your health","Records","Nav Records")
    + summary_row("droplet","Blood group","O+")
    + summary_row("pill","Active prescriptions","2 medicines")
    + summary_row("triangle-alert","Allergies","Penicillin"), p=20, gap=14)
home_body=(f'{searchbar()}{next_visit_card()}'
           f'<Frame w="fill" flex="col" gap={{11}}>{section_head("Browse by specialty","See all","See specialties")}'
           f'{specialty_row(3,3)}</Frame>'
           f'<Frame w="fill" flex="col" gap={{11}}>{section_head("Available today","See all","See doctors")}'
           f'{doctor_card(*DOCTORS[0])}</Frame>')
DASH_STATS=rows_of([
    stat_card("calendar-check","2","Upcoming visits","Next in 2 days","tint-teal.jpg"),
    stat_card("pill","2","Active medicines","1 due at 6pm","tint-blue.jpg"),
    stat_card("clipboard-list","8","Visits on record","Since Jan 2026","tint-ocean.jpg"),
    stat_card("shield-check","O+","Blood group","Allergy: penicillin","tint-navy.jpg"),
], 4, 16)

MEDS_PANEL=card(section_head("Today’s medicines","See all","Nav Meds")
    + med_row("Amlodipine","5 mg · 1 tablet","08:00",True)
    + '<Rect w="fill" h={1} bg="var:border/subtle" />'
    + med_row("Metformin","500 mg · 1 tablet","18:00",False), p=20, gap=8)

RECORDS_PANEL=card(section_head("Recent records","See all","Nav Records")
    + record_row("12 Jun","Hypertension review","Dr. Ngozi Okafor")
    + '<Rect w="fill" h={1} bg="var:border/subtle" />'
    + record_row("28 Apr","Full blood count","Garki Medical Centre"), p=20, gap=8)

DOCS_PANEL=card(section_head("Available today","See all","See doctors")
    + doctor_card(*DOCTORS[0]) + doctor_card(*DOCTORS[1]), p=20, gap=13)

SPEC_PANEL=card(section_head("Browse by specialty","See all","See specialties")
    + specialty_row(6,3), p=20, gap=13)

add("Member","H1-home",
    desk("Member · Home — H1 Home",
        f'{hero_banner()}{DASH_STATS}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{18}}>{DOCS_PANEL}{MEDS_PANEL}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{18}}>{next_visit_card()}{SPEC_PANEL}{RECORDS_PANEL}</Frame></Frame>'),
    mob("Member · Home — H1 Home · Mobile",
        f'{greet_bar()}<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{6}} pb={{8}}>{home_body}</Frame>',
        nav=bottom_nav(0)))

# ============================================================ H2 HOME (new member, empty)
empty_body=(f'{searchbar()}'
            f'<Frame w="fill" flex="col" gap={{14}} items="center" p={{26}} rounded={{26}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{78}} h={{78}} rounded={{999}} bg="var:state/info-bg" flex="col" justify="center" items="center">{I("calendar-plus",34,A_IC)}</Frame>'
            f'{T(18,"bold","var:text/strong","No visits booked yet")}'
            f'{T(14,"regular","var:text/muted","Find a verified doctor near you and book your first appointment — it takes about a minute.",w="fill",align="center")}'
            f'{cta("Find a doctor","Find doctor H2","search")}</Frame>'
            f'<Frame w="fill" flex="col" gap={{11}}>{section_head("Browse by specialty","See all","See specialties")}{specialty_row(3,3)}</Frame>'
            )   # no second doctor block: keeps the first-run screen inside 844
EMPTY_PANEL=card(
    '<Frame w="fill" flex="col" gap={16} items="center" py={10}>'
    + '<Frame w={84} h={84} rounded={999} bg="var:state/info-bg" flex="col" justify="center" items="center">' + I("calendar-plus",36,A_IC) + '</Frame>'
    + T(20,"bold","var:text/strong","No visits booked yet")
    + T(14,"regular","var:text/muted","Find a verified doctor near you and book your first appointment — it takes about a minute.",w="fill",align="center")
    + '<Frame w={280} flex="col">' + cta("Find a doctor","Find doctor H2","search") + '</Frame></Frame>', p=24, gap=0)

add("Member","H2-home-empty",
    desk("Member · Home — H2 First Visit (empty state)",
        f'{hero_banner()}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{18}}>{EMPTY_PANEL}{DOCS_PANEL}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{18}}>{SPEC_PANEL}'
        f'{card(section_head("Your health","Add","Nav Records")+summary_row("droplet","Blood group","Not set yet")+summary_row("pill","Medicines","None added")+summary_row("triangle-alert","Allergies","None added"),p=20,gap=14)}</Frame></Frame>'),
    mob("Member · Home — H2 First Visit · Mobile",
        f'{greet_bar()}<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{6}} pb={{8}}>{empty_body}</Frame>',
        nav=bottom_nav(0)))

# ============================================================ S1 SEARCH RESULTS
def filter_chips(per_row=4):
    cells=[
      f'<Frame name="Btn Filter Today" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{10}} rounded={{999}} image="assets/img/btn-navy.jpg" overflow="hidden">{I("clock",14,W_IC)}{T(13,"semibold","var:text/on-dark","Today")}</Frame>',
      f'<Frame name="Btn Filter Week" grow={{1}} flex="row" justify="center" px={{14}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{T(13,"medium","var:text/default","This week")}</Frame>',
      f'<Frame name="Btn Filter Virtual" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{I("video",14,N_IC)}{T(13,"medium","var:text/default","Virtual")}</Frame>',
      f'<Frame name="Btn Filter Near" grow={{1}} flex="row" gap={{7}} justify="center" items="center" px={{14}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{I("map-pin",14,N_IC)}{T(13,"medium","var:text/default","Near me")}</Frame>',
    ]
    return rows_of(cells, per_row, 9)
FILTERS=filter_chips(4)
FILTERS_M=filter_chips(2)
results=("".join(doctor_card(*d) for d in DOCTORS[:3]))
results_m=("".join(doctor_card(*d) for d in DOCTORS[:2]))   # fits 844 — see SETUP.md
add("Member","S1-results",
    desk("Member · Search — S1 Results",
        f'{searchbar("Cardiologist in Abuja")}'
        f'<Frame w="fill" flex="row" justify="between" items="center">{FILTERS}'
        f'<Frame name="Btn Sort" flex="row" gap={{7}} items="center" px={{15}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
        f'{I("arrow-up-down",14,N_IC)}{T(13,"medium","var:text/default","Soonest")}</Frame></Frame>'
        f'{T(13,"regular","var:text/muted","24 verified doctors available")}'
        + rows_of([f'<Frame grow={{1}} flex="col">{doctor_card(*d)}</Frame>' for d in DOCTORS], 2, 16), 1),
    mob("Member · Search — S1 Results · Mobile",
        f'{appbar("Find care", right=circle_btn("sliders-horizontal","Filters"))}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{15}} px={{20}} pt={{6}} pb={{10}}>'
        f'{searchbar("Cardiologist in Abuja")}{FILTERS_M}'
        f'{T(13,"regular","var:text/muted","24 verified doctors available")}{results_m}</Frame>',
        nav=bottom_nav(1)))

# ============================================================ S2 FILTERS (sheet)
filter_body=(f'<Frame w="fill" flex="col" gap={{20}}>'
             f'{field_chips("Specialty",["Any","Cardiology","General","Paediatrics","Neurology"],1,"FSpec")}'
             f'{field_chips("Availability",["Today","Tomorrow","This week","Any time"],0,"FAvail")}'
             f'{field_chips("Visit type",["Any","In-person","Virtual"],0,"FType")}'
             f'{field_chips("Distance",["Under 2 km","Under 5 km","Under 10 km","Any"],1,"FDist")}'
             f'{field_chips("Price",["Any","Under ₦10k","₦10k – ₦20k","₦20k+"],0,"FPrice")}'
             f'{field_chips("Language",["Any","English","Hausa","Yoruba","Igbo"],0,"FLang")}</Frame>')
add("Member","S2-filters",
    desk("Member · Search — S2 Filters",
        f'{head_chip([("Refine your",False),("search",True)],30)}{filter_body}'
        f'<Frame w="fill" flex="row" gap={{12}}>'
        f'<Frame grow={{1}} flex="col">{ghost("Reset all","Reset filters","refresh-cw")}</Frame>'
        f'<Frame grow={{1}} flex="col">{cta("Show 24 doctors","Apply filters")}</Frame></Frame>', 1),
    mob("Member · Search — S2 Filters · Mobile",
        f'<Frame grow={{1}} w="fill" flex="col" justify="end">'
        f'<Frame w="fill" flex="col" gap={{18}} px={{22}} pt={{16}} pb={{26}} rounded={{32}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
        f'<Frame w="fill" flex="row" justify="center"><Rect w={{44}} h={{5}} rounded={{999}} bg="var:neutral/300" /></Frame>'
        f'<Frame w="fill" flex="row" justify="between" items="center">{T(20,"bold","var:text/strong","Filters")}'
        f'<Frame name="Btn Close filters" flex="row">{I("x",21,N_IC)}</Frame></Frame>'
        f'{filter_body}'
        f'<Frame w="fill" flex="row" gap={{12}}>'
        f'<Frame grow={{1}} flex="col">{ghost("Reset","Reset filters")}</Frame>'
        f'<Frame grow={{1}} flex="col">{cta("Show 24","Apply filters")}</Frame></Frame></Frame></Frame>'))

# ============================================================ S3 NO RESULTS
nores=(f'<Frame w="fill" flex="col" gap={{15}} items="center" p={{28}} rounded={{26}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
       f'<Frame w={{82}} h={{82}} rounded={{999}} bg="var:state/warning-bg" flex="col" justify="center" items="center">{I("search",36,WARN_IC)}</Frame>'
       f'{T(19,"bold","var:text/strong","No doctors match those filters")}'
       f'{T(14,"regular","var:text/muted","Try widening your search — or let us text you the moment a slot opens up.",w="fill",align="center")}'
       f'{cta("Clear filters","Clear filters S3","refresh-cw")}'
       f'{ghost("Notify me when a slot opens","Notify me S3","bell-ring")}</Frame>')
add("Member","S3-empty",
    desk("Member · Search — S3 No Results",
        f'{searchbar("Endocrinologist · Today · Under ₦10k")}{FILTERS}'
        f'<Frame w="fill" flex="row" justify="center" pt={{16}}><Frame w={{520}} flex="col">{nores}</Frame></Frame>'
        f'{section_head("You might also consider","","Alt doctors")}'
        + rows_of([f'<Frame grow={{1}} flex="col">{doctor_card(*d)}</Frame>' for d in DOCTORS[1:3]], 2, 16), 1),
    mob("Member · Search — S3 No Results · Mobile",
        f'{appbar("Find care", right=circle_btn("sliders-horizontal","Filters"))}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{16}} px={{20}} pt={{6}} pb={{10}}>'
        f'{searchbar("Endocrinologist · Today")}{nores}'
        f'{section_head("You might also consider","","Alt doctors")}{doctor_card(*DOCTORS[1])}</Frame>',
        nav=bottom_nav(1)))

# ============================================================ P1 DOCTOR PROFILE
_P1_LATER=True
def stat_cell(v,l,ic):
    return (f'<Frame grow={{1}} flex="col" gap={{4}} items="center" py={{14}} rounded={{18}} bg="var:bg/subtle">'
            f'{I(ic,17,A_IC)}{T(16,"bold","var:text/strong",v)}{T(11,"regular","var:text/muted",l)}</Frame>')
PROFILE_HEAD=(f'<Frame w="fill" flex="col" gap={{16}} p={{20}} rounded={{28}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
              f'<Frame w="fill" flex="row" gap={{16}} items="center">'
              f'<Image image="assets/img/avatar-4.jpg" w={{88}} h={{88}} rounded={{26}} />'
              f'<Frame grow={{1}} flex="col" gap={{5}}>'
              f'<Frame flex="row" gap={{8}} items="center">{T(20,"bold","var:text/strong","Dr. Ngozi Okafor")}{I("badge-check",19,T_IC)}</Frame>'
              f'{T(14,"regular","var:text/muted","Cardiologist · MDCN verified")}'
              f'<Frame flex="row" gap={{7}} items="center">{I("map-pin",14,M_IC)}'
              f'{T(13,"regular","var:text/muted","Garki Medical Centre · 2.4 km")}</Frame></Frame></Frame>'
              f'<Frame w="fill" flex="row" gap={{10}}>{stat_cell("12 yrs","Experience","briefcase-medical")}'
              f'{stat_cell("4.9","Rating","star")}{stat_cell("1.2k","Patients","users")}</Frame></Frame>')
ABOUT=card(T(16,"bold","var:text/strong","About")+
           T(14,"regular","var:text/muted","Consultant cardiologist with 12 years of experience in hypertension, heart failure and preventive cardiology. Speaks English, Hausa and Igbo.",w="fill")
           + rows_of([proof("globe","English · Hausa · Igbo",dark=False),proof("video","In-person &amp; virtual",dark=False)],2,8),p=20,gap=12)
FEEBAR=(f'<Frame w="fill" flex="row" justify="between" items="center" p={{18}} rounded={{22}} bg="var:state/info-bg">'
        f'<Frame flex="col" gap={{2}}>{T(12,"regular","var:text/muted","Consultation fee")}'
        f'{T(22,"bold","var:text/strong","₦15,000")}</Frame>'
        f'<Frame flex="col" gap={{2}} items="end">{T(12,"regular","var:text/muted","Next available")}'
        f'{T(15,"semibold","var:state/success","Today · 10:30")}</Frame></Frame>')
P1_AVAIL=card(T(16,"bold","var:text/strong","Availability this week") + date_strip() + slot_grid(), p=20, gap=14)
P1_SUMMARY=card(summary_row("calendar-days","Date","Wed, 21 August") + summary_row("clock","Time","10:30 AM")
    + summary_row("video","Type","Virtual consultation"), p=20, gap=14)
P1_DATECARD=card(T(16,"bold","var:text/strong","Pick a date") + date_strip(), p=18, gap=13)
ABOUT_M=card(T(16,"bold","var:text/strong","About")+
             T(14,"regular","var:text/muted","Consultant cardiologist, 12 years in hypertension and heart failure. Speaks English, Hausa and Igbo.",w="fill"),p=18,gap=10)
add("Member","P1-profile",
    desk("Member · Doctor — P1 Profile",
        f'<Frame w="fill" flex="row" gap={{22}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{PROFILE_HEAD}{ABOUT}'
        f'{P1_AVAIL}</Frame>'
        f'<Frame w={{368}} flex="col" gap={{16}}>{FEEBAR}'
        f'{P1_SUMMARY}'
        f'{cta("Continue to booking","Book P1")}{ghost("Message the clinic","Message P1","message-square-text")}</Frame></Frame>', 1),
    mob("Member · Doctor — P1 Profile · Mobile",
        f'{appbar("Doctor", right=circle_btn("heart","Save doctor"))}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{15}} px={{20}} pt={{4}} pb={{10}}>'
        f'{PROFILE_HEAD}{FEEBAR}{ABOUT_M}'
        f'{P1_DATECARD}'
        f'{cta("See available times","Book P1","arrow-right")}</Frame>'))

# ============================================================ B1 SELECT TIME
TYPE_CARD=card(T(16,"bold","var:text/strong","How would you like to be seen?")
    + choice("hospital","In person","Garki Medical Centre · 2.4 km away","Type inperson")
    + choice("video","Virtual consultation","Video call — link sent by SMS","Type virtual",sel=True), p=20, gap=13)
TYPE_CARD_M=card(choice("hospital","In person","Garki Medical Centre","Type inperson")
    + choice("video","Virtual consultation","Link sent by SMS","Type virtual",sel=True), p=16, gap=11)
BOOKING_SUMMARY=card(T(16,"bold","var:text/strong","Your booking")
    + summary_row("user","Doctor","Dr. Ngozi Okafor") + summary_row("calendar-days","Date","Wed, 21 August")
    + summary_row("clock","Time","10:30 AM") + summary_row("video","Type","Virtual"), p=20, gap=14)
AVAIL_CARD=card(T(16,"bold","var:text/strong","August 2026") + date_strip() + SP(2)
    + T(13,"semibold","var:text/default","Morning") + slot_grid(), p=20, gap=14)
add("Member","B1-slot",
    desk("Member · Booking — B1 Choose a Time",
        f'{head_chip([("Choose a",False),("time",True)],30)}'
        f'{T(15,"regular","var:text/muted","Only genuinely open slots are shown — if it’s here, you can book it.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{22}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>'
        f'{AVAIL_CARD}'
        f'{TYPE_CARD}</Frame>'
        f'<Frame w={{368}} flex="col" gap={{16}}>'
        f'{BOOKING_SUMMARY}'
        f'{cta("Review booking","Review B1")}</Frame></Frame>', 1),
    mob("Member · Booking — B1 Choose a Time · Mobile",
        f'{appbar("Choose a time")}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{15}} px={{20}} pt={{4}} pb={{10}}>'
        f'{date_strip()}'
        f'{card(T(15,"semibold","var:text/default","Morning &amp; afternoon")+slot_grid(),p=18,gap=13)}'
        f'{TYPE_CARD_M}'
        f'<Frame grow={{1}} />{cta("Review booking","Review B1")}</Frame>'))

# ============================================================ B2 SLOT TAKEN (edge case)
taken=(f'<Frame w="fill" flex="col" gap={{15}} items="center" p={{26}} rounded={{26}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
       f'<Frame w={{80}} h={{80}} rounded={{999}} bg="var:state/warning-bg" flex="col" justify="center" items="center">{I("circle-alert",36,WARN_IC)}</Frame>'
       f'{T(19,"bold","var:text/strong","That slot was just taken")}'
       f'{T(14,"regular","var:text/muted","Someone booked 10:30 a moment ago. Here are the closest times still open with Dr. Okafor.",w="fill",align="center")}'
       f'<Frame w="fill" flex="row" gap={{9}} justify="center">'
       f'<Frame name="Btn Slot 11:00" flex="row" px={{18}} py={{12}} rounded={{16}} image="assets/img/btn-navy.jpg" overflow="hidden">{T(14,"semibold","var:text/on-dark","11:00")}</Frame>'
       f'<Frame name="Btn Slot 14:00" flex="row" px={{18}} py={{12}} rounded={{16}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{T(14,"semibold","var:text/default","14:00")}</Frame>'
       f'<Frame name="Btn Slot 14:30" flex="row" px={{18}} py={{12}} rounded={{16}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{T(14,"semibold","var:text/default","14:30")}</Frame></Frame>'
       f'{cta("Book 11:00 instead","Book alt B2")}{ghost("Pick another day","Another day B2","calendar-days")}</Frame>')
add("Member","B2-taken",
    desk("Member · Booking — B2 Slot Taken",
        f'{head_chip([("Let’s find another",False),("time",True)],30)}'
        f'<Frame w="fill" flex="row" justify="center"><Frame w={{560}} flex="col">{taken}</Frame></Frame>', 1),
    mob("Member · Booking — B2 Slot Taken · Mobile",
        f'{appbar("Choose a time")}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{15}} px={{20}} pt={{4}} pb={{10}}>{taken}</Frame>'))

# ============================================================ B3 REVIEW & CONFIRM
DOC_ROW=(f'<Frame w="fill" flex="row" gap={{13}} items="center">'
         f'<Image image="assets/img/avatar-4.jpg" w={{54}} h={{54}} rounded={{18}} />'
         f'<Frame grow={{1}} flex="col" gap={{2}}>{T(16,"semibold","var:text/strong","Dr. Ngozi Okafor")}'
         f'{T(13,"regular","var:text/muted","Cardiologist · Garki Medical Centre")}</Frame></Frame>')
APPT_CARD=card(T(16,"bold","var:text/strong","Your appointment") + DOC_ROW
    + '<Rect w="fill" h={1} bg="var:border/subtle" />'
    + summary_row("calendar-days","Date","Wednesday, 21 August 2026")
    + summary_row("clock","Time","10:30 AM · 30 minutes")
    + summary_row("video","Type","Virtual consultation")
    + summary_row("credit-card","Fee","₦15,000 — paid at the clinic"), p=20, gap=14)
NEXT_CARD=card(T(15,"bold","var:text/strong","What happens next")
    + summary_row("check","1. We hold your slot","Confirmed instantly")
    + summary_row("message-square-text","2. SMS confirmation","With your booking reference")
    + summary_row("bell-ring","3. Reminders","24 hours and 2 hours before"), p=20, gap=13)
REVIEW=(f'{APPT_CARD}'
        f'{field("Reason for visit (optional)","file-text","e.g. chest pain for 3 days")}'
        f'{note("shield-check","Dr. Okafor will see your allergies and current medicines so they can prescribe safely. Nothing else is shared.","info")}'
        f'{checkbox("Send me SMS reminders 24 hours and 2 hours before","SMS reminders")}')
add("Member","B3-review",
    desk("Member · Booking — B3 Review &amp; Confirm",
        f'{head_chip([("Review and",False),("confirm",True)],30)}'
        f'<Frame w="fill" flex="row" gap={{22}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{REVIEW}</Frame>'
        f'<Frame w={{368}} flex="col" gap={{16}}>'
        f'{NEXT_CARD}'
        f'{cta("Confirm booking","Confirm B3","check")}{ghost("Back to times","Back times B3","arrow-left")}</Frame></Frame>', 1),
    mob("Member · Booking — B3 Review &amp; Confirm · Mobile",
        f'{appbar("Review")}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{10}}>{REVIEW}'
        f'<Frame grow={{1}} />{cta("Confirm booking","Confirm B3","check")}</Frame>'))

# ============================================================ C1 CONFIRMED
CONFIRM_CARD=card(summary_row("calendar-days","Date","Wednesday, 21 August 2026")
    + summary_row("clock","Time","10:30 AM · 30 minutes")
    + summary_row("video","Type","Virtual — link by SMS"), p=20, gap=13)
CONFIRM=(f'<Frame w="fill" flex="col" gap={{16}} items="center">'
         f'{big_icon("circle-check","ok",104)}'
         f'{T(24,"bold","var:text/strong","Booking confirmed")}'
         f'{T(15,"regular","var:text/muted","Dr. Ngozi Okafor is expecting you on Wednesday, 21 August at 10:30 AM.",w="fill",align="center")}'
         f'<Frame w="fill" flex="row" gap={{10}} justify="center" items="center" px={{18}} py={{13}} rounded={{999}} bg="var:bg/muted">'
         f'{I("receipt",16,A_IC)}{T(14,"semibold","var:text/strong","Reference MDR-4820-71")}</Frame>'
         f'{CONFIRM_CARD}'
         f'{note("message-square-text","We’ve texted your confirmation to +234 801 234 5678. Reminders follow 24 hours and 2 hours before.","ok")}</Frame>')
add("Member","C1-confirmed",
    desk("Member · Booking — C1 Confirmed",
        f'<Frame w="fill" flex="row" justify="center" pt={{10}}>'
        f'<Frame w={{620}} flex="col" gap={{18}}>{CONFIRM}'
        f'<Frame w="fill" flex="row" gap={{12}}>'
        f'<Frame grow={{1}} flex="col">{ghost("Add to calendar","Add calendar C1","calendar-plus")}</Frame>'
        f'<Frame grow={{1}} flex="col">{cta("View my visits","View visits C1")}</Frame></Frame></Frame></Frame>', 2),
    mob("Member · Booking — C1 Confirmed · Mobile",
        f'{appbar(None, back=False, right=circle_btn("x","Close confirm"))}'
        f'<Frame grow={{1}} w="fill" flex="col" gap={{16}} px={{20}} pt={{6}} pb={{10}}>{CONFIRM}'
        f'<Frame grow={{1}} />{cta("View my visits","View visits C1")}'
        f'{ghost("Add to calendar","Add calendar C1","calendar-plus")}</Frame>'))

# ============================================================ INTERACTIVE COMPONENT STATES
# Frames named cmp/<Component>/<Prop>=<Value> are converted by components-medra.js
CMP=[]
def cmp_frame(comp, prop, value, body, w=320, h=None):
    hh=f' minH={{{h}}}' if h else ''
    CMP.append((f"cmp/{comp}/{prop}={value}",
        f'<Frame name="cmp/{comp}/{prop}={value}" w={{{w}}}{hh} flex="col" p={{16}} bg="var:bg/base">{body}</Frame>'))

# Primary button
for st,body in [("Default",cta("Book appointment","CBtn")),
                ("Hover",  cta("Book appointment","CBtn")),
                ("Pressed",cta("Book appointment","CBtn")),
                ("Loading",f'<Frame w="fill" flex="row" gap={{10}} justify="center" items="center" px={{24}} py={{17}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden">{I("loader",18,W_IC)}{T(16,"semibold","var:text/on-dark","Booking…")}</Frame>'),
                ("Disabled",f'<Frame w="fill" flex="row" gap={{10}} justify="center" items="center" px={{24}} py={{17}} rounded={{999}} bg="var:neutral/200">{T(16,"semibold","var:text/faint","Book appointment")}</Frame>')]:
    cmp_frame("Button Primary","State",st,body)
# Input
for st,body in [("Default",field("Phone number","phone","801 234 5678",prefix="+234")),
                ("Focus",  field("Phone number","phone","801 234 5678",prefix="+234",focus=True)),
                ("Filled", field("Phone number","phone","801 234 5678",ph=False,prefix="+234")),
                ("Error",  field("Phone number","phone","801 234","",prefix="+234",error="Enter a valid 10-digit number"))]:
    cmp_frame("Input","State",st,body)
# Time slot
for st,body in [("Available",f'<Frame w={{98}} flex="row" justify="center" py={{13}} rounded={{16}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{T(14,"semibold","var:text/default","10:30")}</Frame>'),
                ("Hover",    f'<Frame w={{98}} flex="row" justify="center" py={{13}} rounded={{16}} bg="var:bg/muted" stroke="var:border/accent" strokeWidth={{1}}>{T(14,"semibold","var:text/default","10:30")}</Frame>'),
                ("Selected", f'<Frame w={{98}} flex="row" justify="center" py={{13}} rounded={{16}} image="assets/img/btn-navy.jpg" overflow="hidden">{T(14,"semibold","var:text/on-dark","10:30")}</Frame>'),
                ("Taken",    f'<Frame w={{98}} flex="row" justify="center" py={{13}} rounded={{16}} bg="var:neutral/100">{T(14,"semibold","var:text/faint","10:30")}</Frame>')]:
    cmp_frame("Time Slot","State",st,body,w=140)
# Specialty chip
for st,body in [("Default",f'<Frame w={{92}} flex="col" gap={{9}} items="center" py={{16}} px={{8}} rounded={{20}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}><Frame w={{44}} h={{44}} rounded={{14}} bg="var:bg/muted" flex="col" justify="center" items="center">{I("heart-pulse",21,A_IC)}</Frame>{T(12,"medium","var:text/default","Cardiology")}</Frame>'),
                ("Hover",  f'<Frame w={{92}} flex="col" gap={{9}} items="center" py={{16}} px={{8}} rounded={{20}} bg="var:bg/base" stroke="var:border/accent" strokeWidth={{2}}><Frame w={{44}} h={{44}} rounded={{14}} bg="var:state/info-bg" flex="col" justify="center" items="center">{I("heart-pulse",21,A_IC)}</Frame>{T(12,"medium","var:text/default","Cardiology")}</Frame>'),
                ("Selected",f'<Frame w={{92}} flex="col" gap={{9}} items="center" py={{16}} px={{8}} rounded={{20}} image="assets/img/btn-navy.jpg" overflow="hidden"><Frame w={{44}} h={{44}} rounded={{14}} bg="var:bg/band-2" flex="col" justify="center" items="center">{I("heart-pulse",21,T_IC)}</Frame>{T(12,"medium","var:text/on-dark","Cardiology")}</Frame>')]:
    cmp_frame("Specialty Chip","State",st,body,w=130)
# Toggle + checkbox
for st,body in [("On", f'<Frame w={{52}} h={{30}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden" flex="row" justify="end" items="center" px={{4}}><Ellipse w={{22}} h={{22}} bg="#FFFFFF" /></Frame>'),
                ("Off",f'<Frame w={{52}} h={{30}} rounded={{999}} bg="var:neutral/300" flex="row" justify="start" items="center" px={{4}}><Ellipse w={{22}} h={{22}} bg="#FFFFFF" /></Frame>')]:
    cmp_frame("Toggle","State",st,body,w=100)
for st,body in [("Checked",  f'<Frame w={{24}} h={{24}} rounded={{7}} bg="var:brand/teal" flex="col" justify="center" items="center">{I("check",15,W_IC)}</Frame>'),
                ("Unchecked",'<Rect w={24} h={24} rounded={7} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />')]:
    cmp_frame("Checkbox","State",st,body,w=80)
# Bottom nav item
for st,body in [("Active",  f'<Frame w={{84}} flex="col" gap={{4}} items="center">{I("house",22,T_IC)}{T(11,"semibold","var:text/accent","Home")}</Frame>'),
                ("Inactive",f'<Frame w={{84}} flex="col" gap={{4}} items="center">{I("house",22,M_IC)}{T(11,"regular","var:text/muted","Home")}</Frame>')]:
    cmp_frame("Nav Item","State",st,body,w=120)
# Doctor card
cmp_frame("Doctor Card","State","Default",doctor_card(*DOCTORS[0],nm="CCard"),w=460)
cmp_frame("Doctor Card","State","Hover",
    doctor_card(*DOCTORS[0],nm="CCard").replace('stroke="var:border/subtle" strokeWidth={1}','stroke="var:border/accent" strokeWidth={2}',1),w=460)

for nm, jsx in CMP:
    fid = nm.replace("cmp/","CMP-").replace("/","-").replace("=","-").replace(" ","")
    frames.append(("Components", fid+".jsx", jsx))
    ORDER.setdefault("Components",[]).append(fid)

# ---------------------------------------------------------------- write
def sanitize(s): return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)','&amp;',s)
manifest={}
for page,fn,jsx in frames:
    open(os.path.join(OUT,fn),"w").write(sanitize(jsx))
    manifest.setdefault(page,[]).append(fn)
open(os.path.join(OUT,"pages.json"),"w").write(json.dumps(manifest,indent=2))

PAGE_FIGMA={"Member":"Medra Member — Find &amp; Book","Components":"Medra — Interactive Components"}
TRN=[
 ("H1-home","Btn Search","S1-results"),("H1-home","Btn Filters","S2-filters"),
 ("H1-home","Btn See doctors","S1-results"),("H1-home","Btn See specialties","S1-results"),
 ("H1-home","Btn Upcoming visit","P1-profile"),("H1-home","Btn Join visit","C1-confirmed"),
 ("H1-home","Btn Reschedule","B1-slot"),("H1-home","Btn Nav Visits","C1-confirmed"),
 ("H1-home","Btn Nav Find","S1-results"),("H1-home","Btn Notifications","H1-home"),
 ("H2-home-empty","Btn Find doctor H2","S1-results"),("H2-home-empty","Btn Search","S1-results"),
 ("H2-home-empty","Btn See doctors","S1-results"),("H2-home-empty","Btn Nav Find","S1-results"),
 ("S1-results","Btn Filters","S2-filters"),("S1-results","Btn Sort","S2-filters"),
 ("S1-results","Btn Back","H1-home"),("S1-results","Btn Nav Home","H1-home"),
 ("S2-filters","Btn Apply filters","S1-results"),("S2-filters","Btn Close filters","S1-results"),
 ("S2-filters","Btn Reset filters","S1-results"),("S2-filters","Btn Nav Home","H1-home"),
 ("S3-empty","Btn Clear filters S3","S1-results"),("S3-empty","Btn Notify me S3","S1-results"),
 ("S3-empty","Btn Back","S1-results"),("S3-empty","Btn Filters","S2-filters"),("S3-empty","Btn Nav Home","H1-home"),
 ("P1-profile","Btn Book P1","B1-slot"),("P1-profile","Btn Back","S1-results"),
 ("P1-profile","Btn Message P1","P1-profile"),("P1-profile","Btn Save doctor","P1-profile"),
 ("P1-profile","Btn Nav Home","H1-home"),
 ("B1-slot","Btn Review B1","B3-review"),("B1-slot","Btn Back","P1-profile"),
 ("B1-slot","Btn Slot 10:00","B2-taken"),("B1-slot","Btn Nav Home","H1-home"),
 ("B2-taken","Btn Book alt B2","B3-review"),("B2-taken","Btn Another day B2","B1-slot"),
 ("B2-taken","Btn Back","B1-slot"),("B2-taken","Btn Nav Home","H1-home"),
 ("B3-review","Btn Confirm B3","C1-confirmed"),("B3-review","Btn Back times B3","B1-slot"),
 ("B3-review","Btn Back","B1-slot"),("B3-review","Btn Nav Home","H1-home"),
 ("C1-confirmed","Btn View visits C1","H1-home"),("C1-confirmed","Btn Add calendar C1","C1-confirmed"),
 ("C1-confirmed","Btn Close confirm","H1-home"),("C1-confirmed","Btn Nav Home","H1-home"),
]
# every doctor card / specialty chip opens the profile
for d in DOCTORS:
    for scr in ("H1-home","H2-home-empty","S1-results","S3-empty"):
        TRN.append((scr,f"Btn Doctor {d[1]}","P1-profile"))
        TRN.append((scr,f"Btn Book {d[1]}","B1-slot"))
for ic,label in SPECIALTIES:
    for scr in ("H1-home","H2-home-empty"):
        TRN.append((scr,f"Btn Specialty {label}","S1-results"))

resolved=[]
for a,hot,b in TRN:
    if a in NAMES and b in NAMES:
        resolved.append([NAMES[a][0],hot,NAMES[b][0]]); resolved.append([NAMES[a][1],hot,NAMES[b][1]])
member_ids=[f for f in ORDER.get("Member",[])]
order_js={PAGE_FIGMA["Member"]:[[NAMES[f][0],NAMES[f][1]] for f in member_ids]}
starts_js={PAGE_FIGMA["Member"]:NAMES["H1-home"][0]}

# motion: per-transition easing/duration so the prototype feels designed
MOTION=json.dumps({
  "default":  {"type":"SMART_ANIMATE","easing":"GENTLE","duration":0.28},
  "sheet":    {"type":"MOVE_IN","direction":"BOTTOM","easing":"GENTLE","duration":0.32},
  "sheetOut": {"type":"MOVE_OUT","direction":"BOTTOM","easing":"EASE_IN","duration":0.24},
})
SHEETS=json.dumps(["Btn Filters","Btn Sort"])
SHEET_CLOSE=json.dumps(["Btn Close filters","Btn Apply filters","Btn Reset filters"])

linker=("(async () => {\n"
 "  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();\n"
 "  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();\n"
 "  const pages = figma.root.children.filter(n => n.type==='PAGE');\n"
 "  const byName = {}; for (const pg of pages) for (const f of pg.children) if (f.type==='FRAME') byName[norm(f.name)] = f;\n"
 "  const F = n => byName[norm(n)];\n"
 "  const findAll = (root,t) => { const out=[]; const target=norm(t); const w=n=>{ if(n.name&&norm(n.name)===target) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 f"  const M = {MOTION};\n"
 f"  const SHEETS = {SHEETS}, SHEET_CLOSE = {SHEET_CLOSE};\n"
 "  const ease = e => ({ type: e });\n"
 "  const mk = spec => spec.type==='SMART_ANIMATE'\n"
 "    ? { type:'SMART_ANIMATE', easing:ease(spec.easing), duration:spec.duration }\n"
 "    : { type:spec.type, direction:spec.direction, matchLayers:false, easing:ease(spec.easing), duration:spec.duration };\n"
 f"  const TRN = {json.dumps(resolved)};\n"
 f"  const ORDER = {json.dumps(order_js)};\n"
 f"  const STARTS = {json.dumps(starts_js)};\n"
 "  const jobs=[], missing=[];\n"
 "  for (const [fromN,hot,toN] of TRN){ const fr=F(fromN), to=F(toN); if(!fr||!to) continue;\n"
 "    const nodes=findAll(fr,hot); if(!nodes.length){ missing.push(fromN+' -> '+hot); continue; }\n"
 "    let spec = M.default;\n"
 "    if (SHEETS.includes(hot)) spec = M.sheet;\n"
 "    else if (SHEET_CLOSE.includes(hot)) spec = M.sheetOut;\n"
 "    for (const nd of nodes) jobs.push([nd,to,spec]); }\n"
 "  let linked=0;\n"
 "  for (const [nd,to,spec] of jobs){\n"
 "    await nd.setReactionsAsync([{ trigger:{type:'ON_CLICK'}, actions:[{ type:'NODE', destinationId:to.id, navigation:'NAVIGATE', transition: mk(spec) }] }]);\n"
 "    linked++; }\n"
 "  const GX=170, GY=150;\n"
 "  for (const pg of pages){ const ord=ORDER[pg.name]; if(!ord) continue; let x=0, rowH=0;\n"
 "    for (const [dn,mn] of ord){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const [dn,mn] of ord){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(s&&F(s)) pg.flowStartingPoints=[{ nodeId:F(s).id, name:'Find & book' }]; }\n"
 "  // close the auth dead-end: every auth success lands on the member home\n"
 "  const home = F(" + json.dumps(NAMES['H1-home'][0]) + "), homeM = F(" + json.dumps(NAMES['H1-home'][1]) + ");\n"
 "  const AUTH=[['Auth · Member — M9 Success','Btn Go home M9'],['Auth · Member — M9 Success · Mobile','Btn Go home M9'],\n"
 "              ['Auth · Member — M7 Quick Unlock','Btn Unlock M7'],['Auth · Member — M7 Quick Unlock · Mobile','Btn Unlock M7']];\n"
 "  for (const [fn,hot] of AUTH){ const fr=F(fn); if(!fr) continue; const dest = fn.includes('Mobile')?homeM:home; if(!dest) continue;\n"
 "    for (const nd of findAll(fr,hot)) { await nd.setReactionsAsync([{ trigger:{type:'ON_CLICK'}, actions:[{ type:'NODE', destinationId:dest.id, navigation:'NAVIGATE', transition: mk(M.default) }] }]); linked++; } }\n"
 "  return { linked, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT,"link-member.js"),"w").write(linker)

ps=["# Medra Member app — render + wire (Figma Desktop open + connected).",
    'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
    'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
    "figma-cli tokens import-design-md .\\DESIGN.md",""]
for p,fids in ORDER.items():
    pg=PAGE_FIGMA[p].replace("&amp;","&")
    ps.append(f'# ---- {pg} ----')
    ps.append(f'figma-cli eval "(async()=>{{const t=\'{pg}\';let p=figma.root.children.find(n=>n.name===t);if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"')
    if p=="Components":
        lst=", ".join("'"+f+".jsx'" for f in fids)
    else:
        lst=", ".join("'"+f+"'" for fid in fids for f in (fid+"-d.jsx",fid+"-m.jsx"))
    ps.append(f'foreach ($f in @({lst})) {{ figma-cli render (Get-Content $f -Raw) }}')
    ps.append("")
ps.append("# Turn the cmp/* frames into real interactive components (variants + hover/press)")
ps.append("figma-cli run .\\components-medra.js")
ps.append("")
ps.append("# Wire the prototype with motion + arrange the canvas")
ps.append("figma-cli run .\\link-member.js")
open(os.path.join(OUT,"render-member.ps1"),"w").write("\n".join(ps))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} links")
for p,fs in manifest.items(): print(f"  {p}: {len(fs)}")
