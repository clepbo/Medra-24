#!/usr/bin/env python3
"""Medra — Member app, batch 2.

Closes the bottom nav: every tab now leads somewhere real.
  Visits & Virtual care  V1–V7, W1–W4   (11 screens)
  Records                R1–R9          ( 9 screens)
  Medicines              M1–M5          ( 5 screens)
  Profile & Settings     P0–P9          ( 9 screens)
  Alerts & system states N1–N2, X1–X3   ( 5 screens)
Each screen is drawn for desktop (1440) and mobile (390), so 39 screens = 78 frames,
plus the batch-2 interactive component states.

Every mobile frame is designed to fit inside 390×844 — Figma clips a fixed frame, and
`wrap="wrap"` is not honoured by figma-ds-cli, so rows are chunked with rows_of().
"""
import os, re, json, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from member_kit import *
from member2_kit import *

OUT = "/home/user/Medra-24/figma/medra-member-2"
SRC1 = "/home/user/Medra-24/figma/medra-member"
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(SRC1, "DESIGN.md"), os.path.join(OUT, "DESIGN.md"))
shutil.copyfile(os.path.join(SRC1, "validate.js"), os.path.join(OUT, "validate.js"))

frames = []; NAMES = {}; ORDER = {}
def add(page, fid, d, m):
    frames.append((page, f"{fid}-d.jsx", d)); frames.append((page, f"{fid}-m.jsx", m))
    NAMES[fid] = (re.search(r'name="([^"]+)"', d).group(1), re.search(r'name="([^"]+)"', m).group(1))
    ORDER.setdefault(page, []).append(fid)

PAGE_FIGMA = {
  "Visits":    "Medra Member — Visits &amp; Virtual Care",
  "Records":   "Medra Member — Records",
  "Medicines": "Medra Member — Medicines",
  "Profile":   "Medra Member — Profile &amp; Settings",
  "Alerts":    "Medra Member — Alerts &amp; States",
  "Components":"Medra — Interactive Components · Care",
}
SIDE = {"Home": 0, "Find": 1, "Visits": 2, "Records": 3, "Meds": 4, "Profile": 5}

def desk_stage(name, children, bg="call-ground-d.jpg"):
    """Full-bleed dark stage — used only by the virtual-visit screens, where the dashboard
    chrome would be a distraction (and a privacy problem on a shared screen)."""
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="col" image="assets/img/{bg}" '
            f'overflow="hidden">{children}</Frame>')

def mob_stage(name, children, bg="call-ground.jpg"):
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/{bg}" '
            f'overflow="hidden">{children}</Frame>')

DR_N = ("avatar-4.jpg", "Dr. Ngozi Okafor", "Cardiologist", "Garki Medical Centre")
DR_C = ("avatar-1.jpg", "Dr. Chuka Eze", "General practice", "Wuse Clinic")
DR_K = ("avatar-3.jpg", "Dr. Kemi Adeyemi", "Paediatrician", "Maitama Hospital")
DR_T = ("avatar-5.jpg", "Dr. Tunde Bello", "Neurologist", "Asokoro Specialist")

# =====================================================================================
# VISITS
# =====================================================================================
V_TABS   = tabs(["Upcoming", "Past"], 0, "Visits tab")
V_TABS_P = tabs(["Upcoming", "Past"], 1, "Visits tab")

VC_NEXT = visit_card(*DR_N, "Wed, 21 Aug · 10:30 AM", "Virtual", "soon",
    [("Join visit", "video", "teal", "Join visit"), ("Reschedule", "calendar-clock", "ghost", "Reschedule V1"),
     ("Cancel", None, "ghost", "Cancel V1")], "Visit MDR-4820-71", reason="Hypertension follow-up")
VC_SECOND = visit_card(*DR_K, "Mon, 2 Sep · 09:00 AM", "In person", "confirmed",
    [("View details", "arrow-right", "ghost", "Open visit V1b"), ("Reschedule", "calendar-clock", "ghost", "Reschedule V1")],
    "Visit MDR-4901-08", reason="Chidi — 6-year check-up")
VC_PAST_1 = visit_card(*DR_N, "Thu, 12 Jun · 11:00 AM", "In person", "completed",
    [("View summary", "file-text", "ghost", "Open note R2"), ("Book again", "repeat", "teal", "Book again")],
    "Past visit Jun")
VC_PAST_2 = visit_card(*DR_C, "Sat, 28 Apr · 08:30 AM", "Virtual", "completed",
    [("View summary", "file-text", "ghost", "Open note R2"), ("Book again", "repeat", "teal", "Book again")],
    "Past visit Apr")
VC_PAST_3 = visit_card(*DR_T, "Tue, 5 Mar · 15:00", "In person", "cancelled",
    [("Book again", "repeat", "ghost", "Book again")], "Past visit Mar",
    reason="You cancelled — clinic was too far", dim=True)

V_STATS = rows_of([
    stat_card("calendar-check", "2", "Upcoming visits", "Next in 2 days", "tint-teal.jpg"),
    stat_card("check-check", "8", "Completed", "Since Jan 2026", "tint-ocean.jpg"),
    stat_card("video", "5", "Seen by video", "No travel needed", "tint-blue.jpg"),
    stat_card("clock", "94%", "Seen on time", "Median wait 6 min", "tint-mint.jpg"),
], 4, 16)

PREP_CARD = group_card("Get ready for Wednesday", [
    prep_step(1, "Share your records", "Dr. Okafor can then see your allergies and medicines.", done=True),
    prep_step(2, "Test your camera and mic", "Takes 20 seconds — do it before the call starts."),
    prep_step(3, "Have your last readings handy", "Blood pressure, weight, anything you measured."),
], footer="Joining is free on Wi-Fi or data. Low data mode uses about 12 MB for 20 minutes.")

DIRECTIONS = group_card("Getting there", [
    list_row("hospital", "Garki Medical Centre", value=None, sub="Area 3, Garki, Abuja · 2.4 km", name="Open clinic", chevron=False),
    list_row("navigation", "Open in Maps", name="Open maps"),
    list_row("phone", "Call the clinic", value="+234 809 112 4477", name="Call clinic", chevron=False),
    list_row("car", "Parking available", sub="Free for the first hour", name="Parking", chevron=False),
])

add("Visits", "V1-visits",
    desk("Member · Visits — V1 Upcoming",
        banner("banner-visits.jpg", "MY VISITS", "2 visits coming up",
               "Everything you have booked, for you and the people you care for.",
               actions=mini_btn("Book a visit", "Book new V1", "calendar-plus", "teal", grow=False)
                     + mini_btn("Export list", "Export visits", "download", "dark", grow=False))
        + V_STATS
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{V_TABS}{VC_NEXT}{VC_SECOND}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{PREP_CARD}{DIRECTIONS}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V1 Upcoming · Mobile",
        appbar("My visits", back=False, right=circle_btn("calendar-plus", "Book new V1"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>'
          f'{V_TABS}{VC_NEXT}{VC_SECOND}</Frame>',
        nav=bottom_nav(1)))

PAST_FILTERS = rows_of([
    mini_btn("All time", "Filter all time", None, "navy"),
    mini_btn("2026", "Filter 2026", None, "ghost"),
    mini_btn("2025", "Filter 2025", None, "ghost"),
    mini_btn("Virtual only", "Filter virtual", "video", "ghost"),
], 4, 9)

add("Visits", "V2-past",
    desk("Member · Visits — V2 Past",
        banner("banner-visits.jpg", "MY VISITS", "8 visits on record",
               "Every past consultation, with the note the doctor wrote.",
               actions=mini_btn("Download all summaries", "Export visits", "download", "dark", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{V_TABS_P}{PAST_FILTERS}'
          f'{VC_PAST_1}{VC_PAST_2}{VC_PAST_3}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'{group_card("This year", [list_row("check-check","Completed",value="8",name="Stat completed",chevron=False),list_row("circle-x","Cancelled",value="1",name="Stat cancelled",chevron=False),list_row("circle-slash","Missed",value="0",name="Stat missed",chevron=False),list_row("banknote","Spent on care",value="₦96,000",name="Stat spent",chevron=False)])}'
          f'{note("file-text","Every completed visit adds a note to your records — you keep it even if you change clinic.","info")}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V2 Past · Mobile",
        appbar("My visits", back=False, right=circle_btn("download", "Export visits"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>'
          f'{V_TABS_P}{rows_of([mini_btn("All time","Filter all time",None,"navy"),mini_btn("2026","Filter 2026",None,"ghost")],2,9)}'
          f'{VC_PAST_1}{VC_PAST_3}</Frame>',
        nav=bottom_nav(1)))

V3_EMPTY = empty_state("calendar-plus", "No visits booked yet",
    "When you book a doctor, it shows up here with everything you need — the time, the place, and a link if it's a video visit.",
    primary=cta("Find a doctor", "Find doctor V3", "search"),
    secondary=ghost("See how Medra works", "How it works V3", "book-open"))
V3_WHY = group_card("What you get on every visit", [
    list_row("badge-check", "Only MDCN-verified doctors", sub="We check the register before a doctor can be booked", name="Why verified", chevron=False),
    list_row("clock", "Real availability", sub="If a slot shows here, it is genuinely open", name="Why real", chevron=False),
    list_row("message-square-text", "SMS confirmation", sub="Works even when you have no data", name="Why sms", chevron=False),
    list_row("clipboard-list", "A note you keep", sub="The doctor's summary is added to your records", name="Why note", chevron=False),
])

add("Visits", "V3-visits-empty",
    desk("Member · Visits — V3 No Visits",
        banner("banner-visits.jpg", "MY VISITS", "Nothing booked yet",
               "Find a verified doctor in Abuja and book in about a minute.",
               actions=mini_btn("Find a doctor", "Find doctor V3", "search", "teal", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col">{V3_EMPTY}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{V3_WHY}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V3 No Visits · Mobile",
        appbar("My visits", back=False)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>'
          f'{V_TABS}{V3_EMPTY}</Frame>',
        nav=bottom_nav(1)))

# ---------------- V4 visit detail
def stat_cell_v4(ic, big, small):
    return (f'<Frame grow={{1}} flex="col" gap={{4}} items="center" py={{14}} px={{8}} rounded={{18}} bg="var:bg/subtle">'
            f'{I(ic,17,A_IC)}{T(14,"bold","var:text/strong",big)}{T(11,"regular","var:text/muted",small)}</Frame>')

V4_HEAD = (f'<Frame w="fill" flex="col" gap={{16}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" justify="between" items="center">{status_pill("soon")}'
           f'{T(12,"medium","var:text/muted","Ref MDR-4820-71")}</Frame>'
           f'<Frame w="fill" flex="row" gap={{15}} items="center">'
           f'<Image image="assets/img/avatar-4.jpg" w={{72}} h={{72}} rounded={{24}} />'
           f'<Frame grow={{1}} flex="col" gap={{4}}>'
           f'<Frame flex="row" gap={{8}} items="center">{T(19,"bold","var:text/strong","Dr. Ngozi Okafor")}'
           f'{I("badge-check",17,T_IC)}</Frame>'
           f'{T(13,"regular","var:text/muted","Cardiologist · MDCN verified")}</Frame></Frame>'
           f'<Frame w="fill" flex="row" gap={{10}}>'
           f'{stat_cell_v4("calendar-days","Wed, 21 Aug","Date")}'
           f'{stat_cell_v4("clock","10:30 AM","30 minutes")}'
           f'{stat_cell_v4("video","Virtual","Video call")}</Frame></Frame>')

V4_JOIN_ROWS = [
    prep_step(1, "Open Medra at 10:25", "We will remind you by SMS and notification."),
    prep_step(2, "Tap Join visit", "The button turns on 10 minutes before the time."),
    prep_step(3, "No data? Ask for a phone call", "The clinic can ring you instead — nothing is lost."),
]
V4_JOIN   = group_card("How to join", V4_JOIN_ROWS,
                       footer="If Dr. Okafor is running late, you will see the wait time on this screen.")
V4_JOIN_M = group_card("How to join", V4_JOIN_ROWS, p=16)

V4_SHARE_NUDGE = (f'<Frame w="fill" flex="row" gap={{13}} items="center" p={{16}} rounded={{22}} bg="var:state/info-bg">'
                  f'{I("share-2",20,A_IC)}'
                  f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Share your records first")}'
                  f'{T(12,"regular","var:text/muted","Dr. Okafor sees only what you allow, only until the visit ends.",w="fill")}</Frame>'
                  f'{mini_btn("Share","Share R5","shield-check","teal",grow=False)}</Frame>')

V4_DETAILS = group_card("Visit details", [
    list_row("file-text", "Reason for visit", sub="Hypertension follow-up · BP has been 138/88 at home", name="Reason V4", chevron=False),
    list_row("banknote", "Consultation fee", value="₦15,000", sub="Paid after the visit — card, transfer or cash", name="Fee V4", chevron=False),
    list_row("user", "Who this is for", value="Myself", name="Who V4", chevron=False),
    list_row("bell-ring", "Reminders", value="SMS + push", sub="24 hours and 2 hours before", name="Reminders V4"),
])
V4_ACTIONS_D = (f'<Frame w="fill" flex="col" gap={{11}}>'
                f'{cta("Join visit","Join visit","video")}'
                f'{ghost("Reschedule","Reschedule V4","calendar-clock")}'
                f'{ghost("Cancel this visit","Cancel V4","circle-x")}'
                f'{ghost("Add to calendar","Add calendar V4","calendar-plus")}</Frame>')

add("Visits", "V4-visit",
    desk("Member · Visits — V4 Visit Detail",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","All visits")}</Frame>'
        f'{mini_btn("Share this visit","Share visit V4","share-2","ghost",grow=False)}</Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{V4_HEAD}{V4_SHARE_NUDGE}{V4_DETAILS}{V4_JOIN}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{V4_ACTIONS_D}{DIRECTIONS}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V4 Visit Detail · Mobile",
        appbar("Visit", right=circle_btn("share-2", "Share visit V4"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{V4_HEAD}{V4_SHARE_NUDGE}'
          f'<Frame w="fill" flex="row" gap={{10}}>'
          f'{mini_btn("Join visit","Join visit","video","teal")}'
          f'{mini_btn("Reschedule","Reschedule V4","calendar-clock","ghost")}</Frame>'
          f'{V4_JOIN_M}</Frame>',
        nav=bottom_nav(1)))

# ---------------- V5 reschedule
V5_CURRENT = (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{16}} rounded={{20}} bg="var:neutral/50">'
              f'{I("calendar-x",18,M_IC)}'
              f'<Frame grow={{1}} flex="col" gap={{2}}>{T(12,"regular","var:text/muted","Currently booked")}'
              f'{T(15,"semibold","var:text/faint","Wed, 21 Aug · 10:30 AM")}</Frame>'
              f'{status_pill("confirmed","Will be released")}</Frame>')
V5_POLICY = note("info", "Rescheduling is free up to 4 hours before your visit. After that the clinic may charge a ₦2,000 late-change fee — you will see it before you confirm.", "info")
V5_BODY = (f'{V5_CURRENT}'
           f'{card(T(16,"bold","var:text/strong","Pick a new day")+date_strip(3),p=20,gap=14)}'
           f'{card(T(15,"semibold","var:text/default","Open times with Dr. Okafor")+slot_grid("11:00"),p=20,gap=13)}'
           f'{V5_POLICY}')

add("Visits", "V5-reschedule",
    desk("Member · Visits — V5 Reschedule",
        head_chip([("Move this", False), ("visit", True)], 30)
        + T(15, "regular", "var:text/muted", "Your current slot stays yours until you confirm the new one.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{20}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{V5_BODY}</Frame>'
          f'<Frame w={{368}} flex="col" gap={{16}}>'
          f'{group_card("New booking", [list_row("user","Doctor",value="Dr. Ngozi Okafor",name="V5 doc",chevron=False),list_row("calendar-days","New date",value="Thu, 22 Aug",name="V5 date",chevron=False),list_row("clock","New time",value="11:00 AM",name="V5 time",chevron=False),list_row("banknote","Change fee",value="₦0",sub="More than 4 hours ahead",name="V5 fee",chevron=False)])}'
          f'{cta("Confirm new time","Confirm reschedule","check")}'
          f'{ghost("Keep my original time","Keep original V5","undo-2")}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V5 Reschedule · Mobile",
        appbar("Reschedule")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{V5_CURRENT}{date_strip(3)}'
          f'{card(T(15,"semibold","var:text/default","Open times")+slot_grid("11:00"),p=16,gap=12)}'
          f'<Frame grow={{1}} />{cta("Confirm 11:00 AM","Confirm reschedule","check")}'
          f'{link("","Keep my original time","Keep original V5")}</Frame>'))

# ---------------- V6 cancel
V6_REASONS = (f'<Frame w="fill" flex="col" gap={{2}}>'
              f'{radio_row("I feel better now", on=True, name="Cancel reason better")}{hr()}'
              f'{radio_row("Something came up", name="Cancel reason busy")}{hr()}'
              f'{radio_row("I found an earlier appointment", name="Cancel reason earlier")}{hr()}'
              f'{radio_row("The clinic is too far", name="Cancel reason far")}{hr()}'
              f'{radio_row("Cost", sub="Tell us and we can show you cheaper options", name="Cancel reason cost")}{hr()}'
              f'{radio_row("Another reason", name="Cancel reason other")}</Frame>')
V6_WARN = note("triangle-alert", "Cancelling releases your 10:30 slot immediately — someone else can take it. You can rebook, but the same time may not be free.", "warn")

add("Visits", "V6-cancel",
    desk("Member · Visits — V6 Cancel Visit",
        head_chip([("Cancel this", False), ("visit", True)], 30)
        + f'<Frame w="fill" flex="row" gap={{20}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>'
          f'{V5_CURRENT}'
          f'{group_card("Why are you cancelling?", V6_REASONS, footer="Your answer is only used to improve Medra — the doctor does not see it.")}'
          f'{field("Anything you want the clinic to know? (optional)","message-square-text","e.g. I will rebook for next month")}'
          f'{V6_WARN}</Frame>'
          f'<Frame w={{368}} flex="col" gap={{16}}>'
          f'{group_card("What happens", [list_row("circle-x","Your slot is released",sub="Straight away",name="V6 slot",chevron=False),list_row("banknote","Nothing to refund",sub="You pay after the visit, so no money is held",name="V6 refund",chevron=False),list_row("clipboard-list","Your records stay",sub="Past visits are never removed",name="V6 records",chevron=False)])}'
          f'<Frame w="fill" flex="col" gap={{11}}>'
          f'<Frame name="Btn Confirm cancel" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{24}} py={{16}} rounded={{999}} bg="var:state/error-bg">'
          f'{I("circle-x",18,ERR_IC)}{T(15,"semibold","var:state/error","Cancel my visit")}</Frame>'
          f'{cta("Keep my visit","Keep visit V6","check")}</Frame></Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V6 Cancel Visit · Mobile",
        appbar("Cancel visit")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{group_card("Why are you cancelling?", V6_REASONS, p=16)}'
          f'{V6_WARN}<Frame grow={{1}} />'
          f'<Frame name="Btn Confirm cancel" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{24}} py={{16}} rounded={{999}} bg="var:state/error-bg">'
          f'{I("circle-x",18,ERR_IC)}{T(15,"semibold","var:state/error","Cancel my visit")}</Frame>'
          f'{cta("Keep my visit","Keep visit V6","check")}</Frame>'))

# ---------------- V7 cancelled
V7 = (f'<Frame w="fill" flex="col" gap={{16}} items="center">'
      f'{big_icon("calendar-x","warn",96)}'
      f'{T(23,"bold","var:text/strong","Your visit is cancelled")}'
      f'{T(15,"regular","var:text/muted","We have told Garki Medical Centre. Nothing was charged, and your records are untouched.",w="fill",align="center")}'
      f'{group_card("", [list_row("user","Dr. Ngozi Okafor",value="Cardiologist",name="V7 doc",chevron=False),list_row("calendar-x","Wed, 21 Aug · 10:30 AM",value="Released",name="V7 slot",chevron=False),list_row("message-square-text","SMS sent",value="+234 801 234 5678",name="V7 sms",chevron=False)])}'
      f'{note("info","Feeling unwell again? Dr. Okafor has an opening on Thursday at 11:00 — you can rebook in two taps.","info")}</Frame>')

add("Visits", "V7-cancelled",
    desk("Member · Visits — V7 Cancelled",
        f'<Frame w="fill" flex="row" justify="center" pt={{10}}>'
        f'<Frame w={{620}} flex="col" gap={{18}}>{V7}'
        f'<Frame w="fill" flex="row" gap={{12}}>'
        f'<Frame grow={{1}} flex="col">{ghost("Back to my visits","Back visits V7","arrow-left")}</Frame>'
        f'<Frame grow={{1}} flex="col">{cta("Book another time","Rebook V7","calendar-plus")}</Frame></Frame></Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Visits — V7 Cancelled · Mobile",
        appbar(None, back=False, right=circle_btn("x", "Back visits V7"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{6}} pb={{10}}>{V7}'
          f'<Frame grow={{1}} />{cta("Book another time","Rebook V7","calendar-plus")}'
          f'{ghost("Back to my visits","Back visits V7")}</Frame>'))

# =====================================================================================
# VIRTUAL VISIT
# =====================================================================================
PHASE2 = (f'<Frame flex="row" gap={{7}} items="center" px={{12}} py={{7}} rounded={{999}} bg="var:state/warning-bg">'
          f'{I("sparkles",13,WARN_IC)}{T(11,"semibold","var:state/warning","PHASE 2 · not in the MVP")}</Frame>')
W1_CHECKS = (f'<Frame w="fill" flex="col" gap={{14}} p={{20}} rounded={{24}} bg="var:bg/band-2">'
             f'{eyebrow("BEFORE YOU JOIN","var:brand/teal")}'
             f'{check_line("Camera is working","ok","Front camera · you can see yourself below")}'
             f'{check_line("Microphone is working","ok","Say something — the bars should move")}'
             f'{check_line("Connection is good enough","warn","3.1 Mbps · fine for video, may drop to audio")}'
             f'<Frame w="fill" flex="row" gap={{12}} items="center">{level_meter()}'
             f'{T(12,"regular","var:text/on-dark-muted","Mic level",w="fill")}</Frame></Frame>')
W1_OPTS = (f'<Frame w="fill" flex="col" gap={{12}} p={{20}} rounded={{24}} bg="var:bg/band-2">'
           f'<Frame w="fill" flex="row" gap={{13}} items="center">'
           f'<Frame w={{36}} h={{36}} rounded={{12}} bg="#143352" flex="col" justify="center" items="center">{I("signal",17,T_IC)}</Frame>'
           f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"medium","var:text/on-dark","Low data mode")}'
           f'{T(11,"regular","var:text/on-dark-muted","Smaller video, about 12 MB for 20 minutes",w="fill")}</Frame>'
           f'<Frame name="Btn Low data" w={{50}} h={{29}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden" flex="row" justify="end" items="center" px={{4}}><Ellipse w={{21}} h={{21}} bg="#FFFFFF" /></Frame></Frame>'
           f'{hr("#143352")}'
           f'<Frame w="fill" flex="row" gap={{13}} items="center">'
           f'<Frame w={{36}} h={{36}} rounded={{12}} bg="#143352" flex="col" justify="center" items="center">{I("phone-call",17,T_IC)}</Frame>'
           f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"medium","var:text/on-dark","Call me on the phone instead")}'
           f'{T(11,"regular","var:text/on-dark-muted","No data needed — the clinic rings +234 801 234 5678",w="fill")}</Frame>'
           f'{mini_btn("Use call","Phone instead W1",None,"dark",grow=False)}</Frame></Frame>')
W1_WAIT = (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{16}} rounded={{20}} bg="#143352">'
           f'<Image image="assets/img/avatar-4.jpg" w={{40}} h={{40}} rounded={{999}} />'
           f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/on-dark","Dr. Okafor joins at 10:30")}'
           f'{T(11,"regular","var:text/on-dark-muted","You will wait here — no queue, no dial-in code",w="fill")}</Frame>'
           f'{status_pill("pending","2 min")}</Frame>')

add("Visits", "W1-precall",
    desk_stage("Member · Virtual — W1 Pre-call Check",
        f'<Frame w="fill" flex="row" justify="between" items="center" px={{40}} pt={{26}}>'
        f'<Image image="assets/logo/logo-white.png" w={{92}} h={{68}} />'
        f'<Frame flex="row" gap={{12}} items="center">{PHASE2}'
        f'<Frame name="Btn Leave precall" flex="row" gap={{8}} items="center" px={{15}} py={{10}} rounded={{999}} bg="var:bg/band-2">'
        f'{I("x",16,W_IC)}{T(13,"medium","var:text/on-dark","Leave")}</Frame></Frame></Frame>'
        f'<Frame grow={{1}} w="fill" flex="row" gap={{34}} justify="center" items="center" px={{56}} py={{28}}>'
        f'<Frame w={{620}} h={{460}} rounded={{28}} image="assets/img/call-self.jpg" overflow="hidden" flex="col" justify="between" p={{18}}>'
        f'<Frame w="fill" flex="row" justify="end">{status_pill("live","Camera on")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{12}} justify="center">'
        f'{call_btn("mic","Toggle mic W1","on",52,"Mic on")}'
        f'{call_btn("video","Toggle cam W1","on",52,"Camera on")}'
        f'{call_btn("volume-2","Test speaker W1","dark",52,"Speaker")}</Frame></Frame>'
        f'<Frame w={{460}} flex="col" gap={{16}}>'
        f'{eyebrow("VIRTUAL VISIT","var:brand/teal")}'
        f'{head_chip([("Ready to",False),("join?",True)],32,"var:text/on-dark")}'
        f'{W1_CHECKS}{W1_OPTS}{W1_WAIT}'
        f'{cta("Join the visit","Join call W1","video")}</Frame></Frame>'),
    mob_stage("Member · Virtual — W1 Pre-call Check · Mobile",
        statusbar(dark=True)
        + f'<Frame w="fill" flex="row" justify="between" items="center" px={{20}} pt={{8}} pb={{6}}>'
          f'{circle_btn("arrow-left","Leave precall",dark=True)}{PHASE2}'
          f'{circle_btn("circle-help","Help call",dark=True)}</Frame>'
          f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{20}}>'
          f'<Frame w="fill" h={{250}} rounded={{26}} image="assets/img/call-self.jpg" overflow="hidden" flex="col" justify="between" p={{14}}>'
          f'<Frame w="fill" flex="row" justify="end">{status_pill("live","Camera on")}</Frame>'
          f'<Frame w="fill" flex="row" gap={{12}} justify="center">'
          f'{call_btn("mic","Toggle mic W1","on",48)}'
          f'{call_btn("video","Toggle cam W1","on",48)}'
          f'{call_btn("volume-2","Test speaker W1","dark",48)}</Frame></Frame>'
          f'{W1_CHECKS}{W1_WAIT}'
          f'<Frame grow={{1}} />{cta("Join the visit","Join call W1","video")}'
          f'<Frame name="Btn Phone instead W1" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{20}} py={{14}} rounded={{999}} bg="var:bg/band-2">'
          f'{I("phone-call",16,W_IC)}{T(14,"semibold","var:text/on-dark","Call me on the phone instead")}</Frame></Frame>'))

# ---------------- W2 in call
W2_CONTROLS_M = call_controls([("mic", "Toggle mic W2", "on", 54, "Mute"),
                               ("video", "Toggle cam W2", "on", 54, "Camera"),
                               ("message-circle", "Open chat W2", "dark", 54, "Chat"),
                               ("share-2", "Share record W2", "dark", 54, "Records"),
                               ("phone-off", "End call W2", "end", 54, "End")])
W2_CAPTION = (f'<Frame w="fill" flex="row" gap={{10}} items="start" px={{16}} py={{12}} rounded={{18}} bg="var:bg/band-2">'
              f'{I("type",15,T_IC)}'
              f'{T(12,"regular","var:text/on-dark","“Your readings look better than June. Keep taking the Amlodipine every morning.”",w="fill")}</Frame>')

add("Visits", "W2-incall",
    desk_stage("Member · Virtual — W2 In Call",
        f'<Frame grow={{1}} w="fill" flex="row" gap={{20}} p={{24}}>'
        f'<Frame grow={{1}} h="fill" flex="col" justify="between" rounded={{28}} image="assets/img/call-doctor-d.jpg" overflow="hidden">'
        f'{call_plate("Dr. Ngozi Okafor","Cardiologist · Garki Medical Centre")}'
        f'<Frame w="fill" flex="row" justify="end" px={{18}}>{call_pip("You",176,124)}</Frame>'
        f'<Frame w="fill" flex="col" gap={{10}} px={{18}} pb={{6}}>{W2_CAPTION}'
        f'{call_controls([("mic","Toggle mic W2","on",56,"Mute"),("video","Toggle cam W2","on",56,"Camera"),("screen-share","Share screen W2","dark",56,"Share"),("message-circle","Open chat W2","dark",56,"Chat"),("share-2","Share record W2","dark",56,"Records"),("phone-off","End call W2","end",56,"End")])}'
        f'</Frame></Frame>'
        f'<Frame w={{360}} h="fill" flex="col" gap={{14}} p={{20}} rounded={{28}} bg="var:bg/band-2">'
        f'<Frame w="fill" flex="row" justify="between" items="center">{eyebrow("DURING THE VISIT","var:brand/teal")}{PHASE2}</Frame>'
        f'{T(17,"bold","var:text/on-dark","Dr. Okafor can see")}'
        f'{check_line("Allergies and medicines","ok","Always shared during a visit")}'
        f'{check_line("Your last 3 visits","ok","You allowed this until 11:00")}'
        f'{check_line("Lab results","bad","Not shared — tap to allow")}'
        f'{hr("#143352")}'
        f'{T(13,"semibold","var:text/on-dark","Quick actions")}'
        f'{mini_btn("Share a lab result now","Share record W2","share-2","onpanel",full=True)}'
        f'{mini_btn("Ask for a written note","Ask note W2","notebook-pen","onpanel",full=True)}'
        f'{mini_btn("Report a problem","Report call W2","flag","onpanel",full=True)}'
        f'<Frame grow={{1}} />'
        f'{note("shield-check","This call is end-to-end encrypted. Medra never records video or audio.","info")}</Frame></Frame>'),
    mob_stage("Member · Virtual — W2 In Call · Mobile",
        f'<Frame grow={{1}} w="fill" flex="col" justify="between" image="assets/img/call-doctor-m.jpg" overflow="hidden">'
        f'{statusbar(dark=True)}'
        f'<Frame w="fill" flex="row" justify="center" pt={{6}}>{PHASE2}</Frame>'
        f'{call_plate("Dr. Ngozi Okafor","Cardiologist")}'
        f'<Frame w="fill" flex="row" justify="end" px={{16}}>{call_pip()}</Frame>'
        f'<Frame grow={{1}} />'
        f'<Frame w="fill" flex="col" gap={{10}} px={{16}} pb={{18}}>{W2_CAPTION}{W2_CONTROLS_M}</Frame></Frame>',
        ))

# ---------------- W3 summary
W3_SUMMARY = group_card("What Dr. Okafor recorded", [
    list_row("stethoscope", "Assessment", sub="Hypertension, well controlled on current dose", name="W3 assess", chevron=False),
    list_row("pill", "Prescription", value="2 medicines", sub="Amlodipine 5 mg · Metformin 500 mg", name="W3 rx"),
    list_row("flask-conical", "Tests ordered", value="1", sub="Fasting blood sugar — any Medra lab", name="W3 tests"),
    list_row("calendar-clock", "Follow-up", value="In 3 months", sub="We will remind you in November", name="W3 followup"),
], footer="This note is now in your records. Dr. Okafor signed it — it cannot be changed afterwards.")

W3 = (f'<Frame w="fill" flex="col" gap={{16}} items="center">'
      f'{big_icon("circle-check","ok",96)}'
      f'{T(23,"bold","var:text/strong","Visit finished")}'
      f'{T(15,"regular","var:text/muted","You spoke with Dr. Ngozi Okafor for 12 minutes. The summary is saved to your records.",w="fill",align="center")}'
      f'<Frame w="fill" flex="row" gap={{10}}>'
      f'{mini_btn("Open the note","Open note R2","file-text","ghost")}'
      f'{mini_btn("Download PDF","Download note","download","ghost")}</Frame></Frame>')
W3_M = (f'<Frame w="fill" flex="col" gap={{14}} items="center">'
        f'{big_icon("circle-check","ok",88)}'
        f'{T(22,"bold","var:text/strong","Visit finished")}'
        f'{T(14,"regular","var:text/muted","12 minutes with Dr. Ngozi Okafor. The summary is in your records.",w="fill",align="center")}'
        f'{mini_btn("Open the note","Open note R2","file-text","ghost")}</Frame>')
W3_SUMMARY_M = group_card("What Dr. Okafor recorded", [
    list_row("stethoscope", "Assessment", sub="Hypertension, well controlled", name="W3 assess", chevron=False),
    list_row("pill", "Prescription", value="2 medicines", name="W3 rx"),
    list_row("flask-conical", "Tests ordered", value="1", name="W3 tests"),
    list_row("calendar-clock", "Follow-up", value="In 3 months", name="W3 followup"),
], p=16)
W3_RATE = group_card("How was it?", [
    f'<Frame w="fill" flex="row" gap={{10}} justify="center" py={{6}}>'
    + "".join(f'<Frame name="Btn Rate {n}" w={{48}} h={{48}} rounded={{999}} bg="var:neutral/50" flex="col" justify="center" items="center">{I("star",21,WARN_IC)}</Frame>' for n in range(1, 6))
    + '</Frame>',
    field("Anything to add? (optional)", "message-square-text", "The video was clear and she explained everything"),
], footer="Ratings are anonymous and only shown as an average on the doctor's profile.")

add("Visits", "W3-callend",
    desk("Member · Virtual — W3 Visit Summary",
        f'<Frame w="fill" flex="row" gap={{20}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{W3}{W3_SUMMARY}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{W3_RATE}'
        f'{cta("Back to my visits","Back visits W3","arrow-left")}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Virtual — W3 Visit Summary · Mobile",
        appbar(None, back=False, right=circle_btn("x", "Back visits W3"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{10}}>'
          f'{W3_M}{W3_SUMMARY_M}<Frame grow={{1}} />'
          f'{cta("Rate this visit","Rate 5","star")}</Frame>'))

# ---------------- W4 connection lost
W4 = (f'<Frame w="fill" flex="col" gap={{16}} items="center" p={{26}} rounded={{28}} bg="var:bg/band-2">'
      f'<Frame w={{86}} h={{86}} rounded={{999}} bg="#143352" flex="col" justify="center" items="center">'
      f'{I("wifi-off",38,WARN_IC)}</Frame>'
      f'{PHASE2}{T(21,"bold","var:text/on-dark","Connection lost")}'
      f'{T(14,"regular","var:text/on-dark-muted","We are trying to get you back in — attempt 2 of 5. Dr. Okafor can still see you in the waiting room, so your visit is not gone.",w="fill",align="center")}'
      f'{check_line("Your visit is saved","ok","Nothing you or the doctor recorded is lost")}'
      f'{check_line("Reconnecting…","wait","Usually takes a few seconds")}</Frame>')
W4_FALLBACK = (f'<Frame w="fill" flex="col" gap={{11}}>'
               f'{cta("Try again now","Retry call W4","refresh-cw")}'
               f'<Frame name="Btn Audio only W4" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{20}} py={{15}} rounded={{999}} bg="var:bg/band-2">'
               f'{I("volume-2",17,W_IC)}{T(15,"semibold","var:text/on-dark","Switch to audio only")}</Frame>'
               f'<Frame name="Btn Phone instead W4" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{20}} py={{15}} rounded={{999}} bg="var:bg/band-2">'
               f'{I("phone-call",17,W_IC)}{T(15,"semibold","var:text/on-dark","Ask the clinic to call my phone")}</Frame>'
               f'<Frame name="Btn End call W4" w="fill" flex="row" justify="center" px={{20}} py={{14}} rounded={{999}}>'
               f'{T(14,"semibold","var:text/on-dark-muted","Leave the visit")}</Frame></Frame>')

add("Visits", "W4-lost",
    desk_stage("Member · Virtual — W4 Connection Lost",
        f'<Frame grow={{1}} w="fill" flex="row" gap={{28}} justify="center" items="center" px={{56}}>'
        f'<Frame w={{560}} h={{420}} rounded={{28}} image="assets/img/call-nosignal.jpg" overflow="hidden" flex="col" justify="center" items="center" gap={{14}}>'
        f'{I("video-off",56,DIM)}{T(15,"medium","var:text/on-dark-muted","Video paused")}</Frame>'
        f'<Frame w={{460}} flex="col" gap={{16}}>{W4}{W4_FALLBACK}</Frame></Frame>',
        "call-nosignal.jpg"),
    mob_stage("Member · Virtual — W4 Connection Lost · Mobile",
        statusbar(dark=True)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{16}} px={{20}} pt={{18}} pb={{22}}>'
          f'{W4}<Frame grow={{1}} />{W4_FALLBACK}</Frame>',
        "call-nosignal.jpg"))

# =====================================================================================
# RECORDS  — the reason to switch to Medra: the history is yours, and it travels with you
# =====================================================================================
R_TABS = tabs(["All", "Visits", "Labs", "Medicines"], 0, "Records tab")
R_FILTERS = rows_of([
    mini_btn("All", "Filter records all", None, "navy"),
    mini_btn("Consultations", "Filter records visits", "stethoscope", "ghost"),
    mini_btn("Lab results", "Filter records labs", "flask-conical", "ghost"),
    mini_btn("Prescriptions", "Filter records rx", "pill", "ghost"),
    mini_btn("Vitals", "Filter records vitals", "activity", "ghost"),
    mini_btn("My uploads", "Filter records uploads", "file-plus", "ghost"),
], 3, 9)

R_TIMELINE = timeline([
    ("month", "AUGUST 2026"),
    ("item", ("14", "Aug", "vitals", "Blood pressure 128/82", "You measured at home · pulse 74", "Open vitals R4", "new")),
    ("item", ("02", "Aug", "upload", "Scan of my old NHIS card", "You uploaded · 1 page", "Open upload", None, "thumb-scan.jpg")),
    ("month", "JUNE 2026"),
    ("item", ("12", "Jun", "visit", "Hypertension review", "Dr. Ngozi Okafor · Garki Medical Centre", "Open note R2")),
    ("item", ("12", "Jun", "prescription", "Amlodipine 5 mg · 30 days", "Prescribed by Dr. Ngozi Okafor", "Open med M2")),
    ("item", ("12", "Jun", "lab", "Full blood count", "Garki Medical Centre lab · 1 value out of range", "Open lab R3", None, "thumb-lab.jpg")),
    ("month", "APRIL 2026"),
    ("item", ("28", "Apr", "visit", "Malaria — treated", "Dr. Chuka Eze · Wuse Clinic", "Open note R2")),
    ("item", ("28", "Apr", "vaccine", "Yellow fever booster", "Wuse Clinic · certificate attached", "Open vaccine")),
])
R_TIMELINE_M = timeline([
    ("month", "AUGUST 2026"),
    ("item", ("14", "Aug", "vitals", "Blood pressure 128/82", "You measured at home", "Open vitals R4", "new")),
    ("month", "JUNE 2026"),
    ("item", ("12", "Jun", "visit", "Hypertension review", "Dr. Ngozi Okafor", "Open note R2")),
    ("item", ("12", "Jun", "lab", "Full blood count", "1 value out of range", "Open lab R3", None, "thumb-lab.jpg")),
], gutter=44)

R_SHARE_BANNER = (f'<Frame name="Btn Open access R6" w="fill" flex="row" gap={{13}} items="center" p={{16}} rounded={{22}} bg="var:state/info-bg">'
                  f'{I("share-2",19,A_IC)}'
                  f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","1 doctor can see your records")}'
                  f'{T(12,"regular","var:text/muted","Dr. Ngozi Okafor · until 21 Aug, 11:00. You can stop this any time.",w="fill")}</Frame>'
                  f'{I("chevron-right",18,A_IC)}</Frame>')

R_SUMMARY = group_card("Your health summary", [
    list_row("droplet", "Blood group", value="O+", name="Blood group", chevron=False),
    list_row("triangle-alert", "Allergies", value="Penicillin", name="Allergies", tint="var:state/warning-bg", chevron=False),
    list_row("heart-pulse", "Conditions", value="Hypertension", sub="Diagnosed Jun 2026", name="Conditions", chevron=False),
    list_row("pill", "Current medicines", value="2", name="Open meds R1"),
    list_row("syringe", "Immunisations", value="Up to date", name="Open vaccines"),
], footer="Allergies and current medicines are shared automatically with any doctor you see, so nobody prescribes something unsafe.")

R_STATS = rows_of([
    stat_card("clipboard-list", "14", "Records", "Across 3 clinics", "tint-teal.jpg"),
    stat_card("stethoscope", "8", "Consultations", "Since Jan 2026", "tint-ocean.jpg"),
    stat_card("flask-conical", "4", "Lab results", "1 needs attention", "tint-amber.jpg"),
    stat_card("shield-check", "1", "Active share", "Expires in 6 days", "tint-blue.jpg"),
], 4, 16)

add("Records", "R1-records",
    desk("Member · Records — R1 Timeline",
        banner("banner-records.jpg", "MY RECORDS", "Your history, in one place",
               "Every visit, result and prescription — yours to keep, even if you change clinic or city.",
               actions=mini_btn("Add a record", "Open upload R7", "file-plus", "teal", grow=False)
                     + mini_btn("Share access", "Share R5", "share-2", "dark", grow=False))
        + R_STATS
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R_SHARE_BANNER}'
          f'<Frame w="fill" flex="row" justify="between" items="center">{R_FILTERS}'
          f'<Frame name="Btn Search records" flex="row" gap={{8}} items="center" px={{15}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
          f'{I("search",15,N_IC)}{T(13,"medium","var:text/default","Search")}</Frame></Frame>'
          f'{R_TIMELINE}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{R_SUMMARY}'
          f'{group_card("Bring in older records", [list_row("file-plus","Photograph a paper result",sub="We read the date and file it for you",name="Open upload R7"),list_row("hospital","Ask a clinic to send them",sub="We send the request — most reply in 3 days",name="Request clinic"),list_row("printer","Print a summary for a walk-in",sub="One page, with a QR code",name="Print summary")])}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R1 Timeline · Mobile",
        appbar("My records", back=False, right=circle_btn("file-plus", "Open upload R7"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{searchbar("Search your records","Search records")}'
          f'{R_SHARE_BANNER}'
          f'{rows_of([mini_btn("All","Filter records all",None,"navy"),mini_btn("Visits","Filter records visits","stethoscope","ghost"),mini_btn("Labs","Filter records labs","flask-conical","ghost")],3,8)}'
          f'{R_TIMELINE_M}</Frame>',
        nav=bottom_nav(2)))

# ---------------- R2 consultation note
R2_HEAD = (f'<Frame w="fill" flex="col" gap={{15}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" justify="between" items="center">'
           f'<Frame flex="row" gap={{8}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:state/info-bg">'
           f'{I("stethoscope",13,A_IC)}{T(11,"semibold","var:text/default","Consultation")}</Frame>'
           f'{T(12,"medium","var:text/muted","12 June 2026 · 11:00")}</Frame>'
           f'{T(21,"bold","var:text/strong","Hypertension review")}'
           f'<Frame w="fill" flex="row" gap={{13}} items="center">'
           f'<Image image="assets/img/avatar-4.jpg" w={{48}} h={{48}} rounded={{16}} />'
           f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Dr. Ngozi Okafor")}'
           f'{T(12,"regular","var:text/muted","Cardiologist · Garki Medical Centre")}</Frame>'
           f'{status_pill("completed")}</Frame></Frame>')

R2_NOTE = group_card("The doctor's note", [
    note_section("Why you came", "Follow-up for high blood pressure. Home readings around 138/88 for two weeks. No chest pain, no shortness of breath, no swelling.", "message-square-text"),
    note_section("Examination", "BP 136/86 seated, pulse 78 regular. Weight 74 kg. Heart and lungs normal.", "stethoscope"),
    note_section("Assessment", "Hypertension, partially controlled. No sign of organ damage.", "clipboard-check"),
    note_section("Plan", "Continue Amlodipine 5 mg every morning. Reduce added salt. Walk 30 minutes, five days a week. Fasting blood sugar test before the next visit. Review in three months, sooner if readings go above 160/100.", "list-checks"),
])
R2_LINKED = group_card("Came out of this visit", [
    list_row("pill", "Amlodipine 5 mg", value="30 days", sub="Prescription · still active", name="Open med M2"),
    list_row("flask-conical", "Fasting blood sugar", value="Ordered", sub="Not done yet — any Medra lab", name="Open lab R3"),
    list_row("activity", "BP 136/86 recorded", sub="Added to your vitals trend", name="Open vitals R4"),
    list_row("calendar-clock", "Review in 3 months", value="Sep 2026", sub="We will remind you", name="Open visit V4"),
])
R2_PROV = provenance("Dr. Ngozi Okafor", "MDCN 71482", "12 Jun 2026, 11:42")

add("Records", "R2-note",
    desk("Member · Records — R2 Consultation Note",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","All records")}</Frame>'
        f'<Frame flex="row" gap={{10}} items="center">'
        f'{mini_btn("Share","Share R5","share-2","ghost",grow=False)}'
        f'{mini_btn("Download PDF","Download note","download","ghost",grow=False)}'
        f'{mini_btn("Print","Print note","printer","ghost",grow=False)}</Frame></Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R2_HEAD}{R2_NOTE}{R2_PROV}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{R2_LINKED}'
          f'{note("shield-check","Only you decide who reads this. Dr. Okafor keeps her own copy at the clinic, as the law requires.","info")}'
          f'{mini_btn("Book a follow-up","Book follow-up","calendar-plus","teal")}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R2 Consultation Note · Mobile",
        appbar("Consultation", right=circle_btn("share-2", "Share R5"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{R2_HEAD}'
          f'{group_card("The doctor’s note", [note_section("Assessment","Hypertension, partially controlled. No sign of organ damage.","clipboard-check"),note_section("Plan","Continue Amlodipine 5 mg every morning. Less salt. Walk 30 minutes, five days a week. Review in three months.","list-checks")], p=16)}'
          f'{R2_PROV}</Frame>',
        nav=bottom_nav(2)))

# ---------------- R3 lab result
R3_HEAD = (f'<Frame w="fill" flex="col" gap={{14}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" justify="between" items="center">'
           f'<Frame flex="row" gap={{8}} items="center" px={{10}} py={{6}} rounded={{999}} bg="var:state/info-bg">'
           f'{I("flask-conical",13,A_IC)}{T(11,"semibold","var:text/default","Lab result")}</Frame>'
           f'{status_pill("new","1 out of range")}</Frame>'
           f'{T(21,"bold","var:text/strong","Full blood count")}'
           f'{T(13,"regular","var:text/muted","Collected 12 Jun 2026 · reported 13 Jun 2026",w="fill")}'
           f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{14}} rounded={{18}} bg="var:neutral/50">'
           f'<Image image="assets/img/thumb-lab.jpg" w={{54}} h={{54}} rounded={{14}} />'
           f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong","Garki Medical Centre Laboratory")}'
           f'{T(11,"regular","var:text/muted","MLSCN accredited · ordered by Dr. Ngozi Okafor",w="fill")}</Frame>'
           f'{mini_btn("Original","View original","image","ghost",grow=False)}</Frame></Frame>')

R3_VALUES = group_card("Results", [
    lab_line("Haemoglobin", "11.2 g/dL", "12.0 – 15.5", "Low"),
    lab_line("White cell count", "6.4 ×10⁹/L", "4.0 – 11.0"),
    lab_line("Platelets", "268 ×10⁹/L", "150 – 400"),
    lab_line("Haematocrit", "34%", "34 – 45"),
    lab_line("MCV", "82 fL", "80 – 100"),
], footer="Reference ranges come from the reporting laboratory and can differ slightly between labs.")

R3_PLAIN_M = (f'<Frame w="fill" flex="col" gap={{11}} p={{16}} rounded={{22}} bg="var:state/info-bg">'
              f'<Frame flex="row" gap={{9}} items="center">{I("book-open",16,A_IC)}'
              f'{T(13,"semibold","var:text/default","In plain language")}</Frame>'
              f'{T(13,"regular","var:text/default","Your haemoglobin is a little low — often low iron, usually easy to treat. Everything else looks normal.",w="fill")}'
              f'{mini_btn("Ask a doctor about this","Ask about lab","message-square-text","teal",full=True)}</Frame>')
R3_PLAIN = (f'<Frame w="fill" flex="col" gap={{12}} p={{20}} rounded={{24}} bg="var:state/info-bg">'
            f'<Frame flex="row" gap={{9}} items="center">{I("book-open",17,A_IC)}'
            f'{T(13,"semibold","var:text/default","In plain language")}</Frame>'
            f'{T(14,"regular","var:text/default","Your haemoglobin is slightly below the normal range. That often means low iron, which is common and usually easy to treat. Everything else in this test looks normal.",w="fill")}'
            f'{T(12,"regular","var:text/muted","Written by Medra’s clinical team and reviewed by a doctor. It is not a diagnosis — Dr. Okafor will interpret it with the rest of your history.",w="fill")}'
            f'{mini_btn("Ask a doctor about this","Ask about lab","message-square-text","teal",full=True)}</Frame>')

add("Records", "R3-lab",
    desk("Member · Records — R3 Lab Result",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","All records")}</Frame>'
        f'<Frame flex="row" gap={{10}} items="center">'
        f'{mini_btn("Share","Share R5","share-2","ghost",grow=False)}'
        f'{mini_btn("Download PDF","Download lab","download","ghost",grow=False)}</Frame></Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R3_HEAD}{R3_VALUES}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{R3_PLAIN}'
          f'{group_card("Compare with earlier", [list_row("trending-down","Haemoglobin",value="11.2",sub="Was 12.4 in Jan 2026",name="Trend hb"),list_row("trending-up","Platelets",value="268",sub="Was 240 in Jan 2026",name="Trend plt"),list_row("activity","See all trends",name="Open vitals R4")])}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R3 Lab Result · Mobile",
        appbar("Lab result", right=circle_btn("download", "Download lab"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{R3_HEAD}'
          f'{group_card("Results", [lab_line("Haemoglobin","11.2 g/dL","12.0 – 15.5","Low"),lab_line("White cell count","6.4 ×10⁹/L","4.0 – 11.0")], p=16)}'
          f'{R3_PLAIN_M}</Frame>',
        nav=bottom_nav(2)))

# ---------------- R4 vitals
R4_PERIOD = rows_of([mini_btn("3 months", "Period 3m", None, "ghost"), mini_btn("6 months", "Period 6m", None, "navy"),
                     mini_btn("1 year", "Period 1y", None, "ghost"), mini_btn("All", "Period all", None, "ghost")], 4, 9)
BP_SERIES = [("Mar", "142/92", 132, "bad"), ("Apr", "138/88", 118, "warn"), ("May", "136/86", 112, "warn"),
             ("Jun", "132/84", 100, "ok"), ("Jul", "130/82", 92, "ok"), ("Aug", "128/82", 88, "ok")]
R4_BP = group_card("Blood pressure", [
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    + f'<Frame flex="col" gap={{2}}>{T(26,"bold","var:text/strong","128/82")}'
    + f'{T(12,"regular","var:text/muted","Latest · 14 Aug, at home")}</Frame>'
    + f'<Frame flex="row" gap={{7}} items="center" px={{11}} py={{7}} rounded={{999}} bg="var:state/success-bg">'
    + f'{I("trending-down",14,OK_IC)}{T(12,"semibold","var:state/success","14 points lower since March")}</Frame></Frame>',
    chart(BP_SERIES, 150, "Systolic / diastolic, mmHg"),
], footer="Readings you take at home are marked separately from readings taken at a clinic — a doctor can tell them apart.")

R4_OTHER = group_card("Other measurements", [
    list_row("weight", "Weight", value="74 kg", sub="Down 2 kg since March", name="Vital weight"),
    list_row("heart-pulse", "Resting pulse", value="74 bpm", sub="Normal range", name="Vital pulse"),
    list_row("droplet", "Blood sugar (fasting)", value="Not measured", sub="Dr. Okafor ordered this test", name="Vital sugar"),
    list_row("thermometer", "Temperature", value="36.8 °C", sub="12 Jun, at the clinic", name="Vital temp"),
])

add("Records", "R4-vitals",
    desk("Member · Records — R4 Vitals Trend",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","All records")}</Frame>{R4_PERIOD}</Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R4_BP}{R4_OTHER}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'{group_card("Add a reading", [list_row("heart-pulse","Blood pressure",sub="From a home monitor",name="Add bp"),list_row("weight","Weight",name="Add weight"),list_row("droplet","Blood sugar",name="Add sugar"),list_row("file-plus","Photograph a device screen",sub="We read the numbers for you",name="Open upload R7")], footer="Readings you add are labelled “self-measured”, so no doctor mistakes them for a clinic result.")}'
          f'{cta("Add a reading","Add reading R4","plus")}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R4 Vitals Trend · Mobile",
        appbar("Vitals", right=circle_btn("plus", "Add reading R4"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{rows_of([mini_btn("6 months","Period 6m",None,"navy"),mini_btn("1 year","Period 1y",None,"ghost")],2,9)}'
          f'{group_card("Blood pressure", [chart(BP_SERIES,124,"Systolic, mmHg")], p=16)}'
          f'{R4_OTHER}</Frame>',
        nav=bottom_nav(2)))

# ---------------- R5 share
R5_WHO_ROW_M = (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{4}}>'
                f'<Image image="assets/img/avatar-4.jpg" w={{42}} h={{42}} rounded={{14}} />'
                f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Dr. Ngozi Okafor")}'
                f'{T(12,"regular","var:text/muted","Visit on Wed, 21 Aug",w="fill")}</Frame></Frame>')

R5_WHO = group_card("Who are you sharing with?", [
    f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{6}}>'
    + f'<Image image="assets/img/avatar-4.jpg" w={{46}} h={{46}} rounded={{15}} />'
    + f'<Frame grow={{1}} flex="col" gap={{2}}>{T(15,"semibold","var:text/strong","Dr. Ngozi Okafor")}'
    + f'{T(12,"regular","var:text/muted","Cardiologist · your visit is on Wed, 21 Aug",w="fill")}</Frame>'
    + f'{status_pill("confirmed","Chosen")}</Frame>',
    list_row("search", "Someone else on Medra", sub="Search by name or MDCN number", name="Search doctor R5"),
    list_row("qr-code", "A walk-in clinic", sub="Show them a QR code — no account needed", name="QR share R5"),
])
R5_WHAT = group_card("What can they see?", [
    consent_row("triangle-alert", "Allergies and current medicines", "Always shared, so nobody prescribes something unsafe", "Scope allergies", locked=True),
    consent_row("stethoscope", "Consultation notes", "All 8 visits, including notes from other clinics", "Scope visits"),
    consent_row("flask-conical", "Lab results", "4 results, including the one out of range", "Scope labs"),
    consent_row("pill", "Prescription history", "What you were given and whether you took it", "Scope rx", on=False),
    consent_row("activity", "Vitals you measured at home", "Blood pressure, weight, pulse", "Scope vitals", on=False),
    consent_row("file-plus", "Records you uploaded", "Scans of paper results", "Scope uploads", on=False),
])
R5_HOW_LONG = group_card("For how long?", [
    radio_row("Just this visit", sub="Access ends when the visit is marked complete", on=True, name="Duration visit"),
    radio_row("24 hours", name="Duration 24h"),
    radio_row("7 days", sub="Good if tests are still coming back", name="Duration 7d"),
    radio_row("30 days", sub="For ongoing treatment", name="Duration 30d"),
], footer="Whatever you choose, you can revoke access instantly — and you will see every time someone opens your record.")
R5_CONSENT = note("shield-check", "By sharing, you allow Dr. Ngozi Okafor to read the categories ticked above until the time you chose. Medra logs every view. This consent is recorded under the Nigeria Data Protection Act 2023 and you can withdraw it at any moment.", "info")

add("Records", "R5-share",
    desk("Member · Records — R5 Share Records",
        head_chip([("Share your", False), ("records", True)], 30)
        + T(15, "regular", "var:text/muted", "You choose who, what and for how long. Nothing is shared by default.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R5_WHO}{R5_WHAT}</Frame>'
          f'<Frame w={{400}} flex="col" gap={{16}}>{R5_HOW_LONG}{R5_CONSENT}'
          f'{cta("Share access","Confirm share R5","shield-check")}'
          f'{ghost("Cancel","Cancel share R5")}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R5 Share Records · Mobile",
        appbar("Share records")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{group_card("Sharing with", [R5_WHO_ROW_M], p=16)}'
          f'{group_card("What they can see", [consent_row("triangle-alert","Allergies and medicines","Always shared","Scope allergies",locked=True),consent_row("stethoscope","Consultation notes","All 8 visits","Scope visits"),consent_row("flask-conical","Lab results","4 results","Scope labs"),consent_row("pill","Prescription history","What you were given","Scope rx",on=False)], p=16)}'
          f'{group_card("For how long", [radio_row("Just this visit",on=True,name="Duration visit"),radio_row("7 days",sub="Good if tests are still coming back",name="Duration 7d")], p=16)}'
          f'{note("shield-check","Medra logs every view, and you can revoke access instantly.","info")}'
          f'<Frame grow={{1}} />{cta("Share access","Confirm share R5","shield-check")}</Frame>'))

# ---------------- R6 who has access
def access_row(avatar, who, meta, what, expires, name, checked=False):
    box = (f'<Frame w={{22}} h={{22}} rounded={{7}} bg="var:brand/teal" flex="col" justify="center" items="center">'
           f'{I("check",14,W_IC)}</Frame>' if checked else
           '<Rect w={22} h={22} rounded={7} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />')
    return (f'<Frame name="Btn Select {name}" w="fill" flex="row" gap={{12}} items="center" py={{12}}>{box}'
            f'<Image image="assets/img/{avatar}" w={{40}} h={{40}} rounded={{13}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong",who)}'
            f'{T(11,"regular","var:text/muted",meta,w="fill")}'
            f'{T(11,"regular","var:text/muted",what,w="fill")}</Frame>'
            f'<Frame flex="col" gap={{4}} items="end">'
            f'<Frame flex="row" gap={{5}} items="center">{I("clock",11,WARN_IC)}'
            f'{T(11,"medium","var:state/warning",expires)}</Frame>'
            f'{mini_btn("Revoke","Revoke "+name,"circle-slash","danger",grow=False)}</Frame></Frame>')

R6_SELECT_BAR = (f'<Frame w="fill" flex="row" justify="between" items="center" p={{14}} rounded={{18}} bg="var:bg/muted">'
                 f'<Frame name="Btn Select all access" flex="row" gap={{11}} items="center">'
                 f'<Rect w={{22}} h={{22}} rounded={{7}} bg="var:bg/base" stroke="var:border/strong" strokeWidth={{1}} />'
                 f'{T(13,"medium","var:text/default","Select all")}</Frame>'
                 f'{T(12,"regular","var:text/muted","1 of 3 selected")}</Frame>')
R6_ACTIONS = (f'<Frame w="fill" flex="row" gap={{11}}>'
              f'{mini_btn("Revoke selected (1)","Revoke selected","circle-slash","danger")}'
              f'{mini_btn("Revoke everything","Revoke all","shield-off","ghost")}</Frame>')
R6_ACTIVE = group_card("Can see your records now", [
    R6_SELECT_BAR,
    access_row("avatar-4.jpg", "Dr. Ngozi Okafor", "Cardiologist · Garki Medical Centre",
               "Consultations · lab results", "Ends 21 Aug, 11:00", "Okafor", checked=True),
    access_row("avatar-1.jpg", "Dr. Chuka Eze", "General practice · Wuse Clinic",
               "Allergies and medicines only", "Ends 3 Sep", "Eze"),
    access_row("avatar-3.jpg", "Maitama Hospital reception", "Front desk · check-in only",
               "Name, Medra ID, allergies", "Ends today, 18:00", "Maitama"),
    R6_ACTIONS,
], footer="Revoking takes effect immediately, even if the doctor has the record open on screen.")
R6_PAST = group_card("Ended", [
    list_row("circle-slash", "Dr. Chuka Eze", value="Ended 28 Apr", sub="Consultations only · you revoked it early", name="Past share Eze", chevron=False),
    list_row("circle-slash", "Wuse Clinic reception", value="Ended 28 Apr", sub="Immunisation certificate · QR code, 1 hour", name="Past share Wuse", chevron=False),
])
R6_AUDIT = group_card("Who opened what", [
    audit_row("Dr. Ngozi Okafor", "Opened “Hypertension review”", "Today, 09:12"),
    audit_row("Dr. Ngozi Okafor", "Opened “Full blood count”", "Today, 09:14"),
    audit_row("You", "Shared 2 categories with Dr. Okafor", "14 Aug, 20:31"),
    audit_row("Dr. Chuka Eze", "Opened “Malaria — treated”", "28 Apr, 08:41"),
], footer="This log cannot be edited or deleted, by you or by us. It is your evidence of who saw what.")

add("Records", "R6-access",
    desk("Member · Records — R6 Who Has Access",
        light_banner("banner-meds.jpg", "PRIVACY", "Nobody sees your records unless you say so",
                     "One doctor has access right now. Everything else is closed.",
                     actions=mini_btn("Share with someone", "Share R5", "share-2", "teal", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R6_ACTIVE}{R6_AUDIT}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{R6_PAST}'
          f'<Frame name="Btn Revoke all" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{20}} py={{15}} rounded={{999}} bg="var:state/error-bg">'
          f'{I("shield-off",17,ERR_IC)}{T(15,"semibold","var:state/error","Revoke every share now")}</Frame>'
          f'{group_card("Reception check-in", [list_row("qr-code","Show my Medra ID at reception",sub="A one-hour pass: name, Medra ID and allergies only",name="QR share R5")], p=16)}'
          f'{note("info","Clinics also keep their own copy of notes they wrote — the law requires it. Revoking stops new access to your Medra history.","info")}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R6 Who Has Access · Mobile",
        appbar("Who has access")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{group_card("Can see your records now", [R6_SELECT_BAR, access_row("avatar-4.jpg","Dr. Ngozi Okafor","Cardiologist","Consultations · lab results","Ends 21 Aug","Okafor",checked=True), access_row("avatar-1.jpg","Dr. Chuka Eze","General practice","Allergies and medicines","Ends 3 Sep","Eze"), R6_ACTIONS], p=16)}'
          f'{group_card("Who opened what", [audit_row("Dr. Ngozi Okafor","Opened “Hypertension review”","Today, 09:12"),audit_row("You","Shared 2 categories","14 Aug, 20:31")], p=16)}</Frame>',
        nav=bottom_nav(2)))

# ---------------- R7 upload
R7_TYPE = field_chips("What is it?", ["Lab result", "Prescription", "Scan or X-ray", "Discharge summary", "Other"], 0, "Upload type")
R7_BODY = (f'{upload("Open camera R7", label="Photograph or choose a file")}'
           f'{R7_TYPE}'
           f'{field("When was it done?","calendar-days","12 June 2026",ph=False,trailing=("calendar-days","Pick date R7"))}'
           f'{field("Which clinic or lab?","hospital","Garki Medical Centre",ph=False)}'
           f'{field("Add a note (optional)","message-square-text","Kept from my old clinic file")}')
R7_TIPS = group_card("Getting a good scan", [
    list_row("sun", "Good light, no shadow", sub="Daylight near a window works best", name="Tip light", chevron=False),
    list_row("maximize", "Fill the frame", sub="Corners of the page just inside the edge", name="Tip frame", chevron=False),
    list_row("files", "One page at a time", sub="You can add up to 10 pages to one record", name="Tip pages", chevron=False),
    list_row("lock", "Only you can see it", sub="Uploads are private until you share them", name="Tip private", chevron=False),
], footer="We read the date and the lab name automatically. You can correct anything we get wrong before saving.")

add("Records", "R7-upload",
    desk("Member · Records — R7 Add a Record",
        head_chip([("Add an older", False), ("record", True)], 30)
        + T(15, "regular", "var:text/muted", "Paper results, an old prescription, a discharge letter — bring them in and they become part of your history.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R7_BODY}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'<Frame w="fill" h={{190}} rounded={{24}} image="assets/img/banner-capture.jpg" overflow="hidden" flex="col" justify="end" gap={{6}} p={{20}}>'
          f'{eyebrow("SCAN WITH YOUR PHONE","var:brand/teal")}'
          f'{T(18,"bold","var:text/on-dark","Point, shoot, filed")}</Frame>'
          f'{R7_TIPS}{cta("Save to my records","Save record R7","check")}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R7 Add a Record · Mobile",
        appbar("Add a record")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{upload("Open camera R7", label="Photograph or choose a file")}'
          f'{R7_TYPE}'
          f'{field("When was it done?","calendar-days","12 June 2026",ph=False,trailing=("calendar-days","Pick date R7"))}'
          f'<Frame grow={{1}} />{cta("Save to my records","Save record R7","check")}</Frame>'))

# ---------------- R8 added
R8 = (f'<Frame w="fill" flex="col" gap={{16}} items="center">'
      f'{big_icon("file-check","ok",96)}'
      f'{T(23,"bold","var:text/strong","Filed under Lab results")}'
      f'{T(15,"regular","var:text/muted","We read “Full blood count · 12 June 2026 · Garki Medical Centre” from your photo. Tap anything below to correct it.",w="fill",align="center")}'
      f'{group_card("", [list_row("flask-conical","Type",value="Lab result",name="Edit type R8"),list_row("calendar-days","Date",value="12 June 2026",name="Edit date R8"),list_row("hospital","Clinic",value="Garki Medical Centre",name="Edit clinic R8"),list_row("files","Pages",value="1",name="Edit pages R8"),list_row("lock","Visible to",value="Only you",sub="Share it whenever you want",name="Edit share R8")])}'
      f'{note("shield-check","Uploaded records sit alongside the ones doctors write, but they are labelled “added by you” so a clinician knows the difference.","ok")}</Frame>')

R8_M = (f'<Frame w="fill" flex="col" gap={{14}} items="center">'
        f'{big_icon("file-check","ok",88)}'
        f'{T(22,"bold","var:text/strong","Filed under Lab results")}'
        f'{T(14,"regular","var:text/muted","We read “Full blood count · 12 June 2026” from your photo. Tap to correct anything.",w="fill",align="center")}'
        f'{group_card("", [list_row("flask-conical","Type",value="Lab result",name="Edit type R8"),list_row("calendar-days","Date",value="12 June 2026",name="Edit date R8"),list_row("lock","Visible to",value="Only you",name="Edit share R8")], p=16)}</Frame>')

add("Records", "R8-added",
    desk("Member · Records — R8 Record Added",
        f'<Frame w="fill" flex="row" justify="center" pt={{8}}>'
        f'<Frame w={{640}} flex="col" gap={{18}}>{R8}'
        f'<Frame w="fill" flex="row" gap={{12}}>'
        f'<Frame grow={{1}} flex="col">{ghost("Add another","Open upload R7","file-plus")}</Frame>'
        f'<Frame grow={{1}} flex="col">{cta("See it in my records","Back records R8")}</Frame></Frame></Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R8 Record Added · Mobile",
        appbar(None, back=False, right=circle_btn("x", "Back records R8"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{6}} pb={{10}}>{R8_M}'
          f'<Frame grow={{1}} />{cta("See it in my records","Back records R8")}'
          f'{ghost("Add another","Open upload R7","file-plus")}</Frame>'))

# ---------------- R9 empty
R9_WAYS = group_card("Three ways your history fills up", [
    prep_step(1, "See a doctor on Medra", "Their note lands here the moment the visit ends."),
    prep_step(2, "Photograph what you already have", "Old lab slips, a prescription, a discharge letter."),
    prep_step(3, "Ask a clinic to send your file", "We send the request for you — most reply within three days."),
], footer="Your records stay yours. Change clinic, change city, change phone — the history follows you.")
R9_EMPTY = empty_state("clipboard-list", "Your health history starts here",
    "Right now there is nothing to show. That changes with your first visit — or in a minute, if you have a paper result nearby.",
    primary=cta("Add a record now", "Open upload R7", "file-plus"),
    secondary=ghost("Find a doctor", "Find doctor R9", "search"))

add("Records", "R9-records-empty",
    desk("Member · Records — R9 No Records",
        banner("banner-records.jpg", "MY RECORDS", "Nothing here yet",
               "Medra is not just booking — it is the one place your medical history lives.",
               actions=mini_btn("Add a record", "Open upload R7", "file-plus", "teal", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col">{R9_EMPTY}</Frame>'
          f'<Frame w={{400}} flex="col" gap={{16}}>{R9_WAYS}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R9 No Records · Mobile",
        appbar("My records", back=False)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>'
          f'{R9_EMPTY}{group_card("How it fills up", [prep_step(1,"See a doctor on Medra","Their note lands here automatically."),prep_step(2,"Photograph old results","Lab slips, prescriptions, letters.")], p=16)}</Frame>',
        nav=bottom_nav(2)))

# =====================================================================================
# MEDICINES
# =====================================================================================
M_SCHEDULE = group_card("Today · Thursday 14 August", [
    dose_row("08:00", "Amlodipine", "5 mg · 1 tablet", "taken"),
    dose_row("13:00", "Vitamin D", "1000 IU · 1 tablet", "missed", "Take Vitamin D"),
    dose_row("18:00", "Metformin", "500 mg · 1 tablet", "due", "Take Metformin"),
    dose_row("21:00", "Amlodipine", "5 mg · 1 tablet", "upcoming"),
], footer="Marking a dose is only for you — nothing is sent to your doctor unless you share it.")

MED_1 = med_card("Amlodipine", "5 mg", "Blood pressure", "Every morning at 08:00", "2 refills left",
                 "96%", "yyyyyny", "Open med M2", taken_today=True)
MED_2 = med_card("Metformin", "500 mg", "Blood sugar", "Every evening at 18:00", "Refill due in 4 days",
                 "88%", "yynyyyn", "Open med M2b", taken_today=False)
MED_3 = med_card("Vitamin D", "1000 IU", "Supplement", "Daily at 13:00", "Bought over the counter",
                 "71%", "ynynyyn", "Open med M2c", taken_today=False)

M_STATS = rows_of([
    stat_card("pill", "3", "Active medicines", "1 dose due at 18:00", "tint-mint.jpg"),
    stat_card("check-check", "92%", "Taken on time", "Last 30 days", "tint-teal.jpg"),
    stat_card("package", "1", "Refill due", "Metformin, in 4 days", "tint-amber.jpg"),
    stat_card("bell-ring", "4", "Reminders set", "Push and SMS", "tint-blue.jpg"),
], 4, 16)

M_REFILL_NUDGE = (f'<Frame name="Btn Open refill M3" w="fill" flex="row" gap={{13}} items="center" p={{16}} rounded={{22}} bg="var:state/warning-bg">'
                  f'{I("package",19,WARN_IC)}'
                  f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Metformin runs out in 4 days")}'
                  f'{T(12,"regular","var:text/muted","Ask Dr. Okafor for a refill now — she usually replies within a day.",w="fill")}</Frame>'
                  f'{mini_btn("Ask","Open refill M3","send","teal",grow=False)}</Frame>')

add("Medicines", "M1-meds",
    desk("Member · Medicines — M1 My Medicines",
        light_banner("banner-meds.jpg", "MY MEDICINES", "Three medicines, one routine",
                     "Everything a doctor prescribed on Medra shows up here automatically.",
                     actions=mini_btn("Add a medicine", "Add med M1", "plus", "teal", grow=False)
                           + mini_btn("Reminders", "Open reminders M4", "bell-ring", "ghost", grow=False))
        + M_STATS
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{M_REFILL_NUDGE}{MED_1}{MED_2}{MED_3}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{M_SCHEDULE}'
          f'{group_card("Good to know", [list_row("triangle-alert","You are allergic to penicillin",sub="Any doctor prescribing on Medra is warned",name="Allergy warn",tint="var:state/warning-bg",chevron=False),list_row("info","Take Amlodipine at the same time daily",sub="It works best with a steady level in your blood",name="Tip amlodipine",chevron=False)])}</Frame></Frame>',
        SIDE["Meds"]),
    mob("Member · Medicines — M1 My Medicines · Mobile",
        appbar("My medicines", back=False, right=circle_btn("bell-ring", "Open reminders M4"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{M_REFILL_NUDGE}'
          f'{group_card("Today", [dose_row("13:00","Vitamin D","1000 IU","missed","Take Vitamin D"),dose_row("18:00","Metformin","500 mg","due","Take Metformin")], p=16)}'
          f'{MED_1}'
          f'{group_card("Also taking", [list_row("pill","Metformin and Vitamin D",value="2",sub="Evening and midday doses",name="Open med M2b")], p=16)}</Frame>',
        nav=bottom_nav(3)))

# ---------------- M2 medicine detail
M2_HEAD = (f'<Frame w="fill" flex="col" gap={{15}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" gap={{15}} items="center">'
           f'<Frame w={{62}} h={{62}} rounded={{20}} bg="var:state/success-bg" flex="col" justify="center" items="center">'
           f'{I("pill",28,OK_IC)}</Frame>'
           f'<Frame grow={{1}} flex="col" gap={{3}}>{T(21,"bold","var:text/strong","Amlodipine 5 mg")}'
           f'{T(13,"regular","var:text/muted","For high blood pressure · 1 tablet every morning")}</Frame>'
           f'{status_pill("confirmed","Active")}</Frame>'
           f'<Frame w="fill" flex="row" gap={{10}}>'
           f'{stat_cell_v4("calendar-days","18 days","Left in this course")}'
           f'{stat_cell_v4("check-check","96%","Taken on time")}'
           f'{stat_cell_v4("package","2","Refills left")}</Frame></Frame>')

M2_HOW = group_card("How to take it", [
    list_row("sunrise", "Every morning, around 08:00", sub="With or without food — just be consistent", name="How time", chevron=False),
    list_row("droplets", "With a full glass of water", name="How water", chevron=False),
    list_row("ban", "Avoid grapefruit juice", sub="It changes how much of the drug reaches your blood", name="How avoid", chevron=False),
    list_row("triangle-alert", "If you miss a dose", sub="Take it when you remember, unless the next one is within 6 hours — then skip it", name="How missed", chevron=False),
], footer="Written by a pharmacist for Medra. It does not replace what Dr. Okafor told you.")

M2_SIDE = (f'<Frame w="fill" flex="col" gap={{11}} p={{18}} rounded={{22}} bg="var:state/warning-bg">'
           f'<Frame flex="row" gap={{9}} items="center">{I("triangle-alert",17,WARN_IC)}'
           f'{T(13,"semibold","var:text/default","When to call a doctor")}</Frame>'
           f'{T(13,"regular","var:text/default","Swollen ankles, a pounding heartbeat, or dizziness when you stand up. These are known effects of Amlodipine and the dose can be changed.",w="fill")}'
           f'{mini_btn("Report a side effect","Report side effect","flag","ghost",full=True)}</Frame>')

M2_SOURCE = group_card("Where this came from", [
    list_row("stethoscope", "Prescribed by Dr. Ngozi Okafor", sub="MDCN 71482 · Garki Medical Centre", name="Open note R2"),
    list_row("file-text", "Hypertension review", value="12 Jun 2026", sub="Open the consultation note", name="Open note R2"),
    list_row("history", "Started 12 June 2026", sub="Second course — first was 30 days", name="Med history", chevron=False),
])
M2_ADHERENCE = group_card("Last 14 days", [
    adherence_grid(),
    f'<Frame w="fill" flex="row" gap={{16}} items="center" pt={{4}}>'
    + f'<Frame flex="row" gap={{7}} items="center"><Ellipse w={{10}} h={{10}} bg="#2FA36B" />'
    + T(11, "regular", "var:text/muted", "Taken") + '</Frame>'
    + f'<Frame flex="row" gap={{7}} items="center"><Ellipse w={{10}} h={{10}} bg="#E0A32E" />'
    + T(11, "regular", "var:text/muted", "Missed") + '</Frame></Frame>',
], footer="Only you see this. You can choose to show it to Dr. Okafor at your next visit.")

add("Medicines", "M2-med",
    desk("Member · Medicines — M2 Medicine Detail",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","All medicines")}</Frame>'
        f'{mini_btn("Request a refill","Open refill M3","package","teal",grow=False)}</Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{M2_HEAD}{M2_HOW}{M2_ADHERENCE}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{M2_SIDE}{M2_SOURCE}'
          f'{group_card("Reminders", [toggle_row("bell-ring","Remind me at 08:00",sub="Push notification",on=True,name="Remind push M2"),toggle_row("message-square-text","Also send an SMS",sub="For days with no data",on=False,name="Remind sms M2"),list_row("settings","All reminder settings",name="Open reminders M4")])}</Frame></Frame>',
        SIDE["Meds"]),
    mob("Member · Medicines — M2 Medicine Detail · Mobile",
        appbar("Medicine", right=circle_btn("package", "Open refill M3"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{M2_HEAD}{M2_SIDE}'
          f'{group_card("How to take it", [list_row("sunrise","Every morning, around 08:00",sub="With or without food",name="How time",chevron=False),list_row("triangle-alert","If you miss a dose",sub="Take it unless the next is within 6 hours",name="How missed",chevron=False)], p=16)}</Frame>',
        nav=bottom_nav(3)))

# ---------------- M3 refill
M3_PICK = group_card("Which medicine?", [
    radio_row("Metformin 500 mg", sub="4 days left · prescribed by Dr. Okafor", on=True, name="Refill metformin"),
    radio_row("Amlodipine 5 mg", sub="18 days left", name="Refill amlodipine"),
])
M3_WHERE = group_card("Where do you want to collect it?", [
    radio_row("Garki Medical Centre pharmacy", sub="2.4 km · usually ready in 2 hours", on=True, name="Pharmacy clinic"),
    radio_row("A pharmacy near me", sub="We send the prescription — you choose on collection", name="Pharmacy near"),
    radio_row("Deliver to my address", sub="Area 3, Garki · ₦1,500 · same day if approved before 14:00", name="Pharmacy delivery"),
])
M3_BODY = (f'{M3_PICK}{stepper_ctl("How many days do you need?", 30, "Refill days", "Dr. Okafor can approve up to 90 days at a time")}'
           f'{M3_WHERE}{field("Anything the doctor should know? (optional)","message-square-text","The 500 mg makes me a little nauseous in the evening")}')
M3_WHATNEXT = group_card("What happens next", [
    prep_step(1, "Dr. Okafor reviews it", "Usually within a day — you get a notification either way."),
    prep_step(2, "The pharmacy gets the prescription", "No paper, no second trip to the clinic."),
    prep_step(3, "You collect and confirm", "We update your medicine so the count stays right."),
], footer="A refill is not automatic. If Dr. Okafor wants to see you first, she will say so and you can book from the message.")

add("Medicines", "M3-refill",
    desk("Member · Medicines — M3 Request a Refill",
        head_chip([("Request a", False), ("refill", True)], 30)
        + T(15, "regular", "var:text/muted", "Ask the doctor who prescribed it — no queue, no new consultation fee.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{M3_BODY}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{M3_WHATNEXT}'
          f'{group_card("Summary", [list_row("pill","Medicine",value="Metformin 500 mg",name="M3 med",chevron=False),list_row("calendar-days","Supply",value="30 days",name="M3 days",chevron=False),list_row("store","Collect at",value="Garki pharmacy",name="M3 where",chevron=False),list_row("banknote","Estimated cost",value="₦4,200",sub="Paid at the pharmacy",name="M3 cost",chevron=False)])}'
          f'{cta("Send the request","Send refill M3","send")}</Frame></Frame>',
        SIDE["Meds"]),
    mob("Member · Medicines — M3 Request a Refill · Mobile",
        appbar("Request a refill")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{M3_PICK}{stepper_ctl("Days needed", 30, "Refill days")}'
          f'{group_card("Collect at", [radio_row("Garki Medical Centre pharmacy",sub="Ready in about 2 hours",on=True,name="Pharmacy clinic"),radio_row("Deliver to my address",sub="₦1,500 · same day",name="Pharmacy delivery")], p=16)}'
          f'<Frame grow={{1}} />{cta("Send the request","Send refill M3","send")}</Frame>'))

# ---------------- M4 reminders
M4_TIMES = group_card("Amlodipine 5 mg", [
    list_row("alarm-clock", "08:00", value="Every day", name="Time amlodipine 1"),
    list_row("plus", "Add another time", sub="For a medicine taken twice a day", name="Add time amlodipine", chevron=False),
])
M4_TIMES2 = group_card("Metformin 500 mg", [
    list_row("alarm-clock", "18:00", value="Every day", name="Time metformin 1"),
    list_row("plus", "Add another time", name="Add time metformin", chevron=False),
])
M4_CHANNELS = group_card("How should we remind you?", [
    toggle_row("bell-ring", "Push notification", sub="Free, needs data or Wi-Fi", on=True, name="Channel push"),
    toggle_row("message-square-text", "SMS", sub="Works with no data at all — we pay for it", on=True, name="Channel sms"),
    toggle_row("phone-call", "Voice call for missed doses", sub="Only after two missed doses in a row", on=False, name="Channel voice"),
], footer="If you have no data for a day, SMS is the one that still reaches you. That is why it is on by default.")
M4_QUIET = group_card("Quiet hours", [
    toggle_row("moon", "Do not disturb me at night", sub="22:00 to 06:00 — reminders wait until morning", on=True, name="Quiet on"),
    list_row("sunset", "Starts", value="22:00", name="Quiet start"),
    list_row("sunrise", "Ends", value="06:00", name="Quiet end"),
    toggle_row("triangle-alert", "Except urgent ones", sub="A doctor cancelling your visit still comes through", on=True, name="Quiet except"),
])

add("Medicines", "M4-reminders",
    desk("Member · Medicines — M4 Reminders",
        head_chip([("Medicine", False), ("reminders", True)], 30)
        + T(15, "regular", "var:text/muted", "Set a time per medicine, then choose how we reach you.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{M4_TIMES}{M4_TIMES2}'
          f'{group_card("Vitamin D 1000 IU", [list_row("alarm-clock","13:00",value="Every day",name="Time vitd 1"),toggle_row("bell-off","Pause these reminders",sub="You are travelling until 20 Aug",on=False,name="Pause vitd")])}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{M4_CHANNELS}{M4_QUIET}'
          f'{cta("Save reminders","Save reminders M4","check")}</Frame></Frame>',
        SIDE["Meds"]),
    mob("Member · Medicines — M4 Reminders · Mobile",
        appbar("Reminders")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{M4_TIMES}{M4_CHANNELS}'
          f'<Frame grow={{1}} />{cta("Save reminders","Save reminders M4","check")}</Frame>',
        nav=bottom_nav(3)))

# ---------------- M5 empty
M5_EMPTY = empty_state("pill", "No medicines yet",
    "When a doctor prescribes something on Medra, it appears here with the dose, the reminders and the refill button already set up.",
    primary=cta("Add one myself", "Add med M1", "plus"),
    secondary=ghost("See a doctor", "Find doctor M5", "search"))
add("Medicines", "M5-meds-empty",
    desk("Member · Medicines — M5 No Medicines",
        light_banner("banner-meds.jpg", "MY MEDICINES", "Nothing to take right now",
                     "This screen fills itself the first time a doctor prescribes for you.",
                     actions=mini_btn("Add a medicine", "Add med M1", "plus", "teal", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col">{M5_EMPTY}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'{group_card("Why add them yourself?", [list_row("triangle-alert","Safer prescribing",sub="Any doctor you see is warned about clashes",name="Why safer",chevron=False),list_row("bell-ring","Reminders that actually reach you",sub="Push, or SMS when you have no data",name="Why remind",chevron=False),list_row("package","One-tap refills",sub="No trip to the clinic for a piece of paper",name="Why refill",chevron=False)])}</Frame></Frame>',
        SIDE["Meds"]),
    mob("Member · Medicines — M5 No Medicines · Mobile",
        appbar("My medicines", back=False)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>{M5_EMPTY}</Frame>',
        nav=bottom_nav(3)))

# =====================================================================================
# PROFILE & SETTINGS
# =====================================================================================
P0_HEAD = (f'<Frame w="fill" flex="col" gap={{16}} p={{20}} rounded={{28}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Frame w="fill" flex="row" gap={{15}} items="center">'
           f'<Image image="assets/img/me.jpg" w={{72}} h={{72}} rounded={{999}} />'
           f'<Frame grow={{1}} flex="col" gap={{3}}>{T(20,"bold","var:text/strong","Amara Okeke")}'
           f'{T(13,"regular","var:text/muted","Member since January 2026 · Abuja")}'
           f'<Frame flex="row" gap={{7}} items="center">{I("badge-check",13,OK_IC)}'
           f'{T(12,"medium","var:state/success","Phone verified")}</Frame></Frame>'
           f'{mini_btn("Edit","Open details P2","pencil","ghost",grow=False)}</Frame>'
           f'<Frame w="fill" flex="row" gap={{10}}>'
           f'{stat_cell_v4("droplet","O+","Blood group")}'
           f'{stat_cell_v4("triangle-alert","Penicillin","Allergy")}'
           f'{stat_cell_v4("heart-pulse","Hypertension","Condition")}</Frame></Frame>')

P0_ACCOUNT = group_card("Account", [
    list_row("circle-user", "Personal details", sub="Name, date of birth, phone, address", name="Open details P2"),
    list_row("users-round", "People I care for", value="2", sub="Chidi (6) and Mama Grace (68)", name="Open dependants P3"),
    list_row("qr-code", "My Medra ID", value="MDR-8842-19", sub="Show it at reception instead of filling a form", name="Open qr P0"),
])
P0_SECURITY = group_card("Security", [
    list_row("smartphone", "Devices signed in", value="3", sub="This phone, a laptop and one you may not recognise", name="Open security P5"),
    list_row("fingerprint", "How I unlock Medra", value="Fingerprint", name="Open security P5"),
    list_row("key", "Ask for a code every time", value="Off", sub="Off means faster sign-in on this trusted device", name="Open security P5"),
])
P0_PREFS = group_card("Preferences", [
    list_row("bell-ring", "Notifications", value="App, WhatsApp, SMS", name="Open notifs P6"),
    list_row("languages", "Language", value="English", sub="Hausa, Yoruba, Igbo and Pidgin available", name="Open language P7"),
    list_row("accessibility", "Text size and contrast", value="Default", name="Open language P7"),
])
P0_PRIVACY = group_card("Privacy and data", [
    list_row("shield-check", "Who can see my records", value="1 doctor", name="Open access R6"),
    list_row("download", "Download everything I have", sub="A ZIP with every record, sent to your email", name="Open privacy P8"),
    list_row("trash-2", "Delete my account", sub="What we must keep, and what disappears", name="Open delete P9", danger=True),
])
P0_SUPPORT = group_card("Help", [
    list_row("circle-help", "Help centre", name="Open help"),
    list_row("message-square-text", "Message the Medra team", sub="We reply in minutes, every day", name="Open support"),
    list_row("book-open", "Terms and privacy policy", name="Open terms"),
    list_row("log-out", "Sign out", name="Sign out", chevron=False),
])

P0_PRIVACY_M = group_card("Privacy and data", [
    list_row("shield-check", "Who can see my records", value="1 doctor", name="Open access R6"),
    list_row("trash-2", "Delete my account", name="Open delete P9", danger=True),
], p=16)
P0_ACCOUNT_M = group_card("Account", [
    list_row("circle-user", "Personal details", name="Open details P2"),
    list_row("users-round", "People I care for", value="2", name="Open dependants P3"),
    list_row("smartphone", "Devices and security", value="3", name="Open security P5"),
], p=16)
P0_PREFS_M = group_card("Preferences", [
    list_row("bell-ring", "Notifications", value="App, WhatsApp, SMS", name="Open notifs P6"),
    list_row("languages", "Language", value="English", name="Open language P7"),
], p=16)
P0_TILES_M = rows_of([
    tile("circle-user", "Personal details", "Name, phone, address", "Open details P2"),
    tile("users-round", "People I care for", "Chidi and Mama Grace", "Open dependants P3"),
    tile("smartphone", "Devices", "3 signed in", "Open security P5"),
    tile("bell-ring", "Notifications", "App, WhatsApp, SMS", "Open notifs P6"),
    tile("languages", "Language", "English", "Open language P7"),
    tile("shield-check", "Privacy and data", "1 doctor has access", "Open privacy P8", "var:state/info-bg"),
], 2, 11)
P0_HEAD_M = (f'<Frame w="fill" flex="row" gap={{15}} items="center" p={{18}} rounded={{26}} bg="var:bg/base" '
             f'stroke="var:border/subtle" strokeWidth={{1}}>'
             f'<Image image="assets/img/me.jpg" w={{62}} h={{62}} rounded={{999}} />'
             f'<Frame grow={{1}} flex="col" gap={{3}}>{T(18,"bold","var:text/strong","Amara Okeke")}'
             f'{T(12,"regular","var:text/muted","Member since Jan 2026 · O+ · allergic to penicillin",w="fill")}</Frame>'
             f'{mini_btn("Edit","Open details P2","pencil","ghost",grow=False)}</Frame>')

add("Profile", "P0-profile",
    desk("Member · Profile — P0 Profile",
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{P0_HEAD}{P0_ACCOUNT}{P0_SECURITY}{P0_PREFS}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{qr_card()}{P0_PRIVACY}{P0_SUPPORT}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P0 Profile · Mobile",
        appbar("Profile", back=False, right=circle_btn("settings", "Open notifs P6"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{P0_HEAD_M}{P0_TILES_M}'
          f'{list_row("trash-2","Delete my account",name="Open delete P9",danger=True)}</Frame>',
        nav=bottom_nav(4)))

# ---------------- P2 personal details
P2_FORM = (f'{field("Full name","circle-user","Amara Chinaza Okeke",ph=False,helper="Use the name on your ID — clinics check it at reception")}'
           f'<Frame w="fill" flex="row" gap={{14}}>'
           f'<Frame grow={{1}} flex="col">{field("Date of birth","calendar-days","14 March 1992",ph=False)}</Frame>'
           f'<Frame grow={{1}} flex="col">{field("Blood group","droplet","O+",ph=False)}</Frame></Frame>'
           f'{field_chips("Sex", ["Female", "Male", "Prefer not to say"], 0, "Sex")}'
           f'{field("Phone number","phone","801 234 5678",ph=False,prefix="+234",helper="Verified — used for visit confirmations",trailing=("badge-check","Phone verified"))}'
           f'{field("Email (optional)","mail","amara.okeke@gmail.com",ph=False,helper="For record downloads and receipts",trailing=("send","Verify email"))}'
           f'{field("Where you live","map-pin","Area 3, Garki, Abuja",ph=False,helper="Only used to show doctors near you")}')
P2_EMERGENCY = group_card("Emergency contact", [
    list_row("phone-call", "Ijeoma Okeke", value="Sister", sub="+234 805 998 1122", name="Emergency contact"),
    list_row("plus", "Add another contact", name="Add emergency", chevron=False),
], footer="Shown to a doctor treating you only in an emergency, and the access is logged.")
P2_MEDICAL = group_card("Medical basics", [
    list_row("triangle-alert", "Allergies", value="Penicillin", sub="Add anything else — it protects you", name="Edit allergies", tint="var:state/warning-bg"),
    list_row("heart-pulse", "Long-term conditions", value="Hypertension", name="Edit conditions"),
    list_row("pill", "Medicines you take", value="3", name="Open meds P2"),
    list_row("syringe", "Immunisations", value="Up to date", name="Open vaccines"),
])

add("Profile", "P2-details",
    desk("Member · Profile — P2 Personal Details",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Profile")}</Frame>'
        f'{mini_btn("Save changes","Save details P2","check","teal",grow=False)}</Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P2_FORM}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'<Frame w="fill" flex="col" gap={{12}} items="center" p={{20}} rounded={{24}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
          f'<Image image="assets/img/me.jpg" w={{96}} h={{96}} rounded={{999}} />'
          f'{mini_btn("Change photo","Change photo P2","camera","ghost")}'
          f'{T(11,"regular","var:text/muted","Optional. It helps clinic staff recognise you at reception.",align="center",w="fill")}</Frame>'
          f'{P2_MEDICAL}{P2_EMERGENCY}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P2 Personal Details · Mobile",
        appbar("Personal details", right=circle_btn("check", "Save details P2"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{field("Full name","circle-user","Amara Chinaza Okeke",ph=False,helper="Use the name on your ID")}'
          f'{field("Phone number","phone","801 234 5678",ph=False,prefix="+234",trailing=("badge-check","Phone verified"))}'
          f'{field("Where you live","map-pin","Area 3, Garki, Abuja",ph=False)}'
          f'{P2_MEDICAL}</Frame>'))

# ---------------- P3 dependants
P3_LIST = group_card("People I care for", [
    dependant_row("avatar-6.jpg", "Chidi Okeke", "Son · 6 years · you manage his records", "Chidi"),
    dependant_row("avatar-2.jpg", "Mama Grace Okeke", "Mother · 68 years · diabetes, hypertension", "Grace"),
], footer="You manage a child's records until they turn 18, then the account becomes theirs. An adult must confirm by SMS before you can manage theirs.")
P3_EMPTY_HINT = group_back = group_card("Why add them", [
    list_row("calendar-plus", "Book for them without a second account", name="Why book", chevron=False),
    list_row("clipboard-list", "Keep their history in one place", sub="Immunisations, growth, prescriptions", name="Why history", chevron=False),
    list_row("bell-ring", "Get their reminders on your phone", name="Why remind", chevron=False),
])

add("Profile", "P3-dependants",
    desk("Member · Profile — P3 Dependants",
        light_banner("banner-family.jpg", "PEOPLE I CARE FOR", "Two people in your care",
                     "Book visits, hold records and get reminders for a child or an older relative.",
                     actions=mini_btn("Add someone", "Open add dependant P4", "user-plus", "teal", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P3_LIST}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{P3_EMPTY_HINT}'
          f'{note("shield-check","Their records are separate from yours. A doctor you share your own history with cannot see theirs.","info")}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P3 Dependants · Mobile",
        appbar("People I care for", right=circle_btn("user-plus", "Open add dependant P4"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{P3_LIST}{group_card("Why add them", [list_row("calendar-plus","Book for them without a second account",name="Why book",chevron=False),list_row("clipboard-list","Keep their history in one place",name="Why history",chevron=False)], p=16)}</Frame>',
        nav=bottom_nav(4)))

# ---------------- P4 add dependant
P4_FORM = (f'{field_chips("Who is this?", ["Child", "Parent", "Spouse", "Other"], 0, "Relationship")}'
           f'{field("Their full name","circle-user","Chidi Emeka Okeke")}'
           f'<Frame w="fill" flex="row" gap={{14}}>'
           f'<Frame grow={{1}} flex="col">{field("Date of birth","calendar-days","2 May 2020")}</Frame>'
           f'<Frame grow={{1}} flex="col">{field("Blood group (optional)","droplet","Not known")}</Frame></Frame>'
           f'{field_chips("Sex", ["Female", "Male", "Prefer not to say"], 1, "Dep sex")}'
           f'{field("Their phone (optional)","phone","Leave empty for a child",prefix="+234",helper="An adult gets an SMS to confirm you may manage their records")}')
P4_CONSENT = (f'<Frame w="fill" flex="col" gap={{12}} p={{18}} rounded={{22}} bg="var:state/info-bg">'
              f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",17,A_IC)}'
              f'{T(13,"semibold","var:text/default","What you are agreeing to")}</Frame>'
              f'{checkbox("I am this person’s parent or legal guardian, or they have asked me to manage their care.","Consent guardian")}'
              f'{checkbox("I understand their records are theirs, and a child takes over the account at 18.","Consent handover")}'
              f'{T(11,"regular","var:text/muted","Recorded under the Nigeria Data Protection Act 2023, with the date and time.",w="fill")}</Frame>')

add("Profile", "P4-add-dependant",
    desk("Member · Profile — P4 Add a Dependant",
        head_chip([("Add someone to", False), ("your care", True)], 30)
        + T(15, "regular", "var:text/muted", "A child, a parent, anyone whose visits you arrange.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P4_FORM}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{P4_CONSENT}'
          f'{group_card("For a child", [list_row("syringe","Immunisation schedule",sub="We track what is due and when",name="Child vaccines",chevron=False),list_row("baby","Growth chart",sub="Height and weight over time",name="Child growth",chevron=False),list_row("user-cog","Handover at 18",sub="They get the account, you lose access",name="Child handover",chevron=False)])}'
          f'{cta("Add to my care","Save dependant P4","user-plus")}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P4 Add a Dependant · Mobile",
        appbar("Add someone")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{field_chips("Who is this?", ["Child", "Parent", "Spouse", "Other"], 0, "Relationship")}'
          f'{field("Their full name","circle-user","Chidi Emeka Okeke")}'
          f'{field("Date of birth","calendar-days","2 May 2020")}'
          f'{P4_CONSENT}<Frame grow={{1}} />{cta("Add to my care","Save dependant P4","user-plus")}</Frame>'))

# ---------------- P5 devices & security
P5_DEVICES = group_card("Where you are signed in", [
    device_row("smartphone", "iPhone 13 · this phone", "Abuja · active now · trusted until 12 Sep", "Device phone", current=True),
    device_row("laptop", "Windows laptop · Chrome", "Abuja · last used 2 days ago", "Device laptop"),
    device_row("monitor-smartphone", "Unknown Android device", "Lagos · 6 days ago — was this you?", "Device unknown"),
], footer="A device stays trusted for 30 days. After that, or on a new device, we ask for a code.")
P5_UNLOCK = group_card("How you get in", [
    radio_row("Fingerprint or Face", sub="Fastest — nothing to remember", on=True, name="Unlock biometric"),
    radio_row("6-digit PIN", sub="Use this if biometrics do not work on your phone", name="Unlock pin"),
    radio_row("A code by SMS every time", sub="Slowest, but nothing is stored on the device", name="Unlock otp"),
])
P5_EXTRA = group_card("Extra checks", [
    toggle_row("key", "Ask for a code on a new device", sub="Strongly recommended — leave this on", on=True, name="Check newdevice"),
    toggle_row("shield-check", "Ask again before I share records", sub="A second confirmation before any doctor gets access", on=True, name="Check share"),
    toggle_row("bell", "Tell me when someone signs in", sub="SMS to +234 801 234 5678", on=True, name="Check signin"),
])
P5_ACTIVITY = group_card("Recent activity", [
    audit_row("Signed in", "iPhone 13 · fingerprint · Abuja", "Today, 08:02"),
    audit_row("Records shared", "With Dr. Ngozi Okafor · until 21 Aug", "14 Aug, 20:31"),
    audit_row("Sign-in blocked", "Unknown Android device · wrong code", "8 Aug, 23:14"),
])

add("Profile", "P5-security",
    desk("Member · Profile — P5 Devices &amp; Security",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Profile")}</Frame>'
        f'<Frame name="Btn Sign out all" flex="row" gap={{8}} items="center" px={{15}} py={{10}} rounded={{999}} bg="var:state/error-bg">'
        f'{I("log-out",15,ERR_IC)}{T(13,"semibold","var:state/error","Sign out everywhere")}</Frame></Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P5_DEVICES}{P5_ACTIVITY}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{P5_UNLOCK}{P5_EXTRA}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P5 Devices &amp; Security · Mobile",
        appbar("Devices & security")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{P5_DEVICES}{P5_UNLOCK}</Frame>',
        nav=bottom_nav(4)))

# ---------------- P6 notifications
def notif_matrix(label, sub, push=True, sms=True, key="N"):
    def chip(on, ic, nm, txt):
        st = ('image="assets/img/btn-teal.jpg" overflow="hidden"' if on else
              'bg="var:bg/base" stroke="var:border/default" strokeWidth={1}')
        col = "var:text/on-dark" if on else "var:text/muted"
        return (f'<Frame name="Btn {nm}" flex="row" gap={{6}} items="center" px={{12}} py={{8}} rounded={{999}} {st}>'
                f'{I(ic,13,W_IC if on else M_IC)}{T(11,"semibold",col,txt)}</Frame>')
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center" py={{12}}>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"medium","var:text/strong",label)}'
            f'{T(11,"regular","var:text/muted",sub,w="fill")}</Frame>'
            f'<Frame flex="row" gap={{7}}>{chip(push,"bell",key+" push","Push")}'
            f'{chip(sms,"message-square-text",key+" sms","SMS")}</Frame></Frame>')

P6_MATRIX = group_card("What we tell you about", [
    notif_matrix("Visit confirmed or changed", "Always on by SMS — it is your proof of booking", True, True, "Visit"),
    notif_matrix("Reminder before a visit", "24 hours and 2 hours before", True, True, "Remind"),
    notif_matrix("Medicine reminders", "At the times you set", True, True, "Med"),
    notif_matrix("Someone opened your records", "So you always know who looked", True, False, "Audit"),
    notif_matrix("Refill approved or declined", "From the doctor who prescribed it", True, True, "Refill"),
    notif_matrix("A new result arrived", "From a Medra lab or clinic", True, False, "Result"),
    notif_matrix("Slot opened with a doctor you follow", "Only if you asked to be told", True, False, "Slot"),
    notif_matrix("Health tips and Medra news", "Off by default — we will not nag you", False, False, "News"),
], footer="Visit confirmations always go out by SMS, even with everything else off. That one keeps you covered when your data is down.")

add("Profile", "P6-notifs",
    desk("Member · Profile — P6 Notification Preferences",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Profile")}</Frame>'
        + head_chip([("Notification", False), ("preferences", True)], 30)
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P6_MATRIX}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'{group_card("Quiet hours", [toggle_row("moon","Do not disturb at night",sub="22:00 to 06:00",on=True,name="P6 quiet"),list_row("sunset","Starts",value="22:00",name="P6 start"),list_row("sunrise","Ends",value="06:00",name="P6 end")])}'
          f'{note("info","SMS costs you nothing — Medra pays for every message we send you.","info")}'
          f'{cta("Save preferences","Save notifs P6","check")}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P6 Notification Preferences · Mobile",
        appbar("Notifications", right=circle_btn("check", "Save notifs P6"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{group_card("What we tell you about", [notif_matrix("Visit confirmed or changed","Always on by SMS",True,True,"Visit"),notif_matrix("Reminder before a visit","24h and 2h before",True,True,"Remind"),notif_matrix("Medicine reminders","At your set times",True,True,"Med"),notif_matrix("Someone opened your records","So you always know",True,False,"Audit")], p=16)}</Frame>'))

# ---------------- P7 language & accessibility
P7_LANG = group_card("Language", [
    radio_row("English", sub="Default", on=True, name="Lang english"),
    radio_row("Hausa", sub="Harshen Hausa", name="Lang hausa"),
    radio_row("Yorùbá", sub="Èdè Yorùbá", name="Lang yoruba"),
    radio_row("Igbo", sub="Asụsụ Igbo", name="Lang igbo"),
    radio_row("Nigerian Pidgin", sub="Naija Pidgin", name="Lang pidgin"),
], footer="Doctors’ notes stay in the language the doctor wrote them in. Everything Medra writes is translated.")
P7_TEXT = group_card("Reading comfort", [
    f'<Frame w="fill" flex="col" gap={{11}} py={{6}}>'
    + T(13, "medium", "var:text/default", "Text size")
    + f'<Frame w="fill" flex="row" gap={{12}} items="center">{T(12,"regular","var:text/muted","A")}'
    + f'<Frame grow={{1}} h={{6}} rounded={{999}} bg="var:neutral/200" flex="row" items="center">'
    + f'<Frame w={{140}} h={{6}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden" />'
    + f'<Frame name="Btn Text size" w={{24}} h={{24}} rounded={{999}} bg="var:bg/base" stroke="var:border/strong" strokeWidth={{1}} />'
    + f'</Frame>{T(20,"bold","var:text/muted","A")}</Frame>'
    + T(11, "regular", "var:text/muted", "Everything in Medra scales — nothing gets cut off.", w="fill") + '</Frame>',
    toggle_row("contrast", "Higher contrast", sub="Stronger borders and darker text", on=False, name="A11y contrast"),
    toggle_row("circle-slash", "Reduce motion", sub="Turns off sliding and fading animations", on=False, name="A11y motion"),
    toggle_row("volume-2", "Screen reader hints", sub="Longer labels for TalkBack and VoiceOver", on=True, name="A11y sr"),
], footer="Medra is built to meet WCAG 2.2 AA. If something is hard to read or reach, tell us and we will fix it.")
P7_DATA = group_card("Data and connection", [
    toggle_row("signal", "Data saver", sub="Smaller images, video calls in low quality", on=False, name="Data saver"),
    toggle_row("cloud-off", "Keep records on this phone", sub="Read your history with no connection at all", on=True, name="Data offline"),
    list_row("wifi", "Download over Wi-Fi only", value="On", name="Data wifi"),
])

add("Profile", "P7-language",
    desk("Member · Profile — P7 Language &amp; Accessibility",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Profile")}</Frame>'
        + head_chip([("Language and", False), ("accessibility", True)], 30)
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P7_LANG}{P7_DATA}</Frame>'
          f'<Frame w={{420}} flex="col" gap={{16}}>{P7_TEXT}'
          f'{cta("Save","Save language P7","check")}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P7 Language &amp; Accessibility · Mobile",
        appbar("Language & access", right=circle_btn("check", "Save language P7"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{group_card("Language", [radio_row("English",on=True,name="Lang english"),radio_row("Hausa",name="Lang hausa"),radio_row("Yorùbá",name="Lang yoruba"),radio_row("Igbo",name="Lang igbo"),radio_row("Nigerian Pidgin",name="Lang pidgin")], p=16)}'
          f'{group_card("Data", [toggle_row("signal","Data saver",on=False,name="Data saver"),toggle_row("cloud-off","Keep records on this phone",on=True,name="Data offline")], p=16)}</Frame>'))

# ---------------- P8 privacy & data
P8_WHO = group_card("Who can see what", [
    list_row("shield-check", "Doctors with access", value="1", sub="Dr. Ngozi Okafor · until 21 Aug", name="Open access R6"),
    list_row("eye", "Everyone who has opened a record", sub="A log you cannot edit — and neither can we", name="Open access R6"),
    list_row("hospital", "Clinics that hold their own copy", value="3", sub="Required by law for notes they wrote", name="Clinic copies"),
])
P8_EXPORT = group_card("Your copy of everything", [
    list_row("download", "Download my records", sub="A ZIP of every note, result and prescription — ready in about 10 minutes", name="Export data P8"),
    list_row("printer", "Print a one-page summary", sub="Blood group, allergies, medicines, conditions, with a QR code", name="Print summary"),
    list_row("external-link", "Send to another app or doctor", sub="Standard format, so another system can read it", name="Export fhir"),
], footer="This is your right under the Nigeria Data Protection Act 2023. No fee, no reason needed, as often as you like.")
P8_CONTROL = group_card("How Medra uses your data", [
    toggle_row("activity", "Help improve Medra", sub="Anonymous usage only — never your medical records", on=True, name="Data improve"),
    toggle_row("microscope", "Allow anonymised research", sub="Nigerian public-health research, no name attached, opt out any time", on=False, name="Data research"),
    toggle_row("store", "Marketing from partner clinics", sub="Off, and we will never turn it on for you", on=False, name="Data marketing"),
], footer="Your records are stored in Nigeria. They are never sold, and never used to train anything without the switch above.")
P8_DANGER = (f'<Frame w="fill" flex="col" gap={{13}} p={{20}} rounded={{24}} bg="var:state/error-bg">'
             f'<Frame flex="row" gap={{9}} items="center">{I("triangle-alert",18,ERR_IC)}'
             f'{T(14,"semibold","var:state/error","Leaving Medra")}</Frame>'
             f'{T(13,"regular","var:text/default","You can pause your account and keep everything, or delete it. Deleting is permanent after 30 days.",w="fill")}'
             f'<Frame w="fill" flex="row" gap={{10}}>'
             f'{mini_btn("Pause my account","Pause account","moon","ghost")}'
             f'{mini_btn("Delete my account","Open delete P9","trash-2","danger")}</Frame></Frame>')

add("Profile", "P8-privacy",
    desk("Member · Profile — P8 Privacy &amp; Data",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Profile")}</Frame>'
        + head_chip([("Privacy and", False), ("your data", True)], 30)
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P8_WHO}{P8_CONTROL}</Frame>'
          f'<Frame w={{400}} flex="col" gap={{16}}>{P8_EXPORT}{P8_DANGER}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P8 Privacy &amp; Data · Mobile",
        appbar("Privacy & data")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{group_card("Who can see what", [list_row("shield-check","Doctors with access",value="1",name="Open access R6"),list_row("eye","Everyone who opened a record",name="Open access R6")], p=16)}'
          f'{group_card("Your copy of everything", [list_row("download","Download my records",sub="A ZIP, ready in about 10 minutes",name="Export data P8"),list_row("printer","Print a one-page summary",name="Print summary")], p=16)}'
          f'{P8_DANGER}</Frame>'))

# ---------------- P9 delete account
P9_GONE = group_card("What disappears", [
    list_row("circle-user", "Your profile and login", sub="Name, phone, email, photo, devices", name="Gone profile", chevron=False),
    list_row("file-plus", "Records you uploaded yourself", sub="Scans, photos, readings you entered", name="Gone uploads", chevron=False),
    list_row("bell-ring", "Reminders and preferences", name="Gone prefs", chevron=False),
    list_row("share-2", "Every share you granted", sub="Revoked the moment you confirm", name="Gone shares", chevron=False),
])
P9_KEPT = group_card("What we must keep, and why", [
    list_row("hospital", "Notes a doctor wrote about you", sub="The clinic keeps its own copy — Nigerian medical-records law requires it, and it is not ours to delete", name="Kept notes", chevron=False),
    list_row("receipt", "Payment records", sub="Kept for tax and audit, without your medical details", name="Kept payments", chevron=False),
    list_row("eye", "The access log", sub="Anonymised, so nobody can quietly erase who looked at what", name="Kept audit", chevron=False),
], footer="We would rather tell you this plainly now than surprise you afterwards.")
# Four deliberate gates. Deleting an account holding someone's medical history should take
# more effort than abandoning it — the review asked for exactly this.
P9_CONFIRM = (f'<Frame w="fill" flex="col" gap={{14}} p={{20}} rounded={{24}} bg="var:state/error-bg">'
              f'{T(15,"semibold","var:state/error","Four steps, on purpose")}'
              f'{T(13,"regular","var:text/default","This is not a button you can hit by accident. For 30 days after this you can still sign in and cancel — after that it is gone for good.",w="fill")}'
              f'{prep_step(1,"Tell us why","So we can fix whatever went wrong",done=True)}'
              f'{field("Type DELETE to confirm","type","DELETE",ph=False,focus=True)}'
              f'{prep_step(3,"Confirm it is you","We send a code to +234 801 234 5678")}'
              f'{otp("")}'
              f'{checkbox("I understand my uploaded records will be permanently deleted, and that my clinics keep their own copies.","Confirm delete understood")}'
              f'<Frame name="Btn Confirm delete" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{24}} py={{16}} rounded={{999}} bg="#D14343">'
              f'{I("trash-2",18,W_IC)}{T(15,"semibold","var:text/on-dark","Delete my account")}</Frame>'
              f'{T(11,"regular","var:text/muted","Nothing happens until all four are done.",w="fill",align="center")}</Frame>')
P9_REASON = group_card("Why are you leaving?", [
    radio_row("I do not need Medra any more", name="Del reason nouse"),
    radio_row("I am worried about my data", sub="Tell us — privacy is the thing we most want to get right", on=True, name="Del reason privacy"),
    radio_row("It is too expensive", name="Del reason cost"),
    radio_row("I could not find the care I needed", name="Del reason care"),
    radio_row("Something else", name="Del reason other"),
], footer="A real person reads these. If it is something we can fix, we would rather fix it than lose you.")
P9_ALT = group_card("Or do something smaller", [
    list_row("moon", "Pause my account instead", sub="Nothing is deleted, no notifications, come back any time", name="Pause account"),
    list_row("bell-off", "Just stop the notifications", name="Open notifs P6"),
    list_row("shield-off", "Revoke every share", sub="Keeps your records, closes all access", name="Open access R6"),
    list_row("message-square-text", "Tell us what went wrong", sub="A real person reads this", name="Open support"),
])

add("Profile", "P9-delete",
    desk("Member · Profile — P9 Delete Account",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Privacy and data")}</Frame>'
        + head_chip([("Delete your", False), ("account", True)], 30)
        + T(15, "regular", "var:text/muted", "Read this first — some of it is not ours to delete.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P9_GONE}{P9_KEPT}{P9_REASON}</Frame>'
          f'<Frame w={{400}} flex="col" gap={{16}}>{P9_ALT}{P9_CONFIRM}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P9 Delete Account · Mobile",
        appbar("Delete account")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{P9_ALT}{P9_GONE}</Frame>'))

# =====================================================================================
# ALERTS & SYSTEM STATES
# =====================================================================================
N1_TODAY = (f'<Frame w="fill" flex="col" gap={{10}}>{eyebrow("TODAY")}'
            f'{notif_row("bell-ring","Visit tomorrow at 10:30","Dr. Ngozi Okafor · virtual. Tap to test your camera before then.","2 hours ago","Notif visit",unread=True,tone="info")}'
            f'{notif_row("eye","Dr. Okafor opened your records","She read “Hypertension review” at 09:12. You allowed this until 21 Aug.","3 hours ago","Notif audit",unread=True,tone="muted")}'
            f'{notif_row("pill","Metformin at 18:00","One tablet with food.","5 hours ago","Notif med",unread=True,tone="ok")}</Frame>')
N1_EARLIER = (f'<Frame w="fill" flex="col" gap={{10}}>{eyebrow("EARLIER THIS WEEK")}'
              f'{notif_row("package","Refill approved","Metformin 500 mg · 30 days waiting at Garki pharmacy.","Tue","Notif refill",tone="ok")}'
              f'{notif_row("flask-conical","New result: Full blood count","One value is outside the normal range — we explain what it means.","Mon","Notif result",tone="warn")}'
              f'{notif_row("calendar-clock","Dr. Bello moved your visit","From Tue 5 Mar to Thu 7 Mar. Say yes or pick another time.","Sun","Notif moved",tone="warn")}'
              f'{notif_row("sparkles","A slot opened with Dr. Adeyemi","Thursday 09:00 — you asked to be told.","Sat","Notif slot",tone="info")}</Frame>')

add("Alerts", "N1-notifs",
    desk("Member · Alerts — N1 Notifications",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{head_chip([("Your", False), ("notifications", True)], 30)}'
        f'<Frame flex="row" gap={{10}} items="center">'
        f'{mini_btn("Mark all read","Mark all read","check-check","ghost",grow=False)}'
        f'{mini_btn("Settings","Open notifs P6","settings","ghost",grow=False)}</Frame></Frame>'
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{18}}>{N1_TODAY}{N1_EARLIER}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>'
          f'{group_card("Needs you", [list_row("calendar-clock","Confirm the new time with Dr. Bello",sub="Expires in 2 days",name="Notif moved",tint="var:state/warning-bg"),list_row("flask-conical","Read your blood count result",sub="One value out of range",name="Open lab R3"),list_row("package","Collect your refill",sub="Waiting at Garki pharmacy",name="Open refill M3")])}'
          f'{group_card("Filter", [radio_row("Everything",on=True,name="Notif filter all"),radio_row("Only visits",name="Notif filter visits"),radio_row("Only records and results",name="Notif filter records"),radio_row("Only medicines",name="Notif filter meds")])}</Frame></Frame>',
        SIDE["Home"]),
    mob("Member · Alerts — N1 Notifications · Mobile",
        appbar("Notifications", right=circle_btn("check-check", "Mark all read"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{4}} pb={{8}}>'
          f'{N1_TODAY}</Frame>',
        nav=bottom_nav(0)))

N2_EMPTY = empty_state("inbox", "Nothing needs you right now",
    "Visit reminders, results and refill updates land here. We only send what matters — and never marketing you did not ask for.",
    primary=ghost("Choose what we tell you", "Open notifs P6", "settings"), tone="ok")
add("Alerts", "N2-notifs-empty",
    desk("Member · Alerts — N2 No Notifications",
        head_chip([("Your", False), ("notifications", True)], 30)
        + f'<Frame w="fill" flex="row" justify="center" pt={{20}}>'
          f'<Frame w={{560}} flex="col">{N2_EMPTY}</Frame></Frame>',
        SIDE["Home"]),
    mob("Member · Alerts — N2 No Notifications · Mobile",
        appbar("Notifications", back=False)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{20}} pb={{8}}>{N2_EMPTY}</Frame>',
        nav=bottom_nav(0)))

# ---------------- X1 loading
X1_SKEL_M = (f'<Frame w="fill" flex="col" gap={{14}}>'
             f'<Frame w="fill" flex="row" gap={{12}} items="center">'
             f'<Rect w={{46}} h={{46}} rounded={{999}} bg="var:neutral/200" />'
             f'<Frame grow={{1}} flex="col" gap={{7}}>{skel(w=120,h=11)}{skel(w=90,h=15)}</Frame></Frame>'
             f'{skel(h=50,r=999)}'
             f'{skel_card(3)}'
             f'{rows_of([skel(h=86,r=20),skel(h=86,r=20),skel(h=86,r=20)],3,10)}'
             f'{skel_card(2)}{skel_card(3)}</Frame>')
add("Alerts", "X1-loading",
    desk("Member · States — X1 Loading",
        f'{skel(h=132,r=28)}'
        f'{rows_of([skel(h=118,r=24),skel(h=118,r=24),skel(h=118,r=24),skel(h=118,r=24)],4,16)}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{skel_card(4)}{skel_card(3)}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{skel_card(3,avatar=False)}{skel_card(4,avatar=False)}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{9}} justify="center" items="center" pt={{6}}>'
        f'{I("loader",16,M_IC)}{T(13,"regular","var:text/muted","Loading your records…")}</Frame>',
        SIDE["Home"]),
    mob("Member · States — X1 Loading · Mobile",
        f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{14}} pb={{8}}>{X1_SKEL_M}'
        f'<Frame w="fill" flex="row" gap={{9}} justify="center" items="center">'
        f'{I("loader",15,M_IC)}{T(12,"regular","var:text/muted","Loading…")}</Frame></Frame>',
        nav=bottom_nav(0)))

# ---------------- X2 offline
X2_BANNER = (f'<Frame w="fill" flex="row" gap={{13}} items="center" p={{16}} rounded={{22}} bg="var:state/warning-bg">'
             f'{I("cloud-off",19,WARN_IC)}'
             f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","You are offline")}'
             f'{T(12,"regular","var:text/muted","Showing what was saved on this phone at 08:02 today.",w="fill")}</Frame>'
             f'{mini_btn("Retry","Retry X2","refresh-cw","ghost",grow=False)}</Frame>')
X2_WORKS = group_card("What still works without a connection", [
    list_row("clipboard-list", "Reading your records", sub="Everything downloaded up to 08:02", name="Offline records", chevron=False),
    list_row("pill", "Medicine reminders", sub="They run on your phone, not on our servers", name="Offline meds", chevron=False),
    list_row("qr-code", "Your Medra ID and summary", sub="Enough for a clinic to check you in", name="Offline qr", chevron=False),
    list_row("phone-call", "Calling a clinic", sub="Numbers are saved with each visit", name="Offline call", chevron=False),
])
X2_WAITS = group_card("What has to wait", [
    list_row("search", "Finding and booking a doctor", sub="Availability changes by the minute — we will not show you a stale slot", name="Offline book", chevron=False),
    list_row("video", "Joining a video visit", sub="Ask the clinic to ring your phone instead", name="Offline video", chevron=False),
    list_row("share-2", "Sharing records", sub="Queued — it goes out the moment you are back", name="Offline share", chevron=False),
], footer="Nothing you do offline is lost. Marks, notes and edits sync when the connection returns.")

add("Alerts", "X2-offline",
    desk("Member · States — X2 Offline",
        f'{X2_BANNER}'
        f'<Frame w="fill" flex="row" gap={{18}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{X2_WORKS}{X2_WAITS}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>'
        f'{empty_state("wifi-off","No connection","We keep checking. You do not have to stay on this screen.",primary=cta("Try again","Retry X2","refresh-cw"),tone="warn")}'
        f'{note("info","Saved records use about 8 MB. Turn this off in Language and data if your phone is short on space.","info")}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · States — X2 Offline · Mobile",
        appbar("My records", back=False)
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{X2_BANNER}{X2_WORKS}</Frame>',
        nav=bottom_nav(2)))

# ---------------- X3 error
X3 = empty_state("triangle-alert", "Something went wrong on our side",
    "This is not your phone and it is not your data — a Medra service failed to answer. Nothing you saved is affected.",
    primary=cta("Try again", "Retry X3", "refresh-cw"),
    secondary=ghost("Go to my records", "Nav Records", "clipboard-list"), tone="warn")
X3_REF = (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{16}} rounded={{20}} bg="var:neutral/50">'
          f'{I("copy",17,M_IC)}'
          f'<Frame grow={{1}} flex="col" gap={{2}}>{T(12,"regular","var:text/muted","Reference for support")}'
          f'{T(14,"semibold","var:text/strong","ERR-7731-A2 · 14 Aug 09:41")}</Frame>'
          f'{mini_btn("Copy","Copy error ref","copy","ghost",grow=False)}</Frame>')
X3_HELP = group_card("If it keeps happening", [
    list_row("refresh-cw", "Close Medra and open it again", name="Err retry", chevron=False),
    list_row("wifi", "Check your data or Wi-Fi", name="Err network", chevron=False),
    list_row("message-square-text", "Message us with the reference", sub="We reply in minutes, every day", name="Open support"),
    list_row("phone-call", "Urgent about a visit? Call the clinic", sub="Numbers are on each visit", name="Err call"),
], footer="If you need care right now and Medra is down, go to the clinic — your booking is on their system too.")

add("Alerts", "X3-error",
    desk("Member · States — X3 Something Went Wrong",
        f'<Frame w="fill" flex="row" gap={{20}} justify="center" items="start" pt={{16}}>'
        f'<Frame w={{520}} flex="col" gap={{16}}>{X3}{X3_REF}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{16}}>{X3_HELP}</Frame></Frame>',
        SIDE["Home"]),
    mob("Member · States — X3 Something Went Wrong · Mobile",
        appbar(None, back=False, right=circle_btn("circle-help", "Open support"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{14}} px={{20}} pt={{10}} pb={{8}}>'
          f'{X3}{X3_REF}</Frame>',
        nav=bottom_nav(0)))


# =====================================================================================
# ADDED AFTER THE 1 AUG PRODUCT REVIEW
# =====================================================================================

# ---------------- W0  join a video visit (MVP: the doctor's own meeting link)
# "for MVP make it open ... the doctor will set up the meeting and add the link, and the link
#  is embedded into the Join button" — in-app video (W1/W2/W4) stays designed, for phase 2.
W0_LINK = (f'<Frame w="fill" flex="col" gap={{14}} p={{20}} rounded={{26}} bg="var:bg/base" '
           f'stroke="var:border/accent" strokeWidth={{2}}>'
           f'<Frame w="fill" flex="row" gap={{13}} items="center">'
           f'<Frame w={{46}} h={{46}} rounded={{15}} bg="var:state/info-bg" flex="col" justify="center" items="center">'
           f'{I("video",22,A_IC)}</Frame>'
           f'<Frame grow={{1}} flex="col" gap={{2}}>{T(15,"semibold","var:text/strong","Google Meet")}'
           f'{T(12,"regular","var:text/muted","Dr. Okafor set this up for your visit",w="fill")}</Frame>'
           f'{status_pill("today","Opens 10:20")}</Frame>'
           f'<Frame w="fill" flex="row" gap={{10}} items="center" px={{14}} py={{13}} rounded={{16}} bg="var:neutral/50">'
           f'{I("external-link",15,M_IC)}{T(13,"regular","var:text/default","meet.google.com/kfa-jrqz-nmo",w="fill")}'
           f'<Frame name="Btn Copy meet link" flex="row">{I("copy",15,N_IC)}</Frame></Frame>'
           f'{cta("Join the visit","Open meeting W0","external-link")}'
           f'{T(11,"regular","var:text/muted","This opens Google Meet. You do not need an account — just tap and allow your camera.",w="fill",align="center")}</Frame>')
W0_READY = group_card("Before you tap join", [
    prep_step(1, "Find somewhere quiet with a signal", "A doctor cannot examine what they cannot hear."),
    prep_step(2, "Have your readings and medicines nearby", "Blood pressure, the pack of anything you take."),
    prep_step(3, "Share your records if you have not", "Dr. Okafor sees only what you allow.", done=True),
])
W0_FALLBACK = group_card("If the video will not work", [
    list_row("phone-call", "Ask the clinic to call my phone", sub="+234 801 234 5678 — no data needed at all", name="Phone instead W0"),
    list_row("message-circle", "Message the clinic on WhatsApp", sub="+234 809 112 4477", name="WhatsApp clinic W0"),
    list_row("calendar-clock", "Move this visit", sub="Free more than 4 hours before", name="Reschedule V4"),
], footer="You paid for this consultation. If it cannot go ahead, you are refunded in full — you never chase us for it.")
W0_PHASE2 = (f'<Frame name="Btn Phase 2 call" w="fill" flex="row" gap={{11}} items="center" p={{15}} rounded={{20}} '
             f'bg="var:bg/muted">{I("sparkles",17,A_IC)}'
             f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong","Coming later: video inside Medra")}'
             f'{T(11,"regular","var:text/muted","No third-party app, and the doctor writes the note as you talk. Preview the design →",w="fill")}</Frame></Frame>')

add("Visits", "W0-join",
    desk("Member · Virtual — W0 Join by Link",
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Visit details")}</Frame>{status_pill("soon","Starts in 8 minutes")}</Frame>'
        + head_chip([("Your visit with", False), ("Dr. Okafor", True)], 30)
        + f'<Frame w="fill" flex="row" gap={{20}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{W0_LINK}{W0_READY}</Frame>'
          f'<Frame w={{380}} flex="col" gap={{16}}>{W0_FALLBACK}{W0_PHASE2}</Frame></Frame>',
        SIDE["Visits"]),
    mob("Member · Virtual — W0 Join by Link · Mobile",
        appbar("Your visit", right=circle_btn("circle-help", "Help call"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{8}}>'
          f'{W0_LINK}'
          f'{group_card("If the video will not work", [list_row("phone-call","Ask the clinic to call me",sub="No data needed",name="Phone instead W0"),list_row("message-circle","Message on WhatsApp",name="WhatsApp clinic W0")], p=16)}</Frame>',
        nav=bottom_nav(1)))

# ---------------- R10  print / share a one-page summary
# "what would the print one page summary look like? ... can they select what to print?"
R10_PICK = group_card("What goes on the page?", [
    consent_row("droplet", "Blood group and genotype", "O+ · AA", "Print blood", locked=True),
    consent_row("triangle-alert", "Allergies", "Penicillin", "Print allergies", locked=True),
    consent_row("pill", "Current medicines", "3 medicines with doses", "Print meds"),
    consent_row("heart-pulse", "Long-term conditions", "Hypertension, diagnosed Jun 2026", "Print conditions"),
    consent_row("stethoscope", "Last 3 consultations", "Date, doctor, diagnosis — one line each", "Print visits"),
    consent_row("flask-conical", "Latest lab results", "Full blood count, 12 Jun", "Print labs", on=False),
    consent_row("syringe", "Immunisations", "Yellow fever, tetanus", "Print vaccines", on=False),
    consent_row("phone-call", "Emergency contact", "Ijeoma Okeke · +234 805 998 1122", "Print emergency"),
], footer="Blood group and allergies always print. In an emergency they are the two lines that matter.")

R10_PREVIEW = (f'<Frame w="fill" flex="col" gap={{13}} p={{22}} rounded={{22}} bg="var:bg/base" '
               f'stroke="var:border/default" strokeWidth={{1}}>'
               f'<Frame w="fill" flex="row" justify="between" items="center">'
               f'<Image image="assets/logo/logo-gradient.png" w={{70}} h={{52}} />'
               f'<Frame w={{62}} h={{62}} rounded={{12}} bg="var:neutral/50" flex="col" justify="center" items="center">'
               f'{I("qr-code",36,N_IC)}</Frame></Frame>'
               f'<Frame w="fill" flex="col" gap={{2}}>{T(18,"bold","var:text/strong","Amara Chinaza Okeke")}'
               f'{T(12,"regular","var:text/muted","MDR-8842-19 · 34 years · Area 3, Garki, Abuja")}</Frame>'
               f'{hr()}'
               f'{kv_pair(kv("Blood group","O+","droplet"), kv("Genotype","AA","activity"))}'
               f'{kv("Allergies","Penicillin — rash and swelling","triangle-alert")}'
               f'{kv("Conditions","Hypertension (Jun 2026)","heart-pulse")}'
               f'{kv("Medicines","Amlodipine 5 mg morning · Metformin 500 mg evening · Vitamin D 1000 IU","pill")}'
               f'{kv("Emergency contact","Ijeoma Okeke (sister) · +234 805 998 1122","phone-call")}'
               f'{hr()}'
               f'{T(10,"regular","var:text/faint","Printed from Medra on 14 Aug 2026. Scan the code for the full record, with the member’s permission.",w="fill")}</Frame>')

R10_ACTIONS = (f'<Frame w="fill" flex="col" gap={{11}}>'
               f'{cta("Print this page","Print now R10","printer")}'
               f'{ghost("Save as PDF","Save pdf R10","download")}'
               f'{ghost("Send to my email","Email summary R10","mail")}'
               f'{ghost("Show as a QR code instead","QR share R5","qr-code")}</Frame>')

add("Records", "R10-summary",
    desk("Member · Records — R10 One-page Summary",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Privacy and data")}</Frame>'
        + head_chip([("A page you can", False), ("hand over", True)], 30)
        + T(15, "regular", "var:text/muted",
            "For a walk-in clinic, an emergency, or a relative who keeps your papers. You choose what is on it.", w="fill")
        + f'<Frame w="fill" flex="row" gap={{20}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{R10_PICK}</Frame>'
          f'<Frame w={{420}} flex="col" gap={{16}}>{eyebrow("PREVIEW")}{R10_PREVIEW}{R10_ACTIONS}</Frame></Frame>',
        SIDE["Records"]),
    mob("Member · Records — R10 One-page Summary · Mobile",
        appbar("One-page summary", right=circle_btn("printer", "Print now R10"))
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{group_card("What goes on the page?", [consent_row("droplet","Blood group and genotype","O+ · AA","Print blood",locked=True),consent_row("triangle-alert","Allergies","Penicillin","Print allergies",locked=True),consent_row("pill","Current medicines","3 medicines","Print meds"),consent_row("stethoscope","Last 3 consultations","One line each","Print visits")], p=16)}'
          f'<Frame grow={{1}} />{cta("Preview and print","Print now R10","printer")}'
          f'{ghost("Save as PDF","Save pdf R10","download")}</Frame>'))

# ---------------- N0  the bell overlay
# "once they click on the notification it shows an overlay with maybe five important
#  notifications, then View all brings them to the full screen"
N0_PANEL = (f'<Frame w={{400}} flex="col" gap={{12}} p={{18}} rounded={{26}} bg="var:bg/base" '
            f'stroke="var:border/default" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(16,"bold","var:text/strong","Notifications")}'
            f'<Frame flex="row" gap={{9}} items="center">'
            f'<Frame flex="row" px={{9}} py={{4}} rounded={{999}} bg="var:state/error-bg">'
            f'{T(11,"semibold","var:state/error","3 new")}</Frame>'
            f'<Frame name="Btn Close notif panel" flex="row">{I("x",18,M_IC)}</Frame></Frame></Frame>'
            f'{notif_row("bell-ring","Visit tomorrow at 10:30","Dr. Ngozi Okafor · virtual","2h ago","Notif visit",unread=True,tone="info")}'
            f'{notif_row("eye","Dr. Okafor opened your records","“Hypertension review” at 09:12","3h ago","Notif audit",unread=True,tone="muted")}'
            f'{notif_row("pill","Metformin at 18:00","One tablet with food","5h ago","Notif med",unread=True,tone="ok")}'
            f'{notif_row("package","Refill approved","Waiting at Garki pharmacy","Tue","Notif refill",tone="ok")}'
            f'{notif_row("flask-conical","New result: Full blood count","One value outside the normal range","Mon","Notif result",tone="warn")}'
            f'{hr()}'
            f'<Frame w="fill" flex="row" gap={{11}}>'
            f'{mini_btn("Mark all read","Mark all read","check-check","ghost")}'
            f'{mini_btn("View all","Open notifs N1","arrow-right","teal")}</Frame></Frame>')

# The panel drops over the home screen, so the frame shows the dashboard dimmed behind it.
N0_BEHIND = rows_of([
    stat_card("calendar-check", "2", "Upcoming visits", "Next in 2 days", "tint-teal.jpg"),
    stat_card("pill", "3", "Active medicines", "1 due at 18:00", "tint-mint.jpg"),
    stat_card("clipboard-list", "14", "Records", "Across 3 clinics", "tint-ocean.jpg"),
    stat_card("shield-check", "1", "Active share", "Expires in 6 days", "tint-blue.jpg"),
], 4, 16)
N0_PANEL_M = (f'<Frame w="fill" flex="col" gap={{11}} p={{16}} rounded={{26}} bg="var:bg/base" '
              f'stroke="var:border/default" strokeWidth={{1}}>'
              f'<Frame w="fill" flex="row" justify="between" items="center">'
              f'{T(16,"bold","var:text/strong","Notifications")}'
              f'<Frame flex="row" gap={{9}} items="center">'
              f'<Frame flex="row" px={{9}} py={{4}} rounded={{999}} bg="var:state/error-bg">'
              f'{T(11,"semibold","var:state/error","3 new")}</Frame>'
              f'<Frame name="Btn Close notif panel" flex="row">{I("x",18,M_IC)}</Frame></Frame></Frame>'
              f'{notif_row("bell-ring","Visit tomorrow at 10:30","Dr. Ngozi Okafor · virtual","2h ago","Notif visit",unread=True,tone="info")}'
              f'{notif_row("eye","Dr. Okafor opened your records","“Hypertension review” at 09:12","3h ago","Notif audit",unread=True,tone="muted")}'
              f'{notif_row("pill","Metformin at 18:00","One tablet with food","5h ago","Notif med",unread=True,tone="ok")}'
              f'{notif_row("package","Refill approved","Waiting at Garki pharmacy","Tue","Notif refill",tone="ok")}'
              f'{hr()}'
              f'<Frame w="fill" flex="row" gap={{11}}>'
              f'{mini_btn("Mark all read","Mark all read","check-check","ghost")}'
              f'{mini_btn("View all","Open notifs N1","arrow-right","teal")}</Frame></Frame>')

add("Alerts", "N0-panel",
    desk("Member · Alerts — N0 Notification Panel",
        hero_banner()
        + f'<Frame w="fill" flex="row" justify="end" pt={{2}}>{N0_PANEL}</Frame>'
        + N0_BEHIND,
        SIDE["Home"]),
    mob("Member · Alerts — N0 Notification Panel · Mobile",
        greet_bar()
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{16}} pt={{2}} pb={{8}}>'
          f'{N0_PANEL_M}</Frame>',
        nav=bottom_nav(0)))

# ---------------- P3b  family plan
# "they can book for two people first for free, then from the third they have to pay ...
#  more like they taste the service before"
P3B_STATE = (f'<Frame w="fill" flex="row" gap={{13}} items="center" p={{18}} rounded={{22}} bg="var:state/warning-bg">'
             f'{I("users-round",20,WARN_IC)}'
             f'<Frame grow={{1}} flex="col" gap={{2}}>{T(15,"semibold","var:text/strong","You have used both free places")}'
             f'{T(12,"regular","var:text/muted","Chidi and Mama Grace. Adding a third person needs a family plan.",w="fill")}</Frame></Frame>')
P3B_PLAN = (f'<Frame w="fill" flex="col" gap={{14}} p={{22}} rounded={{26}} bg="var:state/info-bg" '
            f'stroke="var:border/accent" strokeWidth={{2}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{eyebrow("MEDRA FAMILY")}{status_pill("new","Recommended")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="end">{T(34,"bold","var:text/strong","₦3,000")}'
            f'{T(14,"regular","var:text/muted","/month")}</Frame>'
            f'<Frame w="fill" flex="col" gap={{9}}>'
            f'{proof("users-round","Up to 6 people, including you",dark=False)}'
            f'{proof("clipboard-list","A separate record for each of them",dark=False)}'
            f'{proof("calendar-plus","Book and reschedule for anyone",dark=False)}'
            f'{proof("bell-ring","Their reminders on your phone",dark=False)}'
            f'{proof("credit-card","One payment method for the family",dark=False)}</Frame>'
            f'{hr("var:border/accent")}'
            f'{T(12,"regular","var:text/muted","Or ₦1,500 per extra person per month if you only need one more. Cancel any time — nobody loses their records, you just stop managing them.",w="fill")}</Frame>')
P3B_FREE = group_card("Always free, plan or no plan", [
    list_row("circle-user", "Your own account and records", name="Free own", chevron=False),
    list_row("users", "Two people in your care", sub="Chidi and Mama Grace stay free forever", name="Free two", chevron=False),
    list_row("clipboard-list", "Everything they already have", sub="Records, visits and prescriptions are theirs to keep", name="Free records", chevron=False),
], footer="Consultation fees are separate and go to the doctor — the family plan only covers managing people.")

add("Profile", "P3b-family",
    desk("Member · Profile — P3b Family Plan",
        light_banner("banner-family.jpg", "PEOPLE I CARE FOR", "Add a third person",
                     "Two places are free. Beyond that, a family plan keeps everyone in one app.",
                     actions=mini_btn("Maybe later", "Back dependants P3b", None, "ghost", grow=False))
        + f'<Frame w="fill" flex="row" gap={{18}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P3B_STATE}{P3B_FREE}</Frame>'
          f'<Frame w={{400}} flex="col" gap={{16}}>{P3B_PLAN}'
          f'{cta("Start the family plan","Subscribe family P3b","credit-card")}'
          f'{ghost("Add one person for ₦1,500","Add one P3b","user-plus")}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P3b Family Plan · Mobile",
        appbar("Family plan")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{P3B_STATE}{P3B_PLAN}<Frame grow={{1}} />'
          f'{cta("Start the family plan","Subscribe family P3b","credit-card")}'
          f'{link("","Add one person for ₦1,500","Add one P3b")}</Frame>'))

# ---------------- P9b  the deletion gate
add("Profile", "P9b-delete-confirm",
    desk("Member · Profile — P9b Confirm Deletion",
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
        f'{T(14,"semibold","var:text/default","Delete account")}</Frame>'
        + head_chip([("Last chance to", False), ("change your mind", True)], 30)
        + f'<Frame w="fill" flex="row" gap={{20}} items="start">'
          f'<Frame grow={{1}} flex="col" gap={{16}}>{P9_REASON}{P9_KEPT}</Frame>'
          f'<Frame w={{400}} flex="col" gap={{16}}>{P9_CONFIRM}</Frame></Frame>',
        SIDE["Profile"]),
    mob("Member · Profile — P9b Confirm Deletion · Mobile",
        appbar("Confirm deletion")
        + f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{20}} pt={{4}} pb={{10}}>'
          f'{P9_CONFIRM}</Frame>'))

# =====================================================================================
# INTERACTIVE COMPONENT STATES  (components-member2.js turns these into variant sets)
# =====================================================================================
CMP = []
def cmp_frame(comp, prop, value, body, w=320, h=None, dark=False):
    hh = f' minH={{{h}}}' if h else ''
    bg = "var:bg/band" if dark else "var:bg/base"
    CMP.append((f"cmp/{comp}/{prop}={value}",
        f'<Frame name="cmp/{comp}/{prop}={value}" w={{{w}}}{hh} flex="col" p={{16}} bg="{bg}">{body}</Frame>'))

def _tab_one(on):
    bar = ('<Rect w="fill" h={3} rounded={999} bg="var:brand/teal" />' if on
           else '<Rect w="fill" h={3} rounded={999} bg="var:border/subtle" />')
    return (f'<Frame w="fill" flex="col" gap={{9}} items="center">'
            f'{T(15,"semibold" if on else "medium","var:text/strong" if on else "var:text/muted","Upcoming")}'
            f'{bar}</Frame>')
cmp_frame("Tab", "State", "Active", _tab_one(True), w=170)
cmp_frame("Tab", "State", "Inactive", _tab_one(False), w=170)

for kind, label in (("confirmed", "Confirmed"), ("completed", "Completed"),
                    ("cancelled", "Cancelled"), ("pending", "Pending"), ("live", "Live")):
    cmp_frame("Status Pill", "State", label, status_pill(kind), w=170)

cmp_frame("Call Control", "State", "On",    call_btn("mic", "CMic", "on", 56), w=110, dark=True)
cmp_frame("Call Control", "State", "Off",   call_btn("mic-off", "CMic", "off", 56), w=110, dark=True)
cmp_frame("Call Control", "State", "Idle",  call_btn("mic", "CMic", "dark", 56), w=110, dark=True)
cmp_frame("Call Control", "State", "End",   call_btn("phone-off", "CEnd", "end", 56), w=110, dark=True)

_LR = list_row("bell-ring", "Notifications", value="Push + SMS", name="CRow")
cmp_frame("List Row", "State", "Default", _LR, w=420)
cmp_frame("List Row", "State", "Hover",
    f'<Frame w="fill" flex="col" px={{10}} rounded={{16}} bg="var:neutral/50">{_LR}</Frame>', w=420)
cmp_frame("List Row", "State", "Pressed",
    f'<Frame w="fill" flex="col" px={{10}} rounded={{16}} bg="var:bg/muted">{_LR}</Frame>', w=420)

cmp_frame("Consent Scope", "State", "On",
    consent_row("flask-conical", "Lab results", "4 results", "CScope"), w=420)
cmp_frame("Consent Scope", "State", "Off",
    consent_row("flask-conical", "Lab results", "4 results", "CScope", on=False), w=420)
cmp_frame("Consent Scope", "State", "Locked",
    consent_row("triangle-alert", "Allergies and medicines", "Always shared", "CScope", locked=True), w=420)

cmp_frame("Dose", "State", "Due",   dose_row("18:00", "Metformin", "500 mg · 1 tablet", "due", "CDose"), w=380)
cmp_frame("Dose", "State", "Taken", dose_row("08:00", "Amlodipine", "5 mg · 1 tablet", "taken"), w=380)
cmp_frame("Dose", "State", "Missed", dose_row("13:00", "Vitamin D", "1000 IU", "missed", "CDose"), w=380)

for nm, jsx in CMP:
    fid = nm.replace("cmp/", "CMP-").replace("/", "-").replace("=", "-").replace(" ", "")
    frames.append(("Components", fid + ".jsx", jsx))
    ORDER.setdefault("Components", []).append(fid)

# =====================================================================================
# WRITE THE BUNDLE
# =====================================================================================
def sanitize(s): return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)', '&amp;', s)
manifest = {}
for page, fn, jsx in frames:
    open(os.path.join(OUT, fn), "w").write(sanitize(jsx))
    manifest.setdefault(page, []).append(fn)
open(os.path.join(OUT, "pages.json"), "w").write(json.dumps(manifest, indent=2))

# ---- batch-1 frame names, read off disk so the nav map covers Find & Book too ----
B1 = {}
for fn in sorted(os.listdir(SRC1)):
    if not fn.endswith(".jsx") or fn.startswith("CMP-"): continue
    m = re.search(r'name="([^"]+)"', open(os.path.join(SRC1, fn)).read())
    if not m: continue
    fid, side = fn[:-6], fn[-5]
    B1.setdefault(fid, {})[side] = m.group(1)
B1_PAIRS = {k: (v.get("d"), v.get("m")) for k, v in B1.items() if v.get("d") and v.get("m")}

AUTH_LOGIN = ("Auth · Member — M6 Log In", "Auth · Member — M6 Log In · Mobile")

# ---- the nav map: every tab, on every frame in both batches ----
NAV = {
  "Btn Nav Home":      B1_PAIRS["H1-home"],
  "Btn Nav Find":      B1_PAIRS["S1-results"],
  "Btn Nav Visits":    NAMES["V1-visits"],
  "Btn Nav Records":   NAMES["R1-records"],
  "Btn Nav Meds":      NAMES["M1-meds"],
  "Btn Nav Profile":   NAMES["P0-profile"],
  "Btn Notifications": NAMES["N0-panel"],
}
ALL_PAIRS = dict(B1_PAIRS); ALL_PAIRS.update(NAMES)

# ---- screen-to-screen transitions (fid, hotspot, fid|B1:fid|AUTH) ----
TRN = [
 # ---- visits
 ("V1-visits","Btn Visits tab Past","V2-past"),("V1-visits","Btn Visits tab Upcoming","V1-visits"),
 ("V1-visits","Btn Join visit","W0-join"),("V1-visits","Btn Reschedule V1","V5-reschedule"),
 ("V1-visits","Btn Cancel V1","V6-cancel"),("V1-visits","Btn Visit MDR-4820-71","V4-visit"),
 ("V1-visits","Btn Visit MDR-4901-08","V4-visit"),("V1-visits","Btn Open visit V1b","V4-visit"),
 ("V1-visits","Btn Book new V1","B1:S1-results"),("V1-visits","Btn Export visits","V2-past"),
 ("V2-past","Btn Visits tab Upcoming","V1-visits"),("V2-past","Btn Visits tab Past","V2-past"),
 ("V2-past","Btn Open note R2","R2-note"),("V2-past","Btn Book again","B1:P1-profile"),
 ("V2-past","Btn Past visit Jun","R2-note"),("V2-past","Btn Past visit Apr","R2-note"),
 ("V2-past","Btn Past visit Mar","V7-cancelled"),("V2-past","Btn Export visits","V2-past"),
 ("V3-visits-empty","Btn Find doctor V3","B1:S1-results"),("V3-visits-empty","Btn Visits tab Past","V2-past"),
 ("V4-visit","Btn Join visit","W0-join"),("V4-visit","Btn Reschedule V4","V5-reschedule"),
 ("V4-visit","Btn Cancel V4","V6-cancel"),("V4-visit","Btn Share R5","R5-share"),
 ("V4-visit","Btn Share visit V4","R5-share"),("V4-visit","Btn Back","V1-visits"),
 ("V4-visit","Btn Reminders V4","P6-notifs"),
 ("V5-reschedule","Btn Confirm reschedule","V4-visit"),("V5-reschedule","Btn Keep original V5","V4-visit"),
 ("V5-reschedule","Btn Back","V4-visit"),
 ("V6-cancel","Btn Confirm cancel","V7-cancelled"),("V6-cancel","Btn Keep visit V6","V4-visit"),
 ("V6-cancel","Btn Back","V4-visit"),
 ("V7-cancelled","Btn Back visits V7","V1-visits"),("V7-cancelled","Btn Rebook V7","B1:S1-results"),
 # ---- virtual visit
 ("W0-join","Btn Open meeting W0","W3-callend"),("W0-join","Btn Back","V4-visit"),
 ("W0-join","Btn Phone instead W0","V4-visit"),("W0-join","Btn WhatsApp clinic W0","V4-visit"),
 ("W0-join","Btn Reschedule V4","V5-reschedule"),("W0-join","Btn Phase 2 call","W1-precall"),
 ("W0-join","Btn Help call","V4-visit"),
 ("W1-precall","Btn Join call W1","W2-incall"),("W1-precall","Btn Leave precall","V4-visit"),
 ("W1-precall","Btn Phone instead W1","V4-visit"),("W1-precall","Btn Help call","V4-visit"),
 ("W2-incall","Btn End call W2","W3-callend"),("W2-incall","Btn Share record W2","R5-share"),
 ("W3-callend","Btn Open note R2","R2-note"),("W3-callend","Btn Back visits W3","V1-visits"),
 ("W3-callend","Btn W3 rx","M2-med"),("W3-callend","Btn W3 tests","R3-lab"),
 ("W3-callend","Btn W3 followup","B1:B1-slot"),("W3-callend","Btn W3 assess","R2-note"),
 ("W3-callend","Btn Download note","W3-callend"),
 ("W4-lost","Btn Retry call W4","W2-incall"),("W4-lost","Btn Audio only W4","W2-incall"),
 ("W4-lost","Btn Phone instead W4","V4-visit"),("W4-lost","Btn End call W4","V1-visits"),
 # ---- records
 ("R1-records","Btn Open upload R7","R7-upload"),("R1-records","Btn Share R5","R5-share"),
 ("R1-records","Btn Open access R6","R6-access"),("R1-records","Btn Open vitals R4","R4-vitals"),
 ("R1-records","Btn Open note R2","R2-note"),("R1-records","Btn Open med M2","M2-med"),
 ("R1-records","Btn Open lab R3","R3-lab"),("R1-records","Btn Open vaccine","R3-lab"),
 ("R1-records","Btn Open upload","R3-lab"),("R1-records","Btn Open meds R1","M1-meds"),
 ("R1-records","Btn Open vaccines","R3-lab"),("R1-records","Btn Print summary","R10-summary"),
 ("R1-records","Btn Request clinic","R1-records"),("R1-records","Btn Search records","R1-records"),
 ("R2-note","Btn Back","R1-records"),("R2-note","Btn Share R5","R5-share"),
 ("R2-note","Btn Open med M2","M2-med"),("R2-note","Btn Open lab R3","R3-lab"),
 ("R2-note","Btn Open vitals R4","R4-vitals"),("R2-note","Btn Open visit V4","V4-visit"),
 ("R2-note","Btn Book follow-up","B1:B1-slot"),
 ("R3-lab","Btn Back","R1-records"),("R3-lab","Btn Share R5","R5-share"),
 ("R3-lab","Btn Trend hb","R4-vitals"),("R3-lab","Btn Trend plt","R4-vitals"),
 ("R3-lab","Btn Open vitals R4","R4-vitals"),("R3-lab","Btn Ask about lab","B1:S1-results"),
 ("R4-vitals","Btn Back","R1-records"),("R4-vitals","Btn Add reading R4","R7-upload"),
 ("R4-vitals","Btn Add bp","R7-upload"),("R4-vitals","Btn Add weight","R7-upload"),
 ("R4-vitals","Btn Add sugar","R7-upload"),("R4-vitals","Btn Open upload R7","R7-upload"),
 ("R5-share","Btn Confirm share R5","R6-access"),("R5-share","Btn Cancel share R5","R1-records"),
 ("R6-access","Btn Share R5","R5-share"),("R6-access","Btn Revoke Okafor","R6-access"),
 ("R6-access","Btn Revoke all","R6-access"),
 ("R7-upload","Btn Open camera R7","R8-added"),("R7-upload","Btn Save record R7","R8-added"),
 ("R7-upload","Btn Back","R1-records"),
 ("R8-added","Btn Back records R8","R1-records"),("R8-added","Btn Open upload R7","R7-upload"),
 ("R8-added","Btn Edit type R8","R7-upload"),("R8-added","Btn Edit date R8","R7-upload"),
 ("R8-added","Btn Edit clinic R8","R7-upload"),("R8-added","Btn Edit pages R8","R7-upload"),
 ("R8-added","Btn Edit share R8","R5-share"),
 ("R10-summary","Btn Back","P8-privacy"),
 ("R9-records-empty","Btn Open upload R7","R7-upload"),("R9-records-empty","Btn Find doctor R9","B1:S1-results"),
 # ---- medicines
 ("M1-meds","Btn Open med M2","M2-med"),("M1-meds","Btn Open med M2b","M2-med"),
 ("M1-meds","Btn Open med M2c","M2-med"),("M1-meds","Btn Open refill M3","M3-refill"),
 ("M1-meds","Btn Open reminders M4","M4-reminders"),("M1-meds","Btn Add med M1","R7-upload"),
 ("M2-med","Btn Back","M1-meds"),("M2-med","Btn Open refill M3","M3-refill"),
 ("M2-med","Btn Open note R2","R2-note"),("M2-med","Btn Open reminders M4","M4-reminders"),
 ("M3-refill","Btn Send refill M3","M1-meds"),("M3-refill","Btn Back","M2-med"),
 ("M4-reminders","Btn Save reminders M4","M1-meds"),("M4-reminders","Btn Back","M1-meds"),
 ("M5-meds-empty","Btn Add med M1","R7-upload"),("M5-meds-empty","Btn Find doctor M5","B1:S1-results"),
 # ---- profile
 ("P0-profile","Btn Open details P2","P2-details"),("P0-profile","Btn Open dependants P3","P3-dependants"),
 ("P0-profile","Btn Open security P5","P5-security"),("P0-profile","Btn Open notifs P6","P6-notifs"),
 ("P0-profile","Btn Open language P7","P7-language"),("P0-profile","Btn Open access R6","R6-access"),
 ("P0-profile","Btn Open privacy P8","P8-privacy"),("P0-profile","Btn Open delete P9","P9-delete"),
 ("P0-profile","Btn Sign out","AUTH"),
 ("P2-details","Btn Back","P0-profile"),("P2-details","Btn Save details P2","P0-profile"),
 ("P2-details","Btn Open meds P2","M1-meds"),("P2-details","Btn Open vaccines","R3-lab"),
 ("P3-dependants","Btn Open add dependant P4","P3b-family"),
 ("P3b-family","Btn Back dependants P3b","P3-dependants"),
 ("P3b-family","Btn Subscribe family P3b","P4-add-dependant"),
 ("P3b-family","Btn Add one P3b","P4-add-dependant"),("P3b-family","Btn Back","P3-dependants"),("P3-dependants","Btn Back","P0-profile"),
 ("P3-dependants","Btn Book for Chidi","B1:S1-results"),("P3-dependants","Btn Book for Grace","B1:S1-results"),
 ("P3-dependants","Btn Manage Chidi","P2-details"),("P3-dependants","Btn Manage Grace","P2-details"),
 ("P4-add-dependant","Btn Save dependant P4","P3-dependants"),("P4-add-dependant","Btn Back","P3-dependants"),
 ("P5-security","Btn Back","P0-profile"),("P5-security","Btn Sign out all","AUTH"),
 ("P6-notifs","Btn Back","P0-profile"),("P6-notifs","Btn Save notifs P6","P0-profile"),
 ("P7-language","Btn Back","P0-profile"),("P7-language","Btn Save language P7","P0-profile"),
 ("P8-privacy","Btn Back","P0-profile"),("P8-privacy","Btn Open access R6","R6-access"),
 ("P8-privacy","Btn Open delete P9","P9-delete"),("P8-privacy","Btn Print summary","R10-summary"),
 ("P9-delete","Btn Back","P8-privacy"),("P9-delete","Btn Confirm delete","P9b-delete-confirm"),
 ("P9b-delete-confirm","Btn Confirm delete","AUTH"),("P9b-delete-confirm","Btn Back","P9-delete"),
 ("P9-delete","Btn Pause account","P8-privacy"),("P9-delete","Btn Open notifs P6","P6-notifs"),
 ("P9-delete","Btn Open access R6","R6-access"),
 # ---- alerts & states
 ("N0-panel","Btn Open notifs N1","N1-notifs"),("N0-panel","Btn Close notif panel","B1:H1-home"),
 ("N0-panel","Btn Mark all read","N2-notifs-empty"),("N0-panel","Btn Notif visit","V4-visit"),
 ("N0-panel","Btn Notif audit","R6-access"),("N0-panel","Btn Notif med","M1-meds"),
 ("N0-panel","Btn Notif refill","M1-meds"),("N0-panel","Btn Notif result","R3-lab"),
 ("N1-notifs","Btn Notif visit","V4-visit"),("N1-notifs","Btn Notif audit","R6-access"),
 ("N1-notifs","Btn Notif med","M1-meds"),("N1-notifs","Btn Notif refill","M1-meds"),
 ("N1-notifs","Btn Notif result","R3-lab"),("N1-notifs","Btn Notif moved","V5-reschedule"),
 ("N1-notifs","Btn Notif slot","B1:S1-results"),("N1-notifs","Btn Mark all read","N2-notifs-empty"),
 ("N1-notifs","Btn Open notifs P6","P6-notifs"),("N1-notifs","Btn Open lab R3","R3-lab"),
 ("N1-notifs","Btn Open refill M3","M3-refill"),
 ("N2-notifs-empty","Btn Open notifs P6","P6-notifs"),
 ("X2-offline","Btn Retry X2","R1-records"),
 ("X3-error","Btn Retry X3","B1:H1-home"),("X3-error","Btn Open support","X3-error"),
]

def resolve(target, side):
    if target == "AUTH": return AUTH_LOGIN[side]
    if target.startswith("B1:"): return B1_PAIRS[target[3:]][side]
    return NAMES[target][side]

resolved = []
for fid, hot, target in TRN:
    if fid not in NAMES: raise SystemExit(f"unknown source frame {fid}")
    for side in (0, 1):
        resolved.append([NAMES[fid][side], hot, resolve(target, side)])

# the nav map, applied to every frame in both batches
nav_jobs = []
for fid, pair in ALL_PAIRS.items():
    for side in (0, 1):
        for hot, target in NAV.items():
            if target[side]: nav_jobs.append([pair[side], hot, target[side]])

order_js, starts_js = {}, {}
for page, fids in ORDER.items():
    if page == "Components": continue
    order_js[PAGE_FIGMA[page]] = [[NAMES[f][0], NAMES[f][1]] for f in fids]
    starts_js[PAGE_FIGMA[page]] = NAMES[fids[0]][0]

MOTION = json.dumps({
  "default":  {"type": "SMART_ANIMATE", "easing": "GENTLE", "duration": 0.28},
  "sheet":    {"type": "MOVE_IN",  "direction": "BOTTOM", "easing": "GENTLE",  "duration": 0.32},
  "sheetOut": {"type": "MOVE_OUT", "direction": "BOTTOM", "easing": "EASE_IN", "duration": 0.24},
  "push":     {"type": "MOVE_IN",  "direction": "LEFT",   "easing": "GENTLE",  "duration": 0.26},
  "pop":      {"type": "MOVE_OUT", "direction": "RIGHT",  "easing": "EASE_IN", "duration": 0.22},
  "instant":  {"type": "SMART_ANIMATE", "easing": "LINEAR", "duration": 0.01},
})
SHEETS      = json.dumps(["Btn Share R5", "Btn Open refill M3", "Btn Cancel V1", "Btn Cancel V4",
                          "Btn Open upload R7", "Btn Add reading R4"])
SHEET_CLOSE = json.dumps(["Btn Cancel share R5", "Btn Keep visit V6", "Btn Back records R8"])
PUSH        = json.dumps(["Btn Open details P2", "Btn Open dependants P3", "Btn Open security P5",
                          "Btn Open notifs P6", "Btn Open language P7", "Btn Open privacy P8",
                          "Btn Open delete P9", "Btn Open add dependant P4", "Btn Open med M2",
                          "Btn Open med M2b", "Btn Open med M2c", "Btn Open note R2",
                          "Btn Open lab R3", "Btn Open vitals R4", "Btn Open access R6"])
POP         = json.dumps(["Btn Back"])

linker = ("(async () => {\n"
 "  // Medra Member batch 2 — wire the prototype, close the nav, arrange the canvas.\n"
 "  // Run AFTER render-member.ps1 (batch 1) so the cross-batch nav targets exist.\n"
 "  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();\n"
 "  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();\n"
 "  const pages = figma.root.children.filter(n => n.type==='PAGE');\n"
 "  const byName = {}; for (const pg of pages) for (const f of pg.children) if (f.type==='FRAME') byName[norm(f.name)] = f;\n"
 "  const F = n => byName[norm(n)];\n"
 "  const findAll = (root,t) => { const out=[]; const target=norm(t); const w=n=>{ if(n.name&&norm(n.name)===target) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 "  const allBtns = root => { const out=[]; const w=n=>{ if(n.name&&/^Btn /.test(norm(n.name))) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 f"  const M = {MOTION};\n"
 f"  const SHEETS = {SHEETS}, SHEET_CLOSE = {SHEET_CLOSE}, PUSH = {PUSH}, POP = {POP};\n"
 "  const ease = e => ({ type: e });\n"
 "  const mk = spec => spec.type==='SMART_ANIMATE'\n"
 "    ? { type:'SMART_ANIMATE', easing:ease(spec.easing), duration:spec.duration }\n"
 "    : { type:spec.type, direction:spec.direction, matchLayers:false, easing:ease(spec.easing), duration:spec.duration };\n"
 "  const specFor = hot => SHEETS.includes(hot) ? M.sheet : SHEET_CLOSE.includes(hot) ? M.sheetOut\n"
 "                       : PUSH.includes(hot) ? M.push : POP.includes(hot) ? M.pop : M.default;\n"
 f"  const TRN = {json.dumps(resolved)};\n"
 f"  const NAVJOBS = {json.dumps(nav_jobs)};\n"
 f"  const ORDER = {json.dumps(order_js)};\n"
 f"  const STARTS = {json.dumps(starts_js)};\n"
 f"  const OWN = {json.dumps([n for pair in NAMES.values() for n in pair])};\n"
 "  const wired = new Set(); const missing = []; let linked = 0;\n"
 "  const go = async (nd,to,spec) => { await nd.setReactionsAsync([{ trigger:{type:'ON_CLICK'},\n"
 "      actions:[{ type:'NODE', destinationId:to.id, navigation:'NAVIGATE', transition: mk(spec) }] }]);\n"
 "      wired.add(nd.id); linked++; };\n"
 "  // 1. explicit screen-to-screen transitions\n"
 "  for (const [fromN,hot,toN] of TRN){ const fr=F(fromN), to=F(toN);\n"
 "    if(!fr||!to){ missing.push(fromN+' -> '+hot+' -> '+toN); continue; }\n"
 "    const nodes=findAll(fr,hot); if(!nodes.length){ missing.push(fromN+' -> '+hot); continue; }\n"
 "    for (const nd of nodes) await go(nd,to,specFor(hot)); }\n"
 "  // 2. the nav map — every tab on every frame of both batches\n"
 "  let navLinked = 0;\n"
 "  for (const [fromN,hot,toN] of NAVJOBS){ const fr=F(fromN), to=F(toN); if(!fr||!to) continue;\n"
 "    for (const nd of findAll(fr,hot)){ if (wired.has(nd.id)) continue; await go(nd,to,M.default); navLinked++; } }\n"
 "  // 3. no dead hotspots: anything still named \"Btn …\" and unwired stays on its own screen\n"
 "  let stay = 0;\n"
 "  for (const fn of OWN){ const fr=F(fn); if(!fr) continue;\n"
 "    for (const nd of allBtns(fr)){ if (wired.has(nd.id)) continue;\n"
 "      if (nd.reactions && nd.reactions.length) { wired.add(nd.id); continue; }\n"
 "      await go(nd,fr,M.instant); stay++; } }\n"
 "  // 4. arrange each page: desktop row on top, matching mobile row beneath, in flow order\n"
 "  const GX=170, GY=150;\n"
 "  for (const pg of pages){ const ord=ORDER[pg.name]; if(!ord) continue; let x=0, rowH=0;\n"
 "    for (const [dn] of ord){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const [,mn] of ord){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(s&&F(s)) pg.flowStartingPoints=[{ nodeId:F(s).id, name:pg.name }]; }\n"
 "  return { linked, navLinked, stayOnScreen: stay, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT, "link-member2.js"), "w").write(linker)

# ---- interactive components script -------------------------------------------------
components = """(async () => {
  // Medra batch 2 — turn the cmp/* frames on this page into real Figma component sets
  // with variants and wired hover / press / click interactions.
  // Run:  figma-cli run .\\components-member2.js      (idempotent)
  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();
  const PAGE = 'Medra — Interactive Components · Care';
  let page = figma.root.children.find(n => n.name === PAGE);
  if (!page) return { error: `page "${PAGE}" not found — render the cmp/* frames first` };
  await figma.setCurrentPageAsync(page);

  const re = /^cmp\\/(.+?)\\/(.+?)=(.+)$/;
  const groups = {};
  for (const node of [...page.children]) {
    if (node.type !== 'FRAME') continue;
    const m = re.exec((node.name || '').trim());
    if (!m) continue;
    const [, comp, prop, value] = m;
    groups[comp] = groups[comp] || { prop, variants: {} };
    groups[comp].variants[value] = node;
  }
  if (!Object.keys(groups).length) return { error: 'no cmp/* frames found on the page' };

  // only remove the sets this script owns, so the batch-1 component page is untouched
  const OWNED = new Set(Object.keys(groups).map(c => `Medra/${c}`));
  for (const node of [...page.children]) {
    if (node.type === 'COMPONENT_SET' && OWNED.has(node.name)) node.remove();
  }

  const REST = { 'Tab':'Inactive', 'Status Pill':'Confirmed', 'Call Control':'On',
                 'List Row':'Default', 'Consent Scope':'On', 'Dose':'Due' };
  const WIRING = {
    'Tab':           [['ON_CLICK','Active']],
    'Call Control':  [['ON_CLICK','Off'], ['ON_HOVER','Idle']],
    'List Row':      [['ON_HOVER','Hover'], ['ON_PRESS','Pressed']],
    'Consent Scope': [['ON_CLICK','Off']],
    'Dose':          [['ON_CLICK','Taken']],
  };
  const BACK = {
    'Tab':           [['ON_CLICK','Inactive']],
    'Call Control':  [['ON_CLICK','On']],
    'List Row':      [['ON_HOVER','Default'], ['ON_PRESS','Default']],
    'Consent Scope': [['ON_CLICK','On']],
  };
  const smart = (d = 0.16) => ({ type:'SMART_ANIMATE', easing:{type:'GENTLE'}, duration:d });
  const changeTo = id => ({ type:'NODE', destinationId:id, navigation:'CHANGE_TO', transition:smart() });

  const report = { sets:0, variants:0, reactions:0, components:[], notes:[] };
  let cursorX = 0, cursorY = 0, rowH = 0;

  for (const [comp, { prop, variants }] of Object.entries(groups)) {
    try {
      const comps = [];
      for (const [value, frame] of Object.entries(variants)) {
        const c = figma.createComponentFromNode(frame);
        c.name = `${prop}=${value}`;
        comps.push([value, c]);
      }
      const set = figma.combineAsVariants(comps.map(([, c]) => c), page);
      set.name = `Medra/${comp}`;
      set.layoutMode = 'HORIZONTAL';
      set.itemSpacing = 24;
      set.paddingLeft = set.paddingRight = set.paddingTop = set.paddingBottom = 24;
      set.primaryAxisSizingMode = 'AUTO';
      set.counterAxisSizingMode = 'AUTO';
      set.x = cursorX; set.y = cursorY;
      cursorX += set.width + 80;
      rowH = Math.max(rowH, set.height);
      if (cursorX > 2600) { cursorX = 0; cursorY += rowH + 80; rowH = 0; }

      const byValue = Object.fromEntries(comps);
      const rest = REST[comp];
      if (rest && byValue[rest]) {
        for (const [trigger, target] of (WIRING[comp] || [])) {
          if (!byValue[target]) continue;
          const existing = byValue[rest].reactions ? [...byValue[rest].reactions] : [];
          existing.push({ trigger:{ type:trigger }, actions:[changeTo(byValue[target].id)] });
          await byValue[rest].setReactionsAsync(existing);
          report.reactions++;
        }
        for (const [value, node] of comps) {
          if (value === rest) continue;
          for (const [trigger, target] of (BACK[comp] || [])) {
            if (!byValue[target] || value === target) continue;
            const existing = node.reactions ? [...node.reactions] : [];
            existing.push({ trigger:{ type:trigger }, actions:[changeTo(byValue[target].id)] });
            await node.setReactionsAsync(existing);
            report.reactions++;
          }
        }
      }
      report.sets++; report.variants += comps.length;
      report.components.push(`Medra/${comp} (${comps.map(([v]) => v).join(', ')})`);
    } catch (e) { report.notes.push(`${comp}: ${e.message}`); }
  }
  return report;
})();
"""
open(os.path.join(OUT, "components-member2.js"), "w").write(components)

# ---- render script -----------------------------------------------------------------
ps = ["# Medra Member app, batch 2 — render + wire (Figma Desktop open + connected).",
      "# IMPORTANT: run the batch-1 script (medra-member\\render-member.ps1) in the same file first —",
      "# the nav map links these screens back to Home and Find care.",
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
ps.append("# Turn the cmp/* frames into real interactive components (variants + hover/press)")
ps.append("figma-cli run .\\components-member2.js")
ps.append("")
ps.append("# Wire the prototype with motion, close the bottom nav across both batches, arrange")
ps.append("figma-cli run .\\link-member2.js")
open(os.path.join(OUT, "render-member2.ps1"), "w").write("\n".join(ps))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} screen links "
      f"· {len(nav_jobs)} nav links · {len(CMP)} component states")
for p, fs in manifest.items(): print(f"  {p}: {len(fs)}")
