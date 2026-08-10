#!/usr/bin/env python3
"""Medra — Doctor / Medical Practitioner module (rebuild).

Covers the PRD's doctor requirements end to end (§7 Modules 2/4/6/7/8, §10.2 D1–D5, §11.3–11.4),
everything raised about the doctor in the 1 August review, and the AARRR loop a two-sided
marketplace needs on the supply side:

  Acquisition  G2 verification · R3 booking link, QR poster, patient import · G3 invite a colleague
  Activation   G1 setup checklist with a real "you cannot be booked until" gate · X2 first-week empty
  Retention    K1 queue · P4 follow-ups and recalls · P5 messages · R1 insights · R2 reviews · X3 alerts
  Referral     G3 invite a colleague · C6 refer a patient onward · R3 share your booking link
  Revenue      S2 fees · S5 earnings and payouts · S6 subscription, trial countdown, Paystack · X1 locked

45 screens × desktop 1440 + mobile 390 = 90 frames. **Mobile carries the same information as
desktop** — it is a scrolling frame, not a trimmed one.
"""
import os, re, json, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from doctor_kit import *

OUT = "/home/user/Medra-24/figma/medra-doctor"
os.makedirs(OUT, exist_ok=True)

frames = []; NAMES = {}; ORDER = {}
MOBILE_EXTRA = []          # section and sheet frames — mobile-only, still get the tab bar wired
FAMILY = {}                # fid -> every mobile frame that makes up that screen, hub first
AUTO = []                  # hub ⇄ section and hub ⇄ sheet links, generated not hand-written
ROWS = {}                  # per page: the desktop row and the mobile row, in canvas order

def nm_of(jsx): return re.search(r'name="([^"]+)"', jsx).group(1)

def add(page, fid, d, m):
    frames.append((page, f"{fid}-d.jsx", d)); frames.append((page, f"{fid}-m.jsx", m))
    NAMES[fid] = (nm_of(d), nm_of(m))
    FAMILY[fid] = [nm_of(m)]
    ORDER.setdefault(page, []).append(fid)
    r = ROWS.setdefault(page, {"d": [], "m": []})
    r["d"].append(nm_of(d)); r["m"].append(nm_of(m))

def addx(page, fid, desktop, head, pinned="", sections=(), tab=None, sheets=(),
         foot="", sec_title="More on this screen"):
    """A screen whose mobile side is a hub plus its own sections and sheets.

    sections: (key, icon, label, summary, value, tone, body, stats)
    sheets:   (key, icon, label, summary, tone, title, sub, body, actions)

    The hub row that opens a section is named `Btn Sec <fid> <key>`, the one that opens a
    sheet `Btn Sheet <fid> <key>`; both links, and the way back, are generated here so the
    transition table never has to know about them.
    """
    base = nm_of(desktop) + " · Mobile"
    rows = []
    subs = []
    for key, ic, label, summary, value, tone, body, stats in sections:
        sname = f"{base} · {label}"
        rows.append(sec_row(ic, label, summary, f"Sec {fid} {key}", value, tone))
        subs.append((f"{fid}-m-{key}.jsx",
                     mob_section(sname, label, summary, body, tab, stats=stats)))
        AUTO.append([base, f"Btn Sec {fid} {key}", sname, "push"])
        AUTO.append([sname, "Btn Back", base, "pop"])
    for key, ic, label, summary, tone, title, sub, body, actions in sheets:
        sname = f"{base} · {label} sheet"
        rows.append(sec_row(ic, label, summary, f"Sheet {fid} {key}", None, tone))
        subs.append((f"{fid}-m-{key}-sheet.jsx",
                     dr_sheet(sname, title, sub, body, actions, peek=SHEET_PEEK)))
        AUTO.append([base, f"Btn Sheet {fid} {key}", sname, "sheet"])
        AUTO.append([sname, "Btn Close sheet", base, "pop"])

    hub = mob_hub(base, head, pinned, rows, tab, foot, sec_title)
    frames.append((page, f"{fid}-d.jsx", desktop)); frames.append((page, f"{fid}-m.jsx", hub))
    NAMES[fid] = (nm_of(desktop), base)
    FAMILY[fid] = [base] + [nm_of(j) for _, j in subs]
    ORDER.setdefault(page, []).append(fid)
    r = ROWS.setdefault(page, {"d": [], "m": []})
    r["d"].append(nm_of(desktop)); r["m"].append(base)
    for fn, jsx in subs:
        frames.append((page, fn, jsx))
        MOBILE_EXTRA.append(nm_of(jsx))
        r["m"].append(nm_of(jsx))

# The strip of the hub that stays visible behind a sheet. The DSL has no opacity, so the
# dim is painted rather than composited — in build it is the hub at 55% black.
SHEET_PEEK = (f'{statusbar(dark=True)}'
              f'<Frame w="fill" flex="col" gap={{11}} px={{26}} pt={{18}}>'
              f'<Frame w="fill" h={{92}} rounded={{22}} bg="#22303E" />'
              f'<Frame w="fill" flex="row" gap={{9}}>'
              f'<Frame grow={{1}} h={{54}} rounded={{14}} bg="#22303E" />'
              f'<Frame grow={{1}} h={{54}} rounded={{14}} bg="#22303E" />'
              f'<Frame grow={{1}} h={{54}} rounded={{14}} bg="#22303E" /></Frame>'
              f'<Frame w="fill" h={{74}} rounded={{16}} bg="#22303E" /></Frame>')

PAGE_FIGMA = {
  "Start":     "Medra Doctor — 1 Getting Started",
  "Today":     "Medra Doctor — 2 Today &amp; Schedule",
  "Consult":   "Medra Doctor — 3 Consultation",
  "Patients":  "Medra Doctor — 4 Patients",
  "Practice":  "Medra Doctor — 5 Practice &amp; Money",
  "Growth":    "Medra Doctor — 6 Growth",
  "States":    "Medra Doctor — 7 States &amp; Edge Cases",
  "Components":"Medra Doctor — 8 Components",
}
NAV = {"Today": 0, "Requests": 1, "Schedule": 2, "Patients": 3, "Consults": 4,
       "Money": 5, "Growth": 6, "Settings": 7}
MTAB = {"Today": 0, "Requests": 1, "Consult": 2, "Patients": 3, "More": 4}
BADGES = {"Requests": 6, "Consults": 2}

# =====================================================================================
# CONTEXTUAL PANELS — one per section. This column is the reason the app can be dense
# without being cluttered: it always holds what that section needs next.
# =====================================================================================
UPCOMING = (upcoming_card("Amara Okeke", "Thu 10:30 – 11:00 · virtual",
                          ["avatar-2.jpg", "avatar-6.jpg"], "Q Amara", "teal")
            + upcoming_card("Chidi Okeke", "Thu 11:00 – 11:30 · in person",
                            ["avatar-6.jpg", "avatar-2.jpg"], "Q Chidi", "coral")
            + upcoming_card("Musa Ibrahim", "Thu 11:30 – 12:00 · virtual",
                            ["avatar-1.jpg"], "Q Musa", "navy"))

SIGNED_TODAY = (task_row("stethoscope", "mint", "Fatima Bello — signed", "Prescription issued · 09:28", "Open done 1")
                + task_row("stethoscope", "blue", "Emeka Nwosu — signed", "Referred to orthopaedics · 09:56", "Open done 2")
                + task_row("circle-slash", "amber", "Blessing Ade — no-show", "Marked 10:12 · slot reopened", "Open outcome K5"))

PANEL_TODAY = panel("Thursday 14 Aug",
    month_cal()
    + rail_section("Next up", UPCOMING, "View all", "Open week K6")
    + rail_section("Done today", SIGNED_TODAY, "View all", "Nav Consults"),
    foot=dbtn("I am running late", "Open late K3", "timer", "warn", full=True, size="sm")
         + dbtn("Block the next 15 min", "Open timeoff K8", "calendar-x", "ghost", full=True, size="sm"))

PANEL_REQ = panel("Inbox",
    dcard(drow("calendar-clock", "Booking requests", value="3", name="Open requests K2", tone="info", chevron=False)
          + drow("package", "Refills", value="2", name="Open refills P6", chevron=False)
          + drow("flask-conical", "Results to release", value="3", name="Open results P7", tone="warn", chevron=False)
          + drow("message-square-text", "Access replies", value="1", name="Open patients P1", chevron=False)
          + drow("message-circle", "Messages", value="4", name="Open messages P5", chevron=False), p=14, gap=2)
    + alert_strip("clock", "Reply within a day",
                  "Members are told you answer refills and requests within 24 hours. Two are close to that.", "warn"))

PANEL_SCHED = panel("Schedule",
    dcard(eyerow("This week") + kpi_line("Booked", "24") + kpi_line("Open", "9")
          + kpi_line("Cancelled", "2") + kpi_line("No-shows", "1", "warn"), p=14, gap=3)
    + dcard(eyerow("Next free slot") + T(20, "bold", "var:text/strong", "Today 15:00")
            + T(11, "regular", "var:text/muted", "Then 15:30 and 16:00", w="fill")
            + dbtn("Offer it to my waiting list", "Offer waitlist", "send", "ghost", full=True, size="sm"), p=14, gap=8),
    foot=dbtn("Edit my hours", "Open availability K7", "clock", "navy", full=True, size="sm")
         + dbtn("Block time off", "Open timeoff K8", "calendar-x", "ghost", full=True, size="sm"))

PANEL_PATIENTS = panel("Patients",
    dcard(eyerow("Lists") + drow("users", "Everyone", value="42", name="Filter all", chevron=False)
          + drow("calendar-check", "Seen this week", value="8", name="Filter week", chevron=False)
          + drow("flask-conical", "Owing a test", value="5", name="Filter owing", tone="warn", chevron=False)
          + drow("repeat", "Due a follow-up", value="7", name="Open followups P4", tone="warn", chevron=False)
          + drow("circle-slash", "Missed a visit", value="2", name="Filter noshow", chevron=False), p=14, gap=2)
    + dcard(eyerow("Recently opened") + drow("clipboard-list", "Amara Okeke", sub="Today, 09:12", name="Open Amara")
            + drow("clipboard-list", "Grace Okeke", sub="3 Aug", name="Open Grace"), p=14, gap=2))

CONSULT_WHO = (f'<Frame w="fill" flex="row" gap={{10}} items="center">'
               f'<Image image="assets/img/avatar-2.jpg" w={{36}} h={{36}} rounded={{11}} />'
               f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"semibold","var:text/strong","Amara Okeke")}'
               f'{T(10,"regular","var:text/muted","MDR-8842-19")}</Frame></Frame>')
PANEL_CONSULT = panel("Consultation",
    dcard(eyerow("With you now") + CONSULT_WHO + kpi_line("Elapsed", "12:04", "err")
          + kpi_line("Booked for", "30 min"), p=14, gap=8)
    + dcard(eyerow("Add to this visit") + drow("pill", "Prescription", name="Open prescribe C3")
            + drow("flask-conical", "Test order", name="Open tests C4")
            + drow("upload", "Result or file", name="Open upload C5")
            + drow("share-2", "Refer to a colleague", name="Open refer C6")
            + drow("calendar-plus", "Follow-up", name="Open followups P4"), p=14, gap=2),
    foot=dbtn("Finish and review", "Open sign C7", "arrow-right", "navy", full=True, size="sm"))

PANEL_MONEY = panel("Money",
    dcard(eyerow("Next payout") + T(24, "bold", "var:text/strong", "₦129,750")
          + T(11, "regular", "var:text/muted", "Friday 22 August · Zenith ****4421", w="fill"), p=14, gap=6)
    + dcard(eyerow("This month") + kpi_line("Consultations", "32") + kpi_line("Collected", "₦486,000")
            + kpi_line("Refunded", "₦15,000", "muted") + kpi_line("Net", "₦471,000", "ok"), p=14, gap=3)
    + alert_strip("sparkles", "Free trial · 12 days left",
                  "Your practice subscription starts 26 August unless you cancel.", "info"),
    foot=dbtn("Subscription and billing", "Open billing S6", "credit-card", "ghost", full=True, size="sm"))

PANEL_GROWTH = panel("Growth",
    dcard(progress_row("Profile completeness", "85%", 85, "teal")
          + T(11, "regular", "var:text/muted", "Add two more languages and a clinic photo to reach 100%.", w="fill"), p=14, gap=6)
    + dcard(eyerow("Last 30 days") + kpi_line("Profile views", "486") + kpi_line("Booked", "32", "ok")
            + kpi_line("View to booking", "6.6%") + kpi_line("Repeat patients", "61%", "ok"), p=14, gap=3),
    foot=dbtn("Share my booking link", "Open link R3", "share-2", "navy", full=True, size="sm")
         + dbtn("Invite a colleague", "Open invite G3", "user-plus", "ghost", full=True, size="sm"))

SETTINGS_NAV = [("circle-user", "Public profile", "Open profile S1"), ("banknote", "Types and fees", "Open fees S2"),
                ("video", "Virtual visits", "Open virtual S3"), ("message-circle", "How patients reach me", "Open contact S4"),
                ("wallet", "Earnings and payouts", "Open earnings S5"), ("credit-card", "Subscription and billing", "Open billing S6"),
                ("hospital", "Where I practise", "Open practice S7"), ("shield-check", "Account and security", "Open security S8")]
PANEL_SETTINGS = panel("Settings",
    dcard("".join(drow(ic, label, name=nm) for ic, label, nm in SETTINGS_NAV), p=12, gap=2),
    foot=dbtn("Sign out", "Sign out", "log-out", "ghost", full=True, size="sm"))

PANEL_START = panel("Getting started",
    dcard(progress_row("Setup", "4 of 7", 57, "teal")
          + T(11, "regular", "var:text/muted", "You cannot receive bookings until the three required steps are done.", w="fill"), p=14, gap=6)
    + dcard(eyerow("Required") + drow("badge-check", "MDCN verified", value="Pending", name="Open verify G2", tone="warn", chevron=False)
            + drow("clock", "Working hours", value="Done", name="Open availability K7", tone="ok", chevron=False)
            + drow("banknote", "Fees", value="Done", name="Open fees S2", tone="ok", chevron=False), p=14, gap=2))

PANEL_STATES = panel("Diagnostics",
    dcard(eyerow("Session") + kpi_line("Signed in", "Today 07:58") + kpi_line("Device", "Chrome · Windows")
          + kpi_line("Last sync", "2 minutes ago") + kpi_line("Build", "2026.8.14"), p=14, gap=3)
    + dcard(eyerow("If something breaks") + drow("refresh-cw", "Reload the app", name="Retry X5", chevron=False)
            + drow("message-square-text", "Message Medra support", sub="Median reply 4 minutes", name="Open help")
            + drow("phone-call", "Call the clinic line", sub="+234 809 112 4477", name="Call clinic", chevron=False), p=14, gap=2))

# =====================================================================================
# 1. GETTING STARTED — activation and acquisition
# =====================================================================================
G1_STEPS = dgroup("What is left", [
    checklist_row(True, "Register with your MDCN number", "MDCN 71482 · submitted 4 February", "Step mdcn"),
    checklist_row(True, "Set your working hours", "Mon–Thu 09:00–17:00, Wed half day, Sat virtual", "Step hours"),
    checklist_row(True, "Set your consultation types and fees", "3 types, ₦8,000 to ₦20,000", "Step fees"),
    checklist_row(True, "Add a photo and a bio", "Profiles with a photo are booked about twice as often", "Step photo"),
    checklist_row(False, "Connect your video link", "Needed before you can accept virtual bookings", "Step video"),
    checklist_row(False, "Choose how patients reach you", "WhatsApp, email or phone between visits", "Step contact"),
    checklist_row(False, "Add your payout account", "Where Medra sends what patients pay you", "Step payout"),
], footer="The first three are required to appear in search. The rest make you easier to choose.")

G1_GATE = alert_strip("triangle-alert", "You are not bookable yet",
    "MDCN verification is still running. Nothing you set up now is wasted — your profile goes live the moment a reviewer signs it off.",
    "warn", dbtn("Check status", "Open verify G2", None, "ghost", grow=False, size="sm"))

G1_VALUE = dgroup("What happens once you are live", [
    drow("search", "You appear in search", sub="Members filter by specialty, availability, price and language", name="Value search", chevron=False),
    drow("calendar-check", "Bookings arrive with the reason for the visit", sub="You know what it is about before it starts", name="Value reason", chevron=False),
    drow("clipboard-list", "You see the history the member shared", sub="Allergies and medicines always; the rest with permission", name="Value history", chevron=False),
    drow("banknote", "Payment is collected before the visit", sub="No cash conversation, no chasing", name="Value paid", chevron=False),
])

G1_STATS = rows_of([
    stat_tile("users", "1,240", "Members in Abuja", "Looking for care this month", "teal", "Stat members"),
    stat_tile("search", "38", "Cardiology searches", "Your area, last 7 days", "info", "Stat searches"),
    stat_tile("clock", "4 days", "To first booking", "Median, complete profile", "ok", "Stat first"),
], 3, 14)

addx("Start", "G1-checklist",
    dr_desk("Doctor · Start — G1 Setup Checklist", ["Getting started", "Setup"],
        f'{dhead([("Three steps from",False),("your first patient",True)],26)}'
        f'{T(14,"regular","var:text/muted","You have done four. The rest take about six minutes in total.",w="fill")}'
        f'{G1_GATE}{G1_STATS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G1_STEPS}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{G1_VALUE}'
        f'{dcta("Connect my video link","Open virtual S3","video")}</Frame></Frame>',
        NAV["Today"], PANEL_START, urgent=0),
    dr_head("Getting started", "4 of 7 done", back=False,
            stats=[("4/7", "Setup"), ("Pending", "MDCN"), ("0", "Bookings")]),
    pinned=G1_GATE,
    sections=[
      ("steps", "list-checks", "The seven steps", "Three still to do, about six minutes", "4/7", "warn",
       G1_STEPS, [("4", "Done"), ("3", "To do"), ("6 min", "Left")]),
      ("why", "trending-up", "What being live gets you", "1,240 members in Abuja this month", None, None,
       f'{G1_VALUE}{rows_of([stat_tile("users","1,240","Members in Abuja","This month","teal","Stat members"),stat_tile("search","38","Cardiology searches","Last 7 days","info","Stat searches")],2,10)}', None),
    ],
    foot=dcta("Connect my video link", "Open virtual S3", "video"),
    tab=MTAB["Today"])

G2_STEPS = dgroup("Where your application is", [
    prep_step(1, "Details received", "4 February, 09:12", done=True),
    prep_step(2, "MDCN register checked", "4 February, 11:40 — MDCN 71482 found, active, no restrictions", done=True),
    prep_step(3, "Identity confirmed", "A Medra reviewer is comparing your ID with the register. Started 3 hours ago."),
    prep_step(4, "Profile goes live", "Usually within 48 hours of step 3, often the same day"),
], footer="Every doctor is checked by a person. It is slower, and it is why a member trusts a Medra booking.")

G2_DOCS = dgroup("What we have", [
    drow("badge-check", "MDCN certificate", value="Accepted", sub="Uploaded 4 Feb · expires 31 Dec 2026", name="Doc mdcn", tone="ok"),
    drow("id-card", "Government ID", value="Under review", sub="NIN slip · uploaded 4 Feb", name="Doc id", tone="warn"),
    drow("hospital", "Proof of practice", value="Optional", sub="A letter from Garki Medical Centre would speed this up", name="Doc practice"),
    drow("upload", "Add another document", sub="Anything that helps us confirm it is you", name="Doc add", chevron=False),
])

G2_MEANWHILE = dgroup("Worth doing while you wait", [
    drow("circle-user", "Finish your public profile", value="85%", name="Open profile S1"),
    drow("video", "Connect your video link", name="Open virtual S3", tone="warn"),
    drow("message-circle", "Choose how patients reach you", name="Open contact S4"),
    drow("wallet", "Add your payout account", name="Open earnings S5"),
], footer="All of it goes live with you. Nothing needs redoing after approval.")

G2_FAQ = dgroup("Common questions", [
    drow("circle-help", "I entered the wrong MDCN number", sub="Fix it and the check restarts immediately — you keep your place", name="Faq mdcn", chevron=False),
    drow("circle-help", "How long does this usually take?", sub="Median 26 hours on a weekday, longer over a weekend", name="Faq time", chevron=False),
    drow("circle-help", "Can I see patients before approval?", sub="No. An unverified profile is invisible to members, by design", name="Faq before", chevron=False),
    drow("message-square-text", "Ask the Medra team", sub="Median reply 4 minutes", name="Open help"),
])

G2_HERO = (f'<Frame w="fill" flex="col" gap={{13}} p={{22}} rounded={{18}} image="assets/img/btn-navy.jpg" overflow="hidden">'
           f'<Frame w="fill" flex="row" justify="between" items="center">'
           f'{T(11,"semibold","var:brand/teal","VERIFICATION IN PROGRESS")}{status_pill("pending","Step 3 of 4")}</Frame>'
           f'{T(26,"bold","var:text/on-dark","We are checking your licence")}'
           f'{T(14,"regular","var:text/on-dark-muted","Started 3 hours ago. The median for a weekday application is 26 hours.",w="fill")}'
           f'{bar(65,"teal",10)}</Frame>')

addx("Start", "G2-verification",
    dr_desk("Doctor · Start — G2 Verification", ["Getting started", "Verification"],
        f'{G2_HERO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G2_STEPS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{G2_MEANWHILE}{G2_DOCS}'
        f'{alert_strip("message-square-text","Something not right?","Fix a wrong MDCN number, or ask the Medra team — median reply four minutes.","info",dbtn("Ask","Open help",None,"ghost",grow=False,size="sm"))}</Frame></Frame>',
        NAV["Today"], PANEL_START, urgent=0),
    dr_head("Verification", "Step 3 of 4 · started 3 hours ago",
            stats=[("26h", "Median"), ("3h", "Elapsed"), ("Active", "MDCN")]),
    pinned=G2_HERO,
    sections=[
      ("steps", "list-checks", "Where your application is", "Identity confirmation, in progress", "3/4", None,
       G2_STEPS, None),
      ("docs", "file-text", "What we have", "Certificate accepted, ID under review", "3", "warn",
       G2_DOCS, None),
      ("meanwhile", "clock", "Worth doing while you wait", "None of it needs redoing after approval", "4", None,
       G2_MEANWHILE, None),
      ("faq", "circle-help", "Common questions", "And how to reach the Medra team", "4", None,
       G2_FAQ, None),
    ],
    tab=MTAB["Today"])

G3_HOW = dgroup("How it works", [
    prep_step(1, "Send them your invite", "WhatsApp, SMS or a copied link"),
    prep_step(2, "They register and get verified", "Same MDCN check, usually within a day"),
    prep_step(3, "You both get a free month", "Credited after their first completed consultation"),
], footer="Indicative — the referral reward is still being confirmed with the pilot cohort.")

G3_SENT = dgroup("Invitations you have sent", [
    patient_row("avatar-1.jpg", "Dr. Chuka Eze", "MDCN 60112", "General practice · Wuse Clinic", "Joined", "Inv Chuka", tag="completed"),
    patient_row("avatar-5.jpg", "Dr. Tunde Bello", "Invited 2 Aug", "Neurology · Asokoro", "Verifying", "Inv Tunde", tag="pending"),
    patient_row("avatar-3.jpg", "Dr. Kemi Adeyemi", "Invited 28 Jul", "Paediatrics · Maitama", "No reply", "Inv Kemi", tag="missed"),
], footer="One month credited so far. The colleague is never charged for accepting.")

G3_MSG = dcard(
    eyerow("The message they get")
    + f'<Frame w="fill" flex="col" gap={{9}} p={{15}} rounded={{13}} bg="var:state/success-bg">'
    + T(13, "regular", "var:text/default",
        "“Dr. Ngozi Okafor invited you to Medra. Patients in Abuja book verified doctors on it, pay before the visit, and carry their own records between clinics. Your first month is free. — medra.ng/i/ngozi-okafor”", w="fill")
    + '</Frame>'
    + field("Add a personal line (optional)", "message-square-text", "You mentioned the no-show problem — this fixed it for me."))

addx("Start", "G3-invite",
    dr_desk("Doctor · Start — G3 Invite a Colleague", ["Growth", "Invite a colleague"],
        f'{dhead([("The doctors you trust,",False),("on the same system",True)],26)}'
        f'{T(14,"regular","var:text/muted","Referrals are how the supply side of a marketplace actually grows. Yours are tracked here.",w="fill")}'
        f'{rows_of([stat_tile("user-plus","3","Invited","Since July","teal","Stat invited"),stat_tile("badge-check","1","Joined","Dr. Chuka Eze","ok","Stat joined"),stat_tile("sparkles","1 month","Credited","Practice plan","info","Stat credited"),stat_tile("share-2","2","Patients referred to you","By Dr. Eze","ocean","Stat referred")],4,14)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G3_MSG}{G3_SENT}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{G3_HOW}'
        f'{dcta("Send on WhatsApp","Send invite whatsapp","message-circle")}'
        f'{dbtn("Copy my invite link","Copy invite link","copy","ghost",full=True)}</Frame></Frame>',
        NAV["Growth"], PANEL_GROWTH, urgent=0),
    dr_head("Invite a colleague", "3 invited · 1 joined",
            stats=[("3", "Invited"), ("1", "Joined"), ("1 mo", "Credited")]),
    pinned=G3_MSG,
    sections=[
      ("sent", "user-plus", "Invitations you have sent", "Chuka joined, Tunde verifying", "3", None,
       G3_SENT, None),
      ("how", "info", "How it works", "And what you both get", "3", None,
       G3_HOW, None),
    ],
    foot=f'{dcta("Send on WhatsApp","Send invite whatsapp","message-circle")}'
         f'{dbtn("Copy my invite link","Copy invite link","copy","ghost",full=True)}',
    tab=MTAB["More"])

# =====================================================================================
# 2. TODAY & SCHEDULE
# =====================================================================================
NOW = now_card("avatar-2.jpg", "Amara Okeke", "34 · MDR-8842-19 · 4th visit with you",
               "Hypertension follow-up. Home readings 138/88 for two weeks, afternoon headaches.", "10:30")
NOW_M = now_card("avatar-2.jpg", "Amara Okeke", "34 · MDR-8842-19 · 4th visit",
                 "Hypertension follow-up. Home readings 138/88 for two weeks.", "10:30", mobile=True)

Q_CHIDI = dict(time="11:00", avatar="avatar-6.jpg", who="Chidi Okeke",
               meta="6 years · MDR-8842-20", reason="Cough for four days, no fever",
               kind="confirmed", vtype="In person", name="Q Chidi",
               flags=[("baby", "Paediatric", "info"), ("user-check", "Guardian booking", "info")])
Q_MUSA = dict(time="11:30", avatar="avatar-1.jpg", who="Musa Ibrahim",
              meta="51 years · MDR-7714-02 · first visit", reason="Chest tightness climbing stairs",
              kind="confirmed", vtype="Virtual", name="Q Musa",
              flags=[("triangle-alert", "Possible cardiac — flagged", "err"), ("sparkles", "New patient", "info")])
Q_GRACE = dict(time="12:00", avatar="avatar-3.jpg", who="Grace Okeke",
               meta="68 years · MDR-8842-21 · diabetes, hypertension", reason="Review after blood sugar test",
               kind="confirmed", vtype="In person", name="Q Grace",
               flags=[("flask-conical", "Result ready to discuss", "warn")])
Q_TUNDE = dict(time="14:00", avatar="avatar-5.jpg", who="Tunde Bello",
               meta="44 years · MDR-6620-88", reason="Results discussion",
               kind="pending", vtype="Virtual", name="Q Tunde",
               flags=[("credit-card", "Unpaid — slot released 13:30", "warn")])

QUEUE = "".join(queue_row(**q) for q in (Q_CHIDI, Q_MUSA, Q_GRACE, Q_TUNDE))
QUEUE_M = "".join(queue_row(**q, mobile=True) for q in (Q_CHIDI, Q_MUSA, Q_GRACE, Q_TUNDE))

K1_STATS = rows_of([
    stat_tile("users", "8", "Booked today", "3 seen · 5 to go", "teal", "Stat today"),
    stat_tile("clock", "6 min", "Median wait", "You are 4 minutes early", "ok", "Stat wait"),
    stat_tile("video", "5", "Virtual", "3 in person", "info", "Stat virtual"),
    stat_tile("banknote", "₦96,000", "Collected today", "In Friday's payout", "navy", "Stat money"),
], 4, 14)

K1_DONE = dgroup("Already seen", [
    timeline_entry("09", "00", "check-check", "Fatima Bello", "Signed 09:28 · prescription issued", "Open done 1", "ok", "completed"),
    timeline_entry("09", "30", "check-check", "Emeka Nwosu", "Signed 09:56 · referred to orthopaedics", "Open done 2", "ok", "completed"),
    timeline_entry("10", "00", "circle-slash", "Blessing Ade", "Did not arrive · marked no-show 10:12", "Open outcome K5", "warn", "missed"),
], footer="Marking a no-show releases the slot and tells the member. Two no-shows in 60 days and Medra asks them to prepay.")

K1_LATER = dgroup("Rest of the day", [
    drow("coffee", "13:00 — Break", value="1 hour", sub="Blocked, nobody can book it", name="Break row", chevron=False),
    drow("video", "14:00 — Tunde Bello", value="Unpaid", sub="Slot released at 13:30 unless he pays", name="Q Tunde", tone="warn"),
    drow("circle-plus", "15:00 — Open", sub="Bookable now · offer it to your waiting list", name="Open slot 15"),
    drow("circle-plus", "15:30 — Open", sub="Bookable now", name="Open slot 1530"),
    drow("circle-plus", "16:00 — Open", sub="Last slot of the day", name="Open slot 16"),
])

# The panel carried refills and unsigned notes on Requests but not on Today, so the two
# things most likely to be forgotten had no route off the busiest screen.
K1_ALSO = dgroup("Also waiting on you", [
    drow("package", "2 refill requests", sub="Oldest 19 hours — Grace Okeke, metformin", name="Open refills P6", tone="warn"),
    drow("notebook-pen", "2 unsigned notes", sub="Chidi Okeke from yesterday · your fee is held until you sign", name="Open drafts C9", tone="err"),
    drow("flask-conical", "3 results to release", sub="One is out of range and should not go out unexplained", name="Open results P7", tone="warn"),
    drow("calendar-clock", "3 booking requests", sub="Two are close to the day you promise members", name="Open requests K2", tone="info"),
], footer="Everything here is something a patient is waiting on. It clears as you work through it.")

K1_WAITLIST = alert_strip("repeat", "Three open slots today",
    "Six people asked for a cardiology appointment this week and took a later date. Offer them today's gaps and most of them fill within the hour.",
    "info", dbtn("Offer them to my waiting list", "Offer waitlist", "send", "navy", grow=False, size="sm"))

# Desktop shows three of the four waiting and points at the day list for the rest. Four full
# queue cards plus everything else was the screen that read as overloaded.
QUEUE_TOP = "".join(queue_row(**q) for q in (Q_CHIDI, Q_MUSA)) + see_all("waiting", "Open week K6", 5)

K1_LATER_SHORT = dgroup("Rest of the day", [
    drow("video", "14:00 — Tunde Bello", value="Unpaid", sub="Slot released at 13:30", name="Q Tunde", tone="warn"),
    drow("circle-plus", "15:00 — Open", sub="Bookable now", name="Open slot 15"),
    drow("circle-plus", "15:30 · 16:00 — Open", sub="Two more, plus a 13:00 break", name="Open slot 1530"),
]) + dbtn("Offer my open slots to the waiting list", "Offer waitlist", "repeat", "ghost", full=True, size="sm")

K1_ALSO_SHORT = dgroup("Also waiting on you", [
    drow("package", "Refill requests", value="2", sub="Oldest 19 hours", name="Open refills P6", tone="warn"),
    drow("flask-conical", "Results to release", value="3", sub="One is out of range", name="Open results P7", tone="warn"),
    drow("notebook-pen", "Unsigned notes", value="2", sub="Your fee is held until you sign", name="Open drafts C9", tone="err"),
], footer=None) + see_all("six things waiting", "Open requests K2")

K1_WELCOME = welcome("Good morning,", "Dr. Okafor",
    "Eight patients today, three already seen. You are running four minutes early.",
    actions=dbtn("Start next consultation", "Start consult", "stethoscope", "navy", grow=False)
            + dbtn("Read the file first", "Open prep", "clipboard-list", "ghost", grow=False),
    stats=[("3 of 8", "Seen", "teal"), ("6 min", "Median wait", "ok"),
           ("₦96,000", "Collected", "coral"), ("16:40", "Finish by", "warn")])

K1_PROGRESS = dcard(
    eyerow("Today's patients", f'<Frame name="Btn Open week K6" flex="row">{T(11,"semibold","var:text/accent","View all")}</Frame>')
    + person_progress("avatar-2.jpg", "Amara Okeke", 96, "teal", "Q Amara")
    + person_progress("avatar-6.jpg", "Chidi Okeke", 62, "coral", "Q Chidi")
    + person_progress("avatar-1.jpg", "Musa Ibrahim", 38, "amber", "Q Musa")
    + person_progress("avatar-3.jpg", "Grace Okeke", 84, "navy", "Q Grace"),
    p=18, gap=4)

K1_DONUT = donut_card(38, "Clinic progress",
                      [("Seen", "teal"), ("Still to see", "navy")],
                      "Three of eight done. At this rate you finish at 16:40.")

K1_MEDIA = dcard(
    eyerow("Shared with your patients", f'<Frame name="Btn Nav Patients" flex="row">{T(11,"semibold","var:text/accent","View all")}</Frame>')
    + file_row("Rx", "mint", "Amara Okeke", "Amlodipine 5 mg · 30 days", "Sent to pharmacy", "ok", "1 member", "Today", "File rx")
    + hr()
    + file_row("Lab", "blue", "Grace Okeke", "HbA1c result.pdf", "Held — not released", "warn", "1 member", "Yesterday", "Open results P7")
    + hr()
    + file_row("Ref", "coral", "Amara Okeke", "Referral to Dr. Bello.pdf", "Awaiting her consent", "warn", "2 members", "Today", "File ref")
    + hr()
    + file_row("Note", "lilac", "Fatima Bello", "Consultation note.pdf", "Shared", "ok", "1 member", "09:28", "Open done 1"),
    p=18, gap=4)

K1_MEDIA_M = dcard(
    eyerow("Shared with your patients")
    + file_row("Rx", "mint", "Amara Okeke", "Amlodipine 5 mg · 30 days", "Sent to pharmacy", "ok", "1", "Today", "File rx", mobile=True)
    + hr()
    + file_row("Lab", "blue", "Grace Okeke", "HbA1c result.pdf", "Held — not released", "warn", "1", "Yesterday", "Open results P7", mobile=True)
    + hr()
    + file_row("Ref", "coral", "Amara Okeke", "Referral to Dr. Bello.pdf", "Awaiting consent", "warn", "2", "Today", "File ref", mobile=True),
    p=16, gap=4)

addx("Today", "K1-today",
    # Desktop budget: the welcome, what is happening now, and the queue. Everything the old
    # version stacked underneath — media, the rest of the day, what has been seen — is either
    # in the right rail or one row away on the screen that owns it.
    dr_desk("Doctor · Today — K1 Queue", ["Today", "Thursday 14 August"],
        f'{K1_WELCOME}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{NOW}'
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{T(16,"bold","var:text/strong","Waiting")}'
        f'<Frame flex="row" gap={{9}} items="center">'
        f'{dbtn("Requests","Open requests K2","inbox","warn",grow=False,size="sm")}'
        f'{dbtn("Whole week","Open week K6","calendar-days","ghost",grow=False,size="sm")}</Frame></Frame>'
        f'{QUEUE_TOP}</Frame>'
        f'<Frame w={{312}} flex="col" gap={{14}}>{K1_DONUT}{K1_ALSO_SHORT}{K1_LATER_SHORT}</Frame></Frame>',
        NAV["Today"], PANEL_TODAY, badges=BADGES),
    dr_head("Good morning", "Dr. Okafor · 8 today, 3 seen", back=False, illo=True,
            stats=[("3/8", "Seen"), ("6 min", "Wait"), ("₦96k", "Today")]),
    # Pinned: the patient you are about to see, and how far through the day you are. Nothing else.
    pinned=f'{NOW_M}{donut_card(38,"Clinic progress",[("Seen","teal"),("Still to see","navy")],"Three of eight done. At this rate you finish at 16:40.",size=150)}',
    sections=[
      ("waiting", "users", "Waiting", "Chidi, Musa, Grace and Tunde", "5", None,
       f'{QUEUE_M}{K1_PROGRESS}', [("5", "Waiting"), ("6 min", "Median"), ("16:40", "Finish")]),
      ("also", "inbox", "Also waiting on you", "Refills, results, unsigned notes", "6", "warn",
       K1_ALSO, [("2", "Refills"), ("3", "Results"), ("2", "Unsigned")]),
      ("rest", "clock", "The rest of today", "Three slots still open", "4", None,
       f'{K1_LATER}{K1_WAITLIST}{K1_DONE}', [("3", "Open"), ("1", "Break"), ("3", "Seen")]),
      ("files", "folder", "Shared with your patients", "Prescriptions, results, referrals", "4", None,
       K1_MEDIA_M, None),
    ],
    sheets=[
      ("quick", "zap", "Quick actions", "Running late, block time, offer a slot", None,
       "Quick actions", "Thursday 14 August · 09:12",
       f'{sheet_pick("timer","I am running late","Tell everyone waiting, in one message","Open late K3","warn")}'
       f'{sheet_pick("calendar-x","Block the next 15 minutes","Nobody can book it","Open timeoff K8")}'
       f'{sheet_pick("repeat","Offer my open slots","Six people are on the waiting list","Offer waitlist","info")}'
       f'{sheet_pick("circle-slash","Close off an appointment","Mark complete or no-show","Open outcome K5")}', None),
    ],
    tab=MTAB["Today"])

# ---------------- K2 booking requests (PRD D3: confirm / decline)
def req_actions(name):
    return [dbtn("Accept", "Accept " + name, "check", "navy", size="sm"),
            dbtn("Another time", "Suggest " + name, "calendar-clock", "ghost", size="sm"),
            dbtn("Decline", "Decline " + name, "x", "danger", size="sm")]

K2_BOOKINGS = dgroup("Booking requests · 3", [
    request_row("calendar-clock", "Musa Ibrahim · MDR-7714-02",
                "Fri 22 Aug, 09:00 · virtual · first visit · “Chest tightness when I climb stairs.” · paid ₦20,000",
                "12 min ago", "Req Musa", "info", req_actions("Musa")),
    request_row("calendar-clock", "Halima Sani · MDR-9012-44",
                "Fri 22 Aug, 11:30 · in person · “Blood pressure check, my mother has hypertension.” · paid ₦15,000",
                "1 hour ago", "Req Halima", "info", req_actions("Halima")),
    request_row("calendar-clock", "Emeka Nwosu · MDR-4410-07",
                "Sat 23 Aug, 10:00 · virtual · returning · “Follow-up on the knee.” · paid ₦15,000",
                "3 hours ago", "Req Emeka", "warn", req_actions("Emeka")),
], footer="Accepting confirms it instantly for the member. Declining refunds them in full, automatically, and we tell them why in your words.")

K2_RULES = dgroup("Save yourself this screen", [
    dtoggle("zap", "Auto-accept when the slot is open", sub="Anything inside your working hours is confirmed without asking you", on=False, name="Auto accept"),
    dtoggle("user-check", "Auto-accept returning patients only", sub="People you have seen before, in an open slot", on=True, name="Auto returning"),
    drow("clock", "Decline automatically after", value="24 hours", sub="Nobody is left waiting on you indefinitely", name="Auto decline"),
], footer="Auto-accept is off by default. Most doctors turn on the returning-patients rule within a week.")

K2_OTHER = dgroup("Also waiting", [
    drow("package", "2 refill requests", sub="Oldest 19 hours — Grace Okeke, metformin", name="Open refills P6", tone="warn"),
    drow("flask-conical", "3 results to release", sub="One is out of range and should not go out unexplained", name="Open results P7", tone="warn"),
    drow("message-square-text", "1 access reply", sub="Amara Okeke agreed to share her prescription history", name="Open patients P1", tone="ok"),
    drow("message-circle", "4 unread messages", sub="Two are about appointments today", name="Open messages P5"),
    drow("notebook-pen", "2 unsigned notes", sub="Your fee is held until you sign them", name="Open drafts C9", tone="err"),
])

addx("Today", "K2-requests",
    dr_desk("Doctor · Today — K2 Requests", ["Requests", "Booking requests"],
        f'{dhead([("6 things",False),("need you",True)],26)}'
        f'{T(14,"regular","var:text/muted","Members are told you reply within a day. Two of these are close to that.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K2_BOOKINGS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{K2_OTHER}</Frame></Frame>',
        NAV["Requests"], PANEL_REQ, urgent=6, badges=BADGES),
    dr_head("Requests", "6 need you", back=False,
            stats=[("3", "Bookings"), ("2", "Refills"), ("3", "Results")]),
    pinned=alert_strip("clock", "Two are close to a day old",
        "Members are told you answer within 24 hours. Musa asked 12 minutes ago; Emeka three hours ago.", "warn"),
    sections=[
      ("bookings", "calendar-clock", "Booking requests", "Musa, Halima and Emeka", "3", "info",
       K2_BOOKINGS, [("3", "Waiting"), ("₦50k", "Paid"), ("12m", "Newest")]),
      ("other", "inbox", "Also waiting", "Refills, results, messages, replies", "3", "warn",
       K2_OTHER, None),
      ("rules", "zap", "Save yourself this screen", "Auto-accept rules", None, None,
       K2_RULES, None),
    ],
    tab=MTAB["Requests"])

# ---------------- K3 running late
K3_PICK = dgroup("How late are you?", [
    radio_row("10 minutes", sub="Everyone after 11:00 shifts by 10 minutes", name="Late 10"),
    radio_row("20 minutes", sub="Everyone after 11:00 shifts by 20 minutes", on=True, name="Late 20"),
    radio_row("45 minutes", sub="We will suggest moving the last two patients", name="Late 45"),
    radio_row("Something else", sub="Pick a time and we work out the knock-on", name="Late custom"),
])
K3_MSG = dcard(eyerow("What they receive")
    + f'<Frame w="fill" flex="col" gap={{9}} p={{15}} rounded={{13}} bg="var:state/warning-bg">'
    + T(13, "regular", "var:text/default",
        "“Dr. Okafor is running about 20 minutes behind this morning. Your 11:00 will start closer to 11:20. Nothing to do — we will message again if it changes.”", w="fill")
    + '</Frame>'
    + field("Add a line of your own (optional)", "message-square-text", "An emergency came in first thing — thank you for your patience.")
    + dtoggle("message-circle", "Send on WhatsApp and SMS", sub="Reaches people already on their way", on=True, name="Late channels"))

K3_AFFECTED = dgroup("Who this touches", [
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "11:00 → 11:20 · in person · already left home", "Notify", "Late Chidi", tag="soon"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "11:30 → 11:50 · virtual", "Notify", "Late Musa"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "12:00 → 12:20 · in person · 68, travelling from Kubwa", "Notify", "Late Grace", tag="soon"),
], footer="Anyone who has already set out is listed first. They are the ones a message actually helps.")

addx("Today", "K3-late",
    dr_desk("Doctor · Today — K3 Running Late", ["Today", "Running late"],
        f'{dhead([("Tell them before",False),("they wait",True)],26)}'
        f'{T(14,"regular","var:text/muted","A message costs nothing and is the single biggest thing you can do for a clinic’s rating.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K3_PICK}{K3_MSG}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{K3_AFFECTED}'
        f'{dcta("Tell all three","Send late K3","send")}'
        f'{dbtn("Never mind","Back today K3","x","ghost",full=True)}</Frame></Frame>',
        NAV["Today"], PANEL_TODAY, badges=BADGES),
    dr_head("Running late", "3 patients affected", stats=[("20 min", "Behind"), ("3", "To tell"), ("11:20", "New start")]),
    pinned=K3_PICK,
    sections=[
      ("msg", "message-square-text", "What they receive", "Preview and add a line of your own", None, None,
       K3_MSG, None),
      ("who", "users", "Who this touches", "Chidi, Musa and Grace", "3", None,
       K3_AFFECTED, [("3", "Affected"), ("1", "En route"), ("20 min", "Shift")]),
    ],
    foot=f'{dcta("Tell all three","Send late K3","send")}'
         f'{dbtn("Never mind","Back today K3","x","ghost",full=True)}',
    tab=MTAB["Today"])

# ---------------- K4 the file, before you start
K4_META = (f'<Frame w="fill" flex="row" justify="between" items="center">'
           f'{status_pill("soon","Starts in 6 minutes")}'
           f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{5}} rounded={{8}} bg="var:state/info-bg">'
           f'{I("video",12,A_IC)}{T(11,"medium","var:text/default","Virtual · Google Meet")}</Frame></Frame>')
K4_WHO = (f'<Frame w="fill" flex="row" gap={{14}} items="center">'
          f'<Image image="assets/img/avatar-2.jpg" w={{62}} h={{62}} rounded={{18}} />'
          f'<Frame grow={{1}} flex="col" gap={{4}}>{T(19,"bold","var:text/strong","Amara Okeke")}'
          f'<Frame flex="row" gap={{8}} items="center">'
          f'<Frame flex="row" px={{8}} py={{3}} rounded={{6}} bg="var:bg/muted">'
          f'{T(10,"semibold","var:text/accent","MDR-8842-19")}</Frame>'
          f'{T(12,"regular","var:text/muted","34 · female · Garki, Abuja · +234 801 234 5678")}</Frame></Frame>'
          f'{dbtn("Open full record","Open record P2","clipboard-list","ghost",grow=False,size="sm")}</Frame>')
K4_VITALS = (rows_of([kv("Height", "1.68 m", "ruler"), kv("Weight", "74 kg", "weight"),
                      kv("Visits with you", "3", "history"), kv("On Medra since", "Jan 2026", "calendar-days")], 4, 12)
             + hr()
             + health_fact("Blood group", "O+", verified=False, name="Fact blood",
                           by="She entered this herself when she joined")
             + health_fact("Genotype", "AA", verified=False, name="Fact geno",
                           by="She entered this herself when she joined")
             + health_fact("Penicillin allergy", "Rash and swelling", verified=True, name="Fact allergy",
                           by="Confirmed by you, 12 June 2026"))
K4_HEAD = dcard(K4_META + K4_WHO + K4_VITALS, p=18)

K4_SAFETY = alert_strip("triangle-alert", "Allergic to penicillin",
    "Rash and swelling, recorded June 2026. Medra blocks a penicillin prescription for this patient — overriding needs a written reason and is flagged to the clinic.", "err")

K4_REASON = dgroup("Why she is coming", [
    note_section("In her words", "“Hypertension follow-up. My home readings have been around 138/88 for two weeks and I get headaches in the afternoon.”", "message-square-text"),
    note_section("She flagged something", "“There is something in my history from 2019 I have kept off my record — I would rather explain it on the call.”", "notebook-pen"),
], footer="Members choose what history to share. If something is missing, ask — and it is recorded that you asked.")

K4_SHARED = dgroup("What she has shared with you", [
    scope_line("Allergies and current medicines", True, "Always shared — clinical safety"),
    scope_line("Consultation notes", True, "All 8 visits, including two other clinics"),
    scope_line("Lab results", True, "4 results · 1 outside the normal range"),
    scope_line("Prescription history", False, "Not shared — you can ask"),
    scope_line("Home vitals", False, "Not shared — you can ask"),
], footer="Access ends when this visit is marked complete. Every record you open is logged and visible to her.")

K4_LAST = dgroup("Last time you saw her", [
    drow("stethoscope", "Hypertension review", value="12 Jun", sub="Partially controlled, no organ damage", name="Open note last"),
    drow("pill", "Amlodipine 5 mg", value="96% taken", sub="Adherence is not the problem here", name="Open adherence"),
    drow("flask-conical", "Fasting blood sugar", value="Never done", sub="You ordered it in June and it is still outstanding", name="Open tests C4", tone="warn"),
    drow("activity", "BP trend", value="142/92 → 128/82", sub="Six clinic readings since March", name="Open record P2", tone="ok"),
])

K4_PREP = dgroup("Before you start", [
    checklist_row(True, "She has paid", "₦15,000 · Paystack PSK-99417-C · 14 Aug", "Prep paid"),
    checklist_row(True, "Records shared", "Notes and labs, until the visit is marked complete", "Prep shared"),
    checklist_row(False, "Meeting link tested", "Last checked 2 days ago", "Prep link",
                  action=dbtn("Test now", "Test link S3", "refresh-cw", "ghost", grow=False, size="sm")),
])

addx("Today", "K4-file",
    dr_desk("Doctor · Today — K4 Read the File", ["Today", "Amara Okeke"],
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Today’s queue")}</Frame>'
        f'<Frame flex="row" gap={{9}} items="center">'
        f'{dbtn("Ask for more history","Open access P3","message-square-text","ghost",grow=False,size="sm")}'
        f'{dbtn("Send the meeting link","Open virtual C10","send","ghost",grow=False,size="sm")}'
        f'{dbtn("Start consultation","Start consult","stethoscope","navy",grow=False,size="sm")}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K4_HEAD}{K4_SAFETY}{K4_REASON}{K4_LAST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{K4_SHARED}{K4_PREP}'
        f'{dcta("Start consultation","Start consult","stethoscope")}</Frame></Frame>',
        NAV["Today"], PANEL_TODAY, badges=BADGES),
    dr_head("Amara Okeke", "MDR-8842-19 · starts in 6 minutes",
            stats=[("O+", "Blood"), ("AA", "Genotype"), ("3", "Visits")],
            right=f'<Frame name="Btn Open record P2" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("clipboard-list",17,W_IC)}</Frame>'),
    # The allergy is the one thing that must be read before the consultation starts. It stays.
    pinned=K4_SAFETY,
    sections=[
      ("why", "message-square-text", "Why she is coming", "In her words, and what she flagged", None, None,
       K4_REASON, None),
      ("shared", "shield-check", "What she has shared", "Notes and labs · two categories withheld", "4", None,
       K4_SHARED, None),
      ("last", "history", "Last time you saw her", "12 June · hypertension review", None, None,
       K4_LAST, [("96%", "Adherence"), ("128/82", "Last BP"), ("1", "Test due")]),
      ("prep", "list-checks", "Before you start", "Paid · records shared · link untested", None, "warn",
       K4_PREP, None),
    ],
    sheets=[
      ("reach", "send", "Reach her first", "Ask for history, or send the meeting link", None,
       "Before you start", "Amara Okeke · starts in 6 minutes",
       f'{sheet_pick("message-square-text","Ask for more history","Two categories are withheld","Open access P3")}'
       f'{sheet_pick("send","Send the meeting link","WhatsApp, SMS and in-app","Open virtual C10","info")}'
       f'{sheet_pick("clipboard-list","Open her full record","Eight visits, three with you","Open record P2")}', None),
    ],
    foot=dcta("Start consultation", "Start consult", "stethoscope"),
    tab=MTAB["Today"])

# ---------------- K5 outcome (PRD: mark complete / no-show)
K5_PICK = dgroup("How did this appointment end?", [
    outcome_choice("check-check", "Completed", "You saw them. The note goes to their record and the fee is released to you.", "Outcome complete", sel=True, tone="ok"),
    outcome_choice("circle-slash", "Did not arrive", "15 minutes past and no contact. The slot reopens and they are told.", "Outcome noshow", tone="warn"),
    outcome_choice("phone-off", "They could not connect", "Video or network failed. Not their fault — full refund, and we offer them your next slot.", "Outcome failed", tone="info"),
    outcome_choice("calendar-x", "I had to cancel", "Something came up on your side. Full refund and an apology in your words.", "Outcome cancelled", tone="err"),
])
K5_NOSHOW = dgroup("What a no-show means", [
    drow("banknote", "The fee", value="You keep ₦7,500", sub="Half, per the pilot policy — the other half is refunded", name="Noshow fee", chevron=False),
    drow("calendar-check", "The slot", value="Reopens now", sub="Anyone can book it within seconds", name="Noshow slot", chevron=False),
    drow("message-circle", "They are told", sub="With your next three open times, so rebooking is one tap", name="Noshow told", chevron=False),
    drow("triangle-alert", "Their record", value="1st in 60 days", sub="After a second, Medra asks them to prepay in full", name="Noshow record", tone="warn", chevron=False),
], footer="The 50% split is a pilot policy and is being tested with the clinics — it is configurable per clinic.")
K5_NOTE = dcard(eyerow("Anything to add? (optional)")
    + field("For your own records", "message-square-text", "Called twice, no answer. Rain in Kubwa this morning.")
    + dtoggle("bell-ring", "Offer her my next open slot", sub="Today 15:00, then Friday 09:00", on=True, name="Offer slot")
    + dtoggle("shield-check", "Do not count this against her", sub="Use when you know the reason was outside their control", on=False, name="Forgive noshow"))

addx("Today", "K5-outcome",
    dr_desk("Doctor · Today — K5 Appointment Outcome", ["Today", "Blessing Ade", "Outcome"],
        f'{dhead([("Close off",False),("this appointment",True)],26)}'
        f'{T(14,"regular","var:text/muted","10:00 · Blessing Ade · MDR-3311-90 · in person. It is 10:12 and she has not arrived.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K5_PICK}{K5_NOTE}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{K5_NOSHOW}'
        f'{dcta("Mark as did not arrive","Save outcome K5","circle-slash")}'
        f'{dbtn("Give her five more minutes","Wait more K5","clock","ghost",full=True)}</Frame></Frame>',
        NAV["Today"], PANEL_TODAY, badges=BADGES),
    dr_head("Outcome", "Blessing Ade · 10:00 · 12 min late",
            stats=[("₦7,500", "You keep"), ("1st", "No-show"), ("Now", "Slot reopens")]),
    pinned=K5_PICK,
    sections=[
      ("means", "info", "What a no-show means", "The fee, the slot, and her record", None, None,
       K5_NOSHOW, None),
      ("note", "message-square-text", "Add a note", "For your records, and what happens next", None, None,
       K5_NOTE, None),
    ],
    foot=f'{dcta("Mark as did not arrive","Save outcome K5","circle-slash")}'
         f'{dbtn("Give her five more minutes","Wait more K5","clock","ghost",full=True)}',
    tab=MTAB["Today"])

# ---------------- K6 week
WEEK = (f'<Frame w="fill" flex="row" gap={{9}} items="start">'
        + day_col("Mon", "18", [slot_chip("09:00","booked"), slot_chip("09:30","booked"), slot_chip("10:00","open"),
                                slot_chip("10:30","open"), slot_chip("11:00","booked"), slot_chip("13:00","break")])
        + day_col("Tue", "19", [slot_chip("09:00","booked"), slot_chip("09:30","open"), slot_chip("10:00","booked"),
                                slot_chip("10:30","booked"), slot_chip("11:00","hold"), slot_chip("13:00","break")])
        + day_col("Wed", "20", [slot_chip("09:00","open"), slot_chip("09:30","booked"), slot_chip("10:00","booked"),
                                slot_chip("10:30","blocked"), slot_chip("11:00","blocked"), slot_chip("13:00","blocked")])
        + day_col("Thu", "21", [slot_chip("09:00","booked"), slot_chip("09:30","booked"), slot_chip("10:00","booked"),
                                slot_chip("10:30","booked"), slot_chip("11:00","booked"), slot_chip("13:00","break")], today=True)
        + day_col("Fri", "22", [slot_chip("09:00","blocked"), slot_chip("09:30","blocked"), slot_chip("10:00","blocked"),
                                slot_chip("10:30","blocked"), slot_chip("11:00","blocked"), slot_chip("13:00","blocked")])
        + day_col("Sat", "23", [slot_chip("10:00","open"), slot_chip("10:30","open"), slot_chip("11:00","open"),
                                slot_chip("11:30","open"), slot_chip("12:00","open"), slot_chip("12:30","open")])
        + '</Frame>')
LEGEND = (f'<Frame w="fill" flex="row" gap={{16}} items="center">'
          f'<Frame flex="row" gap={{6}} items="center"><Rect w={{11}} h={{11}} rounded={{4}} image="assets/img/btn-navy.jpg" overflow="hidden" />{T(10,"regular","var:text/muted","Booked")}</Frame>'
          f'<Frame flex="row" gap={{6}} items="center"><Rect w={{11}} h={{11}} rounded={{4}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}} />{T(10,"regular","var:text/muted","Open")}</Frame>'
          f'<Frame flex="row" gap={{6}} items="center"><Rect w={{11}} h={{11}} rounded={{4}} bg="var:state/warning-bg" />{T(10,"regular","var:text/muted","Held for payment")}</Frame>'
          f'<Frame flex="row" gap={{6}} items="center"><Rect w={{11}} h={{11}} rounded={{4}} bg="var:bg/muted" />{T(10,"regular","var:text/muted","Break")}</Frame>'
          f'<Frame flex="row" gap={{6}} items="center"><Rect w={{11}} h={{11}} rounded={{4}} bg="var:neutral/100" />{T(10,"regular","var:text/muted","Away")}</Frame></Frame>')

K6_SUM = dgroup("This week", [
    drow("calendar-check", "Booked", value="24", sub="₦366,000 collected", name="W booked", chevron=False),
    drow("circle-plus", "Still open", value="9", sub="Mostly Saturday — your quietest day", name="W open", chevron=False),
    drow("circle-x", "Cancelled", value="2", sub="Both more than a day ahead, both refunded", name="W cancelled", chevron=False),
    drow("circle-slash", "No-shows", value="1", sub="Blessing Ade, Thursday", name="W noshow", tone="warn", chevron=False),
    drow("repeat", "Returning patients", value="61%", sub="Up from 54% last month", name="W repeat", tone="ok", chevron=False),
])

addx("Today", "K6-week",
    dr_desk("Doctor · Schedule — K6 Week", ["Schedule", "Week of 18 August"],
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Week of",False),("18 August",True)],26)}'
        f'<Frame flex="row" gap={{9}} items="center">'
        f'{dbtn("Block time off","Open timeoff K8","calendar-x","ghost",grow=False,size="sm")}'
        f'{dbtn("Edit my hours","Open availability K7","clock","navy",grow=False,size="sm")}</Frame></Frame>'
        f'{dcard(WEEK + LEGEND, p=18)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{12}}>{T(15,"bold","var:text/strong","Thursday 21 August")}{QUEUE_TOP}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{K6_SUM}'
        f'{alert_strip("triangle-alert","Friday is fully blocked","Four people had already booked — decide for each from Time off.","warn")}</Frame></Frame>',
        NAV["Schedule"], PANEL_SCHED, badges=BADGES),
    dr_head("Schedule", "Week of 18 August", back=False,
            stats=[("24", "Booked"), ("9", "Open"), ("1", "No-show")],
            chips=[("Day", "Filter day", False), ("Week", "Filter week", True), ("Month", "Filter month", False)]),
    pinned=f'{dcard(WEEK + LEGEND, p=13)}',
    sections=[
      ("day", "calendar-check", "Thursday 21 August", "Four patients booked", "4", None,
       f'{date_strip(3)}{QUEUE_M}', [("4", "Booked"), ("3", "Open"), ("1", "Unpaid")]),
      ("week", "chart-column", "This week in numbers", "24 booked, 9 open, 1 no-show", None, None,
       f'{K6_SUM}{alert_strip("triangle-alert","Friday is fully blocked","Four people had already booked — decide for each from Time off.","warn",dbtn("Time off","Open timeoff K8",None,"ghost",grow=False,size="sm"))}', None),
    ],
    sheets=[
      ("edit", "settings", "Change this week", "Hours, time off, or offer a slot", None,
       "Change this week", "Week of 18 August",
       f'{sheet_pick("clock","Edit my working hours","Days, slot length and booking rules","Open availability K7")}'
       f'{sheet_pick("calendar-x","Block time off","Nine slots, four already booked","Open timeoff K8","warn")}'
       f'{sheet_pick("repeat","Offer my open slots","Six people are on the waiting list","Offer waitlist","info")}', None),
    ],
    tab=MTAB["Today"])

# ---------------- K7 availability
K7_DAYS = dgroup("Your working week", [
    dtoggle("calendar-days", "Monday", sub="09:00 – 17:00 · 30-minute slots · in person and virtual", on=True, name="Day mon"),
    dtoggle("calendar-days", "Tuesday", sub="09:00 – 17:00 · 30-minute slots", on=True, name="Day tue"),
    dtoggle("calendar-days", "Wednesday", sub="09:00 – 13:00 · theatre list in the afternoon", on=True, name="Day wed"),
    dtoggle("calendar-days", "Thursday", sub="09:00 – 17:00 · 30-minute slots", on=True, name="Day thu"),
    dtoggle("calendar-days", "Friday", sub="Not working", on=False, name="Day fri"),
    dtoggle("calendar-days", "Saturday", sub="10:00 – 14:00 · virtual only", on=True, name="Day sat"),
    dtoggle("calendar-days", "Sunday", sub="Not working", on=False, name="Day sun"),
])
K7_RULES = dgroup("Booking rules", [
    drow("clock", "Default slot length", value="30 minutes", sub="Each consultation type can override this", name="Open fees S2"),
    drow("hourglass", "Gap between patients", value="0 minutes", sub="Add a buffer if you regularly run over", name="Rule buffer"),
    drow("calendar-clock", "How far ahead can people book?", value="8 weeks", name="Rule horizon"),
    drow("timer", "Latest same-day booking", value="2 hours before", name="Rule cutoff"),
    drow("users", "Maximum patients a day", value="12", sub="Medra stops offering slots once you reach it", name="Rule cap"),
    drow("credit-card", "Hold an unpaid slot for", value="30 minutes", sub="Then it is released to everyone else", name="Rule hold"),
], footer="These rules are what makes real availability true on the member side. If a slot shows on Medra, it is genuinely open.")
K7_BREAKS = dgroup("Breaks and buffers", [
    drow("coffee", "13:00 – 14:00", value="Every working day", sub="Nobody can book it", name="Break daily"),
    drow("car", "Travel buffer between sites", value="45 minutes", sub="Garki to Maitama on a Wednesday", name="Break travel"),
    drow("plus", "Add another break", name="Add break", chevron=False),
])
K7_TYPES = dgroup("Where each type can be booked", [
    dtoggle("hospital", "In person at Garki Medical Centre", sub="Mon, Tue, Thu · 09:00 – 17:00", on=True, name="Where garki"),
    dtoggle("video", "Virtual", sub="Any working day, plus Saturday morning", on=True, name="Where virtual"),
    dtoggle("home", "Home visits", sub="Within 10 km · not currently offered", on=False, name="Where home"),
])

addx("Today", "K7-availability",
    dr_desk("Doctor · Schedule — K7 Availability", ["Schedule", "Availability"],
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("When you are",False),("available",True)],26)}'
        f'{dbtn("Save changes","Save availability K7","check","navy",grow=False,size="sm")}</Frame>'
        f'{T(14,"regular","var:text/muted","Change this and the open slots on Medra change with it. Appointments already booked are never touched.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K7_DAYS}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{K7_RULES}'
        f'{alert_strip("info","4 people have booked Friday 29 August","Turning Friday off will not cancel them. Move or cancel each one yourself so they hear it from you.","info")}</Frame></Frame>',
        NAV["Schedule"], PANEL_SCHED, badges=BADGES),
    dr_head("Availability", "Mon–Thu, Sat · 30-minute slots",
            stats=[("5", "Working days"), ("30m", "Slot"), ("12", "Daily cap")],
            right=f'<Frame name="Btn Save availability K7" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("check",17,W_IC)}</Frame>'),
    sections=[
      ("days", "calendar-days", "Your working week", "Mon–Thu and Saturday morning", "5", None,
       K7_DAYS, None),
      ("rules", "sliders-horizontal", "Booking rules", "Slot length, buffer, cap, unpaid hold", "6", None,
       K7_RULES, None),
      ("breaks", "coffee", "Breaks and buffers", "Daily break and travel time", "2", None,
       K7_BREAKS, None),
      ("where", "hospital", "Where each type can be booked", "Garki, virtual, home visits", "3", None,
       K7_TYPES, None),
    ],
    foot=dcta("Save changes", "Save availability K7", "check"),
    tab=MTAB["Today"])

# ---------------- K8 time off
K8_FORM = dcard(
    field_chips("What is this?", ["Leave", "Conference", "Theatre list", "Sick", "Personal"], 0, "Timeoff type")
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("From","calendar-days","Fri, 22 August",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("To","calendar-days","Fri, 22 August",ph=False)}</Frame></Frame>'
    + checkbox("All day", "Timeoff allday")
    + field("Note for your own records (optional)", "message-square-text", "Cardiology conference in Lagos"))

K8_IMPACT = dgroup("What this affects", [
    drow("calendar-x", "9 open slots close", sub="Nobody can book Friday 22 August", name="Impact slots", chevron=False),
    drow("users", "4 patients already booked", sub="They are not cancelled — decide for each below", name="Impact booked", tone="warn", chevron=False),
    drow("banknote", "₦60,000 already collected", sub="Refunded in full the moment you cancel them", name="Impact money", chevron=False),
    drow("message-circle", "We can message them for you", sub="WhatsApp and SMS, with your next open times", name="Impact message", chevron=False),
], footer="Medra never cancels a patient on your behalf without you choosing it here.")

K8_AFFECTED = dgroup("The four already booked", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "Fri 22 Aug · 09:00 · virtual · paid", "Move", "Move Amara"),
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "Fri 22 Aug · 09:30 · in person · paid", "Move", "Move Chidi"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "Fri 22 Aug · 11:00 · virtual · first visit", "Move", "Move Musa", tag="new"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "Fri 22 Aug · 14:00 · in person · paid", "Move", "Move Grace"),
])

K8_COVER = dgroup("Or hand them to a colleague", [
    patient_row("avatar-1.jpg", "Dr. Chuka Eze", "MDCN 60112", "General practice · Wuse Clinic · free that morning", "Ask", "Cover Chuka"),
    patient_row("avatar-5.jpg", "Dr. Tunde Bello", "MDCN 55208", "Neurology · Asokoro · partially free", "Ask", "Cover Tunde"),
], footer="They see the reason for each visit and can accept or decline per patient. Your notes are not transferred — only the booking.")

addx("Today", "K8-timeoff",
    dr_desk("Doctor · Schedule — K8 Time Off", ["Schedule", "Time off"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Schedule")}</Frame>'
        f'{dhead([("Block time",False),("off",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K8_FORM}{K8_AFFECTED}{K8_COVER}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{K8_IMPACT}'
        f'{dcta("Block this time","Save timeoff K8","calendar-x")}'
        f'{dbtn("Offer everyone my next open slot","Offer slots K8","repeat","ghost",full=True)}</Frame></Frame>',
        NAV["Schedule"], PANEL_SCHED, badges=BADGES),
    dr_head("Time off", "Friday 22 August",
            stats=[("9", "Slots close"), ("4", "Booked"), ("₦60k", "To refund")]),
    pinned=K8_FORM,
    sections=[
      ("impact", "info", "What this affects", "Nine slots, four patients, ₦60,000", None, "warn",
       K8_IMPACT, None),
      ("who", "users", "The four already booked", "Amara, Chidi, Musa and Grace", "4", "warn",
       K8_AFFECTED, None),
      ("cover", "user-plus", "Hand them to a colleague", "Dr. Eze and Dr. Bello are partly free", "2", None,
       K8_COVER, None),
    ],
    foot=f'{dcta("Block this time","Save timeoff K8","calendar-x")}'
         f'{dbtn("Offer everyone my next open slot","Offer slots K8","repeat","ghost",full=True)}',
    tab=MTAB["Today"])


# ---------------- K9 more (the fifth mobile tab)
# The sidebar carries eight destinations. A phone tab bar carries five, so four of them —
# Schedule, Consults, Money, Growth — had no route on mobile at all. This screen is that
# route, and on desktop the same directory answers "where is everything?".
K9_CLINICAL = dgroup("Clinical", [
    drow("calendar-days", "Schedule", sub="Your week, availability and time off", name="Nav Schedule"),
    drow("notebook-pen", "Consultations", sub="In progress, unsigned notes and templates", name="Nav Consults", tone="warn"),
    drow("users", "Patients", sub="42 people · records, follow-ups, messages", name="Nav Patients"),
    drow("flask-conical", "Results to release", value="3", sub="One is out of range", name="Open results P7", tone="warn"),
    drow("package", "Refill requests", value="2", sub="Oldest 19 hours", name="Open refills P6", tone="warn"),
    drow("notebook-pen", "Unsigned notes", value="2", sub="Your fee is held until you sign", name="Open drafts C9", tone="err"),
])

K9_BUSINESS = dgroup("Your practice", [
    drow("banknote", "Earnings and payouts", sub="₦129,750 due Friday", name="Nav Money"),
    drow("credit-card", "Subscription and billing", sub="Free trial · 12 days left", name="Open billing S6", tone="warn"),
    drow("trending-up", "Growth and insights", sub="486 profile views · 6.6% booked", name="Nav Growth"),
    drow("star", "Ratings and reviews", value="4.9", sub="1 review waiting on a reply", name="Open reviews R2"),
    drow("share-2", "My booking link", sub="13 of 34 bookings came from it", name="Open link R3"),
    drow("user-plus", "Invite a colleague", sub="₦10,000 off each, after their first month", name="Open invite G3"),
])

K9_ACCOUNT = dgroup("Account", [
    drow("circle-user", "Public profile", value="85%", sub="What patients see before booking", name="Open profile S1"),
    drow("banknote", "Types and fees", sub="4 types · ₦8,000 to ₦45,000", name="Open fees S2"),
    drow("video", "Virtual visits", sub="Google Meet · lobby on", name="Open virtual S3"),
    drow("message-circle", "How patients reach me", sub="3 channels · 08:00–18:00", name="Open contact S4"),
    drow("hospital", "Where I practise", sub="2 locations + virtual", name="Open practice S7"),
    drow("shield-check", "Account and security", sub="3 devices · 2FA on", name="Open security S8"),
    drow("badge-check", "Verification", value="Pending", sub="MDCN 71482 · submitted 12 Aug", name="Open verify G2", tone="warn"),
    drow("bell", "Notifications", value="6", name="Notifications"),
    drow("circle-help", "Help and support", sub="WhatsApp the Medra team", name="Open help"),
])

K9_SETUP = alert_strip("sparkles", "Setup is 4 of 7 done",
    "Three steps are still open. Finish them and your profile appears in more searches.",
    "info", dbtn("Finish setup", "Open verify G2", "arrow-right", "navy", grow=False, size="sm"))

addx("Today", "K9-more",
    dr_desk("Doctor · Today — K9 Everything", ["Medra", "Everything in Medra"],
        f'{T(14,"regular","var:text/muted","Every destination in one place. On a phone this is the More tab; here it is what the search box opens.",w="fill")}'
        f'{K9_SETUP}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{K9_CLINICAL}{K9_BUSINESS}</Frame>'
        f'<Frame w={{420}} flex="col" gap={{14}}>{K9_ACCOUNT}'
        f'{dbtn("Sign out","Sign out","log-out","ghost",full=True)}</Frame></Frame>',
        NAV["Today"], PANEL_TODAY, badges=BADGES),
    dr_head("Everything", "Dr. Ngozi Okafor · Cardiology", back=False,
            stats=[("6", "Need you"), ("12d", "Trial left"), ("85%", "Profile")]),
    pinned=K9_SETUP,
    sections=[
      ("clinical", "stethoscope", "Clinical", "Schedule, consultations, patients, results", "6", None,
       K9_CLINICAL, None),
      ("business", "banknote", "Your practice", "Earnings, billing, growth, ratings", "6", None,
       K9_BUSINESS, None),
      ("account", "settings", "Account", "Profile, fees, virtual visits, security", "9", None,
       K9_ACCOUNT, None),
    ],
    foot=dbtn("Sign out", "Sign out", "log-out", "ghost", full=True),
    sec_title="Everything in Medra",
    tab=MTAB["More"])

# =====================================================================================
# 3. CONSULTATION — the spine
# =====================================================================================
C_STRIP = (f'<Frame w="fill" flex="row" gap={{13}} items="center" p={{14}} rounded={{15}} bg="var:bg/base" '
           f'stroke="var:border/subtle" strokeWidth={{1}}>'
           f'<Image image="assets/img/avatar-2.jpg" w={{44}} h={{44}} rounded={{14}} />'
           f'<Frame grow={{1}} flex="col" gap={{3}}>'
           f'<Frame flex="row" gap={{8}} items="center">{T(15,"semibold","var:text/strong","Amara Okeke")}'
           f'<Frame flex="row" px={{8}} py={{2}} rounded={{6}} bg="var:bg/muted">'
           f'{T(10,"semibold","var:text/accent","MDR-8842-19")}</Frame></Frame>'
           f'{T(11,"regular","var:text/muted","34 · O+ · AA · penicillin allergy · hypertension · 74 kg",w="fill")}</Frame>'
           f'<Frame flex="row" gap={{7}} items="center" px={{11}} py={{7}} rounded={{9}} bg="var:state/error-bg">'
           f'<Ellipse w={{7}} h={{7}} bg="#D14343" />{T(12,"semibold","var:state/error","12:04")}</Frame>'
           f'{dbtn("Open the call","Open virtual C10","video","navy",grow=False,size="sm")}'
           f'{dbtn("Autosaved","Autosave",None,"ok",grow=False,size="sm")}</Frame>')

C_STRIP_M = (f'<Frame w="fill" flex="col" gap={{10}} p={{13}} rounded={{14}} bg="var:bg/base" '
             f'stroke="var:border/subtle" strokeWidth={{1}}>'
             f'<Frame w="fill" flex="row" gap={{11}} items="center">'
             f'<Image image="assets/img/avatar-2.jpg" w={{40}} h={{40}} rounded={{12}} />'
             f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Amara Okeke")}'
             f'{T(10,"regular","var:text/muted","MDR-8842-19 · penicillin allergy",w="fill")}</Frame>'
             f'<Frame flex="row" gap={{6}} items="center" px={{10}} py={{6}} rounded={{9}} bg="var:state/error-bg">'
             f'<Ellipse w={{7}} h={{7}} bg="#D14343" />{T(11,"semibold","var:state/error","12:04")}</Frame></Frame>'
             f'<Frame w="fill" flex="row" gap={{8}}>'
             f'{dbtn("Open the call","Open virtual C10","video","navy",size="sm")}'
             f'{dbtn("Record","Open record P2","clipboard-list","ghost",size="sm")}</Frame></Frame>')

C_TABS   = tabs(["Note", "Prescription", "Tests", "Files", "Referral"], 0, "Consult tab", size=13)
C_TABS_M = tabs(["Note", "Rx", "Tests", "Files"], 0, "Consult tab", size=13)

def c_chips(active):
    """The consult tab strip, as header chips. Same hotspot names as the desktop tabs so a
    phone can move between note, prescription, tests, files and referral exactly as desktop can."""
    labels = [("Note", "Consult tab Note"), ("Rx", "Consult tab Prescription"),
              ("Tests", "Consult tab Tests"), ("Files", "Consult tab Files"),
              ("Refer", "Consult tab Referral")]
    return [(l, n, i == active) for i, (l, n) in enumerate(labels)]


# PRD §7 Module 6 names these fields exactly. Keep them.
C_NOTE = dgroup("Consultation note", [
    note_field("Presenting complaint", "message-square-text",
        "Hypertension follow-up. Home readings 138/88 for two weeks, afternoon headaches. No chest pain, no breathlessness, no ankle swelling.", "complaint", lines=2),
    note_field("Examination", "stethoscope",
        "BP 136/86 seated, repeated 134/84. Pulse 78 regular. Weight 74 kg, unchanged. Heart sounds normal, chest clear, no oedema.", "exam", lines=2),
    note_field("Diagnosis", "clipboard-check",
        "Hypertension, partially controlled. No evidence of end-organ damage. Headaches likely tension-type rather than hypertensive.", "diagnosis", lines=2),
    note_field("Treatment plan", "list-checks",
        "Continue Amlodipine 5 mg mane. Reduce added salt. 30 minutes walking, five days a week. Fasting blood sugar and HbA1c before next review.", "plan", lines=3),
    note_field("Doctor's comment for the patient", "message-circle",
        "Your readings are better than June. Keep taking the Amlodipine every morning — it works best at a steady level.", "comment", lines=2),
    note_field("Private notes", "eye-off",
        "Mother died of stroke at 61. Anxious about it — worth watching, do not raise unprompted.", "private", lines=2, template=False, private=True),
], footer="Private notes never appear on the member's phone. They stay in the clinical record for you and the clinic. The member is told a private note exists, not what it says.")

C_AI = alert_strip("sparkles", "Transcribe this consultation",
    "Phase 2 — Medra drafts the note as you talk, you edit and sign. Nothing is recorded without the member agreeing first.",
    "info", dbtn("PHASE 2", "Phase2 transcribe", None, "ghost", grow=False, size="sm"))

C_HISTORY = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("notebook-pen",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","She said something is missing from her record")}</Frame>'
    + T(12, "regular", "var:text/default",
        "“There is something in my history from 2019 I have kept off my record.” Ask about it, and record what you were told — or that you were told nothing.", w="fill")
    + note_field("What she told you", "message-circle",
        "Treated for a thyroid condition in 2019 at a private clinic in Enugu. No records available. Says it resolved; takes nothing for it now.",
        "undisclosed", lines=2, template=False)
    + checkbox("She declined to give more detail", "Declined detail", checked=False)
    + T(11, "regular", "var:text/muted",
        "Stored with the consultation, so it is always clear what you were and were not told.", w="fill"),
    bg="var:state/info-bg", stroke=None)

C_SIDE = dgroup("While you talk", [
    drow("triangle-alert", "Allergic to penicillin", sub="Rash and swelling · Jun 2026 · confirmed by you", name="Side allergy", tone="err", chevron=False),
    drow("circle-help", "Blood group O+ · genotype AA", sub="Not medically verified — she told us, nobody tested it", name="Side unverified", tone="warn", chevron=False),
    drow("pill", "On Amlodipine 5 mg", sub="96% taken on time over 30 days", name="Side meds"),
    drow("activity", "BP trend", sub="142/92 in March down to 128/82 this month", name="Side vitals", tone="ok"),
    drow("flask-conical", "Outstanding test", sub="Fasting blood sugar, ordered 12 Jun, never done", name="Open tests C4", tone="warn"),
    drow("history", "Previous notes", value="8", sub="3 with you, 5 at other clinics", name="Open record P2"),
    drow("users-round", "Family", sub="Chidi (6) and Grace (68) are also your patients", name="Side family"),
])

C_ADD = dgroup("Add to this visit", [
    drow("pill", "Prescription", value="1", name="Open prescribe C3"),
    drow("flask-conical", "Test order", value="2", name="Open tests C4"),
    drow("upload", "Result or file", name="Open upload C5"),
    drow("share-2", "Refer to a colleague", name="Open refer C6"),
    drow("calendar-plus", "Follow-up", value="3 months", name="Open followups P4"),
])

addx("Consult", "C1-room",
    # Desktop: the note is the work, so it gets the main column alone. Everything that
    # supports it — what to watch for, what she flagged, what you can attach — is in the
    # side column and the rail, not stacked under the note.
    dr_desk("Doctor · Consult — C1 In Progress", ["Consults", "Amara Okeke", "In progress"],
        f'{C_STRIP}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C_TABS}{C_NOTE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{C_SIDE}{C_HISTORY}{C_AI}'
        f'{dcta("Finish and review","Open sign C7","arrow-right")}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Consultation", "Amara Okeke · 12:04 elapsed",
            stats=[("30m", "Booked"), ("4th", "Visit"), ("Saved", "Autosave")],
            chips=c_chips(0)),
    pinned=C_STRIP_M,
    sections=[
      ("note", "notebook-pen", "The consultation note", "Six fields · autosaved 4 seconds ago", "6", None,
       f'{C_NOTE}{C_AI}', [("6", "Fields"), ("1", "Private"), ("Saved", "Autosave")]),
      ("side", "eye", "While you talk", "Allergy, adherence, BP trend, an overdue test", "6", "err",
       C_SIDE, None),
      ("flagged", "message-square-text", "She flagged something", "History from 2019 kept off her record", None, "info",
       C_HISTORY, None),
    ],
    sheets=[
      ("add", "circle-plus", "Add to this visit", "Prescription, tests, files, referral, follow-up", None,
       "Add to this visit", "Amara Okeke · 12:04 elapsed",
       f'{sheet_pick("pill","Prescription","One on this visit already","Open prescribe C3")}'
       f'{sheet_pick("flask-conical","Test order","Two selected · ₦8,500","Open tests C4")}'
       f'{sheet_pick("upload","Result or file","Photograph it or choose a file","Open upload C5")}'
       f'{sheet_pick("share-2","Refer to a colleague","Dr. Bello has a slot on Tuesday","Open refer C6")}'
       f'{sheet_pick("calendar-plus","Follow-up","Suggested: 3 months","Open followups P4")}', None),
    ],
    foot=dcta("Finish and review", "Open sign C7", "arrow-right"),
    tab=MTAB["Consult"])

# ---------------- C2 templates
C2_LIST = dgroup("Your templates", [
    drow("file-text", "Hypertension follow-up", value="42 uses", sub="Exam, diagnosis and plan pre-filled", name="Use template hyp"),
    drow("file-text", "New patient — cardiology", value="18 uses", name="Use template new"),
    drow("file-text", "Post-discharge review", value="7 uses", name="Use template discharge"),
    drow("file-text", "Paediatric fever", value="Shared", sub="From Garki Medical Centre's shared set", name="Use template fever"),
    drow("file-text", "Diabetes review", value="Shared", sub="From Garki Medical Centre's shared set", name="Use template diabetes"),
    drow("plus", "Save this note as a template", sub="Strips the patient details, keeps the structure", name="Save template", chevron=False),
], footer="Templates fill boxes. Nothing is submitted for you, and every note still needs your signature.")

C2_PREVIEW = dgroup("Hypertension follow-up", [
    note_section("Presenting complaint", "Hypertension follow-up. Home readings [__/__] for [__]. Symptoms: [headache / chest pain / breathlessness / ankle swelling / none].", "message-square-text"),
    note_section("Examination", "BP [__/__] seated, repeated [__/__]. Pulse [__] regular. Weight [__] kg. Heart sounds [__], chest [__], oedema [__].", "stethoscope"),
    note_section("Diagnosis", "Hypertension, [controlled / partially controlled / uncontrolled]. [Evidence / no evidence] of end-organ damage.", "clipboard-check"),
    note_section("Treatment plan", "Continue [__]. Salt reduction. Exercise [__]. Tests: [__]. Review in [__].", "list-checks"),
])

C2_SETTINGS = dgroup("Template settings", [
    dtoggle("zap", "Suggest a template automatically", sub="Based on the reason for the visit", on=True, name="Tpl auto"),
    dtoggle("users", "Share mine with the clinic", sub="Colleagues at Garki Medical Centre can use them", on=False, name="Tpl share"),
    drow("download", "Import a colleague's template", name="Tpl import"),
])

addx("Consult", "C2-templates",
    dr_desk("Doctor · Consult — C2 Templates", ["Consults", "Templates"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Consultation")}</Frame>'
        f'{dhead([("Type less,",False),("say more",True)],26)}'
        f'{T(14,"regular","var:text/muted","A template fills the structure so your typing goes into what is actually different about this patient.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C2_LIST}{C2_SETTINGS}</Frame>'
        f'<Frame w={{420}} flex="col" gap={{14}}>{C2_PREVIEW}'
        f'{dcta("Use this template","Use template hyp","check")}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Templates", "5 available · 42 uses this year",
            stats=[("5", "Templates"), ("42", "Uses"), ("2", "Shared")]),
    pinned=C2_LIST,
    sections=[
      ("preview", "eye", "Preview: hypertension follow-up", "What the four fields fill with", None, None,
       C2_PREVIEW, [("42", "Uses"), ("4", "Fields"), ("Yours", "Owner")]),
      ("settings", "settings", "Template settings", "Auto-suggest, clinic sharing, import", "3", None,
       C2_SETTINGS, None),
    ],
    foot=dcta("Use this template", "Use template hyp", "check"),
    tab=MTAB["Consult"])

# ---------------- C3 prescribe
C3_SEARCH = dcard(
    field("Search a medicine", "search", "amlod", ph=False, focus=True,
          helper="Nigerian essential medicines list plus the NAFDAC register — three letters is enough.")
    + f'<Frame w="fill" flex="col" gap={{8}}>'
    + drug_result("Amlodipine", "Tablet · 5 mg, 10 mg", "Calcium channel blocker", "Pick amlodipine")
    + drug_result("Amlodipine / Valsartan", "Tablet · 5/80 mg, 10/160 mg", "Combination", "Pick amlodval")
    + drug_result("Amoxicillin", "Capsule · 250 mg, 500 mg", "Penicillin class", "Pick amoxicillin", blocked=True)
    + '</Frame>')

C3_BLOCK = alert_strip("triangle-alert", "Amoxicillin is blocked for this patient",
    "Amara is allergic to penicillin — rash and swelling, June 2026. Prescribing it needs a written reason and is flagged to the clinic's medical director.",
    "err", dbtn("Override", "Override allergy", "unlock", "danger", grow=False, size="sm"))

C3_BUILDER = dgroup("Amlodipine", [
    f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Strength","pill","5 mg",ph=False,trailing=("chevron-down","Strength dropdown"))}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Form","package","Tablet",ph=False,trailing=("chevron-down","Form dropdown"))}</Frame></Frame>',
    field_chips("How often", ["Once daily", "Twice daily", "Three times", "As needed"], 0, "Rx freq"),
    field_chips("When", ["Morning", "Night", "With food", "Any time"], 0, "Rx when"),
    f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{stepper_ctl("Days",30,"Rx days")}</Frame>'
    + f'<Frame grow={{1}} flex="col">{stepper_ctl("Refills allowed",2,"Rx refills")}</Frame></Frame>',
    field("Instructions the patient will see", "message-square-text",
          "One tablet every morning with water. Do not stop without speaking to me.", ph=False),
    dtoggle("bell-ring", "Set her reminder for 08:00", sub="App, WhatsApp and SMS", on=True, name="Rx remind"),
], footer="Written in plain language on her phone, with a reminder at the time you set and a refill button when it runs low.")

C3_CURRENT = dgroup("On this prescription", [
    rx_line("Amlodipine", "5 mg", "Once daily, morning", "30 days", "rx1"),
    rx_line("Metformin", "500 mg", "Once daily, evening", "30 days", "rx2"),
], footer="Both go to her Medicines tab and to Garki pharmacy the moment you sign.")

C3_CHECKS = dgroup("Safety checks", [
    drow("shield-check", "No interactions found", sub="Checked against everything on her record", name="Chk interactions", tone="ok", chevron=False),
    drow("triangle-alert", "1 allergy blocked a suggestion", sub="Amoxicillin — penicillin class", name="Chk allergy", tone="err", chevron=False),
    drow("baby", "Not pregnant or breastfeeding", sub="Recorded 12 Jun — ask again if unsure", name="Chk pregnancy", chevron=False),
    drow("activity", "Kidney function unknown", sub="No U&E on file. Consider one before increasing the dose.", name="Chk renal", tone="warn", chevron=False),
    drow("pill", "Also taking Vitamin D 1000 IU", sub="Over the counter, not prescribed by you", name="Chk otc", chevron=False),
], footer="Automated checks assist, they do not decide. The prescription is your clinical judgement and carries your MDCN number.")

addx("Consult", "C3-prescribe",
    dr_desk("Doctor · Consult — C3 Prescribe", ["Consults", "Amara Okeke", "Prescription"],
        f'{C_STRIP}{C_TABS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C3_SEARCH}{C3_BUILDER}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{C3_BLOCK}{C3_CURRENT}'
        f'{dcta("Add to the visit","Open sign C7","check")}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Prescribe", "Amara Okeke · 2 on this prescription",
            stats=[("2", "Medicines"), ("1", "Blocked"), ("0", "Interactions")],
            chips=c_chips(1)),
    pinned=f'{C3_SEARCH}{C3_BLOCK}',
    sections=[
      ("builder", "pill", "Dose and instructions", "Amlodipine 5 mg · 30 days · 1 refill", None, None,
       C3_BUILDER, None),
      ("current", "list", "On this prescription", "Amlodipine and metformin", "2", None,
       C3_CURRENT, None),
      ("checks", "shield-check", "Safety checks", "One allergy blocked, kidney function unknown", "5", "warn",
       C3_CHECKS, None),
    ],
    foot=dcta("Add to the visit", "Open sign C7", "check"),
    tab=MTAB["Consult"])

# ---------------- C4 tests
C4_PICK = dgroup("Order a test", [
    field("Search tests", "search", "fasting blood", ph=False, focus=True),
    drow("flask-conical", "Fasting blood sugar", value="₦3,500", sub="Already outstanding from 12 June", name="Test fbs", tone="warn"),
    drow("flask-conical", "HbA1c", value="₦5,000", sub="Three-month average — better than a single reading", name="Test hba1c"),
    drow("flask-conical", "Lipid profile", value="₦7,500", sub="Total cholesterol, HDL, LDL, triglycerides", name="Test lipid"),
    drow("flask-conical", "Urea, creatinine and electrolytes", value="₦6,000", sub="Kidney function on antihypertensives", name="Test uce"),
    drow("heart-pulse", "ECG", value="₦12,000", sub="Available at Garki Medical Centre", name="Test ecg"),
    drow("scan", "Echocardiogram", value="₦45,000", sub="Referral to the imaging centre", name="Test echo"),
])
C4_WHERE = dgroup("Where should she go?", [
    radio_row("Garki Medical Centre laboratory", sub="MLSCN accredited · results usually next day · ₦8,500 total", on=True, name="Lab garki"),
    radio_row("Any Medra partner laboratory", sub="She picks what is near her — the price varies", name="Lab any"),
    radio_row("She already has a lab in mind", sub="We send her the request to take with her", name="Lab own"),
], footer="Whichever she picks, the result comes back into her record and into your Needs-you list.")
C4_NOTE = dgroup("For the laboratory", [
    field("Clinical details", "file-text", "Hypertension on amlodipine. Screening for diabetes. Fasting sample please.", ph=False),
    checkbox("Mark as urgent — same-day result", "Test urgent", checked=False),
    dtoggle("bell-ring", "Remind her if it is not done in 7 days", sub="She never did the June one", on=True, name="Test remind"),
])
C4_ORDER = dgroup("On this order", [
    drow("flask-conical", "Fasting blood sugar", value="₦3,500", name="Ord fbs", chevron=False),
    drow("flask-conical", "HbA1c", value="₦5,000", name="Ord hba1c", chevron=False),
    drow("receipt", "She pays the laboratory", value="₦8,500", sub="Medra takes nothing from test fees", name="Ord pay", chevron=False),
])

addx("Consult", "C4-tests",
    dr_desk("Doctor · Consult — C4 Order Tests", ["Consults", "Amara Okeke", "Tests"],
        f'{C_STRIP}{C_TABS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C4_PICK}{C4_NOTE}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C4_WHERE}{C4_ORDER}'
        f'{dcta("Send it to a laboratory","Open route C11","send")}'
        f'{dbtn("Add to the visit without sending","Open sign C7","check","ghost",full=True)}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Order tests", "Amara Okeke · 2 selected",
            stats=[("2", "Tests"), ("₦8,500", "She pays"), ("1", "Overdue")],
            chips=c_chips(2)),
    pinned=C4_PICK,
    sections=[
      ("order", "receipt", "On this order", "Two tests · she pays ₦8,500", "2", None,
       C4_ORDER, None),
      ("where", "hospital", "Where should she go?", "Garki laboratory, or any partner", "3", None,
       C4_WHERE, None),
      ("note", "file-text", "For the laboratory", "Clinical details, urgency, reminder", None, None,
       C4_NOTE, None),
    ],
    foot=f'{dcta("Send it to a laboratory","Open route C11","send")}'
         f'{dbtn("Add to the visit without sending","Open sign C7","check","ghost",full=True)}',
    tab=MTAB["Consult"])

# ---------------- C5 upload / release a result
C5_UPLOAD = dcard(
    upload("Open camera C5", label="Photograph or choose the result")
    + field_chips("What is it?", ["Lab result", "Imaging", "Discharge summary", "Referral letter", "Other"], 0, "Upload kind")
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Test","flask-conical","Full blood count",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Date taken","calendar-days","12 June 2026",ph=False)}</Frame></Frame>'
    + field("Which laboratory?", "hospital", "Garki Medical Centre Laboratory", ph=False))

C5_READ = dgroup("What we read from the page", [
    lab_line("Haemoglobin", "11.2 g/dL", "12.0 – 15.5", "Low"),
    lab_line("White cell count", "6.4 ×10⁹/L", "4.0 – 11.0"),
    lab_line("Platelets", "268 ×10⁹/L", "150 – 400"),
    lab_line("Haematocrit", "34%", "34 – 45"),
], footer="Check every number before you release it. You are signing for what the patient reads.")

C5_EXPLAIN = dgroup("Before it reaches her", [
    field("In plain language (optional)", "book-open",
          "Your haemoglobin is slightly low, which often means low iron. Nothing else is out of range. We will talk about it at your review.", ph=False),
    dtoggle("eye", "Release it to her now", sub="Turn this off to hold it until you have spoken", on=False, name="Release result"),
    dtoggle("bell-ring", "Tell her it has arrived", sub="App, WhatsApp and SMS", on=True, name="Notify result"),
    dtoggle("calendar-plus", "Book a follow-up to discuss it", sub="Suggests your next three open slots", on=True, name="Result followup"),
], footer="A result out of range with no explanation frightens people. One sentence from you prevents a panicked call at 22:00.")

C5_QUEUE = dgroup("Other results waiting on you", [
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "Troponin · normal · arrived 2 hours ago", "Release", "Rel Musa", tag="new"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "HbA1c 8.4% · high · arrived yesterday", "Release", "Rel Grace", tag="pending"),
], footer="Results are never released automatically. Nothing reaches a member until a doctor has looked at it.")

addx("Consult", "C5-upload",
    dr_desk("Doctor · Consult — C5 Result", ["Consults", "Result"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Consultation")}</Frame>'
        f'{dhead([("Add a result to",False),("her record",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C5_UPLOAD}{C5_READ}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>'
        f'<Frame w="fill" h={{180}} rounded={{15}} image="assets/img/thumb-lab.jpg" overflow="hidden" />'
        f'{C5_EXPLAIN}{C5_QUEUE}{dcta("Save to her record","Open sign C7","check")}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=3, badges=BADGES),
    dr_head("Add a result", "Full blood count · 12 June",
            stats=[("1", "Out of range"), ("3", "Waiting"), ("Held", "Release")]),
    pinned=C5_UPLOAD,
    sections=[
      ("read", "scan-text", "What we read off it", "Check every value before it goes out", "6", "warn",
       C5_READ, [("6", "Values"), ("1", "Out of range"), ("You", "Checks")]),
      ("explain", "message-circle", "One line for her", "Plain language, or hold until you speak", None, None,
       C5_EXPLAIN, None),
      ("queue", "flask-conical", "Other results waiting", "Grace, Musa and Amara", "3", "warn",
       C5_QUEUE, None),
    ],
    foot=dcta("Save to her record", "Open sign C7", "check"),
    tab=MTAB["Consult"])

# ---------------- C6 refer onward
C6_WHO = dgroup("Refer to", [
    patient_row("avatar-5.jpg", "Dr. Tunde Bello", "MDCN 55208", "Neurology · Asokoro Specialist · 2.1 km · next slot Tue", "Choose", "Refer Tunde", tag="confirmed"),
    patient_row("avatar-1.jpg", "Dr. Chuka Eze", "MDCN 60112", "General practice · Wuse Clinic · next slot today", "Choose", "Refer Chuka"),
    drow("search", "Someone else on Medra", sub="Search by name, specialty or MDCN number", name="Refer search"),
    drow("hospital", "A hospital or clinic", sub="For admission or a service you do not offer", name="Refer facility"),
    drow("file-text", "Write a letter instead", sub="For a doctor who is not on Medra — she carries it or you email it", name="Refer letter"),
])
C6_LETTER = dgroup("The referral", [
    field("Reason for referral", "file-text",
          "Recurrent afternoon headaches on a background of hypertension, partially controlled. Neurological examination normal. Grateful for your assessment.", ph=False),
    field_chips("Urgency", ["Routine", "Soon — 2 weeks", "Urgent — 48 hours"], 0, "Refer urgency"),
    checkbox("Share my consultation notes with them", "Refer share notes"),
    checkbox("Share her lab results", "Refer share labs"),
    checkbox("Copy the letter to the patient", "Refer copy patient"),
], footer="She is asked to approve the share before the other doctor can open anything. Her record is hers, not yours to pass on.")
C6_WHAT = dgroup("What happens", [
    prep_step(1, "She gets the referral on her phone", "With who, why, and what you want to share"),
    prep_step(2, "She approves the share", "Or declines it — the referral still stands, just without the history"),
    prep_step(3, "Dr. Bello sees it in his requests", "He accepts and offers her a time"),
    prep_step(4, "You get the reply", "His note lands back in your inbox when the visit is done"),
], footer="Referrals that come back are the loop that keeps a specialist network honest. You always find out what happened.")

addx("Consult", "C6-refer",
    dr_desk("Doctor · Consult — C6 Refer", ["Consults", "Amara Okeke", "Referral"],
        f'{C_STRIP}{C_TABS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C6_WHO}{C6_LETTER}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C6_WHAT}'
        f'{dcta("Send the referral","Send refer C6","send")}'
        f'{dbtn("Save it with the note instead","Save refer C6","file-text","ghost",full=True)}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Refer", "Amara Okeke · neurology",
            stats=[("Routine", "Urgency"), ("2", "Suggested"), ("Tue", "Next slot")],
            chips=c_chips(4)),
    pinned=C6_WHO,
    sections=[
      ("letter", "file-text", "The referral letter", "Reason, urgency and what you have done", None, None,
       C6_LETTER, None),
      ("what", "shield-check", "What he sees", "And how his reply comes back to you", None, None,
       C6_WHAT, None),
    ],
    foot=f'{dcta("Send the referral","Send refer C6","send")}'
         f'{dbtn("Save it with the note instead","Save refer C6","file-text","ghost",full=True)}',
    tab=MTAB["Consult"])

# ---------------- C7 review & sign
C7_SHARE = dgroup("What Amara sees", [
    share_toggle("Presenting complaint, in her words", "Share complaint"),
    share_toggle("Examination findings", "Share exam"),
    share_toggle("Diagnosis", "Share diagnosis"),
    share_toggle("Treatment plan and advice", "Share plan"),
    share_toggle("Your comment for her", "Share comment"),
    share_toggle("Prescription", "Share rx"),
    share_toggle("Tests ordered", "Share tests"),
    share_toggle("Referral to Dr. Bello", "Share referral"),
    share_toggle("Private notes", "Share private", on=False, sub="Always off by default — she is told a private note exists, not what it says"),
], footer="Anything switched off stays in the clinical record for you and the clinic, and never appears on her phone.")

C7_PREVIEW = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'<Frame flex="row" gap={{7}} items="center" px={{9}} py={{5}} rounded={{8}} bg="var:state/info-bg">'
    f'{I("stethoscope",12,A_IC)}{T(10,"semibold","var:text/default","Consultation")}</Frame>'
    f'{T(10,"regular","var:text/muted","How it looks on her phone")}</Frame>'
    + T(17, "bold", "var:text/strong", "Hypertension review")
    + note_section("Diagnosis", "Hypertension, partially controlled. No sign of organ damage.", "clipboard-check")
    + note_section("Treatment plan", "Continue Amlodipine 5 mg every morning. Less added salt. Walk 30 minutes, five days a week. Fasting blood sugar before your next visit. Review in three months.", "list-checks")
    + note_section("From Dr. Okafor", "Your readings are better than June. Keep taking the Amlodipine every morning — it works best at a steady level.", "message-circle")
    + hr() + provenance("Dr. Ngozi Okafor", "MDCN 71482", "21 Aug 2026, 11:04"))

C7_ALSO = dgroup("Also going to her", [
    drow("pill", "Amlodipine 5 mg · 30 days", sub="With reminders at 08:00 and a refill button", name="Sign rx", chevron=False),
    drow("flask-conical", "Fasting blood sugar, HbA1c", sub="Garki Medical Centre laboratory · ₦8,500", name="Sign tests", chevron=False),
    drow("share-2", "Referral to Dr. Tunde Bello", sub="Neurology · routine · awaiting her approval to share", name="Sign referral", chevron=False),
    drow("calendar-plus", "Follow-up in 3 months", sub="She gets a reminder in November", name="Sign followup", chevron=False),
])

C7_SIGN = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",17,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Signing makes this permanent")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Once signed, this note cannot be edited — only amended with a new, dated entry. That is what makes it worth anything to the next doctor who reads it.", w="fill")
    + checkbox("I confirm this is an accurate record of the consultation.", "Confirm accurate")
    + dcta("Sign and send to Amara", "Sign C7", "badge-check")
    + dbtn("Save as a draft", "Save draft C7", "file-text", "ghost", full=True)
    + T(11, "regular", "var:text/muted", "Drafts are kept for 30 days and shown in Unsigned notes. The patient sees nothing until you sign.", w="fill"),
    bg="var:state/info-bg", stroke=None)

addx("Consult", "C7-sign",
    dr_desk("Doctor · Consult — C7 Review &amp; Sign", ["Consults", "Amara Okeke", "Review"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Back to the note")}</Frame>'
        f'{C_STRIP}'
        f'{dhead([("Check it, then",False),("sign it",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C7_SHARE}{C7_ALSO}</Frame>'
        f'<Frame w={{420}} flex="col" gap={{14}}>{eyerow("Preview")}{C7_PREVIEW}{C7_SIGN}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Review and sign", "Amara Okeke · 14 minutes",
            stats=[("8", "Shared"), ("1", "Private"), ("4", "Attached")]),
    sections=[
      ("share", "eye", "What Amara sees", "Eight sections shared, private notes withheld", "9", None,
       C7_SHARE, [("8", "Shared"), ("1", "Withheld"), ("Her", "Phone")]),
      ("also", "paperclip", "Also going to her", "Prescription, tests, referral, follow-up", "4", None,
       C7_ALSO, None),
      ("preview", "smartphone", "Preview on her phone", "Exactly what she will read", None, None,
       f'{eyerow("Preview")}{C7_PREVIEW}', None),
    ],
    foot=C7_SIGN,
    tab=MTAB["Consult"])

# ---------------- C8 signed
C8_DONE = dcard(
    f'<Frame w="fill" flex="col" gap={{13}} items="center">'
    f'{big_icon("badge-check","ok",84)}'
    f'{T(22,"bold","var:text/strong","Signed and sent")}'
    f'{T(14,"regular","var:text/muted","Amara has the note, the prescription and the test request on her phone. The consultation took 14 minutes.",w="fill",align="center")}</Frame>')
C8_WENT = dgroup("Where everything went", [
    drow("file-text", "Consultation note", value="Shared", sub="Private notes withheld, as you set", name="Done note", tone="ok", chevron=False),
    drow("pill", "Amlodipine 5 mg", value="Sent", sub="Garki pharmacy notified · reminder set for 08:00", name="Done rx", tone="ok", chevron=False),
    drow("flask-conical", "2 tests ordered", value="Sent", sub="Results return to your Needs-you list", name="Done tests", tone="ok", chevron=False),
    drow("share-2", "Referral to Dr. Bello", value="Awaiting her approval", sub="She decides what history he sees", name="Done referral", tone="warn", chevron=False),
    drow("banknote", "₦15,000", value="Released", sub="In Friday's payout", name="Done paid", tone="ok", chevron=False),
])
C8_NEXT = dgroup("Next patient", [
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "11:00 · in person · cough for four days", "Ready", "Q Chidi", tag="soon"),
], footer="You are running four minutes early.")
C8_RATE = dgroup("Two seconds of feedback", [
    drow("thumbs-up", "The note template saved me time", name="Fb good", chevron=False),
    drow("circle-help", "Something slowed me down", sub="Tell us what — this is how the tool gets better", name="Fb bad", chevron=False),
])

add("Consult", "C8-signed",
    dr_desk("Doctor · Consult — C8 Signed", ["Consults", "Signed"],
        f'<Frame w="fill" flex="row" gap={{16}} justify="center" items="start" pt={{8}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C8_DONE}{C8_WENT}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{C8_NEXT}'
        f'{dcta("Start the next consultation","Start consult","stethoscope")}'
        f'{dbtn("Back to today","Nav Today","arrow-left","ghost",full=True)}{C8_RATE}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_mob("Doctor · Consult — C8 Signed · Mobile",
        dr_head("Signed", "Amara Okeke · 14 minutes", back=False,
                stats=[("14m", "Length"), ("₦15k", "Released"), ("4", "Sent")]),
        f'{C8_DONE}{C8_WENT}{C8_NEXT}'
        f'{dcta("Start the next consultation","Start consult","stethoscope")}'
        f'{dbtn("Back to today","Nav Today","arrow-left","ghost",full=True)}',
        MTAB["Consult"]))

# ---------------- C9 drafts and unsigned
C9_LIST = dgroup("Unsigned notes · 2", [
    request_row("notebook-pen", "Chidi Okeke · MDR-8842-20",
                "Yesterday 16:40 · paediatric review · complaint and examination written, no diagnosis yet",
                "18 hours", "Draft Chidi", "err",
                [dbtn("Finish it", "Open room C1", "arrow-right", "navy", size="sm"),
                 dbtn("Discard", "Discard draft", "trash-2", "danger", size="sm")]),
    request_row("notebook-pen", "Fatima Bello · MDR-2201-13",
                "12 Aug · follow-up · complete but unsigned",
                "2 days", "Draft Fatima", "warn",
                [dbtn("Review and sign", "Open sign C7", "badge-check", "navy", size="sm"),
                 dbtn("Discard", "Discard draft", "trash-2", "danger", size="sm")]),
], footer="A patient cannot see anything until you sign. An unsigned note two days after a visit is the most common complaint a clinic gets.")
C9_WHY = dgroup("Why this matters", [
    drow("eye-off", "The patient sees nothing", sub="No diagnosis, no prescription, no test request", name="Why nothing", chevron=False),
    drow("pill", "The pharmacy has nothing", sub="Chidi's mother cannot collect anything", name="Why pharmacy", tone="warn", chevron=False),
    drow("banknote", "Your fee is not released", sub="Payment clears to you on signature", name="Why fee", tone="warn", chevron=False),
    drow("clock", "Drafts expire after 30 days", sub="Then it is gone and the visit has no record", name="Why expire", tone="err", chevron=False),
])
C9_RECOVERED = alert_strip("refresh-cw", "We recovered a note you did not save",
    "Chidi Okeke, yesterday 16:40 — your browser closed mid-consultation. Everything you had typed is here.", "info",
    dbtn("Open it", "Open room C1", None, "ghost", grow=False, size="sm"))

addx("Consult", "C9-drafts",
    dr_desk("Doctor · Consult — C9 Unsigned Notes", ["Consults", "Unsigned"],
        f'{dhead([("Two notes",False),("are not signed",True)],26)}'
        f'{T(14,"regular","var:text/muted","Until you sign, the visit effectively did not happen — for the patient, the pharmacy or your payout.",w="fill")}'
        f'{C9_RECOVERED}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C9_LIST}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C9_WHY}'
        f'{dgroup("Stop this happening", [dtoggle("bell-ring","Remind me at the end of clinic",sub="17:00 on a working day",on=True,name="Draft remind"),dtoggle("message-circle","And on WhatsApp if still unsigned next morning",on=True,name="Draft remind wa"),dtoggle("zap","Auto-sign a note I have not touched in 48 hours",sub="Off — a signature should be a decision",on=False,name="Draft autosign")])}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=2, badges=BADGES),
    dr_head("Unsigned notes", "2 waiting on you", back=False,
            stats=[("2", "Unsigned"), ("18h", "Oldest"), ("30d", "Expiry")]),
    pinned=f'{C9_RECOVERED}{C9_LIST}',
    sections=[
      ("why", "info", "Why this matters", "The patient, the pharmacy and your payout", "4", "warn",
       C9_WHY, None),
      ("stop", "bell-ring", "Stop this happening", "Reminders at the end of clinic", "3", None,
       dgroup("Stop this happening", [dtoggle("bell-ring","Remind me at the end of clinic",sub="17:00 on a working day",on=True,name="Draft remind"),dtoggle("message-circle","And on WhatsApp if still unsigned next morning",on=True,name="Draft remind wa"),dtoggle("zap","Auto-sign a note I have not touched in 48 hours",sub="Off — a signature should be a decision",on=False,name="Draft autosign")]), None),
    ],
    tab=MTAB["Consult"])

# ---------------- C10 virtual visit (PRD D5: doctor sends the room link)
C10_LINK = dcard(
    f'<Frame w="fill" flex="row" gap={{12}} items="center">'
    f'<Frame w={{42}} h={{42}} rounded={{13}} bg="var:state/info-bg" flex="col" justify="center" items="center">'
    f'{I("video",20,A_IC)}</Frame>'
    f'<Frame grow={{1}} flex="col" gap={{2}}>{T(14,"semibold","var:text/strong","Google Meet")}'
    f'{T(11,"regular","var:text/muted","A fresh link for this appointment only",w="fill")}</Frame>'
    f'{status_pill("ok" if False else "confirmed","Tested 2 min ago")}</Frame>'
    + f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{13}} py={{11}} rounded={{11}} bg="var:neutral/50">'
    + I("external-link", 14, M_IC) + T(12, "regular", "var:text/default", "meet.google.com/kfa-jrqz-nmo", w="fill")
    + f'<Frame name="Btn Copy meet link" flex="row">{I("copy",14,N_IC)}</Frame></Frame>'
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Join the call", "Join call C10", "video", "navy")
    + dbtn("Send it to her again", "Send link C10", "send", "ghost") + '</Frame>')

C10_SENT = dgroup("How she got the link", [
    drow("message-circle", "WhatsApp", value="Delivered 09:30", sub="Read 09:31", name="Sent wa", tone="ok", chevron=False),
    drow("message-square-text", "SMS", value="Delivered 09:30", sub="The backstop when data is down", name="Sent sms", tone="ok", chevron=False),
    drow("bell-ring", "In-app notification", value="Opened 10:18", sub="She is in the waiting room now", name="Sent app", tone="ok", chevron=False),
    drow("send", "Send it once more", sub="If she says she cannot find it", name="Send link C10"),
], footer="PRD D5 at MVP: you send the room link, Medra makes sure it actually reached her by three routes.")

C10_TROUBLE = dgroup("If the video will not work", [
    drow("phone-call", "Call her instead", value="+234 801 234 5678", sub="The consultation still counts and is still paid", name="Call patient"),
    drow("volume-2", "Switch to audio only", sub="Works on a much weaker connection", name="Audio only"),
    drow("calendar-clock", "Move the appointment", sub="Free for her, no penalty, your next slot is 15:00", name="Open week K6"),
    drow("banknote", "Refund and reschedule", sub="If nothing works, she should not pay for it", name="Refund visit", tone="warn"),
], footer="A failed video call is not the member's fault. The default is a full refund and your next open slot.")

C10_WAITING = dgroup("Waiting room", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "Joined 10:18 · camera on · good connection", "Now", "Admit Amara", tag="live"),
], footer="She can see a holding screen with your name and the wait time, not the previous consultation.")

addx("Consult", "C10-virtual",
    dr_desk("Doctor · Consult — C10 Virtual Visit", ["Consults", "Virtual visit"],
        f'{C_STRIP}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>'
        f'<Frame w="fill" h={{300}} rounded={{16}} image="assets/img/call-doctor-d.jpg" overflow="hidden" '
        f'flex="col" justify="end" p={{16}}>'
        f'<Frame flex="row" gap={{8}} items="center" px={{11}} py={{7}} rounded={{9}} bg="var:bg/band-2">'
        f'{I("video",13,T_IC)}{T(12,"medium","var:text/on-dark","Your camera preview")}</Frame></Frame>'
        f'{C10_LINK}{C10_WAITING}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C10_SENT}{C10_TROUBLE}'
        f'{dcta("Admit her and start","Start consult","stethoscope")}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Virtual visit", "Amara Okeke · waiting since 10:18",
            stats=[("10:18", "Joined"), ("Good", "Signal"), ("3", "Sent by")]),
    pinned=f'{C10_WAITING}{C10_LINK}',
    sections=[
      ("sent", "send", "How the link reached her", "WhatsApp, SMS and in-app", "3", "ok",
       C10_SENT, None),
      ("trouble", "circle-help", "If the video will not work", "Four fallbacks, none of them her fault", "4", None,
       C10_TROUBLE, None),
    ],
    foot=dcta("Admit her and start", "Start consult", "stethoscope"),
    tab=MTAB["Consult"])

# =====================================================================================
# 3b. WHERE AN ORDER GOES, AND WHO IS ALLOWED TO SEE IT
# C4 lets a doctor write an order. These five screens are what happens to it next: it is
# routed to a department inside an organisation, to a partner on Medra, or — because most
# Nigerian laboratories are not on Medra and will not sign up to run one test — to a
# stranger through a link that carries the minimum, needs the member's consent, and dies
# when the job is done.
# =====================================================================================

# ---------------- C11 route the order
C11_WHERE = dgroup("Send this order to", [
    dept_choice("hospital", "Garki Medical Centre — Laboratory", "Your own facility · in-house · results return structured · usually same day",
                "Route dept", sel=True, tone="ok",
                meta="Open now · 3 samples in the queue · median 4 hours"),
    dept_choice("hospital", "Garki Medical Centre — Imaging", "Your own facility · X-ray and ultrasound only · no MRI",
                "Route imaging", tone="info", meta="Open now · MRI would have to go outside"),
    dept_choice("building-2", "Ketu Medical Laboratory", "On Medra · partner · results return structured · 2.1 km",
                "Route partner", tone="info", meta="Accepts online orders · she pays them directly"),
    dept_choice("link", "Somewhere not on Medra", "A laboratory you trust that has no Medra account — send a single-use link",
                "Route external", tone="warn",
                meta="They upload the result; the link dies when they do"),
    dept_choice("printer", "Print it and give it to her", "The paper route. Nothing comes back to you automatically",
                "Route paper", tone="muted", meta="Use this only if the others are impossible"),
])

C11_ORDER = dgroup("What you are sending", [
    drow("flask-conical", "Fasting blood sugar", sub="Routine · fasting required · ₦3,500", name="Ord fbs", chevron=False),
    drow("flask-conical", "HbA1c", sub="Routine · no fasting needed · ₦5,000", name="Ord hba1c", chevron=False),
    drow("user", "Amara Okeke · MDR-8842-19", sub="34 · hypertension · penicillin allergy", name="Ord who", chevron=False),
    drow("banknote", "₦8,500", sub="She pays the laboratory, not you. Medra takes nothing from this.", name="Ord fee", chevron=False),
])

C11_CARRY = dgroup("What the laboratory will see", [
    scope_line("Her name, age and Medra ID", True, "They need to label the sample and match the result back"),
    scope_line("The tests you ordered, and why", True, "“Hypertension review, screening for diabetes” — clinical detail changes how a lab reports"),
    scope_line("Penicillin allergy", True, "Always travels. It is the line that prevents harm"),
    scope_line("Her consultation notes", False, "Not needed to run a blood test"),
    scope_line("Her other conditions and medicines", False, "Not needed to run a blood test"),
    scope_line("Her phone number", False, "The lab reaches her through Medra, so a stranger never gets it"),
], footer="A department sees what the job needs and nothing else. That is not a setting you have to remember — it is how the order is built.")

C11_NOTE = dgroup("Anything the laboratory should know", [
    note_field("For the laboratory", "file-text",
        "Fasting sample please — she has been told to come before breakfast. Known hypertensive on Amlodipine. Flag the HbA1c urgently if it is above 8.",
        "lab note", lines=3, template=False),
    field_chips("How soon?", ["Routine — 48 hours", "Soon — same day", "Urgent — 2 hours"], 0, "Ord urgency"),
    checkbox("Tell me the moment the result is verified", "Ord notify"),
], footer="Urgency costs the laboratory something. Mark it urgent when it is, and they will believe you when it matters.")

addx("Consult", "C11-route",
    dr_desk("Doctor · Consult — C11 Send the Order", ["Consults", "Amara Okeke", "Tests"],
        f'{C_STRIP}{C_TABS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C11_WHERE}{C11_NOTE}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C11_ORDER}{C11_CARRY}'
        f'{dcta("Send to the laboratory","Send order C11","send")}'
        f'{dbtn("Back to the tests","Open tests C4","arrow-left","ghost",full=True)}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Send the order", "Amara Okeke · 2 tests · ₦8,500",
            stats=[("2", "Tests"), ("4h", "Median"), ("3", "In queue")],
            chips=c_chips(2)),
    pinned=C11_WHERE,
    sections=[
      ("order", "receipt", "What you are sending", "Two tests · she pays ₦8,500", "2", None,
       C11_ORDER, None),
      ("carry", "shield-check", "What the laboratory will see", "Three things travel, three do not", "3", None,
       C11_CARRY, [("3", "Sent"), ("3", "Withheld"), ("0", "Notes")]),
      ("note", "file-text", "Anything they should know", "Clinical detail and urgency", None, None,
       C11_NOTE, None),
    ],
    foot=f'{dcta("Send to the laboratory","Send order C11","send")}'
         f'{dbtn("Back to the tests","Open tests C4","arrow-left","ghost",full=True)}',
    tab=MTAB["Consult"])

# ---------------- C12 the order, once it has left you
C12_TRACK = dgroup("Fasting blood sugar · HbA1c", [
    track_step("Sent to Garki laboratory", "Today 11:06", done=True,
               sub="Received by Ifeoma Nwachukwu, laboratory scientist"),
    track_step("She arrives and gives the sample", "Expected tomorrow, before 09:00", done=True,
               sub="Sample GK-2291 · fasting confirmed at reception"),
    track_step("Analysis", "In progress · started 08:41", current=True,
               sub="Both tests on the same sample"),
    track_step("A scientist verifies it", "Not yet", sub="No result leaves a laboratory unverified"),
    track_step("It comes back to you", "Not yet", sub="You release it to her, or hold it until you have spoken"),
], footer="You do not have to chase this. If it stops moving for longer than the laboratory promised, it appears in your Needs-you list on its own.")

C12_STUCK = dgroup("If it stalls", [
    drow("phone-call", "Call the laboratory", sub="Garki Medical Centre laboratory · extension 214", name="Ord call", tone="info"),
    drow("message-square-text", "Message the department", sub="Goes to whoever is on shift, not to one person", name="Ord message"),
    drow("repeat", "Send it somewhere else", sub="Cancels this order and takes you back to routing", name="Open route C11", tone="warn"),
    drow("x", "Cancel the order", sub="She is told, and is not charged", name="Ord cancel", tone="err"),
], footer="An order that has been sitting for two days is the single most common reason a member loses faith in a clinic. Chase it before they have to.")

C12_HER = dgroup("What Amara sees right now", [
    drow("smartphone", "“Your tests are being analysed”", sub="With where to go, what it costs, and whether to fast", name="Ord hers", chevron=False),
    drow("bell", "She is told when you release it", sub="Not when it arrives — when you have looked at it", name="Ord told", chevron=False, tone="ok"),
    drow("eye-off", "She cannot see the values yet", sub="A number out of range with nobody to explain it does harm", name="Ord hidden", chevron=False),
], footer="The gap between a result arriving and a doctor reading it is the most dangerous hour in the whole system. Medra keeps her out of it.")

C12_OTHER = dgroup("Your other open orders · 4", [
    request_row("flask-conical", "Musa Ibrahim · troponin", "Ketu Medical Laboratory · verified · waiting on you", "2h", "Ord musa", "warn",
                [dbtn("Read it", "Open result P8", "arrow-right", "navy", size="sm")]),
    request_row("scan", "Emeka Nwosu · knee X-ray", "Zenith Imaging · single-use link · not opened yet", "1d", "Ord emeka", "info",
                [dbtn("Chase it", "Open links C15", "link", "ghost", size="sm")]),
    request_row("flask-conical", "Grace Okeke · HbA1c", "Garki laboratory · sample not given yet", "3d", "Ord grace", "err",
                [dbtn("Remind her", "Ord remind", "bell", "ghost", size="sm")]),
], footer="Sorted by what is closest to going wrong, not by when you sent it.")

addx("Consult", "C12-order",
    dr_desk("Doctor · Consult — C12 Order Status", ["Consults", "Amara Okeke", "Order"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Tests")}</Frame>'
        f'{C_STRIP}'
        f'{dhead([("Order",False),("GK-2291",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C12_TRACK}{C12_OTHER}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C12_HER}{C12_STUCK}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=1, badges=BADGES),
    dr_head("Order GK-2291", "Amara Okeke · in analysis",
            stats=[("3/5", "Steps"), ("08:41", "Started"), ("4", "Open orders")]),
    pinned=C12_TRACK,
    sections=[
      ("hers", "smartphone", "What Amara sees right now", "Not the values — not until you have read them", None, None,
       C12_HER, None),
      ("stuck", "circle-help", "If it stalls", "Call, message, reroute or cancel", "4", "warn",
       C12_STUCK, None),
      ("other", "flask-conical", "Your other open orders", "One verified and waiting on you", "4", "warn",
       C12_OTHER, [("4", "Open"), ("1", "Waiting"), ("3d", "Oldest")]),
    ],
    foot=dcta("Read the result that is ready", "Open result P8", "arrow-right"),
    tab=MTAB["Consult"])

# ---------------- C13 a link for someone who is not on Medra
C13_WHO = dgroup("Who is this for?", [
    field("Organisation or person", "building-2", "Lifebridge Diagnostics", ph=False,
          helper="The name goes on the page they open, so they know it is not a phishing link."),
    field("Their phone number", "phone", "805 441 2290", ph=False, prefix="+234",
          helper="The link is sent here and nowhere else. It is not emailed, and it is not guessable from anything else you have typed."),
    field_chips("What do you need from them?", ["Run a test", "Read an image", "Send a report", "Give an opinion"], 0, "Link job"),
    drow("history", "You have sent to Lifebridge before", sub="Four times · they have always returned the report inside a day", name="Link history", chevron=False, tone="ok"),
])

C13_SCOPE = dgroup("What the link will carry", [
    consent_row("user", "Her name, age and Medra ID", "Amara Okeke · 34 · MDR-8842-19", "Lk identity", locked=True),
    consent_row("triangle-alert", "Allergies", "Penicillin", "Lk allergy", locked=True),
    consent_row("file-text", "Why you are asking", "MRI lumbar spine — six weeks of low back pain, no red flags", "Lk reason"),
    consent_row("clipboard-list", "The relevant part of her history", "Hypertension, on Amlodipine 5 mg", "Lk history"),
    consent_row("flask-conical", "Her last blood results", "Full blood count, 12 June", "Lk labs", on=False),
    consent_row("stethoscope", "Your full consultation note", "Everything you wrote today", "Lk note", on=False),
    consent_row("phone", "Her phone number", "So they can call her directly", "Lk phone", on=False),
], footer="Two lines always travel and cannot be switched off: who she is, and what she is allergic to. Everything else starts off. A radiographer does not need her medicine list to take a picture of her spine.")

C13_LIFE = dgroup("How long it lives", [
    field_chips("It dies when", ["They finish the job", "24 hours", "48 hours", "7 days"], 0, "Lk expiry"),
    dtoggle("shield-check", "They must accept a privacy undertaking first", sub="Recorded with the time — this is what makes the share lawful under the NDPA", on=True, name="Lk undertaking"),
    dtoggle("eye", "Tell me the moment they open it", sub="And again if they have not opened it in 24 hours", on=True, name="Lk watch"),
    dtoggle("user-check", "Amara must approve before it exists", sub="Cannot be switched off. It is her record", on=True, name="Lk consent"),
], footer="Whichever comes first. A link that outlives the job it was made for is just an unlocked door.")

C13_RULES = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","What a link is, and is not")}</Frame>'
    + T(12, "regular", "var:text/default",
        "It is a page for one job, for one recipient, that closes behind them. It is not an account, not a login, and not a copy of her record. They cannot browse from it, cannot download the rest, and cannot come back tomorrow to look again.", w="fill")
    + T(11, "regular", "var:text/muted",
        "The address is a random token, not her Medra ID — nobody can guess a link by counting, and one link tells you nothing about any other.", w="fill"),
    bg="var:state/info-bg", stroke=None)

addx("Consult", "C13-link",
    dr_desk("Doctor · Consult — C13 Send to Someone Not on Medra", ["Consults", "Amara Okeke", "External"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Where the order goes")}</Frame>'
        f'{C_STRIP}'
        f'{dhead([("A link for",False),("Lifebridge Diagnostics",True)],26)}'
        f'{T(14,"regular","var:text/muted","They have no Medra account and will not open one to read a single scan. This gives them exactly what the job needs.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C13_WHO}{C13_SCOPE}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{C13_RULES}{C13_LIFE}'
        f'{dcta("Ask Amara to approve it","Ask consent C13","user-check")}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Send outside Medra", "Lifebridge Diagnostics · MRI",
            stats=[("4", "Items"), ("3", "Withheld"), ("1 job", "Lifespan")]),
    pinned=C13_WHO,
    sections=[
      ("scope", "shield-check", "What the link will carry", "Four items on, three off, two locked", "4", None,
       C13_SCOPE, [("4", "Shared"), ("3", "Withheld"), ("2", "Always")]),
      ("life", "timer", "How long it lives", "One job, then it dies", None, None,
       C13_LIFE, None),
      ("rules", "info", "What a link is, and is not", "Not an account, not a copy", None, None,
       C13_RULES, None),
    ],
    foot=dcta("Ask Amara to approve it", "Ask consent C13", "user-check"),
    tab=MTAB["Consult"])

# ---------------- C14 waiting on the member
C14_WAIT = dcard(
    f'<Frame w="fill" flex="col" gap={{13}} items="center">'
    f'{big_icon("user-check","warn",84)}'
    f'{T(22,"bold","var:text/strong","Waiting for Amara")}'
    f'{T(14,"regular","var:text/muted","She has the request on her phone. Nothing exists until she says yes — there is no link to send, and Lifebridge has been told nothing.",w="fill",align="center")}'
    f'<Frame flex="row" gap={{8}} items="center" px={{13}} py={{8}} rounded={{10}} bg="var:state/warning-bg">'
    f'{I("clock",14,WARN_IC)}{T(12,"semibold","var:state/warning","Asked 2 minutes ago · she usually replies within the hour")}</Frame></Frame>')

C14_SEES = dgroup("What she was asked", [
    drow("user-check", "“Dr. Okafor wants to send your details to Lifebridge Diagnostics”", sub="With your name, your MDCN number and your photo, so she knows it is really you", name="Cs who", chevron=False),
    drow("list-checks", "The four things it would carry", sub="Written out in full, not summarised as “your records”", name="Cs what", chevron=False),
    drow("timer", "That it dies when the scan is done", sub="And that she can revoke it at any point before then", name="Cs life", chevron=False),
    drow("circle-help", "That declining does not affect her care", sub="Stated plainly. A consent given out of fear is not consent", name="Cs free", chevron=False, tone="ok"),
], footer="She is shown exactly what you ticked. Not a summary of it — the same list, in the same words.")

C14_IF = dgroup("If she says no", [
    outcome_choice("printer", "Print it and give it to her", "She carries the request to Lifebridge herself. Slower, and the report comes back on paper — but it is still her choice to make.", "Cn print", tone="info"),
    outcome_choice("building-2", "Use a laboratory on Medra instead", "Ketu Medical Laboratory can do this scan. Nothing leaves the platform, so nothing needs a link.", "Cn partner", tone="ok"),
    outcome_choice("message-circle", "Ask her why", "Sometimes it is one item on the list, not the whole idea. You can send a narrower request.", "Cn ask", tone="info"),
    outcome_choice("x", "Do not do the scan", "Record that it was offered and declined. That belongs in the note.", "Cn none", tone="warn"),
], footer="Do not send it anyway on paper without telling her. That is the same share with the audit trail removed.")

C14_TRAIL = dgroup("What is being recorded", [
    audit_row("You", "Asked to share 4 items with Lifebridge Diagnostics", "2 min ago"),
    audit_row("Amara", "Opened the request", "1 min ago"),
    audit_row("Medra", "Nothing sent — no link exists yet", "now"),
], footer="This trail is hers. It is append-only, and neither you nor Medra can edit it — which is exactly why it is worth anything if she is ever asked what she agreed to.")

addx("Consult", "C14-consent",
    dr_desk("Doctor · Consult — C14 Waiting on Consent", ["Consults", "Amara Okeke", "Consent"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Change what it carries")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} justify="center" items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C14_WAIT}{C14_SEES}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{C14_TRAIL}'
        f'{dcta("She approved — create the link","Open links C15","link")}'
        f'{dbtn("Withdraw the request","Withdraw consent C14","x","ghost",full=True)}'
        f'{C14_IF}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("Waiting on Amara", "Lifebridge Diagnostics · asked 11:22",
            stats=[("4", "Items asked"), ("2m", "Waiting"), ("<1h", "Usual reply")]),
    pinned=C14_WAIT,
    sections=[
      ("sees", "smartphone", "What she was asked", "Your name, the four items, and that no is free", "4", None,
       C14_SEES, None),
      ("trail", "history", "What is being recorded", "Append-only, and it is hers", "3", None,
       C14_TRAIL, None),
      ("if", "circle-help", "If she says no", "Four ways forward, none of them a workaround", "4", "warn",
       C14_IF, None),
    ],
    foot=f'{dcta("She approved — create the link","Open links C15","link")}'
         f'{dbtn("Withdraw the request","Withdraw consent C14","x","ghost",full=True)}',
    tab=MTAB["Consult"])

# ---------------- C15 the link exists
C15_LINK = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'<Frame flex="row" gap={{8}} items="center" px={{10}} py={{6}} rounded={{8}} bg="var:state/success-bg">'
    f'{I("circle-check",13,OK_IC)}{T(11,"semibold","var:state/success","Amara approved it at 11:29")}</Frame>'
    f'{T(11,"regular","var:text/muted","Expires when the report is uploaded")}</Frame>'
    + f'<Frame w="fill" flex="row" gap={{11}} items="center" px={{15}} py={{14}} rounded={{13}} bg="var:neutral/50" '
    + f'stroke="var:border/subtle" strokeWidth={{1}}>{I("link",16,M_IC)}'
    + T(14, "semibold", "var:text/strong", "medra.ng/s/7fQ2-K9mR-4vXt", w="fill")
    + f'<Frame name="Btn Copy link C15" flex="row">{I("copy",16,N_IC)}</Frame></Frame>'
    + T(11, "regular", "var:text/muted",
        "A random token, not her Medra ID. Nobody can reach her record by guessing, and this link tells you nothing about any other.", w="fill")
    + rows_of([dbtn("Send on WhatsApp", "Send wa C15", "message-circle", "navy", size="sm"),
               dbtn("Send by SMS", "Send sms C15", "message-square-text", "ghost", size="sm")], 2, 8)
    + rows_of([dbtn("Show the QR", "Show qr C15", "qr-code", "ghost", size="sm"),
               dbtn("Revoke it now", "Revoke C15", "ban", "danger", size="sm")], 2, 8))

C15_THEY = dgroup("What Lifebridge will see", [
    prep_step(1, "A privacy undertaking", "Three clauses, a name, and a tick. Recorded with the time — that is what makes this lawful"),
    prep_step(2, "The job, and only the job", "Amara Okeke, 34, MDR-8842-19 · penicillin allergy · MRI lumbar spine · your clinical reason"),
    prep_step(3, "A way to send the report back", "Photograph it or attach a file. It arrives in your list as a structured result, not an email"),
    prep_step(4, "The page closing behind them", "The moment they mark it done, the link is dead. Opening it again shows an expired page"),
], footer="Four screens, no account, no training, no way back in. Somebody who has never heard of Medra can finish this on a phone in a waiting room.")

C15_ALL = dgroup("Your open links · 3", [
    link_row_dr("Lifebridge Diagnostics", "Amara Okeke · MRI lumbar spine", "open", "Just created", "Link lifebridge"),
    link_row_dr("Zenith Imaging", "Emeka Nwosu · knee X-ray", "open", "Not opened · 1 day", "Link zenith"),
    link_row_dr("Ketu Medical Laboratory", "Musa Ibrahim · troponin", "used", "Report returned 09:40", "Open result P8"),
    link_row_dr("St. Mary's Clinic", "Fatima Bello · discharge summary", "expired", "4 Aug", "Link stmarys"),
], footer="Anything still unopened after 24 hours is chased for you. Anything you no longer want open is revoked here in one tap, and the recipient sees an expired page immediately.")

C15_AUDIT = dgroup("Amara's audit trail", [
    audit_row("You", "Created a link for Lifebridge Diagnostics", "11:29"),
    audit_row("Amara", "Approved 4 items · declined 3", "11:29"),
    audit_row("Lifebridge", "Has not opened it yet", "—"),
], footer="She sees this list on her phone, in the same words, without asking you. She can revoke the link from there at any moment, and you are told when she does.")

addx("Consult", "C15-links",
    dr_desk("Doctor · Consult — C15 The Link Is Ready", ["Consults", "Amara Okeke", "Link"],
        f'{dhead([("Send this to",False),("Lifebridge",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C15_LINK}{C15_ALL}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{C15_THEY}{C15_AUDIT}'
        f'{dbtn("Back to the consultation","Open room C1","arrow-left","ghost",full=True)}</Frame></Frame>',
        NAV["Consults"], PANEL_CONSULT, urgent=0, badges=BADGES),
    dr_head("The link is ready", "Lifebridge Diagnostics · approved 11:29",
            stats=[("4", "Items"), ("1 job", "Lifespan"), ("3", "Open links")]),
    pinned=C15_LINK,
    sections=[
      ("they", "monitor-smartphone", "What Lifebridge will see", "Four screens, no account, no way back", "4", None,
       C15_THEY, None),
      ("all", "link", "Your open links", "Three open, one used, one expired", "3", "warn",
       C15_ALL, [("3", "Open"), ("1", "Unopened"), ("1", "Expired")]),
      ("audit", "history", "Amara's audit trail", "She sees this without asking you", "3", None,
       C15_AUDIT, None),
    ],
    foot=dbtn("Back to the consultation", "Open room C1", "arrow-left", "ghost", full=True),
    tab=MTAB["Consult"])

# =====================================================================================
# 4. PATIENTS
# =====================================================================================
P1_SEARCH = dcard(
    field("Find a patient", "search", "MDR-8842", ph=False, focus=True,
          helper="Medra ID, full name or phone number. Partial IDs work — MDR-88 is enough.")
    + rows_of([dbtn("My patients", "Filter mine", None, "navy", size="sm"),
               dbtn("Seen this week", "Filter week", None, "ghost", size="sm"),
               dbtn("Owing a test", "Filter owing", "flask-conical", "ghost", size="sm"),
               dbtn("Due a follow-up", "Open followups P4", "repeat", "ghost", size="sm")], 4, 8)
    + rows_of([dbtn("Scan their code", "Scan patient", "qr-code", "ghost", size="sm"),
               dbtn("Add a walk-in", "Add walkin", "user-plus", "ghost", size="sm")], 2, 8))

P1_LIST = dgroup("42 patients", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "34 · hypertension · O+ · AA", "Today", "Open Amara", tag="today"),
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "6 · guardian Amara Okeke", "Today", "Open Chidi", tag="today"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "68 · diabetes, hypertension", "28 Apr", "Open Grace"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "51 · first visit today", "Never", "Open Musa", tag="new"),
    patient_row("avatar-5.jpg", "Tunde Bello", "MDR-6620-88", "44 · awaiting results", "2 Aug", "Open Tunde", tag="pending"),
    patient_row("avatar-4.jpg", "Fatima Bello", "MDR-2201-13", "29 · asthma", "12 Aug", "Open Fatima"),
], footer="You see a patient here if they booked you, or if they granted you access. Nobody else.")

P1_CANT = dgroup("Cannot find someone?", [
    drow("qr-code", "Scan the code on their phone", sub="Or the QR on their printed summary", name="Scan patient"),
    drow("user-plus", "Add a walk-in", sub="They get a Medra ID and can claim the record later", name="Add walkin"),
    drow("circle-help", "They may not have shared with you", sub="Medra does not show you patients who have not", name="Why missing", chevron=False),
    drow("hospital", "Ask reception to look them up", sub="Front desk can search the whole facility", name="Ask reception", chevron=False),
])

P1_ACCESS = dgroup("Access replies", [
    audit_row("Amara Okeke", "Agreed to share her prescription history", "12 min ago"),
    audit_row("Grace Okeke", "Declined to share home vitals", "Yesterday"),
], footer="Declining is normal and does not affect their care. It is recorded either way.")

addx("Patients", "P1-patients",
    dr_desk("Doctor · Patients — P1 Find a Patient", ["Patients", "All"],
        f'{dhead([("Your",False),("patients",True)],26)}'
        f'{T(14,"regular","var:text/muted","Search by Medra ID when someone cannot remember anything else — it is on their phone and on their printed summary.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P1_SEARCH}{P1_LIST}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{P1_ACCESS}{P1_CANT}</Frame></Frame>',
        NAV["Patients"], PANEL_PATIENTS, badges=BADGES),
    dr_head("Patients", "42 · 8 seen this week", back=False,
            stats=[("42", "Total"), ("7", "Follow-up due"), ("5", "Owing a test")],
            chips=[("All", "Filter mine", True), ("This week", "Filter week", False), ("Follow-up", "Open followups P4", False)],
            right=f'<Frame name="Btn Scan patient" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("qr-code",17,W_IC)}</Frame>'),
    pinned=f'{P1_SEARCH}{P1_LIST}',
    sections=[
      ("access", "message-square-text", "Access replies", "Amara agreed; Musa declined one category", "2", None,
       P1_ACCESS, None),
      ("cant", "circle-help", "Cannot find someone?", "Scan, search by phone, or add a walk-in", "3", None,
       P1_CANT, None),
    ],
    tab=MTAB["Patients"])

# ---------------- P2 patient record
P2_HEAD = dcard(
    f'<Frame w="fill" flex="row" gap={{14}} items="center">'
    f'<Image image="assets/img/avatar-2.jpg" w={{62}} h={{62}} rounded={{18}} />'
    # The ID chip and the meta line were competing for one row with the status pill and both
    # wrapped. Name and ID on one line, everything else underneath.
    # A pill inside a grow column shrinks below its text. The ID is a plain line instead.
    f'<Frame grow={{1}} flex="col" gap={{4}}>'
    f'{T(19,"bold","var:text/strong","Amara Okeke",w="fill")}'
    f'{T(12,"semibold","var:text/accent","MDR-8842-19",w="fill")}'
    f'{T(12,"regular","var:text/muted","34 · female · Garki, Abuja · +234 801 234 5678",w="fill")}</Frame>'
    f'{status_pill("shared","Access until 21 Aug, 11:00")}</Frame>'
    + rows_of([kv("Height", "1.68 m", "ruler"), kv("Weight", "74 kg", "weight"),
               kv("Visits with you", "3", "history"), kv("On Medra since", "Jan 2026", "calendar-days")], 4, 12)
    + hr()
    + health_fact("Blood group", "O+", verified=False, name="Fact blood",
                  by="She entered this herself · no laboratory result on file")
    + health_fact("Genotype", "AA", verified=False, name="Fact geno",
                  by="She entered this herself · no laboratory result on file")
    + note("circle-help",
           "Two values on this record have never been tested. Do not act on them as fact — order a "
           "group and screen if it matters for what you are about to do.", "warn"))

P2_SAFETY = alert_strip("triangle-alert", "Penicillin allergy · hypertension",
    "Shown to any doctor treating her, whatever else she has shared. Reaction: rash and swelling, June 2026.", "err")

P2_TIMELINE = dgroup("Her history", [
    timeline_entry("14", "Aug", "activity", "Blood pressure 128/82", "Measured at home — not shared with you", "Open vitals", "muted"),
    timeline_entry("12", "Jun", "stethoscope", "Hypertension review", "You · Garki Medical Centre · signed 11:42", "Open note last", "info"),
    timeline_entry("12", "Jun", "pill", "Amlodipine 5 mg · 30 days", "You · 96% taken on time", "Open adherence", "ok"),
    timeline_entry("12", "Jun", "flask-conical", "Full blood count", "Haemoglobin low at 11.2", "Open lab", "warn", "new"),
    timeline_entry("28", "Apr", "stethoscope", "Malaria — treated", "Dr. Chuka Eze · Wuse Clinic", "Open other note", "info"),
    timeline_entry("28", "Apr", "syringe", "Yellow fever booster", "Wuse Clinic · certificate attached", "Open vaccine", "ok"),
    timeline_entry("02", "Aug", "file-plus", "Scan of an old NHIS card", "Added by the patient — not clinician-verified", "Open upload", "muted"),
], footer="Records added by the patient are labelled. So are readings they took themselves — you can always tell what a record is worth.")

P2_LOCKED = dgroup("Not shared with you", [
    scope_line("Prescription history from other clinics", False, "She can turn this on from her phone"),
    scope_line("Home vitals", False, "Blood pressure readings she takes herself"),
    scope_line("Records she has marked private", False, "You are told they exist, not what they say"),
], footer="Asking is a normal part of a consultation. Use “Ask for more history” — she can accept, part-accept or decline.")

P2_VITALS = dgroup("Blood pressure · clinic readings", [
    chart([("Mar", "142/92", 92, "bad"), ("Apr", "138/88", 82, "warn"), ("May", "136/86", 78, "warn"),
           ("Jun", "132/84", 70, "ok"), ("Jul", "130/82", 64, "ok"), ("Aug", "128/82", 60, "ok")], 118, "Systolic, mmHg"),
], footer="Clinic readings only. Her home readings are not shared with you.")

P2_ACTIONS = dgroup("Do something", [
    drow("stethoscope", "Start a consultation", sub="Even without a booking — a walk-in counts", name="Start consult"),
    drow("message-square-text", "Ask for more history", name="Open access P3"),
    drow("calendar-plus", "Book her a follow-up", name="Open followups P4"),
    drow("message-circle", "Message her", sub="WhatsApp · she replies most days", name="Open messages P5"),
    drow("printer", "Print a summary for her file", name="Print summary"),
])

addx("Patients", "P2-record",
    dr_desk("Doctor · Patients — P2 Record", ["Patients", "Amara Okeke"],
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Patients")}</Frame>'
        f'<Frame flex="row" gap={{9}} items="center">'
        f'{dbtn("Ask for more history","Open access P3","message-square-text","ghost",grow=False,size="sm")}'
        f'{dbtn("Start a consultation","Start consult","stethoscope","navy",grow=False,size="sm")}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P2_HEAD}{P2_SAFETY}{P2_TIMELINE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{P2_VITALS}{P2_LOCKED}{P2_ACTIONS}</Frame></Frame>',
        NAV["Patients"], PANEL_PATIENTS, badges=BADGES),
    dr_head("Amara Okeke", "MDR-8842-19 · access until 11:00",
            stats=[("O+", "Blood"), ("AA", "Genotype"), ("3", "Visits")],
            right=f'<Frame name="Btn Start consult" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("stethoscope",17,W_IC)}</Frame>'),
    pinned=P2_SAFETY,
    sections=[
      ("timeline", "history", "Her history", "Eight visits · three with you", "8", None,
       P2_TIMELINE, [("8", "Visits"), ("3", "With you"), ("5", "Elsewhere")]),
      ("vitals", "activity", "Vitals and measurements", "BP, weight, and what she records herself", "6", None,
       P2_VITALS, None),
      ("locked", "lock", "What she has not shared", "Two categories — you can ask", "2", "warn",
       P2_LOCKED, None),
      ("actions", "circle-plus", "What you can do here", "Consult, ask, message, follow up", "5", None,
       P2_ACTIONS, None),
    ],
    tab=MTAB["Patients"])

# ---------------- P3 ask for more history
P3_PICK = dgroup("What do you need to see?", [
    consent_row("pill", "Prescription history from other clinics", "What she was given and whether she took it", "Ask rx"),
    consent_row("activity", "Home blood pressure readings", "Her own measurements between visits", "Ask vitals"),
    consent_row("flask-conical", "Older lab results", "Anything before January 2026", "Ask labs", on=False),
    consent_row("file-plus", "Records she uploaded herself", "Scans of paper results", "Ask uploads", on=False),
])
P3_WHY = dgroup("Why are you asking?", [
    field("She sees this message", "message-square-text",
          "I want to check whether the headaches started before or after we changed your dose. Your older prescriptions would tell me.", ph=False),
    radio_row("Just for this consultation", sub="Access ends when you sign the note", on=True, name="Ask window visit"),
    radio_row("For 7 days", sub="If you are waiting on results", name="Ask window 7d"),
    radio_row("For 30 days", sub="Ongoing treatment", name="Ask window 30d"),
], footer="She can accept, accept part of it, or decline. Declining is recorded and does not affect her care.")
P3_ASKED = dgroup("What you have already asked", [
    audit_row("You asked for prescription history", "Declined by the patient · 12 Jun", "2 months ago"),
    audit_row("You asked about undisclosed history", "Answered on the call · 21 Aug", "Today"),
    audit_row("You opened “Hypertension review”", "Logged and visible to her", "Today, 09:12"),
], footer="Asking is logged, so it is always clear what you tried to find out and what you were told.")
P3_HOW = dgroup("How she gets it", [
    drow("bell-ring", "In the app", value="Now", sub="She is in the waiting room, so she will see it", name="Ask app", tone="ok", chevron=False),
    drow("message-circle", "WhatsApp", value="Now", sub="Most people answer within a few minutes during a consultation", name="Ask wa", tone="ok", chevron=False),
    drow("message-square-text", "SMS", value="If no reply in 5 min", name="Ask sms", chevron=False),
])

addx("Patients", "P3-access",
    dr_desk("Doctor · Patients — P3 Ask for More", ["Patients", "Amara Okeke", "Ask for more"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Amara Okeke")}</Frame>'
        f'{dhead([("Ask her for",False),("more history",True)],26)}'
        f'{T(14,"regular","var:text/muted","She controls her record. You can always ask — and what you asked, and what she answered, is recorded.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P3_PICK}{P3_WHY}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{P3_HOW}{P3_ASKED}'
        f'{dcta("Send the request","Send access P3","send")}</Frame></Frame>',
        NAV["Patients"], PANEL_PATIENTS, badges=BADGES),
    dr_head("Ask for more", "Amara Okeke · 2 categories",
            stats=[("2", "Selected"), ("Visit", "Window"), ("3", "Channels")]),
    pinned=P3_PICK,
    sections=[
      ("why", "message-circle", "Tell her why", "She is far more likely to say yes", None, None,
       P3_WHY, None),
      ("how", "settings", "How and for how long", "Channel, window, and what she sees", None, None,
       P3_HOW, None),
      ("asked", "history", "What you have already asked", "Two answered, one declined", "3", None,
       P3_ASKED, None),
    ],
    foot=dcta("Send the request", "Send access P3", "send"),
    tab=MTAB["Patients"])

# ---------------- P4 follow-ups and recalls  (Retention)
P4_DUE = dgroup("Due now · 7", [
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "3-month review · due 2 weeks ago · diabetes", "Overdue", "Fu Grace", tag="missed"),
    patient_row("avatar-4.jpg", "Fatima Bello", "MDR-2201-13", "Asthma review · due this week", "Due", "Fu Fatima", tag="soon"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "Post-result discussion · due Friday", "Due", "Fu Musa", tag="soon"),
    patient_row("avatar-5.jpg", "Tunde Bello", "MDR-6620-88", "Never did the MRI you ordered · 6 weeks", "Overdue", "Fu Tunde", tag="missed"),
], footer="A recall list is the cheapest retention there is. These are people who already trust you.")

P4_TESTS = dgroup("Ordered but never done · 5", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "Fasting blood sugar · ordered 12 Jun", "9 weeks", "Test Amara", tag="missed"),
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "Chest X-ray · ordered 2 Aug", "2 weeks", "Test Chidi", tag="pending"),
], footer="Medra reminds them automatically. This list is who is still ignoring it.")

P4_SEND = dgroup("Send a recall", [
    field("The message", "message-square-text",
          "It is time for your three-month review. I have slots on Tuesday and Thursday — booking takes about a minute.", ph=False),
    dtoggle("message-circle", "WhatsApp", on=True, name="Recall wa"),
    dtoggle("message-square-text", "SMS", sub="For anyone who has not opened the app in 30 days", on=True, name="Recall sms"),
    dtoggle("calendar-plus", "Include my next three open slots", sub="One tap to book, which roughly doubles the response", on=True, name="Recall slots"),
], footer="Recalls are capped at one per patient per month. Medra will not let you become a nuisance.")

P4_RESULT = dgroup("How recalls have gone", [
    kpi_line("Sent in the last 30 days", "24"),
    kpi_line("Booked from a recall", "11", "ok"),
    kpi_line("Response rate", "46%", "ok"),
    kpi_line("Opted out", "1", "muted"),
], footer="Indicative pilot figures.")

addx("Patients", "P4-followups",
    dr_desk("Doctor · Patients — P4 Follow-ups", ["Patients", "Follow-ups and recalls"],
        f'{dhead([("Twelve people",False),("owe you a visit",True)],26)}'
        f'{T(14,"regular","var:text/muted","Seven are due a review; five never did a test you ordered. Both are easier to convert than a stranger.",w="fill")}'
        f'{rows_of([stat_tile("repeat","7","Reviews due","2 overdue","warn","Stat due"),stat_tile("flask-conical","5","Tests never done","Oldest 9 weeks","err","Stat tests"),stat_tile("send","24","Recalls sent","Last 30 days","info","Stat sent"),stat_tile("calendar-check","11","Booked from a recall","46% response","ok","Stat booked")],4,14)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P4_DUE}{P4_TESTS}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{P4_SEND}{P4_RESULT}'
        f'{dcta("Send to all 12","Send recall P4","send")}</Frame></Frame>',
        NAV["Patients"], PANEL_PATIENTS, badges=BADGES),
    dr_head("Follow-ups", "12 people owe you a visit", back=False,
            stats=[("7", "Reviews due"), ("5", "Tests undone"), ("46%", "Response")]),
    sections=[
      ("due", "repeat", "Reviews due", "Grace two weeks overdue", "7", "warn",
       P4_DUE, [("7", "Due"), ("2", "Overdue"), ("46%", "Respond")]),
      ("tests", "flask-conical", "Tests never done", "Oldest ordered nine weeks ago", "5", "err",
       P4_TESTS, None),
      ("send", "send", "The recall message", "With your next open times", None, None,
       P4_SEND, None),
      ("result", "chart-column", "How recalls have performed", "11 booked from 24 sent", None, "ok",
       P4_RESULT, None),
    ],
    foot=dcta("Send to all 12", "Send recall P4", "send"),
    tab=MTAB["Patients"])

# ---------------- P5 messages
P5_LIST = dgroup("Messages · 4 unread", [
    msg_row("avatar-3.jpg", "Grace Okeke", "“Doctor, the new tablet is making me dizzy in the mornings. Should I stop?”", "8 min", "Msg Grace", unread=True),
    msg_row("avatar-2.jpg", "Amara Okeke", "“Thank you for today. I have booked the blood test for Saturday.”", "1 h", "Msg Amara", unread=True),
    msg_row("avatar-1.jpg", "Musa Ibrahim", "“Is the 09:00 on Friday still going ahead?”", "3 h", "Msg Musa", unread=True, channel="email"),
    msg_row("avatar-4.jpg", "Fatima Bello", "“Sent the inhaler photo you asked for.”", "Yesterday", "Msg Fatima", unread=True),
    msg_row("avatar-6.jpg", "Amara Okeke (for Chidi)", "“His cough is better, thank you.”", "2 days", "Msg Chidi", channel="inapp"),
], footer="Only patients you have consulted can message you, on the channels you turned on. Everything is attached to their record.")

P5_URGENT = alert_strip("triangle-alert", "One message mentions a symptom",
    "Grace Okeke wrote “dizzy in the mornings”. Medra flags possible side effects so they do not sit unread in a busy day.", "err",
    dbtn("Open it", "Msg Grace", None, "ghost", grow=False, size="sm"))

P5_QUICK = dgroup("Quick replies", [
    drow("message-square-text", "“Stop it and let us speak today.”", sub="Attaches your next open slot", name="Quick stop"),
    drow("message-square-text", "“Yes, that appointment is going ahead.”", name="Quick confirm"),
    drow("message-square-text", "“Please book a visit so I can examine you.”", sub="Attaches your booking link", name="Quick book"),
    drow("plus", "Write a new quick reply", name="Quick new", chevron=False),
])

P5_RULES = dgroup("Your boundaries", [
    drow("clock", "You show as available", value="08:00 – 18:00", sub="Outside this, patients see “replies tomorrow”", name="Msg hours"),
    dtoggle("moon", "Do not disturb outside those hours", on=True, name="Msg dnd"),
    drow("triangle-alert", "Emergencies are never handled here", sub="Chest pain, breathlessness or bleeding show an emergency banner instead", name="Msg emergency", chevron=False),
], footer="Medra tells patients plainly that messages are not for emergencies, and shows them what to do instead.")

addx("Patients", "P5-messages",
    dr_desk("Doctor · Patients — P5 Messages", ["Patients", "Messages"],
        f'{dhead([("Four people",False),("are waiting",True)],26)}'
        f'{P5_URGENT}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P5_LIST}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{P5_QUICK}{P5_RULES}</Frame></Frame>',
        NAV["Patients"], PANEL_PATIENTS, urgent=4, badges=BADGES),
    dr_head("Messages", "4 unread · 1 flagged", back=False,
            stats=[("4", "Unread"), ("1", "Flagged"), ("18:00", "Until")]),
    pinned=f'{P5_URGENT}{P5_LIST}',
    sections=[
      ("quick", "zap", "Quick replies", "Four you send most often", "4", None,
       P5_QUICK, None),
      ("rules", "moon", "Your boundaries", "Hours, do-not-disturb, what counts as urgent", None, None,
       P5_RULES, None),
    ],
    tab=MTAB["Requests"])

# ---------------- P6 refill requests
def refill_actions(name):
    return [dbtn("Approve", "Approve " + name, "check", "navy", size="sm"),
            dbtn("Change it", "Change " + name, "pencil", "ghost", size="sm"),
            dbtn("Ask them in", "Visit " + name, "calendar-plus", "warn", size="sm"),
            dbtn("Decline", "Decline " + name, "x", "danger", size="sm")]

P6_LIST = dgroup("Refill requests · 2", [
    request_row("package", "Grace Okeke · MDR-8842-21",
                "Metformin 500 mg · 30 days · 4 days left · collect at Garki pharmacy · “The evening one makes me a little nauseous.”",
                "19 hours", "Refill Grace", "warn", refill_actions("Grace")),
    request_row("package", "Fatima Bello · MDR-2201-13",
                "Salbutamol inhaler · 1 unit · delivery to Wuse II · last review 12 Aug",
                "4 hours", "Refill Fatima", "info", refill_actions("Fatima")),
], footer="Approving sends the prescription straight to the pharmacy. Nothing is automatic — a refill is still a clinical decision.")

P6_CONTEXT = dgroup("Before you approve Grace", [
    drow("history", "Last seen", value="28 Apr", sub="Nearly four months ago", name="Ref lastseen", tone="warn", chevron=False),
    drow("check-check", "Adherence", value="88%", sub="Taking it, mostly on time", name="Ref adherence", tone="ok", chevron=False),
    drow("flask-conical", "HbA1c", value="8.4% · high", sub="Arrived yesterday, not yet released to her", name="Ref hba1c", tone="err", chevron=False),
    drow("message-circle", "She reports nausea", sub="A known effect. Worth a conversation, not just a refill.", name="Ref side", tone="warn", chevron=False),
    drow("calendar-clock", "Review due", value="Overdue 2 weeks", name="Open followups P4", tone="warn", chevron=False),
], footer="Medra shows you this so a refill is never a blind renewal. On this one, asking her to come in is probably right.")

P6_RULES = dgroup("Refill rules", [
    drow("repeat", "Refills allowed without a visit", value="2", sub="Then a review is required", name="Rule refills"),
    drow("clock", "Reply within", value="24 hours", sub="What members are promised on your profile", name="Rule reply"),
    dtoggle("zap", "Auto-approve if seen in the last 3 months and refills remain", on=False, name="Rule auto"),
], footer="Auto-approve stays off by default. It is your MDCN number on the prescription.")

addx("Patients", "P6-refills",
    dr_desk("Doctor · Patients — P6 Refills", ["Requests", "Refills"],
        f'{dhead([("Two refills",False),("waiting",True)],26)}'
        f'{T(14,"regular","var:text/muted","The oldest has been waiting 19 hours. Members are told you reply within a day.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P6_LIST}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{P6_CONTEXT}{P6_RULES}</Frame></Frame>',
        NAV["Requests"], PANEL_REQ, urgent=6, badges=BADGES),
    dr_head("Refills", "2 waiting · oldest 19 hours", back=False,
            stats=[("2", "Waiting"), ("19h", "Oldest"), ("24h", "Promised")]),
    pinned=P6_LIST,
    sections=[
      ("context", "clipboard-list", "What makes this a decision", "Adherence, last review, and the dose", None, None,
       P6_CONTEXT, None),
      ("rules", "sliders-horizontal", "Refill rules", "What can be renewed without asking you", None, None,
       P6_RULES, None),
    ],
    tab=MTAB["Requests"])

# ---------------- P7 results inbox
def result_actions(name):
    return [dbtn("Release", "Release " + name, "send", "navy", size="sm"),
            dbtn("Hold it", "Hold " + name, "eye-off", "warn", size="sm"),
            dbtn("Book a follow-up", "Book " + name, "calendar-plus", "ghost", size="sm")]

P7_LIST = dgroup("Results waiting on you · 3", [
    request_row("flask-conical", "Grace Okeke · HbA1c 8.4%",
                "High · Garki laboratory · arrived yesterday 16:10 · diabetes, on metformin",
                "18 hours", "Res Grace", "err", result_actions("Grace")),
    request_row("flask-conical", "Musa Ibrahim · Troponin",
                "Normal · Garki laboratory · arrived 2 hours ago · ordered after chest tightness",
                "2 hours", "Res Musa", "ok", result_actions("Musa")),
    request_row("flask-conical", "Amara Okeke · Full blood count",
                "Haemoglobin 11.2 low · arrived 13 Jun · everything else normal",
                "Old", "Res Amara", "warn", result_actions("Amara")),
], footer="Nothing reaches a member until a doctor has looked at it. A number with no explanation is how people end up in an emergency room at midnight.")

P7_WHY = dgroup("Why a doctor releases results", [
    drow("eye-off", "No auto-release", sub="Not even normal results — “normal” still needs context", name="Why noauto", chevron=False),
    drow("book-open", "One line in plain language", sub="Prevents most of the panicked calls", name="Why plain", chevron=False),
    drow("calendar-plus", "Abnormal results suggest a follow-up", sub="Booked in the same action", name="Why followup", chevron=False),
    drow("clock", "Held results are chased", sub="We remind you at 48 hours — a held result must not become a forgotten one", name="Why chase", tone="warn", chevron=False),
])

P7_TREND = dgroup("Grace's HbA1c over time", [
    chart([("Aug 25", "7.1%", 48, "ok"), ("Feb 26", "7.6%", 60, "warn"), ("May 26", "8.0%", 72, "warn"),
           ("Aug 26", "8.4%", 88, "bad")], 118, "Target below 7.0%"),
], footer="Rising for a year. This is a conversation, not a text message.")

addx("Patients", "P7-results",
    dr_desk("Doctor · Patients — P7 Results", ["Requests", "Results"],
        f'{dhead([("Three results",False),("need a doctor",True)],26)}'
        f'{T(14,"regular","var:text/muted","One is out of range and rising. It should not go out without you.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P7_LIST}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{P7_TREND}{P7_WHY}</Frame></Frame>',
        NAV["Requests"], PANEL_REQ, urgent=6, badges=BADGES),
    dr_head("Results", "3 waiting · 1 out of range", back=False,
            stats=[("3", "Waiting"), ("1", "Abnormal"), ("18h", "Oldest")]),
    pinned=P7_LIST,
    sections=[
      ("trend", "trending-up", "Grace's HbA1c over a year", "6.9 → 8.4 · rising", None, "warn",
       P7_TREND, None),
      ("why", "info", "Why a doctor releases results", "And what happens if nobody does", None, None,
       P7_WHY, None),
    ],
    tab=MTAB["Requests"])

# ---------------- P8 a result that came back as data, not as a photograph
# C5 is the photograph path: a doctor holds a piece of paper and types what it says. This is
# the other one — a laboratory that is on Medra, or that used a single-use link, returns the
# values themselves. The difference matters clinically: these numbers can be trended, flagged
# and compared without anyone having read them off a page first.
P8_HEAD = dcard(
    f'<Frame w="fill" flex="row" gap={{13}} items="center">'
    f'<Image image="assets/img/avatar-1.jpg" w={{44}} h={{44}} rounded={{14}} />'
    f'<Frame grow={{1}} flex="col" gap={{3}}>'
    f'<Frame flex="row" gap={{8}} items="center">{T(15,"semibold","var:text/strong","Musa Ibrahim")}'
    f'<Frame flex="row" px={{8}} py={{2}} rounded={{6}} bg="var:bg/muted">'
    f'{T(10,"semibold","var:text/accent","MDR-7714-02")}</Frame></Frame>'
    f'{T(11,"regular","var:text/muted","51 · chest pain, seen 09:10 today · no known allergies",w="fill")}</Frame>'
    f'{status_pill("pending","Not released")}</Frame>'
    + f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{13}} py={{10}} rounded={{11}} bg="var:state/success-bg">'
    + I("database", 15, OK_IC)
    + T(12, "semibold", "var:state/success", "Structured result — the laboratory sent the values, nobody typed them", w="fill")
    + '</Frame>')

P8_VALUES = dgroup("Troponin I · high sensitivity", [
    lab_line("Troponin I", "12 ng/L", "0 – 14"),
    lab_line("Repeat at 3 hours", "13 ng/L", "0 – 14"),
    lab_line("Creatinine", "94 µmol/L", "62 – 106"),
    lab_line("Potassium", "5.4 mmol/L", "3.5 – 5.1", "High"),
    lab_line("eGFR", "78 mL/min", "> 90", "Low"),
], footer="Five values, two outside range. The reference ranges came from the laboratory that ran it — not from Medra — because ranges differ by analyser and by population.")

P8_DELTA = dgroup("Against his own history", [
    drow("trending-up", "Potassium", value="4.8 → 5.4", sub="First time above range. Was 4.8 in April, 4.6 in January", name="Del k", tone="warn", chevron=False),
    drow("trending-down", "eGFR", value="91 → 78", sub="Falling over eight months. Worth a look even though today's story is the chest pain", name="Del egfr", tone="warn", chevron=False),
    drow("minus", "Troponin", value="Flat", sub="No rise between the two samples — that is the finding, not the number itself", name="Del trop", tone="ok", chevron=False),
], footer="A single value is a number. Three of them across a year is the thing you actually treat. This is what a structured result buys you that a photograph of a page never can.")

P8_PROV = dgroup("Where this came from", [
    drow("building-2", "Ketu Medical Laboratory", sub="On Medra · MLSCN 4471 · accredited to 2027", name="Prov lab", chevron=False, tone="ok"),
    drow("user-check", "Verified by Ifeoma Nwachukwu", sub="Laboratory scientist · MLSCN 22019 · today 09:38", name="Prov who", chevron=False),
    drow("microscope", "Abbott Architect i2000SR", sub="Analyser and lot number are on the record. This is what makes the range meaningful", name="Prov machine", chevron=False),
    drow("clock", "Sample taken 06:20, verified 09:38", sub="Three hours eighteen minutes — inside their published turnaround", name="Prov when", chevron=False),
    drow("file-text", "The original report", sub="The laboratory's own PDF, unaltered, kept alongside the values", name="Prov pdf"),
], footer="Every clinical fact on Medra carries who produced it and when. A number with no provenance is a rumour, and no doctor should have to act on one.")

P8_ACT = dgroup("What happens next", [
    note_field("One line for Musa", "message-circle",
        "Your heart tracing and blood tests do not show a heart attack. One salt level is a little high and your kidney reading has drifted — nothing urgent, but I want to see you next week.",
        "p8 explain", lines=3, template=False),
    dtoggle("eye", "Release it to him now", sub="Turn this off to hold it until you have spoken to him", on=True, name="P8 release"),
    dtoggle("bell-ring", "Tell him it has arrived", sub="App, WhatsApp and SMS", on=True, name="P8 notify"),
    dtoggle("calendar-plus", "Book a follow-up", sub="Suggests your next three open slots", on=True, name="P8 followup"),
    dtoggle("flask-conical", "Order a repeat potassium", sub="Adds it to a new order you can route in one tap", on=False, name="P8 repeat"),
], footer="A result out of range with no explanation frightens people. One sentence from you prevents a call at 22:00 — and in this case it is the sentence that stops him thinking he has had a heart attack.")

P8_VS = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("info",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Why this is not the same as a photograph")}</Frame>'
    + T(12, "regular", "var:text/default",
        "A photographed report is an image with a doctor's transcription attached. It cannot be trended, cannot be flagged against a range, and any typing error becomes part of the record silently. A structured result is the laboratory's own numbers, with its own ranges, its own analyser and its own verifier's name.", w="fill")
    + T(11, "regular", "var:text/muted",
        "Both are supported, because most laboratories still hand over paper. But every result that arrives structured is one a future doctor can rely on without re-reading a photograph.", w="fill"),
    bg="var:state/info-bg", stroke=None)

addx("Patients", "P8-result",
    dr_desk("Doctor · Patients — P8 Structured Result", ["Requests", "Results", "Musa Ibrahim"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Results waiting")}</Frame>'
        f'{P8_HEAD}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{P8_VALUES}{P8_DELTA}{P8_PROV}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{P8_ACT}'
        f'{dcta("Release it to Musa","Release P8","badge-check")}'
        f'{dbtn("Hold it until I have spoken to him","Hold P8","pause","ghost",full=True)}{P8_VS}</Frame></Frame>',
        NAV["Requests"], PANEL_REQ, urgent=6, badges=BADGES),
    dr_head("Troponin · Musa", "Verified 09:38 · 2 out of range",
            stats=[("5", "Values"), ("2", "Out of range"), ("3h18", "Turnaround")]),
    pinned=f'{P8_HEAD}{P8_VALUES}',
    sections=[
      ("delta", "trending-up", "Against his own history", "Potassium rising, eGFR falling", "3", "warn",
       P8_DELTA, [("2", "Moving"), ("8mo", "Span"), ("1", "New")]),
      ("prov", "shield-check", "Where this came from", "Laboratory, scientist, analyser, timing", "5", None,
       P8_PROV, None),
      ("act", "send", "What happens next", "One line for him, then release or hold", None, None,
       P8_ACT, None),
      ("vs", "info", "Why this is not a photograph", "Trendable, flagged, and nobody transcribed it", None, None,
       P8_VS, None),
    ],
    foot=f'{dcta("Release it to Musa","Release P8","badge-check")}'
         f'{dbtn("Hold it until I have spoken to him","Hold P8","pause","ghost",full=True)}',
    tab=MTAB["Requests"])

# =====================================================================================
# 5. PRACTICE & MONEY
# =====================================================================================
S1_PROFILE = dcard(
    f'<Frame w="fill" flex="row" gap={{14}} items="center">'
    f'<Image image="assets/img/avatar-4.jpg" w={{72}} h={{72}} rounded={{20}} />'
    f'<Frame grow={{1}} flex="col" gap={{4}}>'
    f'<Frame flex="row" gap={{8}} items="center">{T(19,"bold","var:text/strong","Dr. Ngozi Okafor")}'
    f'{I("badge-check",17,T_IC)}</Frame>'
    f'{T(12,"regular","var:text/muted","Cardiologist · MDCN 71482 · verified 4 February 2026")}</Frame>'
    f'{dbtn("Change photo","Change photo S1","camera","ghost",grow=False,size="sm")}</Frame>'
    + field("Short bio", "file-text",
            "Consultant cardiologist with 12 years in hypertension, heart failure and preventive cardiology.",
            ph=False, helper="Members read this before they book. Two sentences beat two paragraphs.")
    + field("Specialisation", "stethoscope", "Cardiology", ph=False, trailing=("chevron-down", "Specialty dropdown"),
            helper="From the Medra list, which the platform team keeps current.")
    + f'<Frame w="fill" flex="col" gap={{8}}>{T(12,"medium","var:text/default","Also practises")}'
    + f'<Frame w="fill" flex="row" gap={{8}}>'
    + f'<Frame name="Btn Spec internal" flex="row" gap={{6}} items="center" px={{11}} py={{7}} rounded={{9}} bg="var:bg/muted">'
    + T(12, "medium", "var:text/default", "Internal medicine") + I("x", 12, M_IC) + '</Frame>'
    + f'<Frame name="Btn Add specialty" flex="row" gap={{6}} items="center" px={{11}} py={{7}} rounded={{9}} '
    + f'bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>' + I("plus", 12, N_IC)
    + T(12, "medium", "var:text/default", "Add another") + '</Frame></Frame></Frame>'
    + field_chips("Languages you consult in", ["English", "Hausa", "Yoruba", "Igbo", "Pidgin"], 0, "Langs")
    + field("Years in practice", "briefcase-medical", "12", ph=False)
    + field("Where you practise", "hospital", "Garki Medical Centre, Area 3, Abuja", ph=False,
            trailing=("chevron-down", "Open practice S7")))

S1_PUBLIC = dgroup("How members see you", [
    drow("star", "Rating", value="4.9", sub="From 148 completed visits", name="Open reviews R2", tone="ok"),
    drow("users", "Patients seen on Medra", value="1,204", name="Prof patients", chevron=False),
    drow("clock", "Median wait to be seen", value="6 minutes", sub="Shown on your profile — it is why people pick you", name="Prof wait", chevron=False),
    drow("repeat", "Patients who come back", value="61%", sub="Well above the pilot average of 43%", name="Prof repeat", tone="ok", chevron=False),
    drow("eye", "Preview my public profile", sub="Exactly what a member sees before booking", name="Preview profile"),
])

S1_COMPLETE = dgroup("Profile completeness · 85%", [
    bar(85, "teal", 10),
    checklist_row(True, "Photo", "Clear, recent, facing the camera", "Cpl photo"),
    checklist_row(True, "Bio", "Two sentences", "Cpl bio"),
    checklist_row(True, "Specialisation and languages", "Cardiology, internal medicine · English", "Cpl spec"),
    checklist_row(False, "Two more languages", "Hausa and Igbo would reach 40% more searches in Abuja", "Cpl langs"),
    checklist_row(False, "A photo of where you practise", "Members are more likely to book somewhere they can picture", "Cpl clinic"),
], footer="Pilot observation, not a promise: complete profiles get roughly twice the bookings of 60% ones.")

S1_LINKS = dgroup("Practice settings", [
    drow(ic, label, name=nm) for ic, label, nm in SETTINGS_NAV[1:]
], footer="Everything the desktop keeps in the right-hand rail. Nothing here is desktop-only.")

S1_SIGNOUT = dbtn("Sign out", "Sign out", "log-out", "ghost", full=True)

addx("Practice", "S1-profile",
    dr_desk("Doctor · Practice — S1 Public Profile", ["Settings", "Public profile"],
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("What patients",False),("see",True)],26)}'
        f'{dbtn("Save changes","Save profile S1","check","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S1_PROFILE}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{S1_COMPLETE}{S1_PUBLIC}</Frame></Frame>',
        NAV["Settings"], PANEL_SETTINGS, urgent=0, badges=BADGES),
    dr_head("Public profile", "Cardiologist · MDCN 71482", back=False,
            stats=[("85%", "Complete"), ("4.9", "Rating"), ("1,204", "Patients")],
            right=f'<Frame name="Btn Save profile S1" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("check",17,W_IC)}</Frame>'),
    pinned=S1_COMPLETE,
    sections=[
      ("edit", "pencil", "Edit your profile", "Photo, bio, specialisation, languages", None, None,
       f'{S1_PROFILE}{dcta("Save changes","Save profile S1","check")}', None),
      ("public", "eye", "How members see you", "4.9 from 148 visits · 61% come back", None, "ok",
       S1_PUBLIC, [("4.9", "Rating"), ("6 min", "Wait"), ("61%", "Return")]),
      ("links", "settings", "Practice settings", "Fees, virtual visits, payouts, security", "7", None,
       f'{S1_LINKS}{S1_SIGNOUT}', None),
    ],
    tab=MTAB["More"])

# ---------------- S2 types and fees
def fee_card(title, mins, price, desc, name, on=True, virtual=True, inperson=True):
    sw = (f'<Frame name="Btn Toggle {name}" w={{42}} h={{24}} rounded={{999}} image="assets/img/btn-teal.jpg" '
          f'overflow="hidden" flex="row" justify="end" items="center" px={{3}}><Ellipse w={{18}} h={{18}} bg="#FFFFFF" /></Frame>'
          if on else
          f'<Frame name="Btn Toggle {name}" w={{42}} h={{24}} rounded={{999}} bg="var:neutral/300" '
          f'flex="row" justify="start" items="center" px={{3}}><Ellipse w={{18}} h={{18}} bg="#FFFFFF" /></Frame>')
    modes = ""
    for label, ic, active in (("In person", "hospital", inperson), ("Virtual", "video", virtual)):
        bg = 'bg="var:state/info-bg"' if active else 'bg="var:neutral/100"'
        col = "var:text/default" if active else "var:text/faint"
        modes += (f'<Frame name="Btn Mode {name} {label}" flex="row" gap={{5}} items="center" px={{9}} py={{5}} '
                  f'rounded={{8}} {bg}>{I(ic,11,A_IC if active else M_IC)}{T(10,"medium",col,label)}</Frame>')
    return dcard(
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame flex="col" gap={{3}}>{T(15,"semibold","var:text/strong",title)}'
        f'{T(11,"regular","var:text/muted",desc)}</Frame>{sw}</Frame>'
        + f'<Frame w="fill" flex="row" gap={{9}}>'
        + f'<Frame grow={{1}} flex="col" gap={{2}} items="center" py={{11}} rounded={{12}} bg="var:bg/subtle">'
        + T(15, "bold", "var:text/strong", mins) + T(10, "regular", "var:text/muted", "minutes") + '</Frame>'
        + f'<Frame grow={{1}} flex="col" gap={{2}} items="center" py={{11}} rounded={{12}} bg="var:bg/subtle">'
        + T(15, "bold", "var:text/strong", price) + T(10, "regular", "var:text/muted", "per consultation") + '</Frame></Frame>'
        + f'<Frame w="fill" flex="row" gap={{7}} items="center">{modes}<Frame grow={{1}} />'
        + dbtn("Edit", "Edit " + name, "pencil", "ghost", grow=False, size="sm") + '</Frame>', p=15)

S2_TYPES = (fee_card("First visit", "45", "₦20,000", "New patients — more time to take a history", "Fee first")
            + fee_card("Follow-up", "30", "₦15,000", "Someone you have seen before", "Fee followup")
            + fee_card("Quick video review", "15", "₦8,000", "Results, prescriptions, short questions", "Fee quick", inperson=False)
            + fee_card("Home visit", "60", "₦45,000", "Within 10 km of Garki", "Fee home", on=False, virtual=False))

S2_MONEY = dgroup("What you actually receive", [
    earn_row("Consultation fee", "What the member pays before the visit", "₦15,000"),
    earn_row("Payment processing", "Paystack, deducted at source", "− ₦225", "muted"),
    earn_row("You receive", "Paid out every Friday", "₦14,775", "ok"),
], footer="Medra earns from your practice subscription, not from a cut of your consultation. See Subscription and billing.")

S2_RULES = dgroup("Fee rules", [
    drow("banknote", "Payment is taken", value="Before the visit", sub="A booking is not confirmed until it clears", name="Fee when", chevron=False),
    drow("undo-2", "Cancelled by the member", value="Full refund", sub="If more than 4 hours before", name="Fee refund", chevron=False),
    drow("circle-slash", "Did not arrive", value="You keep 50%", sub="Pilot policy, configurable per clinic", name="Fee noshow", chevron=False),
    drow("phone-off", "Video failed", value="Full refund", sub="Never the member's fault", name="Fee failed", chevron=False),
    drow("calendar-clock", "Late change by the member", value="₦2,000", sub="Inside 4 hours", name="Fee late", chevron=False),
], footer="Every one of these is shown to the member before they book. Nobody is surprised afterwards.")

addx("Practice", "S2-fees",
    dr_desk("Doctor · Practice — S2 Types &amp; Fees", ["Settings", "Types and fees"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Settings")}</Frame>'
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("What you offer,",False),("and for how much",True)],26)}'
        f'{dbtn("Add a type","Add fee type","plus","navy",grow=False,size="sm")}</Frame>'
        f'{T(14,"regular","var:text/muted","Each type has its own length, so your calendar blocks correctly. Members see the price before they book — never after.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S2_TYPES}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{S2_MONEY}'
        f'{alert_strip("info","Changing a fee never changes an existing booking","Anyone who has already paid keeps the price they paid.","info")}'
        f'{dcta("Save fees","Save fees S2","check")}</Frame></Frame>',
        NAV["Settings"], PANEL_SETTINGS, urgent=0, badges=BADGES),
    dr_head("Types and fees", "4 types · ₦8,000 to ₦45,000",
            stats=[("3", "Active"), ("₦15k", "Typical"), ("₦14,775", "You get")],
            right=f'<Frame name="Btn Add fee type" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("plus",17,W_IC)}</Frame>'),
    pinned=S2_TYPES,
    sections=[
      ("money", "wallet", "What you actually receive", "₦14,775 of a ₦15,000 follow-up", None, "ok",
       S2_MONEY, None),
      ("rules", "scale", "Fee rules", "Refunds, no-shows, late changes", "5", None,
       S2_RULES, None),
    ],
    foot=dcta("Save fees", "Save fees S2", "check"),
    tab=MTAB["More"])

# ---------------- S3 virtual visits
S3_PROVIDER = dgroup("Which app do you use?", [
    radio_row("Google Meet", sub="A fresh link is created for every appointment", on=True, name="Provider meet"),
    radio_row("Zoom", sub="Your personal room, or a new link per visit", name="Provider zoom"),
    radio_row("Microsoft Teams", name="Provider teams"),
    radio_row("WhatsApp video", sub="Common in Nigeria, but it shows the patient your personal number", name="Provider whatsapp"),
    radio_row("I paste a link myself each time", sub="Slowest, works with anything", name="Provider manual"),
], footer="Medra does not host the call in the MVP. It creates the booking, takes the payment, delivers the link three ways, and keeps the note — the call itself is yours.")

S3_SETUP = dgroup("Your link", [
    field("Meeting link", "video", "meet.google.com/kfa-jrqz-nmo", ph=False, trailing=("copy", "Copy meet link"),
          helper="Sent one hour before, again ten minutes before, and again if they say they cannot find it."),
    dtoggle("refresh-cw", "New link for every appointment", sub="Safer — nobody wanders into someone else's consultation", on=True, name="New link each"),
    dtoggle("lock", "Wait in a lobby until I admit them", sub="Strongly recommended", on=True, name="Lobby on"),
    dtoggle("phone-call", "Offer a phone call if the video fails", sub="The clinic rings the number they registered", on=True, name="Phone fallback"),
    dtoggle("signal", "Warn me when their connection is poor", sub="Before you both waste five minutes", on=True, name="Signal warn"),
])

S3_TEST = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("circle-check",16,OK_IC)}'
    f'{T(14,"semibold","var:text/strong","Link tested and working")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Checked 2 minutes ago. Medra tests it before every virtual appointment and warns you the moment it breaks.", w="fill")
    + dbtn("Test it again now", "Test link S3", "refresh-cw", "ghost", full=True, size="sm"),
    bg="var:state/success-bg", stroke=None)

S3_PHASE2 = dgroup("Coming later", [
    drow("sparkles", "Video inside Medra", sub="No third-party app, and no link to send", name="Phase2 video", chevron=False),
    drow("type", "Automatic transcription", sub="Medra drafts the note as you talk; you edit and sign", name="Phase2 transcribe", chevron=False),
    drow("shield-check", "Consent recorded first", sub="Nothing is transcribed without the member agreeing on screen", name="Phase2 consent", chevron=False),
], footer="Phase 2. The member-side designs already exist — ask to see them.")

addx("Practice", "S3-virtual",
    dr_desk("Doctor · Practice — S3 Virtual Visits", ["Settings", "Virtual visits"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Settings")}</Frame>'
        f'{dhead([("How your video",False),("visits happen",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S3_PROVIDER}{S3_SETUP}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{S3_TEST}{S3_PHASE2}'
        f'{dcta("Save","Save virtual S3","check")}</Frame></Frame>',
        NAV["Settings"], PANEL_SETTINGS, urgent=0, badges=BADGES),
    dr_head("Virtual visits", "Google Meet · tested 2 min ago",
            stats=[("Meet", "Provider"), ("On", "Lobby"), ("3", "Delivery routes")],
            right=f'<Frame name="Btn Save virtual S3" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("check",17,W_IC)}</Frame>'),
    pinned=S3_TEST,
    sections=[
      ("provider", "video", "Which app do you use?", "Google Meet · a fresh link each visit", "5", None,
       S3_PROVIDER, None),
      ("setup", "settings", "Your link and its rules", "Lobby, phone fallback, signal warning", "5", None,
       S3_SETUP, None),
      ("later", "sparkles", "Coming later", "Video inside Medra, and transcription", "3", None,
       S3_PHASE2, None),
    ],
    foot=dcta("Save", "Save virtual S3", "check"),
    tab=MTAB["More"])

# ---------------- S4 contact channels
S4_CHANNELS = dgroup("How patients can reach you between visits", [
    dtoggle("message-circle", "WhatsApp", sub="+234 803 555 0110 — the number most people will actually use", on=True, name="Contact whatsapp"),
    dtoggle("mail", "Work email", sub="dr.okafor@clinic.ng", on=True, name="Contact email"),
    dtoggle("phone-call", "Phone call", sub="They can ring you directly", on=False, name="Contact phone"),
    dtoggle("message-square-text", "Messages inside Medra", sub="Kept with the patient's record — the only channel that is", on=True, name="Contact inapp"),
], footer="Only patients you have actually consulted see these. Turn one off and it disappears from their screen immediately.")

S4_LIMITS = dgroup("Protect your evenings", [
    drow("clock", "Show as available", value="08:00 – 18:00", sub="Outside this, patients see “replies tomorrow”", name="Contact hours"),
    drow("calendar-days", "Days", value="Monday to Saturday", name="Contact days"),
    dtoggle("moon", "Do not disturb outside those hours", sub="Messages still arrive, they just do not ring", on=True, name="Contact dnd"),
    drow("triangle-alert", "What counts as urgent", sub="Chest pain, breathlessness, bleeding — these always ring through", name="Contact urgent"),
    drow("timer", "Auto-reply when you are consulting", value="On", sub="“In clinic — I will reply this evening”", name="Contact autoreply"),
], footer="Medra tells patients plainly that these channels are not for emergencies, and shows them what to do instead.")

S4_PREVIEW = dcard(
    eyerow("How it looks on her phone")
    + T(15, "bold", "var:text/strong", "Contact Dr. Okafor")
    + drow("message-circle", "WhatsApp", sub="Usually replies within a few hours", name="Prev whatsapp")
    + drow("mail", "Email", sub="dr.okafor@clinic.ng", name="Prev email")
    + note("triangle-alert", "For chest pain, breathlessness or bleeding, do not message — go to the nearest emergency department or call 112.", "warn"))

addx("Practice", "S4-contact",
    dr_desk("Doctor · Practice — S4 Contact Channels", ["Settings", "How patients reach me"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Settings")}</Frame>'
        f'{dhead([("Reachable, but",False),("on your terms",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S4_CHANNELS}{S4_LIMITS}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{S4_PREVIEW}{dcta("Save","Save contact S4","check")}</Frame></Frame>',
        NAV["Settings"], PANEL_SETTINGS, urgent=0, badges=BADGES),
    dr_head("How patients reach me", "3 channels on",
            stats=[("3", "Channels"), ("08–18", "Hours"), ("On", "Do not disturb")],
            right=f'<Frame name="Btn Save contact S4" w={{38}} h={{38}} rounded={{12}} bg="#17324D" flex="col" justify="center" items="center">{I("check",17,W_IC)}</Frame>'),
    pinned=S4_CHANNELS,
    sections=[
      ("limits", "moon", "Protect your evenings", "Hours, do-not-disturb, auto-reply", "5", None,
       S4_LIMITS, None),
      ("preview", "smartphone", "How it looks on her phone", "Including the emergency line", None, None,
       S4_PREVIEW, None),
    ],
    foot=dcta("Save", "Save contact S4", "check"),
    tab=MTAB["More"])

# ---------------- S5 earnings
S5_STATS = rows_of([
    stat_tile("banknote", "₦486,000", "Collected this month", "32 consultations", "teal", "Stat month"),
    stat_tile("wallet", "₦129,750", "Next payout", "Friday 22 August", "ok", "Stat payout"),
    stat_tile("trending-up", "+18%", "Vs last month", "More follow-ups", "ocean", "Stat trend"),
    stat_tile("circle-slash", "₦15,000", "Refunded", "1 cancellation by you", "warn", "Stat refund"),
], 4, 14)

S5_BREAKDOWN = dgroup("August so far", [
    earn_row("22 follow-ups", "₦15,000 each", "₦330,000"),
    earn_row("6 first visits", "₦20,000 each", "₦120,000"),
    earn_row("4 quick video reviews", "₦8,000 each", "₦32,000"),
    earn_row("1 no-show", "Blessing Ade, 14 Aug — you kept half", "₦7,500"),
    earn_row("1 refund", "You cancelled — Amara Okeke, 8 Aug", "− ₦15,000", "err"),
    earn_row("Payment processing", "Paystack, 1.5% capped", "− ₦7,290", "muted"),
    earn_row("Your total", "Before tax", "₦467,210", "ok"),
], footer="Medra reports what it pays you to FIRS. Keeping your own records is still your responsibility.")

S5_CHART = dgroup("Last six months", [
    chart([("Mar", "₦280k", 58, "slate"), ("Apr", "₦310k", 66, "slate"), ("May", "₦356k", 76, "navy"),
           ("Jun", "₦402k", 86, "navy"), ("Jul", "₦412k", 88, "ok"), ("Aug", "₦486k", 104, "ok")], 128, "Collected per month"),
])

S5_PAYOUTS = dgroup("Payouts", [
    drow("building-2", "Zenith Bank · ****4421", sub="Ngozi Okafor · verified 6 Feb", name="Payout account", tone="ok"),
    drow("calendar-days", "Every Friday", sub="Everything completed by Thursday midnight", name="Payout schedule"),
    drow("clock", "Held for", value="24 hours", sub="After a consultation is signed, in case of a dispute", name="Payout hold"),
    drow("download", "Download statements", sub="Monthly PDF and CSV", name="Payout statements"),
    drow("receipt", "Tax summary for the year", value="2026", name="Payout tax"),
    drow("history", "Payout history", value="14 payouts", name="Payout history"),
])

addx("Practice", "S5-earnings",
    dr_desk("Doctor · Practice — S5 Earnings", ["Money", "Earnings"],
        f'{dhead([("What you have",False),("earned",True)],26)}{S5_STATS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S5_CHART}{S5_BREAKDOWN}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{S5_PAYOUTS}'
        f'{alert_strip("wallet","Next payout ₦129,750 on Friday","Sent to Zenith ****4421. It usually lands the same day.","ok")}</Frame></Frame>',
        NAV["Money"], PANEL_MONEY, urgent=0, badges=BADGES),
    dr_head("Earnings", "August · ₦486,000 collected", back=False,
            stats=[("₦486k", "This month"), ("₦129.8k", "Next payout"), ("+18%", "Vs July")]),
    pinned=S5_CHART,
    sections=[
      ("breakdown", "receipt", "August so far", "32 consultations, one refund", None, None,
       S5_BREAKDOWN, [("32", "Visits"), ("₦486k", "Collected"), ("₦15k", "Refunded")]),
      ("payouts", "wallet", "Payouts and account", "Zenith ****4421 · every Friday", None, None,
       f'{S5_PAYOUTS}{dbtn("Statements","Payout statements","file-text","ghost",full=True,size="sm")}', None),
      ("billing", "credit-card", "Subscription and billing", "Free trial · 12 days left", None, "warn",
       f'{alert_strip("sparkles","Free trial · 12 days left","Your practice subscription starts on 26 August unless you cancel.","info",dbtn("See plans","Open billing S6",None,"navy",grow=False,size="sm"))}', None),
    ],
    tab=MTAB["More"])

# ---------------- S6 subscription (PRD §7 Module 8)
S6_TRIAL = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:brand/teal","FREE TRIAL")}{status_pill("pending","12 days left")}</Frame>'
    + T(26, "bold", "var:text/on-dark", "Your trial ends on 26 August")
    + T(14, "regular", "var:text/on-dark-muted",
        "Everything is unlocked until then. Add a card before the 26th and nothing changes; do not, and your dashboard locks while your patients keep their records.", w="fill")
    + bar(60, "teal", 10)
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Add a card now", "Add card S6", "credit-card", "teal")
    + dbtn("Compare plans", "Compare plans S6", "list-checks", "dark") + '</Frame>',
    bg="var:bg/band", stroke=None, p=22, r=18)

def plan_card(name, price, sub, feats, sel=False, badge=None):
    bd = "var:border/accent" if sel else "var:border/subtle"
    bw = 2 if sel else 1
    b = (f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="var:state/info-bg">'
         f'{T(10,"semibold","var:text/accent",badge)}</Frame>') if badge else ''
    return dcard(
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{T(15,"semibold","var:text/strong",name)}{b}</Frame>'
        + f'<Frame flex="row" gap={{5}} items="end">{T(26,"bold","var:text/strong",price)}'
        + T(12, "regular", "var:text/muted", "/month") + '</Frame>'
        + T(11, "regular", "var:text/muted", sub, w="fill") + hr()
        + "".join(f'<Frame w="fill" flex="row" gap={{8}} items="start" py={{4}}>{I("check",13,OK_IC)}'
                  f'{T(12,"regular","var:text/default",f,w="fill")}</Frame>' for f in feats)
        + dbtn("Choose " + name, "Choose " + name, None, "navy" if sel else "ghost", full=True, size="sm"),
        p=16, stroke=bd, sw=bw)

S6_PLAN_CARDS = [
    plan_card("Solo", "₦12,000", "One practitioner, one location",
              ["Unlimited bookings", "Records and notes", "SMS and WhatsApp to patients", "Weekly payouts"]),
    plan_card("Practice", "₦28,000", "One practitioner, up to 3 locations",
              ["Everything in Solo", "Recalls and follow-up lists", "Templates and shared templates", "Insights and reviews"],
              sel=True, badge="RECOMMENDED"),
    plan_card("Group", "₦75,000", "Up to 5 practitioners under one account",
              ["Everything in Practice", "Shared patient list", "Cover for a colleague", "One invoice"]),
]
S6_PLANS   = rows_of(S6_PLAN_CARDS, 3, 14)
S6_PLANS_M = rows_of(S6_PLAN_CARDS, 1, 12)

S6_INVOICES = dgroup("Invoices", [
    drow("receipt", "August 2026", value="₦0", sub="Free trial", name="Inv aug", chevron=False),
    drow("receipt", "Card on file", value="None yet", sub="Add one before 26 August", name="Add card S6", tone="warn"),
    drow("download", "Download invoices", sub="PDF, for your accountant", name="Inv download"),
    drow("building-2", "Billing details", sub="Name, address and TIN for the invoice", name="Inv details"),
])

S6_WHAT = dgroup("What happens if you do not subscribe", [
    drow("lock", "Your dashboard locks", sub="No queue, no new bookings, no note writing", name="Lock dash", tone="err", chevron=False),
    drow("clipboard-list", "Your patients keep their records", sub="Everything you signed stays theirs — that is not held hostage", name="Lock records", tone="ok", chevron=False),
    drow("calendar-x", "Bookings already made are honoured", sub="You can still see anyone who booked before the lock", name="Lock booked", chevron=False),
    drow("undo-2", "Unlock any time", sub="Add a card and everything comes back exactly as it was", name="Lock undo", chevron=False),
], footer="A doctor's unpaid invoice must never cost a patient their medical history. That is a design rule, not a policy setting.")

addx("Practice", "S6-billing",
    dr_desk("Doctor · Practice — S6 Subscription", ["Money", "Subscription and billing"],
        f'{S6_TRIAL}'
        f'{T(15,"bold","var:text/strong","Plans")}{S6_PLANS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S6_INVOICES}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{S6_WHAT}</Frame></Frame>',
        NAV["Money"], PANEL_MONEY, urgent=0, badges=BADGES),
    dr_head("Subscription", "Free trial · 12 days left", back=False,
            stats=[("12", "Days left"), ("₦28k", "Recommended"), ("None", "Card")]),
    pinned=S6_TRIAL,
    sections=[
      ("plans", "layers", "Plans", "Solo, Practice and Group", "3", None,
       S6_PLANS_M, None),
      ("invoices", "receipt", "Invoices", "Nothing charged yet", None, None,
       S6_INVOICES, None),
      ("what", "info", "What a subscription covers", "And what happens if it lapses", None, None,
       S6_WHAT, None),
    ],
    tab=MTAB["More"])

# ---------------- S7 where I practise
S7_PLACES = dgroup("Where you see patients", [
    drow("hospital", "Garki Medical Centre", value="Primary", sub="Area 3, Garki · Mon, Tue, Thu · you are staff here", name="Place garki", tone="ok"),
    drow("hospital", "Maitama Specialist", value="Visiting", sub="Wednesdays · you are a visiting consultant", name="Place maitama"),
    drow("video", "Virtual only", value="Anywhere", sub="Saturdays 10:00 – 14:00", name="Place virtual"),
    drow("plus", "Add somewhere else", name="Place add", chevron=False),
], footer="Members see which location a slot is at before they book, and get directions to the right one.")

S7_FACILITY = dgroup("Your link with Garki Medical Centre", [
    drow("building-2", "Facility admin", value="Yusuf Bello", sub="Medical Director · he manages staff and billing", name="Fac admin", chevron=False),
    drow("shield-check", "What the facility can see", sub="Your schedule and appointment counts. Not your consultation notes.", name="Fac sees", chevron=False),
    drow("banknote", "Who is paid", value="You directly", sub="Garki invoices you for rooms separately — Medra is not involved", name="Fac paid", chevron=False),
    drow("users", "Cover arrangements", sub="Dr. Chuka Eze can be offered your patients when you are away", name="Fac cover"),
    drow("log-out", "Leave this facility", sub="Your patients and records stay with you", name="Fac leave", tone="warn"),
], footer="An independent practitioner can ignore all of this. Medra works either way — that is what §11.4 of the PRD asks for.")

S7_MODE = dgroup("How you practise", [
    radio_row("Independent practitioner", sub="You are your own practice. You keep everything.", name="Mode indep"),
    radio_row("Attached to a facility", sub="Garki Medical Centre manages your rooms; Medra manages your bookings", on=True, name="Mode facility"),
    radio_row("Both", sub="Facility on some days, independent on others", name="Mode both"),
])

addx("Practice", "S7-practice",
    dr_desk("Doctor · Practice — S7 Where I Practise", ["Settings", "Where I practise"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Settings")}</Frame>'
        f'{dhead([("Where you",False),("see patients",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S7_MODE}{S7_PLACES}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{S7_FACILITY}{dcta("Save","Save practice S7","check")}</Frame></Frame>',
        NAV["Settings"], PANEL_SETTINGS, urgent=0, badges=BADGES),
    dr_head("Where I practise", "2 locations + virtual",
            stats=[("2", "Locations"), ("1", "Facility"), ("Sat", "Virtual only")]),
    pinned=S7_MODE,
    sections=[
      ("places", "hospital", "Your locations", "Garki, Maitama, and virtual", "3", None,
       S7_PLACES, None),
      ("facility", "building-2", "What the facility can see", "And what it cannot", None, None,
       S7_FACILITY, None),
    ],
    foot=dcta("Save", "Save practice S7", "check"),
    tab=MTAB["More"])

# ---------------- S8 account and security
S8_DEVICES = dgroup("Where you are signed in", [
    drow("laptop", "Windows laptop · Chrome", value="This device", sub="Garki Medical Centre · active now", name="Dev laptop", tone="ok", chevron=False),
    drow("smartphone", "iPhone 13", sub="Abuja · last used 40 minutes ago", name="Dev phone",
         right=dbtn("Sign out", "Signout phone", None, "ghost", grow=False, size="sm")),
    drow("monitor", "Clinic desktop · reception", sub="Shared machine — last used yesterday", name="Dev clinic", tone="warn",
         right=dbtn("Sign out", "Signout clinic", None, "ghost", grow=False, size="sm")),
], footer="A shared clinic machine should never stay signed in. Medra signs you out of one automatically after 15 minutes idle.")

S8_SECURITY = dgroup("Getting in", [
    drow("key", "Password", value="Changed 4 Feb", name="Sec password"),
    dtoggle("shield-check", "Two-factor on a new device", sub="Required — a doctor account opens medical records", on=True, name="Sec 2fa"),
    dtoggle("fingerprint", "Fingerprint on my phone", on=True, name="Sec bio"),
    dtoggle("timer", "Sign me out after 15 minutes idle", sub="On a shared machine this is not optional", on=True, name="Sec idle"),
    dtoggle("bell", "Tell me when someone signs in", sub="WhatsApp and email", on=True, name="Sec alert"),
])

S8_AUDIT = dgroup("Recent activity", [
    audit_row("Signed in", "Chrome · Windows · Garki Medical Centre", "Today, 07:58"),
    audit_row("Opened a record", "Amara Okeke · MDR-8842-19", "Today, 09:12"),
    audit_row("Signed a note", "Fatima Bello · MDR-2201-13", "Today, 09:28"),
    audit_row("Sign-in blocked", "Unknown device · Lagos · wrong code", "8 Aug, 23:14"),
], footer="Everything you do with a patient record is logged with your name — and the patient can see the part that concerns them.")

S8_DANGER = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("triangle-alert",16,ERR_IC)}'
    f'{T(14,"semibold","var:state/error","Leaving Medra")}</Frame>'
    + T(12, "regular", "var:text/default",
        "You can pause your listing and keep everything, or close the account. Notes you have signed stay with the patient and with the clinic — they are not yours to withdraw.", w="fill")
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Pause my listing", "Pause listing", "moon", "ghost")
    + dbtn("Close my account", "Close account", "trash-2", "danger") + '</Frame>',
    bg="var:state/error-bg", stroke=None)

addx("Practice", "S8-security",
    dr_desk("Doctor · Practice — S8 Account &amp; Security", ["Settings", "Account and security"],
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Settings")}</Frame>'
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Your account,",False),("and who can use it",True)],26)}'
        f'<Frame name="Btn Sign out all" flex="row" gap={{7}} items="center" px={{13}} py={{9}} rounded={{11}} bg="var:state/error-bg">'
        f'{I("log-out",14,ERR_IC)}{T(12,"semibold","var:state/error","Sign out everywhere")}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{S8_DEVICES}{S8_AUDIT}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{S8_SECURITY}{S8_DANGER}</Frame></Frame>',
        NAV["Settings"], PANEL_SETTINGS, urgent=0, badges=BADGES),
    dr_head("Account and security", "3 devices signed in",
            stats=[("3", "Devices"), ("On", "2FA"), ("15m", "Idle timeout")]),
    pinned=S8_DEVICES,
    sections=[
      ("security", "shield-check", "Sign-in and security", "2FA on · 15-minute idle timeout", None, None,
       S8_SECURITY, None),
      ("audit", "history", "Who opened what", "Every record you touch is logged", None, None,
       S8_AUDIT, None),
      ("danger", "triangle-alert", "Leaving Medra", "Export or close your account", None, "err",
       S8_DANGER, None),
    ],
    foot=dbtn("Sign out everywhere", "Sign out all", "log-out", "ghost", full=True),
    tab=MTAB["More"])

# =====================================================================================
# 6. GROWTH — the AARRR screens a supply side actually needs
# =====================================================================================
R_LINKS = dgroup("Grow your practice", [
    drow("share-2", "My booking link", sub="13 of 34 bookings came from it", name="Open link R3"),
    drow("user-plus", "Invite a colleague", sub="₦10,000 off each, after their first month", name="Open invite G3"),
    drow("circle-user", "My public profile", value="85%", sub="What patients see before booking", name="Open profile S1"),
    drow("star", "Ratings and reviews", value="4.9", sub="1 review waiting on a reply", name="Open reviews R2"),
], footer="The desktop keeps these in the right-hand rail. On a phone they live here.")

R1_STATS = rows_of([
    stat_tile("eye", "486", "Profile views", "Last 30 days · +22%", "info", "Ins views"),
    stat_tile("calendar-check", "32", "Booked", "6.6% of views", "teal", "Ins booked"),
    stat_tile("repeat", "61%", "Came back", "Pilot average is 43%", "ok", "Ins repeat"),
    stat_tile("circle-slash", "3%", "No-show rate", "Pilot average is 11%", "ok", "Ins noshow"),
], 4, 14)

R1_FUNNEL = dgroup("From search to signed note", [
    progress_row("Appeared in a search", "1,840", 100, "navy"),
    progress_row("Opened your profile", "486", 44, "navy"),
    progress_row("Started a booking", "58", 20, "teal"),
    progress_row("Paid and confirmed", "34", 14, "teal"),
    progress_row("Attended", "33", 13, "mint"),
    progress_row("Signed note within a day", "31", 12, "mint"),
], footer="The two biggest losses are search → profile and profile → booking. Both are profile problems, not clinical ones.")

R1_WHY = dgroup("What is costing you bookings", [
    drow("languages", "You only list English", value="−40% reach", sub="Hausa and Igbo are the two most searched in Abuja", name="Fix langs", tone="warn"),
    drow("clock", "No slots before 09:00 or after 17:00", value="−18%", sub="07:00 and 19:00 are the most searched times", name="Fix hours", tone="warn"),
    drow("camera", "No photo of your clinic", value="−9%", sub="Members book somewhere they can picture", name="Fix photo"),
    drow("video", "Virtual only on Saturday", value="−12%", sub="Video visits are booked three times as often as in-person", name="Fix virtual", tone="warn"),
], footer="Observations from the pilot cohort, not promises. Every one is a setting you control.")

R1_TIME = dgroup("When people look for you", [
    chart([("6am", "12", 22, "slate"), ("9am", "68", 74, "navy"), ("12pm", "51", 58, "navy"),
           ("3pm", "44", 50, "navy"), ("6pm", "89", 96, "ok"), ("9pm", "62", 68, "ok")], 120, "Searches by hour"),
], footer="Most searches happen after work — when you have no open slots.")

addx("Growth", "R1-insights",
    dr_desk("Doctor · Growth — R1 Insights", ["Growth", "Insights"],
        f'{dhead([("Where your bookings",False),("come from",True)],26)}'
        f'{T(14,"regular","var:text/muted","Thirty days. The point of this screen is the four fixable things on the right.",w="fill")}'
        f'{R1_STATS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{R1_FUNNEL}{R1_TIME}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{R1_WHY}'
        f'{dcta("Open more evening slots","Open availability K7","clock")}</Frame></Frame>',
        NAV["Growth"], PANEL_GROWTH, urgent=0, badges=BADGES),
    dr_head("Insights", "Last 30 days", back=False,
            stats=[("486", "Views"), ("32", "Booked"), ("6.6%", "Conversion")]),
    pinned=R1_FUNNEL,
    sections=[
      ("why", "wrench", "Four things costing you bookings", "All four are settings, not effort", "4", "warn",
       R1_WHY, None),
      ("when", "clock", "When people look for you", "Evenings and Saturday mornings", None, None,
       f'{R1_TIME}{R1_STATS}', None),
      ("grow", "trending-up", "Grow your practice", "Booking link, invitations, ratings", "4", None,
       R_LINKS, None),
    ],
    foot=dcta("Open more evening slots", "Open availability K7", "clock"),
    tab=MTAB["More"])

# ---------------- R2 reviews
R2_SUMMARY = dcard(
    f'<Frame w="fill" flex="row" gap={{20}} items="center">'
    f'<Frame flex="col" gap={{4}} items="center">{T(40,"bold","var:text/strong","4.9")}'
    f'<Frame flex="row" gap={{2}}>{"".join(I("star",13,"#E0A32E") for _ in range(5))}</Frame>'
    f'{T(11,"regular","var:text/muted","148 ratings")}</Frame>'
    f'<Frame grow={{1}} flex="col" gap={{6}}>'
    f'{progress_row("5 stars","131",89,"teal")}{progress_row("4 stars","12",8,"teal")}'
    f'{progress_row("3 stars","3",2,"amber")}{progress_row("2 stars","1",1,"red")}'
    f'{progress_row("1 star","1",1,"red")}</Frame></Frame>')

R2_SUMMARY_M = dcard(
    f'<Frame w="fill" flex="row" gap={{16}} items="center">'
    f'<Frame flex="col" gap={{3}} items="center">{T(34,"bold","var:text/strong","4.9")}'
    f'<Frame flex="row" gap={{2}}>{"".join(I("star",11,"#E0A32E") for _ in range(5))}</Frame>'
    f'{T(10,"regular","var:text/muted","148 ratings")}</Frame>'
    f'<Frame grow={{1}} flex="col" gap={{4}}>'
    f'{progress_row("5 stars","131",89,"teal")}{progress_row("4 stars","12",8,"teal")}'
    f'{progress_row("3 stars","3",2,"amber")}</Frame></Frame>')

R2_THEMES = dgroup("What people mention", [
    drow("message-square-text", "“Explained everything”", value="41 times", name="Theme explain", tone="ok", chevron=False),
    drow("clock", "“Did not keep me waiting”", value="28 times", name="Theme wait", tone="ok", chevron=False),
    drow("heart-handshake", "“Did not rush me”", value="22 times", name="Theme rush", tone="ok", chevron=False),
    drow("video", "“Video call kept dropping”", value="4 times", name="Theme video", tone="warn", chevron=False),
    drow("banknote", "“Expensive”", value="3 times", name="Theme price", chevron=False),
], footer="Pulled from the free-text comments. The video complaints all came from one week in June.")

R2_LIST = dgroup("Recent", [
    review_row(5, "“She explained everything and did not rush me. First doctor in Abuja who actually looked at my old results.”", "Verified visit · 12 Aug", "2 days ago"),
    review_row(5, "“Booked at 9pm, seen the next morning. My mother now uses her too.”", "Verified visit · 9 Aug", "5 days ago"),
    review_row(3, "“Good doctor but the video kept freezing and we had to move to a phone call.”", "Verified visit · 2 Aug",
               "12 days ago", reply="You replied: “Sorry about that — I have since switched to a new link for every call, which fixed it.”"),
    review_row(5, "“Sent my prescription straight to the pharmacy. I did not have to go back to the clinic at all.”", "Verified visit · 28 Jul", "3 weeks ago"),
], footer="Only a member with a completed, paid visit can leave a rating. Nobody can review a doctor they never saw.")

R2_RULES = dgroup("How ratings work", [
    drow("badge-check", "Verified visits only", sub="No anonymous drive-by reviews", name="Rev verified", chevron=False),
    drow("eye-off", "The rating is anonymous to you", sub="You see the words, not who wrote them", name="Rev anon", chevron=False),
    drow("corner-down-right", "You can reply once", sub="Publicly, under the review", name="Rev reply", chevron=False),
    drow("flag", "Report an unfair review", sub="A person reads it — abuse and identifying details are removed", name="Rev report"),
], footer="Medra does not delete a review because a doctor dislikes it. It removes abuse, and it removes anything that identifies a patient.")

addx("Growth", "R2-reviews",
    dr_desk("Doctor · Growth — R2 Ratings", ["Growth", "Ratings and reviews"],
        f'{dhead([("What patients",False),("say about you",True)],26)}'
        f'{R2_SUMMARY}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{R2_LIST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{R2_THEMES}{R_LINKS}</Frame></Frame>',
        NAV["Growth"], PANEL_GROWTH, urgent=0, badges=BADGES),
    dr_head("Ratings", "4.9 from 148 visits", back=False,
            stats=[("4.9", "Rating"), ("148", "Ratings"), ("1", "To reply")]),
    pinned=R2_SUMMARY_M,
    sections=[
      ("reviews", "message-circle", "What they wrote", "One is waiting on a reply", "4", "warn",
       R2_LIST, None),
      ("themes", "tags", "Recurring themes", "Pulled from 148 comments", "5", None,
       R2_THEMES, None),
      ("rules", "info", "How ratings work", "Who can rate, and what you can do about one", None, None,
       R2_RULES, None),
      ("grow", "trending-up", "Grow your practice", "Booking link, invitations, profile", "4", None,
       R_LINKS, None),
    ],
    tab=MTAB["More"])

# ---------------- R3 booking link and promotion
R3_LINK = dcard(
    eyerow("Your booking link")
    + f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{14}} py={{12}} rounded={{12}} bg="var:neutral/50">'
    + I("link", 15, M_IC) + T(13, "regular", "var:text/strong", "medra.ng/dr-ngozi-okafor", w="fill")
    + f'<Frame name="Btn Copy booking link" flex="row">{I("copy",15,N_IC)}</Frame></Frame>'
    + T(11, "regular", "var:text/muted",
        "Anyone with this link books straight into your calendar — no searching, no app store, works on any phone.", w="fill")
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Share on WhatsApp", "Share wa R3", "message-circle", "navy")
    + dbtn("Copy", "Copy booking link", "copy", "ghost") + '</Frame>')

R3_QR = dcard(
    f'<Frame w="fill" flex="col" gap={{12}} items="center">'
    f'<Frame w={{132}} h={{132}} rounded={{14}} bg="var:neutral/50" flex="col" justify="center" items="center">'
    f'{I("qr-code",76,N_IC)}</Frame>'
    f'{T(14,"semibold","var:text/strong","A poster for your waiting room")}'
    f'{T(11,"regular","var:text/muted","A4, your name, your QR code. Print it and put it on the wall — the cheapest acquisition channel you have.",w="fill",align="center")}'
    f'{dbtn("Download the poster","Download poster R3","printer","ghost",full=True,size="sm")}</Frame>')

R3_IMPORT = dgroup("Bring your existing patients across", [
    drow("upload", "Upload a list", sub="Name and phone number, CSV or a photo of your book", name="Import list"),
    drow("message-circle", "Invite them on WhatsApp", sub="One message each, with your booking link", name="Import wa"),
    drow("printer", "Give them a card at the desk", sub="Your QR code, wallet sized", name="Import card"),
    drow("hospital", "Ask reception to hand out the link", sub="Works for everyone who walks in", name="Import reception"),
], footer="Members you invite still choose whether to share their history with you. Importing a phone number does not import a record.")

R3_PERF = dgroup("Where your bookings came from", [
    kpi_line("Medra search", "18"),
    kpi_line("Your booking link", "9", "ok"),
    kpi_line("Waiting-room QR code", "4", "ok"),
    kpi_line("Referred by another doctor", "2"),
    kpi_line("Facility page", "1"),
], footer="Thirteen of thirty-four came from something you shared yourself.")

addx("Growth", "R3-link",
    dr_desk("Doctor · Growth — R3 Booking Link", ["Growth", "Booking link"],
        f'{dhead([("Send people",False),("straight to your calendar",True)],26)}'
        f'{T(14,"regular","var:text/muted","Search brings you strangers. Your own link brings you the patients you already have.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{R3_LINK}{R3_IMPORT}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{R3_QR}{R3_PERF}</Frame></Frame>',
        NAV["Growth"], PANEL_GROWTH, urgent=0, badges=BADGES),
    dr_head("Booking link", "13 of 34 bookings came from it", back=False,
            stats=[("9", "From link"), ("4", "From QR"), ("2", "Referred")]),
    pinned=R3_LINK,
    sections=[
      ("qr", "qr-code", "A poster for your waiting room", "A4, your name, your QR code", None, None,
       R3_QR, None),
      ("import", "upload", "Bring your patients across", "Upload a list, or invite on WhatsApp", "4", None,
       R3_IMPORT, None),
      ("perf", "chart-column", "Where your bookings came from", "13 of 34 from your own link", None, "ok",
       f'{R3_PERF}{dbtn("Open my booking page","Open link R3","external-link","ghost",full=True)}', None),
      ("grow", "trending-up", "Grow your practice", "Invitations, ratings, profile", "4", None,
       R_LINKS, None),
    ],
    tab=MTAB["More"])

# =====================================================================================
# 7. STATES & EDGE CASES
# =====================================================================================
X1_LOCK = dcard(
    f'<Frame w="fill" flex="col" gap={{13}} items="center">'
    f'<Frame w={{76}} h={{76}} rounded={{999}} bg="var:state/error-bg" flex="col" justify="center" items="center">'
    f'{I("lock",34,ERR_IC)}</Frame>'
    f'{T(22,"bold","var:text/strong","Your dashboard is locked")}'
    f'{T(14,"regular","var:text/muted","The free trial ended on 26 August and no card was added. Add one and everything comes back exactly as you left it.",w="fill",align="center")}'
    f'{dcta("Add a card and unlock","Add card S6","credit-card")}'
    f'{dbtn("Compare plans","Compare plans S6","list-checks","ghost",full=True)}</Frame>')

X1_STILL = dgroup("What still works", [
    drow("clipboard-list", "Your patients keep every record", sub="Everything you signed is theirs. It is not held hostage.", name="Lock records", tone="ok", chevron=False),
    drow("calendar-check", "Appointments already booked", value="4", sub="You can still see them and write the notes", name="Lock booked", tone="ok", chevron=False),
    drow("download", "Export your own data", sub="Patient list, notes you authored, earnings — any time", name="Lock export", tone="ok", chevron=False),
    drow("message-circle", "Messages from existing patients", sub="You can reply, so nobody is left mid-conversation", name="Lock messages", tone="ok", chevron=False),
])
X1_STOPPED = dgroup("What has stopped", [
    drow("search", "You are hidden from search", sub="Nobody new can find or book you", name="Stop search", tone="err", chevron=False),
    drow("calendar-x", "No new bookings", sub="Your open slots are withdrawn", name="Stop bookings", tone="err", chevron=False),
    drow("repeat", "Recalls and follow-up reminders", sub="Paused, not deleted", name="Stop recalls", tone="err", chevron=False),
    drow("trending-up", "Insights and reviews", name="Stop insights", tone="err", chevron=False),
], footer="Nothing is deleted. Unlock and every list, template and setting is where you left it.")

STATE_LIST = [("X1", "lock", "Subscription locked"), ("X2", "calendar-check", "Nothing booked"),
              ("X3", "bell", "Notifications"), ("X4", "cloud-off", "Offline"),
              ("X5", "triangle-alert", "Error"), ("X6", "loader", "Loading")]

def state_nav(active, per=6):
    """These screens appear because of a condition, not a tap. In a click-through that leaves
    most of them unreachable, so each one carries a switcher — the design-file equivalent of
    forcing the state. wrap is not honoured by the renderer, so the chips are chunked."""
    cells = []
    for code, ic, label in STATE_LIST:
        on = code == active
        st = ('image="assets/img/btn-navy.jpg" overflow="hidden"' if on
              else 'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}')
        col = "var:text/on-dark" if on else "var:text/muted"
        cells.append(f'<Frame name="Btn State {code}" flex="row" gap={{6}} items="center" px={{11}} py={{7}} '
                     f'rounded={{999}} {st}>{I(ic,12,W_IC if on else M_IC)}'
                     f'{T(11,"semibold" if on else "regular",col,label)}</Frame>')
    return (f'<Frame w="fill" flex="col" gap={{7}}>'
            f'{T(10,"semibold","var:text/faint","STATE — FOR REVIEW, NOT A REAL CONTROL")}'
            f'{rows_of(cells, per, 7)}</Frame>')

addx("States", "X1-locked",
    dr_desk("Doctor · States — X1 Subscription Locked", ["Money", "Subscription"],
        f'{state_nav("X1")}'
        f'<Frame w="fill" flex="row" gap={{16}} justify="center" items="start" pt={{10}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X1_LOCK}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{X1_STILL}{X1_STOPPED}</Frame></Frame>',
        NAV["Money"], PANEL_MONEY, urgent=0),
    dr_head("Locked", "Trial ended 26 August", back=False,
            stats=[("0", "New bookings"), ("4", "Still booked"), ("Safe", "Records")]),
    pinned=f'{state_nav("X1",3)}{X1_LOCK}',
    sections=[
      ("still", "circle-check", "What still works", "Records, booked visits, export, messages", "4", "ok",
       X1_STILL, None),
      ("stopped", "circle-x", "What has stopped", "Search, new bookings, recalls, insights", "4", "err",
       X1_STOPPED, None),
    ],
    tab=MTAB["More"])

X2_EMPTY = empty_state("calendar-check", "Nothing booked today",
    "Your hours are set and your profile is live. When someone books, they appear here and you get a notification.",
    primary=dcta("Open more slots", "Open availability K7", "clock"),
    secondary=dbtn("Share my booking link", "Open link R3", "share-2", "ghost", full=True), tone="ok")

X2_WHY = dgroup("Getting booked more", [
    drow("clock", "Open earlier or later slots", sub="07:00 and 19:00 are the two most-searched times in Abuja", name="Open availability K7"),
    drow("video", "Offer virtual visits on weekdays", sub="Members book three times as many video visits", name="Open fees S2"),
    drow("languages", "Add Hausa and Igbo", sub="You are invisible to 40% of searches in your area", name="Open profile S1"),
    drow("share-2", "Send your link to existing patients", sub="Nine of last month's bookings came from it", name="Open link R3"),
    drow("user-plus", "Invite a colleague", sub="Their referrals come back to you", name="Open invite G3"),
], footer="Pilot observations, not promises.")

X2_WEEK = dgroup("The rest of your week", [
    drow("calendar-check", "Friday", value="2 booked", sub="09:00 and 11:30", name="Open week K6"),
    drow("calendar-check", "Saturday", value="Fully open", sub="6 virtual slots, nobody has taken one", name="Open week K6", tone="warn"),
    drow("calendar-x", "Monday", value="Blocked", sub="You marked it as leave", name="Open timeoff K8"),
])

addx("States", "X2-empty",
    dr_desk("Doctor · States — X2 Nothing Booked", ["Today", "Nothing booked"],
        f'{state_nav("X2")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X2_EMPTY}{X2_WEEK}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{X2_WHY}</Frame></Frame>',
        NAV["Today"], PANEL_TODAY, urgent=0),
    dr_head("Thursday 14 Aug", "Nothing booked today", back=False,
            stats=[("0", "Today"), ("2", "Friday"), ("6", "Open Saturday")]),
    pinned=f'{state_nav("X2",3)}{X2_EMPTY}',
    sections=[
      ("week", "calendar-days", "The rest of the week", "Two on Friday, six open Saturday", None, None,
       X2_WEEK, None),
      ("why", "trending-up", "What actually gets you booked", "In the order that works", "5", None,
       X2_WHY, None),
    ],
    tab=MTAB["Today"])

X3_TODAY = (f'<Frame w="fill" flex="col" gap={{9}}>{eyerow("Today")}'
            f'{notif_row("flask-conical","Result back for Musa Ibrahim","Troponin normal. Release it or hold it until you speak.","12 min","Notif result",unread=True,tone="warn")}'
            f'{notif_row("calendar-clock","New booking request","Halima Sani · Fri 22 Aug 11:30 · paid","1 h","Notif booking",unread=True,tone="info")}'
            f'{notif_row("package","Refill request from Grace Okeke","Metformin 500 mg · she has 4 days left","1 h","Notif refill",unread=True,tone="info")}'
            f'{notif_row("calendar-x","Amara Okeke cancelled","Thu 28 Aug 10:30 — released back to your open slots","3 h","Notif cancel",unread=True,tone="muted")}'
            f'{notif_row("notebook-pen","Yesterday’s note is still unsigned","Chidi Okeke, 16:40. He cannot see it until you sign.","This morning","Notif unsigned",tone="warn")}</Frame>')
X3_EARLIER = (f'<Frame w="fill" flex="col" gap={{9}}>{eyerow("Earlier")}'
              f'{notif_row("message-square-text","Amara Okeke answered your request","She agreed to share her prescription history for this visit.","Tue","Notif access",tone="ok")}'
              f'{notif_row("banknote","₦129,750 paid out","Zenith ****4421 · 32 consultations","Fri","Notif payout",tone="ok")}'
              f'{notif_row("star","New rating: 5 stars","“She explained everything and did not rush me.”","Fri","Notif rating",tone="ok")}'
              f'{notif_row("user-plus","Dr. Chuka Eze accepted your invitation","Your free month is credited","28 Jul","Notif invite",tone="ok")}</Frame>')

X3_BLOCKING = dgroup("Blocking a patient right now", [
    drow("flask-conical", "1 result to release", name="Open results P7", tone="warn"),
    drow("package", "2 refills waiting", name="Open refills P6", tone="warn"),
    drow("notebook-pen", "1 unsigned note", name="Open drafts C9", tone="err"),
], footer="Everything else can wait until after clinic.")

X3_CHANNELS = dgroup("How you get told", [
    dtoggle("bell", "In the app", on=True, name="Dr notif app"),
    dtoggle("message-circle", "WhatsApp", sub="Urgent only — results, cancellations, new bookings", on=True, name="Dr notif wa"),
    dtoggle("message-square-text", "SMS", sub="When you have no data", on=False, name="Dr notif sms"),
    dtoggle("mail", "A daily email summary", sub="07:00, before clinic starts", on=True, name="Dr notif email"),
    dtoggle("moon", "Nothing between 21:00 and 07:00", sub="Except a cancellation for the next morning", on=True, name="Dr notif quiet"),
])

addx("States", "X3-notifications",
    dr_desk("Doctor · States — X3 Notifications", ["Requests", "Notifications"],
        f'{state_nav("X3")}'
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("What needs",False),("your attention",True)],26)}'
        f'{dbtn("Mark all read","Mark all read","check-check","ghost",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{16}}>{X3_TODAY}{X3_EARLIER}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{X3_BLOCKING}{X3_CHANNELS}</Frame></Frame>',
        NAV["Requests"], PANEL_REQ, urgent=6, badges=BADGES),
    dr_head("Notifications", "5 new · 4 blocking a patient", back=False,
            stats=[("5", "New"), ("4", "Blocking"), ("On", "WhatsApp")]),
    pinned=f'{state_nav("X3",3)}{X3_BLOCKING}{X3_TODAY}',
    sections=[
      ("earlier", "history", "Earlier", "Access replies, payouts, ratings", "4", None,
       X3_EARLIER, None),
      ("channels", "bell", "Where each one reaches you", "Push, WhatsApp, email, quiet hours", None, None,
       X3_CHANNELS, None),
    ],
    tab=MTAB["Requests"])

# ---------------- X4 offline
X4_BANNER = alert_strip("cloud-off", "You are offline",
    "Showing what was on this device at 09:41. Anything you write is saved here and syncs the moment you are back.", "warn",
    dbtn("Retry", "Retry X4", "refresh-cw", "ghost", grow=False, size="sm"))

X4_WORKS = dgroup("What still works", [
    drow("notebook-pen", "Writing a consultation note", sub="Saved on this device, synced later — you never lose a note to a dropped line", name="Off note", tone="ok", chevron=False),
    drow("clipboard-list", "Reading records you already opened", sub="Today's patients were cached at 09:41", name="Off records", tone="ok", chevron=False),
    drow("calendar-days", "Today's queue", sub="As it stood at 09:41", name="Off queue", tone="ok", chevron=False),
    drow("phone-call", "Phone numbers", sub="Every patient's number is on the device", name="Off phones", tone="ok", chevron=False),
])
X4_WAITS = dgroup("What has to wait", [
    drow("badge-check", "Signing a note", sub="A signature needs a trusted timestamp from the server", name="Off sign", tone="err", chevron=False),
    drow("pill", "Sending a prescription", sub="The pharmacy has to actually receive it", name="Off rx", tone="err", chevron=False),
    drow("eye", "Releasing a result", name="Off result", tone="err", chevron=False),
    drow("video", "Starting a video visit", name="Off video", tone="err", chevron=False),
], footer="Three notes are queued and will sync automatically. Nothing you have typed is at risk.")

X4_QUEUE = dgroup("Waiting to sync · 3", [
    drow("notebook-pen", "Chidi Okeke — consultation note", value="Draft", sub="Written 10:04, complete", name="Sync 1", chevron=False),
    drow("activity", "Grace Okeke — BP 148/92 recorded", value="Queued", sub="Written 10:22", name="Sync 2", chevron=False),
    drow("circle-slash", "Blessing Ade — marked no-show", value="Queued", sub="Written 10:12", name="Sync 3", chevron=False),
])

addx("States", "X4-offline",
    dr_desk("Doctor · States — X4 Offline", ["Today", "Offline"],
        f'{state_nav("X4")}'
        f'{X4_BANNER}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X4_WORKS}{X4_WAITS}</Frame>'
        f'<Frame w={{380}} flex="col" gap={{14}}>{X4_QUEUE}'
        f'{alert_strip("info","Records use about 40 MB on this device","Turn caching off in Account and security if the clinic machine is short on space.","info")}</Frame></Frame>',
        NAV["Today"], PANEL_STATES, urgent=0),
    dr_head("Offline", "Last synced 09:41", back=False,
            stats=[("3", "Queued"), ("09:41", "Synced"), ("8", "Cached")]),
    pinned=f'{state_nav("X4",3)}{X4_BANNER}{X4_QUEUE}',
    sections=[
      ("works", "circle-check", "What still works", "Writing a note, reading cached records", "4", "ok",
       X4_WORKS, None),
      ("waits", "clock", "What waits for the connection", "Signing, prescribing, releasing", "4", "warn",
       X4_WAITS, None),
    ],
    tab=MTAB["Today"])

# ---------------- X5 error
X5_MAIN = empty_state("triangle-alert", "Something went wrong on our side",
    "This is not your device and it is not your data — a Medra service failed to answer. Nothing you have written is affected.",
    primary=dcta("Try again", "Retry X5", "refresh-cw"),
    secondary=dbtn("Go to today's queue", "Nav Today", "layout-dashboard", "ghost", full=True), tone="warn")

X5_REF = dcard(
    f'<Frame w="fill" flex="row" gap={{11}} items="center">{I("copy",16,M_IC)}'
    f'<Frame grow={{1}} flex="col" gap={{2}}>{T(11,"regular","var:text/muted","Reference for support")}'
    f'{T(14,"semibold","var:text/strong","ERR-7731-A2 · 14 Aug 09:41 · notes-service")}</Frame>'
    f'{dbtn("Copy","Copy error ref","copy","ghost",grow=False,size="sm")}</Frame>')

X5_HELP = dgroup("If it keeps happening", [
    drow("refresh-cw", "Reload the app", name="Retry X5", chevron=False),
    drow("wifi", "Check the clinic network", sub="Medra needs about 1 Mbps to work properly", name="Err network", chevron=False),
    drow("message-square-text", "Message Medra with the reference", sub="Median reply 4 minutes during clinic hours", name="Open help"),
    drow("phone-call", "Call the clinic support line", value="+234 809 112 4477", name="Call clinic", chevron=False),
], footer="If a patient is in front of you and Medra is down, write on paper and add it afterwards — the note screen accepts a backdated entry.")

X5_SAFE = dgroup("What is safe", [
    drow("notebook-pen", "Your open note", value="Saved locally", sub="Auto-saved 40 seconds ago", name="Safe note", tone="ok", chevron=False),
    drow("badge-check", "Everything you have signed", sub="Signed notes are written before you see a confirmation", name="Safe signed", tone="ok", chevron=False),
    drow("banknote", "Payments already taken", sub="Held by Paystack, not by this service", name="Safe money", tone="ok", chevron=False),
])

addx("States", "X5-error",
    dr_desk("Doctor · States — X5 Error", ["Today", "Error"],
        f'{state_nav("X5")}'
        f'<Frame w="fill" flex="row" gap={{16}} justify="center" items="start" pt={{10}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X5_MAIN}{X5_REF}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{X5_SAFE}{X5_HELP}</Frame></Frame>',
        NAV["Today"], PANEL_STATES, urgent=0),
    dr_head("Something went wrong", "ERR-7731-A2", back=False,
            stats=[("Saved", "Your note"), ("Safe", "Signed"), ("4 min", "Support")]),
    pinned=f'{state_nav("X5",3)}{X5_MAIN}{X5_REF}',
    sections=[
      ("safe", "shield-check", "What is safe", "Everything you have written and signed", "4", "ok",
       X5_SAFE, None),
      ("help", "message-square-text", "If a patient is in front of you", "Write on paper, and reach us", None, None,
       X5_HELP, None),
    ],
    tab=MTAB["Today"])

# ---------------- X6 loading
X6_SKEL_D = (f'{skel(h=110,r=18)}'
             f'{rows_of([skel(h=104,r=16),skel(h=104,r=16),skel(h=104,r=16),skel(h=104,r=16)],4,14)}'
             f'<Frame w="fill" flex="row" gap={{16}} items="start">'
             f'<Frame grow={{1}} flex="col" gap={{12}}>{skel_card(3)}{skel_card(3)}{skel_card(2)}</Frame>'
             f'<Frame w={{360}} flex="col" gap={{12}}>{skel_card(4,avatar=False)}{skel_card(3,avatar=False)}</Frame></Frame>'
             f'<Frame w="fill" flex="row" gap={{9}} justify="center" items="center" pt={{4}}>'
             f'{I("loader",15,M_IC)}{T(12,"regular","var:text/muted","Loading today’s queue…")}</Frame>')
X6_SKEL_M = (f'{skel(h=104,r=16)}'
             f'{rows_of([skel(h=88,r=14),skel(h=88,r=14)],2,10)}'
             f'{skel_card(3)}{skel_card(3)}{skel_card(2)}'
             f'<Frame w="fill" flex="row" gap={{9}} justify="center" items="center">'
             f'{I("loader",14,M_IC)}{T(12,"regular","var:text/muted","Loading…")}</Frame>')

add("States", "X6-loading",
    dr_desk("Doctor · States — X6 Loading", ["Today", "Loading"],
        state_nav("X6") + X6_SKEL_D, NAV["Today"], PANEL_STATES, urgent=0),
    dr_mob("Doctor · States — X6 Loading · Mobile",
        dr_head("Thursday 14 Aug", "Loading…", back=False, stats=[("—", "Seen"), ("—", "Wait"), ("—", "Today")]),
        state_nav("X6", 3) + X6_SKEL_M, MTAB["Today"]))

# =====================================================================================
# 8. COMPONENT STATES
# =====================================================================================
CMP = []
def cmp_frame(comp, prop, value, body, w=320, h=None, dark=False):
    hh = f' minH={{{h}}}' if h else ''
    bg = "var:bg/band" if dark else "var:bg/base"
    CMP.append((f"cmp/{comp}/{prop}={value}",
        f'<Frame name="cmp/{comp}/{prop}={value}" w={{{w}}}{hh} flex="col" p={{16}} bg="{bg}">{body}</Frame>'))

for st, state in (("Open", "open"), ("Booked", "booked"), ("Held", "hold"), ("Break", "break"), ("Away", "blocked")):
    cmp_frame("Slot", "State", st, f'<Frame w="fill" flex="row">{slot_chip("10:30", state, "CSlot")}</Frame>', w=150)

cmp_frame("Queue Row", "State", "Waiting",
    queue_row("11:00", "avatar-6.jpg", "Chidi Okeke", "6 years · MDR-8842-20", "Cough for four days",
              "confirmed", "In person", "CQueue"), w=620)
cmp_frame("Queue Row", "State", "Now",
    queue_row("10:30", "avatar-2.jpg", "Amara Okeke", "34 years · MDR-8842-19", "Hypertension follow-up",
              "today", "Virtual", "CQueue", now=True,
              flags=[("triangle-alert", "Penicillin allergy", "err")]), w=620)
cmp_frame("Queue Row", "State", "Unpaid",
    queue_row("14:00", "avatar-5.jpg", "Tunde Bello", "44 years · MDR-6620-88", "Results discussion",
              "pending", "Virtual", "CQueue",
              flags=[("credit-card", "Unpaid — released 13:30", "warn")]), w=620)

for st, on in (("Shared", True), ("Withheld", False)):
    cmp_frame("Share Toggle", "State", st, share_toggle("Diagnosis", "CShare", on), w=340)
for st, granted in (("Granted", True), ("Locked", False)):
    cmp_frame("Scope Line", "State", st, scope_line("Lab results", granted, "4 results · 1 out of range"), w=380)
cmp_frame("Drug Result", "State", "Default",
    drug_result("Amlodipine", "Tablet · 5 mg, 10 mg", "Calcium channel blocker", "CDrug"), w=420)
cmp_frame("Drug Result", "State", "Blocked",
    drug_result("Amoxicillin", "Capsule · 250 mg", "Penicillin class", "CDrug", blocked=True), w=420)

for st, tone in (("Info", "info"), ("Warning", "warn"), ("Danger", "err"), ("Good", "ok")):
    cmp_frame("Stat Tile", "State", st,
              f'<Frame w="fill" flex="row">{stat_tile("users","8","Booked today","3 seen · 5 to go",tone,"CTile")}</Frame>', w=260)

cmp_frame("Checklist Row", "State", "Done",
    checklist_row(True, "Set your working hours", "Mon–Thu 09:00–17:00", "CCheck"), w=440)
cmp_frame("Checklist Row", "State", "Todo",
    checklist_row(False, "Connect your video link", "Needed for virtual bookings", "CCheck"), w=440)

cmp_frame("Outcome", "State", "Selected",
    outcome_choice("check-check", "Completed", "The note goes to their record and the fee is released.", "COut", sel=True, tone="ok"), w=440)
cmp_frame("Outcome", "State", "Default",
    outcome_choice("circle-slash", "Did not arrive", "The slot reopens and they are told.", "COut", tone="warn"), w=440)

def rail_item(on):
    box = ('bg="#17324D" stroke="#2B5B85" strokeWidth={1}' if on else '')
    return (f'<Frame w={{70}} flex="col" gap={{5}} items="center" py={{10}} rounded={{13}} {box}>'
            f'{I("calendar-days",20,RAIL_ON if on else RAIL_DIM)}'
            f'{T(9,"semibold" if on else "medium","var:text/on-dark" if on else "#7FA3BE","Schedule")}</Frame>')
cmp_frame("Rail Item", "State", "Active", rail_item(True), w=110, dark=True)
cmp_frame("Rail Item", "State", "Inactive", rail_item(False), w=110, dark=True)

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

NAVMAP = {
  "Btn Nav Today":     NAMES["K1-today"],
  "Btn Nav Requests":  NAMES["K2-requests"],
  "Btn Nav Schedule":  NAMES["K6-week"],
  "Btn Nav Patients":  NAMES["P1-patients"],
  "Btn Nav Consults":  NAMES["C1-room"],
  "Btn Nav Money":     NAMES["S5-earnings"],
  "Btn Nav Growth":    NAMES["R1-insights"],
  "Btn Nav Settings":  NAMES["S1-profile"],
  "Btn Notifications": NAMES["X3-notifications"],
  "Btn Search patient": NAMES["P1-patients"],
  "Btn Start consult": NAMES["C1-room"],
  "Btn Open help":     NAMES["X5-error"],
  "Btn Nav More":      NAMES["K9-more"],
}

TRN = [
 # ---- start
 ("G1-checklist","Btn Open verify G2","G2-verification"),("G1-checklist","Btn Open virtual S3","S3-virtual"),
 ("G1-checklist","Btn Step video","S3-virtual"),("G1-checklist","Btn Step contact","S4-contact"),
 ("G1-checklist","Btn Step payout","S5-earnings"),("G1-checklist","Btn Step hours","K7-availability"),
 ("G1-checklist","Btn Step fees","S2-fees"),("G1-checklist","Btn Step photo","S1-profile"),
 ("G1-checklist","Btn Do Step video","S3-virtual"),("G1-checklist","Btn Do Step contact","S4-contact"),
 ("G1-checklist","Btn Do Step payout","S5-earnings"),
 ("G2-verification","Btn Open profile S1","S1-profile"),("G2-verification","Btn Open virtual S3","S3-virtual"),
 ("G2-verification","Btn Open contact S4","S4-contact"),("G2-verification","Btn Open earnings S5","S5-earnings"),
 ("G2-verification","Btn Open help","X5-error"),
 ("G3-invite","Btn Send invite whatsapp","G3-invite"),("G3-invite","Btn Copy invite link","G3-invite"),
 # ---- today & schedule
 ("K1-today","Btn Open prep","K4-file"),("K1-today","Btn Start consult","C1-room"),
 ("K1-today","Btn Q Chidi","K4-file"),("K1-today","Btn Q Musa","K4-file"),
 ("K1-today","~Btn Q Grace","K4-file"),("K1-today","Btn Q Tunde","K4-file"),
 ("K1-today","Btn Open Q Chidi","K4-file"),("K1-today","Btn Open Q Musa","K4-file"),
 ("K1-today","~Btn Open Q Grace","K4-file"),("K1-today","~Btn Open Q Tunde","K4-file"),
 ("K1-today","Btn Open requests K2","K2-requests"),("K1-today","Btn Open week K6","K6-week"),
 ("K1-today","Btn Open results P7","P7-results"),("K1-today","Btn Open refills P6","P6-refills"),
 ("K1-today","Btn Open drafts C9","C9-drafts"),("K1-today","Btn Open late K3","K3-late"),
 ("K1-today","Btn Open timeoff K8","K8-timeoff"),("K1-today","Btn Open outcome K5","K5-outcome"),
 ("K1-today","Btn Open done 1","C8-signed"),("K1-today","Btn Open done 2","C8-signed"),
 ("K1-today","Btn Open slot 15","K6-week"),("K1-today","Btn Open slot 1530","K6-week"),
 ("K1-today","~Btn Open slot 16","K6-week"),("K1-today","Btn Offer waitlist","K6-week"),
 ("K2-requests","Btn Accept Musa","K1-today"),("K2-requests","Btn Decline Musa","K2-requests"),
 ("K2-requests","Btn Suggest Musa","K6-week"),("K2-requests","Btn Accept Halima","K1-today"),
 ("K2-requests","Btn Accept Emeka","K1-today"),("K2-requests","Btn Open refills P6","P6-refills"),
 ("K2-requests","Btn Open results P7","P7-results"),("K2-requests","Btn Open messages P5","P5-messages"),
 ("K2-requests","Btn Open patients P1","P1-patients"),("K2-requests","Btn Req Musa","K4-file"),
 ("K3-late","Btn Send late K3","K1-today"),("K3-late","Btn Back today K3","K1-today"),
 ("K3-late","Btn Late Chidi","K4-file"),("K3-late","Btn Late Musa","K4-file"),("K3-late","Btn Late Grace","K4-file"),
 ("K4-file","Btn Back","K1-today"),("K4-file","Btn Start consult","C1-room"),
 ("K4-file","Btn Open access P3","P3-access"),("K4-file","Btn Open record P2","P2-record"),
 ("K4-file","Btn Open note last","P2-record"),("K4-file","Btn Open virtual C10","C10-virtual"),
 ("K4-file","Btn Open tests C4","C4-tests"),("K4-file","Btn Open adherence","P2-record"),
 ("K4-file","Btn Test link S3","S3-virtual"),
 ("K5-outcome","Btn Save outcome K5","K1-today"),("K5-outcome","Btn Wait more K5","K1-today"),
 ("K6-week","Btn Open timeoff K8","K8-timeoff"),("K6-week","Btn Open availability K7","K7-availability"),
 ("K6-week","Btn Q Chidi","K4-file"),("K6-week","Btn Q Musa","K4-file"),
 ("K6-week","Btn Open Q Chidi","K4-file"),("K6-week","Btn Open Q Musa","K4-file"),
 ("K7-availability","Btn Save availability K7","K6-week"),("K7-availability","Btn Open fees S2","S2-fees"),
 ("K8-timeoff","Btn Back","K6-week"),("K8-timeoff","Btn Save timeoff K8","K6-week"),
 ("K8-timeoff","Btn Offer slots K8","K6-week"),
 ("K8-timeoff","Btn Move Amara","K4-file"),("K8-timeoff","Btn Move Chidi","K4-file"),
 ("K8-timeoff","Btn Move Musa","K4-file"),("K8-timeoff","Btn Move Grace","K4-file"),
 ("K8-timeoff","Btn Cover Chuka","K8-timeoff"),("K8-timeoff","Btn Cover Tunde","K8-timeoff"),
 # ---- consultation
 ("C1-room","Btn Open sign C7","C7-sign"),("C1-room","Btn Open prescribe C3","C3-prescribe"),
 ("C1-room","Btn Open tests C4","C4-tests"),("C1-room","Btn Open upload C5","C5-upload"),
 ("C1-room","Btn Open refer C6","C6-refer"),("C1-room","Btn Open followups P4","P4-followups"),
 ("C1-room","Btn Open virtual C10","C10-virtual"),("C1-room","Btn Open record P2","P2-record"),
 ("C1-room","Btn Side meds","P2-record"),("C1-room","Btn Side vitals","P2-record"),
 ("C1-room","Btn Side family","P1-patients"),
 ("C1-room","Btn Template complaint","C2-templates"),("C1-room","Btn Template exam","C2-templates"),
 ("C1-room","Btn Template diagnosis","C2-templates"),("C1-room","Btn Template plan","C2-templates"),
 ("C1-room","Btn Template comment","C2-templates"),
 ("C1-room","Btn Consult tab Prescription","C3-prescribe"),("C1-room","Btn Consult tab Tests","C4-tests"),
 ("C1-room","Btn Consult tab Files","C5-upload"),("C1-room","Btn Consult tab Referral","C6-refer"),
 ("C1-room","Btn Phase2 transcribe","C1-room"),
 ("C2-templates","Btn Back","C1-room"),("C2-templates","Btn Use template hyp","C1-room"),
 ("C2-templates","Btn Use template new","C1-room"),("C2-templates","Btn Use template discharge","C1-room"),
 ("C2-templates","Btn Use template fever","C1-room"),("C2-templates","Btn Use template diabetes","C1-room"),
 ("C3-prescribe","Btn Open sign C7","C7-sign"),("C3-prescribe","Btn Consult tab Note","C1-room"),
 ("C3-prescribe","Btn Consult tab Tests","C4-tests"),("C3-prescribe","Btn Override allergy","C3-prescribe"),
 ("C4-tests","Btn Open sign C7","C7-sign"),("C4-tests","Btn Consult tab Note","C1-room"),
 ("C5-upload","Btn Open sign C7","C7-sign"),("C5-upload","Btn Back","C1-room"),
 ("C5-upload","Btn Open camera C5","C5-upload"),("C5-upload","Btn Rel Musa","P7-results"),
 ("C5-upload","Btn Rel Grace","P7-results"),
 ("C6-refer","Btn Send refer C6","C7-sign"),("C6-refer","Btn Save refer C6","C1-room"),
 ("C6-refer","Btn Consult tab Note","C1-room"),("C6-refer","Btn Refer Tunde","C6-refer"),
 ("C6-refer","Btn Refer Chuka","C6-refer"),
 ("C7-sign","Btn Sign C7","C8-signed"),("C7-sign","Btn Save draft C7","C9-drafts"),
 ("C7-sign","Btn Back","C1-room"),
 ("C8-signed","Btn Start consult","C1-room"),("C8-signed","Btn Nav Today","K1-today"),
 ("C8-signed","Btn Q Chidi","K4-file"),
 ("C9-drafts","Btn Open room C1","C1-room"),("C9-drafts","Btn Open sign C7","C7-sign"),
 ("C9-drafts","Btn Draft Chidi","C1-room"),("C9-drafts","Btn Draft Fatima","C7-sign"),
 ("C10-virtual","Btn Join call C10","C1-room"),("C10-virtual","Btn Start consult","C1-room"),
 ("C10-virtual","Btn Send link C10","C10-virtual"),("C10-virtual","Btn Open week K6","K6-week"),
 ("C10-virtual","Btn Admit Amara","C1-room"),("C10-virtual","Btn Refund visit","K5-outcome"),
 # ---- patients
 ("P1-patients","Btn Open Amara","P2-record"),("P1-patients","Btn Open Chidi","P2-record"),
 ("P1-patients","Btn Open Grace","P2-record"),("P1-patients","Btn Open Musa","P2-record"),
 ("P1-patients","Btn Open Tunde","P2-record"),("P1-patients","Btn Open Fatima","P2-record"),
 ("P1-patients","Btn Scan patient","P2-record"),("P1-patients","Btn Add walkin","P2-record"),
 ("P1-patients","Btn Open followups P4","P4-followups"),
 ("P2-record","Btn Back","P1-patients"),("P2-record","Btn Start consult","C1-room"),
 ("P2-record","Btn Open access P3","P3-access"),("P2-record","Btn Open note last","C8-signed"),
 ("P2-record","Btn Open lab","C5-upload"),("P2-record","Btn Open other note","C8-signed"),
 ("P2-record","Btn Open followups P4","P4-followups"),("P2-record","Btn Open messages P5","P5-messages"),
 ("P3-access","Btn Back","P2-record"),("P3-access","Btn Send access P3","P2-record"),
 ("P4-followups","Btn Send recall P4","P4-followups"),
 ("P4-followups","Btn Fu Grace","P2-record"),("P4-followups","Btn Fu Fatima","P2-record"),
 ("P4-followups","Btn Fu Musa","P2-record"),("P4-followups","Btn Fu Tunde","P2-record"),
 ("P4-followups","Btn Test Amara","P2-record"),("P4-followups","Btn Test Chidi","P2-record"),
 ("P5-messages","Btn Msg Grace","P2-record"),("P5-messages","Btn Msg Amara","P2-record"),
 ("P5-messages","Btn Msg Musa","P2-record"),("P5-messages","Btn Msg Fatima","P2-record"),
 ("P5-messages","Btn Msg Chidi","P2-record"),
 ("P6-refills","Btn Approve Grace","P6-refills"),("P6-refills","Btn Visit Grace","P4-followups"),
 ("P6-refills","Btn Change Grace","C3-prescribe"),("P6-refills","Btn Decline Grace","P6-refills"),
 ("P6-refills","Btn Approve Fatima","P6-refills"),("P6-refills","Btn Refill Grace","P2-record"),
 ("P6-refills","Btn Open followups P4","P4-followups"),
 ("P7-results","Btn Release Grace","C5-upload"),("P7-results","Btn Hold Grace","P7-results"),
 ("P7-results","Btn Book Grace","P4-followups"),("P7-results","Btn Release Musa","C5-upload"),
 ("P7-results","Btn Release Amara","C5-upload"),("P7-results","Btn Res Grace","C5-upload"),
 ("P7-results","Btn Res Musa","P8-result"),("P7-results","Btn Res Amara","C5-upload"),
 # ---- where an order goes, and who is allowed to see it
 # C4 writes the order; C11 decides who runs it. Choosing a laboratory that is not on Medra
 # is what starts the link flow, so the two chains meet on one screen rather than living in
 # separate corners of the app.
 ("C4-tests","Btn Open route C11","C11-route"),
 ("C11-route","Btn Send order C11","C12-order"),("C11-route","Btn Open tests C4","C4-tests"),
 ("C11-route","Btn Route external","C13-link"),("C11-route","Btn Route dept","C11-route"),
 ("C11-route","Btn Route imaging","C11-route"),("C11-route","Btn Route partner","C11-route"),
 ("C11-route","Btn Route paper","C11-route"),("C11-route","Btn Consult tab Note","C1-room"),
 ("C11-route","Btn Consult tab Tests","C4-tests"),
 ("C12-order","Btn Back","C4-tests"),("C12-order","Btn Open result P8","P8-result"),
 ("C12-order","Btn Open route C11","C11-route"),("C12-order","Btn Open links C15","C15-links"),
 ("C12-order","Btn Ord musa","P8-result"),("C12-order","Btn Ord emeka","C15-links"),
 ("C12-order","Btn Ord message","P5-messages"),("C12-order","Btn Ord cancel","C4-tests"),
 ("C13-link","Btn Ask consent C13","C14-consent"),("C13-link","Btn Back","C11-route"),
 ("C14-consent","Btn Open links C15","C15-links"),("C14-consent","Btn Back","C13-link"),
 ("C14-consent","Btn Withdraw consent C14","C11-route"),
 ("C14-consent","Btn Cn partner","C11-route"),("C14-consent","Btn Cn print","C4-tests"),
 ("C14-consent","Btn Cn ask","P5-messages"),("C14-consent","Btn Cn none","C1-room"),
 ("C15-links","Btn Open room C1","C1-room"),("C15-links","Btn Open result P8","P8-result"),
 ("C15-links","Btn Link zenith","C15-links"),("C15-links","Btn Link stmarys","C15-links"),
 ("C15-links","Btn Link lifebridge","C15-links"),("C15-links","Btn Revoke C15","C15-links"),
 # a doctor who is not on Medra is the same problem as a laboratory that is not
 ("C6-refer","Btn Refer letter","C13-link"),
 # ---- a result that came back as data
 ("P8-result","Btn Back","P7-results"),("P8-result","Btn Release P8","P7-results"),
 ("P8-result","Btn Hold P8","P7-results"),("P8-result","~Btn Prov pdf","P8-result"),
 ("P8-result","Btn Del k","P2-record"),("P8-result","Btn Del egfr","P2-record"),
 # ---- practice
 ("S1-profile","Btn Open fees S2","S2-fees"),("S1-profile","Btn Open virtual S3","S3-virtual"),
 ("S1-profile","Btn Open contact S4","S4-contact"),("S1-profile","Btn Save profile S1","S1-profile"),
 ("S1-profile","Btn Open reviews R2","R2-reviews"),("S1-profile","Btn Preview profile","S1-profile"),
 ("S1-profile","Btn Open practice S7","S7-practice"),("S1-profile","Btn Sign out","AUTH"),
 ("S2-fees","Btn Save fees S2","S1-profile"),("S2-fees","Btn Back","S1-profile"),
 ("S3-virtual","Btn Save virtual S3","S1-profile"),("S3-virtual","Btn Back","S1-profile"),
 ("S4-contact","Btn Save contact S4","S1-profile"),("S4-contact","Btn Back","S1-profile"),
 ("S5-earnings","Btn Payout statements","S5-earnings"),("S5-earnings","Btn Open billing S6","S6-billing"),
 ("S6-billing","Btn Add card S6","S6-billing"),("S6-billing","Btn Compare plans S6","S6-billing"),
 ("S6-billing","Btn Choose Solo","S6-billing"),("S6-billing","Btn Choose Practice","S6-billing"),
 ("S6-billing","Btn Choose Group","S6-billing"),
 ("S7-practice","Btn Back","S1-profile"),("S7-practice","Btn Save practice S7","S1-profile"),
 ("S8-security","Btn Sign out all","AUTH"),("S8-security","Btn Close account","AUTH"),
 # ---- growth
 ("R1-insights","Btn Open availability K7","K7-availability"),("R1-insights","Btn Fix hours","K7-availability"),
 ("R1-insights","Btn Fix langs","S1-profile"),("R1-insights","Btn Fix photo","S1-profile"),
 ("R1-insights","Btn Fix virtual","S2-fees"),
 ("R2-reviews","~Btn Rev report","R2-reviews"),
 ("R3-link","Btn Share wa R3","R3-link"),("R3-link","Btn Copy booking link","R3-link"),
 ("R3-link","Btn Download poster R3","R3-link"),("R3-link","Btn Import list","R3-link"),
 ("R3-link","Btn Open link R3","R3-link"),
 # ---- states
 ("X1-locked","Btn Add card S6","S6-billing"),("X1-locked","Btn Compare plans S6","S6-billing"),
 ("X2-empty","Btn Open availability K7","K7-availability"),("X2-empty","Btn Open link R3","R3-link"),
 ("X2-empty","Btn Open fees S2","S2-fees"),("X2-empty","Btn Open profile S1","S1-profile"),
 ("X2-empty","Btn Open invite G3","G3-invite"),("X2-empty","Btn Open week K6","K6-week"),
 ("X2-empty","Btn Open timeoff K8","K8-timeoff"),
 ("X3-notifications","Btn Notif result","P7-results"),("X3-notifications","Btn Notif refill","P6-refills"),
 ("X3-notifications","Btn Notif cancel","K6-week"),("X3-notifications","Btn Notif unsigned","C9-drafts"),
 ("X3-notifications","Btn Notif access","P2-record"),("X3-notifications","Btn Notif payout","S5-earnings"),
 ("X3-notifications","Btn Notif rating","R2-reviews"),("X3-notifications","Btn Notif booking","K2-requests"),
 ("X3-notifications","Btn Notif invite","G3-invite"),("X3-notifications","Btn Open results P7","P7-results"),
 ("X3-notifications","Btn Open refills P6","P6-refills"),("X3-notifications","Btn Open drafts C9","C9-drafts"),
 ("X4-offline","Btn Retry X4","K1-today"),
 ("X5-error","Btn Retry X5","K1-today"),("X5-error","Btn Open help","X5-error"),
 # ---- routes that existed as affordances but had never been wired
 ("S1-profile","Btn Open security S8","S8-security"),("S1-profile","Btn Open earnings S5","S5-earnings"),
 ("S1-profile","Btn Open billing S6","S6-billing"),
 ("S8-security","Btn Back","S1-profile"),
 ("R1-insights","Btn Open link R3","R3-link"),("R1-insights","Btn Open invite G3","G3-invite"),
 ("R2-reviews","Btn Open link R3","R3-link"),("R2-reviews","Btn Open profile S1","S1-profile"),
 ("R3-link","Btn Open invite G3","G3-invite"),
 ("K1-today","Btn Nav More","K9-more"),
 ("K2-requests","Btn Open drafts C9","C9-drafts"),
 # K9 — the fifth mobile tab and the desktop directory
 ("K9-more","Btn Open results P7","P7-results"),("K9-more","Btn Open refills P6","P6-refills"),
 ("K9-more","Btn Open drafts C9","C9-drafts"),("K9-more","Btn Open billing S6","S6-billing"),
 ("K9-more","Btn Open reviews R2","R2-reviews"),("K9-more","Btn Open link R3","R3-link"),
 ("K9-more","Btn Open invite G3","G3-invite"),("K9-more","Btn Open profile S1","S1-profile"),
 ("K9-more","Btn Open fees S2","S2-fees"),("K9-more","Btn Open virtual S3","S3-virtual"),
 ("K9-more","Btn Open contact S4","S4-contact"),("K9-more","Btn Open practice S7","S7-practice"),
 ("K9-more","Btn Open security S8","S8-security"),("K9-more","Btn Open verify G2","G2-verification"),
 ("K9-more","Btn Open help","X5-error"),("K9-more","Btn Sign out","AUTH"),
 # the message action a mobile queue row carries instead of the desktop row's Open button
 ("K1-today","Btn Msg Q Chidi","P5-messages"),("K1-today","Btn Msg Q Musa","P5-messages"),
 ("K1-today","~Btn Msg Q Grace","P5-messages"),("K1-today","~Btn Msg Q Tunde","P5-messages"),
 ("K6-week","Btn Msg Q Chidi","P5-messages"),("K6-week","Btn Msg Q Musa","P5-messages"),
 ("K6-week","~Btn Msg Q Grace","P5-messages"),("K6-week","~Btn Msg Q Tunde","P5-messages"),
] + [
 # States are reached by condition, not by tapping, so each one carries a switcher strip.
 # Without it half the States page is unreachable in a click-through and cannot be demoed.
 (src, "Btn State " + dst[:2], dst)
 for src in ("X1-locked","X2-empty","X3-notifications","X4-offline","X5-error","X6-loading")
 for dst in ("X1-locked","X2-empty","X3-notifications","X4-offline","X5-error","X6-loading")
 if src != dst
]

def resolve(target, side):
    if target == "AUTH": return AUTH_DR[side]
    return NAMES[target][side]

# Which Btn names each frame actually contains. Splitting mobile into a hub plus sections
# moved a lot of hotspots off the hub; the transition table describes a *screen*, so a link
# is attached to whichever frame of that screen carries the control.
BTNS = {}
for _pg, _fn, _jsx in frames:
    BTNS[nm_of(_jsx)] = set(re.findall(r'name="(Btn [^"]+)"', _jsx))

# These two are owned by the generated hub ⇄ section wiring and must not be fanned out.
HUB_ONLY = {"Btn Back", "Btn Close sheet"}

resolved = []
for fid, hot, target in TRN:
    if fid not in NAMES: raise SystemExit(f"unknown source frame {fid}")
    # A leading "~" marks a control that exists on one breakpoint only — mobile carries a
    # per-row action the capped desktop list does not. Absence is then not an error.
    soft = hot.startswith("~")
    hot = hot[1:] if soft else hot
    if not soft or hot in BTNS.get(NAMES[fid][0], ()):
        resolved.append([NAMES[fid][0], hot, resolve(target, 0)])
    fam = FAMILY.get(fid, [NAMES[fid][1]])
    if hot in HUB_ONLY:
        hits = [fam[0]]
    else:
        hits = [f for f in fam if hot in BTNS.get(f, ())]
        if not hits and not soft: hits = [fam[0]]
    for f in hits:
        resolved.append([f, hot, resolve(target, 1)])

# Auto-generated hub ⇄ section and hub ⇄ sheet links, with their own motion class.
AUTO_SPEC = {}
for _frm, _hot, _to, _kind in AUTO:
    resolved.append([_frm, _hot, _to])
    AUTO_SPEC[_hot] = _kind

nav_jobs = []
for fid, pair in NAMES.items():
    for side in (0, 1):
        for hot, target in NAVMAP.items():
            nav_jobs.append([pair[side], hot, target[side]])
# Section and sheet frames carry the tab bar too, so the sweep has to reach them.
for _nm in MOBILE_EXTRA:
    for hot, target in NAVMAP.items():
        nav_jobs.append([_nm, hot, target[1]])

order_js, starts_js = {}, {}
for page, fids in ORDER.items():
    if page == "Components": continue
    order_js[PAGE_FIGMA[page]] = ROWS[page]
    # Two starting points per page. With one, the mobile row is not a prototype at all —
    # you cannot present it without hand-picking a frame each time.
    starts_js[PAGE_FIGMA[page]] = [NAMES[fids[0]][0], NAMES[fids[0]][1]]

MOTION = json.dumps({
  "default": {"type": "SMART_ANIMATE", "easing": "GENTLE", "duration": 0.26},
  "push":    {"type": "MOVE_IN",  "direction": "LEFT",   "easing": "GENTLE",  "duration": 0.24},
  "pop":     {"type": "MOVE_OUT", "direction": "RIGHT",  "easing": "EASE_IN", "duration": 0.20},
  "sheet":   {"type": "MOVE_IN",  "direction": "BOTTOM", "easing": "GENTLE",  "duration": 0.30},
  "instant": {"type": "SMART_ANIMATE", "easing": "LINEAR", "duration": 0.01},
})
PUSH = json.dumps(["Btn Open prep", "Btn Open record P2", "Btn Open access P3", "Btn Open fees S2",
                   "Btn Open virtual S3", "Btn Open contact S4", "Btn Open profile S1", "Btn Open billing S6",
                   "Btn Open availability K7", "Btn Open timeoff K8", "Btn Open note last", "Btn Open practice S7",
                   "Btn Open Amara", "Btn Open Chidi", "Btn Open Grace", "Btn Open Musa", "Btn Open Tunde",
                   "Btn Open Fatima", "Btn Open verify G2", "Btn Open reviews R2", "Btn Open link R3"])
POP  = json.dumps(["Btn Back"])
SHEET = json.dumps(["Btn Open prescribe C3", "Btn Open tests C4", "Btn Open upload C5", "Btn Open refer C6",
                    "Btn Open late K3", "Btn Open outcome K5", "Btn Template complaint", "Btn Template exam",
                    "Btn Template diagnosis", "Btn Template plan", "Btn Template comment"])

linker = ("(async () => {\n"
 "  // Medra Doctor — wire the prototype, close the navigation, arrange the canvas.\n"
 "  // Doctor-module only. It touches nothing outside the eight 'Medra Doctor —' pages, except\n"
 "  // one cross-link: Sign out goes to the auth bundle's doctor login if that page exists.\n"
 "  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();\n"
 "  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();\n"
 "  const pages = figma.root.children.filter(n => n.type==='PAGE');\n"
 "  const byName = {}; for (const pg of pages) for (const f of pg.children) if (f.type==='FRAME') byName[norm(f.name)] = f;\n"
 "  const F = n => byName[norm(n)];\n"
 "  const findAll = (root,t) => { const out=[]; const target=norm(t); const w=n=>{ if(n.name&&norm(n.name)===target) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 "  const allBtns = root => { const out=[]; const w=n=>{ if(n.name&&/^Btn /.test(norm(n.name))) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 f"  const M = {MOTION};\n"
 f"  const PUSH = {PUSH}, POP = {POP}, SHEET = {SHEET};\n"
 f"  const AUTOSPEC = {json.dumps(AUTO_SPEC)};\n"
 "  const ease = e => ({ type: e });\n"
 "  const mk = spec => spec.type==='SMART_ANIMATE'\n"
 "    ? { type:'SMART_ANIMATE', easing:ease(spec.easing), duration:spec.duration }\n"
 "    : { type:spec.type, direction:spec.direction, matchLayers:false, easing:ease(spec.easing), duration:spec.duration };\n"
 "  const specFor = hot => AUTOSPEC[hot] ? M[AUTOSPEC[hot]]\n"
 "                       : PUSH.includes(hot) ? M.push : POP.includes(hot) ? M.pop\n"
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
 "  // 1. explicit screen-to-screen transitions\n"
 "  for (const [fromN,hot,toN] of TRN){ const fr=F(fromN), to=F(toN);\n"
 "    if(!fr||!to){ missing.push(fromN+' -> '+hot+' -> '+toN); continue; }\n"
 "    const nodes=findAll(fr,hot); if(!nodes.length){ missing.push(fromN+' -> '+hot); continue; }\n"
 "    for (const nd of nodes) await go(nd,to,specFor(hot)); }\n"
 "  // 2. the rail, the tab bar and the command strip, on every doctor frame\n"
 "  let navLinked = 0;\n"
 "  for (const [fromN,hot,toN] of NAVJOBS){ const fr=F(fromN), to=F(toN); if(!fr||!to) continue;\n"
 "    for (const nd of findAll(fr,hot)){ if (wired.has(nd.id)) continue; await go(nd,to,M.default); navLinked++; } }\n"
 "  // 3. no dead hotspots: anything still named \"Btn …\" stays on its own screen\n"
 "  let stay = 0;\n"
 "  for (const fn of OWN){ const fr=F(fn); if(!fr) continue;\n"
 "    for (const nd of allBtns(fr)){ if (wired.has(nd.id)) continue;\n"
 "      if (nd.reactions && nd.reactions.length) { wired.add(nd.id); continue; }\n"
 "      await go(nd,fr,M.instant); stay++; } }\n"
 "  // 4. arrange: desktop row on top, matching mobile row beneath, in flow order\n"
 "  const GX=170, GY=150;\n"
 "  for (const pg of pages){ const ord=ORDER[pg.name]; if(!ord) continue; let x=0, rowH=0;\n"
 "    for (const dn of ord.d){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const mn of ord.m){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(!s) continue;\n"
 "    const pts=[]; if(F(s[0])) pts.push({ nodeId:F(s[0]).id, name:pg.name+' · Desktop' });\n"
 "    if(F(s[1])) pts.push({ nodeId:F(s[1]).id, name:pg.name+' · Mobile' });\n"
 "    if(pts.length) pg.flowStartingPoints=pts; }\n"
 "  return { linked, navLinked, stayOnScreen: stay, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT, "link-doctor.js"), "w").write(linker)

# ---- components script -------------------------------------------------------------
components = """(async () => {
  // Medra Doctor — turn the cmp/* frames on the doctor components page into component sets.
  // Doctor-module only: it looks at one page and removes only the sets it owns.
  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();
  const PAGE = 'Medra Doctor — 8 Components';
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

  const OWNED = new Set(Object.keys(groups).map(c => `Medra Doctor/${c}`));
  for (const node of [...page.children]) {
    if (node.type === 'COMPONENT_SET' && OWNED.has(node.name)) node.remove();
  }

  const REST = { 'Slot':'Open', 'Queue Row':'Waiting', 'Share Toggle':'Shared', 'Scope Line':'Granted',
                 'Drug Result':'Default', 'Stat Tile':'Info', 'Checklist Row':'Todo',
                 'Outcome':'Default', 'Rail Item':'Inactive' };
  const WIRING = {
    'Slot':          [['ON_CLICK','Booked']],
    'Queue Row':     [['ON_HOVER','Now']],
    'Share Toggle':  [['ON_CLICK','Withheld']],
    'Checklist Row': [['ON_CLICK','Done']],
    'Outcome':       [['ON_CLICK','Selected']],
    'Rail Item':     [['ON_HOVER','Active']],
  };
  const BACK = {
    'Slot':          [['ON_CLICK','Open']],
    'Queue Row':     [['ON_HOVER','Waiting']],
    'Share Toggle':  [['ON_CLICK','Shared']],
    'Outcome':       [['ON_CLICK','Default']],
    'Rail Item':     [['ON_HOVER','Inactive']],
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
      set.name = `Medra Doctor/${comp}`;
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
      report.components.push(`Medra Doctor/${comp} (${comps.map(([v]) => v).join(', ')})`);
    } catch (e) { report.notes.push(`${comp}: ${e.message}`); }
  }
  return report;
})();
"""
open(os.path.join(OUT, "components-doctor.js"), "w").write(components)

# ---- render script (DOCTOR MODULE ONLY) --------------------------------------------
ps = ["# ============================================================================",
      "# Medra — DOCTOR MODULE ONLY.",
      "# Renders the eight 'Medra Doctor —' pages and nothing else. It does not touch the",
      "# design-system, authentication or member pages: it creates its own pages, renders",
      "# into them, and wires only frames whose names begin with 'Doctor · '.",
      "# Requires: Figma Desktop open, the file open, figma-ds-cli connected.",
      "# ============================================================================",
      "",
      "# 1. prime the offline icon cache (safe to re-run)",
      'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
      'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
      "",
      "# 2. tokens — the same 41 tokens as every other Medra bundle, so this is a no-op",
      "#    if you have already imported them. It never removes or renames anything.",
      "figma-cli tokens import-design-md .\\DESIGN.md",
      ""]
for p, fids in ORDER.items():
    pg = PAGE_FIGMA[p].replace("&amp;", "&")
    ps.append(f'# ---- {pg} ----')
    ps.append(f'figma-cli eval "(async()=>{{const t=\'{pg}\';let p=figma.root.children.find(n=>n.name===t);if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"')
    # Take the filenames from the manifest, not from the screen ids — a mobile screen is now
    # a hub plus its section and sheet frames, and deriving "-d/-m" would skip every one.
    lst = ", ".join("'" + f + "'" for f in manifest[p])
    ps.append(f'foreach ($f in @({lst})) {{ figma-cli render (Get-Content $f -Raw) }}')
    ps.append("")
ps.append("# 3. turn the cmp/* frames into interactive component sets (doctor page only)")
ps.append("figma-cli run .\\components-doctor.js")
ps.append("")
ps.append("# 4. wire the prototype, close the navigation, arrange the canvas")
ps.append("figma-cli run .\\link-doctor.js")
ps.append("")
ps.append("# Expected: link-doctor.js returns { linked, navLinked, stayOnScreen, framesFound, missing }.")
ps.append("# A non-empty 'missing' means that frame did not render — re-render that one .jsx and re-run step 4.")
open(os.path.join(OUT, "render-doctor.ps1"), "w").write("\n".join(ps))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} screen links "
      f"· {len(nav_jobs)} nav links · {len(CMP)} component states")
for p, fs in manifest.items(): print(f"  {p}: {len(fs)}")
