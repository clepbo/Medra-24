#!/usr/bin/env python3
"""Medra — Organisation module.

Covers PRD v2.0 Modules 10–13 end to end:
  10 Organisation onboarding, departments, seats, staff, allocation, billing
  11 The clinical chain — nursing, laboratory, pharmacy, front desk, each a task-scoped app
  12 The scoped, single-use external access link, including the external party's own screens
  13 Verification state on health data, shown wherever a value appears

Seven pages, 55 screens. Desktop 1440 + a mobile hub with its own sections and sheets, so a
front desk on a phone gets one screenful at a time rather than a console shrunk down.
"""
import os, re, json, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *
from org_kit import *

OUT = "/home/user/Medra-24/figma/medra-org"
os.makedirs(OUT, exist_ok=True)

frames = []; NAMES = {}; ORDER = {}
MOBILE_EXTRA = []; AUTO = []; FAMILY = {}; ROWS = {}

def nm_of(jsx): return re.search(r'name="([^"]+)"', jsx).group(1)

def add(page, fid, d, m):
    frames.append((page, f"{fid}-d.jsx", d)); frames.append((page, f"{fid}-m.jsx", m))
    NAMES[fid] = (nm_of(d), nm_of(m)); FAMILY[fid] = [nm_of(m)]
    ORDER.setdefault(page, []).append(fid)
    r = ROWS.setdefault(page, {"d": [], "m": []})
    r["d"].append(nm_of(d)); r["m"].append(nm_of(m))

def addx(page, fid, desktop, head, pinned="", sections=(), tab_items=None, tab=None, sheets=(),
         foot="", sec_title="More on this screen"):
    """sections: (key, icon, label, summary, value, tone, body, stats)
       sheets:   (key, icon, label, summary, tone, title, sub, body, actions)"""
    base = nm_of(desktop) + " · Mobile"
    rows, subs = [], []
    for key, ic, label, summary, value, tone, body, stats in sections:
        sname = f"{base} · {label}"
        rows.append(o_sec_row(ic, label, summary, f"Sec {fid} {key}", value, tone))
        subs.append((f"{fid}-m-{key}.jsx",
                     o_mob(sname, o_head(label, summary, back=True, stats=stats), body, tab_items, tab)))
        AUTO.append([base, f"Btn Sec {fid} {key}", sname, "push"])
        AUTO.append([sname, "Btn Back", base, "pop"])
    for key, ic, label, summary, tone, title, sub, body, actions in sheets:
        sname = f"{base} · {label} sheet"
        rows.append(o_sec_row(ic, label, summary, f"Sheet {fid} {key}", None, tone))
        subs.append((f"{fid}-m-{key}-sheet.jsx", o_sheet(sname, title, sub, body, actions)))
        AUTO.append([base, f"Btn Sheet {fid} {key}", sname, "sheet"])
        AUTO.append([sname, "Btn Close sheet", base, "pop"])
    body = (pinned or '') + (o_hub_list(rows, sec_title) if rows else '') + (foot or '')
    hub = o_mob(base, head, body, tab_items, tab)
    frames.append((page, f"{fid}-d.jsx", desktop)); frames.append((page, f"{fid}-m.jsx", hub))
    NAMES[fid] = (nm_of(desktop), base)
    FAMILY[fid] = [base] + [nm_of(j) for _, j in subs]
    ORDER.setdefault(page, []).append(fid)
    r = ROWS.setdefault(page, {"d": [], "m": []})
    r["d"].append(nm_of(desktop)); r["m"].append(base)
    for fn, jsx in subs:
        frames.append((page, fn, jsx)); MOBILE_EXTRA.append(nm_of(jsx)); r["m"].append(nm_of(jsx))

PAGE_FIGMA = {
  "Setup":    "Medra Org — 1 Setup &amp; Verification",
  "Today":    "Medra Org — 2 Today &amp; Bookings",
  "People":   "Medra Org — 3 Departments &amp; People",
  "Chain":    "Medra Org — 4 The Clinical Chain",
  "Referral": "Medra Org — 5 Referrals &amp; External Access",
  "Govern":   "Medra Org — 6 Access, Money &amp; Reports",
  "States":   "Medra Org — 7 States &amp; Edge Cases",
}
NAV = {"Today": 0, "Bookings": 1, "People": 2, "Departments": 3,
       "Referrals": 4, "Access": 5, "Reports": 6, "Settings": 7}
BADGES = {"Today": 7, "Bookings": 4, "Referrals": 3}

# The mobile tab bar is role-aware: an admin, a nurse and a front desk do not want the same
# five destinations. Three bars, one shell.
TAB_ADMIN = [("layout-dashboard", "Today", "Nav Today"), ("calendar-check", "Bookings", "Nav Bookings"),
             ("users", "People", "Nav People"), ("share-2", "Referrals", "Nav Referrals"),
             ("ellipsis", "More", "Nav More")]
TAB_STAFF = [("list-checks", "My queue", "Nav Queue"), ("users", "Members", "Nav Members"),
             ("share-2", "Referrals", "Nav Referrals"), ("bell", "Alerts", "Notifications"),
             ("ellipsis", "More", "Nav More")]
TAB_DESK  = [("concierge-bell", "Front desk", "Nav Desk"), ("calendar-check", "Bookings", "Nav Bookings"),
             ("user-plus", "Walk-in", "Nav Walkin"), ("users", "Members", "Nav Members"),
             ("ellipsis", "More", "Nav More")]

ADMIN = ("Mrs. Adaeze Nwosu", "Organisation admin")
NURSE = ("Sister Ifeoma Uche", "Nurse · Nursing")
LAB   = ("Mr. Sola Adeniyi", "Lab technician · Laboratory")
PHARM = ("Mr. Bayo Ogun", "Pharmacist · Pharmacy")
DESK  = ("Miss Ngozi Peter", "Front desk")

# =====================================================================================
# 1. SETUP & VERIFICATION  (PRD v2.0 Module 10.1–10.2)
# =====================================================================================
A1_GATE = alert_strip("triangle-alert", "You cannot receive bookings yet",
    "Two required steps are open: your practice licence is still being checked, and no department has a practitioner in it.",
    "warn", dbtn("Finish setup", "Open verify A2", "arrow-right", "navy", grow=False, size="sm"))

A1_STEPS = dgroup("Seven steps to being live", [
    checklist_row(True, "Organisation registered", "Garki Medical Centre · hospital · 3 branches", "Step org"),
    checklist_row(True, "Contact person verified", "Mrs. Adaeze Nwosu · NIN confirmed 4 Feb", "Step contact"),
    checklist_row(False, "RC number and practice licence accepted", "Licence under review since 3 hours ago", "Step licence",
                  action=dbtn("View", "Open verify A2", None, "ghost", grow=False, size="sm")),
    checklist_row(True, "Data-privacy undertaking accepted", "v2.1 · accepted 4 Feb 09:12", "Step privacy"),
    checklist_row(True, "Departments created", "Consulting, Nursing, Laboratory, Pharmacy, Front desk", "Step depts"),
    checklist_row(False, "People invited into each department", "Laboratory and Pharmacy have no one yet", "Step people",
                  action=dbtn("Invite", "Open invite C5", None, "ghost", grow=False, size="sm")),
    checklist_row(False, "Plan chosen", "Free trial · 26 days left", "Step plan",
                  action=dbtn("See plans", "Open billing F6", None, "ghost", grow=False, size="sm")),
], footer="Steps 3 and 6 are the ones that stop you being bookable. The rest can wait.")

A1_WHY = dgroup("What being live gets you", [
    drow("search", "1,240 members searched in Abuja this month", sub="184 of them for something you offer", name="Why search", chevron=False),
    drow("calendar-check", "Bookings arrive already paid", sub="No deposit chasing, no no-show gamble", name="Why paid", chevron=False, tone="ok"),
    drow("share-2", "Referrals in from other organisations", sub="Three came to Garki last week from doctors not on your staff", name="Why refer", chevron=False),
])

addx("Setup", "A1-setup",
    o_desk("Org · Setup — A1 Setup Checklist", ("Setup",),
        f'{dhead([("Two steps from",False),("your first booking",True)],26)}'
        f'{A1_GATE}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{A1_STEPS}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{A1_WHY}</Frame></Frame>',
        NAV["Today"], urgent=2, badges=BADGES),
    o_head("Setup", "5 of 7 done", back=False, ctx="Garki Medical Centre · 3 branches",
           stats=[("5/7", "Setup"), ("Review", "Licence"), ("26d", "Trial")]),
    pinned=A1_GATE,
    sections=[
      ("steps", "list-checks", "The seven steps", "Two are still open", "5/7", "warn", A1_STEPS, None),
      ("why", "trending-up", "What being live gets you", "1,240 members searched this month", None, None, A1_WHY, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- A2 verification
A2_HERO = (f'<Frame w="fill" flex="col" gap={{13}} p={{22}} rounded={{18}} image="assets/img/btn-slate.jpg" '
           f'overflow="hidden">'
           f'<Frame w="fill" flex="row" justify="between" items="center">'
           f'{T(11,"semibold","#E8A24A","VERIFICATION IN PROGRESS")}{status_pill("pending","Step 3 of 4")}</Frame>'
           f'{T(26,"bold","var:text/on-dark","We are checking your licence")}'
           f'{T(14,"regular","var:text/on-dark-muted","Started 3 hours ago. The median for a weekday application is 31 hours.",w="fill")}'
           f'{bar(60,"amber",10)}</Frame>')

A2_STEPS = dgroup("Where your application is", [
    prep_step(1, "Details received", "4 February, 09:12", done=True),
    prep_step(2, "CAC register checked", "RC 1489302 found, active", done=True),
    prep_step(3, "Practice licence checked", "A Medra reviewer is confirming the licence with the registry. Started 3 hours ago."),
    prep_step(4, "Contact person confirmed", "NIN matched. Awaiting step 3 to complete."),
], footer="Every organisation is checked by a person. An RC number only proves a company exists — the practice licence is the clinical credential, and it is the one that takes time.")

A2_DOCS = dgroup("Documents", [
    drow("file-badge", "CAC certificate", value="Accepted", sub="RC 1489302 · uploaded 4 Feb", name="Doc cac", tone="ok"),
    drow("badge-check", "Organisation practice licence", value="Under review", sub="Uploaded 4 Feb · expires 31 Dec 2026", name="Doc licence", tone="warn"),
    drow("id-card", "Contact person ID", value="Accepted", sub="NIN · Mrs. Adaeze Nwosu", name="Doc nin", tone="ok"),
    drow("upload", "Add another document", sub="Anything that helps us confirm the organisation", name="Doc add", chevron=False),
], footer="A diagnostic laboratory or a pharmacy also holds its own regulator's registration. Upload it here — the exact list per organisation type is being confirmed.")

A2_MEANWHILE = dgroup("Worth doing while you wait", [
    drow("building-2", "Add your branches", value="3", name="Open branches A3"),
    drow("layers", "Create your departments", value="5", name="Nav Departments"),
    drow("user-plus", "Invite your people", sub="They verify themselves while you wait", name="Open invite C5", tone="warn"),
    drow("circle-user", "Finish your public profile", value="70%", name="Open profile A5"),
], footer="All of it goes live with you. Nothing needs redoing after approval.")

addx("Setup", "A2-verify",
    o_desk("Org · Setup — A2 Verification", ("Setup", "Verification"),
        f'{A2_HERO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{A2_STEPS}{A2_DOCS}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{A2_MEANWHILE}</Frame></Frame>',
        NAV["Today"], urgent=2, badges=BADGES),
    o_head("Verification", "Step 3 of 4 · started 3 hours ago",
           stats=[("31h", "Median"), ("3h", "Elapsed"), ("2/3", "Docs")]),
    pinned=A2_HERO,
    sections=[
      ("steps", "list-checks", "Where your application is", "Licence check in progress", "3/4", None, A2_STEPS, None),
      ("docs", "file-text", "Documents", "Licence under review", "3", "warn", A2_DOCS, None),
      ("meanwhile", "clock", "Worth doing while you wait", "None of it needs redoing", "4", None, A2_MEANWHILE, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- A3 branches
def branch_row(name_, addr, staff, open_h, nm, main=False):
    tag = (f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="var:state/info-bg">'
           f'{T(10,"semibold","var:text/accent","Main")}</Frame>') if main else ''
    return (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{13}} items="center" py={{12}}>'
            f'<Frame w={{38}} h={{38}} rounded={{12}} bg="var:bg/muted" flex="col" justify="center" '
            f'items="center">{I("building-2",18,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>'
            f'<Frame flex="row" gap={{8}} items="center">{T(14,"semibold","var:text/strong",name_)}{tag}</Frame>'
            f'{T(11,"regular","var:text/muted",addr,w="fill")}</Frame>'
            f'{T(12,"regular","var:text/muted",staff,w=96)}'
            f'{T(12,"regular","var:text/muted",open_h,w=126)}{I("chevron-right",16,M_IC)}</Frame>')

A3_LIST = dgroup("Branches · 3", [
    branch_row("Garki Medical Centre", "Area 3, Garki, Abuja", "24 staff", "Mon–Sat 08:00–18:00", "Branch garki", main=True),
    branch_row("Maitama Annex", "Aguiyi Ironsi Street, Maitama", "9 staff", "Mon–Fri 09:00–17:00", "Branch maitama"),
    branch_row("Wuse Clinic", "Zone 5, Wuse, Abuja", "6 staff", "Mon–Sat 08:00–16:00", "Branch wuse"),
], footer="Multi-branch is billed as one organisation, never per branch account. A member books a branch, not the company.")

A3_LIST_M = dgroup("Branches · 3", [
    branch_row_m("Garki Medical Centre", "Area 3, Garki, Abuja", "24 staff", "Mon–Sat 08:00–18:00", "Branch garki", main=True),
    branch_row_m("Maitama Annex", "Aguiyi Ironsi Street, Maitama", "9 staff", "Mon–Fri 09:00–17:00", "Branch maitama"),
    branch_row_m("Wuse Clinic", "Zone 5, Wuse, Abuja", "6 staff", "Mon–Sat 08:00–16:00", "Branch wuse"),
], footer="Billed as one organisation, never per branch.")

A3_ADD = dcard(
    field("Branch name", "building-2", "Kubwa Clinic")
    + field("Address", "map-pin", "Phase 2, Kubwa, Abuja")
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Opens","clock","08:00",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Closes","clock","18:00",ph=False)}</Frame></Frame>'
    + dtoggle("share-2", "Show this branch on Medra", sub="Members can find and book it", on=True, name="Branch public")
    + dcta("Add branch", "Save branch A3", "plus"))

addx("Setup", "A3-branches",
    o_desk("Org · Setup — A3 Branches", ("Settings", "Branches"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Where you",False),("see people",True)],26)}'
        f'{dbtn("Add a branch","Add branch A3","plus","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{A3_LIST}</Frame>'
        f'<Frame w={{360}} flex="col" gap={{14}}>{A3_ADD}</Frame></Frame>',
        NAV["Settings"], badges=BADGES),
    o_head("Branches", "3 locations", ctx="Garki Medical Centre",
           stats=[("3", "Branches"), ("39", "Staff"), ("1", "Main")]),
    pinned=A3_LIST_M,
    sections=[("add", "plus", "Add a branch", "Name, address, hours, visibility", None, None, A3_ADD, None)],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- A4 plan & seats
A4_SIZE = dcard(
    eyerow("Tell us your size — it sets the price, nothing else")
    + stepper_ctl("Practitioners", 12, "Size practitioners", helper="Doctors and consultants who see members")
    + stepper_ctl("Branches", 3, "Size branches")
    + stepper_ctl("Clinical support seats", 14, "Size support", helper="Nursing, laboratory and pharmacy")
    + stepper_ctl("Front desk seats", 5, "Size desk")
    + field("Members seen a month, roughly", "users", "1,400", ph=False,
            helper="Only used to recommend a plan. It never limits anything."))

def plan_card(title, price, sub, feats, name, sel=False):
    st = ('stroke="var:border/accent" strokeWidth={2}' if sel else 'stroke="var:border/subtle" strokeWidth={1}')
    tag = (f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} image="assets/img/btn-amber.jpg" '
           f'overflow="hidden">{T(10,"semibold","var:text/on-dark","Recommended")}</Frame>') if sel else ''
    rows = "".join(f'<Frame w="fill" flex="row" gap={{9}} items="start" py={{4}}>{I("check",14,OK_IC)}'
                   f'{T(12,"regular","var:text/default",f,w="fill")}</Frame>' for f in feats)
    return (f'<Frame name="Btn {name}" grow={{1}} flex="col" gap={{12}} p={{18}} rounded={{18}} '
            f'bg="var:bg/base" {st}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(15,"bold","var:text/strong",title)}{tag}</Frame>'
            f'<Frame w="fill" flex="col" gap={{2}}>{T(26,"bold","var:text/strong",price)}'
            f'{T(11,"regular","var:text/muted",sub,w="fill")}</Frame>{rows}</Frame>')

A4_PLANS = (f'<Frame w="fill" flex="row" gap={{12}} items="start">'
            + plan_card("Practice", "₦120,000", "per month", ["Up to 10 practitioners", "1 branch", "All departments", "Staff roles and allocation"], "Plan practice")
            + plan_card("Group", "₦280,000", "per month", ["Up to 30 practitioners", "Up to 3 branches", "Multi-branch day view", "Reports"], "Plan group", sel=True)
            + plan_card("Enterprise", "Custom", "talk to us", ["Unlimited practitioners", "Unlimited branches", "SSO", "Dedicated support"], "Plan enterprise")
            + '</Frame>')

A4_SEATS = dgroup("What you are buying", [
    kpi_line("Group plan", "₦280,000"),
    kpi_line("12 practitioners — 2 over the plan", "+ ₦16,000"),
    kpi_line("14 clinical support seats", "Included"),
    kpi_line("5 front desk seats", "Included"),
    kpi_line("Total each month", "₦296,000", "ok"),
], footer="Support and front-desk seats are priced below a practitioner seat. They are what makes the record complete — pricing them like a consultant would defeat the point of having them.")

A4_TRIAL = alert_strip("sparkles", "Free trial · 26 days left",
    "Nothing is charged until 5 March. You can change plan or cancel at any point and keep everything you have entered.", "info")

addx("Setup", "A4-plan",
    o_desk("Org · Setup — A4 Plan &amp; Seats", ("Money", "Plan and seats"),
        f'{dhead([("Priced by",False),("your size",True)],26)}'
        f'{T(14,"regular","var:text/muted","Seats live inside departments, not with named people. When a technician leaves, the seat stays.",w="fill")}'
        f'{A4_PLANS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{A4_SIZE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{A4_SEATS}{A4_TRIAL}'
        f'{dcta("Confirm plan","Save plan A4","check")}</Frame></Frame>',
        NAV["Settings"], badges=BADGES),
    o_head("Plan and seats", "Group · ₦296,000 a month",
           stats=[("12", "Practitioners"), ("3", "Branches"), ("26d", "Trial")]),
    pinned=A4_TRIAL,
    sections=[
      ("plans", "layers", "Plans", "Practice, Group and Enterprise", "3", None, A4_PLANS, None),
      ("size", "sliders-horizontal", "Your size", "It sets the price, nothing else", None, None, A4_SIZE, None),
      ("seats", "receipt", "What you are buying", "₦296,000 each month", None, None, A4_SEATS, None),
    ],
    foot=dcta("Confirm plan", "Save plan A4", "check"),
    tab_items=TAB_ADMIN, tab=4)

# ---------------- A5 public profile
A5_PROFILE = dcard(
    f'<Frame w="fill" flex="row" gap={{14}} items="center">'
    f'<Frame w={{72}} h={{72}} rounded={{20}} bg="var:bg/muted" flex="col" justify="center" '
    f'items="center">{I("building-2",32,A_IC)}</Frame>'
    f'<Frame grow={{1}} flex="col" gap={{4}}>'
    f'<Frame flex="row" gap={{8}} items="center">{T(19,"bold","var:text/strong","Garki Medical Centre")}'
    f'{I("badge-check",17,OK_IC)}</Frame>'
    f'{T(12,"regular","var:text/muted","Hospital · RC 1489302 · licence verified 6 February 2026")}</Frame>'
    f'{dbtn("Change logo","Change logo A5","camera","ghost",grow=False,size="sm")}</Frame>'
    + field("About this organisation", "file-text",
            "A 40-bed general hospital in Area 3 with an in-house laboratory and pharmacy, open six days a week.",
            ph=False, helper="Members read this before they book. Two sentences beat two paragraphs.")
    + field_chips("Services offered", ["Consulting", "Laboratory", "Pharmacy", "Imaging", "Day surgery"], 0, "Svc")
    + field("Contact number members see", "phone", "+234 803 555 0110", ph=False)
    + dtoggle("share-2", "List us on Medra search", sub="Members can find and book this organisation", on=True, name="Public listed"))

A5_HOW = dgroup("How members see you", [
    drow("star", "Rating", value="4.7", sub="From 302 completed visits", name="Prof rating", tone="ok"),
    drow("users", "Members seen on Medra", value="1,842", name="Prof seen", chevron=False),
    drow("clock", "Median wait to be seen", value="14 minutes", sub="Shown on your profile", name="Prof wait", chevron=False),
    drow("eye", "Preview our public page", sub="Exactly what a member sees before booking", name="Preview profile A5"),
])

A5_COMPLETE = dgroup("Profile completeness · 70%", [
    bar(70, "amber", 10),
    checklist_row(True, "Logo and about", "Both set", "Cpl about"),
    checklist_row(True, "Services and contact", "Five services listed", "Cpl svc"),
    checklist_row(False, "Photos of the building and reception", "Members are far more likely to book somewhere they can picture", "Cpl photos"),
    checklist_row(False, "Opening hours per branch", "Maitama and Wuse are still using the default", "Cpl hours"),
])

addx("Setup", "A5-profile",
    o_desk("Org · Setup — A5 Public Profile", ("Settings", "Public profile"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("What members",False),("see",True)],26)}'
        f'{dbtn("Save changes","Save profile A5","check","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{A5_PROFILE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{A5_COMPLETE}{A5_HOW}</Frame></Frame>',
        NAV["Settings"], badges=BADGES),
    o_head("Public profile", "Garki Medical Centre · verified", back=False,
           stats=[("70%", "Complete"), ("4.7", "Rating"), ("1,842", "Seen")],
           right=f'<Frame name="Btn Save profile A5" w={{36}} h={{36}} rounded={{12}} bg="#2E3640" flex="col" justify="center" items="center">{I("check",17,W_IC)}</Frame>'),
    pinned=A5_COMPLETE,
    sections=[
      ("edit", "pencil", "Edit the profile", "Logo, about, services, contact", None, None, A5_PROFILE, None),
      ("how", "eye", "How members see you", "4.7 from 302 visits", None, "ok", A5_HOW, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# =====================================================================================
# 2. TODAY & BOOKINGS  (the admin's console)
# =====================================================================================
B_STATS = rows_of([
    stat_tile("users", "148", "Expected today", "3 branches", "teal", "Stat expected"),
    stat_tile("clock", "14 min", "Median wait", "Up 4 minutes on yesterday", "warn", "Stat wait"),
    stat_tile("calendar-x", "4", "Unassigned", "Nobody is allocated to them", "err", "Stat unassigned"),
    stat_tile("banknote", "₦1.86m", "Collected today", "Across all branches", "navy", "Stat money"),
], 4, 14)

B1_DEPTS = (f'<Frame w="fill" flex="row" gap={{12}} items="start">'
            + dept_card("clinic", 11, 12, 9, "Dept clinic", "6 consulting rooms")
            + dept_card("nursing", 6, 8, 5, "Dept nursing", "Vitals and injections")
            + dept_card("lab", 3, 4, 7, "Dept lab", "Samples waiting")
            + '</Frame>'
            + f'<Frame w="fill" flex="row" gap={{12}} items="start">'
            + dept_card("pharmacy", 2, 3, 4, "Dept pharmacy", "Prescriptions to dispense")
            + dept_card("desk", 5, 5, 12, "Dept desk", "In the waiting room")
            + f'<Frame grow={{1}} flex="col" gap={{12}} p={{16}} rounded={{16}} bg="var:bg/base" '
            + f'stroke="var:border/subtle" strokeWidth={{1}}>{dept_badge("clinic")}'
            + f'<Frame w="fill" flex="col" gap={{3}}>{T(14,"semibold","var:text/strong","Add a department")}'
            + T(11, "regular", "var:text/muted", "Imaging, physiotherapy, records — anything with its own queue", w="fill")
            + f'</Frame>{dbtn("Add","Add dept C3","plus","ghost",full=True,size="sm")}</Frame></Frame>')

B1_NEEDS = dgroup("Needs a person, not a system", [
    drow("calendar-x", "4 bookings with nobody assigned", sub="Earliest is 10:30 — 42 minutes away", name="Open alloc B2", tone="err"),
    drow("share-2", "3 referrals waiting on us", sub="Oldest 19 hours; we tell members we answer in a day", name="Nav Referrals", tone="warn"),
    drow("user-plus", "2 people invited but never joined", sub="Laboratory has no one in it", name="Nav People", tone="warn"),
    drow("flask-conical", "7 samples not yet accepted", sub="Laboratory queue is the longest it has been this week", name="Open lab D5", tone="warn"),
])

B1_ASIDE = (rail_section("Across the branches",
    dcard(kpi_line("Garki", "96 expected") + kpi_line("Maitama", "34 expected")
          + kpi_line("Wuse", "18 expected") + kpi_line("No-shows so far", "6", "warn"), p=14, gap=3), None)
    + rail_section("Now in the building",
        task_row("concierge-bell", "amber", "12 in the waiting room", "Longest wait 26 minutes", "Open desk D12")
        + task_row("stethoscope", "blue", "9 with a doctor", "Across 6 rooms", "Dept clinic")
        + task_row("flask-conical", "mint", "7 at the laboratory", "3 accepted, 4 waiting", "Open lab D5"), None))

addx("Today", "B1-today",
    o_desk("Org · Today — B1 Today", ("Today", "Thursday 14 August"),
        f'{dhead([("Thursday",False),("14 August",True)],26)}'
        f'{B_STATS}{B1_NEEDS}'
        f'{T(16,"bold","var:text/strong","Departments")}{B1_DEPTS}',
        NAV["Today"], urgent=7, aside=B1_ASIDE, badges=BADGES),
    o_head("Today", "148 expected · 3 branches", back=False, ctx="All branches",
           stats=[("148", "Expected"), ("14m", "Wait"), ("4", "Unassigned")]),
    pinned=B1_NEEDS,
    sections=[
      ("depts", "layers", "Departments", "Consulting, nursing, lab, pharmacy, desk", "5", None, B1_DEPTS, None),
      ("branches", "building-2", "Across the branches", "Garki 96 · Maitama 34 · Wuse 18", "3", None,
       dcard(kpi_line("Garki", "96 expected") + kpi_line("Maitama", "34 expected")
             + kpi_line("Wuse", "18 expected") + kpi_line("No-shows so far", "6", "warn"), p=14, gap=3), None),
      ("now", "activity", "Now in the building", "12 waiting · 9 with a doctor", None, None,
       task_row("concierge-bell", "amber", "12 in the waiting room", "Longest wait 26 minutes", "Open desk D12")
       + task_row("stethoscope", "blue", "9 with a doctor", "Across 6 rooms", "Dept clinic")
       + task_row("flask-conical", "mint", "7 at the laboratory", "3 accepted, 4 waiting", "Open lab D5"), None),
    ],
    sheets=[("quick", "zap", "Quick actions", "Register, allocate, refer", None, "Quick actions",
             "Garki Medical Centre · 09:12",
             f'{sheet_pick("user-plus","Register a walk-in","Someone at the desk with no booking","Open walkin D13")}'
             f'{sheet_pick("calendar-x","Allocate the 4 unassigned","Earliest is 10:30","Open alloc B2","err")}'
             f'{sheet_pick("share-2","Refer a member out","To an organisation or a practitioner","Open refer E2")}'
             f'{sheet_pick("link","Issue a single-use link","For a lab that is not on Medra","Open links E6","info")}', None)],
    tab_items=TAB_ADMIN, tab=0)

# ---------------- B2 bookings & allocation
def alloc_row(time, who, meta, reason, nm, assigned=None, tone=None):
    tag = (f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{5}} rounded={{8}} bg="var:state/success-bg">'
           f'{I("user-check",12,OK_IC)}{T(11,"semibold","var:state/success",assigned)}</Frame>' if assigned else
           f'<Frame flex="row" gap={{7}} items="center" px={{10}} py={{5}} rounded={{8}} bg="var:state/error-bg">'
           f'{I("user-x",12,ERR_IC)}{T(11,"semibold","var:state/error","Nobody assigned")}</Frame>')
    act = (dbtn("Change", "Change " + nm, "repeat", "ghost", grow=False, size="sm") if assigned
           else dbtn("Assign", "Assign " + nm, "user-plus", "navy", grow=False, size="sm"))
    return (f'<Frame name="Btn {nm}" w="fill" flex="col" gap={{9}} p={{13}} rounded={{14}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{12}} items="center">'
            f'<Frame w={{54}} flex="col" gap={{1}} items="center">{T(14,"bold","var:text/strong",time)}'
            f'{T(9,"regular","var:text/muted","30 min")}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame>{tag}{act}</Frame>'
            f'<Frame w="fill" flex="row" gap={{8}} items="center" px={{11}} py={{8}} rounded={{10}} '
            f'bg="var:neutral/50">{I("file-text",12,M_IC)}'
            f'{T(11,"regular","var:text/muted",reason,w="fill")}</Frame></Frame>')

B2_UNASSIGNED = dgroup("Nobody assigned · 4", [
    alloc_row("10:30", "Amara Okeke · MDR-8842-19", "Paid ₦15,000 · in person · Garki",
              "“Hypertension follow-up, headaches in the afternoon.”", "Alloc Amara"),
    alloc_row("11:00", "Musa Ibrahim · MDR-7714-02", "Paid ₦20,000 · virtual · first visit",
              "“Chest tightness when I climb stairs.”", "Alloc Musa"),
    alloc_row("11:30", "Halima Sani · MDR-9012-44", "Paid ₦15,000 · in person · Maitama",
              "“Blood pressure check.”", "Alloc Halima"),
    alloc_row("14:00", "Emeka Nwosu · MDR-4410-07", "Paid ₦15,000 · virtual", "“Follow-up on the knee.”", "Alloc Emeka"),
], footer="A booking with nobody assigned is the one thing on this console that becomes a complaint if it is left. They are sorted by how soon they start, not by when they arrived.")

B2_ASSIGNED = dgroup("Assigned · 12 of 16", [
    alloc_row("09:00", "Fatima Bello · MDR-2201-13", "Seen · signed 09:28", "Asthma review", "Alloc Fatima", assigned="Dr. Okafor"),
    alloc_row("09:30", "Chidi Okeke · MDR-8842-20", "With the doctor now", "Cough for four days", "Alloc Chidi", assigned="Dr. Eze"),
    alloc_row("10:00", "Grace Okeke · MDR-8842-21", "Waiting · arrived 09:47", "Review after blood sugar test", "Alloc Grace", assigned="Dr. Okafor"),
])

B2_ASIDE = (rail_section("Who is free",
    dcard(drow("stethoscope", "Dr. Ngozi Okafor", value="2 free", sub="Cardiology · Garki", name="Free okafor")
          + drow("stethoscope", "Dr. Chuka Eze", value="4 free", sub="General practice · Garki", name="Free eze")
          + drow("stethoscope", "Dr. Kemi Adeyemi", value="1 free", sub="Paediatrics · Maitama", name="Free kemi")
          + drow("stethoscope", "Dr. Tunde Bello", value="Full", sub="Neurology · Wuse", name="Free bello", tone="warn"), p=14, gap=2), None)
    + alert_strip("zap", "Assign automatically?",
        "Match on specialty, branch and the first free slot. You keep an override on every one.",
        "info", dbtn("Rules", "Alloc rules B2", None, "ghost", grow=False, size="sm")))

addx("Today", "B2-bookings",
    o_desk("Org · Today — B2 Bookings &amp; Allocation", ("Bookings", "Allocation"),
        f'{dhead([("Four bookings",False),("have nobody",True)],26)}'
        f'{T(14,"regular","var:text/muted","The earliest starts in 42 minutes. Members were told a doctor would be waiting.",w="fill")}'
        f'{B2_UNASSIGNED}{B2_ASSIGNED}',
        NAV["Bookings"], urgent=7, aside=B2_ASIDE, badges=BADGES),
    o_head("Bookings", "4 unassigned · 16 today", back=False, ctx="All branches",
           stats=[("16", "Today"), ("4", "Unassigned"), ("3", "Free now")],
           chips=[("Unassigned", "Filter unassigned", True), ("Assigned", "Filter assigned", False), ("Done", "Filter done", False)]),
    pinned=dgroup("Nobody assigned · 4", [
        drow("user-x", "10:30 · Amara Okeke", sub="Paid · in person · Garki · starts in 42 minutes", name="Alloc Amara", tone="err"),
        drow("user-x", "11:00 · Musa Ibrahim", sub="Paid · virtual · first visit", name="Alloc Musa", tone="err"),
        drow("user-x", "11:30 · Halima Sani", sub="Paid · in person · Maitama", name="Alloc Halima", tone="warn"),
        drow("user-x", "14:00 · Emeka Nwosu", sub="Paid · virtual", name="Alloc Emeka", tone="warn"),
    ], footer="Sorted by how soon they start, not by when they arrived."),
    sections=[
      ("unassigned", "user-x", "The four in full", "Reason for the visit and what they paid", "4", "err",
       dgroup("Nobody assigned · 4", [
         alloc_row_m("10:30", "Amara Okeke", "Paid ₦15,000 · in person · Garki", "“Hypertension follow-up, headaches in the afternoon.”", "Alloc Amara"),
         alloc_row_m("11:00", "Musa Ibrahim", "Paid ₦20,000 · virtual · first visit", "“Chest tightness when I climb stairs.”", "Alloc Musa"),
         alloc_row_m("11:30", "Halima Sani", "Paid ₦15,000 · in person · Maitama", "“Blood pressure check.”", "Alloc Halima"),
         alloc_row_m("14:00", "Emeka Nwosu", "Paid ₦15,000 · virtual", "“Follow-up on the knee.”", "Alloc Emeka"),
       ], footer="Sorted by how soon they start."), None),
      ("assigned", "user-check", "Already assigned", "12 of 16 have a practitioner", "12", None,
       dgroup("Assigned · 12 of 16", [
         alloc_row_m("09:00", "Fatima Bello", "Seen · signed 09:28", "Asthma review", "Alloc Fatima", assigned="Dr. Okafor"),
         alloc_row_m("09:30", "Chidi Okeke", "With the doctor now", "Cough for four days", "Alloc Chidi", assigned="Dr. Eze"),
         alloc_row_m("10:00", "Grace Okeke", "Waiting · arrived 09:47", "Review after blood sugar test", "Alloc Grace", assigned="Dr. Okafor"),
       ]), None),
      ("free", "stethoscope", "Who is free", "Three practitioners have space", "3", None,
       dcard(drow("stethoscope", "Dr. Ngozi Okafor", value="2 free", sub="Cardiology · Garki", name="Free okafor")
             + drow("stethoscope", "Dr. Chuka Eze", value="4 free", sub="General practice · Garki", name="Free eze")
             + drow("stethoscope", "Dr. Kemi Adeyemi", value="1 free", sub="Paediatrics · Maitama", name="Free kemi")
             + drow("stethoscope", "Dr. Tunde Bello", value="Full", sub="Neurology · Wuse", name="Free bello", tone="warn"), p=14, gap=2), None),
    ],
    sheets=[("assign", "user-plus", "Assign someone", "Pick a practitioner for 10:30", None,
             "Assign 10:30 · Amara Okeke", "Cardiology · in person · Garki",
             f'{sheet_pick("stethoscope","Dr. Ngozi Okafor","Cardiology · 2 slots free · same branch","Pick okafor","ok")}'
             f'{sheet_pick("stethoscope","Dr. Chuka Eze","General practice · 4 slots free","Pick eze")}'
             f'{sheet_pick("zap","Let Medra choose","Specialty, branch, first free slot","Alloc rules B2","info")}', None)],
    tab_items=TAB_ADMIN, tab=1)

# ---------------- B3 member lookup
B3_SEARCH = dcard(
    field("Search by name, phone or Medra ID", "search", "MDR-8842", ph=False, focus=True,
          helper="A member's Medra ID is on their phone and on any printed summary. It is the fastest way to find the right person.")
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Scan their QR code", "Scan member B3", "qr-code", "ghost")
    + dbtn("Register a walk-in", "Open walkin D13", "user-plus", "navy") + '</Frame>')

B3_RESULTS = dgroup("3 matches", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "34 · Garki · last seen today 09:12", "Open", "Open Amara"),
    patient_row("avatar-6.jpg", "Chidi Okeke", "MDR-8842-20", "6 · dependant of Amara Okeke · last seen 12 Jun", "Open", "Open Chidi", tag="new"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "68 · Kubwa · last seen 3 Aug", "Open", "Open Grace"),
], footer="An organisation only sees a member's record while they are in its care, and only what the member has shared. Searching finds the person, not their history.")

B3_CANT = dgroup("Cannot find them?", [
    drow("user-plus", "They have never used Medra", sub="Register them at the desk — it takes about a minute", name="Open walkin D13"),
    drow("phone", "Search by phone number", sub="Works if they registered with it", name="Search phone"),
    drow("shield-question", "They are here but unconscious", sub="Emergency access needs a reason and tells the member afterwards", name="Break glass B3", tone="err"),
])

addx("Today", "B3-find",
    o_desk("Org · Today — B3 Find a Member", ("Today", "Find a member"),
        f'{dhead([("Find",False),("a member",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{B3_SEARCH}{B3_RESULTS}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{B3_CANT}</Frame></Frame>',
        NAV["Today"], badges=BADGES),
    o_head("Find a member", "Name, phone or Medra ID", back=False,
           right=f'<Frame name="Btn Scan member B3" w={{36}} h={{36}} rounded={{12}} bg="#2E3640" flex="col" justify="center" items="center">{I("qr-code",17,W_IC)}</Frame>'),
    pinned=f'{B3_SEARCH}{B3_RESULTS}',
    sections=[("cant", "circle-help", "Cannot find them?", "Register, search by phone, or emergency access", "3", None, B3_CANT, None)],
    tab_items=TAB_ADMIN, tab=1)

# =====================================================================================
# 3. DEPARTMENTS & PEOPLE  (Module 10.3 — departments are the unit, not individuals)
# =====================================================================================
C1_GRID = (f'<Frame w="fill" flex="row" gap={{12}} items="start">'
           + dept_card("clinic", 11, 12, 9, "Dept clinic", "Doctors and consultants")
           + dept_card("nursing", 6, 8, 5, "Dept nursing", "Vitals, injections, observations")
           + '</Frame><Frame w="fill" flex="row" gap={{12}} items="start">'
           + dept_card("lab", 3, 4, 7, "Dept lab", "Tests ordered and returned")
           + dept_card("pharmacy", 2, 3, 4, "Dept pharmacy", "Dispensing against prescriptions")
           + '</Frame><Frame w="fill" flex="row" gap={{12}} items="start">'
           + dept_card("desk", 5, 5, 12, "Dept desk", "Registration, check-in, payment")
           + f'<Frame grow={{1}} flex="col" gap={{12}} p={{16}} rounded={{16}} bg="var:bg/base" '
           + f'stroke="var:border/subtle" strokeWidth={{1}}>{dept_badge("clinic")}'
           + f'<Frame w="fill" flex="col" gap={{3}}>{T(14,"semibold","var:text/strong","Add a department")}'
           + T(11, "regular", "var:text/muted", "Imaging, physiotherapy, medical records", w="fill")
           + f'</Frame>{dbtn("Add a department","Add dept C3","plus","ghost",full=True,size="sm")}</Frame></Frame>')

C1_WHY = dgroup("Why departments and not people", [
    drow("layers", "You buy seats, not licences for names", sub="When a technician leaves, the seat stays and you reassign it", name="Why seats", chevron=False),
    drow("shield-check", "Permissions follow the department", sub="Nobody carries access from a job they no longer do", name="Why perms", chevron=False),
    drow("inbox", "Work is routed to a department, never a person", sub="An order sits in the laboratory queue, so nothing waits on one individual being at work", name="Why route", chevron=False),
], footer="This is also why the price follows practitioners, branches and seats — the unit of billing and the unit of administration are the same thing.")

C1_ASIDE = (rail_section("Seats",
    dcard(kpi_line("Practitioner seats", "11 of 12") + kpi_line("Clinical support", "11 of 15")
          + kpi_line("Front desk", "5 of 5", "warn") + kpi_line("Unassigned seats", "5", "ok"), p=14, gap=3), None)
    + alert_strip("triangle-alert", "Front desk is full",
        "Every front-desk seat is in use. Add seats before you invite anyone else to that department.",
        "warn", dbtn("Add seats", "Open plan A4", None, "ghost", grow=False, size="sm")))

addx("People", "C1-departments",
    o_desk("Org · People — C1 Departments", ("Departments",),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Five",False),("departments",True)],26)}'
        f'{dbtn("Add a department","Add dept C3","plus","navy",grow=False,size="sm")}</Frame>'
        f'{C1_GRID}{C1_WHY}',
        NAV["Departments"], aside=C1_ASIDE, badges=BADGES),
    o_head("Departments", "5 · 27 of 32 seats used", back=False, ctx="Garki Medical Centre",
           stats=[("5", "Departments"), ("27", "Seats used"), ("5", "Free")]),
    pinned=C1_GRID,
    sections=[
      ("why", "info", "Why departments, not people", "Seats stay when people leave", "3", None, C1_WHY, None),
      ("seats", "layers", "Seats", "27 of 32 used · front desk is full", "27", "warn",
       dcard(kpi_line("Practitioner seats", "11 of 12") + kpi_line("Clinical support", "11 of 15")
             + kpi_line("Front desk", "5 of 5", "warn") + kpi_line("Unassigned seats", "5", "ok"), p=14, gap=3)
       + alert_strip("triangle-alert", "Front desk is full", "Add seats before inviting anyone else there.", "warn",
                     dbtn("Add seats", "Open plan A4", None, "ghost", grow=False, size="sm")), None),
    ],
    tab_items=TAB_ADMIN, tab=2)

# ---------------- C2 department detail
C2_PEOPLE = dgroup("People in Laboratory · 3 of 4 seats", [
    seat_row("avatar-1.jpg", "Mr. Sola Adeniyi", "Lab technician", "Laboratory", "Joined 6 Feb · 214 results entered", "Person sola"),
    seat_row("avatar-5.jpg", "Mrs. Kemi Bassey", "Lab technician", "Laboratory", "Joined 12 Feb · 96 results entered", "Person kemi"),
    seat_row("avatar-6.jpg", "Mr. Tunde Alabi", "Laboratory lead", "Laboratory", "Joined 6 Feb · can accept and reject samples", "Person tunde"),
    seat_row("avatar-3.jpg", "Invited: chidera@garki.ng", "Lab technician", "Laboratory", "Invited 3 days ago · not yet joined", "Person chidera", state="invited"),
], footer="One seat is free. Anyone you invite into it inherits the laboratory's permissions and nothing else.")

C2_QUEUE = dgroup("What the laboratory is holding", [
    drow("flask-conical", "Orders waiting to be accepted", value="4", sub="Oldest 41 minutes", name="Open lab D5", tone="warn"),
    drow("beaker", "Samples in progress", value="3", name="Lab progress"),
    drow("send", "Results entered today", value="11", sub="All released by a doctor", name="Lab done", tone="ok"),
    drow("triangle-alert", "Samples rejected", value="1", sub="Haemolysed — the member has been asked to return", name="Open lab D8", tone="err"),
])

C2_PERMS = dgroup("What this department can do", [
    perm_row("Receive test orders addressed to it", True),
    perm_row("Read the clinical detail attached to an order", True, "Only the detail on the order — not the member's whole record"),
    perm_row("Enter a structured result", True),
    perm_row("Release a result to the member", False, "A doctor releases. An out-of-range value arriving on a phone with nobody to explain it is a harm, not a feature"),
    perm_row("See a member's consultation notes", False, "Nothing in a note changes how a test is run"),
])

addx("People", "C2-department",
    o_desk("Org · People — C2 Department", ("Departments", "Laboratory"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame flex="row" gap={{13}} items="center">{dept_badge("lab",44)}'
        f'{dhead([("Laboratory",True)],26)}</Frame>'
        f'{dbtn("Invite someone","Open invite C5","user-plus","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C2_PEOPLE}{C2_PERMS}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{C2_QUEUE}</Frame></Frame>',
        NAV["Departments"], dept="Laboratory", badges=BADGES),
    o_head("Laboratory", "3 of 4 seats · 4 orders waiting",
           stats=[("3/4", "Seats"), ("4", "Waiting"), ("11", "Done today")]),
    pinned=C2_QUEUE,
    sections=[
      ("people", "users", "People in this department", "Three joined, one invited", "4", None,
       dgroup("People in Laboratory · 3 of 4 seats", [
         seat_row_m("avatar-1.jpg", "Mr. Sola Adeniyi", "Lab technician", "Laboratory", "Person sola"),
         seat_row_m("avatar-5.jpg", "Mrs. Kemi Bassey", "Lab technician", "Laboratory", "Person kemi"),
         seat_row_m("avatar-6.jpg", "Mr. Tunde Alabi", "Laboratory lead", "Laboratory", "Person tunde"),
         seat_row_m("avatar-3.jpg", "chidera@garki.ng", "Lab technician", "Laboratory", "Person chidera", state="invited"),
       ], footer="One seat is free. Anyone you invite inherits the laboratory's permissions and nothing else."), None),
      ("perms", "shield-check", "What this department can do", "And what it deliberately cannot", "5", None, C2_PERMS, None),
    ],
    foot=dbtn("Invite someone", "Open invite C5", "user-plus", "navy", full=True),
    tab_items=TAB_ADMIN, tab=2)

# ---------------- C3 add a department
C3_FORM = dcard(
    field_chips("What kind of department?", ["Consulting", "Nursing", "Laboratory", "Pharmacy", "Front desk"], 2, "Dept kind")
    + field("Name members and staff will see", "layers", "Imaging", ph=False)
    + field("Which branch?", "building-2", "Garki Medical Centre", ph=False, trailing=("chevron-down", "Dept branch"))
    + stepper_ctl("Seats to start with", 3, "Dept seats", helper="You can add more at any time; the price updates live")
    + dtoggle("inbox", "This department receives orders", sub="Doctors can send tests or requests to it", on=True, name="Dept orders")
    + dtoggle("share-2", "Show on our public page", sub="Members can see the service is offered here", on=True, name="Dept public"))

C3_PRESET = dgroup("What it will be able to do", [
    perm_row("Receive orders addressed to it", True),
    perm_row("Enter a structured result against a template", True),
    perm_row("Release a result to the member", False, "A doctor releases"),
    perm_row("See consultation notes", False),
], footer="Preset by department kind. You can tighten it afterwards, but not loosen the two denials — they are platform rules, not settings.")

addx("People", "C3-add-dept",
    o_desk("Org · People — C3 Add a Department", ("Departments", "New department"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Departments")}</Frame>'
        f'{dhead([("Add a",False),("department",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C3_FORM}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{C3_PRESET}'
        f'{dcta("Create department","Save dept C3","check")}</Frame></Frame>',
        NAV["Departments"], badges=BADGES),
    o_head("Add a department", "Imaging · Garki", stats=[("3", "Seats"), ("Lab", "Kind"), ("Garki", "Branch")]),
    pinned=C3_FORM,
    sections=[("perms", "shield-check", "What it will be able to do", "Preset by department kind", "4", None, C3_PRESET, None)],
    foot=dcta("Create department", "Save dept C3", "check"),
    tab_items=TAB_ADMIN, tab=2)

# ---------------- C4 people directory
C4_LIST = dgroup("Everyone · 27", [
    seat_row("avatar-4.jpg", "Dr. Ngozi Okafor", "Doctor", "Consulting", "Cardiology · MDCN 71482 · Garki", "Person okafor"),
    seat_row("avatar-1.jpg", "Dr. Chuka Eze", "Doctor", "Consulting", "General practice · MDCN 60112 · Garki", "Person eze"),
    seat_row("avatar-2.jpg", "Sister Ifeoma Uche", "Nurse", "Nursing", "RN 22841 · Garki · 41 vitals today", "Person ifeoma"),
    seat_row("avatar-1.jpg", "Mr. Sola Adeniyi", "Lab technician", "Laboratory", "MLSCN 9931 · Garki", "Person sola"),
    seat_row("avatar-6.jpg", "Mr. Bayo Ogun", "Pharmacist", "Pharmacy", "PCN 4471 · Garki", "Person bayo"),
    seat_row("avatar-3.jpg", "Miss Ngozi Peter", "Front desk", "Front desk", "Garki · 62 check-ins today", "Person ngozi"),
    seat_row("avatar-5.jpg", "chidera@garki.ng", "Lab technician", "Laboratory", "Invited 3 days ago", "Person chidera", state="invited"),
    seat_row("avatar-2.jpg", "Mr. Emeka Obi", "Front desk", "Front desk", "Suspended 2 Aug · left the organisation", "Person emeka", state="suspended"),
], footer="A suspended person keeps nothing. Their seat returns to the department the moment you suspend them, and every record they opened stays in the audit log.")

C4_LIST_M = dgroup("Everyone · 27", [
    seat_row_m("avatar-4.jpg", "Dr. Ngozi Okafor", "Doctor", "Consulting", "Person okafor"),
    seat_row_m("avatar-2.jpg", "Sister Ifeoma Uche", "Nurse", "Nursing", "Person ifeoma"),
    seat_row_m("avatar-1.jpg", "Mr. Sola Adeniyi", "Lab technician", "Laboratory", "Person sola"),
    seat_row_m("avatar-6.jpg", "Mr. Bayo Ogun", "Pharmacist", "Pharmacy", "Person bayo"),
    seat_row_m("avatar-3.jpg", "Miss Ngozi Peter", "Front desk", "Front desk", "Person ngozi"),
    seat_row_m("avatar-5.jpg", "chidera@garki.ng", "Lab technician", "Laboratory", "Person chidera", state="invited"),
])

C4_FILTERS = rows_of([
    dbtn("Everyone", "Filter all", None, "navy", size="sm"),
    dbtn("Doctors", "Filter doctors", None, "ghost", size="sm"),
    dbtn("Nursing", "Filter nursing", None, "ghost", size="sm"),
    dbtn("Laboratory", "Filter lab", None, "ghost", size="sm"),
    dbtn("Pharmacy", "Filter pharmacy", None, "ghost", size="sm"),
    dbtn("Front desk", "Filter desk", None, "ghost", size="sm"),
], 6, 8)

C4_ASIDE = (rail_section("Needs you",
    dcard(drow("mail", "2 invitations never accepted", sub="Oldest 3 days", name="Filter invited", tone="warn")
          + drow("badge-alert", "1 credential expiring", sub="Dr. Eze's licence expires in 21 days", name="Person eze", tone="warn")
          + drow("user-x", "1 suspended person", sub="Mr. Emeka Obi · seat returned", name="Person emeka"), p=14, gap=2), None)
    + rail_section("Add someone",
        dbtn("Invite into a department", "Open invite C5", "user-plus", "navy", full=True, size="sm")
        + dbtn("Import a staff list", "Import staff C4", "upload", "ghost", full=True, size="sm"), None))

addx("People", "C4-people",
    o_desk("Org · People — C4 People", ("People",),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Twenty-seven",False),("people",True)],26)}'
        f'{dbtn("Invite someone","Open invite C5","user-plus","navy",grow=False,size="sm")}</Frame>'
        f'{C4_FILTERS}{C4_LIST}',
        NAV["People"], aside=C4_ASIDE, badges=BADGES),
    o_head("People", "27 · 2 invitations pending", back=False, ctx="Garki Medical Centre",
           stats=[("27", "People"), ("2", "Invited"), ("1", "Suspended")],
           chips=[("Everyone", "Filter all", True), ("Doctors", "Filter doctors", False), ("Support", "Filter support", False)]),
    pinned=C4_LIST_M,
    sections=[
      ("needs", "bell", "Needs you", "Invitations, credentials, suspensions", "4", "warn",
       dcard(drow("mail", "2 invitations never accepted", sub="Oldest 3 days", name="Filter invited", tone="warn")
             + drow("badge-alert", "1 credential expiring", sub="Dr. Eze's licence expires in 21 days", name="Person eze", tone="warn")
             + drow("user-x", "1 suspended person", sub="Mr. Emeka Obi · seat returned", name="Person emeka"), p=14, gap=2), None),
    ],
    foot=dbtn("Invite someone", "Open invite C5", "user-plus", "navy", full=True),
    tab_items=TAB_ADMIN, tab=2)

# ---------------- C5 invite
C5_FORM = dcard(
    field("Their work email or phone", "mail", "chidera@garki.ng", ph=False,
          helper="We send the invitation there. They set their own password and prove their own identity — you never hold it.")
    + field_chips("Which department?", ["Consulting", "Nursing", "Laboratory", "Pharmacy", "Front desk"], 2, "Inv dept")
    + field_chips("Role in that department", ["Technician", "Department lead"], 0, "Inv role")
    + field("Which branch?", "building-2", "Garki Medical Centre", ph=False, trailing=("chevron-down", "Inv branch"))
    + field("Professional registration number", "badge-check", "MLSCN 9931", ph=False,
            helper="Checked against the register before they can pick up work. A clinical seat is never active on trust alone."))

C5_WHAT = dgroup("What they will be able to do", [
    perm_row("See orders addressed to the laboratory", True),
    perm_row("Enter results against the test template", True),
    perm_row("Release a result to a member", False, "A doctor releases"),
    perm_row("Open a member's consultation notes", False),
    perm_row("See any branch other than Garki", False, "Scope follows the branch you pick"),
], footer="They inherit the department's permissions. There is no per-person permission editing — that is how organisations end up with someone holding access nobody remembers granting.")

C5_STEPS = dgroup("What happens next", [
    prep_step(1, "They get the invitation", "Email and SMS, valid for 7 days"),
    prep_step(2, "They verify themselves", "NIN and their registration number"),
    prep_step(3, "The seat becomes active", "You are told; they appear in the department"),
], footer="Until step 3 they cannot see anything at all, and the seat is only counted once they join.")

addx("People", "C5-invite",
    o_desk("Org · People — C5 Invite Someone", ("People", "Invite"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","People")}</Frame>'
        f'{dhead([("Invite someone",False),("into a department",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C5_FORM}{C5_STEPS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{C5_WHAT}'
        f'{dcta("Send the invitation","Send invite C5","send")}</Frame></Frame>',
        NAV["People"], badges=BADGES),
    o_head("Invite someone", "Into Laboratory · Garki", stats=[("1", "Seat free"), ("7d", "Valid"), ("Lab", "Department")]),
    pinned=C5_FORM,
    sections=[
      ("what", "shield-check", "What they will be able to do", "And what they cannot", "5", None, C5_WHAT, None),
      ("next", "list-checks", "What happens next", "Invite, verify, seat activates", "3", None, C5_STEPS, None),
    ],
    foot=dcta("Send the invitation", "Send invite C5", "send"),
    tab_items=TAB_ADMIN, tab=2)

# ---------------- C6 person detail
C6_HEAD = dcard(
    f'<Frame w="fill" flex="row" gap={{14}} items="center">'
    f'<Image image="assets/img/avatar-2.jpg" w={{62}} h={{62}} rounded={{18}} />'
    f'<Frame grow={{1}} flex="col" gap={{4}}>'
    f'<Frame flex="row" gap={{8}} items="center">{T(19,"bold","var:text/strong","Sister Ifeoma Uche")}'
    f'{I("badge-check",17,OK_IC)}</Frame>'
    f'{T(12,"regular","var:text/muted","Nurse · Nursing · Garki Medical Centre · RN 22841 · NIN confirmed")}</Frame>'
    f'{dbtn("Message","Msg ifeoma","message-circle","ghost",grow=False,size="sm")}</Frame>'
    + rows_of([kv("Joined", "6 Feb 2026", "calendar-days"), kv("Seat", "Nursing", "layers"),
               kv("Branch", "Garki", "building-2"), kv("Last active", "4 min ago", "activity")], 4, 12))

C6_ACTIVITY = dgroup("What she has done today", [
    drow("activity", "41 sets of vitals recorded", sub="Across consulting and the day ward", name="Act vitals", chevron=False, tone="ok"),
    drow("syringe", "9 injections administered", sub="Each one signed and timestamped", name="Act inject", chevron=False),
    drow("triangle-alert", "2 escalations to a doctor", sub="One BP 178/104, one chest pain", name="Act escalate", tone="warn"),
    drow("clipboard-list", "18 member records opened", sub="All within an episode of care", name="Open audit F2"),
])

C6_SCOPE = dgroup("What she can see", [
    perm_row("Members assigned to today's clinic at Garki", True, "Access ends when the visit is marked complete"),
    perm_row("Record vitals, injections and observations", True),
    perm_row("Escalate to the doctor on duty", True),
    perm_row("Diagnose, prescribe or sign a note", False, "That is the doctor's signature, and it carries their MDCN number"),
    perm_row("Members at Maitama or Wuse", False, "Scope follows her branch"),
])

C6_DANGER = dgroup("Managing this seat", [
    drow("repeat", "Move to another department", sub="The seat goes with the department, not with her", name="Move ifeoma"),
    drow("building-2", "Change branch", value="Garki", name="Branch ifeoma"),
    drow("pause", "Suspend", sub="Access stops immediately; the seat returns to Nursing", name="Suspend ifeoma", tone="warn"),
    drow("user-x", "Remove from the organisation", sub="Everything she recorded stays in the record and the audit log", name="Remove ifeoma", tone="err"),
])

addx("People", "C6-person",
    o_desk("Org · People — C6 Person", ("People", "Sister Ifeoma Uche"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","People")}</Frame>'
        f'{C6_HEAD}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C6_ACTIVITY}{C6_SCOPE}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>{C6_DANGER}</Frame></Frame>',
        NAV["People"], dept="Nursing", badges=BADGES),
    o_head("Sister Ifeoma Uche", "Nurse · Nursing · Garki",
           stats=[("41", "Vitals"), ("9", "Injections"), ("2", "Escalations")]),
    pinned=C6_HEAD,
    sections=[
      ("activity", "activity", "What she has done today", "41 vitals, 9 injections", None, None, C6_ACTIVITY, None),
      ("scope", "shield-check", "What she can see", "And what she cannot", "5", None, C6_SCOPE, None),
      ("manage", "settings", "Managing this seat", "Move, suspend or remove", "4", None, C6_DANGER, None),
    ],
    tab_items=TAB_ADMIN, tab=2)

# ---------------- C7 roles & permissions
C7_MATRIX = dgroup("Who can do what", [
    drow("stethoscope", "Doctor", sub="Consult, diagnose, prescribe, order, refer, sign, release results", name="Role doctor"),
    drow("syringe", "Nurse", sub="Vitals, injections, procedures, observations, escalate", name="Role nurse"),
    drow("flask-conical", "Lab technician", sub="Accept orders, enter structured results, flag sample problems", name="Role lab"),
    drow("pill", "Pharmacist", sub="Dispense against a prescription, record what was given, flag substitutions", name="Role pharm"),
    drow("concierge-bell", "Front desk", sub="Register, check in, queue, record payment, allocate", name="Role desk"),
    drow("shield-check", "Organisation admin", sub="Departments, seats, staff, allocation, billing, referrals", name="Role admin"),
])

C7_DENIALS = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-alert",17,ERR_IC)}'
    f'{T(14,"semibold","var:text/strong","Two denials you cannot switch on")}</Frame>'
    + perm_row("Front desk reading clinical content", False,
               "They register, schedule, check in and take money. Giving the busiest, highest-turnover seat in the building a window into diagnoses is the fastest way to lose a member's trust and breach the NDPA.")
    + perm_row("A lab technician releasing a result to a member", False,
               "They enter it; a doctor releases it. An out-of-range value arriving on a phone with nobody to explain it is a harm, not a feature.")
    + T(11, "regular", "var:text/muted",
        "These are platform rules rather than settings. Every other permission on this screen is yours to tighten.", w="fill"),
    bg="var:state/error-bg", stroke=None)

C7_EPISODE = dgroup("How access ends", [
    prep_step(1, "A member arrives", "Their record opens to the people on that episode of care, and only to what they shared"),
    prep_step(2, "The visit is marked complete", "Access closes the same moment, for everyone"),
    prep_step(3, "The member can see it happened", "Every read is in their own audit trail, by name and by time"),
], footer="Access is per episode of care, never per person and never permanent. This is the one rule that makes a shared record safe to hand around a hospital.")

addx("People", "C7-roles",
    o_desk("Org · People — C7 Roles &amp; Permissions", ("People", "Roles"),
        f'{dhead([("What each role",False),("can reach",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C7_MATRIX}{C7_EPISODE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{C7_DENIALS}</Frame></Frame>',
        NAV["People"], badges=BADGES),
    o_head("Roles", "Six roles in this organisation", stats=[("6", "Roles"), ("2", "Hard denials"), ("Episode", "Scope")]),
    pinned=C7_DENIALS,
    sections=[
      ("matrix", "users", "Who can do what", "Six roles", "6", None, C7_MATRIX, None),
      ("episode", "clock", "How access ends", "Per episode of care, never permanent", "3", None, C7_EPISODE, None),
    ],
    tab_items=TAB_ADMIN, tab=2)

# =====================================================================================
# 4. THE CLINICAL CHAIN  (Module 11 — a task queue, not a copy of the doctor's app)
# =====================================================================================
def task_row_big(time, who, meta, what, nm, tone=None, action="Start", avatar="avatar-2.jpg", flags=None):
    bg = {"warn": "var:state/warning-bg", "err": "var:state/error-bg", "ok": "var:state/success-bg",
          None: "var:bg/muted"}[tone]
    c = {"warn": WARN_IC, "err": ERR_IC, "ok": OK_IC, None: A_IC}[tone]
    fl = ''
    if flags:
        ff = "".join(f'<Frame flex="row" gap={{5}} items="center" px={{8}} py={{4}} rounded={{7}} bg="{bg}">'
                     f'{I(ic,11,c)}{T(10,"semibold","var:text/default",lbl)}</Frame>' for ic, lbl in flags)
        fl = f'<Frame w="fill" flex="row" gap={{6}}>{ff}</Frame>'
    return (f'<Frame name="Btn {nm}" w="fill" flex="col" gap={{9}} p={{13}} rounded={{14}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{11}} items="center">'
            f'<Frame w={{50}} flex="col" gap={{1}} items="center">{T(13,"bold","var:text/strong",time)}</Frame>'
            f'<Image image="assets/img/{avatar}" w={{34}} h={{34}} rounded={{11}} />'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",who)}'
            f'{T(10,"regular","var:text/muted",meta,w="fill")}</Frame>'
            f'{dbtn(action, action + " " + nm, "arrow-right", "navy", grow=False, size="sm")}</Frame>{fl}'
            f'<Frame w="fill" flex="row" gap={{8}} items="center" px={{11}} py={{8}} rounded={{10}} '
            f'bg="var:neutral/50">{I("clipboard-list",12,M_IC)}'
            f'{T(11,"regular","var:text/muted",what,w="fill")}</Frame></Frame>')

# ---------------- D1–D4 NURSING
D1_QUEUE = dgroup("Waiting for you · 5", [
    task_row_big("09:40", "Amara Okeke · MDR-8842-19", "34 · before Dr. Okafor at 10:30",
                 "Vitals before the consultation", "Task amara",
                 flags=[("triangle-alert", "Penicillin allergy")], tone="err"),
    task_row_big("09:45", "Chidi Okeke · MDR-8842-20", "6 · paediatric · with his mother",
                 "Weight, temperature, then Dr. Eze", "Task chidi", avatar="avatar-6.jpg"),
    task_row_big("10:00", "Musa Ibrahim · MDR-7714-02", "44 · ordered by Dr. Okafor 09:12",
                 "Ceftriaxone 1 g IM — second of five", "Task musa", avatar="avatar-1.jpg",
                 flags=[("syringe", "Injection")], tone="warn"),
    task_row_big("10:10", "Grace Okeke · MDR-8842-21", "68 · diabetic · travelling from Kubwa",
                 "Blood pressure and blood sugar", "Task grace", avatar="avatar-3.jpg"),
    task_row_big("10:30", "Halima Sani · MDR-9012-44", "29 · post-consultation",
                 "Dressing change, then discharge", "Task halima", avatar="avatar-5.jpg"),
], footer="Ordered by when the doctor needs them, not by when they arrived. Anything a doctor is waiting on sits at the top.")

D1_DONE = dgroup("Done today · 12", [
    drow("check-check", "Fatima Bello", value="09:12", sub="Vitals · BP 118/76 · handed to Dr. Okafor", name="Done fatima", tone="ok"),
    drow("check-check", "Emeka Nwosu", value="09:24", sub="Ceftriaxone 1 g IM · signed", name="Done emeka", tone="ok"),
    drow("triangle-alert", "Blessing Ade", value="09:31", sub="BP 178/104 — escalated to Dr. Eze, seen within 4 minutes", name="Done blessing", tone="warn"),
])

D1_ASIDE = (rail_section("Standing orders",
    dcard(drow("syringe", "Ceftriaxone course", value="3 people", sub="Days 2, 3 and 5", name="SO ceftriaxone", chevron=False)
          + drow("droplet", "Fasting glucose before clinic", value="2 people", name="SO glucose", chevron=False)
          + drow("bandage", "Daily dressing", value="1 person", name="SO dressing", chevron=False), p=14, gap=2), None)
    + alert_strip("triangle-alert", "Escalate, do not wait",
        "Anything outside the range you were given goes to the doctor on duty immediately. It is never a message that waits in a queue.",
        "err", dbtn("How", "Open escalate D4", None, "ghost", grow=False, size="sm")))

addx("Chain", "D1-nursing",
    o_desk("Org · Nursing — D1 My Queue", ("Nursing", "Thursday 14 August"),
        f'{dhead([("Five people",False),("waiting for you",True)],26)}'
        f'{rows_of([stat_tile("users","5","Waiting","Next in 6 minutes","teal","Stat waiting"),stat_tile("check-check","12","Done today","41 vitals recorded","ok","Stat done"),stat_tile("syringe","9","Injections","All signed","info","Stat inject"),stat_tile("triangle-alert","2","Escalated","Both seen inside 5 minutes","warn","Stat esc")],4,14)}'
        f'{D1_QUEUE}{D1_DONE}',
        NAV["Departments"], dept="Nursing", urgent=1, aside=D1_ASIDE, who=NURSE, badges=BADGES),
    o_head("My queue", "5 waiting · next in 6 min", back=False, ctx="Nursing · Garki",
           stats=[("5", "Waiting"), ("12", "Done"), ("2", "Escalated")]),
    pinned=D1_QUEUE,
    sections=[
      ("done", "check-check", "Done today", "12 people · 41 vitals", "12", "ok", D1_DONE, None),
      ("standing", "repeat", "Standing orders", "Courses that run over several days", "3", None,
       dcard(drow("syringe", "Ceftriaxone course", value="3 people", sub="Days 2, 3 and 5", name="SO ceftriaxone", chevron=False)
             + drow("droplet", "Fasting glucose before clinic", value="2 people", name="SO glucose", chevron=False)
             + drow("bandage", "Daily dressing", value="1 person", name="SO dressing", chevron=False), p=14, gap=2), None),
    ],
    foot=dbtn("Get a doctor to look at someone", "Open escalate D4", "triangle-alert", "warn", full=True),
    tab_items=TAB_STAFF, tab=0)

# ---------------- D2 record vitals
D2_WHO = dcard(
    f'<Frame w="fill" flex="row" gap={{13}} items="center">'
    f'<Image image="assets/img/avatar-2.jpg" w={{48}} h={{48}} rounded={{15}} />'
    f'<Frame grow={{1}} flex="col" gap={{3}}>'
    f'<Frame flex="row" gap={{8}} items="center">{T(15,"semibold","var:text/strong","Amara Okeke")}'
    f'<Frame flex="row" px={{8}} py={{2}} rounded={{6}} bg="var:bg/muted">'
    f'{T(10,"semibold","var:text/accent","MDR-8842-19")}</Frame></Frame>'
    f'{T(11,"regular","var:text/muted","34 · before Dr. Okafor at 10:30 · hypertension",w="fill")}</Frame></Frame>'
    + alert_strip("triangle-alert", "Allergic to penicillin", "Rash and swelling · recorded June 2026", "err"))

D2_FORM = dcard(
    eyerow("Vitals")
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Systolic","activity","136",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Diastolic","activity","86",ph=False)}</Frame></Frame>'
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Pulse","heart-pulse","78",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Temperature °C","thermometer","36.8",ph=False)}</Frame></Frame>'
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Weight kg","weight","74",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("SpO₂ %","wind","98",ph=False)}</Frame></Frame>'
    + field("Anything you noticed (optional)", "message-square-text", "Says the headaches are worse in the afternoon."))

D2_RANGE = dgroup("Against her own history", [
    drow("activity", "Blood pressure", value="136/86", sub="Last visit 142/92 · improving", name="Rng bp", tone="ok", chevron=False),
    drow("weight", "Weight", value="74 kg", sub="Unchanged since March", name="Rng weight", chevron=False),
    drow("thermometer", "Temperature", value="36.8 °C", sub="Normal", name="Rng temp", tone="ok", chevron=False),
], footer="Anything outside the range you were given turns amber and offers to escalate. You never have to remember the numbers.")

D2_VERIFY = dgroup("What she told us herself", [
    unverified("Blood group", "O+", verified=False, name="Uv blood"),
    unverified("Genotype", "AA", verified=False, name="Uv geno"),
    unverified("Allergy", "Penicillin", verified=True, name="Uv allergy"),
], footer="Blood group and genotype came from her, not from a test. They stay marked until a laboratory result confirms them — and the mark travels with the value into every other hospital.")

addx("Chain", "D2-vitals",
    o_desk("Org · Nursing — D2 Record Vitals", ("Nursing", "Amara Okeke", "Vitals"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","My queue")}</Frame>'
        f'{D2_WHO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D2_FORM}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D2_RANGE}{D2_VERIFY}'
        f'{dcta("Save and hand to the doctor","Save vitals D2","check")}</Frame></Frame>',
        NAV["Departments"], dept="Nursing", who=NURSE, badges=BADGES),
    o_head("Vitals", "Amara Okeke · before 10:30", stats=[("136/86", "BP"), ("78", "Pulse"), ("74kg", "Weight")]),
    pinned=f'{D2_WHO}{D2_FORM}',
    sections=[
      ("history", "trending-up", "Against her own history", "BP improving since last visit", None, "ok", D2_RANGE, None),
      ("self", "circle-help", "What she told us herself", "Blood group and genotype are unverified", "3", "warn", D2_VERIFY, None),
    ],
    foot=dcta("Save and hand to the doctor", "Save vitals D2", "check"),
    tab_items=TAB_STAFF, tab=0)

# ---------------- D3 administer
D3_ORDER = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","ORDERED BY DR. OKAFOR · 09:12")}{status_pill("pending","Day 2 of 5")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(20,"bold","var:text/strong","Ceftriaxone 1 g")}'
    + T(13, "regular", "var:text/muted", "Intramuscular · once daily · five days · right or left gluteal, alternate", w="fill") + '</Frame>'
    + alert_strip("triangle-alert", "Allergic to penicillin",
                  "Ceftriaxone is a cephalosporin. Dr. Okafor recorded the allergy and prescribed it anyway with a written reason — read it before you give this.",
                  "err", dbtn("Read", "Read reason D3", None, "ghost", grow=False, size="sm")))

D3_CHECK = dgroup("Before you give it", [
    checklist_row(True, "Right member", "Amara Okeke · MDR-8842-19 · confirmed at the chair", "Chk member"),
    checklist_row(True, "Right drug and dose", "Ceftriaxone 1 g · matches the order", "Chk drug"),
    checklist_row(False, "Right site", "Day 1 was left gluteal — today is right", "Chk site"),
    checklist_row(False, "Allergy reviewed", "Penicillin allergy · prescriber's reason read", "Chk allergy"),
], footer="Five rights, shortened to the four that a queue actually gets wrong. Each one is signed by you, with the time.")

D3_AFTER = dcard(
    eyerow("After you give it")
    + field("Site used", "map-pin", "Right gluteal", ph=False, trailing=("chevron-down", "Site pick"))
    + field("Batch number", "package", "CFX-2026-0841", ph=False)
    + dtoggle("clock", "Observe for 15 minutes", sub="Standard after a first or second dose", on=True, name="Observe on")
    + field("Anything to note (optional)", "message-square-text", "Tolerated well, no reaction at 15 minutes."))

addx("Chain", "D3-administer",
    o_desk("Org · Nursing — D3 Administer &amp; Record", ("Nursing", "Musa Ibrahim", "Injection"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","My queue")}</Frame>'
        f'{D3_ORDER}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D3_CHECK}{D3_AFTER}</Frame>'
        f'<Frame w={{330}} flex="col" gap={{14}}>'
        f'{dgroup("The course", [drow("check-check","Day 1","","Given 13 Aug 09:40 · left gluteal","Course 1",tone="ok",chevron=False),drow("circle-dot","Day 2","Today","Now","Course 2",chevron=False),drow("circle","Day 3","15 Aug","Not yet due","Course 3",chevron=False),drow("circle","Day 5","17 Aug","Last dose","Course 5",chevron=False)])}'
        f'{dcta("Record as given","Save administer D3","check")}'
        f'{dbtn("Could not give it","Not given D3","x","danger",full=True)}</Frame></Frame>',
        NAV["Departments"], dept="Nursing", who=NURSE, badges=BADGES),
    o_head("Give an injection", "Musa Ibrahim · day 2 of 5", stats=[("1 g", "Dose"), ("IM", "Route"), ("2/5", "Day")]),
    pinned=D3_ORDER,
    sections=[
      ("checks", "list-checks", "Before you give it", "Four checks, each signed by you", "4", "warn", D3_CHECK, None),
      ("after", "clipboard-check", "After you give it", "Site, batch, observation", None, None, D3_AFTER, None),
      ("course", "repeat", "The course", "Day 2 of 5", "5", None,
       dgroup("The course", [drow("check-check","Day 1","","Given 13 Aug 09:40 · left gluteal","Course 1",tone="ok",chevron=False),drow("circle-dot","Day 2","Today","Now","Course 2",chevron=False),drow("circle","Day 3","15 Aug","Not yet due","Course 3",chevron=False),drow("circle","Day 5","17 Aug","Last dose","Course 5",chevron=False)]), None),
    ],
    foot=f'{dcta("Record as given","Save administer D3","check")}'
         f'{dbtn("Could not give it","Not given D3","x","danger",full=True)}',
    tab_items=TAB_STAFF, tab=0)

# ---------------- D4 escalate
D4_PICK = dgroup("What did you find?", [
    outcome_choice("activity", "A reading outside the range", "Blood pressure, sugar, temperature, oxygen — anything the doctor set a limit on.", "Esc reading", sel=True, tone="warn"),
    outcome_choice("heart-pulse", "The member looks unwell", "Your judgement counts even when the numbers do not.", "Esc looks", tone="err"),
    outcome_choice("syringe", "A reaction after something I gave", "Rash, swelling, breathlessness, faintness.", "Esc reaction", tone="err"),
    outcome_choice("circle-help", "Something I need a decision on", "A dose that does not look right, a member refusing, a missing order.", "Esc decision", tone="info"),
])

D4_FORM = dcard(
    field("What you found", "message-square-text", "BP 178/104 seated, repeated after 5 minutes at 174/100. She has a headache and says her vision is blurry.", ph=False)
    + field_chips("How urgent?", ["Now", "Within 15 minutes", "Before they leave"], 0, "Esc urgency")
    + dtoggle("phone-call", "Also ring the doctor on duty", sub="Do not rely on a screen for something happening now", on=True, name="Esc ring"))

D4_WHO = dgroup("Who this goes to", [
    patient_row("avatar-4.jpg", "Dr. Ngozi Okafor", "Cardiology", "Her doctor today · in room 3 · with a member", "Send", "Esc okafor", tag="confirmed"),
    patient_row("avatar-1.jpg", "Dr. Chuka Eze", "General practice", "On duty · free now", "Send", "Esc eze", tag="new"),
], footer="If the first doctor does not answer within two minutes it goes to the duty doctor automatically. An escalation is never left sitting in one person's queue.")

addx("Chain", "D4-escalate",
    o_desk("Org · Nursing — D4 Escalate", ("Nursing", "Grace Okeke", "Escalate"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","My queue")}</Frame>'
        f'{dhead([("Get a doctor",False),("to look",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D4_PICK}{D4_FORM}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D4_WHO}'
        f'{dcta("Escalate now","Send escalate D4","triangle-alert")}</Frame></Frame>',
        NAV["Departments"], dept="Nursing", urgent=1, who=NURSE, badges=BADGES),
    o_head("Escalate", "Grace Okeke · BP 178/104", stats=[("Now", "Urgency"), ("2 min", "Fallback"), ("2", "Doctors")]),
    pinned=D4_PICK,
    sections=[
      ("detail", "message-square-text", "What you found", "And how urgent it is", None, None, D4_FORM, None),
      ("who", "stethoscope", "Who this goes to", "Her doctor, then the duty doctor", "2", None, D4_WHO, None),
    ],
    foot=dcta("Escalate now", "Send escalate D4", "triangle-alert"),
    tab_items=TAB_STAFF, tab=0)

# ---------------- D5–D8 LABORATORY
D5_QUEUE = dgroup("Orders waiting · 4", [
    task_row_big("09:12", "Amara Okeke · MDR-8842-19", "Ordered by Dr. Okafor · Garki",
                 "Fasting blood sugar · HbA1c — fasting sample please", "Order amara", action="Accept",
                 flags=[("clock", "41 min waiting")], tone="warn"),
    task_row_big("09:31", "Grace Okeke · MDR-8842-21", "Ordered by Dr. Okafor · diabetic",
                 "HbA1c — repeat, previous was 8.4%", "Order grace", action="Accept", avatar="avatar-3.jpg"),
    task_row_big("09:48", "Musa Ibrahim · MDR-7714-02", "Ordered by Dr. Eze · urgent",
                 "Full blood count · troponin", "Order musa", action="Accept", avatar="avatar-1.jpg",
                 flags=[("zap", "Urgent · same day")], tone="err"),
    task_row_big("10:02", "Halima Sani · MDR-9012-44", "Referred in from Wuse Clinic",
                 "Urea, creatinine and electrolytes", "Order halima", action="Accept", avatar="avatar-5.jpg",
                 flags=[("share-2", "From a referral")]),
], footer="You see the order and the clinical detail attached to it. Nothing else from the member's record opens here — a test is run the same way whatever the diagnosis is.")

D5_PROGRESS = dgroup("In progress · 3", [
    drow("beaker", "Fatima Bello · FBC", value="Running", sub="Accepted 09:20 · analyser 2", name="Prog fatima"),
    drow("beaker", "Emeka Nwosu · Lipid profile", value="Running", sub="Accepted 09:26", name="Prog emeka"),
    drow("triangle-alert", "Blessing Ade · FBC", value="Sample problem", sub="Haemolysed — she has been asked to return", name="Open lab D8", tone="err"),
])

D5_ASIDE = (rail_section("Today",
    dcard(kpi_line("Accepted", "14") + kpi_line("Results entered", "11")
          + kpi_line("Median turnaround", "2h 40m") + kpi_line("Samples rejected", "1", "warn"), p=14, gap=3), None)
    + alert_strip("clock", "Urgent means same day",
        "Dr. Eze marked one order urgent. Members are told a same-day result means before 17:00.", "warn"))

addx("Chain", "D5-lab-queue",
    o_desk("Org · Laboratory — D5 Order Queue", ("Laboratory", "Thursday 14 August"),
        f'{dhead([("Four orders",False),("waiting",True)],26)}'
        f'{rows_of([stat_tile("inbox","4","Waiting","Oldest 41 minutes","warn","Stat lwaiting"),stat_tile("beaker","3","In progress","Two analysers","info","Stat lprog"),stat_tile("send","11","Entered today","All released by a doctor","ok","Stat ldone"),stat_tile("timer","2h 40m","Median turnaround","Target is 4 hours","teal","Stat lturn")],4,14)}'
        f'{D5_QUEUE}{D5_PROGRESS}',
        NAV["Departments"], dept="Laboratory", urgent=1, aside=D5_ASIDE, who=LAB, badges=BADGES),
    o_head("Order queue", "4 waiting · 1 urgent", back=False, ctx="Laboratory · Garki",
           stats=[("4", "Waiting"), ("3", "Running"), ("11", "Done")]),
    pinned=D5_QUEUE,
    sections=[
      ("progress", "beaker", "In progress", "Three samples running", "3", None, D5_PROGRESS, None),
      ("today", "chart-column", "Today", "14 accepted · 2h 40m median", None, None,
       dcard(kpi_line("Accepted", "14") + kpi_line("Results entered", "11")
             + kpi_line("Median turnaround", "2h 40m") + kpi_line("Samples rejected", "1", "warn"), p=14, gap=3), None),
    ],
    tab_items=TAB_STAFF, tab=0)

# ---------------- D6 order detail
D6_ORDER = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","ORDERED BY DR. NGOZI OKAFOR · 09:12")}{status_pill("pending","Waiting 41 min")}</Frame>'
    + f'<Frame w="fill" flex="row" gap={{13}} items="center">'
    + f'<Image image="assets/img/avatar-2.jpg" w={{48}} h={{48}} rounded={{15}} />'
    + f'<Frame grow={{1}} flex="col" gap={{3}}>{T(16,"semibold","var:text/strong","Amara Okeke")}'
    + T(11, "regular", "var:text/muted", "34 · MDR-8842-19 · Garki · fasting since 22:00", w="fill") + '</Frame></Frame>'
    + hr()
    + drow("flask-conical", "Fasting blood sugar", value="₦3,500", name="Ord fbs", chevron=False)
    + drow("flask-conical", "HbA1c", value="₦5,000", name="Ord hba1c", chevron=False)
    + note_section("Clinical details from the doctor",
                   "Hypertension on amlodipine. Screening for diabetes. Fasting sample please — she was told to fast from 22:00.",
                   "file-text"))

D6_WHAT = dgroup("What you can and cannot see", [
    perm_row("This order and its clinical details", True),
    perm_row("Her previous results for the same tests", True, "So you can spot a sample that does not fit"),
    perm_row("Her consultation notes and diagnosis", False, "Nothing in a note changes how a test is run"),
    perm_row("Release the result to her", False, "You enter it; Dr. Okafor releases it"),
])

D6_PREV = dgroup("Her previous results", [
    lab_line("Fasting blood sugar", "5.8 mmol/L", "3.9 – 5.5", "High"),
    lab_line("HbA1c", "6.1 %", "< 5.7", "High"),
], footer="From 12 March, at this laboratory. Shown so an implausible reading gets a second look before it leaves the bench.")

addx("Chain", "D6-lab-order",
    o_desk("Org · Laboratory — D6 Order", ("Laboratory", "Amara Okeke"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Order queue")}</Frame>'
        f'<Frame flex="row" gap={{9}} items="center">'
        f'{dbtn("Sample problem","Open lab D8","triangle-alert","danger",grow=False,size="sm")}'
        f'{dbtn("Accept and start","Open result D7","arrow-right","navy",grow=False,size="sm")}</Frame></Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D6_ORDER}{D6_PREV}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D6_WHAT}'
        f'{dcta("Accept and start","Open result D7","arrow-right")}</Frame></Frame>',
        NAV["Departments"], dept="Laboratory", who=LAB, badges=BADGES),
    o_head("Order", "Amara Okeke · 2 tests", stats=[("2", "Tests"), ("41m", "Waiting"), ("₦8,500", "She pays")]),
    pinned=D6_ORDER,
    sections=[
      ("prev", "history", "Her previous results", "From 12 March, at this laboratory", "2", None, D6_PREV, None),
      ("scope", "shield-check", "What you can and cannot see", "The order, not the record", "4", None, D6_WHAT, None),
    ],
    foot=f'{dcta("Accept and start","Open result D7","arrow-right")}'
         f'{dbtn("Sample problem","Open lab D8","triangle-alert","danger",full=True)}',
    tab_items=TAB_STAFF, tab=0)

# ---------------- D7 structured result entry
def result_line(analyte, unit, ref, value="", flag=None):
    tone = {"high": ("var:state/warning-bg", "var:state/warning", "High"),
            "low": ("var:state/warning-bg", "var:state/warning", "Low"),
            None: ("var:state/success-bg", "var:state/success", "Normal")}[flag]
    tag = (f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="{tone[0]}">'
           f'{T(10,"semibold",tone[1],tone[2])}</Frame>') if value else ''
    box = (f'<Frame w={{104}} flex="row" px={{12}} py={{9}} rounded={{10}} bg="var:bg/base" '
           f'stroke="{"var:border/accent" if value else "var:border/default"}" strokeWidth={{1}}>'
           f'{T(13,"semibold" if value else "regular","var:text/strong" if value else "var:text/faint",value or "—")}</Frame>')
    return (f'<Frame name="Btn Res {analyte}" w="fill" flex="row" gap={{12}} items="center" py={{10}}>'
            f'{T(13,"medium","var:text/strong",analyte,w=178)}{box}'
            f'{T(12,"regular","var:text/muted",unit,w=76)}'
            f'{T(11,"regular","var:text/faint",ref,w="fill")}{tag}</Frame>')

D7_TEMPLATE = dcard(
    eyerow("Fasting blood sugar", f'<Frame name="Btn Change template" flex="row">{T(11,"semibold","var:text/accent","Change template")}</Frame>')
    + result_line("Fasting plasma glucose", "mmol/L", "3.9 – 5.5", "6.4", "high")
    + hr() + eyerow("HbA1c")
    + result_line("HbA1c", "%", "< 5.7", "6.8", "high")
    + result_line("Estimated average glucose", "mmol/L", "—", "8.5")
    + hr()
    + field("Comment for the doctor (optional)", "message-square-text",
            "Sample taken fasting at 07:40. Slight lipaemia, does not affect these assays.")
    + upload("Attach report D7", label="Attach the analyser printout"))

D7_WHY = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("info",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Why a form and not a paragraph")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Typed prose cannot be trended, cannot be flagged against a range, and cannot be compared with a result from another laboratory. You fill numbers; Medra does the rest. The comment box is for anything a number cannot carry.", w="fill"),
    bg="var:state/info-bg", stroke=None)

D7_NEXT = dgroup("What happens when you finish", [
    prep_step(1, "The result goes to Dr. Okafor", "Not to the member — a doctor releases it"),
    prep_step(2, "Out-of-range values are flagged", "Both of these are above range and will be marked for her"),
    prep_step(3, "Her record is updated", "And her HbA1c trend gains a point"),
], footer="If nobody releases it within 24 hours, the doctor is reminded and the organisation admin sees it on Today.")

addx("Chain", "D7-lab-result",
    o_desk("Org · Laboratory — D7 Enter Result", ("Laboratory", "Amara Okeke", "Result"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Order")}</Frame>'
        f'{dhead([("Enter the",False),("result",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D7_TEMPLATE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D7_WHY}{D7_NEXT}'
        f'{dcta("Send to the doctor","Save result D7","send")}</Frame></Frame>',
        NAV["Departments"], dept="Laboratory", who=LAB, badges=BADGES),
    o_head("Enter result", "Amara Okeke · 2 tests", stats=[("2", "Tests"), ("2", "Out of range"), ("Dr. Okafor", "Goes to")]),
    pinned=D7_TEMPLATE,
    sections=[
      ("why", "info", "Why a form and not a paragraph", "So it can be trended and compared", None, None, D7_WHY, None),
      ("next", "list-checks", "What happens when you finish", "It goes to the doctor, not the member", "3", None, D7_NEXT, None),
    ],
    foot=dcta("Send to the doctor", "Save result D7", "send"),
    tab_items=TAB_STAFF, tab=0)

# ---------------- D8 sample problem
D8_PICK = dgroup("What is wrong with it?", [
    outcome_choice("droplet", "Haemolysed", "Broken red cells make several assays unusable.", "Prob haemolysed", sel=True, tone="warn"),
    outcome_choice("package-x", "Not enough sample", "Under the minimum volume for the tests ordered.", "Prob volume", tone="warn"),
    outcome_choice("tag", "Labelling does not match", "The tube and the request name different people.", "Prob label", tone="err"),
    outcome_choice("clock", "Too old by the time it reached us", "Outside the stability window for this assay.", "Prob old", tone="warn"),
    outcome_choice("circle-help", "Wrong tube or preservative", "Right sample, wrong container.", "Prob tube", tone="info"),
])

D8_WHAT = dcard(
    field("What should happen now?", "message-square-text",
          "A fresh sample is needed. She fasted this morning, so the repeat should be tomorrow morning rather than today.", ph=False)
    + dtoggle("message-circle", "Tell the member", sub="With what to do and when to come back", on=True, name="Prob tell member")
    + dtoggle("stethoscope", "Tell the doctor who ordered it", sub="Dr. Okafor is expecting this before her 14:00 clinic", on=True, name="Prob tell doctor")
    + dtoggle("banknote", "Do not charge her again", sub="The repeat is at our cost — the sample failed here", on=True, name="Prob no charge"))

D8_RULE = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",16,OK_IC)}'
    f'{T(14,"semibold","var:text/strong","A rejected sample is never a silent one")}</Frame>'
    + T(12, "regular", "var:text/default",
        "The commonest failure in a paper laboratory is a sample quietly discarded, with the member turning up a week later to be told nothing was ever run. Rejecting here always tells someone.", w="fill"),
    bg="var:state/success-bg", stroke=None)

addx("Chain", "D8-lab-problem",
    o_desk("Org · Laboratory — D8 Sample Problem", ("Laboratory", "Blessing Ade", "Sample"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Order queue")}</Frame>'
        f'{dhead([("This sample",False),("cannot be run",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D8_PICK}{D8_WHAT}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D8_RULE}'
        f'{dcta("Reject and tell them","Save problem D8","send")}'
        f'{dbtn("Never mind","Open lab D5","x","ghost",full=True)}</Frame></Frame>',
        NAV["Departments"], dept="Laboratory", who=LAB, badges=BADGES),
    o_head("Sample problem", "Blessing Ade · FBC", stats=[("Haemolysed", "Reason"), ("2", "To tell"), ("Free", "Repeat")]),
    pinned=D8_PICK,
    sections=[
      ("what", "message-square-text", "What should happen now", "Who is told, and who pays", None, None, D8_WHAT, None),
      ("rule", "shield-check", "Why this screen exists", "A rejected sample is never silent", None, "ok", D8_RULE, None),
    ],
    foot=f'{dcta("Reject and tell them","Save problem D8","send")}'
         f'{dbtn("Never mind","Open lab D5","x","ghost",full=True)}',
    tab_items=TAB_STAFF, tab=0)

# ---------------- D9–D11 PHARMACY
D9_QUEUE = dgroup("Prescriptions waiting · 4", [
    task_row_big("09:28", "Fatima Bello · MDR-2201-13", "Dr. Okafor · signed 09:28 · she is at the counter",
                 "Salbutamol inhaler 100 mcg · 1 unit", "Rx fatima", action="Dispense", avatar="avatar-4.jpg",
                 flags=[("user-check", "Waiting here")], tone="ok"),
    task_row_big("09:31", "Amara Okeke · MDR-8842-19", "Dr. Okafor · 30 days",
                 "Amlodipine 5 mg · 30 tablets", "Rx amara", action="Dispense",
                 flags=[("triangle-alert", "Penicillin allergy")], tone="err"),
    task_row_big("09:44", "Grace Okeke · MDR-8842-21", "Dr. Okafor · repeat approved",
                 "Metformin 500 mg · 60 tablets", "Rx grace", action="Dispense", avatar="avatar-3.jpg",
                 flags=[("package", "Low stock")], tone="warn"),
    task_row_big("10:02", "Musa Ibrahim · MDR-7714-02", "Dr. Eze · collect for a relative",
                 "Ceftriaxone 1 g · 5 vials", "Rx musa", action="Dispense", avatar="avatar-1.jpg",
                 flags=[("users", "Collected by someone else")]),
], footer="Someone standing at the counter comes first, whatever the order they arrived in. The queue is sorted by who is waiting, not by when it was signed.")

D9_STOCK = dgroup("Watch the shelf", [
    drow("package", "Metformin 500 mg", value="18 left", sub="Three prescriptions today need 60", name="Stock metformin", tone="warn"),
    drow("package", "Amlodipine 5 mg", value="240 left", sub="Comfortable", name="Stock amlodipine", tone="ok"),
    drow("package-x", "Salbutamol inhaler", value="Out", sub="Two waiting — substitution needed", name="Open sub D11", tone="err"),
], footer="Stock is a count you keep here, not a warehouse system. It exists so you can tell a member before they queue, not to run the pharmacy.")

addx("Chain", "D9-pharmacy",
    o_desk("Org · Pharmacy — D9 Prescription Queue", ("Pharmacy", "Thursday 14 August"),
        f'{dhead([("Four prescriptions",False),("waiting",True)],26)}'
        f'{rows_of([stat_tile("inbox","4","Waiting","1 at the counter","teal","Stat pwaiting"),stat_tile("check-check","23","Dispensed today","All recorded","ok","Stat pdone"),stat_tile("package-x","1","Out of stock","Salbutamol inhaler","err","Stat pstock"),stat_tile("repeat","3","Substitutions","This week","warn","Stat psub")],4,14)}'
        f'{D9_QUEUE}',
        NAV["Departments"], dept="Pharmacy", urgent=1,
        aside=rail_section("Watch the shelf", D9_STOCK, None), who=PHARM, badges=BADGES),
    o_head("Prescriptions", "4 waiting · 1 at the counter", back=False, ctx="Pharmacy · Garki",
           stats=[("4", "Waiting"), ("23", "Done"), ("1", "Out of stock")]),
    pinned=D9_QUEUE,
    sections=[("stock", "package", "Watch the shelf", "One out of stock, one low", "3", "warn", D9_STOCK, None)],
    tab_items=TAB_STAFF, tab=0)

# ---------------- D10 dispense
D10_RX = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","PRESCRIBED BY DR. NGOZI OKAFOR · MDCN 71482")}{status_pill("confirmed","Signed 09:31")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(20,"bold","var:text/strong","Amlodipine 5 mg")}'
    + T(13, "regular", "var:text/muted", "One tablet every morning · 30 days · one repeat authorised", w="fill") + '</Frame>'
    + hr()
    + note_section("Instructions for the member",
                   "Take one tablet each morning, with or without food. It works best at a steady level, so take it at about the same time each day.",
                   "message-circle")
    + alert_strip("triangle-alert", "Allergic to penicillin",
                  "Not relevant to this medicine, but check anything you add or substitute against it.", "err"))

D10_FORM = dcard(
    eyerow("What you are handing over")
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Quantity","package","30",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Batch","hash","AML-2026-3391",ph=False)}</Frame></Frame>'
    + field("Expiry on the pack", "calendar-days", "March 2028", ph=False)
    + field_chips("Who is collecting?", ["The member", "A relative", "A courier"], 0, "Rx collector")
    + dtoggle("message-circle", "Send her the instructions again", sub="To her phone, in the words the doctor wrote", on=True, name="Rx send instr")
    + dtoggle("bell-ring", "Set her a reminder at 08:00", sub="She can turn it off from her own app", on=True, name="Rx remind"))

D10_COUNSEL = dgroup("Say this at the counter", [
    drow("sunrise", "Every morning, at about the same time", sub="A steady level is what makes it work", name="Cn time", chevron=False),
    drow("circle-alert", "Ankle swelling is the common side effect", sub="Tell her it is not dangerous but she should mention it", name="Cn side", chevron=False),
    drow("calendar-check", "Come back in 30 days", sub="One repeat is already authorised, so she does not need a new appointment", name="Cn repeat", chevron=False),
], footer="Written by the prescriber, not by the pharmacy. If you disagree with any of it, flag it back rather than change it at the counter.")

addx("Chain", "D10-dispense",
    o_desk("Org · Pharmacy — D10 Dispense", ("Pharmacy", "Amara Okeke"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Prescription queue")}</Frame>'
        f'{D10_RX}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D10_FORM}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D10_COUNSEL}'
        f'{dcta("Record as dispensed","Save dispense D10","check")}'
        f'{dbtn("Cannot dispense this","Open sub D11","triangle-alert","warn",full=True)}</Frame></Frame>',
        NAV["Departments"], dept="Pharmacy", who=PHARM, badges=BADGES),
    o_head("Dispense", "Amara Okeke · amlodipine", stats=[("30", "Tablets"), ("30d", "Supply"), ("1", "Repeat")]),
    pinned=f'{D10_RX}{D10_FORM}',
    sections=[("counsel", "message-circle", "Say this at the counter", "Written by the prescriber", "3", None, D10_COUNSEL, None)],
    foot=f'{dcta("Record as dispensed","Save dispense D10","check")}'
         f'{dbtn("Cannot dispense this","Open sub D11","triangle-alert","warn",full=True)}',
    tab_items=TAB_STAFF, tab=0)

# ---------------- D11 substitution / stock-out
D11_PICK = dgroup("Why can you not dispense it?", [
    outcome_choice("package-x", "Out of stock", "We do not have it and cannot get it today.", "Sub stock", sel=True, tone="err"),
    outcome_choice("repeat", "Only a different brand or strength is available", "Same molecule, different pack.", "Sub brand", tone="warn"),
    outcome_choice("banknote", "The member cannot pay for it", "There may be a cheaper equivalent worth asking about.", "Sub cost", tone="warn"),
    outcome_choice("triangle-alert", "I think this prescription is wrong", "Dose, interaction, or something the record shows.", "Sub clinical", tone="err"),
])

D11_OPTIONS = dgroup("What we could give instead", [
    patient_row("avatar-6.jpg", "Salbutamol 100 mcg — Ventolin", "Same molecule", "In stock · 12 units · ₦4,200", "Propose", "Alt ventolin", tag="confirmed"),
    patient_row("avatar-6.jpg", "Salbutamol 100 mcg — generic", "Same molecule", "In stock · 40 units · ₦1,900", "Propose", "Alt generic", tag="new"),
    drow("x", "Nothing suitable — send her elsewhere", sub="We print the prescription and tell her which pharmacy has it", name="Alt none"),
], footer="A substitution is a proposal, never a decision. It goes to the prescriber and the member sees it only once the doctor has agreed.")

D11_MSG = dcard(
    eyerow("What the doctor will see")
    + f'<Frame w="fill" flex="col" gap={{9}} p={{15}} rounded={{13}} bg="var:state/warning-bg">'
    + T(13, "regular", "var:text/default",
        "“Salbutamol inhaler is out of stock at Garki. We have the generic at ₦1,900 or Ventolin at ₦4,200, both 100 mcg. Fatima is at the counter now. Which would you like?”", w="fill")
    + '</Frame>'
    + field("Add anything (optional)", "message-square-text", "She has used the generic before without trouble."))

addx("Chain", "D11-substitute",
    o_desk("Org · Pharmacy — D11 Cannot Dispense", ("Pharmacy", "Fatima Bello", "Substitution"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Prescription queue")}</Frame>'
        f'{dhead([("Ask the doctor,",False),("do not swap it",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D11_PICK}{D11_OPTIONS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D11_MSG}'
        f'{dcta("Send to the prescriber","Send sub D11","send")}</Frame></Frame>',
        NAV["Departments"], dept="Pharmacy", urgent=1, who=PHARM, badges=BADGES),
    o_head("Cannot dispense", "Fatima Bello · out of stock", stats=[("2", "Alternatives"), ("Here", "She is"), ("Dr. Okafor", "Goes to")]),
    pinned=D11_PICK,
    sections=[
      ("options", "repeat", "What we could give instead", "Two alternatives in stock", "2", None, D11_OPTIONS, None),
      ("msg", "message-circle", "What the doctor will see", "And anything you add", None, None, D11_MSG, None),
    ],
    foot=dcta("Send to the prescriber", "Send sub D11", "send"),
    tab_items=TAB_STAFF, tab=0)

# ---------------- D12–D14 FRONT DESK
D12_BOARD = (f'<Frame w="fill" flex="row" gap={{12}} items="start">'
             + board_col("Expected", 8, board_card("Amara Okeke", "10:30 · Dr. Okafor", "Bd amara")
                         + board_card("Musa Ibrahim", "11:00 · Dr. Eze · virtual", "Bd musa", avatar="avatar-1.jpg")
                         + board_card("Halima Sani", "11:30 · unassigned", "Bd halima", tag="pending", avatar="avatar-5.jpg"), "See expected")
             + board_col("In the waiting room", 12, board_card("Grace Okeke", "Arrived 09:47 · waiting 26 min", "Bd grace", tag="soon", avatar="avatar-3.jpg")
                         + board_card("Chidi Okeke", "Arrived 09:52 · with his mother", "Bd chidi", avatar="avatar-6.jpg")
                         + board_card("Blessing Ade", "Arrived 10:02 · unpaid", "Bd blessing", tag="pending", avatar="avatar-2.jpg"), "See waiting", tone="warn")
             + board_col("With a clinician", 9, board_card("Fatima Bello", "Room 3 · Dr. Okafor", "Bd fatima", avatar="avatar-4.jpg")
                         + board_card("Emeka Nwosu", "Nursing · vitals", "Bd emeka", avatar="avatar-1.jpg"), "See withdoc")
             + board_col("Done", 23, board_card("Ngozi Bala", "Left 09:40 · paid", "Bd ngozi", tag="completed", avatar="avatar-5.jpg")
                         + board_card("Sola Ade", "Left 09:55 · pharmacy", "Bd sola", tag="completed", avatar="avatar-6.jpg"), "See done", tone="ok")
             + '</Frame>')

D12_NEEDS = dgroup("Needs you at the desk", [
    drow("banknote", "1 person here has not paid", sub="Blessing Ade · arrived 10:02 · ₦15,000", name="Open checkin D14", tone="err"),
    drow("user-x", "1 booking has nobody assigned", sub="Halima Sani at 11:30 — tell the admin or assign", name="Open alloc B2", tone="warn"),
    drow("clock", "Longest wait is 26 minutes", sub="Grace Okeke · she is 68 and travelled from Kubwa", name="Bd grace", tone="warn"),
])

addx("Chain", "D12-desk",
    o_desk("Org · Front Desk — D12 The Day", ("Front desk", "Thursday 14 August"),
        f'{dhead([("Twelve people",False),("in the waiting room",True)],26)}'
        f'{D12_NEEDS}{D12_BOARD}',
        NAV["Today"], dept="Front desk", urgent=2, who=DESK, badges=BADGES),
    o_head("Front desk", "12 waiting · longest 26 min", back=False, ctx="Garki Medical Centre",
           stats=[("12", "Waiting"), ("9", "With a clinician"), ("23", "Done")],
           chips=[("Waiting", "Filter waiting", True), ("Expected", "Filter expected", False), ("Done", "Filter done", False)]),
    pinned=D12_NEEDS,
    sections=[
      ("board", "columns-3", "The whole board", "Expected, waiting, with a clinician, done", "52", None,
       board_stack("In the waiting room", 12, board_card("Grace Okeke", "Arrived 09:47 · waiting 26 min", "Bd grace", tag="soon", avatar="avatar-3.jpg")
                   + board_card("Chidi Okeke", "Arrived 09:52 · with his mother", "Bd chidi", avatar="avatar-6.jpg")
                   + board_card("Blessing Ade", "Arrived 10:02 · unpaid", "Bd blessing", tag="pending", avatar="avatar-2.jpg"), "See waiting", tone="warn")
       + board_stack("Expected", 8, board_card("Amara Okeke", "10:30 · Dr. Okafor", "Bd amara")
                     + board_card("Musa Ibrahim", "11:00 · Dr. Eze · virtual", "Bd musa", avatar="avatar-1.jpg"), "See expected")
       + board_stack("With a clinician", 9, board_card("Fatima Bello", "Room 3 · Dr. Okafor", "Bd fatima", avatar="avatar-4.jpg")
                     + board_card("Emeka Nwosu", "Nursing · vitals", "Bd emeka", avatar="avatar-1.jpg"), "See withdoc")
       + board_stack("Done", 23, board_card("Ngozi Bala", "Left 09:40 · paid", "Bd ngozi", tag="completed", avatar="avatar-5.jpg"), "See done", tone="ok"), None),
    ],
    sheets=[("desk", "zap", "Desk actions", "Register, check in, take payment", None, "At the desk", "Garki · 10:14",
             f'{sheet_pick("user-plus","Register a walk-in","Someone with no booking","Open walkin D13")}'
             f'{sheet_pick("user-check","Check someone in","They have a booking","Open checkin D14")}'
             f'{sheet_pick("search","Find a member","Name, phone or Medra ID","Nav Members")}'
             f'{sheet_pick("share-2","A referral arrived with them","From another organisation","Open inbound E4","info")}', None)],
    tab_items=TAB_DESK, tab=0)

# ---------------- D13 walk-in registration
D13_FIND = dcard(
    field("Do they already use Medra?", "search", "Name, phone or Medra ID", focus=True,
          helper="Always check first. A duplicate record is the one mistake that cannot be undone from the desk.")
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Scan their QR code", "Scan member B3", "qr-code", "ghost")
    + dbtn("They are new", "New member D13", "user-plus", "navy") + '</Frame>')

D13_FORM = dcard(
    eyerow("Register them")
    + field("Full name", "circle-user", "Ibrahim Danjuma", ph=False)
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Date of birth","calendar-days","14 / 03 / 1978",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Phone","phone","+234 806 555 0192",ph=False)}</Frame></Frame>'
    + field("NIN", "id-card", "Optional but strongly recommended", helper="Two people can share a name and a birthday. The NIN is what stops the wrong record being opened next year.")
    + field_chips("Why are they here?", ["New complaint", "Follow-up", "Test only", "Pharmacy only", "Emergency"], 0, "Walk reason")
    + dtoggle("smartphone", "Send them their Medra ID", sub="By SMS, so they can carry the record themselves from now on", on=True, name="Walk send id"))

D13_CONSENT = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","What they are agreeing to")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Read this aloud. They are agreeing that Garki Medical Centre may hold a record for them, and that they own it and can take it anywhere.", w="fill")
    + checkbox("They agreed, and I read it to them", "Walk consent")
    + T(11, "regular", "var:text/muted",
        "Recorded with your name and the time. It is the only thing that makes the record lawful.", w="fill"),
    bg="var:state/info-bg", stroke=None)

addx("Chain", "D13-walkin",
    o_desk("Org · Front Desk — D13 Register a Walk-in", ("Front desk", "Walk-in"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","The day")}</Frame>'
        f'{dhead([("Register",False),("a walk-in",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D13_FIND}{D13_FORM}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D13_CONSENT}'
        f'{dcta("Register and add to the queue","Save walkin D13","check")}</Frame></Frame>',
        NAV["Today"], dept="Front desk", who=DESK, badges=BADGES),
    o_head("Walk-in", "Register someone at the desk", stats=[("New", "Member"), ("1 min", "Takes"), ("SMS", "Their ID")]),
    pinned=f'{D13_FIND}{D13_FORM}',
    sections=[("consent", "shield-check", "What they are agreeing to", "Read it aloud, then tick", None, "info", D13_CONSENT, None)],
    foot=dcta("Register and add to the queue", "Save walkin D13", "check"),
    tab_items=TAB_DESK, tab=2)

# ---------------- D14 check-in & payment
D14_WHO = dcard(
    f'<Frame w="fill" flex="row" gap={{13}} items="center">'
    f'<Image image="assets/img/avatar-2.jpg" w={{48}} h={{48}} rounded={{15}} />'
    f'<Frame grow={{1}} flex="col" gap={{3}}>'
    f'<Frame flex="row" gap={{8}} items="center">{T(16,"semibold","var:text/strong","Blessing Ade")}'
    f'<Frame flex="row" px={{8}} py={{2}} rounded={{6}} bg="var:bg/muted">'
    f'{T(10,"semibold","var:text/accent","MDR-3311-90")}</Frame></Frame>'
    f'{T(11,"regular","var:text/muted","Arrived 10:02 · 10:30 with Dr. Eze · in person",w="fill")}</Frame>'
    f'{status_pill("pending","Not paid")}</Frame>')

D14_PAY = dcard(
    eyerow("Payment")
    + price_line("Follow-up consultation", "₦15,000")
    + price_line("Paid on Medra before arriving", "— ₦0", strong=False)
    + price_line("To collect now", "₦15,000", strong=True)
    + field_chips("How did they pay?", ["Transfer", "Card", "Cash", "Insurance", "Not yet"], 0, "Pay method")
    + field("Reference", "hash", "TRF-88421-C", ph=False, helper="Whatever your own till or bank gives you. Medra records it; it does not take the money.")
    + dtoggle("receipt", "Send a receipt to her phone", on=True, name="Pay receipt"))

D14_INS = dgroup("Insurance on her profile", [
    drow("shield-check", "NHIS", value="NHIS-4471-88", sub="Garki Medical Centre accepts NHIS", name="Ins nhis", tone="ok"),
    drow("credit-card", "Private insurance", value="None on file", sub="She can add one from her own app", name="Ins private", chevron=False),
], footer="Medra stores the number and tells you whether this branch accepts it. Claims still go through your usual process.")

D14_NEXT = dgroup("Then what?", [
    drow("users", "Send to the waiting room", sub="Dr. Eze is running about 12 minutes behind", name="Send waiting"),
    drow("syringe", "Send to nursing first", sub="Vitals before the consultation", name="Send nursing"),
    drow("flask-conical", "Send to the laboratory first", sub="If a test was ordered before the visit", name="Send lab"),
])

addx("Chain", "D14-checkin",
    o_desk("Org · Front Desk — D14 Check In", ("Front desk", "Blessing Ade"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","The day")}</Frame>'
        f'{D14_WHO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D14_PAY}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D14_INS}{D14_NEXT}'
        f'{dcta("Check in","Save checkin D14","check")}</Frame></Frame>',
        NAV["Today"], dept="Front desk", urgent=2, who=DESK, badges=BADGES),
    o_head("Check in", "Blessing Ade · not paid", stats=[("₦15,000", "To collect"), ("10:30", "Booked"), ("NHIS", "Insurance")]),
    pinned=f'{D14_WHO}{D14_PAY}',
    sections=[
      ("ins", "shield-check", "Insurance on her profile", "NHIS accepted here", "2", None, D14_INS, None),
      ("next", "arrow-right", "Then what?", "Waiting room, nursing or laboratory", "3", None, D14_NEXT, None),
    ],
    foot=dcta("Check in", "Save checkin D14", "check"),
    tab_items=TAB_DESK, tab=0)

# =====================================================================================
# 5. REFERRALS & EXTERNAL ACCESS  (Module 12)
# =====================================================================================
def ref_row(ic, who, what, when, nm, tone="info", actions=None, tag=None):
    bg = {"info": "var:state/info-bg", "warn": "var:state/warning-bg", "err": "var:state/error-bg",
          "ok": "var:state/success-bg"}[tone]
    c = {"info": A_IC, "warn": WARN_IC, "err": ERR_IC, "ok": OK_IC}[tone]
    acts = rows_of(actions, 2, 8) if actions else ''
    pill = status_pill(tag, size=10) if tag else ''
    return (f'<Frame name="Btn {nm}" w="fill" flex="col" gap={{10}} p={{14}} rounded={{14}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w="fill" flex="row" gap={{12}} items="start">'
            f'<Frame w={{36}} h={{36}} rounded={{12}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I(ic,17,c)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{8}} items="center">{T(14,"semibold","var:text/strong",who)}{pill}</Frame>'
            f'{T(11,"regular","var:text/muted",what,w="fill")}</Frame>'
            f'{T(11,"regular","var:text/faint",when)}</Frame>{acts}</Frame>')

# ---------------- E1 outbound
E1_LIST = dgroup("Referred out · 5", [
    ref_row("share-2", "Amara Okeke → Dr. Tunde Bello", "Neurology · Asokoro Specialist · routine · sent 12 Aug",
            "2 days", "Ref amara", tag="pending",
            actions=[dbtn("Chase", "Chase amara", "bell", "ghost", size="sm"),
                     dbtn("Withdraw", "Withdraw amara", "x", "danger", size="sm")]),
    ref_row("flask-conical", "Halima Sani → Lifebridge Diagnostics", "MRI lumbar spine · off Medra · single-use link opened 09:14",
            "Today", "Ref halima", tone="warn", tag="soon",
            actions=[dbtn("See the link", "Open links E6", "link", "ghost", size="sm"),
                     dbtn("Resend", "Resend halima", "send", "ghost", size="sm")]),
    ref_row("check-check", "Emeka Nwosu → Dr. Chuka Eze", "Orthopaedics · accepted, seen 11 Aug · reply received",
            "3 days", "Ref emeka", tone="ok", tag="completed",
            actions=[dbtn("Read the reply", "Read reply E1", "file-text", "navy", size="sm")]),
], footer="A referral that is never answered is the commonest way a patient falls through a gap. Anything unanswered after two days appears on Today.")

E1_STATS = rows_of([
    stat_tile("share-2", "5", "Sent this month", "3 answered", "teal", "Stat sent"),
    stat_tile("clock", "1.4 days", "Median reply", "Target is 2 days", "ok", "Stat reply"),
    stat_tile("link", "2", "Off-Medra links", "Both still open", "warn", "Stat links"),
    stat_tile("inbox", "3", "Referred to us", "Waiting on us", "info", "Stat inbound"),
], 4, 14)

addx("Referral", "E1-outbound",
    o_desk("Org · Referrals — E1 Referred Out", ("Referrals", "Sent"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Where we have",False),("sent people",True)],26)}'
        f'{dbtn("Refer someone","Open refer E2","share-2","navy",grow=False,size="sm")}</Frame>'
        f'{E1_STATS}{E1_LIST}',
        NAV["Referrals"], urgent=3,
        aside=rail_section("Waiting on us",
            dcard(drow("inbox", "3 referrals to answer", sub="Oldest 19 hours", name="Open inbound E4", tone="warn")
                  + drow("link", "2 single-use links open", sub="Both expire when the lab finishes", name="Open links E6")
                  + drow("bell", "1 chase due", sub="Dr. Bello has not answered in 2 days", name="Chase amara", tone="warn"), p=14, gap=2), None),
        badges=BADGES),
    o_head("Referrals", "5 sent · 3 waiting on us", back=False, ctx="Garki Medical Centre",
           stats=[("5", "Sent"), ("3", "Inbound"), ("1.4d", "Median")],
           chips=[("Sent", "Filter sent", True), ("Received", "Open inbound E4", False), ("Links", "Open links E6", False)]),
    pinned=E1_LIST,
    sections=[("stats", "chart-column", "How referrals are going", "1.4 days median reply", None, "ok", E1_STATS, None)],
    foot=dbtn("Refer someone", "Open refer E2", "share-2", "navy", full=True),
    tab_items=TAB_ADMIN, tab=3)

# ---------------- E2 create a referral
E2_WHO = dgroup("Who is it for?", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "34 · seen today by Dr. Okafor · hypertension", "Chosen", "Ref who amara", tag="confirmed"),
])

E2_DEST = dgroup("Where are they going?", [
    patient_row("avatar-5.jpg", "Dr. Tunde Bello", "MDCN 55208", "Neurology · Asokoro Specialist · on Medra · next slot Tue", "Choose", "Dest bello", tag="confirmed"),
    patient_row("avatar-1.jpg", "Wuse Diagnostics", "RC 2210934", "Laboratory and imaging · on Medra · 3.1 km", "Choose", "Dest wuse"),
    drow("link", "Somewhere not on Medra", sub="We generate a single-use link they open on any phone — no account, no app", name="Dest external", tone="warn"),
    drow("search", "Search Medra", sub="By name, specialty, organisation or MDCN number", name="Dest search"),
], footer="If they are on Medra the referral lands in their inbox. If they are not, the same information goes down a link that expires the moment they are finished with it.")

E2_WHAT = dgroup("What are you asking for?", [
    field_chips("Type", ["Consultation", "Test", "Imaging", "Procedure", "Admission"], 1, "Ref type"),
    field("What you want done", "clipboard-list", "MRI lumbar spine, without contrast", ph=False),
    field_chips("Urgency", ["Routine", "Soon — within a week", "Urgent — today"], 0, "Ref urgency"),
    note_section("Why you are referring",
                 "Six weeks of lower back pain with left leg radiation. No red flags. Conservative treatment has not helped. Please assess for disc herniation.",
                 "file-text"),
])

E2_SHARE = dgroup("What they will be able to see", [
    consent_row("file-text", "This referral letter", "Always included — it is the referral", "Sh letter"),
    consent_row("flask-conical", "The results that led to it", "Two lumbar X-rays from June", "Sh results"),
    consent_row("pill", "Current medicines", "So they do not prescribe something that clashes", "Sh meds"),
    consent_row("history", "Her full consultation history", "Not shared — they do not need it for this", "Sh history"),
], footer="The default is the minimum. Amara approves this list before anything leaves, and she can see afterwards exactly what was sent and to whom.")

addx("Referral", "E2-create",
    o_desk("Org · Referrals — E2 Refer Someone", ("Referrals", "New referral"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Referrals")}</Frame>'
        f'{dhead([("Refer",False),("someone out",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{E2_WHO}{E2_DEST}{E2_WHAT}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{E2_SHARE}'
        f'{dcta("Ask Amara to approve","Send refer E2","send")}'
        f'{dbtn("Save as a draft","Draft refer E2","file-text","ghost",full=True)}</Frame></Frame>',
        NAV["Referrals"], badges=BADGES),
    o_head("Refer someone", "Amara Okeke · imaging", stats=[("Routine", "Urgency"), ("3", "Items shared"), ("Her", "Approves")]),
    pinned=E2_DEST,
    sections=[
      ("who", "circle-user", "Who it is for", "Amara Okeke · seen today", None, None, E2_WHO, None),
      ("what", "clipboard-list", "What you are asking for", "MRI lumbar spine", None, None, E2_WHAT, None),
      ("share", "shield-check", "What they will see", "The minimum, and she approves it", "4", None, E2_SHARE, None),
    ],
    foot=f'{dcta("Ask Amara to approve","Send refer E2","send")}'
         f'{dbtn("Save as a draft","Draft refer E2","file-text","ghost",full=True)}',
    tab_items=TAB_ADMIN, tab=3)

# ---------------- E3 referral sent
E3_DONE = dcard(
    f'<Frame w="fill" flex="col" gap={{13}} items="center">'
    f'{big_icon("send","ok",84)}'
    f'{T(22,"bold","var:text/strong","Waiting on Amara")}'
    f'{T(14,"regular","var:text/muted","She has been asked to approve what gets shared. Nothing leaves Garki until she does — usually within a few minutes.",w="fill",align="center")}</Frame>')

E3_TRACK = dgroup("What happens next", [
    prep_step(1, "Amara approves what is shared", "On her phone · asked 10:22", done=True),
    prep_step(2, "Lifebridge Diagnostics opens the link", "No account needed — it opens on any phone"),
    prep_step(3, "They do the scan and upload the report", "Against the same template a Medra laboratory uses"),
    prep_step(4, "The link expires and the report lands here", "And in Amara's own record, which she keeps"),
], footer="You are told at every step. If nothing happens in 48 hours we chase them, and you see it on Today.")

E3_LINK = dcard(
    eyerow("The link they will get")
    + f'<Frame w="fill" flex="row" gap={{9}} items="center" px={{14}} py={{12}} rounded={{12}} bg="var:neutral/50">'
    + I("link", 15, M_IC) + T(13, "regular", "var:text/strong", "medra.ng/MDR-8842-19", w="fill")
    + f'<Frame name="Btn Copy link E3" flex="row">{I("copy",15,N_IC)}</Frame></Frame>'
    + T(11, "regular", "var:text/muted",
        "Short enough to read down a phone. It opens one job, expires when they finish it, and shows them a privacy notice before anything else.", w="fill")
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("Send on WhatsApp", "Send wa E3", "message-circle", "navy")
    + dbtn("Print the slip", "Print slip E3", "printer", "ghost") + '</Frame>')

addx("Referral", "E3-sent",
    o_desk("Org · Referrals — E3 Referral Sent", ("Referrals", "Sent"),
        f'<Frame w="fill" flex="row" gap={{16}} justify="center" items="start" pt={{8}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{E3_DONE}{E3_TRACK}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{E3_LINK}'
        f'{dbtn("Back to referrals","Nav Referrals","arrow-left","ghost",full=True)}</Frame></Frame>',
        NAV["Referrals"], badges=BADGES),
    o_head("Referral sent", "Waiting on Amara to approve", back=False,
           stats=[("1 of 4", "Steps"), ("48h", "We chase"), ("1", "Link")]),
    pinned=E3_DONE,
    sections=[
      ("track", "list-checks", "What happens next", "Four steps, you are told at each", "4", None, E3_TRACK, None),
      ("link", "link", "The link they will get", "medra.ng/MDR-8842-19", None, None, E3_LINK, None),
    ],
    tab_items=TAB_ADMIN, tab=3)

# ---------------- E4 inbound
E4_LIST = dgroup("Referred to us · 3", [
    ref_row("inbox", "Halima Sani · from Wuse Clinic", "Dr. Kemi Adeyemi · urea, creatinine and electrolytes · routine · 19 hours ago",
            "19 h", "In halima", tone="warn", tag="pending",
            actions=[dbtn("Accept", "Accept halima", "check", "navy", size="sm"),
                     dbtn("Offer a time", "Time halima", "calendar-clock", "ghost", size="sm"),
                     dbtn("Decline", "Decline halima", "x", "danger", size="sm")]),
    ref_row("inbox", "Ibrahim Danjuma · from Dr. Sani (independent)", "Cardiology opinion · chest pain on exertion · soon",
            "4 h", "In ibrahim", tone="err", tag="soon",
            actions=[dbtn("Accept", "Accept ibrahim", "check", "navy", size="sm"),
                     dbtn("Offer a time", "Time ibrahim", "calendar-clock", "ghost", size="sm"),
                     dbtn("Decline", "Decline ibrahim", "x", "danger", size="sm")]),
    ref_row("inbox", "Ngozi Bala · from Maitama Annex", "Physiotherapy after knee surgery · routine",
            "2 d", "In ngozi", tag="pending",
            actions=[dbtn("Accept", "Accept ngozi", "check", "navy", size="sm"),
                     dbtn("Decline", "Decline ngozi", "x", "danger", size="sm")]),
], footer="Accepting creates a booking and tells the member and the referring doctor. Declining also tells them, with your reason in your words — silence is the one option that is not available.")

E4_RULES = dgroup("Save yourself this screen", [
    dtoggle("zap", "Auto-accept from organisations we work with", sub="Wuse Clinic and Maitama Annex", on=False, name="Ref auto"),
    dtoggle("clock", "Answer within", sub="After 24 hours we chase you, and the referrer is told we have not answered", on=True, name="Ref sla"),
    drow("users", "Who sees inbound referrals", value="Admin + department leads", name="Ref who"),
])

addx("Referral", "E4-inbound",
    o_desk("Org · Referrals — E4 Referred To Us", ("Referrals", "Received"),
        f'{dhead([("Three people",False),("referred to us",True)],26)}'
        f'{T(14,"regular","var:text/muted","The oldest has waited 19 hours. Referring doctors are told we answer within a day.",w="fill")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{E4_LIST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{E4_RULES}</Frame></Frame>',
        NAV["Referrals"], urgent=3, badges=BADGES),
    o_head("Referred to us", "3 waiting · oldest 19 hours", back=False,
           stats=[("3", "Waiting"), ("19h", "Oldest"), ("24h", "Promised")]),
    pinned=E4_LIST,
    sections=[("rules", "zap", "Save yourself this screen", "Auto-accept and answer rules", "3", None, E4_RULES, None)],
    tab_items=TAB_ADMIN, tab=3)

# ---------------- E5 inbound detail
E5_HEAD = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","REFERRED BY DR. KEMI ADEYEMI · WUSE CLINIC · MDCN 44120")}'
    f'{status_pill("pending","19 hours ago")}</Frame>'
    + f'<Frame w="fill" flex="row" gap={{13}} items="center">'
    + f'<Image image="assets/img/avatar-5.jpg" w={{52}} h={{52}} rounded={{16}} />'
    + f'<Frame grow={{1}} flex="col" gap={{3}}>{T(17,"semibold","var:text/strong","Halima Sani")}'
    + T(11, "regular", "var:text/muted", "29 · MDR-9012-44 · Wuse · she has agreed to this referral", w="fill") + '</Frame></Frame>'
    + note_section("What they are asking for", "Urea, creatinine and electrolytes. Routine.", "clipboard-list")
    + note_section("Why", "Started lisinopril six weeks ago for hypertension. Baseline renal function before the next dose increase. No symptoms.", "file-text"))

E5_SHARED = dgroup("What Halima shared with us", [
    consent_row("file-text", "The referral letter", "Included", "Sh e5 letter"),
    consent_row("pill", "Current medicines", "Lisinopril 10 mg, started 3 July", "Sh e5 meds"),
    consent_row("activity", "Recent blood pressure readings", "Six clinic readings since June", "Sh e5 bp"),
    consent_row("history", "Her full consultation history", "Not shared", "Sh e5 hist"),
], footer="This is what she agreed to send, not everything we could ask for. If you need more, ask her — she can add to it from her own phone.")

E5_ACT = dgroup("Your answer", [
    outcome_choice("check-check", "Accept and book her in", "Creates a booking, tells her and Dr. Adeyemi.", "E5 accept", sel=True, tone="ok"),
    outcome_choice("calendar-clock", "Accept but offer times", "She picks from your open slots.", "E5 times", tone="info"),
    outcome_choice("share-2", "Pass it on", "Somewhere better suited, with the same information.", "E5 pass", tone="warn"),
    outcome_choice("x", "Decline", "With a reason in your words. She and Dr. Adeyemi both see it.", "E5 decline", tone="err"),
])

addx("Referral", "E5-inbound-detail",
    o_desk("Org · Referrals — E5 Referral Detail", ("Referrals", "Halima Sani"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Referred to us")}</Frame>'
        f'{E5_HEAD}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{E5_ACT}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{E5_SHARED}'
        f'{dcta("Accept and book her in","Accept E5","check")}</Frame></Frame>',
        NAV["Referrals"], urgent=3, badges=BADGES),
    o_head("Halima Sani", "From Wuse Clinic · 19 hours ago",
           stats=[("Routine", "Urgency"), ("3", "Items shared"), ("19h", "Waiting")]),
    pinned=E5_HEAD,
    sections=[
      ("answer", "reply", "Your answer", "Accept, offer times, pass on or decline", "4", None, E5_ACT, None),
      ("shared", "shield-check", "What Halima shared", "Only what she agreed to", "4", None, E5_SHARED, None),
    ],
    foot=dcta("Accept and book her in", "Accept E5", "check"),
    tab_items=TAB_ADMIN, tab=3)

# ---------------- E6 links issued
def link_row(who, what, state, when, nm):
    tone = {"open": ("warn", "Open"), "used": ("ok", "Used and expired"),
            "expired": ("muted", "Expired unused"), "revoked": ("err", "Revoked")}[state]
    bg = {"warn": "var:state/warning-bg", "ok": "var:state/success-bg",
          "muted": "var:bg/muted", "err": "var:state/error-bg"}[tone[0]]
    col = {"warn": "var:state/warning", "ok": "var:state/success",
           "muted": "var:text/muted", "err": "var:state/error"}[tone[0]]
    return (f'<Frame name="Btn {nm}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="{bg}" flex="col" justify="center" items="center">'
            f'{I("link",16,ERR_IC if tone[0]=="err" else A_IC)}</Frame>'
            f'{T(13,"semibold","var:text/strong",who,w=150)}'
            f'{T(12,"regular","var:text/muted",what,w="fill")}'
            f'{T(11,"regular","var:text/faint",when,w=88)}'
            f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="{bg}">'
            f'{T(10,"semibold",col,tone[1])}</Frame>{I("chevron-right",15,M_IC)}</Frame>')

E6_LIST = dgroup("Single-use links · 6", [
    link_row("Lifebridge Diagnostics", "Halima Sani · MRI lumbar spine", "open", "Opened 09:14", "Link lifebridge"),
    link_row("Ketu Medical Lab", "Amara Okeke · HbA1c", "open", "Not opened yet", "Link ketu"),
    link_row("Zenith Imaging", "Emeka Nwosu · knee X-ray", "used", "11 Aug", "Link zenith"),
    link_row("St. Mary's Clinic", "Ngozi Bala · discharge summary", "expired", "4 Aug", "Link stmarys"),
    link_row("Unknown recipient", "Blessing Ade · FBC", "revoked", "2 Aug", "Link revoked"),
], footer="A link is one job, for one recipient, and it dies when they finish. Anything still open after 48 hours is chased; anything you no longer want open can be revoked here in one tap.")

E6_HOW = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Why a link and not an account")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Most laboratories and clinics in Nigeria are not on Medra, and will not sign up to run one test. A member should not have to carry paper because of that. The link gives the other side exactly what they need, takes the result back in a structured form, and closes behind them.", w="fill")
    + T(11, "regular", "var:text/muted",
        "It is also how those organisations find us: a lab that keeps receiving these can onboard properly and stop using them.", w="fill"),
    bg="var:state/info-bg", stroke=None)

E6_RULES = dgroup("Rules that apply to every link", [
    drow("user-check", "The member consents before it exists", sub="No link is created without it", name="Lr consent", chevron=False, tone="ok"),
    drow("eye", "It carries the minimum", sub="Only what the creator ticked, never the whole record", name="Lr min", chevron=False),
    drow("timer", "One job, then it dies", sub="It expires the moment they mark it done, and after 7 days regardless", name="Lr expire", chevron=False),
    drow("file-text", "They accept a privacy undertaking first", sub="Recorded with the time — that is what makes it lawful", name="Lr privacy", chevron=False),
    drow("history", "Every link is in the member's own audit trail", sub="She sees who opened it and when", name="Open audit F2", chevron=False),
])

addx("Referral", "E6-links",
    o_desk("Org · Referrals — E6 Single-use Links", ("Referrals", "Links"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Links to people",False),("not on Medra",True)],26)}'
        f'{dbtn("Issue a link","Open refer E2","link","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{E6_LIST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{E6_HOW}{E6_RULES}</Frame></Frame>',
        NAV["Referrals"], badges=BADGES),
    o_head("Single-use links", "2 open · 6 this month", back=False,
           stats=[("2", "Open"), ("1", "Not opened"), ("1", "Revoked")]),
    pinned=dgroup("Single-use links · 6", [
        link_row_m("Lifebridge Diagnostics", "Halima Sani · MRI lumbar spine", "open", "Opened 09:14", "Link lifebridge"),
        link_row_m("Ketu Medical Lab", "Amara Okeke · HbA1c", "open", "Not opened yet", "Link ketu"),
        link_row_m("Zenith Imaging", "Emeka Nwosu · knee X-ray", "used", "11 Aug", "Link zenith"),
        link_row_m("St. Mary's Clinic", "Ngozi Bala · discharge summary", "expired", "4 Aug", "Link stmarys"),
        link_row_m("Unknown recipient", "Blessing Ade · FBC", "revoked", "2 Aug", "Link revoked"),
    ], footer="One job, one recipient. It dies when they finish."),
    sections=[
      ("how", "info", "Why a link and not an account", "Most labs will not sign up to run one test", None, None, E6_HOW, None),
      ("rules", "shield-check", "Rules that apply to every link", "Consent, minimum, one job, then it dies", "5", None, E6_RULES, None),
    ],
    tab_items=TAB_ADMIN, tab=3)

# =====================================================================================
# THE EXTERNAL PARTY'S OWN SCREENS
# Nobody here has an account, has been trained, or will ever come back. Four screens,
# no navigation, one job. The chrome is deliberately not the console — this is a page on
# a stranger's phone, not an app.
# =====================================================================================
def ext_desk(name, children):
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="col" items="center" '
            f'image="assets/img/canvas-org.jpg" overflow="hidden" px={{24}} py={{32}}>'
            f'<Frame w={{680}} flex="col" gap={{16}}>'
            f'<Frame w="fill" flex="row" gap={{11}} items="center" pb={{4}}>'
            f'<Image image="assets/logo/appicon.png" w={{34}} h={{34}} rounded={{11}} />'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(15,"bold","var:text/strong","Medra")}'
            f'{T(11,"regular","var:text/muted","medra.ng/MDR-9012-44")}</Frame>'
            f'<Frame name="Btn Open help" flex="row" gap={{7}} items="center" px={{11}} py={{7}} '
            f'rounded={{10}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{I("circle-help",14,N_IC)}{T(12,"medium","var:text/default","Help")}</Frame></Frame>'
            f'{children}</Frame></Frame>')

def ext_mob(name, children):
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" '
            f'image="assets/img/canvas-org-m.jpg" overflow="hidden">{statusbar()}'
            f'<Frame w="fill" flex="row" gap={{10}} items="center" px={{18}} pt={{10}} pb={{8}}>'
            f'<Image image="assets/logo/appicon.png" w={{30}} h={{30}} rounded={{10}} />'
            f'<Frame grow={{1}} flex="col" gap={{1}}>{T(13,"bold","var:text/strong","Medra")}'
            f'{T(10,"regular","var:text/muted","medra.ng/MDR-9012-44")}</Frame>'
            f'<Frame name="Btn Open help" flex="row" px={{9}} py={{7}} rounded={{9}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{I("circle-help",14,N_IC)}</Frame></Frame>'
            f'<Frame grow={{1}} w="fill" flex="col" gap={{13}} px={{16}} pt={{4}} pb={{14}}>{children}</Frame></Frame>')

E7_NOTICE = dcard(
    f'<Frame w="fill" flex="col" gap={{11}} items="center" pb={{2}}>'
    f'{big_icon("shield-check","ok",72)}'
    f'{T(21,"bold","var:text/strong","You are opening one person’s medical request")}'
    f'{T(14,"regular","var:text/muted","Halima Sani asked Garki Medical Centre to send you what you need for an MRI. Please read this before you continue.",w="fill",align="center")}</Frame>'
    + hr()
    + perm_row("You will see the request and why it was made", True)
    + perm_row("You can upload the report when you are finished", True)
    + perm_row("You will not see the rest of her medical history", False, "Only what she agreed to send for this one job")
    + perm_row("This link stops working once you finish", False, "It is for this request only, and expires in 7 days regardless")
    + hr()
    + checkbox("I am the person this was sent to, and I will use it only for this request", "Ext confirm")
    + T(11, "regular", "var:text/muted",
        "Recorded with the time you accepted. Misusing a medical record is an offence under the Nigeria Data Protection Act 2023.", w="fill"))

add("Referral", "E7-ext-notice",
    ext_desk("Org · External — E7 Privacy Notice",
        f'{E7_NOTICE}{dcta("Continue","Open ext task E8","arrow-right")}'
        f'{dbtn("This is not for me","Ext wrong E7","x","ghost",full=True)}'),
    ext_mob("Org · External — E7 Privacy Notice · Mobile",
        f'{E7_NOTICE}{dcta("Continue","Open ext task E8","arrow-right")}'
        f'{dbtn("This is not for me","Ext wrong E7","x","ghost",full=True)}'))

E8_TASK = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","FROM GARKI MEDICAL CENTRE")}{status_pill("pending","Not started")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(22,"bold","var:text/strong","MRI lumbar spine")}'
    + T(13, "regular", "var:text/muted", "Without contrast · routine · requested 12 August by Dr. Ngozi Okafor", w="fill") + '</Frame>'
    + hr()
    + rows_of([kv("Patient", "Halima Sani", "circle-user"), kv("Age", "29", "cake"),
               kv("Medra ID", "MDR-9012-44", "hash"), kv("Phone", "+234 803 555 0144", "phone")], 4, 12)
    + note_section("Why it was requested",
                   "Six weeks of lower back pain with left leg radiation. No red flags. Conservative treatment has not helped. Please assess for disc herniation.",
                   "file-text")
    + note_section("What they also sent",
                   "Two lumbar X-rays from June 2026, and her current medicines. Nothing else from her record was shared.",
                   "paperclip"))

E8_STEPS = dgroup("Three steps", [
    prep_step(1, "Do the scan", "Whenever suits you and her — there is no booking to keep"),
    prep_step(2, "Upload the report here", "A short form, plus the file itself"),
    prep_step(3, "Press done", "The link closes and the report reaches her doctor and her record"),
], footer="You do not need an account and you will not be asked for one. If you would rather use Medra properly, there is a link at the end.")

add("Referral", "E8-ext-task",
    ext_desk("Org · External — E8 What You Are Asked To Do",
        f'{E8_TASK}{E8_STEPS}{dcta("Upload the report","Open ext upload E9","upload")}'
        f'{dbtn("I cannot do this","Ext decline E8","x","ghost",full=True)}'),
    ext_mob("Org · External — E8 What You Are Asked To Do · Mobile",
        f'{E8_TASK}{E8_STEPS}{dcta("Upload the report","Open ext upload E9","upload")}'
        f'{dbtn("I cannot do this","Ext decline E8","x","ghost",full=True)}'))

E9_FORM = dcard(
    eyerow("The report")
    + upload("Ext camera E9", label="Photograph the report or choose a file")
    + f'<Frame w="fill" flex="row" gap={{12}}>'
    + f'<Frame grow={{1}} flex="col">{field("Date done","calendar-days","14 August 2026",ph=False)}</Frame>'
    + f'<Frame grow={{1}} flex="col">{field("Your facility","building-2","Lifebridge Diagnostics",ph=False)}</Frame></Frame>'
    + field("Reported by", "circle-user", "Dr. A. Ogundipe, Radiologist", ph=False)
    + hr() + eyerow("Findings")
    + field("Impression", "file-text",
            "L4/L5 left paracentral disc protrusion with contact of the traversing left L5 nerve root. No canal stenosis. No other abnormality.", ph=False)
    + field_chips("Overall", ["Normal", "Abnormal — routine", "Abnormal — needs attention"], 1, "Ext overall")
    + dtoggle("phone-call", "Happy to be called about this", sub="Only by the doctor who requested it, only about this request", on=True, name="Ext callable"))

E9_WHY = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("info",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Why the boxes")}</Frame>'
    + T(12, "regular", "var:text/default",
        "The file on its own cannot be searched, trended or compared with her last scan. The three boxes take a few seconds and make it useful for the rest of her life. Everything else is optional.", w="fill"),
    bg="var:state/info-bg", stroke=None)

add("Referral", "E9-ext-upload",
    ext_desk("Org · External — E9 Upload the Report",
        f'{E9_FORM}{E9_WHY}{dcta("Send it and finish","Open ext done E10","send")}'),
    ext_mob("Org · External — E9 Upload the Report · Mobile",
        f'{E9_FORM}{E9_WHY}{dcta("Send it and finish","Open ext done E10","send")}'))

E10_DONE = dcard(
    f'<Frame w="fill" flex="col" gap={{13}} items="center">'
    f'{big_icon("badge-check","ok",84)}'
    f'{T(22,"bold","var:text/strong","Sent. This link is now closed.")}'
    f'{T(14,"regular","var:text/muted","The report is with Dr. Ngozi Okafor and in Halima Sani’s own record, which she keeps wherever she goes next. Thank you.",w="fill",align="center")}</Frame>')

E10_NEXT = dgroup("What happened", [
    drow("check-check", "Report delivered", value="14 Aug 14:22", sub="To Dr. Okafor at Garki Medical Centre", name="Ext d1", tone="ok", chevron=False),
    drow("clipboard-list", "Added to her record", sub="Labelled with your facility and the radiologist's name", name="Ext d2", tone="ok", chevron=False),
    drow("lock", "Your access has ended", sub="This page will not open again", name="Ext d3", chevron=False),
])

E10_JOIN = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("sparkles",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","You have had four of these this month")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Organisations on Medra get requests in a queue instead of a link, keep their own record of what they reported, and are listed where members search. It costs nothing to look.", w="fill")
    + f'<Frame w="fill" flex="row" gap={{9}}>'
    + dbtn("See what it involves", "Ext join E10", "arrow-right", "navy")
    + dbtn("No thanks", "Ext nothanks E10", None, "ghost") + '</Frame>',
    bg="var:state/info-bg", stroke=None)

add("Referral", "E10-ext-done",
    ext_desk("Org · External — E10 Done",
        f'{E10_DONE}{E10_NEXT}{E10_JOIN}'),
    ext_mob("Org · External — E10 Done · Mobile",
        f'{E10_DONE}{E10_NEXT}{E10_JOIN}'))

E11_GONE = empty_state("link-2-off", "This link has already been used",
    "It was opened and completed on 11 August by Zenith Imaging. A single-use link only works once, which is what keeps a member's record safe.",
    primary=dcta("Ask Garki Medical Centre for a new one", "Ext newlink E11", "message-circle"),
    secondary=dbtn("What is Medra?", "Ext about E11", "circle-help", "ghost", full=True), tone="warn")

E11_WHY = dgroup("Why you are seeing this", [
    drow("check-check", "The job was already done", sub="Completed 11 August at 16:04", name="Ex1", chevron=False, tone="ok"),
    drow("timer", "Or the link timed out", sub="Every link expires after 7 days whether it was used or not", name="Ex2", chevron=False),
    drow("shield-x", "Or the sender revoked it", sub="They can close a link at any time", name="Ex3", chevron=False),
], footer="If you still need to send a report, ask the organisation that referred the patient to issue a new link. It takes them a few seconds.")

add("Referral", "E11-ext-expired",
    ext_desk("Org · External — E11 Link Expired", f'{E11_GONE}{E11_WHY}'),
    ext_mob("Org · External — E11 Link Expired · Mobile", f'{E11_GONE}{E11_WHY}'))

# =====================================================================================
# 6. ACCESS, MONEY & REPORTS
# =====================================================================================
F1_NOW = dgroup("Who can see a record right now", [
    patient_row("avatar-4.jpg", "Dr. Ngozi Okafor", "Consulting", "Amara Okeke · until this visit is marked complete", "End", "Acc okafor", tag="confirmed"),
    patient_row("avatar-2.jpg", "Sister Ifeoma Uche", "Nursing", "Amara Okeke · vitals · until complete", "End", "Acc ifeoma", tag="confirmed"),
    patient_row("avatar-1.jpg", "Mr. Sola Adeniyi", "Laboratory", "Amara Okeke · this order only, not the record", "End", "Acc sola", tag="soon"),
    patient_row("avatar-6.jpg", "Lifebridge Diagnostics", "External · single-use link", "Halima Sani · MRI request · expires when done", "Revoke", "Acc lifebridge", tag="pending"),
], footer="Access is per episode of care. Ending one here closes it immediately and the member is told — use it when someone opened something they should not have.")

F1_RULE = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",17,OK_IC)}'
    f'{T(14,"semibold","var:text/strong","The organisation never owns the record")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Garki holds a copy of what happened here. The record belongs to the member, travels with them, and is theirs to share or withhold. If Garki left Medra tomorrow, every member would keep everything.", w="fill"),
    bg="var:state/success-bg", stroke=None)

F1_ASKS = dgroup("Requests we have made", [
    drow("message-square-text", "Amara Okeke — prescription history", value="Agreed", sub="Asked by Dr. Okafor 09:14 · she agreed 09:16", name="Ask amara", tone="ok"),
    drow("message-square-text", "Musa Ibrahim — home readings", value="Declined", sub="Asked 12 Aug · declining is normal and does not affect his care", name="Ask musa"),
    drow("message-square-text", "Grace Okeke — records from another clinic", value="Waiting", sub="Asked 2 hours ago", name="Ask grace", tone="warn"),
    drow("history", "Every read and write, by name and time", sub="The member sees the same list for their own record", name="Open audit F2"),
])

addx("Govern", "F1-access",
    o_desk("Org · Access — F1 Who Has Access", ("Access",),
        f'{dhead([("Who can see",False),("what, right now",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F1_NOW}{F1_ASKS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F1_RULE}</Frame></Frame>',
        NAV["Access"], badges=BADGES),
    o_head("Access", "4 open · 1 external", back=False,
           stats=[("4", "Open now"), ("1", "External"), ("3", "Requests")]),
    pinned=F1_NOW,
    sections=[
      ("asks", "message-square-text", "Requests we have made", "One agreed, one declined, one waiting", "3", None, F1_ASKS, None),
      ("rule", "shield-check", "The organisation never owns the record", "It belongs to the member", None, "ok", F1_RULE, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F2 audit
F2_LOG = dgroup("Today", [
    audit_row("Dr. Ngozi Okafor", "Opened Amara Okeke's record", "09:14 · consultation · Garki"),
    audit_row("Sister Ifeoma Uche", "Recorded vitals for Amara Okeke", "09:22 · nursing · Garki"),
    audit_row("Mr. Sola Adeniyi", "Accepted a test order for Amara Okeke", "09:31 · laboratory · Garki"),
    audit_row("Miss Ngozi Peter", "Checked in Blessing Ade", "10:02 · front desk · Garki"),
    audit_row("Lifebridge Diagnostics", "Opened a single-use link for Halima Sani", "09:14 · external"),
    audit_row("Mrs. Adaeze Nwosu", "Suspended Mr. Emeka Obi", "08:40 · admin · Garki"),
], footer="Every read and every write, by name and by time. The member sees the same list for their own record — which is the point.")

F2_FILTERS = rows_of([
    dbtn("Everything", "Aud all", None, "navy", size="sm"),
    dbtn("Record opened", "Aud read", None, "ghost", size="sm"),
    dbtn("Changed", "Aud write", None, "ghost", size="sm"),
    dbtn("External", "Aud ext", None, "ghost", size="sm"),
    dbtn("Admin", "Aud admin", None, "ghost", size="sm"),
], 5, 8)

F2_FLAGS = dgroup("Worth a look", [
    drow("shield-alert", "1 emergency access used", sub="Dr. Eze · unconscious member · 2 Aug · reason recorded, member told", name="Flag glass", tone="err"),
    drow("clock", "2 records opened outside working hours", sub="Both by Dr. Okafor, both her own patients", name="Flag hours", tone="warn"),
    drow("user-x", "0 reads by anyone suspended", sub="As it should be", name="Flag suspended", tone="ok"),
])

addx("Govern", "F2-audit",
    o_desk("Org · Access — F2 Audit Log", ("Access", "Audit"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("Who opened",False),("what",True)],26)}'
        f'{dbtn("Export","Export audit F2","download","ghost",grow=False,size="sm")}</Frame>'
        f'{F2_FILTERS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F2_LOG}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F2_FLAGS}</Frame></Frame>',
        NAV["Access"], badges=BADGES),
    o_head("Audit log", "Every read and every write", stats=[("312", "Today"), ("1", "Emergency"), ("0", "By suspended")]),
    pinned=F2_LOG,
    sections=[("flags", "shield-alert", "Worth a look", "One emergency access this month", "3", "warn", F2_FLAGS, None)],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F3 compliance
F3_UNDERTAKING = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","DATA-PRIVACY UNDERTAKING")}{status_pill("confirmed","Accepted")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(18,"bold","var:text/strong","Version 2.1")}'
    + T(12, "regular", "var:text/muted", "Accepted 4 February 2026, 09:12, by Mrs. Adaeze Nwosu on behalf of Garki Medical Centre", w="fill") + '</Frame>'
    + hr()
    + drow("shield-check", "We hold member data only for care", sub="Never for marketing, never sold, never shared without consent", name="Und care", chevron=False)
    + drow("users", "Only people with a reason may look", sub="Access is per episode of care and every read is logged", name="Und access", chevron=False)
    + drow("triangle-alert", "We report a breach within 72 hours", sub="To Medra and to the NDPC, as the NDPA 2023 requires", name="Und breach", chevron=False)
    + drow("file-text", "Read the full undertaking", sub="The exact text you accepted", name="Und read"))

F3_STATE = dgroup("Where you stand", [
    checklist_row(True, "Undertaking accepted", "v2.1 · by the contact person · timestamped", "Cmp und"),
    checklist_row(True, "Every seat has a named person", "27 of 27 — no shared logins found", "Cmp seats"),
    checklist_row(False, "Retention policy set", "How long you keep a record after someone stops coming", "Cmp retention",
                  action=dbtn("Set it", "Set retention F3", None, "ghost", grow=False, size="sm")),
    checklist_row(False, "Named data protection contact", "Required once you pass 50 staff — you have 27", "Cmp dpo"),
], footer="Medra cannot make an organisation compliant. It can make it obvious what is missing, and prove what happened when someone asks.")

F3_SHARED = dgroup("Shared logins are the risk", [
    drow("user-x", "0 accounts used from two places at once", sub="Checked continuously", name="Sh none", chevron=False, tone="ok"),
    drow("smartphone", "Every seat is one person", sub="A shared front-desk login would make the audit log meaningless", name="Sh one", chevron=False),
    drow("banknote", "Seats are cheap for exactly this reason", sub="Front-desk and support seats are priced below a practitioner", name="Open plan A4"),
])

addx("Govern", "F3-compliance",
    o_desk("Org · Access — F3 Privacy &amp; Compliance", ("Access", "Compliance"),
        f'{dhead([("What you signed,",False),("and where you stand",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F3_UNDERTAKING}{F3_STATE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F3_SHARED}</Frame></Frame>',
        NAV["Access"], badges=BADGES),
    o_head("Privacy and compliance", "Undertaking v2.1 accepted",
           stats=[("v2.1", "Accepted"), ("2/4", "Complete"), ("0", "Shared logins")]),
    pinned=F3_UNDERTAKING,
    sections=[
      ("state", "list-checks", "Where you stand", "Two items still open", "2/4", "warn", F3_STATE, None),
      ("shared", "user-x", "Shared logins are the risk", "None found", "3", "ok", F3_SHARED, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F4 reports
F4_CHART = dcard(
    eyerow("Visits a month", f'<Frame name="Btn Report range" flex="row">{T(11,"semibold","var:text/accent","Last 6 months")}</Frame>')
    + f'<Frame w="fill" flex="row" gap={{10}} items="end" h={{176}}>'
    + "".join(f'<Frame grow={{1}} flex="col" gap={{7}} items="center">'
              f'<Frame w="fill" h={{{h}}} rounded={{10}} image="assets/img/btn-amber.jpg" overflow="hidden" />'
              f'{T(10,"regular","var:text/muted",m)}</Frame>'
              for m, h in (("Mar", 74), ("Apr", 96), ("May", 88), ("Jun", 118), ("Jul", 132), ("Aug", 146)))
    + '</Frame>'
    + T(11, "regular", "var:text/muted", "1,412 visits in August so far — up 11% on July, mostly follow-ups.", w="fill"))

F4_BREAK = dgroup("Where the load is", [
    kpi_line("Consulting", "1,412 visits"),
    kpi_line("Laboratory", "612 orders"),
    kpi_line("Pharmacy", "489 dispensed"),
    kpi_line("Nursing", "1,106 tasks"),
    kpi_line("Front desk", "1,842 check-ins"),
], footer="Nursing and the front desk do more transactions than anyone. It is worth remembering when you decide how many seats each department gets.")

F4_QUALITY = dgroup("Things worth watching", [
    drow("circle-slash", "No-show rate", value="7.2%", sub="Down from 11% before payment-before-booking", name="Rep noshow", tone="ok", chevron=False),
    drow("clock", "Median wait to be seen", value="14 min", sub="Up 4 minutes this week — Tuesdays are the worst", name="Rep wait", tone="warn", chevron=False),
    drow("notebook-pen", "Notes signed same day", value="94%", sub="Six unsigned notes older than 48 hours", name="Rep signed", tone="warn", chevron=False),
    drow("timer", "Laboratory turnaround", value="2h 40m", sub="Target 4 hours", name="Rep lab", tone="ok", chevron=False),
    drow("share-2", "Referrals answered in a day", value="88%", sub="Three took longer than two days", name="Rep ref", chevron=False),
])

addx("Govern", "F4-reports",
    o_desk("Org · Reports — F4 Reports", ("Reports",),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("How the",False),("organisation is running",True)],26)}'
        f'{dbtn("Export","Export report F4","download","ghost",grow=False,size="sm")}</Frame>'
        f'{F4_CHART}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F4_QUALITY}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F4_BREAK}</Frame></Frame>',
        NAV["Reports"], badges=BADGES),
    o_head("Reports", "August · 1,412 visits", back=False, ctx="All branches",
           stats=[("1,412", "Visits"), ("7.2%", "No-show"), ("14m", "Wait")]),
    pinned=F4_CHART,
    sections=[
      ("quality", "activity", "Things worth watching", "Waits are up, notes are behind", "5", "warn", F4_QUALITY, None),
      ("load", "layers", "Where the load is", "Nursing and the desk do the most", "5", None, F4_BREAK, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F5 settings
F5_HOURS = dgroup("When you are open", [
    dtoggle("calendar-days", "Monday to Friday", sub="08:00 – 18:00 · all departments", on=True, name="Hrs weekday"),
    dtoggle("calendar-days", "Saturday", sub="09:00 – 14:00 · consulting and laboratory only", on=True, name="Hrs sat"),
    dtoggle("calendar-days", "Sunday", sub="Closed", on=False, name="Hrs sun"),
    drow("calendar-x", "Public holidays", value="Nigeria", sub="Bookings close automatically; you can override any one", name="Hrs holidays"),
])

F5_POLICY = dgroup("Policies members are shown", [
    drow("banknote", "Payment", value="Before booking", sub="Shown on every provider page in this organisation", name="Pol pay"),
    drow("undo-2", "Cancellation", value="Free over 4 hours ahead", name="Pol cancel"),
    drow("circle-slash", "No-show", value="We keep 50%", sub="Pilot policy, configurable per organisation", name="Pol noshow"),
    drow("clock", "We answer requests within", value="24 hours", sub="Referrals, refills and messages", name="Pol sla"),
], footer="Every one of these is shown to a member before they book. Nobody is surprised afterwards.")

F5_CONTACT = dcard(
    eyerow("How members and other organisations reach you")
    + field("Reception phone", "phone", "+234 803 555 0110", ph=False)
    + field("Email", "mail", "hello@garkimedical.ng", ph=False)
    + dtoggle("message-circle", "WhatsApp for appointments", sub="+234 803 555 0110", on=True, name="Ct wa")
    + dtoggle("share-2", "Accept referrals from any Medra organisation", sub="Turning this off makes you invisible to referrers", on=True, name="Ct refer"))

addx("Govern", "F5-settings",
    o_desk("Org · Settings — F5 Organisation Settings", ("Settings",),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("How this organisation",False),("behaves",True)],26)}'
        f'{dbtn("Save changes","Save settings F5","check","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F5_HOURS}{F5_CONTACT}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F5_POLICY}'
        f'{dgroup("Also here", [drow("building-2","Branches",value="3",name="Open branches A3"),drow("circle-user","Public profile",value="70%",name="Open profile A5"),drow("users","Roles and permissions",sub="What each role can reach",name="Open roles C7"),drow("shield-check","Privacy and compliance",sub="Undertaking v2.1 accepted",name="Open compliance F3"),drow("chart-column","Reports",sub="Volumes, waits, turnaround",name="Nav Reports"),drow("credit-card","Subscription and invoices",name="Open billing F6")])}</Frame></Frame>',
        NAV["Settings"], badges=BADGES),
    o_head("Settings", "Garki Medical Centre", back=False, ctx="Garki Medical Centre",
           right=f'<Frame name="Btn Save settings F5" w={{36}} h={{36}} rounded={{12}} bg="#2E3640" flex="col" justify="center" items="center">{I("check",17,W_IC)}</Frame>'),
    sections=[
      ("hours", "clock", "When you are open", "Mon–Sat · holidays automatic", None, None, F5_HOURS, None),
      ("policy", "scale", "Policies members are shown", "Payment, cancellation, no-show", "4", None, F5_POLICY, None),
      ("contact", "phone", "How people reach you", "Phone, email, WhatsApp, referrals", None, None, F5_CONTACT, None),
      ("more", "layers", "Branches, departments and profile", "The rest of the organisation", None, None,
       dgroup("Also here", [
         drow("building-2", "Branches", value="3", name="Open branches A3"),
         drow("layers", "Departments and seats", value="5", name="Nav Departments"),
         drow("circle-user", "Public profile", value="70%", name="Open profile A5"),
         drow("users", "Roles and permissions", sub="What each role can reach", name="Open roles C7"),
         drow("shield-check", "Privacy and compliance", sub="Undertaking v2.1 accepted", name="Open compliance F3"),
         drow("chart-column", "Reports", sub="Volumes, waits, turnaround", name="Nav Reports"),
         drow("credit-card", "Subscription and invoices", sub="Group plan · ₦296,000 a month", name="Open billing F6"),
       ]), None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F6 subscription
F6_STATE = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","FREE TRIAL")}{status_pill("soon","26 days left")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(28,"bold","var:text/strong","₦296,000 a month")}'
    + T(13, "regular", "var:text/muted", "Group plan · 12 practitioners · 3 branches · 19 support and desk seats. First charge 5 March.", w="fill") + '</Frame>'
    + bar(13, "amber", 10)
    + f'<Frame w="fill" flex="row" gap={{10}}>'
    + dbtn("Add a card", "Add card F6", "credit-card", "navy")
    + dbtn("Change plan", "Open plan A4", "layers", "ghost") + '</Frame>')

F6_INVOICES = dgroup("Invoices", [
    drow("receipt", "Nothing charged yet", sub="Your first invoice will be dated 5 March 2026", name="Inv none", chevron=False),
    drow("download", "Download a pro-forma", sub="Some organisations need one to raise a purchase order", name="Inv proforma"),
    drow("building-2", "Billing details", value="Garki Medical Centre", sub="RC 1489302 · TIN on file", name="Inv details"),
])

F6_WHAT = dgroup("What the subscription covers", [
    drow("infinity", "Every department and every seat you have bought", name="Cov seats", chevron=False, tone="ok"),
    drow("users", "Unlimited members", sub="You are never charged for the people you care for", name="Cov members", chevron=False, tone="ok"),
    drow("share-2", "Referrals in and out, and single-use links", name="Cov refer", chevron=False, tone="ok"),
    drow("banknote", "Not a cut of your fees", sub="Medra earns from the subscription, not from what a member pays you", name="Cov cut", chevron=False, tone="ok"),
], footer="If the trial ends without a card, the console locks but nothing is deleted — and members keep their records regardless. An unpaid invoice never costs a member their history.")

addx("Govern", "F6-billing",
    o_desk("Org · Settings — F6 Subscription", ("Money", "Subscription"),
        f'{F6_STATE}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F6_WHAT}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F6_INVOICES}</Frame></Frame>',
        NAV["Settings"], badges=BADGES),
    o_head("Subscription", "Free trial · 26 days left", back=False,
           stats=[("₦296k", "A month"), ("26d", "Trial"), ("None", "Card")]),
    pinned=F6_STATE,
    sections=[
      ("what", "info", "What it covers", "Every seat, unlimited members", "4", "ok", F6_WHAT, None),
      ("invoices", "receipt", "Invoices", "Nothing charged yet", None, None, F6_INVOICES, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# =====================================================================================
# 7. STATES & EDGE CASES
# =====================================================================================
STATE_LIST = [("X1", "lock", "Seats full"), ("X2", "badge-alert", "Not verified"),
              ("X3", "credit-card", "Locked"), ("X4", "calendar-check", "Nothing booked"),
              ("X5", "cloud-off", "Offline"), ("X6", "triangle-alert", "Error"),
              ("X7", "loader", "Loading")]

def state_nav(active, per=7):
    cells = []
    for code, ic, label in STATE_LIST:
        on = code == active
        st = ('image="assets/img/btn-amber.jpg" overflow="hidden"' if on
              else 'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}')
        col = "var:text/on-dark" if on else "var:text/muted"
        cells.append(f'<Frame name="Btn State {code}" flex="row" gap={{6}} items="center" px={{11}} py={{7}} '
                     f'rounded={{999}} {st}>{I(ic,12,W_IC if on else M_IC)}'
                     f'{T(11,"semibold" if on else "regular",col,label)}</Frame>')
    return (f'<Frame w="fill" flex="col" gap={{7}}>'
            f'{T(10,"semibold","var:text/faint","STATE — FOR REVIEW, NOT A REAL CONTROL")}'
            f'{rows_of(cells, per, 7)}</Frame>')

X1_MAIN = empty_state("lock", "Front desk has no seats left",
    "All five front-desk seats are in use. You can add seats, move a seat from another department, or suspend someone who has left.",
    primary=dcta("Add seats", "Open plan A4", "plus"),
    secondary=dbtn("Move a seat from another department", "Nav Departments", "repeat", "ghost", full=True), tone="warn")

X1_OPTS = dgroup("Three ways out", [
    drow("plus", "Add seats to this department", value="+₦6,000 each", sub="Charged pro rata from today", name="Open plan A4"),
    drow("repeat", "Move an unused seat", sub="Consulting has one seat nobody is sitting in", name="Nav Departments"),
    drow("user-x", "Free a seat", sub="Mr. Emeka Obi has been suspended since 2 August", name="Person emeka", tone="warn"),
])

addx("States", "X1-seats",
    o_desk("Org · States — X1 Seats Full", ("Departments", "Front desk"),
        f'{state_nav("X1")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X1_MAIN}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{X1_OPTS}</Frame></Frame>',
        NAV["Departments"], dept="Front desk", badges=BADGES),
    o_head("Seats full", "Front desk · 5 of 5", back=False, stats=[("5/5", "Seats"), ("1", "Suspended"), ("₦6k", "Per seat")]),
    pinned=f'{state_nav("X1",3)}{X1_MAIN}',
    sections=[("opts", "layers", "Three ways out", "Add, move or free a seat", "3", None, X1_OPTS, None)],
    tab_items=TAB_ADMIN, tab=2)

X2_MAIN = empty_state("badge-alert", "You are not visible to members yet",
    "Your practice licence is still being checked. Everything inside the console works — you can add branches, departments and people — but nobody can find or book you.",
    primary=dcta("See where the check is", "Open verify A2", "arrow-right"),
    secondary=dbtn("What we still need", "Open verify A2", "file-text", "ghost", full=True), tone="warn")

X2_WORKS = dgroup("What works right now", [
    drow("layers", "Departments and seats", sub="Set them up so you are ready the moment you are approved", name="Nav Departments", tone="ok"),
    drow("user-plus", "Inviting people", sub="They verify themselves while you wait", name="Open invite C5", tone="ok"),
    drow("circle-user", "Your public profile", sub="It goes live with you", name="Open profile A5", tone="ok"),
    drow("search", "Being found by members", sub="Not until the licence is accepted", name="Open verify A2", tone="err"),
])

addx("States", "X2-unverified",
    o_desk("Org · States — X2 Not Yet Verified", ("Setup", "Verification"),
        f'{state_nav("X2")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X2_MAIN}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{X2_WORKS}</Frame></Frame>',
        NAV["Today"], urgent=1, badges=BADGES),
    o_head("Not verified yet", "Licence under review", back=False, stats=[("3/4", "Steps"), ("31h", "Median"), ("0", "Bookings")]),
    pinned=f'{state_nav("X2",3)}{X2_MAIN}',
    sections=[("works", "circle-check", "What works right now", "Everything except being found", "4", None, X2_WORKS, None)],
    tab_items=TAB_ADMIN, tab=0)

X3_MAIN = empty_state("credit-card", "The console is locked",
    "The trial ended on 5 March and no card was added. Nothing has been deleted, and no member has lost anything.",
    primary=dcta("Add a card and unlock", "Add card F6", "credit-card"),
    secondary=dbtn("See the plans again", "Open plan A4", "layers", "ghost", full=True), tone="warn")

X3_SAFE = dgroup("What is still true", [
    drow("clipboard-list", "Every member keeps their whole record", sub="It was always theirs. A billing problem here never touches it", name="Lk records", tone="ok", chevron=False),
    drow("calendar-check", "Appointments already booked still happen", value="17", sub="You can still see them and write the notes", name="Lk booked", tone="ok", chevron=False),
    drow("download", "You can export everything", sub="Members, staff, invoices — any time, locked or not", name="Lk export", tone="ok", chevron=False),
])

X3_STOP = dgroup("What has stopped", [
    drow("search", "You are hidden from search", name="Lk search", tone="err", chevron=False),
    drow("calendar-x", "No new bookings or referrals", name="Lk bookings", tone="err", chevron=False),
    drow("inbox", "Department queues are read-only", sub="Nothing new can be ordered, entered or dispensed", name="Lk queues", tone="err", chevron=False),
], footer="Unlock and every queue, seat and setting is exactly where you left it.")

addx("States", "X3-locked",
    o_desk("Org · States — X3 Subscription Locked", ("Money", "Subscription"),
        f'{state_nav("X3")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X3_MAIN}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{X3_SAFE}{X3_STOP}</Frame></Frame>',
        NAV["Settings"], badges=BADGES),
    o_head("Locked", "Trial ended 5 March", back=False, stats=[("0", "New bookings"), ("17", "Still booked"), ("Safe", "Records")]),
    pinned=f'{state_nav("X3",3)}{X3_MAIN}',
    sections=[
      ("safe", "circle-check", "What is still true", "Members keep everything", "3", "ok", X3_SAFE, None),
      ("stop", "circle-x", "What has stopped", "Search, bookings, queues", "3", "err", X3_STOP, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

X4_MAIN = empty_state("calendar-check", "Nothing booked today",
    "Three branches, nobody expected. That is unusual for a Thursday — it is worth checking that your hours and departments are set the way you think they are.",
    primary=dcta("Check the week", "Nav Bookings", "calendar-days"),
    secondary=dbtn("Check opening hours", "Nav Settings", "clock", "ghost", full=True), tone="ok")

X4_WHY = dgroup("What usually causes this", [
    drow("clock", "Hours not set for a branch", sub="Maitama and Wuse are still on the default", name="Nav Settings", tone="warn"),
    drow("stethoscope", "No practitioner has availability", sub="A department with no open slots cannot be booked", name="Nav Departments", tone="warn"),
    drow("badge-alert", "Not verified yet", sub="An unverified organisation is invisible in search", name="Open verify A2"),
    drow("share-2", "Nobody knows you are here", sub="Share your booking link, or ask a referring doctor", name="Nav Referrals"),
])

addx("States", "X4-empty",
    o_desk("Org · States — X4 Nothing Booked", ("Today", "Nothing booked"),
        f'{state_nav("X4")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X4_MAIN}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{X4_WHY}</Frame></Frame>',
        NAV["Today"], urgent=0, badges=BADGES),
    o_head("Nothing booked", "Thursday 14 August", back=False, stats=[("0", "Today"), ("3", "Branches"), ("0", "Waiting")]),
    pinned=f'{state_nav("X4",3)}{X4_MAIN}',
    sections=[("why", "circle-help", "What usually causes this", "Four things worth checking", "4", None, X4_WHY, None)],
    tab_items=TAB_ADMIN, tab=0)

X5_BANNER = alert_strip("cloud-off", "You are offline",
    "Showing what was on this device at 09:41. Check-ins and vitals are saved here and sync the moment you are back.", "warn",
    dbtn("Retry", "Retry X5", "refresh-cw", "ghost", grow=False, size="sm"))

X5_QUEUE = dgroup("Waiting to sync · 4", [
    drow("user-check", "3 check-ins", sub="Blessing Ade, Ngozi Bala, Sola Ade", name="Q checkins", chevron=False),
    drow("activity", "1 set of vitals", sub="Grace Okeke · recorded 09:52", name="Q vitals", chevron=False),
])

X5_WORKS = dgroup("What still works", [
    drow("user-check", "Checking people in", sub="The queue is on this device", name="Off checkin", tone="ok", chevron=False),
    drow("activity", "Recording vitals", sub="Saved here, synced later", name="Off vitals", tone="ok", chevron=False),
    drow("send", "Entering a lab result", sub="Held until you are back", name="Off result", tone="ok", chevron=False),
])

X5_WAITS = dgroup("What waits for the connection", [
    drow("banknote", "Taking a payment", sub="A reference has to be checked against your bank", name="Off pay", tone="warn", chevron=False),
    drow("share-2", "Sending or accepting a referral", sub="It has to reach the other organisation", name="Off refer", tone="warn", chevron=False),
    drow("link", "Issuing a single-use link", sub="The member has to consent first, on their own phone", name="Off link", tone="warn", chevron=False),
])

addx("States", "X5-offline",
    o_desk("Org · States — X5 Offline", ("Front desk", "Offline"),
        f'{state_nav("X5")}{X5_BANNER}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X5_WORKS}{X5_WAITS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{X5_QUEUE}</Frame></Frame>',
        NAV["Today"], dept="Front desk", who=DESK, badges=BADGES),
    o_head("Offline", "Last synced 09:41", back=False, stats=[("4", "Queued"), ("09:41", "Synced"), ("12", "Cached")]),
    pinned=f'{state_nav("X5",3)}{X5_BANNER}{X5_QUEUE}',
    sections=[
      ("works", "circle-check", "What still works", "Check-in, vitals, results", "3", "ok", X5_WORKS, None),
      ("waits", "clock", "What waits", "Payment, referrals, links", "3", "warn", X5_WAITS, None),
    ],
    tab_items=TAB_DESK, tab=0)

X6_MAIN = empty_state("triangle-alert", "Something went wrong on our side",
    "This is not your device and it is not your data — a Medra service failed to answer. Nothing anyone has entered is affected.",
    primary=dcta("Try again", "Retry X6", "refresh-cw"),
    secondary=dbtn("Go to Today", "Nav Today", "layout-dashboard", "ghost", full=True), tone="warn")

X6_REF = dcard(
    f'<Frame w="fill" flex="row" gap={{11}} items="center">{I("copy",16,M_IC)}'
    f'<Frame grow={{1}} flex="col" gap={{2}}>{T(11,"regular","var:text/muted","Reference for support")}'
    f'{T(14,"semibold","var:text/strong","ERR-9920-B4 · 14 Aug 10:18 · allocation-service")}</Frame>'
    f'{dbtn("Copy","Copy ref X6","copy","ghost",grow=False,size="sm")}</Frame>')

X6_SAFE = dgroup("What is safe", [
    drow("user-check", "Every check-in already recorded", name="S checkin", tone="ok", chevron=False),
    drow("badge-check", "Every signed note and entered result", name="S signed", tone="ok", chevron=False),
    drow("banknote", "Payments already taken", sub="Held by your bank, not by this service", name="S money", tone="ok", chevron=False),
])

X6_MEANWHILE = dgroup("If people are waiting", [
    drow("clipboard-list", "Write on paper and enter it later", sub="It has always been the fallback and it is still fine", name="M paper", chevron=False),
    drow("phone-call", "Reach the Medra team", value="4 min median", sub="They can see the same error you can", name="Open help"),
])

addx("States", "X6-error",
    o_desk("Org · States — X6 Error", ("Today", "Error"),
        f'{state_nav("X6")}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start" pt={{6}}>'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{X6_MAIN}{X6_REF}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{X6_SAFE}{X6_MEANWHILE}</Frame></Frame>',
        NAV["Today"], badges=BADGES),
    o_head("Something went wrong", "ERR-9920-B4", back=False, stats=[("Safe", "Your data"), ("4 min", "Support"), ("Ours", "Fault")]),
    pinned=f'{state_nav("X6",3)}{X6_MAIN}{X6_REF}',
    sections=[
      ("safe", "shield-check", "What is safe", "Everything already recorded", "3", "ok", X6_SAFE, None),
      ("meanwhile", "clipboard-list", "If people are waiting", "Paper still works", "2", None, X6_MEANWHILE, None),
    ],
    tab_items=TAB_ADMIN, tab=0)

X7_SKEL_D = (f'{skel(h=104,r=16)}'
             f'{rows_of([skel(h=100,r=16),skel(h=100,r=16),skel(h=100,r=16),skel(h=100,r=16)],4,14)}'
             f'<Frame w="fill" flex="row" gap={{14}} items="start">'
             f'<Frame grow={{1}} flex="col" gap={{12}}>{skel_card(3)}{skel_card(3)}</Frame>'
             f'<Frame grow={{1}} flex="col" gap={{12}}>{skel_card(3)}{skel_card(2)}</Frame></Frame>'
             f'<Frame w="fill" flex="row" gap={{9}} justify="center" items="center" pt={{4}}>'
             f'{I("loader",15,M_IC)}{T(12,"regular","var:text/muted","Loading the day…")}</Frame>')
X7_SKEL_M = (f'{skel(h=96,r=16)}{rows_of([skel(h=84,r=14),skel(h=84,r=14)],2,10)}'
             f'{skel_card(3)}{skel_card(2)}'
             f'<Frame w="fill" flex="row" gap={{9}} justify="center" items="center">'
             f'{I("loader",14,M_IC)}{T(12,"regular","var:text/muted","Loading…")}</Frame>')

addx("States", "X7-loading",
    o_desk("Org · States — X7 Loading", ("Today", "Loading"),
        state_nav("X7") + X7_SKEL_D, NAV["Today"], badges=BADGES),
    o_head("Today", "Loading…", back=False, stats=[("—", "Expected"), ("—", "Waiting"), ("—", "Done")]),
    pinned=state_nav("X7", 3) + X7_SKEL_M,
    tab_items=TAB_ADMIN, tab=0)

# =====================================================================================
# COMPONENT STATES
# =====================================================================================
CMP = []
def cmp_frame(comp, prop, value, body, w=340, h=None, dark=False):
    hh = f' minH={{{h}}}' if h else ''
    bg = "var:bg/band" if dark else "var:bg/base"
    CMP.append((f"cmp/{comp}/{prop}={value}",
        f'<Frame name="cmp/{comp}/{prop}={value}" w={{{w}}}{hh} flex="col" p={{16}} bg="{bg}">{body}</Frame>'))

for st, state in (("Active", "active"), ("Invited", "invited"), ("Suspended", "suspended")):
    cmp_frame("Seat Row", "State", st, seat_row_m("avatar-2.jpg", "Sister Ifeoma Uche", "Nurse", "Nursing", "CSeat", state), w=360)
for st, val, ver in (("Unverified", "O+", False), ("Verified", "O+", True)):
    cmp_frame("Health Fact", "State", st, unverified("Blood group", val, ver, "CFact"), w=360)
for key in ("nursing", "lab", "pharmacy", "desk", "clinic"):
    cmp_frame("Department Card", "Kind", DEPT[key][2].replace(" ", ""), dept_card(key, 3, 4, 5, "CDept"), w=300)
for st, state in (("Open", "open"), ("Used", "used"), ("Expired", "expired"), ("Revoked", "revoked")):
    cmp_frame("Access Link", "State", st, link_row("Lifebridge", "MRI request", state, "Today", "CLink"), w=560)
for st, flag in (("Normal", None), ("High", "high"), ("Low", "low")):
    cmp_frame("Result Line", "Flag", st, result_line("Fasting glucose", "mmol/L", "3.9 – 5.5", "6.4", flag), w=520)
for st, allowed in (("Allowed", True), ("Denied", False)):
    cmp_frame("Permission Row", "State", st, perm_row("Release a result to the member", allowed,
              None if allowed else "A doctor releases"), w=380)

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

AUTH_ORG = ("Auth · Institution — I6 Log In", "Auth · Institution — I6 Log In · Mobile")

NAVMAP = {
  "Btn Nav Today":       NAMES["B1-today"],
  "Btn Nav Bookings":    NAMES["B2-bookings"],
  "Btn Nav People":      NAMES["C4-people"],
  "Btn Nav Departments": NAMES["C1-departments"],
  "Btn Nav Referrals":   NAMES["E1-outbound"],
  "Btn Nav Access":      NAMES["F1-access"],
  "Btn Nav Reports":     NAMES["F4-reports"],
  "Btn Nav Settings":    NAMES["F5-settings"],
  "Btn Notifications":   NAMES["B1-today"],
  "Btn Search member":   NAMES["B3-find"],
  "Btn Open help":       NAMES["X6-error"],
  "Btn Nav More":        NAMES["F5-settings"],
  "Btn Nav Queue":       NAMES["D1-nursing"],
  "Btn Nav Members":     NAMES["B3-find"],
  "Btn Nav Desk":        NAMES["D12-desk"],
  "Btn Nav Walkin":      NAMES["D13-walkin"],
  "Btn Switch branch":   NAMES["A3-branches"],
  "Btn Switch dept":     NAMES["C1-departments"],
}

TRN = [
 # ---- setup
 ("A1-setup","Btn Open verify A2","A2-verify"),("A1-setup","Btn Open invite C5","C5-invite"),
 ("A1-setup","Btn Open billing F6","F6-billing"),
 ("A2-verify","Btn Open branches A3","A3-branches"),("A2-verify","Btn Open invite C5","C5-invite"),
 ("A2-verify","Btn Open profile A5","A5-profile"),
 ("A3-branches","Btn Save branch A3","A3-branches"),("A3-branches","~Btn Add branch A3","A3-branches"),
 ("A3-branches","Btn Branch garki","A3-branches"),("A3-branches","Btn Branch maitama","A3-branches"),
 ("A4-plan","Btn Save plan A4","F6-billing"),("A4-plan","Btn Plan practice","A4-plan"),
 ("A4-plan","Btn Plan group","A4-plan"),("A4-plan","Btn Plan enterprise","A4-plan"),
 ("A5-profile","Btn Save profile A5","A5-profile"),("A5-profile","Btn Preview profile A5","A5-profile"),
  # ---- today & bookings
 ("B1-today","Btn Open alloc B2","B2-bookings"),
 ("B1-today","Btn Open lab D5","D5-lab-queue"),("B1-today","Btn Open desk D12","D12-desk"),
 ("B1-today","~Btn Open walkin D13","D13-walkin"),("B1-today","~Btn Open refer E2","E2-create"),
 ("B1-today","~Btn Open links E6","E6-links"),("B1-today","Btn Add dept C3","C3-add-dept"),
 ("B1-today","Btn Dept clinic","C2-department"),("B1-today","Btn Dept nursing","D1-nursing"),
 ("B1-today","Btn Dept lab","C2-department"),("B1-today","Btn Dept pharmacy","D9-pharmacy"),
 ("B1-today","Btn Dept desk","D12-desk"),
 ("B2-bookings","Btn Assign Alloc Amara","B2-bookings"),("B2-bookings","Btn Assign Alloc Musa","B2-bookings"),
 ("B2-bookings","Btn Alloc rules B2","B2-bookings"),("B2-bookings","~Btn Pick okafor","B2-bookings"),
 ("B2-bookings","~Btn Pick eze","B2-bookings"),
 ("B3-find","Btn Open Amara","D14-checkin"),("B3-find","Btn Open Chidi","D14-checkin"),
 ("B3-find","Btn Open Grace","D14-checkin"),("B3-find","Btn Open walkin D13","D13-walkin"),
 ("B3-find","Btn Scan member B3","B3-find"),("B3-find","Btn Break glass B3","F2-audit"),
 # ---- departments & people
 ("C1-departments","Btn Dept clinic","C2-department"),("C1-departments","Btn Dept nursing","C2-department"),
 ("C1-departments","Btn Dept lab","C2-department"),("C1-departments","Btn Dept pharmacy","C2-department"),
 ("C1-departments","Btn Dept desk","C2-department"),("C1-departments","Btn Add dept C3","C3-add-dept"),
 ("C1-departments","Btn Open plan A4","A4-plan"),
 ("C2-department","Btn Open invite C5","C5-invite"),("C2-department","Btn Open lab D5","D5-lab-queue"),
 ("C2-department","Btn Open lab D8","D8-lab-problem"),
 ("C2-department","Btn Person sola","C6-person"),("C2-department","Btn Person kemi","C6-person"),
 ("C2-department","Btn Person tunde","C6-person"),("C2-department","Btn Person chidera","C6-person"),
 ("C3-add-dept","Btn Back","C1-departments"),("C3-add-dept","Btn Save dept C3","C1-departments"),
 ("C4-people","Btn Open invite C5","C5-invite"),("C4-people","~Btn Import staff C4","C4-people"),
 ("C4-people","Btn Person okafor","C6-person"),("C4-people","Btn Person eze","C6-person"),
 ("C4-people","Btn Person ifeoma","C6-person"),("C4-people","Btn Person sola","C6-person"),
 ("C4-people","Btn Person bayo","C6-person"),("C4-people","Btn Person ngozi","C6-person"),
 ("C4-people","Btn Person chidera","C6-person"),("C4-people","Btn Person emeka","C6-person"),
 ("C5-invite","Btn Back","C4-people"),("C5-invite","Btn Send invite C5","C4-people"),
 ("C6-person","Btn Back","C4-people"),("C6-person","Btn Open audit F2","F2-audit"),
 ("C6-person","Btn Move ifeoma","C1-departments"),("C6-person","Btn Suspend ifeoma","C6-person"),
 ("C6-person","Btn Remove ifeoma","C4-people"),("C6-person","Btn Msg ifeoma","C6-person"),
 ("C7-roles","Btn Role doctor","C7-roles"),("C7-roles","Btn Role nurse","D1-nursing"),
 ("C7-roles","Btn Role lab","D5-lab-queue"),("C7-roles","Btn Role pharm","D9-pharmacy"),
 ("C7-roles","Btn Role desk","D12-desk"),("C7-roles","Btn Role admin","B1-today"),
 # ---- the clinical chain
 ("D1-nursing","Btn Start Task amara","D2-vitals"),("D1-nursing","Btn Start Task chidi","D2-vitals"),
 ("D1-nursing","Btn Start Task musa","D3-administer"),("D1-nursing","Btn Start Task grace","D2-vitals"),
 ("D1-nursing","Btn Start Task halima","D2-vitals"),("D1-nursing","Btn Open escalate D4","D4-escalate"),
 ("D1-nursing","Btn Done blessing","D4-escalate"),
 ("D2-vitals","Btn Back","D1-nursing"),("D2-vitals","Btn Save vitals D2","D1-nursing"),
 ("D3-administer","Btn Back","D1-nursing"),("D3-administer","Btn Save administer D3","D1-nursing"),
 ("D3-administer","Btn Not given D3","D4-escalate"),("D3-administer","Btn Read reason D3","D3-administer"),
 ("D4-escalate","Btn Back","D1-nursing"),("D4-escalate","Btn Send escalate D4","D1-nursing"),
 ("D4-escalate","Btn Esc okafor","D1-nursing"),("D4-escalate","Btn Esc eze","D1-nursing"),
 ("D5-lab-queue","Btn Accept Order amara","D6-lab-order"),("D5-lab-queue","Btn Accept Order grace","D6-lab-order"),
 ("D5-lab-queue","Btn Accept Order musa","D6-lab-order"),("D5-lab-queue","Btn Accept Order halima","D6-lab-order"),
 ("D5-lab-queue","Btn Open lab D8","D8-lab-problem"),("D5-lab-queue","Btn Prog fatima","D7-lab-result"),
 ("D5-lab-queue","Btn Prog emeka","D7-lab-result"),
 ("D6-lab-order","Btn Back","D5-lab-queue"),("D6-lab-order","Btn Open result D7","D7-lab-result"),
 ("D6-lab-order","Btn Open lab D8","D8-lab-problem"),
 ("D7-lab-result","Btn Back","D6-lab-order"),("D7-lab-result","Btn Save result D7","D5-lab-queue"),
 ("D7-lab-result","Btn Change template","D7-lab-result"),
 ("D8-lab-problem","Btn Back","D5-lab-queue"),("D8-lab-problem","Btn Save problem D8","D5-lab-queue"),
 ("D8-lab-problem","Btn Open lab D5","D5-lab-queue"),
 ("D9-pharmacy","Btn Dispense Rx fatima","D10-dispense"),("D9-pharmacy","Btn Dispense Rx amara","D10-dispense"),
 ("D9-pharmacy","Btn Dispense Rx grace","D10-dispense"),("D9-pharmacy","Btn Dispense Rx musa","D10-dispense"),
 ("D9-pharmacy","Btn Open sub D11","D11-substitute"),
 ("D10-dispense","Btn Back","D9-pharmacy"),("D10-dispense","Btn Save dispense D10","D9-pharmacy"),
 ("D10-dispense","Btn Open sub D11","D11-substitute"),
 ("D11-substitute","Btn Back","D9-pharmacy"),("D11-substitute","Btn Send sub D11","D9-pharmacy"),
 ("D11-substitute","Btn Alt ventolin","D11-substitute"),("D11-substitute","Btn Alt generic","D11-substitute"),
 ("D11-substitute","Btn Alt none","D9-pharmacy"),
 ("D12-desk","Btn Open checkin D14","D14-checkin"),("D12-desk","~Btn Open walkin D13","D13-walkin"),
 ("D12-desk","Btn Open alloc B2","B2-bookings"),("D12-desk","~Btn Open inbound E4","E4-inbound"),
 ("D12-desk","Btn Bd amara","D14-checkin"),("D12-desk","Btn Bd grace","D14-checkin"),
 ("D12-desk","Btn Bd blessing","D14-checkin"),("D12-desk","Btn Bd chidi","D14-checkin"),
 ("D13-walkin","Btn Back","D12-desk"),("D13-walkin","Btn Save walkin D13","D12-desk"),
 ("D13-walkin","Btn Scan member B3","B3-find"),("D13-walkin","Btn New member D13","D13-walkin"),
 ("D14-checkin","Btn Back","D12-desk"),("D14-checkin","Btn Save checkin D14","D12-desk"),
 ("D14-checkin","Btn Send waiting","D12-desk"),("D14-checkin","Btn Send nursing","D1-nursing"),
 ("D14-checkin","Btn Send lab","D5-lab-queue"),
 # ---- referrals & external
 ("E1-outbound","Btn Open refer E2","E2-create"),("E1-outbound","Btn Open links E6","E6-links"),
 ("E1-outbound","Btn Open inbound E4","E4-inbound"),("E1-outbound","Btn Ref amara","E3-sent"),
 ("E1-outbound","Btn Ref halima","E6-links"),("E1-outbound","Btn Ref emeka","E1-outbound"),
 ("E1-outbound","Btn Read reply E1","E1-outbound"),("E1-outbound","Btn Chase amara","E1-outbound"),
 ("E2-create","Btn Back","E1-outbound"),("E2-create","Btn Send refer E2","E3-sent"),
 ("E2-create","Btn Draft refer E2","E1-outbound"),("E2-create","Btn Dest bello","E2-create"),
 ("E2-create","Btn Dest wuse","E2-create"),("E2-create","Btn Dest external","E2-create"),
 ("E3-sent","Btn Copy link E3","E3-sent"),("E3-sent","Btn Send wa E3","E7-ext-notice"),
 ("E3-sent","Btn Print slip E3","E3-sent"),
 ("E4-inbound","Btn In halima","E5-inbound-detail"),("E4-inbound","Btn In ibrahim","E5-inbound-detail"),
 ("E4-inbound","Btn In ngozi","E5-inbound-detail"),("E4-inbound","Btn Accept halima","B2-bookings"),
 ("E4-inbound","Btn Accept ibrahim","B2-bookings"),("E4-inbound","Btn Accept ngozi","B2-bookings"),
 ("E5-inbound-detail","Btn Back","E4-inbound"),("E5-inbound-detail","Btn Accept E5","B2-bookings"),
 ("E6-links","~Btn Open refer E2","E2-create"),("E6-links","Btn Link lifebridge","E7-ext-notice"),
 ("E6-links","Btn Link ketu","E7-ext-notice"),("E6-links","Btn Link zenith","E11-ext-expired"),
 ("E6-links","Btn Link stmarys","E11-ext-expired"),("E6-links","Btn Link revoked","E11-ext-expired"),("E6-links","Btn Open audit F2","F2-audit"),
 # ---- the external party's four screens
 ("E7-ext-notice","Btn Open ext task E8","E8-ext-task"),("E7-ext-notice","Btn Ext wrong E7","E11-ext-expired"),
 ("E8-ext-task","Btn Open ext upload E9","E9-ext-upload"),("E8-ext-task","Btn Ext decline E8","E11-ext-expired"),
 ("E9-ext-upload","Btn Open ext done E10","E10-ext-done"),("E9-ext-upload","Btn Ext camera E9","E9-ext-upload"),
 ("E10-ext-done","Btn Ext join E10","E10-ext-done"),("E10-ext-done","Btn Ext nothanks E10","E10-ext-done"),
 ("E11-ext-expired","Btn Ext newlink E11","E11-ext-expired"),("E11-ext-expired","Btn Ext about E11","E11-ext-expired"),
 # ---- govern
 ("F1-access","Btn Open audit F2","F2-audit"),("F1-access","Btn Acc lifebridge","E6-links"),
 ("F1-access","Btn Ask amara","F1-access"),("F1-access","Btn Ask grace","F1-access"),
 ("F2-audit","~Btn Export audit F2","F2-audit"),("F2-audit","Btn Flag glass","F2-audit"),
 ("F3-compliance","Btn Und read","F3-compliance"),("F3-compliance","Btn Set retention F3","F3-compliance"),
 ("F3-compliance","Btn Open plan A4","A4-plan"),
 ("F4-reports","~Btn Export report F4","F4-reports"),("F4-reports","Btn Report range","F4-reports"),
 ("F5-settings","Btn Save settings F5","F5-settings"),("F5-settings","Btn Open branches A3","A3-branches"),
 ("F5-settings","Btn Open profile A5","A5-profile"),("F5-settings","Btn Open billing F6","F6-billing"),
 ("F5-settings","Btn Open roles C7","C7-roles"),("F5-settings","Btn Open compliance F3","F3-compliance"),
 ("F6-billing","Btn Add card F6","F6-billing"),("F6-billing","Btn Open plan A4","A4-plan"),
 ("F6-billing","Btn Inv proforma","F6-billing"),("F6-billing","Btn Inv details","F6-billing"),
 # ---- states
 ("X1-seats","Btn Open plan A4","A4-plan"),("X1-seats","Btn Person emeka","C6-person"),
 ("X2-unverified","Btn Open verify A2","A2-verify"),("X2-unverified","Btn Open invite C5","C5-invite"),
 ("X2-unverified","Btn Open profile A5","A5-profile"),
 ("X3-locked","Btn Add card F6","F6-billing"),("X3-locked","Btn Open plan A4","A4-plan"),
 ("X4-empty","Btn Open verify A2","A2-verify"),
 ("X5-offline","Btn Retry X5","D12-desk"),
 ("X6-error","Btn Retry X6","B1-today"),("X6-error","Btn Copy ref X6","X6-error"),
 ("X7-loading","Btn State X1","X1-seats"),
] + [
 (src, "Btn State " + dst[:2], dst)
 for src in ("X1-seats","X2-unverified","X3-locked","X4-empty","X5-offline","X6-error","X7-loading")
 for dst in ("X1-seats","X2-unverified","X3-locked","X4-empty","X5-offline","X6-error","X7-loading")
 if src != dst
]

def resolve(target, side):
    if target == "AUTH": return AUTH_ORG[side]
    return NAMES[target][side]

BTNS = {}
for _pg, _fn, _jsx in frames:
    BTNS[nm_of(_jsx)] = set(re.findall(r'name="(Btn [^"]+)"', _jsx))
HUB_ONLY = {"Btn Back", "Btn Close sheet"}

resolved = []
for fid, hot, target in TRN:
    if fid not in NAMES: raise SystemExit(f"unknown source frame {fid}")
    soft = hot.startswith("~"); hot = hot[1:] if soft else hot
    if not soft or hot in BTNS.get(NAMES[fid][0], ()):
        resolved.append([NAMES[fid][0], hot, resolve(target, 0)])
    fam = FAMILY.get(fid, [NAMES[fid][1]])
    hits = [fam[0]] if hot in HUB_ONLY else [f for f in fam if hot in BTNS.get(f, ())]
    if not hits and not soft: hits = [fam[0]]
    for f in hits:
        resolved.append([f, hot, resolve(target, 1)])

AUTO_SPEC = {}
for _frm, _hot, _to, _kind in AUTO:
    resolved.append([_frm, _hot, _to]); AUTO_SPEC[_hot] = _kind

# The external party's four screens have no navigation at all — they are a page on a
# stranger's phone. The sweep must not staple a console tab bar onto them.
EXT = {f for fid in ("E7-ext-notice", "E8-ext-task", "E9-ext-upload", "E10-ext-done", "E11-ext-expired")
       for f in NAMES[fid]}

nav_jobs = []
for fid, pair in NAMES.items():
    for side in (0, 1):
        if pair[side] in EXT: continue
        for hot, target in NAVMAP.items():
            nav_jobs.append([pair[side], hot, target[side]])
for _nm in MOBILE_EXTRA:
    for hot, target in NAVMAP.items():
        nav_jobs.append([_nm, hot, target[1]])

order_js, starts_js = {}, {}
for page, fids in ORDER.items():
    if page == "Components": continue
    order_js[PAGE_FIGMA[page]] = ROWS[page]
    starts_js[PAGE_FIGMA[page]] = [NAMES[fids[0]][0], NAMES[fids[0]][1]]

MOTION = json.dumps({
  "default": {"type": "SMART_ANIMATE", "easing": "GENTLE", "duration": 0.26},
  "push":    {"type": "MOVE_IN",  "direction": "LEFT",   "easing": "GENTLE",  "duration": 0.24},
  "pop":     {"type": "MOVE_OUT", "direction": "RIGHT",  "easing": "EASE_IN", "duration": 0.20},
  "sheet":   {"type": "MOVE_IN",  "direction": "BOTTOM", "easing": "GENTLE",  "duration": 0.30},
  "instant": {"type": "SMART_ANIMATE", "easing": "LINEAR", "duration": 0.01},
})
PUSH = json.dumps(["Btn Open verify A2", "Btn Open branches A3", "Btn Open profile A5", "Btn Open plan A4",
                   "Btn Open invite C5", "Btn Open billing F6", "Btn Open audit F2", "Btn Open refer E2",
                   "Btn Open links E6", "Btn Open inbound E4", "Btn Open result D7", "Btn Open checkin D14",
                   "Btn Open walkin D13", "Btn Person okafor", "Btn Person ifeoma", "Btn Person sola",
                   "Btn Dept clinic", "Btn Dept nursing", "Btn Dept lab", "Btn Dept pharmacy", "Btn Dept desk"])
POP = json.dumps(["Btn Back"])
SHEET = json.dumps(["Btn Open escalate D4", "Btn Open sub D11", "Btn Open lab D8", "Btn Add dept C3"])

linker = ("(async () => {\n"
 "  // Medra Organisation — wire the prototype, close the navigation, arrange the canvas.\n"
 "  // Organisation-module only. It touches nothing outside the seven 'Medra Org —' pages.\n"
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
 f"  const OWN = {json.dumps([n for pair in NAMES.values() for n in pair] + MOBILE_EXTRA)};\n"
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
 "    for (const dn of ord.d){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const mn of ord.m){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(!s) continue;\n"
 "    const pts=[]; if(F(s[0])) pts.push({ nodeId:F(s[0]).id, name:pg.name+' · Desktop' });\n"
 "    if(F(s[1])) pts.push({ nodeId:F(s[1]).id, name:pg.name+' · Mobile' });\n"
 "    if(pts.length) pg.flowStartingPoints=pts; }\n"
 "  return { linked, navLinked, stayOnScreen: stay, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT, "link-org.js"), "w").write(linker)

ps = ["# Medra Organisation module — render + wire (Figma Desktop open + connected).",
      "# Organisation-module only: it creates and fills the seven 'Medra Org —' pages and nothing else.",
      "",
      "# 1. prime the offline icon cache (safe to re-run)",
      'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
      'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
      "",
      "# 2. tokens — the same 41 tokens as every other Medra bundle, so this is a no-op",
      "figma-cli tokens import-design-md .\\DESIGN.md",
      ""]
for p_, fids in ORDER.items():
    pg = PAGE_FIGMA.get(p_, "Medra Org — 8 Components").replace("&amp;", "&")
    ps.append(f'# ---- {pg} ----')
    ps.append(f'figma-cli eval "(async()=>{{const t=\'{pg}\';let p=figma.root.children.find(n=>n.name===t);if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"')
    lst = ", ".join("'" + f + "'" for f in manifest[p_])
    ps.append(f'foreach ($f in @({lst})) {{ figma-cli render (Get-Content $f -Raw) }}')
    ps.append("")
ps.append("# 3. wire the prototype, close the navigation, arrange the canvas")
ps.append("figma-cli run .\\link-org.js")
open(os.path.join(OUT, "render-org.ps1"), "w").write("\n".join(ps))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} screen links "
      f"· {len(nav_jobs)} nav links · {len(CMP)} component states")
for p_, fs in manifest.items(): print(f"  {p_}: {len(fs)}")
