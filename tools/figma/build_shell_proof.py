#!/usr/bin/env python3
"""Four screens in the unified shell — one per persona family — so the look can be judged
before ~150 desktop screens are converted to it. Proof only; not part of any bundle."""
import os, re, sys, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from shell import *
from normalise import normalise
from member2_kit import hr, status_pill, lab_line, audit_row

OUT = "/home/user/Medra-24/figma/medra-shell-proof"
os.makedirs(OUT, exist_ok=True)
for f in ("DESIGN.md", "validate.js"):
    shutil.copyfile(f"/home/user/Medra-24/figma/medra-member/{f}", os.path.join(OUT, f))
if not os.path.exists(os.path.join(OUT, "assets")):
    shutil.copytree("/home/user/Medra-24/figma/medra-member/assets", os.path.join(OUT, "assets"))

frames = []
def add(fid, jsx): frames.append((fid, jsx))

NAV_MEMBER = [("house","Nav Home","Home"),("search","Nav Find","Find care"),
              ("calendar-days","Nav Visits","My visits"),("clipboard-list","Nav Records","Records"),
              ("pill","Nav Meds","Medicines"),("circle-user","Nav Profile","Profile")]
NAV_DOCTOR = [("layout-dashboard","Nav Today","Today"),("inbox","Nav Requests","Requests"),
              ("calendar-days","Nav Schedule","Schedule"),("users","Nav Patients","Patients"),
              ("stethoscope","Nav Consults","Consults"),("banknote","Nav Money","Money"),
              ("trending-up","Nav Growth","Growth")]
NAV_ADMIN  = [("layout-dashboard","Nav Today","Today"),("calendar-check","Nav Bookings","Bookings"),
              ("building-2","Nav Departments","Departments"),("users","Nav People","People"),
              ("share-2","Nav Referrals","Referrals"),("shield-check","Nav Access","Access"),
              ("chart-column","Nav Reports","Reports")]
NAV_NURSE  = [("list-checks","Nav Queue","My queue"),("heart-pulse","Nav Vitals","Vitals"),
              ("users","Nav Members","Members"),("message-square-text","Nav Messages","Messages")]

# ---------------------------------------------------------------- 1. member
add("proof-member", app_desk(
    "Member · Home — H1 Home", "member", "Good morning, Amara",
    f'<Frame w="fill" flex="row" gap={{14}}>'
    f'{stat("calendar-check","2","Upcoming visits","Next in 2 days",filled=True,name="Nav Visits")}'
    f'{stat("pill","2","Active medicines","1 due at 6pm",name="Nav Meds")}'
    f'{stat("clipboard-list","8","Visits on record","Since Jan 2026",name="Nav Records")}'
    f'{stat("droplet","O+","Blood group","Not medically verified",name="Nav Records")}</Frame>'
    f'<Frame w="fill" flex="row" gap={{16}} items="start">'
    f'<Frame grow={{1}} flex="col" gap={{16}}>'
    f'{panel("Available today", row("stethoscope","Dr. Ngozi Okafor","Cardiologist · Garki Medical Centre · 2.4 km",value="₦15,000",name="Btn Doctor N") + hr() + row("stethoscope","Dr. Chuka Eze","General practice · Wuse Clinic · 2.4 km",value="₦8,000",name="Btn Doctor C"), "See all", "Nav Find")}'
    f'{panel("Today’s medicines", row("pill","Amlodipine","5 mg · 1 tablet · 08:00",value="Taken",tone="ok",name="Med A",chevron=False) + hr() + row("pill","Metformin","500 mg · 1 tablet · 18:00",value="Due",name="Med M",chevron=False), "See all", "Nav Meds")}'
    f'</Frame>'
    f'<Frame w={{380}} flex="col" gap={{16}}>'
    f'{panel("Your next visit", T(14,"semibold","var:text/strong","Dr. Ngozi Okafor") + T(12,"regular","var:text/muted","Tue, 12 Aug · 10:30 AM · virtual",w="fill") + cta("Join the visit","Join visit","video"))}'
    f'{panel("Recent records", row("file-text","Hypertension review","Dr. Ngozi Okafor · 12 Jun",name="Rec 1") + hr() + row("flask-conical","Full blood count","Garki Medical Centre · 28 Apr",name="Rec 2"), "See all", "Nav Records")}'
    f'</Frame></Frame>',
    NAV_MEMBER, 0, sub="Tuesday 11 August"))

# ---------------------------------------------------------------- 2. doctor
add("proof-doctor", app_desk(
    "Doctor · Today — K1 Queue", "doctor", "Thursday 14 August",
    f'<Frame w="fill" flex="row" gap={{14}}>'
    f'{stat("users","8","In your queue","3 waiting now",filled=True,name="Nav Patients")}'
    f'{stat("inbox","6","Booking requests","2 near the 24h reply",name="Nav Requests")}'
    f'{stat("flask-conical","3","Results to release","1 out of range",name="Nav Requests")}'
    f'{stat("banknote","₦96,000","Released this week","Payout Friday",name="Nav Money")}</Frame>'
    f'<Frame w="fill" flex="row" gap={{16}} items="start">'
    f'<Frame grow={{1}} flex="col" gap={{16}}>'
    f'{panel("Waiting now", row("user","Amara Okeke","MDR-8842-19 · 10:30 · virtual · hypertension review",value="Ready",tone="ok",name="Q Amara") + hr() + row("user","Chidi Okeke","MDR-8842-20 · 11:00 · in person · cough four days",value="11:00",name="Q Chidi") + hr() + row("user","Musa Ibrahim","MDR-7714-02 · 11:30 · first visit",value="11:30",name="Q Musa"), "Week view", "Nav Schedule")}'
    f'{panel("Needs you", row("flask-conical","Grace Okeke · HbA1c 8.4%","High · arrived yesterday 16:10",value="18h",tone="err",name="Res Grace") + hr() + row("notebook-pen","Chidi Okeke · unsigned note","Yesterday 16:40 · no diagnosis yet",value="18h",tone="warn",name="Draft Chidi"), "All", "Nav Requests")}'
    f'</Frame>'
    f'<Frame w={{380}} flex="col" gap={{16}}>'
    f'{panel("Next up", row("user","Amara Okeke","10:30 – 11:00 · virtual",name="Q Amara") + cta("Start the consultation","Start consult","stethoscope"))}'
    f'{panel("Running late?", T(12,"regular","var:text/muted","Everyone waiting is told once, with a new time. Nobody has to ring the clinic.",w="fill") + ghost("Tell them I am 15 minutes late","Open late K3","timer"))}'
    f'</Frame></Frame>',
    NAV_DOCTOR, 0, sub="Garki Medical Centre", badges={"Nav Requests"}, expanded=True))

# ---------------------------------------------------------------- 3. org admin
add("proof-admin", app_desk(
    "Org · Today — B1 Today", "admin", "Garki Medical Centre",
    f'<Frame w="fill" flex="row" gap={{14}}>'
    f'{stat("calendar-check","47","Booked today","7 unallocated",filled=True,name="Nav Bookings")}'
    f'{stat("users","23","Staff on duty","2 departments short",name="Nav People")}'
    f'{stat("clock","14 min","Median wait","Down from 22",name="Nav Reports")}'
    f'{stat("banknote","₦1.42m","Taken this week","Reconciled to Thursday",name="Nav Reports")}</Frame>'
    f'<Frame w="fill" flex="row" gap={{16}} items="start">'
    f'<Frame grow={{1}} flex="col" gap={{16}}>'
    f'{panel("Departments right now", row("heart-pulse","Nursing","6 on duty · 4 patients waiting",value="Normal",tone="ok",name="Dept nursing") + hr() + row("flask-conical","Laboratory","3 on duty · 11 samples · median 4h",value="Busy",tone="warn",name="Dept lab") + hr() + row("pill","Pharmacy","2 on duty · 1 stock-out flagged",value="Attention",tone="err",name="Dept pharmacy") + hr() + row("concierge-bell","Front desk","4 on duty · 2 walk-ins waiting",value="Normal",tone="ok",name="Dept desk"), "All departments", "Nav Departments")}'
    f'{panel("Unallocated bookings", row("calendar-clock","Halima Sani · 11:30","Paid ₦15,000 · in person · needs a doctor",value="Allocate",tone="warn",name="Alloc halima") + hr() + row("calendar-clock","Emeka Nwosu · 12:00","Paid ₦8,000 · virtual · needs a doctor",value="Allocate",tone="warn",name="Alloc emeka"), "All bookings", "Nav Bookings")}'
    f'</Frame>'
    f'<Frame w={{380}} flex="col" gap={{16}}>'
    f'{panel("Needs a decision", row("user-plus","Ifeoma Nwachukwu","Lab scientist · MLSCN verified · awaiting a seat",value="Approve",tone="warn",name="Seat ifeoma") + hr() + row("shield-alert","Break-glass access used","Dr. Eze · 02:14 · reason recorded",value="Review",tone="err",name="Open audit F2"))}'
    f'{panel("Seats", T(26,"bold","var:text/strong","18 / 25") + T(12,"regular","var:text/muted","Seats used. Two clinical seats are unassigned.",w="fill") + ghost("Manage seats","Nav People","users"))}'
    f'</Frame></Frame>',
    NAV_ADMIN, 0, sub="Area 3 branch · all departments", badges={"Nav People"}))

# ---------------------------------------------------------------- 4. org nurse
add("proof-nurse", app_desk(
    "Org · Nursing — D1 My Queue", "nurse", "My queue",
    f'<Frame w="fill" flex="row" gap={{14}}>'
    f'{stat("list-checks","4","Waiting for you","Oldest 12 min",filled=True,name="Nav Queue")}'
    f'{stat("heart-pulse","9","Vitals taken today",name="Nav Vitals")}'
    f'{stat("syringe","3","Injections due","1 overdue",name="Nav Queue")}'
    f'{stat("triangle-alert","1","Escalated","Dr. Okafor notified",name="Nav Messages")}</Frame>'
    f'<Frame w="fill" flex="row" gap={{16}} items="start">'
    f'<Frame grow={{1}} flex="col" gap={{16}}>'
    f'{panel("Waiting for vitals", row("user","Amara Okeke","MDR-8842-19 · for Dr. Okafor at 10:30 · hypertension review",value="Start",tone="ok",name="Vit amara") + hr() + row("user","Halima Sani","MDR-9012-44 · for Dr. Eze at 11:30 · referred in",value="Waiting",name="Vit halima") + hr() + row("user","Musa Ibrahim","MDR-7714-02 · chest pain · triage first",value="Urgent",tone="err",name="Vit musa"), "Whole queue", "Nav Queue")}'
    f'{panel("Standing orders", row("syringe","Ngozi Bala · ceftriaxone 1g IM","Ordered by Dr. Eze 09:10 · second of five",value="Give",tone="warn",name="Inj ngozi",chevron=False) + hr() + row("syringe","Blessing Ade · tetanus toxoid","Ordered by Dr. Okafor 08:40 · overdue by 40 min",value="Overdue",tone="err",name="Inj blessing",chevron=False))}'
    f'</Frame>'
    f'<Frame w={{380}} flex="col" gap={{16}}>'
    f'{panel("Escalate to a doctor", T(12,"regular","var:text/muted","Goes to whoever is on duty for that department, not to one person — and it is recorded either way.",w="fill") + cta("Flag a patient now","Open escalate D4","triangle-alert"))}'
    f'{panel("Your shift", row("clock","07:00 – 15:00","Handover to Ifeoma at 15:00",name="Shift",chevron=False) + hr() + row("users","Six on duty","Two in outpatient, four on the ward",name="Duty",chevron=False))}'
    f'</Frame></Frame>',
    NAV_NURSE, 0, sub="Garki Medical Centre · Area 3"))

def sanitize(s): return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)', '&amp;', s)
for fid, jsx in frames:
    open(os.path.join(OUT, f"{fid}.jsx"), "w").write(sanitize(normalise(jsx)))
open(os.path.join(OUT, "pages.json"), "w").write(json.dumps({"Proof": [f"{f}.jsx" for f, _ in frames]}, indent=2))
print(f"{len(frames)} proof frames -> {OUT}")
