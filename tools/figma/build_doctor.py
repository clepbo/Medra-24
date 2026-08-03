#!/usr/bin/env python3
"""Medra — Doctor app, batch 1.

Built from the 1 August product review, where the doctor flow was asked to be "much more
robust". The spine is: see today's queue → read the file before you walk in → consult and write
the note as you go → decide what the patient sees → sign it. Everything else (schedule, fees,
meeting links, contact channels, earnings) exists to serve that spine.

23 screens × desktop 1440 + mobile 390 = 46 frames, plus the doctor component states.
"""
import os, re, json, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from doctor_kit import *

OUT = "/home/user/Medra-24/figma/medra-doctor"
os.makedirs(OUT, exist_ok=True)

frames = []; NAMES = {}; ORDER = {}
def add(page, fid, d, m):
    frames.append((page, f"{fid}-d.jsx", d)); frames.append((page, f"{fid}-m.jsx", m))
    NAMES[fid] = (re.search(r'name="([^"]+)"', d).group(1), re.search(r'name="([^"]+)"', m).group(1))
    ORDER.setdefault(page, []).append(fid)

PAGE_FIGMA = {
  "Today":        "Medra Doctor — Today &amp; Schedule",
  "Consultation": "Medra Doctor — Consultation",
  "Patients":     "Medra Doctor — Patients",
  "Practice":     "Medra Doctor — Practice &amp; Earnings",
  "States":       "Medra Doctor — States",
  "Components":   "Medra Doctor — Components",
}
SIDE = {"Today": 0, "Schedule": 1, "Patients": 2, "Notes": 3, "Earnings": 4, "Settings": 5}
TAB  = {"Today": 0, "Schedule": 1, "Patients": 2, "Earnings": 3, "Settings": 4}

# =====================================================================================
# TODAY & SCHEDULE
# =====================================================================================
K_STATS = rows_of([
    stat_card("users", "8", "Patients today", "3 seen, 5 to go", "tint-teal.jpg"),
    stat_card("clock", "6 min", "Median wait", "Better than last week", "tint-mint.jpg"),
    stat_card("video", "5", "Virtual", "3 in person", "tint-ocean.jpg"),
    stat_card("banknote", "₦96,000", "Earned today", "Paid out Friday", "tint-navy.jpg"),
], 4, 16)

NOW = now_card("avatar-2.jpg", "Amara Okeke", "34 years · MDR-8842-19 · seen 3 times",
               "Hypertension follow-up. Home readings around 138/88 for two weeks.", "10:30")

QUEUE = (queue_row("11:00", "avatar-6.jpg", "Chidi Okeke", "6 years · MDR-8842-20 · guardian: Amara Okeke",
                   "Cough for four days, no fever", "confirmed", "In person", "Q Chidi")
         + queue_row("11:30", "avatar-1.jpg", "Musa Ibrahim", "51 years · MDR-7714-02 · first visit",
                     "Chest tightness when climbing stairs", "confirmed", "Virtual", "Q Musa")
         + queue_row("12:00", "avatar-3.jpg", "Grace Okeke", "68 years · MDR-8842-21 · diabetes, hypertension",
                     "Review after blood sugar test", "confirmed", "In person", "Q Grace")
         + queue_row("14:00", "avatar-5.jpg", "Tunde Bello", "44 years · MDR-6620-88",
                     "Results discussion", "pending", "Virtual", "Q Tunde"))

K_ATTENTION = group_card("Needs you", [
    list_row("flask-conical", "3 results waiting to be released", sub="Musa Ibrahim, Grace Okeke, Amara Okeke", name="Open results", tint="var:state/warning-bg"),
    list_row("package", "2 refill requests", sub="Oldest is 19 hours old — members are told you reply within a day", name="Open refills", tint="var:state/warning-bg"),
    list_row("notebook-pen", "1 unsigned note", sub="Yesterday, 16:40 — the patient cannot see it until you sign", name="Open unsigned", tint="var:state/error-bg"),
], footer="Anything here is blocking a patient. Everything else can wait until after clinic.")

K_TIMELINE = group_card("Rest of the day", [
    list_row("coffee", "13:00 — Break", value="1 hour", sub="Blocked, nobody can book it", name="Break row", chevron=False),
    list_row("video", "14:00 — Tunde Bello", value="Virtual", sub="Awaiting his payment — slot released at 13:30 if unpaid", name="Q Tunde"),
    list_row("circle-plus", "15:00 — Open", sub="Bookable right now", name="Open slot 15", chevron=False),
    list_row("circle-plus", "15:30 — Open", sub="Bookable right now", name="Open slot 1530", chevron=False),
])

add("Today", "K1-today",
    dr_desk("Doctor · Today — K1 Queue",
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{NOW}{K_STATS}'
        f'<Frame w="fill" flex="col" gap={{11}}>'
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{T(17,"bold","var:text/strong","Waiting")}'
        f'{mini_btn("See the whole week","Nav Schedule","calendar-days","ghost",grow=False)}</Frame>'
        f'{QUEUE}</Frame></Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{K_ATTENTION}{K_TIMELINE}</Frame></Frame>',
        SIDE["Today"]),
    dr_mob("Doctor · Today — K1 Queue · Mobile",
        dr_greet()
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{NOW}'
          f'<Frame w="fill" flex="row" justify="between" items="center">'
          f'{T(16,"bold","var:text/strong","Waiting")}'
          f'{T(12,"regular","var:text/muted","5 more today")}</Frame>'
          f'{queue_row_m("11:00","avatar-6.jpg","Chidi Okeke","6 years · MDR-8842-20","Cough for four days, no fever","confirmed","In person","Q Chidi")}'
          f'{queue_row_m("11:30","avatar-1.jpg","Musa Ibrahim","51 years · first visit","Chest tightness on stairs","confirmed","Virtual","Q Musa")}'
          f'</Frame>',
        nav=dr_bottom_nav(TAB["Today"])))

# ---------------- K2 appointments
K2_TABS = tabs(["Today", "This week", "Past"], 1, "Appt tab")
K2_FILTERS = rows_of([
    mini_btn("All", "Filter appt all", None, "navy"),
    mini_btn("Virtual", "Filter appt virtual", "video", "ghost"),
    mini_btn("In person", "Filter appt person", "hospital", "ghost"),
    mini_btn("Unpaid", "Filter appt unpaid", "credit-card", "ghost"),
], 4, 9)

WEEK = (f'<Frame w="fill" flex="row" gap={{10}} items="start">'
        + day_col("Mon", "18", [slot_chip("09:00", "booked"), slot_chip("09:30", "booked"),
                                slot_chip("10:00", "open"), slot_chip("10:30", "open")])
        + day_col("Tue", "19", [slot_chip("09:00", "booked"), slot_chip("09:30", "open"),
                                slot_chip("10:00", "booked"), slot_chip("10:30", "booked")])
        + day_col("Wed", "20", [slot_chip("09:00", "open"), slot_chip("09:30", "booked"),
                                slot_chip("10:00", "booked"), slot_chip("10:30", "break")])
        + day_col("Thu", "21", [slot_chip("09:00", "booked"), slot_chip("09:30", "booked"),
                                slot_chip("10:00", "booked"), slot_chip("10:30", "booked")], today=True)
        + day_col("Fri", "22", [slot_chip("09:00", "blocked"), slot_chip("09:30", "blocked"),
                                slot_chip("10:00", "blocked"), slot_chip("10:30", "blocked")])
        + day_col("Sat", "23", [slot_chip("10:00", "open"), slot_chip("10:30", "open"),
                                slot_chip("11:00", "open"), slot_chip("11:30", "open")])
        + '</Frame>')

K2_LEGEND = (f'<Frame w="fill" flex="row" gap={{18}} items="center">'
             f'<Frame flex="row" gap={{7}} items="center"><Rect w={{12}} h={{12}} rounded={{4}} image="assets/img/btn-navy.jpg" overflow="hidden" />'
             f'{T(11,"regular","var:text/muted","Booked")}</Frame>'
             f'<Frame flex="row" gap={{7}} items="center"><Rect w={{12}} h={{12}} rounded={{4}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}} />'
             f'{T(11,"regular","var:text/muted","Open")}</Frame>'
             f'<Frame flex="row" gap={{7}} items="center"><Rect w={{12}} h={{12}} rounded={{4}} bg="var:state/warning-bg" />'
             f'{T(11,"regular","var:text/muted","Break")}</Frame>'
             f'<Frame flex="row" gap={{7}} items="center"><Rect w={{12}} h={{12}} rounded={{4}} bg="var:neutral/100" />'
             f'{T(11,"regular","var:text/muted","Blocked — you are away")}</Frame></Frame>')

add("Today", "K2-appointments",
    dr_desk("Doctor · Schedule — K2 Week",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{head_chip([("Week of",False),("18 August",True)],28)}'
        f'<Frame flex="row" gap={{10}} items="center">'
        f'{mini_btn("Block time off","Open timeoff K5","calendar-x","ghost",grow=False)}'
        f'{mini_btn("Edit my hours","Open availability K4","clock","navy",grow=False)}</Frame></Frame>'
        f'{K2_TABS}{K2_FILTERS}'
        f'{group_card("", [WEEK, K2_LEGEND], p=20)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{11}}>{T(16,"bold","var:text/strong","Thursday 21 August")}{QUEUE}</Frame>'
        f'<Frame w={{340}} flex="col" gap={{16}}>'
        f'{group_card("This week", [list_row("calendar-check","Booked",value="24",name="W booked",chevron=False),list_row("circle-plus","Still open",value="9",name="W open",chevron=False),list_row("circle-x","Cancelled",value="2",sub="Both more than a day ahead",name="W cancelled",chevron=False),list_row("circle-slash","No-shows",value="1",sub="Musa Ibrahim, 12 Aug",name="W noshow",chevron=False)])}'
        f'{alert_strip("triangle-alert","Friday is fully blocked","You marked 22 August as time off. Nobody can book it — undo from “Block time off”.","warn")}</Frame></Frame>',
        SIDE["Schedule"]),
    dr_mob("Doctor · Schedule — K2 Week · Mobile",
        dr_appbar("Schedule", back=False, right=circle_btn("calendar-x", "Open timeoff K5"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{K2_TABS}{date_strip(3)}'
          f'{T(15,"semibold","var:text/default","Thursday 21 August")}'
          f'{queue_row_m("11:00","avatar-6.jpg","Chidi Okeke","6 years · MDR-8842-20","Cough for four days","confirmed","In person","Q Chidi")}'
          f'{queue_row_m("11:30","avatar-1.jpg","Musa Ibrahim","51 years · first visit","Chest tightness","confirmed","Virtual","Q Musa")}'
          f'{queue_row_m("12:00","avatar-3.jpg","Grace Okeke","68 years · diabetes","Blood sugar review","confirmed","In person","Q Grace")}</Frame>',
        nav=dr_bottom_nav(TAB["Schedule"])))

# ---------------- K3 appointment detail / read the file first
def stat_cell_dr(ic, big, small):
    return (f'<Frame grow={{1}} flex="col" gap={{4}} items="center" py={{13}} px={{8}} rounded={{18}} bg="var:bg/subtle">'
            f'{I(ic,16,A_IC)}{T(14,"bold","var:text/strong",big)}{T(11,"regular","var:text/muted",small)}</Frame>')

K3_HEAD = (f'<Frame w="fill" flex="col" gap={{15}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" justify="between" items="center">{status_pill("soon","Starts in 6 minutes")}'
           f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:state/info-bg">'
           f'{I("video",12,A_IC)}{T(11,"medium","var:text/default","Virtual")}</Frame></Frame>'
           f'<Frame w="fill" flex="row" gap={{15}} items="center">'
           f'<Image image="assets/img/avatar-2.jpg" w={{68}} h={{68}} rounded={{22}} />'
           f'<Frame grow={{1}} flex="col" gap={{4}}>{T(20,"bold","var:text/strong","Amara Okeke")}'
           f'<Frame flex="row" gap={{9}} items="center">'
           f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="var:bg/muted">'
           f'{T(11,"semibold","var:text/accent","MDR-8842-19")}</Frame>'
           f'{T(13,"regular","var:text/muted","34 years · female · Garki, Abuja")}</Frame></Frame>'
           f'{mini_btn("Open full record","Open record T2","clipboard-list","ghost",grow=False)}</Frame>'
           f'<Frame w="fill" flex="row" gap={{10}}>'
           f'{stat_cell_dr("droplet","O+","Blood group")}{stat_cell_dr("activity","AA","Genotype")}'
           f'{stat_cell_dr("weight","74 kg","Weight")}{stat_cell_dr("history","3","Visits with you")}</Frame></Frame>')

K3_HEAD_M = (f'<Frame w="fill" flex="col" gap={{13}} p={{16}} rounded={{24}} bg="var:bg/base" '
             f'stroke="var:border/subtle" strokeWidth={{1}}>'
             f'<Frame w="fill" flex="row" justify="between" items="center">{status_pill("soon","In 6 minutes")}'
             f'<Frame flex="row" gap={{6}} items="center" px={{10}} py={{5}} rounded={{999}} bg="var:state/info-bg">'
             f'{I("video",11,A_IC)}{T(10,"medium","var:text/default","Virtual")}</Frame></Frame>'
             f'<Frame w="fill" flex="row" gap={{13}} items="center">'
             f'<Image image="assets/img/avatar-2.jpg" w={{54}} h={{54}} rounded={{18}} />'
             f'<Frame grow={{1}} flex="col" gap={{3}}>{T(17,"bold","var:text/strong","Amara Okeke")}'
             f'<Frame flex="row" px={{8}} py={{3}} rounded={{7}} bg="var:bg/muted">'
             f'{T(10,"semibold","var:text/accent","MDR-8842-19")}</Frame>'
             f'{T(11,"regular","var:text/muted","34 · female · O+ · AA",w="fill")}</Frame></Frame></Frame>')

K3_SAFETY = alert_strip("triangle-alert", "Allergic to penicillin",
    "Reaction: rash and swelling, recorded Jun 2026. Medra blocks a penicillin prescription for this patient — you can override with a reason.", "err")

K3_REASON = group_card("Why they are coming", [
    note_section("In their words", "“Hypertension follow-up. My home readings have been around 138/88 for two weeks and I get headaches in the afternoon.”", "message-square-text"),
    note_section("They also told you", "“There is something in my history from 2019 I have kept off my record — I would rather explain it on the call.”", "notebook-pen"),
], footer="Members choose what history to share. If something is missing, ask — and it is recorded that you asked.")

K3_SHARED = group_card("What Amara has shared with you", [
    scope_line("Allergies and current medicines", True, "Always shared — clinical safety"),
    scope_line("Consultation notes", True, "All 8 visits, including other clinics"),
    scope_line("Lab results", True, "4 results · 1 outside the normal range"),
    scope_line("Prescription history", False, "Not shared — you can ask"),
    scope_line("Home vitals", False, "Not shared — you can ask"),
], footer="Access ends when this visit is marked complete. Every record you open is logged and visible to the patient.")

K3_LAST = group_card("Last time you saw her", [
    list_row("stethoscope", "Hypertension review", value="12 Jun 2026", sub="Partially controlled, no organ damage", name="Open note last"),
    list_row("pill", "Amlodipine 5 mg", value="96% taken", sub="She has been consistent — adherence is not the issue", name="Open adherence"),
    list_row("flask-conical", "Fasting blood sugar", value="Not done", sub="You ordered it in June and it is still outstanding", name="Open outstanding", tint="var:state/warning-bg"),
])

add("Today", "K3-appointment",
    dr_desk("Doctor · Today — K3 Read the File",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Today’s queue")}</Frame>'
        f'<Frame flex="row" gap={{10}} items="center">'
        f'{mini_btn("Ask for more history","Open access T3","message-square-text","ghost",grow=False)}'
        f'{mini_btn("Start consultation","Start consult","stethoscope","navy",grow=False)}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{K3_HEAD}{K3_SAFETY}{K3_REASON}{K3_LAST}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{K3_SHARED}'
        f'{group_card("The visit", [list_row("calendar-days","Thursday, 21 August",value="10:30",name="K3 when",chevron=False),list_row("clock","30 minutes",sub="Your standard follow-up length",name="K3 length",chevron=False),list_row("credit-card","₦15,000",value="Paid",sub="Paystack ref PSK-99417-C · 14 Aug",name="K3 paid",chevron=False),list_row("video","Google Meet",sub="meet.google.com/kfa-jrqz-nmo",name="Open meeting")])}'
        f'{dcta("Start consultation","Start consult","stethoscope")}</Frame></Frame>',
        SIDE["Today"]),
    dr_mob("Doctor · Today — K3 Read the File · Mobile",
        dr_appbar("Before you start")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{K3_HEAD_M}{K3_SAFETY}'
          f'{group_card("Why they are coming", [note_section("In their words","“Hypertension follow-up. Home readings around 138/88 for two weeks, with afternoon headaches.”","message-square-text")], p=16)}'
          f'<Frame grow={{1}} />{dcta("Start consultation","Start consult","stethoscope")}</Frame>'))

# ---------------- K4 availability
K4_DAYS = group_card("Your working week", [
    toggle_row("calendar-days", "Monday", sub="09:00 – 17:00 · 30-minute slots", on=True, name="Day mon"),
    toggle_row("calendar-days", "Tuesday", sub="09:00 – 17:00 · 30-minute slots", on=True, name="Day tue"),
    toggle_row("calendar-days", "Wednesday", sub="09:00 – 13:00 · theatre in the afternoon", on=True, name="Day wed"),
    toggle_row("calendar-days", "Thursday", sub="09:00 – 17:00 · 30-minute slots", on=True, name="Day thu"),
    toggle_row("calendar-days", "Friday", sub="Not working", on=False, name="Day fri"),
    toggle_row("calendar-days", "Saturday", sub="10:00 – 14:00 · virtual only", on=True, name="Day sat"),
    toggle_row("calendar-days", "Sunday", sub="Not working", on=False, name="Day sun"),
])
K4_RULES = group_card("Booking rules", [
    list_row("clock", "Slot length", value="30 minutes", sub="Set a different length per consultation type in Fees", name="Open fees S2"),
    list_row("hourglass", "Gap between patients", value="0 minutes", sub="Add a buffer if you run over often", name="Rule buffer"),
    list_row("calendar-clock", "How far ahead can people book?", value="8 weeks", name="Rule horizon"),
    list_row("timer", "Latest a same-day booking is allowed", value="2 hours before", name="Rule cutoff"),
    list_row("users", "Maximum patients a day", value="12", sub="Medra stops offering slots once you hit this", name="Rule cap"),
], footer="These rules are what members see as “real availability”. If a slot shows on Medra, it is genuinely open.")
K4_BREAKS = group_card("Breaks", [
    list_row("coffee", "13:00 – 14:00", value="Every working day", sub="Nobody can book it", name="Break daily"),
    list_row("plus", "Add another break", name="Add break", chevron=False),
])

add("Today", "K4-availability",
    dr_desk("Doctor · Schedule — K4 Availability",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{head_chip([("When you are",False),("available",True)],28)}'
        f'{mini_btn("Save changes","Save availability K4","check","navy",grow=False)}</Frame>'
        f'{T(15,"regular","var:text/muted","Change this and the open slots on Medra change with it. Booked appointments are never touched.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{K4_DAYS}{K4_BREAKS}</Frame>'
        f'<Frame w={{400}} flex="col" gap={{16}}>{K4_RULES}'
        f'{alert_strip("info","4 people have booked Friday 29 August","Turning Friday off will not cancel them. Move or cancel each one yourself so they hear it from you.","info")}</Frame></Frame>',
        SIDE["Schedule"]),
    dr_mob("Doctor · Schedule — K4 Availability · Mobile",
        dr_appbar("Availability", right=circle_btn("check", "Save availability K4"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{K4_DAYS}</Frame>',
        nav=dr_bottom_nav(TAB["Schedule"])))

# ---------------- K5 time off
K5_FORM = (f'{field_chips("What is this?", ["Leave", "Conference", "Theatre list", "Personal"], 0, "Timeoff type")}'
           f'<Frame w="fill" flex="row" gap={{14}}>'
           f'<Frame grow={{1}} flex="col">{field("From","calendar-days","Fri, 22 August",ph=False)}</Frame>'
           f'<Frame grow={{1}} flex="col">{field("To","calendar-days","Fri, 22 August",ph=False)}</Frame></Frame>'
           f'{checkbox("All day","Timeoff allday")}'
           f'{field("Note for your own records (optional)","message-square-text","Cardiology conference in Lagos")}')
K5_IMPACT = group_card("What this affects", [
    list_row("calendar-x", "9 open slots close", sub="Nobody can book Friday 22 August", name="Impact slots", chevron=False),
    list_row("users", "4 patients already booked", sub="They are not cancelled — decide for each one below", name="Impact booked", tint="var:state/warning-bg", chevron=False),
    list_row("message-circle", "We can message them for you", sub="WhatsApp and SMS, with your next open times", name="Impact message", chevron=False),
], footer="Medra will never cancel a patient on your behalf without you choosing it here.")
K5_AFFECTED = group_card("The four already booked", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "Fri 22 Aug · 09:00 · virtual", "12 Jun", "Move Amara"),
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "Fri 22 Aug · 09:30 · in person", "12 Jun", "Move Chidi"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "Fri 22 Aug · 11:00 · virtual", "First visit", "Move Musa"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "Fri 22 Aug · 14:00 · in person", "28 Apr", "Move Grace"),
])

add("Today", "K5-timeoff",
    dr_desk("Doctor · Schedule — K5 Time Off",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Schedule")}</Frame>'
        f'{head_chip([("Block time",False),("off",True)],28)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{K5_FORM}{K5_AFFECTED}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{K5_IMPACT}'
        f'{dcta("Block this time","Save timeoff K5","calendar-x")}'
        f'{mini_btn("Offer everyone my next open slot","Offer slots K5","repeat","ghost",full=True)}</Frame></Frame>',
        SIDE["Schedule"]),
    dr_mob("Doctor · Schedule — K5 Time Off · Mobile",
        dr_appbar("Time off")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{K5_FORM}'
          f'{group_card("What this affects", [list_row("calendar-x","9 open slots close",name="Impact slots",chevron=False),list_row("users","4 patients already booked",sub="Decide for each one",name="Impact booked",tint="var:state/warning-bg",chevron=False)], p=16)}'
          f'<Frame grow={{1}} />'
          f'{dcta("Block this time","Save timeoff K5","calendar-x")}</Frame>'))

# =====================================================================================
# CONSULTATION — the spine of the doctor app
# =====================================================================================
C_PATIENT_STRIP = (f'<Frame w="fill" flex="row" gap={{14}} items="center" p={{16}} rounded={{22}} '
                   f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
                   f'<Image image="assets/img/avatar-2.jpg" w={{48}} h={{48}} rounded={{16}} />'
                   f'<Frame grow={{1}} flex="col" gap={{3}}>'
                   f'<Frame flex="row" gap={{9}} items="center">{T(16,"semibold","var:text/strong","Amara Okeke")}'
                   f'<Frame flex="row" px={{9}} py={{3}} rounded={{7}} bg="var:bg/muted">'
                   f'{T(10,"semibold","var:text/accent","MDR-8842-19")}</Frame></Frame>'
                   f'{T(12,"regular","var:text/muted","34 · O+ · AA · allergic to penicillin · hypertension",w="fill")}</Frame>'
                   f'<Frame flex="row" gap={{8}} items="center" px={{12}} py={{8}} rounded={{999}} bg="var:state/error-bg">'
                   f'<Ellipse w={{8}} h={{8}} bg="#D14343" />{T(12,"semibold","var:state/error","12:04")}</Frame>'
                   f'{mini_btn("Open the call","Open meeting","video","navy",grow=False)}</Frame>')

C_TABS   = tabs(["Note", "Prescription", "Tests", "Files"], 0, "Consult tab")
C_TABS_M = tabs(["Note", "Rx", "Tests", "Files"], 0, "Consult tab", size=14)

C_NOTE_FIELDS = (note_field("Why they came", "message-square-text",
    "Hypertension follow-up. Home readings 138/88 for two weeks, afternoon headaches. No chest pain, no breathlessness, no ankle swelling.", "reason")
    + note_field("Examination", "stethoscope",
        "BP 136/86 seated, repeated 134/84. Pulse 78 regular. Weight 74 kg. Heart sounds normal, chest clear, no oedema.", "exam", lines=2)
    + note_field("Assessment", "clipboard-check",
        "Hypertension, partially controlled. No evidence of end-organ damage. Headaches likely tension-type rather than hypertensive.", "assessment", lines=2)
    + note_field("Plan", "list-checks",
        "Continue Amlodipine 5 mg mane. Reduce added salt. 30 minutes walking, five days a week. Fasting blood sugar before next review. Review in 3 months, sooner if BP > 160/100.", "plan", lines=3))

C_AI = (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{15}} rounded={{20}} bg="var:bg/muted">'
        f'{I("sparkles",18,A_IC)}'
        f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong","Transcribe this consultation")}'
        f'{T(11,"regular","var:text/muted","Phase 2 — Medra listens and drafts the note, you edit and sign. Nothing is stored without the patient agreeing first.",w="fill")}</Frame>'
        f'<Frame flex="row" px={{10}} py={{5}} rounded={{999}} bg="var:state/warning-bg">'
        f'{T(10,"semibold","var:state/warning","PHASE 2")}</Frame></Frame>')

C_HISTORY_ASK = (f'<Frame w="fill" flex="col" gap={{11}} p={{18}} rounded={{22}} bg="var:state/info-bg">'
                 f'<Frame flex="row" gap={{9}} items="center">{I("notebook-pen",17,A_IC)}'
                 f'{T(14,"semibold","var:text/strong","She said something is missing from her record")}</Frame>'
                 f'{T(13,"regular","var:text/default","“There is something in my history from 2019 I have kept off my record.” Ask about it, and record what you were told — or that you were told nothing.",w="fill")}'
                 f'{note_field("What she told you on the call","message-circle","Treated for a thyroid condition in 2019 at a private clinic in Enugu. No records available. Says it resolved and she takes nothing for it now.","undisclosed",lines=2)}'
                 f'{checkbox("She declined to give more detail","Declined detail",checked=False)}'
                 f'{T(11,"regular","var:text/muted","This is stored with the consultation, so it is clear later what you were and were not told.",w="fill")}</Frame>')

C_SIDE = group_card("While you talk", [
    list_row("triangle-alert", "Allergic to penicillin", sub="Rash and swelling · Jun 2026", name="Side allergy", tint="var:state/warning-bg", chevron=False),
    list_row("pill", "On Amlodipine 5 mg", sub="96% taken on time over 30 days", name="Side meds"),
    list_row("activity", "BP trend", sub="142/92 in March down to 128/82 this month", name="Side vitals"),
    list_row("flask-conical", "Outstanding test", sub="Fasting blood sugar, ordered 12 Jun, never done", name="Side outstanding", tint="var:state/warning-bg"),
    list_row("history", "Previous notes", value="8", sub="3 with you, 5 at other clinics", name="Side notes"),
])

add("Consultation", "C1-room",
    dr_desk("Doctor · Consultation — C1 In Progress",
        f'{C_PATIENT_STRIP}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{C_TABS}{C_AI}'
        f'{group_card("Consultation note", [C_NOTE_FIELDS], p=20)}'
        f'{C_HISTORY_ASK}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{C_SIDE}'
        f'{group_card("Add to this visit", [list_row("pill","Prescribe a medicine",name="Open prescribe C3"),list_row("flask-conical","Order a test",name="Open tests C4"),list_row("upload","Attach a file or result",name="Open upload C5"),list_row("calendar-plus","Book the follow-up now",name="Book followup")])}'
        f'{dcta("Finish and review","Open sign C6","arrow-right")}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C1 In Progress · Mobile",
        dr_appbar("Consultation", right=circle_btn("video", "Open meeting"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{patient_strip_m()}{C_TABS_M}'
          f'{note_field("Assessment","clipboard-check","Hypertension, partially controlled. No end-organ damage.","assessment",lines=2)}'
          f'{note_field("Plan","list-checks","Continue Amlodipine 5 mg mane. Fasting blood sugar. Review in 3 months.","plan",lines=2)}'
          f'<Frame grow={{1}} />{dcta("Finish and review","Open sign C6","arrow-right")}</Frame>'))

# ---------------- C2 note templates
C2_TEMPLATES = group_card("Your templates", [
    list_row("file-text", "Hypertension follow-up", sub="Used 42 times · exam, assessment and plan pre-filled", name="Use template hyp"),
    list_row("file-text", "New patient — cardiology", sub="Used 18 times", name="Use template new"),
    list_row("file-text", "Post-discharge review", sub="Used 7 times", name="Use template discharge"),
    list_row("file-text", "Paediatric fever", sub="Shared by Garki Medical Centre", name="Use template fever"),
    list_row("plus", "Save this note as a template", sub="Strip the patient details, keep the structure", name="Save template", chevron=False),
], footer="Templates only fill the boxes. Nothing is submitted for you, and every note still needs your signature.")
C2_PREVIEW = group_card("Hypertension follow-up", [
    note_section("Why they came", "Hypertension follow-up. Home readings [__/__] for [__]. Symptoms: [headache / chest pain / breathlessness / ankle swelling / none].", "message-square-text"),
    note_section("Examination", "BP [__/__] seated, repeated [__/__]. Pulse [__] regular. Weight [__] kg. Heart sounds [__], chest [__], oedema [__].", "stethoscope"),
    note_section("Assessment", "Hypertension, [controlled / partially controlled / uncontrolled]. [Evidence / no evidence] of end-organ damage.", "clipboard-check"),
    note_section("Plan", "Continue [__]. Salt reduction. Exercise [__]. Tests: [__]. Review in [__].", "list-checks"),
])

add("Consultation", "C2-templates",
    dr_desk("Doctor · Consultation — C2 Note Templates",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Consultation")}</Frame>'
        f'{head_chip([("Write less,",False),("say more",True)],28)}'
        f'{T(15,"regular","var:text/muted","A template fills the structure so your typing goes into what is actually different about this patient.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{C2_TEMPLATES}</Frame>'
        f'<Frame w={{440}} flex="col" gap={{16}}>{eyebrow("PREVIEW")}{C2_PREVIEW}'
        f'{dcta("Use this template","Use template hyp","check")}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C2 Note Templates · Mobile",
        dr_appbar("Templates")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{C2_TEMPLATES}<Frame grow={{1}} />'
          f'{dcta("Use this template","Use template hyp","check")}</Frame>'))

# ---------------- C3 prescribe
# "unless there's an open API with the name of drugs and the details ... they can just search"
C3_SEARCH = (f'{field("Search a medicine","search","amlod",ph=False,focus=True,helper="From the Nigerian essential medicines list plus the NAFDAC register — type three letters.")}'
             f'<Frame w="fill" flex="col" gap={{9}}>'
             f'{drug_result("Amlodipine","Tablet · 5 mg, 10 mg","Calcium channel blocker","Pick amlodipine")}'
             f'{drug_result("Amlodipine / Valsartan","Tablet · 5/80 mg, 10/160 mg","Combination","Pick amlodval")}'
             f'{drug_result("Amoxicillin","Capsule · 250 mg, 500 mg","Penicillin — patient is allergic","Pick amoxicillin")}</Frame>')
C3_BLOCK = alert_strip("triangle-alert", "Amoxicillin is blocked for this patient",
    "Amara is allergic to penicillin — rash and swelling, recorded June 2026. Prescribing it needs a written reason and is flagged to the clinic.", "err")
C3_BUILDER = group_card("Amlodipine", [
    f'<Frame w="fill" flex="row" gap={{14}}>'
    + f'<Frame grow={{1}} flex="col">{field("Strength","pill","5 mg",ph=False,trailing=("chevron-down","Strength dropdown"))}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Form","package","Tablet",ph=False,trailing=("chevron-down","Form dropdown"))}</Frame></Frame>',
    field_chips("How often", ["Once daily", "Twice daily", "Three times", "As needed"], 0, "Rx freq"),
    field_chips("When", ["Morning", "Night", "With food", "Any time"], 0, "Rx when"),
    f'<Frame w="fill" flex="row" gap={{14}}>'
    + f'<Frame grow={{1}} flex="col">{stepper_ctl("Days",30,"Rx days")}</Frame>'
    + f'<Frame grow={{1}} flex="col">{stepper_ctl("Refills allowed",2,"Rx refills")}</Frame></Frame>',
    field("Instructions the patient will see", "message-square-text", "One tablet every morning with water. Do not stop without speaking to me.", ph=False),
], footer="This is written in plain language on the member's phone, with a reminder at the time you set.")
C3_CURRENT = group_card("On this prescription", [
    rx_line("Amlodipine", "5 mg", "Once daily, morning", "30 days", "rx1"),
    rx_line("Metformin", "500 mg", "Once daily, evening", "30 days", "rx2"),
], footer="Both go to the member's Medicines tab and to Garki pharmacy the moment you sign.")

add("Consultation", "C3-prescribe",
    dr_desk("Doctor · Consultation — C3 Prescribe",
        f'{C_PATIENT_STRIP}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{C3_SEARCH}{C3_BLOCK}{C3_BUILDER}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{C3_CURRENT}'
        f'{group_card("Already taking", [list_row("pill","Vitamin D 1000 IU",sub="Over the counter · not prescribed by you",name="Cur vitd",chevron=False),list_row("shield-check","No interactions found",sub="Checked against everything on her record",name="Cur interactions",tint="var:state/success-bg",chevron=False)])}'
        f'{dcta("Add to the visit","Open sign C6","check")}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C3 Prescribe · Mobile",
        dr_appbar("Prescribe")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{patient_strip_m()}'
          f'{field("Search a medicine","search","amlod",ph=False,focus=True)}'
          f'{drug_result("Amlodipine","Tablet · 5 mg, 10 mg","Calcium channel blocker","Pick amlodipine")}'
          f'{drug_result("Amoxicillin","Capsule · 250 mg","Penicillin — allergic","Pick amoxicillin")}'
          f'{C3_BLOCK}'
          f'{group_card("On this prescription", [rx_line("Amlodipine","5 mg","Once daily, morning","30 days","rx1")], p=16)}'
          f'<Frame grow={{1}} />'
          f'{dcta("Add to the visit","Open sign C6","check")}</Frame>'))

# ---------------- C4 order tests
C4_PICK = group_card("Order a test", [
    field("Search tests", "search", "fasting blood", ph=False, focus=True),
    list_row("flask-conical", "Fasting blood sugar", sub="Already outstanding from 12 June", name="Test fbs", tint="var:state/warning-bg"),
    list_row("flask-conical", "HbA1c", sub="Three-month average — better than a single reading", name="Test hba1c"),
    list_row("flask-conical", "Lipid profile", sub="Total cholesterol, HDL, LDL, triglycerides", name="Test lipid"),
    list_row("flask-conical", "Urea, creatinine and electrolytes", sub="Kidney function on antihypertensives", name="Test uce"),
    list_row("heart-pulse", "ECG", sub="Available at Garki Medical Centre", name="Test ecg"),
])
C4_WHERE = group_card("Where should she go?", [
    radio_row("Garki Medical Centre laboratory", sub="MLSCN accredited · results usually next day · ₦8,500", on=True, name="Lab garki"),
    radio_row("Any Medra partner laboratory", sub="She picks what is near her — price varies", name="Lab any"),
    radio_row("She already has a lab in mind", sub="We send her the request to take with her", name="Lab own"),
], footer="Whichever she picks, the result comes back into her record and into your Needs-you list.")
C4_NOTE = group_card("Note for the laboratory", [
    field("Clinical details", "file-text", "Hypertension on amlodipine. Screening for diabetes. Fasting sample please.", ph=False),
    checkbox("Mark as urgent — results the same day", "Test urgent", checked=False),
])

add("Consultation", "C4-tests",
    dr_desk("Doctor · Consultation — C4 Order Tests",
        f'{C_PATIENT_STRIP}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{C4_PICK}{C4_NOTE}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{C4_WHERE}'
        f'{group_card("On this order", [list_row("flask-conical","Fasting blood sugar",value="₦3,500",name="Ord fbs",chevron=False),list_row("flask-conical","HbA1c",value="₦5,000",name="Ord hba1c",chevron=False),list_row("receipt","She pays the laboratory",sub="Medra does not take a cut of test fees",name="Ord pay",chevron=False)])}'
        f'{dcta("Add to the visit","Open sign C6","check")}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C4 Order Tests · Mobile",
        dr_appbar("Order tests")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{group_card("Order a test", [field("Search tests","search","fasting blood",ph=False,focus=True),list_row("flask-conical","Fasting blood sugar",sub="Outstanding since 12 June",name="Test fbs",tint="var:state/warning-bg"),list_row("flask-conical","HbA1c",name="Test hba1c")], p=16)}'
          f'<Frame grow={{1}} />{dcta("Add to the visit","Open sign C6","check")}</Frame>'))

# ---------------- C5 upload a result
# "the doctor can upload the result of that particular test ... or the hospital's lab technician"
C5_UPLOAD = (f'{upload("Open camera C5", label="Photograph or choose the result")}'
             f'{field_chips("What is it?", ["Lab result", "Imaging", "Discharge summary", "Referral", "Other"], 0, "Upload kind")}'
             f'<Frame w="fill" flex="row" gap={{14}}>'
             f'<Frame grow={{1}} flex="col">{field("Test","flask-conical","Full blood count",ph=False)}</Frame>'
             f'<Frame grow={{1}} flex="col">{field("Date taken","calendar-days","12 June 2026",ph=False)}</Frame></Frame>'
             f'{field("Which laboratory?","hospital","Garki Medical Centre Laboratory",ph=False)}')
C5_READ = group_card("We read this from the page", [
    lab_line("Haemoglobin", "11.2 g/dL", "12.0 – 15.5", "Low"),
    lab_line("White cell count", "6.4 ×10⁹/L", "4.0 – 11.0"),
    lab_line("Platelets", "268 ×10⁹/L", "150 – 400"),
], footer="Check the numbers before you release them. You are signing for what the patient sees.")
C5_EXPLAIN = group_card("Add a line the patient will understand", [
    field("In plain language (optional)", "book-open", "Your haemoglobin is slightly low, which often means low iron. Nothing else is out of range. We will talk about it at your review.", ph=False),
    toggle_row("bell-ring", "Tell her it has arrived", sub="App, WhatsApp and SMS", on=True, name="Notify result"),
    toggle_row("eye", "Release it to her now", sub="Turn this off to hold it until you have spoken", on=False, name="Release result"),
], footer="A result out of range with no explanation frightens people. One sentence from you prevents a panicked call.")

add("Consultation", "C5-upload",
    dr_desk("Doctor · Consultation — C5 Upload a Result",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Consultation")}</Frame>'
        f'{head_chip([("Add a result to",False),("her record",True)],28)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{C5_UPLOAD}{C5_READ}</Frame>'
        f'<Frame w={{400}} flex="col" gap={{16}}>'
        f'<Frame w="fill" h={{200}} rounded={{22}} image="assets/img/thumb-lab.jpg" overflow="hidden" />'
        f'{C5_EXPLAIN}{dcta("Save to her record","Open sign C6","check")}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C5 Upload a Result · Mobile",
        dr_appbar("Upload a result")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{upload("Open camera C5", label="Photograph the result")}'
          f'{field_chips("What is it?", ["Lab result", "Imaging", "Other"], 0, "Upload kind")}'
          f'{C5_READ}<Frame grow={{1}} />{dcta("Save to her record","Open sign C6","check")}</Frame>'))

# ---------------- C6 review, choose what to share, sign
# "the doctor can pick what they want to share with the patient"
C6_SHARE = group_card("What Amara sees", [
    share_toggle("Why she came, in her words", "Share reason"),
    share_toggle("Examination findings", "Share exam"),
    share_toggle("Assessment and diagnosis", "Share assessment"),
    share_toggle("Plan and advice", "Share plan"),
    share_toggle("Prescription", "Share rx"),
    share_toggle("Tests ordered", "Share tests"),
    share_toggle("Your private working notes", "Share private", on=False),
], footer="Anything switched off stays in the clinical record for you and the clinic, and never appears on her phone. She is told a private note exists — she is not shown what it says.")
C6_PREVIEW = (f'<Frame w="fill" flex="col" gap={{13}} p={{20}} rounded={{24}} bg="var:bg/base" '
              f'stroke="var:border/default" strokeWidth={{1}}>'
              f'<Frame w="fill" flex="row" justify="between" items="center">'
              f'<Frame flex="row" gap={{8}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:state/info-bg">'
              f'{I("stethoscope",13,A_IC)}{T(11,"semibold","var:text/default","Consultation")}</Frame>'
              f'{T(11,"regular","var:text/muted","How it looks on her phone")}</Frame>'
              f'{T(18,"bold","var:text/strong","Hypertension review")}'
              f'{note_section("Assessment","Hypertension, partially controlled. No sign of organ damage.","clipboard-check")}'
              f'{note_section("Plan","Continue Amlodipine 5 mg every morning. Less added salt. Walk 30 minutes, five days a week. Fasting blood sugar before your next visit. Review in three months.","list-checks")}'
              f'{hr()}{provenance("Dr. Ngozi Okafor","MDCN 71482","21 Aug 2026, 11:04")}</Frame>')
C6_SIGN = (f'<Frame w="fill" flex="col" gap={{13}} p={{20}} rounded={{24}} bg="var:state/info-bg">'
           f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",18,A_IC)}'
           f'{T(14,"semibold","var:text/strong","Signing makes this permanent")}</Frame>'
           f'{T(13,"regular","var:text/default","Once signed, this note cannot be edited — only amended with a new, dated entry. That is what makes it worth anything to the next doctor who reads it.",w="fill")}'
           f'{checkbox("I confirm this is an accurate record of the consultation.","Confirm accurate")}'
           f'{dcta("Sign and send to Amara","Sign C6","badge-check")}'
           f'{mini_btn("Save as a draft","Save draft C6","file-text","ghost",full=True)}</Frame>')

add("Consultation", "C6-sign",
    dr_desk("Doctor · Consultation — C6 Review &amp; Sign",
        f'{C_PATIENT_STRIP}'
        f'{head_chip([("Check it, then",False),("sign it",True)],28)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{C6_SHARE}'
        f'{group_card("Also going to her", [list_row("pill","Amlodipine 5 mg · 30 days",sub="With reminders at 08:00",name="Sign rx",chevron=False),list_row("flask-conical","Fasting blood sugar, HbA1c",sub="Garki Medical Centre laboratory",name="Sign tests",chevron=False),list_row("calendar-plus","Follow-up in 3 months",sub="She gets a reminder in November",name="Sign followup",chevron=False)])}</Frame>'
        f'<Frame w={{420}} flex="col" gap={{16}}>{eyebrow("PREVIEW")}{C6_PREVIEW}{C6_SIGN}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C6 Review &amp; Sign · Mobile",
        dr_appbar("Review and sign")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{group_card("What Amara sees", [share_toggle("Assessment and diagnosis","Share assessment"),share_toggle("Plan and advice","Share plan"),share_toggle("Prescription","Share rx"),share_toggle("Your private working notes","Share private",on=False)], p=16)}'
          f'<Frame grow={{1}} />{C6_SIGN}</Frame>'))

# ---------------- C7 done
C7 = (f'<Frame w="fill" flex="col" gap={{16}} items="center">'
      f'{big_icon("badge-check","ok",96)}'
      f'{T(23,"bold","var:text/strong","Signed and sent")}'
      f'{T(15,"regular","var:text/muted","Amara has the note, the prescription and the test request on her phone. The consultation took 14 minutes.",w="fill",align="center")}'
      f'{group_card("", [list_row("file-text","Consultation note",value="Shared",sub="Private working notes withheld",name="Done note",chevron=False),list_row("pill","Amlodipine 5 mg",value="Sent",sub="Garki pharmacy notified",name="Done rx",chevron=False),list_row("flask-conical","2 tests ordered",value="Sent",sub="Results come back to your Needs-you list",name="Done tests",chevron=False),list_row("banknote","₦15,000",value="Paid",sub="In Friday’s payout",name="Done paid",chevron=False)])}</Frame>')
C7_NEXT = group_card("Next patient", [
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "11:00 · in person · cough for four days", "12 Jun", "Q Chidi"),
], footer="You are running four minutes early.")

add("Consultation", "C7-done",
    dr_desk("Doctor · Consultation — C7 Signed",
        f'<Frame w="fill" flex="row" gap={{20}} justify="center" items="start" pt={{10}}>'
        f'<Frame w={{560}} flex="col" gap={{16}}>{C7}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{C7_NEXT}'
        f'{dcta("Start the next consultation","Start consult","stethoscope")}'
        f'{mini_btn("Back to today","Nav Today","arrow-left","ghost",full=True)}</Frame></Frame>',
        SIDE["Notes"], topbar=False),
    dr_mob("Doctor · Consultation — C7 Signed · Mobile",
        dr_appbar(None, back=False, right=circle_btn("x", "Nav Today"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{6}} pb={{10}}>{C7}'
          f'<Frame grow={{1}} />{dcta("Start the next consultation","Start consult","stethoscope")}</Frame>'))

# =====================================================================================
# PATIENTS
# =====================================================================================
# "the doctor can search for their card based on their user ID ... in a case where they don't
#  remember their NIN"
T1_SEARCH = (f'<Frame w="fill" flex="col" gap={{11}}>'
             f'{field("Find a patient","search","MDR-8842",ph=False,focus=True,helper="Medra ID, full name, or phone number. Partial IDs work.")}'
             f'<Frame w="fill" flex="row" gap={{9}} items="center">'
             f'{mini_btn("My patients","Filter mine",None,"navy")}'
             f'{mini_btn("Seen this week","Filter week",None,"ghost")}'
             f'{mini_btn("Owing a test","Filter owing","flask-conical","ghost")}'
             f'{mini_btn("Scan a code","Scan patient","qr-code","ghost")}</Frame></Frame>')
T1_LIST = group_card("42 patients", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "34 · hypertension · O+", "Today", "Open Amara", tag="today"),
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "6 · guardian: Amara Okeke", "Today", "Open Chidi", tag="today"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "68 · diabetes, hypertension", "28 Apr", "Open Grace"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "51 · first visit today", "Never", "Open Musa", tag="new"),
    patient_row("avatar-5.jpg", "Tunde Bello", "MDR-6620-88", "44 · awaiting results", "2 Aug", "Open Tunde", tag="pending"),
])
T1_RECENT = group_card("You looked at recently", [
    list_row("clipboard-list", "Amara Okeke", sub="Hypertension review · 12 Jun", name="Open Amara"),
    list_row("clipboard-list", "Grace Okeke", sub="Blood sugar result · 3 Aug", name="Open Grace"),
], footer="Every record you open is logged with your name and the time, and the patient can see it.")

add("Patients", "T1-patients",
    dr_desk("Doctor · Patients — T1 Find a Patient",
        f'{head_chip([("Your",False),("patients",True)],28)}'
        f'{T(15,"regular","var:text/muted","Search by Medra ID when someone cannot remember anything else — it is on their phone and on their printed summary.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{T1_SEARCH}{T1_LIST}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{T1_RECENT}'
        f'{group_card("Cannot find someone?", [list_row("qr-code","Scan the code on their phone",sub="Or the QR on their printed summary",name="Scan patient"),list_row("user-plus","Add a walk-in",sub="They get a Medra ID and can claim the record later",name="Add walkin"),list_row("circle-help","They may not have shared with you",sub="You only see patients who booked you or granted access",name="Why missing",chevron=False)])}</Frame></Frame>',
        SIDE["Patients"]),
    dr_mob("Doctor · Patients — T1 Find a Patient · Mobile",
        dr_appbar("Patients", back=False, right=circle_btn("qr-code", "Scan patient"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{field("Find a patient","search","MDR-8842",ph=False,focus=True)}'
          f'{group_card("42 patients", [patient_row("avatar-2.jpg","Amara Okeke","MDR-8842-19","34 · hypertension","Today","Open Amara",tag="today"),patient_row("avatar-6.jpg","Chidi Okeke","MDR-8842-20","6 · guardian: Amara","Today","Open Chidi",tag="today"),patient_row("avatar-1.jpg","Musa Ibrahim","MDR-7714-02","51 · first visit","Never","Open Musa",tag="new")], p=16)}</Frame>',
        nav=dr_bottom_nav(TAB["Patients"])))

# ---------------- T2 patient record (consent-scoped)
T2_HEAD = (f'<Frame w="fill" flex="col" gap={{15}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" gap={{15}} items="center">'
           f'<Image image="assets/img/avatar-2.jpg" w={{68}} h={{68}} rounded={{22}} />'
           f'<Frame grow={{1}} flex="col" gap={{4}}>{T(20,"bold","var:text/strong","Amara Okeke")}'
           f'<Frame flex="row" gap={{9}} items="center">'
           f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="var:bg/muted">'
           f'{T(11,"semibold","var:text/accent","MDR-8842-19")}</Frame>'
           f'{T(13,"regular","var:text/muted","34 · female · +234 801 234 5678")}</Frame></Frame>'
           f'{status_pill("shared","Access until 21 Aug, 11:00")}</Frame>'
           f'<Frame w="fill" flex="row" gap={{10}}>'
           f'{stat_cell_dr("droplet","O+","Blood group")}{stat_cell_dr("activity","AA","Genotype")}'
           f'{stat_cell_dr("ruler","1.68 m","Height")}{stat_cell_dr("weight","74 kg","Weight")}</Frame></Frame>')
T2_HEAD_M = (f'<Frame w="fill" flex="row" gap={{13}} items="center" p={{16}} rounded={{24}} bg="var:bg/base" '
             f'stroke="var:border/subtle" strokeWidth={{1}}>'
             f'<Image image="assets/img/avatar-2.jpg" w={{54}} h={{54}} rounded={{18}} />'
             f'<Frame grow={{1}} flex="col" gap={{3}}>{T(17,"bold","var:text/strong","Amara Okeke")}'
             f'<Frame flex="row" px={{8}} py={{3}} rounded={{7}} bg="var:bg/muted">'
             f'{T(10,"semibold","var:text/accent","MDR-8842-19")}</Frame>'
             f'{T(11,"regular","var:text/muted","34 · O+ · AA · 1.68 m · 74 kg",w="fill")}</Frame></Frame>')

T2_SAFETY = alert_strip("triangle-alert", "Penicillin allergy · hypertension",
    "Always visible to any doctor treating her, whatever else she has shared.", "warn")
T2_TIMELINE = group_card("Her history", [
    list_row("stethoscope", "Hypertension review", value="12 Jun", sub="You · Garki Medical Centre", name="Open note last"),
    list_row("flask-conical", "Full blood count", value="12 Jun", sub="Haemoglobin low at 11.2", name="Open lab", tint="var:state/warning-bg"),
    list_row("pill", "Amlodipine 5 mg", value="Active", sub="96% taken on time", name="Open adherence"),
    list_row("stethoscope", "Malaria — treated", value="28 Apr", sub="Dr. Chuka Eze · Wuse Clinic", name="Open other note"),
    list_row("syringe", "Yellow fever booster", value="28 Apr", sub="Wuse Clinic", name="Open vaccine"),
    list_row("file-plus", "Scan of old NHIS card", value="2 Aug", sub="Added by the patient", name="Open upload"),
])
T2_LOCKED = group_card("Not shared with you", [
    scope_line("Prescription history from other clinics", False, "She can turn this on from her phone"),
    scope_line("Home vitals", False, "Blood pressure readings she takes herself"),
    scope_line("Records she has marked private", False, "You are told they exist, not what they say"),
], footer="Asking is a normal part of a consultation. Use “Ask for more history” and she gets a request she can accept or decline.")
T2_VITALS = group_card("Blood pressure", [
    chart([("Mar", "142/92", 96, "bad"), ("Apr", "138/88", 86, "warn"), ("May", "136/86", 82, "warn"),
           ("Jun", "132/84", 74, "ok"), ("Jul", "130/82", 68, "ok"), ("Aug", "128/82", 64, "ok")], 120, "Systolic, mmHg"),
], footer="Clinic readings only. Her home readings are not shared with you.")

add("Patients", "T2-record",
    dr_desk("Doctor · Patients — T2 Patient Record",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Patients")}</Frame>'
        f'<Frame flex="row" gap={{10}} items="center">'
        f'{mini_btn("Ask for more history","Open access T3","message-square-text","ghost",grow=False)}'
        f'{mini_btn("Start a consultation","Start consult","stethoscope","navy",grow=False)}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{T2_HEAD}{T2_SAFETY}{T2_TIMELINE}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{T2_VITALS}{T2_LOCKED}</Frame></Frame>',
        SIDE["Patients"]),
    dr_mob("Doctor · Patients — T2 Patient Record · Mobile",
        dr_appbar("Patient", right=circle_btn("stethoscope", "Start consult"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{8}}>'
          f'{T2_HEAD_M}{T2_SAFETY}'
          f'{group_card("Her history", [list_row("stethoscope","Hypertension review",value="12 Jun",name="Open note last"),list_row("flask-conical","Full blood count",value="12 Jun",sub="Haemoglobin low",name="Open lab",tint="var:state/warning-bg"),list_row("pill","Amlodipine 5 mg",value="Active",name="Open adherence")], p=16)}'
          f'{group_card("Blood pressure", [chart([("Jun","132/84",56,"ok"),("Jul","130/82",50,"ok"),("Aug","128/82",46,"ok")],96,"Clinic readings only")], p=16)}</Frame>',
        nav=dr_bottom_nav(TAB["Patients"])))

# ---------------- T3 ask for more access / history
T3_PICK = group_card("What do you need to see?", [
    consent_row("pill", "Prescription history from other clinics", "What she was given and whether she took it", "Ask rx"),
    consent_row("activity", "Home blood pressure readings", "Her own measurements between visits", "Ask vitals"),
    consent_row("flask-conical", "Older lab results", "Anything before January 2026", "Ask labs", on=False),
    consent_row("file-plus", "Records she uploaded herself", "Scans of paper results", "Ask uploads", on=False),
])
T3_WHY = group_card("Why are you asking?", [
    field("She sees this message", "message-square-text",
          "I want to check whether the headaches started before or after we changed your dose. Your older prescriptions would tell me.", ph=False),
    radio_row("Just for this consultation", sub="Access ends when you sign the note", on=True, name="Ask window visit"),
    radio_row("For 7 days", sub="If you are waiting on results", name="Ask window 7d"),
], footer="She can accept, accept part of it, or decline. Declining is recorded and does not affect her care.")
T3_ASKED = group_card("What you have already asked", [
    audit_row("You asked for prescription history", "Declined by the patient · 12 Jun", "2 months ago"),
    audit_row("You asked about undisclosed history", "Answered on the call · 21 Aug", "Today"),
], footer="Asking is logged so it is always clear what you tried to find out and what you were told.")

add("Patients", "T3-access",
    dr_desk("Doctor · Patients — T3 Ask for More",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Amara Okeke")}</Frame>'
        f'{head_chip([("Ask her for",False),("more history",True)],28)}'
        f'{T(15,"regular","var:text/muted","She controls her record. You can always ask — and what you asked, and what she answered, is recorded.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{T3_PICK}{T3_WHY}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{T3_ASKED}'
        f'{dcta("Send the request","Send access T3","send")}'
        f'{alert_strip("info","She gets this on WhatsApp and in the app","Most people answer within a few minutes during a consultation.","info")}</Frame></Frame>',
        SIDE["Patients"]),
    dr_mob("Doctor · Patients — T3 Ask for More · Mobile",
        dr_appbar("Ask for more")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{T3_PICK}<Frame grow={{1}} />{dcta("Send the request","Send access T3","send")}</Frame>'))

# =====================================================================================
# PRACTICE & EARNINGS
# =====================================================================================
S1_PROFILE = (f'<Frame w="fill" flex="col" gap={{16}} p={{20}} rounded={{28}} bg="var:bg/base" '
              f'stroke="var:border/subtle" strokeWidth={{1}}>'
              f'<Frame w="fill" flex="row" gap={{15}} items="center">'
              f'<Image image="assets/img/avatar-4.jpg" w={{78}} h={{78}} rounded={{26}} />'
              f'<Frame grow={{1}} flex="col" gap={{4}}>'
              f'<Frame flex="row" gap={{8}} items="center">{T(20,"bold","var:text/strong","Dr. Ngozi Okafor")}'
              f'{I("badge-check",18,T_IC)}</Frame>'
              f'{T(13,"regular","var:text/muted","Cardiologist · MDCN 71482 · verified 4 Feb 2026")}</Frame>'
              f'{mini_btn("Change photo","Change photo S1","camera","ghost",grow=False)}</Frame>'
              f'{field("Short bio","file-text","Consultant cardiologist with 12 years in hypertension, heart failure and preventive cardiology.",ph=False,helper="Members read this before they book. Two sentences beat two paragraphs.")}'
              f'{field("Specialisation","stethoscope","Cardiology",ph=False,trailing=("chevron-down","Specialty dropdown"),helper="From the Medra list, which the platform team keeps current.")}'
              f'{field_chips("Languages you consult in",["English","Hausa","Yoruba","Igbo","Pidgin"],0,"Langs")}'
              f'{field("Where you practise","hospital","Garki Medical Centre, Area 3, Abuja",ph=False)}</Frame>')
S1_PROFILE_M = (f'<Frame w="fill" flex="col" gap={{14}} p={{18}} rounded={{26}} bg="var:bg/base" '
                f'stroke="var:border/subtle" strokeWidth={{1}}>'
                f'<Frame w="fill" flex="row" gap={{13}} items="center">'
                f'<Image image="assets/img/avatar-4.jpg" w={{62}} h={{62}} rounded={{20}} />'
                f'<Frame grow={{1}} flex="col" gap={{3}}>'
                f'<Frame flex="row" gap={{7}} items="center">{T(17,"bold","var:text/strong","Dr. Ngozi Okafor")}'
                f'{I("badge-check",16,T_IC)}</Frame>'
                f'{T(11,"regular","var:text/muted","Cardiologist · MDCN 71482 · verified",w="fill")}</Frame>'
                f'{mini_btn("Photo","Change photo S1","camera","ghost",grow=False)}</Frame>'
                f'{field("Short bio","file-text","Consultant cardiologist, 12 years in hypertension and heart failure.",ph=False)}'
                f'{field("Specialisation","stethoscope","Cardiology",ph=False,trailing=("chevron-down","Specialty dropdown"))}</Frame>')

S1_PUBLIC = group_card("How members see you", [
    list_row("star", "Rating", value="4.9", sub="From 148 completed visits", name="Prof rating", chevron=False),
    list_row("users", "Patients seen on Medra", value="1,204", name="Prof patients", chevron=False),
    list_row("clock", "Median wait to be seen", value="6 minutes", sub="Shown on your profile — it is why people pick you", name="Prof wait", chevron=False),
    list_row("eye", "Preview my public profile", name="Preview profile", ),
])

add("Practice", "S1-profile",
    dr_desk("Doctor · Practice — S1 Public Profile",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{head_chip([("What patients",False),("see",True)],28)}'
        f'{mini_btn("Save changes","Save profile S1","check","navy",grow=False)}</Frame>'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{S1_PROFILE}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{S1_PUBLIC}'
        f'{group_card("Settings", [list_row("banknote","Consultation types and fees",value="3",name="Open fees S2"),list_row("video","Virtual meeting link",value="Google Meet",name="Open meeting S3"),list_row("message-circle","How patients reach me",value="WhatsApp, email",name="Open contact S4"),list_row("clock","Availability",name="Nav Schedule"),list_row("log-out","Sign out",name="Sign out",chevron=False)])}</Frame></Frame>',
        SIDE["Settings"]),
    dr_mob("Doctor · Practice — S1 Public Profile · Mobile",
        dr_appbar("Profile", back=False, right=circle_btn("check", "Save profile S1"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{S1_PROFILE_M}'
          f'{group_card("Settings", [list_row("banknote","Fees",value="3 types",name="Open fees S2"),list_row("video","Meeting link",value="Google Meet",name="Open meeting S3"),list_row("message-circle","How patients reach me",name="Open contact S4")], p=16)}</Frame>',
        nav=dr_bottom_nav(TAB["Settings"])))

# ---------------- S2 consultation types & fees
def fee_card(title, mins, price, desc, name, on=True):
    sw = (f'<Frame name="Btn Toggle {name}" w={{44}} h={{25}} rounded={{999}} image="assets/img/btn-teal.jpg" '
          f'overflow="hidden" flex="row" justify="end" items="center" px={{3}}><Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame>'
          if on else
          f'<Frame name="Btn Toggle {name}" w={{44}} h={{25}} rounded={{999}} bg="var:neutral/300" '
          f'flex="row" justify="start" items="center" px={{3}}><Ellipse w={{19}} h={{19}} bg="#FFFFFF" /></Frame>')
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{12}} p={{18}} rounded={{22}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'<Frame flex="col" gap={{3}}>{T(16,"semibold","var:text/strong",title)}'
            f'{T(12,"regular","var:text/muted",desc)}</Frame>{sw}</Frame>'
            f'<Frame w="fill" flex="row" gap={{10}}>'
            f'<Frame grow={{1}} flex="col" gap={{2}} items="center" py={{12}} rounded={{16}} bg="var:bg/subtle">'
            f'{T(16,"bold","var:text/strong",mins)}{T(11,"regular","var:text/muted","minutes")}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}} items="center" py={{12}} rounded={{16}} bg="var:bg/subtle">'
            f'{T(16,"bold","var:text/strong",price)}{T(11,"regular","var:text/muted","per consultation")}</Frame></Frame></Frame>')

S2_TYPES = (fee_card("First visit", "45", "₦20,000", "New patients — more time to take a history", "Fee first")
            + fee_card("Follow-up", "30", "₦15,000", "Someone you have seen before", "Fee followup")
            + fee_card("Quick video review", "15", "₦8,000", "Results, prescriptions, short questions", "Fee quick")
            + fee_card("Home visit", "60", "₦45,000", "Within 10 km of Garki", "Fee home", on=False))
S2_PAYOUT = group_card("What you actually receive", [
    earn_row("Consultation fee", "What the member pays", "₦15,000"),
    earn_row("Medra commission", "12% while the pilot runs", "− ₦1,800", "muted"),
    earn_row("Payment processing", "Paystack, deducted at source", "− ₦225", "muted"),
    earn_row("You receive", "Paid out every Friday", "₦12,975", "ok"),
], footer="Commission is set by the Medra team and shown here before any change takes effect. Test and procedure fees are not commissioned.")

add("Practice", "S2-fees",
    dr_desk("Doctor · Practice — S2 Types &amp; Fees",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{head_chip([("What you offer,",False),("and for how much",True)],28)}'
        f'{mini_btn("Add a type","Add fee type","plus","navy",grow=False)}</Frame>'
        f'{T(15,"regular","var:text/muted","Each type has its own length, so your calendar blocks correctly. Members see the price before they book — never after.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{S2_TYPES}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{S2_PAYOUT}'
        f'{alert_strip("info","Changing a fee does not change existing bookings","Anyone who already paid keeps the price they paid.","info")}'
        f'{dcta("Save fees","Save fees S2","check")}</Frame></Frame>',
        SIDE["Settings"]),
    dr_mob("Doctor · Practice — S2 Types &amp; Fees · Mobile",
        dr_appbar("Types and fees", right=circle_btn("plus", "Add fee type"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{fee_card("Follow-up","30","₦15,000","Someone you have seen before","Fee followup")}'
          f'{fee_card("First visit","45","₦20,000","New patients","Fee first")}'
          f'{fee_card("Quick video review","15","₦8,000","Results and short questions","Fee quick")}'
          f'<Frame grow={{1}} />{dcta("Save fees","Save fees S2","check")}</Frame>'))

# ---------------- S3 virtual meeting link
# "the doctor will set up the meeting and add the link ... the link is embedded into the button"
S3_PROVIDER = group_card("Which app do you use?", [
    radio_row("Google Meet", sub="A new link is created for every appointment", on=True, name="Provider meet"),
    radio_row("Zoom", sub="We use your personal meeting room, or a new link per visit", name="Provider zoom"),
    radio_row("Microsoft Teams", name="Provider teams"),
    radio_row("I paste a link myself each time", sub="Slowest, but works with anything", name="Provider manual"),
], footer="Medra does not host the call in the MVP — it hands the patient a working link at the right moment, and holds their booking and payment around it.")
S3_SETUP = group_card("Your link", [
    field("Meeting link", "video", "meet.google.com/kfa-jrqz-nmo", ph=False, trailing=("copy", "Copy meet link"),
          helper="Sent to the patient one hour before, and again 10 minutes before."),
    toggle_row("refresh-cw", "New link for every appointment", sub="Safer — nobody wanders into someone else's consultation", on=True, name="New link each"),
    toggle_row("lock", "Wait in a lobby until I admit them", sub="Strongly recommended", on=True, name="Lobby on"),
    toggle_row("phone-call", "Offer a phone call if the video fails", sub="The clinic rings them on the number they registered", on=True, name="Phone fallback"),
])
S3_TEST = (f'<Frame w="fill" flex="col" gap={{12}} p={{18}} rounded={{22}} bg="var:state/success-bg">'
           f'<Frame flex="row" gap={{9}} items="center">{I("circle-check",17,OK_IC)}'
           f'{T(14,"semibold","var:text/strong","Link tested and working")}</Frame>'
           f'{T(13,"regular","var:text/default","Checked 2 minutes ago. We test it before every virtual appointment and warn you if it breaks.",w="fill")}'
           f'{mini_btn("Test it again now","Test link S3","refresh-cw","ghost",full=True)}</Frame>')

add("Practice", "S3-meeting",
    dr_desk("Doctor · Practice — S3 Virtual Visits",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Practice settings")}</Frame>'
        f'{head_chip([("How your video",False),("visits happen",True)],28)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{S3_PROVIDER}{S3_SETUP}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{S3_TEST}'
        f'{group_card("Coming later", [list_row("sparkles","Video inside Medra",sub="No third-party app, and the note writes itself as you talk",name="Phase2 video",chevron=False),list_row("type","Automatic transcription",sub="You edit and sign — nothing is stored without the patient agreeing",name="Phase2 transcribe",chevron=False)], footer="Phase 2. The designs exist — ask to see them.")}'
        f'{dcta("Save","Save meeting S3","check")}</Frame></Frame>',
        SIDE["Settings"]),
    dr_mob("Doctor · Practice — S3 Virtual Visits · Mobile",
        dr_appbar("Virtual visits", right=circle_btn("check", "Save meeting S3"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{S3_PROVIDER}{S3_TEST}</Frame>'))

# ---------------- S4 contact channels
# "allow patient contact via either email, phone number or WhatsApp"
S4_CHANNELS = group_card("How patients can reach you between visits", [
    toggle_row("message-circle", "WhatsApp", sub="+234 803 555 0110 — the number most people will actually use", on=True, name="Contact whatsapp"),
    toggle_row("mail", "Work email", sub="dr.okafor@clinic.ng", on=True, name="Contact email"),
    toggle_row("phone-call", "Phone call", sub="They can ring you directly", on=False, name="Contact phone"),
    toggle_row("message-square-text", "Messages inside Medra", sub="Kept with the patient's record — the only channel that is", on=True, name="Contact inapp"),
], footer="Only patients you have actually consulted see these. Turn any of them off and it disappears from their screen immediately.")
S4_LIMITS = group_card("Protect your evenings", [
    list_row("clock", "Show as available", value="08:00 – 18:00", sub="Outside this, patients see “replies tomorrow”", name="Contact hours"),
    list_row("calendar-days", "Days", value="Monday to Saturday", name="Contact days"),
    toggle_row("moon", "Do not disturb outside those hours", sub="Messages still arrive, they just do not ring", on=True, name="Contact dnd"),
    list_row("triangle-alert", "What counts as urgent", sub="Chest pain, breathlessness, bleeding — these always ring through", name="Contact urgent"),
], footer="Medra tells patients plainly that these channels are not for emergencies, and shows them what to do instead.")
S4_PREVIEW = (f'<Frame w="fill" flex="col" gap={{13}} p={{20}} rounded={{24}} bg="var:bg/base" '
              f'stroke="var:border/default" strokeWidth={{1}}>'
              f'{eyebrow("HOW IT LOOKS ON HER PHONE")}'
              f'{T(16,"bold","var:text/strong","Contact Dr. Okafor")}'
              f'{list_row("message-circle","WhatsApp",sub="Usually replies within a few hours",name="Prev whatsapp")}'
              f'{list_row("mail","Email",sub="dr.okafor@clinic.ng",name="Prev email")}'
              f'{note("triangle-alert","For chest pain, breathlessness or bleeding, do not message — go to the nearest emergency department or call 112.","warn")}</Frame>')

add("Practice", "S4-contact",
    dr_desk("Doctor · Practice — S4 How Patients Reach You",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Practice settings")}</Frame>'
        f'{head_chip([("Reachable, but",False),("on your terms",True)],28)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{S4_CHANNELS}{S4_LIMITS}</Frame>'
        f'<Frame w={{400}} flex="col" gap={{16}}>{S4_PREVIEW}{dcta("Save","Save contact S4","check")}</Frame></Frame>',
        SIDE["Settings"]),
    dr_mob("Doctor · Practice — S4 How Patients Reach You · Mobile",
        dr_appbar("Contact channels", right=circle_btn("check", "Save contact S4"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{12}} px={{20}} pt={{2}} pb={{10}}>'
          f'{S4_CHANNELS}</Frame>'))

# ---------------- S5 earnings
S5_STATS = rows_of([
    stat_card("banknote", "₦486,000", "This month", "32 consultations", "tint-teal.jpg"),
    stat_card("wallet", "₦129,750", "Next payout", "Friday 22 August", "tint-mint.jpg"),
    stat_card("trending-up", "+18%", "Vs last month", "More follow-ups", "tint-ocean.jpg"),
    stat_card("circle-slash", "₦15,000", "Refunded", "1 cancellation by you", "tint-amber.jpg"),
], 4, 16)
S5_BREAKDOWN = group_card("August so far", [
    earn_row("22 follow-ups", "₦15,000 each", "₦330,000"),
    earn_row("6 first visits", "₦20,000 each", "₦120,000"),
    earn_row("4 quick video reviews", "₦8,000 each", "₦32,000"),
    earn_row("1 refund", "You cancelled — Amara Okeke, 8 Aug", "− ₦15,000", "muted"),
    earn_row("Medra commission and fees", "12% plus processing", "− ₦58,320", "muted"),
    earn_row("Your total", "Before tax", "₦408,680", "ok"),
], footer="Medra reports what it pays you to FIRS. Keeping your own records is still your responsibility.")
S5_PAYOUTS = group_card("Payouts", [
    list_row("building-2", "Zenith Bank · ****4421", sub="Ngozi Okafor · verified", name="Payout account"),
    list_row("calendar-days", "Every Friday", sub="Anything completed by Thursday midnight", name="Payout schedule"),
    list_row("download", "Download statements", sub="Monthly PDF and CSV", name="Payout statements"),
    list_row("receipt", "Tax summary for the year", value="2026", name="Payout tax"),
])

add("Practice", "S5-earnings",
    dr_desk("Doctor · Practice — S5 Earnings",
        f'{head_chip([("What you have",False),("earned",True)],28)}{S5_STATS}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{S5_BREAKDOWN}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{S5_PAYOUTS}'
        f'{alert_strip("wallet","Next payout ₦129,750 on Friday","Sent to Zenith Bank ****4421. It usually lands the same day.","ok")}</Frame></Frame>',
        SIDE["Earnings"]),
    dr_mob("Doctor · Practice — S5 Earnings · Mobile",
        dr_appbar("Earnings", back=False, right=circle_btn("download", "Payout statements"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{rows_of([stat_card("banknote","₦486,000","This month","32 consultations","tint-teal.jpg"),stat_card("wallet","₦129,750","Next payout","Friday","tint-mint.jpg")],2,12)}'
          f'{group_card("August so far", [earn_row("22 follow-ups","₦15,000 each","₦330,000"),earn_row("6 first visits","₦20,000 each","₦120,000"),earn_row("Commission and fees","12% plus processing","− ₦58,320","muted"),earn_row("Your total","Before tax","₦408,680","ok")], p=16)}</Frame>',
        nav=dr_bottom_nav(TAB["Earnings"])))

# =====================================================================================
# STATES
# =====================================================================================
X1_STEPS = group_card("Where your application is", [
    prep_step(1, "Details received", "4 February, 09:12", done=True),
    prep_step(2, "MDCN register checked", "4 February, 11:40 — MDCN 71482 found and active", done=True),
    prep_step(3, "Identity confirmed", "A Medra reviewer is checking your ID against the register"),
    prep_step(4, "Profile goes live", "Usually within 48 hours of step 3"),
], footer="We check every doctor by hand. It is slower, and it is the reason members trust a Medra booking.")
X1_MEANWHILE = group_card("What you can do now", [
    list_row("circle-user", "Finish your public profile", sub="Photo, bio, languages — the parts members read first", name="Open profile S1"),
    list_row("banknote", "Set your consultation types and fees", name="Open fees S2"),
    list_row("clock", "Set your working hours", sub="Nothing is bookable until you are verified", name="Nav Schedule"),
    list_row("video", "Connect your meeting link", name="Open meeting S3"),
], footer="Everything you set up now goes live the moment you are verified — no second setup.")

add("States", "X1-verifying",
    dr_desk("Doctor · States — X1 Verification Pending",
        f'<Frame w="fill" flex="col" gap={{14}} p={{26}} rounded={{28}} image="assets/img/btn-navy.jpg" overflow="hidden">'
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{eyebrow("VERIFICATION IN PROGRESS","var:brand/teal")}{status_pill("pending","Step 3 of 4")}</Frame>'
        f'{T(28,"bold","var:text/on-dark","We are checking your licence")}'
        f'{T(15,"regular","var:text/on-dark-muted","You can set everything up while you wait. Your profile appears to members the moment a reviewer signs it off.",w="fill")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{X1_STEPS}</Frame>'
        f'<Frame w={{400}} flex="col" gap={{16}}>{X1_MEANWHILE}'
        f'{alert_strip("info","Entered the wrong MDCN number?","Fix it now and we restart the check straight away — it does not go to the back of the queue.","info")}'
        f'{mini_btn("Contact the Medra team","Contact support","message-square-text","ghost",full=True)}</Frame></Frame>',
        SIDE["Today"], topbar=False),
    dr_mob("Doctor · States — X1 Verification Pending · Mobile",
        dr_appbar("Verification", back=False)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{X1_STEPS}'
          f'{group_card("What you can do now", [list_row("circle-user","Finish your public profile",name="Open profile S1"),list_row("banknote","Set your fees",name="Open fees S2"),list_row("clock","Set your hours",name="Nav Schedule")], p=16)}</Frame>',
        nav=dr_bottom_nav(TAB["Today"])))

# ---------------- X2 nothing booked
X2_EMPTY = empty_state("calendar-check", "Nothing booked today",
    "Your hours are set and your profile is live. When someone books you, they appear here — and you get a notification.",
    primary=dcta("Open more slots", "Open availability K4", "clock"),
    secondary=mini_btn("Share my booking link", "Share booking link", "share-2", "ghost", full=True), tone="ok")
X2_WHY = group_card("Getting booked more", [
    list_row("clock", "Open earlier or later slots", sub="7am and 7pm are the two most-searched times in Abuja", name="Open availability K4"),
    list_row("video", "Offer virtual visits", sub="Members book 3× more video visits than in-person", name="Open fees S2"),
    list_row("camera", "Add a photo", sub="Profiles with a photo are booked twice as often", name="Open profile S1"),
    list_row("share-2", "Share your booking link", sub="Send it to existing patients on WhatsApp", name="Share booking link"),
], footer="These are observations from the pilot, not promises.")

add("States", "X2-empty",
    dr_desk("Doctor · States — X2 Nothing Booked",
        f'<Frame w="fill" flex="row" gap={{18}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{X2_EMPTY}</Frame>'
        f'<Frame w={{400}} flex="col" gap={{16}}>{X2_WHY}</Frame></Frame>',
        SIDE["Today"]),
    dr_mob("Doctor · States — X2 Nothing Booked · Mobile",
        dr_greet()
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>{X2_EMPTY}</Frame>',
        nav=dr_bottom_nav(TAB["Today"])))

# ---------------- X3 notifications
X3_TODAY = (f'<Frame w="fill" flex="col" gap={{10}}>{eyebrow("TODAY")}'
            f'{notif_row("flask-conical","Result back for Musa Ibrahim","Troponin normal. Release it to him or hold it until you speak.","12 min ago","Notif result",unread=True,tone="warn")}'
            f'{notif_row("package","Refill request from Grace Okeke","Metformin 500 mg · 30 days · she has 4 days left","1h ago","Notif refill",unread=True,tone="info")}'
            f'{notif_row("calendar-x","Amara Okeke cancelled","Thu 28 Aug, 10:30 — released back to your open slots","3h ago","Notif cancel",unread=True,tone="muted")}'
            f'{notif_row("notebook-pen","Yesterday’s note is still unsigned","Chidi Okeke, 16:40. He cannot see it until you sign.","This morning","Notif unsigned",tone="warn")}</Frame>')
X3_EARLIER = (f'<Frame w="fill" flex="col" gap={{10}}>{eyebrow("EARLIER")}'
              f'{notif_row("message-square-text","Amara Okeke answered your request","She agreed to share her prescription history for this visit.","Tue","Notif access",tone="ok")}'
              f'{notif_row("banknote","₦129,750 paid out","Zenith Bank ****4421 · 32 consultations","Fri","Notif payout",tone="ok")}'
              f'{notif_row("star","New rating: 5 stars","“She explained everything and did not rush me.”","Fri","Notif rating",tone="ok")}</Frame>')

add("States", "X3-notifications",
    dr_desk("Doctor · States — X3 Notifications",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{head_chip([("What needs",False),("your attention",True)],28)}'
        f'{mini_btn("Mark all read","Mark all read","check-check","ghost",grow=False)}</Frame>'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{18}}>{X3_TODAY}{X3_EARLIER}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>'
        f'{group_card("Blocking a patient right now", [list_row("flask-conical","1 result to release",name="Notif result",tint="var:state/warning-bg"),list_row("package","2 refills waiting",name="Open refills",tint="var:state/warning-bg"),list_row("notebook-pen","1 unsigned note",name="Notif unsigned",tint="var:state/error-bg")], footer="Everything else can wait until after clinic.")}'
        f'{group_card("How you get told", [toggle_row("bell","In the app",on=True,name="Dr notif app"),toggle_row("message-circle","WhatsApp",sub="Urgent only — results and cancellations",on=True,name="Dr notif wa"),toggle_row("message-square-text","SMS",sub="If you have no data",on=False,name="Dr notif sms"),toggle_row("mail","A daily email summary",sub="07:00, before clinic",on=True,name="Dr notif email")])}</Frame></Frame>',
        SIDE["Today"]),
    dr_mob("Doctor · States — X3 Notifications · Mobile",
        dr_appbar("Notifications", right=circle_btn("check-check", "Mark all read"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>{X3_TODAY}</Frame>',
        nav=dr_bottom_nav(TAB["Today"])))

# =====================================================================================
# COMPONENT STATES
# =====================================================================================
CMP = []
def cmp_frame(comp, prop, value, body, w=320, h=None):
    hh = f' minH={{{h}}}' if h else ''
    CMP.append((f"cmp/{comp}/{prop}={value}",
        f'<Frame name="cmp/{comp}/{prop}={value}" w={{{w}}}{hh} flex="col" p={{16}} bg="var:bg/base">{body}</Frame>'))

for st, state in (("Open", "open"), ("Booked", "booked"), ("Blocked", "blocked"), ("Break", "break")):
    cmp_frame("Slot", "State", st, f'<Frame w="fill" flex="row">{slot_chip("10:30", state)}</Frame>', w=150)
for st, on in (("Shared", True), ("Withheld", False)):
    cmp_frame("Share Toggle", "State", st, share_toggle("Assessment and diagnosis", "CShare", on), w=340)
cmp_frame("Queue Row", "State", "Waiting",
    queue_row("11:00", "avatar-6.jpg", "Chidi Okeke", "6 years · MDR-8842-20", "Cough for four days",
              "confirmed", "In person", "CQueue"), w=620)
cmp_frame("Queue Row", "State", "Now",
    queue_row("10:30", "avatar-2.jpg", "Amara Okeke", "34 years · MDR-8842-19", "Hypertension follow-up",
              "today", "Virtual", "CQueue", now=True), w=620)
for st, kind in (("Granted", True), ("Locked", False)):
    cmp_frame("Scope Line", "State", st, scope_line("Lab results", kind, "4 results · 1 out of range"), w=380)
cmp_frame("Drug Result", "State", "Default", drug_result("Amlodipine", "Tablet · 5 mg, 10 mg", "Calcium channel blocker", "CDrug"), w=420)
cmp_frame("Drug Result", "State", "Blocked", drug_result("Amoxicillin", "Capsule · 250 mg", "Penicillin — allergic", "CDrug"), w=420)

for nm, jsx in CMP:
    fid = nm.replace("cmp/", "CMP-").replace("/", "-").replace("=", "-").replace(" ", "")
    frames.append(("Components", fid + ".jsx", jsx))
    ORDER.setdefault("Components", []).append(fid)

# =====================================================================================
# WRITE
# =====================================================================================
def sanitize(s): return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)', '&amp;', s)
manifest = {}
for page, fn, jsx in frames:
    open(os.path.join(OUT, fn), "w").write(sanitize(jsx))
    manifest.setdefault(page, []).append(fn)
open(os.path.join(OUT, "pages.json"), "w").write(json.dumps(manifest, indent=2))

AUTH_DR = ("Auth · Doctor — D6 Log In", "Auth · Doctor — D6 Log In · Mobile")

NAV = {
  "Btn Nav Today":     NAMES["K1-today"],
  "Btn Nav Schedule":  NAMES["K2-appointments"],
  "Btn Nav Patients":  NAMES["T1-patients"],
  "Btn Nav Notes":     NAMES["C1-room"],
  "Btn Nav Earnings":  NAMES["S5-earnings"],
  "Btn Nav Settings":  NAMES["S1-profile"],
  "Btn Notifications": NAMES["X3-notifications"],
}

TRN = [
 # today & schedule
 ("K1-today","Btn Open prep","K3-appointment"),("K1-today","Btn Start consult","C1-room"),
 ("K1-today","Btn Q Chidi","K3-appointment"),("K1-today","Btn Q Musa","K3-appointment"),
 ("K1-today","Btn Q Grace","K3-appointment"),("K1-today","Btn Q Tunde","K3-appointment"),
 ("K1-today","Btn Open Q Chidi","K3-appointment"),("K1-today","Btn Open Q Musa","K3-appointment"),
 ("K1-today","Btn Open Q Grace","K3-appointment"),("K1-today","Btn Open Q Tunde","K3-appointment"),
 ("K1-today","Btn Start Q Chidi","C1-room"),
 ("K1-today","Btn Open results","X3-notifications"),("K1-today","Btn Open refills","X3-notifications"),
 ("K1-today","Btn Open unsigned","C6-sign"),("K1-today","Btn Search patient","T1-patients"),
 ("K2-appointments","Btn Open timeoff K5","K5-timeoff"),("K2-appointments","Btn Open availability K4","K4-availability"),
 ("K2-appointments","Btn Q Chidi","K3-appointment"),("K2-appointments","Btn Open Q Chidi","K3-appointment"),
 ("K2-appointments","Btn Q Musa","K3-appointment"),("K2-appointments","Btn Open Q Musa","K3-appointment"),
 ("K2-appointments","Btn Search patient","T1-patients"),
 ("K3-appointment","Btn Back","K1-today"),("K3-appointment","Btn Start consult","C1-room"),
 ("K3-appointment","Btn Open access T3","T3-access"),("K3-appointment","Btn Open record T2","T2-record"),
 ("K3-appointment","Btn Open note last","T2-record"),("K3-appointment","Btn Open meeting","C1-room"),
 ("K3-appointment","Btn Search patient","T1-patients"),
 ("K4-availability","Btn Save availability K4","K2-appointments"),("K4-availability","Btn Open fees S2","S2-fees"),
 ("K5-timeoff","Btn Back","K2-appointments"),("K5-timeoff","Btn Save timeoff K5","K2-appointments"),
 ("K5-timeoff","Btn Offer slots K5","K2-appointments"),
 ("K5-timeoff","Btn Move Amara","K3-appointment"),("K5-timeoff","Btn Move Chidi","K3-appointment"),
 ("K5-timeoff","Btn Move Musa","K3-appointment"),("K5-timeoff","Btn Move Grace","K3-appointment"),
 # consultation
 ("C1-room","Btn Open sign C6","C6-sign"),("C1-room","Btn Open prescribe C3","C3-prescribe"),
 ("C1-room","Btn Open tests C4","C4-tests"),("C1-room","Btn Open upload C5","C5-upload"),
 ("C1-room","Btn Back","K3-appointment"),("C1-room","Btn Book followup","K2-appointments"),
 ("C1-room","Btn Side notes","T2-record"),("C1-room","Btn Side meds","T2-record"),
 ("C1-room","Btn Side vitals","T2-record"),("C1-room","Btn Side outstanding","C4-tests"),
 ("C1-room","Btn Template reason","C2-templates"),("C1-room","Btn Template exam","C2-templates"),
 ("C1-room","Btn Template assessment","C2-templates"),("C1-room","Btn Template plan","C2-templates"),
 ("C1-room","Btn Consult tab Prescription","C3-prescribe"),("C1-room","Btn Consult tab Tests","C4-tests"),
 ("C1-room","Btn Consult tab Files","C5-upload"),
 ("C2-templates","Btn Back","C1-room"),("C2-templates","Btn Use template hyp","C1-room"),
 ("C2-templates","Btn Use template new","C1-room"),("C2-templates","Btn Use template discharge","C1-room"),
 ("C2-templates","Btn Use template fever","C1-room"),
 ("C3-prescribe","Btn Open sign C6","C6-sign"),("C3-prescribe","Btn Back","C1-room"),
 ("C3-prescribe","Btn Consult tab Note","C1-room"),
 ("C4-tests","Btn Open sign C6","C6-sign"),("C4-tests","Btn Back","C1-room"),
 ("C5-upload","Btn Open sign C6","C6-sign"),("C5-upload","Btn Back","C1-room"),
 ("C5-upload","Btn Open camera C5","C5-upload"),
 ("C6-sign","Btn Sign C6","C7-done"),("C6-sign","Btn Save draft C6","C1-room"),
 ("C6-sign","Btn Back","C1-room"),
 ("C7-done","Btn Start consult","C1-room"),("C7-done","Btn Nav Today","K1-today"),
 ("C7-done","Btn Q Chidi","K3-appointment"),("C7-done","Btn Open Q Chidi","K3-appointment"),
 # patients
 ("T1-patients","Btn Open Amara","T2-record"),("T1-patients","Btn Open Chidi","T2-record"),
 ("T1-patients","Btn Open Grace","T2-record"),("T1-patients","Btn Open Musa","T2-record"),
 ("T1-patients","Btn Open Tunde","T2-record"),("T1-patients","Btn Scan patient","T2-record"),
 ("T1-patients","Btn Add walkin","T2-record"),
 ("T2-record","Btn Back","T1-patients"),("T2-record","Btn Start consult","C1-room"),
 ("T2-record","Btn Open access T3","T3-access"),("T2-record","Btn Open note last","C6-sign"),
 ("T2-record","Btn Open lab","C5-upload"),("T2-record","Btn Open other note","C6-sign"),
 ("T3-access","Btn Back","T2-record"),("T3-access","Btn Send access T3","T2-record"),
 # practice
 ("S1-profile","Btn Open fees S2","S2-fees"),("S1-profile","Btn Open meeting S3","S3-meeting"),
 ("S1-profile","Btn Open contact S4","S4-contact"),("S1-profile","Btn Save profile S1","S1-profile"),
 ("S1-profile","Btn Sign out","AUTH"),("S1-profile","Btn Preview profile","S1-profile"),
 ("S2-fees","Btn Save fees S2","S1-profile"),("S2-fees","Btn Back","S1-profile"),
 ("S3-meeting","Btn Save meeting S3","S1-profile"),("S3-meeting","Btn Back","S1-profile"),
 ("S4-contact","Btn Save contact S4","S1-profile"),("S4-contact","Btn Back","S1-profile"),
 ("S5-earnings","Btn Payout statements","S5-earnings"),
 # states
 ("X1-verifying","Btn Open profile S1","S1-profile"),("X1-verifying","Btn Open fees S2","S2-fees"),
 ("X1-verifying","Btn Open meeting S3","S3-meeting"),("X1-verifying","Btn Contact support","X1-verifying"),
 ("X2-empty","Btn Open availability K4","K4-availability"),("X2-empty","Btn Open fees S2","S2-fees"),
 ("X2-empty","Btn Open profile S1","S1-profile"),
 ("X3-notifications","Btn Notif result","C5-upload"),("X3-notifications","Btn Notif refill","T2-record"),
 ("X3-notifications","Btn Notif cancel","K2-appointments"),("X3-notifications","Btn Notif unsigned","C6-sign"),
 ("X3-notifications","Btn Notif access","T2-record"),("X3-notifications","Btn Notif payout","S5-earnings"),
 ("X3-notifications","Btn Notif rating","S1-profile"),("X3-notifications","Btn Open refills","T2-record"),
 ("X3-notifications","Btn Mark all read","X3-notifications"),
]

def resolve(target, side):
    if target == "AUTH": return AUTH_DR[side]
    return NAMES[target][side]

resolved = []
for fid, hot, target in TRN:
    if fid not in NAMES: raise SystemExit(f"unknown source frame {fid}")
    for side in (0, 1):
        resolved.append([NAMES[fid][side], hot, resolve(target, side)])

nav_jobs = []
for fid, pair in NAMES.items():
    for side in (0, 1):
        for hot, target in NAV.items():
            nav_jobs.append([pair[side], hot, target[side]])

order_js, starts_js = {}, {}
for page, fids in ORDER.items():
    if page == "Components": continue
    order_js[PAGE_FIGMA[page]] = [[NAMES[f][0], NAMES[f][1]] for f in fids]
    starts_js[PAGE_FIGMA[page]] = NAMES[fids[0]][0]

MOTION = json.dumps({
  "default":  {"type": "SMART_ANIMATE", "easing": "GENTLE", "duration": 0.28},
  "push":     {"type": "MOVE_IN",  "direction": "LEFT",   "easing": "GENTLE",  "duration": 0.26},
  "pop":      {"type": "MOVE_OUT", "direction": "RIGHT",  "easing": "EASE_IN", "duration": 0.22},
  "sheet":    {"type": "MOVE_IN",  "direction": "BOTTOM", "easing": "GENTLE",  "duration": 0.32},
  "instant":  {"type": "SMART_ANIMATE", "easing": "LINEAR", "duration": 0.01},
})
PUSH = json.dumps(["Btn Open prep", "Btn Open record T2", "Btn Open access T3", "Btn Open fees S2",
                   "Btn Open meeting S3", "Btn Open contact S4", "Btn Open profile S1",
                   "Btn Open availability K4", "Btn Open timeoff K5", "Btn Open note last",
                   "Btn Open Amara", "Btn Open Chidi", "Btn Open Grace", "Btn Open Musa", "Btn Open Tunde"])
POP  = json.dumps(["Btn Back"])
SHEET = json.dumps(["Btn Open prescribe C3", "Btn Open tests C4", "Btn Open upload C5",
                    "Btn Template reason", "Btn Template exam", "Btn Template assessment", "Btn Template plan"])

linker = ("(async () => {\n"
 "  // Medra Doctor — wire the prototype, close the nav, arrange the canvas.\n"
 "  // Run after the auth bundle so the sign-out link resolves.\n"
 "  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();\n"
 "  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();\n"
 "  const pages = figma.root.children.filter(n => n.type==='PAGE');\n"
 "  const byName = {}; for (const pg of pages) for (const f of pg.children) if (f.type==='FRAME') byName[norm(f.name)] = f;\n"
 "  const F = n => byName[norm(n)];\n"
 "  const findAll = (root,t) => { const out=[]; const target=norm(t); const w=n=>{ if(n.name&&norm(n.name)===target) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 "  const allBtns = root => { const out=[]; const w=n=>{ if(n.name&&/^Btn /.test(norm(n.name))) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 f"  const M = {MOTION};\n"
 f"  const PUSH = {PUSH}, POP = {POP}, SHEET = {SHEET};\n"
 "  const ease = e => ({ type: e });\n"
 "  const mk = spec => spec.type==='SMART_ANIMATE'\n"
 "    ? { type:'SMART_ANIMATE', easing:ease(spec.easing), duration:spec.duration }\n"
 "    : { type:spec.type, direction:spec.direction, matchLayers:false, easing:ease(spec.easing), duration:spec.duration };\n"
 "  const specFor = hot => PUSH.includes(hot) ? M.push : POP.includes(hot) ? M.pop\n"
 "                       : SHEET.includes(hot) ? M.sheet : M.default;\n"
 f"  const TRN = {json.dumps(resolved)};\n"
 f"  const NAVJOBS = {json.dumps(nav_jobs)};\n"
 f"  const ORDER = {json.dumps(order_js)};\n"
 f"  const STARTS = {json.dumps(starts_js)};\n"
 f"  const OWN = {json.dumps([n for pair in NAMES.values() for n in pair])};\n"
 "  const wired = new Set(); const missing = []; let linked = 0;\n"
 "  const go = async (nd,to,spec) => { await nd.setReactionsAsync([{ trigger:{type:'ON_CLICK'},\n"
 "      actions:[{ type:'NODE', destinationId:to.id, navigation:'NAVIGATE', transition: mk(spec) }] }]);\n"
 "      wired.add(nd.id); linked++; };\n"
 "  for (const [fromN,hot,toN] of TRN){ const fr=F(fromN), to=F(toN);\n"
 "    if(!fr||!to){ missing.push(fromN+' -> '+hot+' -> '+toN); continue; }\n"
 "    const nodes=findAll(fr,hot); if(!nodes.length){ missing.push(fromN+' -> '+hot); continue; }\n"
 "    for (const nd of nodes) await go(nd,to,specFor(hot)); }\n"
 "  let navLinked = 0;\n"
 "  for (const [fromN,hot,toN] of NAVJOBS){ const fr=F(fromN), to=F(toN); if(!fr||!to) continue;\n"
 "    for (const nd of findAll(fr,hot)){ if (wired.has(nd.id)) continue; await go(nd,to,M.default); navLinked++; } }\n"
 "  let stay = 0;\n"
 "  for (const fn of OWN){ const fr=F(fn); if(!fr) continue;\n"
 "    for (const nd of allBtns(fr)){ if (wired.has(nd.id)) continue;\n"
 "      if (nd.reactions && nd.reactions.length) { wired.add(nd.id); continue; }\n"
 "      await go(nd,fr,M.instant); stay++; } }\n"
 "  const GX=170, GY=150;\n"
 "  for (const pg of pages){ const ord=ORDER[pg.name]; if(!ord) continue; let x=0, rowH=0;\n"
 "    for (const [dn] of ord){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const [,mn] of ord){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(s&&F(s)) pg.flowStartingPoints=[{ nodeId:F(s).id, name:pg.name }]; }\n"
 "  return { linked, navLinked, stayOnScreen: stay, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT, "link-doctor.js"), "w").write(linker)

ps = ["# Medra Doctor app — render + wire (Figma Desktop open + connected).",
      "# Render the auth bundle first if you want the sign-out link to resolve.",
      'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
      'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
      "figma-cli tokens import-design-md .\\DESIGN.md", ""]
for p, fids in ORDER.items():
    pg = PAGE_FIGMA[p].replace("&amp;", "&")
    ps.append(f'# ---- {pg} ----')
    ps.append(f'figma-cli eval "(async()=>{{const t=\'{pg}\';let p=figma.root.children.find(n=>n.name===t);if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"')
    if p == "Components":
        lst = ", ".join("'" + f + ".jsx'" for f in fids)
    else:
        lst = ", ".join("'" + f + "'" for fid in fids for f in (fid + "-d.jsx", fid + "-m.jsx"))
    ps.append(f'foreach ($f in @({lst})) {{ figma-cli render (Get-Content $f -Raw) }}')
    ps.append("")
ps.append("# Wire the prototype with motion and arrange the canvas")
ps.append("figma-cli run .\\link-doctor.js")
open(os.path.join(OUT, "render-doctor.ps1"), "w").write("\n".join(ps))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} screen links "
      f"· {len(nav_jobs)} nav links · {len(CMP)} component states")
for p, fs in manifest.items(): print(f"  {p}: {len(fs)}")
