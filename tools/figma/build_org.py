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
from normalise import normalise
from fixups import fix_script
from org_kit import *
from shell import ONE_PAGE, BAND_Y0, one_page_ps1, LAYOUT_JS

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
  "Clinic":   "Medra Org — 7 The Doctor Inside It",
  "States":   "Medra Org — 8 States &amp; Edge Cases",
  "Components": "Medra Org — 9 Components",
}
NAV = {"Today": 0, "Bookings": 1, "People": 2, "Departments": 3,
       "Referrals": 4, "Access": 5, "Reports": 6, "Settings": 7}
BADGES = {"Today": 7, "Bookings": 4, "Referrals": 3}

# The mobile tab bar is role-aware: an admin, a nurse and a front desk do not want the same
# five destinations. Three bars, one shell.
TAB_ADMIN = [("layout-dashboard", "Today", "Nav Today"), ("calendar-check", "Bookings", "Nav Bookings"),
             ("users", "People", "Nav People"), ("share-2", "Referrals", "Nav Referrals"),
             ("ellipsis", "More", "Nav More")]
# TAB_STAFF and TAB_DESK are gone. A phone tab bar is now generated from the persona's own
# rail by `o_tabs_for()` — first four destinations plus More — so a nurse's phone and a nurse's
# desktop offer the same places. Two hand-written bars covering eight personas was the mobile
# half of the same mistake the shared rail was making.

ADMIN = ("Mrs. Adaeze Nwosu", "Organisation admin")
NURSE = ("Sister Ifeoma Uche", "Nurse · Nursing")
LAB   = ("Mr. Sola Adeniyi", "Lab technician · Laboratory")
PHARM = ("Mr. Bayo Ogun", "Pharmacist · Pharmacy")
DESK  = ("Miss Ngozi Peter", "Front desk")
ORGDOC = ("Dr. Chuka Eze", "General practice · Garki")

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
], footer="Checked by a person. An RC number proves a company exists; the practice licence is the clinical credential.")

A2_DOCS = dgroup("Documents", [
    drow("file-badge", "CAC certificate", value="Accepted", sub="RC 1489302 · uploaded 4 Feb", name="Doc cac", tone="ok"),
    drow("badge-check", "Organisation practice licence", value="Under review", sub="Uploaded 4 Feb · expires 31 Dec 2026", name="Doc licence", tone="warn"),
    drow("id-card", "Contact person ID", value="Accepted", sub="NIN · Mrs. Adaeze Nwosu", name="Doc nin", tone="ok"),
    drow("upload", "Add another document", sub="Anything that helps us confirm the organisation", name="Doc add", chevron=False),
], footer="A laboratory or pharmacy also holds its own regulator's registration. Upload it here.")

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
], footer="Support and front-desk seats cost less than a practitioner seat. They are what makes the record complete.")

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
            + dept_card("imaging", 2, 3, 6, "Dept imaging", "Studies booked today")
            + '</Frame>'
            + f'<Frame w="fill" flex="row" gap={{12}} items="start">'
            + dept_card("billing", 2, 2, 9, "Dept billing", "Bills and claims open")
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

# Godwin: the admin is "the one in charge of onboarding other department or staff". That was
# true of the module already — C3 adds a department, C5 invites a person — but it was two rows
# deep in People, which is not where you look when somebody starts on Monday. It belongs on the
# admin's own first screen, and on nobody else's.
B1_ONBOARD = dgroup("Onboarding", [
    drow("user-plus", "Invite someone into a department", sub="They prove their own identity and registration; you never hold a password", name="Open invite C5"),
    drow("building-2", "Add a department", sub="Physiotherapy, records, anything with its own queue and its own seats", name="Add dept C3"),
    drow("badge-alert", "2 invited, never joined", value="7 days", sub="Laboratory has nobody in it. Resend or withdraw.", name="Open people C4", tone="warn"),
    drow("lock", "Front desk has no spare seat", value="5 of 5", sub="The busiest department in the building, and it cannot take anyone", name="Open plan A4", tone="err"),
], footer="Only you can do any of this. A department lead can ask for a seat; nobody but an administrator can create one.")

B1_ASIDE = (rail_section("Onboarding", B1_ONBOARD, None)
            + rail_section("Across the branches",
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
      ("onboard", "user-plus", "Onboarding", "Invite someone, add a department", "4", "warn", B1_ONBOARD, None),
      ("depts", "layers", "Departments", "All seven, and what each is carrying", "7", None, B1_DEPTS, None),
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
], footer="A booking with nobody assigned becomes a complaint if it is left. Sorted by how soon they start.")

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
           + '</Frame><Frame w="fill" flex="row" gap={12} items="start">'
           + dept_card("lab", 3, 4, 7, "Dept lab", "Tests ordered and returned")
           + dept_card("pharmacy", 2, 3, 4, "Dept pharmacy", "Dispensing against prescriptions")
           + '</Frame><Frame w="fill" flex="row" gap={12} items="start">'
           + dept_card("desk", 5, 5, 12, "Dept desk", "Registration, check-in, payment")
           + dept_card("imaging", 2, 3, 6, "Dept imaging", "X-ray, ultrasound, CT, MRI, ECG")
           + '</Frame><Frame w="fill" flex="row" gap={12} items="start">'
           + dept_card("billing", 2, 2, 9, "Dept billing", "Payments, receipts, insurance claims")
           + f'<Frame grow={{1}} flex="col" gap={{12}} p={{16}} rounded={{16}} bg="var:bg/base" '
           + f'stroke="var:border/subtle" strokeWidth={{1}}>{dept_badge("clinic")}'
           + f'<Frame w="fill" flex="col" gap={{3}}>{T(14,"semibold","var:text/strong","Add a department")}'
           + T(11, "regular", "var:text/muted", "Imaging, physiotherapy, medical records", w="fill")
           + f'</Frame>{dbtn("Add a department","Add dept C3","plus","ghost",full=True,size="sm")}</Frame></Frame>')

C1_WHY = dgroup("Why departments and not people", [
    drow("layers", "You buy seats, not licences for names", sub="When a technician leaves, the seat stays and you reassign it", name="Why seats", chevron=False),
    drow("shield-check", "Permissions follow the department", sub="Nobody carries access from a job they no longer do", name="Why perms", chevron=False),
    drow("inbox", "Work is routed to a department, never a person", sub="An order sits in the laboratory queue, so nothing waits on one individual being at work", name="Why route", chevron=False),
], footer="It is why the price follows practitioners, branches and seats.")

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

# The other half of Godwin's split on 14 August: a private doctor sets their own consultation
# length, and an organisation sets it for the doctors working in it. A hospital trading volume
# against depth is a management decision, so it belongs to the department, not to each doctor.
C2_LENGTH = dgroup("How long is one consultation here?", [
    field_chips("Standard length", ["10 min", "15 min", "20 min", "30 min"], 2, "Dept slot length"),
    drow("calendar-days", "What a member sees", value="10:20 · 10:40 · 11:00",
         sub="Your length repeated. It overrides what an individual doctor set for their own rooms",
         name="Dept slot preview", chevron=False, tone="ok"),
    drow("user-cog", "A consultant may set their own", sub="Two doctors here are allowed to — it is off for everyone else",
         name="Dept slot override", tone="warn"),
], footer="Shorter slots mean more patients and less time each. Whoever runs the department decides, and it is recorded.")

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
        f'<Frame grow={{1}} flex="col" gap={{14}}>{C2_PEOPLE}{C2_LENGTH}{C2_PERMS}</Frame>'
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
      ("length", "clock", "How long is one consultation here?", "20 minutes — the department decides", "20 min", None, C2_LENGTH, None),
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
], footer="They inherit the department's permissions. Per-person editing is how organisations end up with access nobody remembers granting.")

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
               "Giving the busiest, highest-turnover seat in the building a window into diagnoses is the fastest way to breach the NDPA.")
    + perm_row("A lab technician releasing a result to a member", False,
               "They enter it, a doctor releases it. An out-of-range value with nobody to explain it is a harm.")
    + T(11, "regular", "var:text/muted",
        "These are platform rules rather than settings. Every other permission on this screen is yours to tighten.", w="fill"),
    bg="var:state/error-bg", stroke=None)

C7_EPISODE = dgroup("How access ends", [
    prep_step(1, "A member arrives", "Their record opens to the people on that episode of care, and only to what they shared"),
    prep_step(2, "The visit is marked complete", "Access closes the same moment, for everyone"),
    prep_step(3, "The member can see it happened", "Every read is in their own audit trail, by name and by time"),
], footer="Per episode of care, never per person and never permanent. It is what makes a shared record safe.")

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
        "My queue", dept="Nursing", urgent=1, aside=D1_ASIDE, who=NURSE, badges=BADGES),
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
    tab_items=o_tabs_for("nurse"), tab=0)

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
        "Record vitals", dept="Nursing", who=NURSE, badges=BADGES),
    o_head("Vitals", "Amara Okeke · before 10:30", stats=[("136/86", "BP"), ("78", "Pulse"), ("74kg", "Weight")]),
    pinned=f'{D2_WHO}{D2_FORM}',
    sections=[
      ("history", "trending-up", "Against her own history", "BP improving since last visit", None, "ok", D2_RANGE, None),
      ("self", "circle-help", "What she told us herself", "Blood group and genotype are unverified", "3", "warn", D2_VERIFY, None),
    ],
    foot=dcta("Save and hand to the doctor", "Save vitals D2", "check"),
    tab_items=o_tabs_for("nurse"), tab=1)

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
        "My queue", dept="Nursing", who=NURSE, badges=BADGES),
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
    tab_items=o_tabs_for("nurse"), tab=0)

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
], footer="No answer in two minutes and it goes to the duty doctor. An escalation never sits in one person's queue.")

addx("Chain", "D4-escalate",
    o_desk("Org · Nursing — D4 Escalate", ("Nursing", "Grace Okeke", "Escalate"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","My queue")}</Frame>'
        f'{dhead([("Get a doctor",False),("to look",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D4_PICK}{D4_FORM}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D4_WHO}'
        f'{dcta("Escalate now","Send escalate D4","triangle-alert")}</Frame></Frame>',
        "My queue", dept="Nursing", urgent=1, who=NURSE, badges=BADGES),
    o_head("Escalate", "Grace Okeke · BP 178/104", stats=[("Now", "Urgency"), ("2 min", "Fallback"), ("2", "Doctors")]),
    pinned=D4_PICK,
    sections=[
      ("detail", "message-square-text", "What you found", "And how urgent it is", None, None, D4_FORM, None),
      ("who", "stethoscope", "Who this goes to", "Her doctor, then the duty doctor", "2", None, D4_WHO, None),
    ],
    foot=dcta("Escalate now", "Send escalate D4", "triangle-alert"),
    tab_items=o_tabs_for("nurse"), tab=0)

# ---------------- D5–D8 LABORATORY
D5_CRIT = alert_strip("siren", "1 critical value waiting on a phone call",
    "Musa Ibrahim · potassium 7.2 · verified 09:41. Nobody has confirmed they heard it.",
    "err", dbtn("Open it", "Crit waiting", "arrow-right", "danger", grow=False, size="sm"))

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
], footer="The order and its clinical detail, nothing else. A test is run the same way whatever the diagnosis.")

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
        f'{D5_CRIT}{D5_QUEUE}{D5_PROGRESS}',
        "Order queue", dept="Laboratory", urgent=1, aside=D5_ASIDE, who=LAB, badges=BADGES),
    o_head("Order queue", "4 waiting · 1 urgent", back=False, ctx="Laboratory · Garki",
           stats=[("4", "Waiting"), ("3", "Running"), ("11", "Done")]),
    pinned=f'{D5_CRIT}{D5_QUEUE}',
    sections=[
      ("progress", "beaker", "In progress", "Three samples running", "3", None, D5_PROGRESS, None),
      ("today", "chart-column", "Today", "14 accepted · 2h 40m median", None, None,
       dcard(kpi_line("Accepted", "14") + kpi_line("Results entered", "11")
             + kpi_line("Median turnaround", "2h 40m") + kpi_line("Samples rejected", "1", "warn"), p=14, gap=3), None),
    ],
    tab_items=o_tabs_for("lab"), tab=0)

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
        "Order queue", dept="Laboratory", who=LAB, badges=BADGES),
    o_head("Order", "Amara Okeke · 2 tests", stats=[("2", "Tests"), ("41m", "Waiting"), ("₦8,500", "She pays")]),
    pinned=D6_ORDER,
    sections=[
      ("prev", "history", "Her previous results", "From 12 March, at this laboratory", "2", None, D6_PREV, None),
      ("scope", "shield-check", "What you can and cannot see", "The order, not the record", "4", None, D6_WHAT, None),
    ],
    foot=f'{dcta("Accept and start","Open result D7","arrow-right")}'
         f'{dbtn("Sample problem","Open lab D8","triangle-alert","danger",full=True)}',
    tab_items=o_tabs_for("lab"), tab=0)

# ---------------- D7 structured result entry
def result_line(analyte, unit, ref, value="", flag=None, mobile=False):
    """One analyte. Desktop puts the name, the box, the unit, the range and the flag on a single
    line — 178 + 104 + 76 of it fixed — which is wider than a phone. On mobile the same five
    facts stack into two rows rather than being cut off, because a reference range the technician
    cannot see is the one thing on this screen that makes a number meaningless."""
    tone = {"high": ("var:state/warning-bg", "var:state/warning", "High"),
            "low": ("var:state/warning-bg", "var:state/warning", "Low"),
            None: ("var:state/success-bg", "var:state/success", "Normal")}[flag]
    tag = (f'<Frame flex="row" px={{9}} py={{4}} rounded={{7}} bg="{tone[0]}">'
           f'{T(10,"semibold",tone[1],tone[2])}</Frame>') if value else ''
    box = (f'<Frame w={{104}} flex="row" px={{12}} py={{9}} rounded={{10}} bg="var:bg/base" '
           f'stroke="{"var:border/accent" if value else "var:border/default"}" strokeWidth={{1}}>'
           f'{T(13,"semibold" if value else "regular","var:text/strong" if value else "var:text/faint",value or "—")}</Frame>')
    if mobile:
        return (f'<Frame name="Btn Res {analyte}" w="fill" flex="col" gap={{8}} py={{10}}>'
                f'<Frame w="fill" flex="row" gap={{10}} items="center">'
                f'{T(13,"medium","var:text/strong",analyte,w="fill")}{tag}</Frame>'
                f'<Frame w="fill" flex="row" gap={{10}} items="center">{box}'
                f'<Frame grow={{1}} flex="col" gap={{1}}>{T(12,"regular","var:text/muted",unit)}'
                f'{T(11,"regular","var:text/faint","Normal " + ref if ref != "—" else "No range")}</Frame></Frame></Frame>')
    return (f'<Frame name="Btn Res {analyte}" w="fill" flex="row" gap={{12}} items="center" py={{10}}>'
            f'{T(13,"medium","var:text/strong",analyte,w=178)}{box}'
            f'{T(12,"regular","var:text/muted",unit,w=76)}'
            f'{T(11,"regular","var:text/faint",ref,w="fill")}{tag}</Frame>')


def result_template(mobile=False):
    return dcard(
        eyerow("Fasting blood sugar", f'<Frame name="Btn Change template" flex="row">{T(11,"semibold","var:text/accent","Change template")}</Frame>')
        + result_line("Fasting plasma glucose", "mmol/L", "3.9 – 5.5", "6.4", "high", mobile)
        + hr() + eyerow("HbA1c")
        + result_line("HbA1c", "%", "< 5.7", "6.8", "high", mobile)
        + result_line("Estimated average glucose", "mmol/L", "—", "8.5", None, mobile)
        + hr()
        + field("Comment for the doctor (optional)", "message-square-text",
                "Sample taken fasting at 07:40. Slight lipaemia, does not affect these assays.")
        + upload("Attach report D7", label="Attach the analyser printout"))

# The laboratory's own flag. A technician decides a value is on the critical list, and the
# screen then refuses to let it be "sent" like an ordinary result.
D7_CRIT = alert_strip("siren", "Potassium 7.2 is on the critical list",
    "This cannot go to a queue. It has to reach Dr. Okafor by voice, with a read-back.",
    "err", dbtn("Open the critical path", "Crit flag", "arrow-right", "danger", grow=False, size="sm"))

D7_TEMPLATE = result_template()
D7_TEMPLATE_M = result_template(mobile=True)

D7_WHY = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("info",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Why a form and not a paragraph")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Prose cannot be trended, flagged against a range or compared with another laboratory. You fill numbers; the comment box carries the rest.", w="fill"),
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
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D7_CRIT}{D7_TEMPLATE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D7_WHY}{D7_NEXT}'
        f'{dcta("Send to the doctor","Save result D7","send")}</Frame></Frame>',
        "Enter result", dept="Laboratory", who=LAB, badges=BADGES),
    o_head("Enter result", "Amara Okeke · 2 tests", stats=[("2", "Tests"), ("2", "Out of range"), ("Dr. Okafor", "Goes to")]),
    pinned=f'{D7_CRIT}{D7_TEMPLATE_M}',
    sections=[
      ("why", "info", "Why a form and not a paragraph", "So it can be trended and compared", None, None, D7_WHY, None),
      ("next", "list-checks", "What happens when you finish", "It goes to the doctor, not the member", "3", None, D7_NEXT, None),
    ],
    foot=dcta("Send to the doctor", "Save result D7", "send"),
    tab_items=o_tabs_for("lab"), tab=1)

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
        "In a paper laboratory a bad sample is quietly discarded and the member finds out a week later. Rejecting here always tells someone.", w="fill"),
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
        "Sample problems", dept="Laboratory", who=LAB, badges=BADGES),
    o_head("Sample problem", "Blessing Ade · FBC", stats=[("Haemolysed", "Reason"), ("2", "To tell"), ("Free", "Repeat")]),
    pinned=D8_PICK,
    sections=[
      ("what", "message-square-text", "What should happen now", "Who is told, and who pays", None, None, D8_WHAT, None),
      ("rule", "shield-check", "Why this screen exists", "A rejected sample is never silent", None, "ok", D8_RULE, None),
    ],
    foot=f'{dcta("Reject and tell them","Save problem D8","send")}'
         f'{dbtn("Never mind","Open lab D5","x","ghost",full=True)}',
    tab_items=o_tabs_for("lab"), tab=0)

# ---------------- D15 a value that cannot wait in a queue
# A potassium of 7.2 kills people while a result sits in an inbox. Every laboratory in the world
# runs a critical list: values that must reach a named human by voice, be read back, and be
# recorded — not released into a queue and hoped for. Medra had no path for this at all, which
# made it the one genuine safety defect in the file rather than a missing feature.
D15_VALUE = dcard(
    f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{15}} rounded={{14}} bg="var:state/error-bg">'
    f'{I("siren",22,ERR_IC)}'
    f'<Frame grow={{1}} flex="col" gap={{2}}>{T(16,"bold","var:state/error","Critical value")}'
    f'{T(12,"regular","var:text/default","This is on the critical list. It does not go in a queue.",w="fill")}</Frame>'
    f'{T(13,"semibold","var:state/error","09:41")}</Frame>'
    + lab_line("Potassium", "7.2 mmol/L", "3.5 – 5.1", "High")
    + lab_line("Sodium", "138 mmol/L", "135 – 145")
    + lab_line("Creatinine", "212 µmol/L", "62 – 106", "High")
    + T(11, "regular", "var:text/muted",
        "Critical limit for potassium is 6.5. Repeated on a second aliquot at 09:38 — 7.1. Not haemolysed.", w="fill"))

D15_WHO = dgroup("Who has to be told, by voice", [
    request_row("stethoscope", "Dr. Ngozi Okafor", "Ordered it · on duty until 17:00 · +234 801 234 5678",
                "now", "Crit call okafor", "err",
                [dbtn("Call now", "Crit call", "phone-call", "danger", size="sm"),
                 dbtn("She is not answering", "Crit noanswer", "phone-off", "ghost", size="sm")]),
    request_row("user-round-check", "Dr. Chuka Eze", "Medical officer on call · if the requester cannot be reached",
                "backup", "Crit call eze", "warn",
                [dbtn("Call instead", "Crit call", "phone-call", "ghost", size="sm")]),
    drow("shield-alert", "Then it escalates on its own", sub="Unacknowledged after 15 minutes it goes to the medical director and onto the governance board", name="Crit escalate", tone="err", chevron=False),
], footer="You cannot mark this done by sending it. A critical value is closed by a person confirming they heard it.")

D15_READBACK = dgroup("Record the call", [
    field("Who did you speak to?", "user", "Dr. Ngozi Okafor", ph=False,
          helper="A name, not a department. This is the line an audit reads."),
    field("They read the value back as", "repeat", "Potassium seven point two", ph=False,
          helper="Read-back is what catches a number heard wrong down a bad line."),
    field("Time of the call", "clock", "09:44", ph=False),
    checkbox("They confirmed they will act on it now", "Crit confirmed"),
], footer="Everything here goes into the member's record and the organisation's audit log, and neither can be edited afterwards.")

D15_NOT = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("eye-off",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","The member is not told yet")}</Frame>'
    + T(12, "regular", "var:text/default",
        "She sees that a result has arrived, never the number. A potassium of 7.2 read on a phone with nobody to explain it sends a frightened person to the wrong place.", w="fill"),
    bg="var:state/info-bg", stroke=None)

addx("Chain", "D15-critical",
    o_desk("Org · Laboratory — D15 Critical Value", ("Laboratory", "Musa Ibrahim", "Critical"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Result")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D15_VALUE}{D15_WHO}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D15_READBACK}{D15_NOT}'
        f'{dcta("Record the call and close it","Close critical D15","check")}</Frame></Frame>',
        "Critical", dept="Laboratory", who=LAB, badges=BADGES, urgent=1),
    o_head("Critical value", "Musa Ibrahim · potassium 7.2",
           stats=[("7.2", "Potassium"), ("6.5", "Critical at"), ("3 min", "Since verified")]),
    pinned=D15_VALUE,
    sections=[
      ("who", "phone-call", "Who has to be told, by voice", "Dr. Okafor, then the on-call, then it escalates", "2", "err", D15_WHO, None),
      ("readback", "repeat", "Record the call", "Name, read-back, time — this is the audit line", None, None, D15_READBACK, None),
      ("not", "eye-off", "The member is not told yet", "She sees a result arrived, never the number", None, None, D15_NOT, None),
    ],
    foot=dcta("Record the call and close it", "Close critical D15", "check"),
    tab_items=o_tabs_for("lab"), tab=2)

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
], footer="Somebody at the counter comes first. Sorted by who is waiting, not by when it was signed.")

D9_STOCK = dgroup("Watch the shelf", [
    drow("package", "Metformin 500 mg", value="18 left", sub="Three prescriptions today need 60", name="Stock metformin", tone="warn"),
    drow("package", "Amlodipine 5 mg", value="240 left", sub="Comfortable", name="Stock amlodipine", tone="ok"),
    drow("package-x", "Salbutamol inhaler", value="Out", sub="Two waiting — substitution needed", name="Open sub D11", tone="err"),
], footer="A count you keep here, not a warehouse system — so you can tell a member before they queue.")

addx("Chain", "D9-pharmacy",
    o_desk("Org · Pharmacy — D9 Prescription Queue", ("Pharmacy", "Thursday 14 August"),
        f'{dhead([("Four prescriptions",False),("waiting",True)],26)}'
        f'{rows_of([stat_tile("inbox","4","Waiting","1 at the counter","teal","Stat pwaiting"),stat_tile("check-check","23","Dispensed today","All recorded","ok","Stat pdone"),stat_tile("package-x","1","Out of stock","Salbutamol inhaler","err","Stat pstock"),stat_tile("repeat","3","Substitutions","This week","warn","Stat psub")],4,14)}'
        f'{D9_QUEUE}',
        "Prescriptions", dept="Pharmacy", urgent=1,
        aside=rail_section("Watch the shelf", D9_STOCK, None), who=PHARM, badges=BADGES),
    o_head("Prescriptions", "4 waiting · 1 at the counter", back=False, ctx="Pharmacy · Garki",
           stats=[("4", "Waiting"), ("23", "Done"), ("1", "Out of stock")]),
    pinned=D9_QUEUE,
    sections=[("stock", "package", "Watch the shelf", "One out of stock, one low", "3", "warn", D9_STOCK, None)],
    tab_items=o_tabs_for("pharm"), tab=0)

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
], footer="Written by the prescriber. Disagree with any of it and flag it back rather than change it here.")

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
        "Prescriptions", dept="Pharmacy", who=PHARM, badges=BADGES),
    o_head("Dispense", "Amara Okeke · amlodipine", stats=[("30", "Tablets"), ("30d", "Supply"), ("1", "Repeat")]),
    pinned=f'{D10_RX}{D10_FORM}',
    sections=[("counsel", "message-circle", "Say this at the counter", "Written by the prescriber", "3", None, D10_COUNSEL, None)],
    foot=f'{dcta("Record as dispensed","Save dispense D10","check")}'
         f'{dbtn("Cannot dispense this","Open sub D11","triangle-alert","warn",full=True)}',
    tab_items=o_tabs_for("pharm"), tab=0)

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
        "Substitutions", dept="Pharmacy", urgent=1, who=PHARM, badges=BADGES),
    o_head("Cannot dispense", "Fatima Bello · out of stock", stats=[("2", "Alternatives"), ("Here", "She is"), ("Dr. Okafor", "Goes to")]),
    pinned=D11_PICK,
    sections=[
      ("options", "repeat", "What we could give instead", "Two alternatives in stock", "2", None, D11_OPTIONS, None),
      ("msg", "message-circle", "What the doctor will see", "And anything you add", None, None, D11_MSG, None),
    ],
    foot=dcta("Send to the prescriber", "Send sub D11", "send"),
    tab_items=o_tabs_for("pharm"), tab=2)

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
        "The day", dept="Front desk", urgent=2, who=DESK, badges=BADGES),
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
    tab_items=o_tabs_for("desk"), tab=0)

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
        "Walk-in", dept="Front desk", who=DESK, badges=BADGES),
    o_head("Walk-in", "Register someone at the desk", stats=[("New", "Member"), ("1 min", "Takes"), ("SMS", "Their ID")]),
    pinned=f'{D13_FIND}{D13_FORM}',
    sections=[("consent", "shield-check", "What they are agreeing to", "Read it aloud, then tick", None, "info", D13_CONSENT, None)],
    foot=dcta("Register and add to the queue", "Save walkin D13", "check"),
    tab_items=o_tabs_for("desk"), tab=2)

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
        "Payments", dept="Front desk", urgent=2, who=DESK, badges=BADGES),
    o_head("Check in", "Blessing Ade · not paid", stats=[("₦15,000", "To collect"), ("10:30", "Booked"), ("NHIS", "Insurance")]),
    pinned=f'{D14_WHO}{D14_PAY}',
    sections=[
      ("ins", "shield-check", "Insurance on her profile", "NHIS accepted here", "2", None, D14_INS, None),
      ("next", "arrow-right", "Then what?", "Waiting room, nursing or laboratory", "3", None, D14_NEXT, None),
    ],
    foot=dcta("Check in", "Save checkin D14", "check"),
    tab_items=o_tabs_for("desk"), tab=0)

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

# =====================================================================================
# D16–D18  IMAGING / RADIOLOGY
# Godwin asked for instrumental diagnostics in the third review — ECG, echo, CT, MRI,
# gastroscopy — and they do not behave like blood. A specimen leaves the patient; an image
# does not, so the patient has to be *present, prepared and safe* before anything happens,
# and the result is a radiologist's sentence rather than a number against a range. That is
# three screens the laboratory chain cannot carry: a worklist, a safety stop, and a report.
# =====================================================================================
IMAGING = ("Mr. Tunde Adebayo", "Radiographer · Imaging")
RADIOL  = ("Dr. Ifeanyi Nwachukwu", "Radiologist · Imaging")

D16_WORK = dgroup("Studies requested · 6", [
    task_row_big("09:30", "Halima Sani · MDR-9012-44", "Dr. Okafor · routine · she is in the waiting room",
                 "MRI lumbar spine · 45 min · no contrast", "Img halima", action="Prepare", avatar="avatar-5.jpg",
                 flags=[("user-check", "Here now"), ("magnet", "Metal check not done")], tone="warn"),
    task_row_big("09:50", "Musa Ibrahim · MDR-7714-02", "Dr. Eze · urgent · chest pain",
                 "Chest X-ray · 5 min", "Img musa", action="Prepare", avatar="avatar-1.jpg",
                 flags=[("triangle-alert", "Urgent")], tone="err"),
    task_row_big("10:15", "Amara Okeke · MDR-8842-19", "Dr. Okafor · routine",
                 "ECG · 10 min · resting twelve-lead", "Img amara", action="Prepare",
                 flags=[("activity", "No prep needed")], tone="ok"),
    task_row_big("11:00", "Grace Okeke · MDR-8842-21", "Dr. Okafor · routine · fasting since midnight",
                 "Abdominal ultrasound · 20 min", "Img grace", action="Prepare", avatar="avatar-3.jpg",
                 flags=[("utensils-crossed", "Fasting confirmed")], tone="ok"),
    task_row_big("11:45", "Fatima Bello · MDR-2201-13", "Dr. Eze · routine · contrast",
                 "CT abdomen with contrast · 30 min", "Img fatima", action="Prepare", avatar="avatar-4.jpg",
                 flags=[("droplet", "Creatinine needed"), ("radiation", "Dose recorded")], tone="warn"),
], footer="Ordered by appointment, not by request. An image needs the person, the room and the machine at once.")

D16_ROOMS = dgroup("Rooms and machines", [
    drow("scan", "MRI suite", value="In use", sub="Until 09:25 · Halima is next", name="Room mri", tone="warn"),
    drow("scan-line", "CT", value="Free", sub="Next booked 11:45", name="Room ct", tone="ok"),
    drow("radiation", "X-ray room 1", value="Free", sub="Musa can go now", name="Room xr", tone="ok"),
    drow("monitor", "Ultrasound", value="Free", sub="Sonographer in at 10:30", name="Room us", tone="ok"),
    drow("activity", "ECG trolley", value="Ward 2", sub="Bring it back before 10:15", name="Room ecg"),
], footer="A free machine, a free room and somebody to run it are three different facts. All three have to be true.")

D16_UNREAD = dgroup("Waiting for a radiologist", [
    drow("file-image", "3 studies acquired, not yet reported", sub="Oldest 2 hours · Dr. Nwachukwu is in until 16:00", name="Open report D18", tone="warn"),
    drow("siren", "1 urgent, unread", sub="Musa Ibrahim's chest film · the doctor is waiting", name="Open report D18", tone="err"),
], footer="An image nobody has read is not a result. Until a radiologist has written a sentence, the doctor has a picture and a guess.")

addx("Chain", "D16-imaging",
    o_desk("Org · Imaging — D16 Worklist", ("Imaging", "Thursday 14 August"),
        f'{dhead([("Six studies",False),("today",True)],26)}'
        f'{rows_of([stat_tile("scan","6","Booked today","2 in the next hour","teal","Stat imgbook"),stat_tile("check-check","9","Acquired","3 not yet reported","ok","Stat imgdone"),stat_tile("file-image","3","Waiting on a report","1 urgent","err","Open report D18"),stat_tile("user-x","1","Did not attend","Grace, 12 Aug","warn","Stat imgdna")],4,14)}'
        f'{D16_WORK}',
        "Worklist", dept="Imaging", urgent=1,
        aside=rail_section("Rooms and machines", D16_ROOMS, None) + rail_section("Waiting for a radiologist", D16_UNREAD, None),
        who=IMAGING, badges=BADGES, persona="imaging"),
    o_head("Imaging", "6 booked · 2 in the next hour", back=False, ctx="Imaging · Garki",
           stats=[("6", "Booked"), ("9", "Acquired"), ("3", "Unread")]),
    pinned=D16_WORK,
    sections=[
      ("rooms", "scan", "Rooms and machines", "One in use, three free", "5", None, D16_ROOMS, None),
      ("unread", "file-image", "Waiting for a radiologist", "3 studies, 1 urgent", "2", "err", D16_UNREAD, None),
    ],
    tab_items=o_tabs_for("imaging"), tab=0)

# ---------------- D17 the safety stop
D17_ORDER = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","REQUESTED BY DR. NGOZI OKAFOR · 08:41")}{status_pill("pending","Not started")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(20,"bold","var:text/strong","MRI lumbar spine")}'
    + T(13, "regular", "var:text/muted", "Halima Sani · 29 · no contrast · about 45 minutes in the scanner", w="fill") + '</Frame>'
    + hr()
    + note_section("Why the doctor asked for it",
                   "Six weeks of lower back pain with numbness down the right leg. Not settling with rest. Looking for a disc pressing on the nerve root.",
                   "file-text")
    + note("info", "A question, not just a body part. A radiologist who knows what is being asked writes a better report."))

D17_SAFETY = dgroup("Before she goes anywhere near the magnet", [
    checklist_row(True,  "Identity checked out loud", "She said her own name and date of birth — you did not read it to her", "Sf id"),
    checklist_row(False, "Any metal in or on her body?", "Pacemaker, clips, plates, coil, shrapnel, piercings, hearing aid. Every one is a stop.", "Sf metal"),
    checklist_row(False, "Could she be pregnant?", "Ask everyone who could be. It is a question, not an accusation.", "Sf preg"),
    checklist_row(True,  "She understands what will happen", "Loud, narrow, 45 minutes, she can talk to you the whole time", "Sf explain"),
    checklist_row(True,  "Claustrophobia asked about", "She says she will be fine with the intercom on", "Sf claus"),
], footer="Two are unanswered, so the study cannot start. A metal implant in an MRI scanner injures somebody in seconds.")

D17_STOP = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("octagon-alert",17,ERR_IC)}'
    f'{T(14,"semibold","var:text/strong","Two answers missing")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Ask her, record what she says, and the button turns on. If she is unsure about metal, ask the radiologist.", w="fill")
    + dbtn("Ask the radiologist first", "Open messages G3", "message-square-text", "ghost", full=True),
    bg="var:state/error-bg", stroke=None)

D17_DOSE = dgroup("What gets recorded", [
    drow("radiation", "No ionising radiation", sub="MRI is a magnet. Nothing to record here — on a CT or an X-ray this line carries the dose", name="Dose none", chevron=False, tone="ok"),
    drow("user-round", "Who ran the study", sub="You, by name, with the time it started and finished", name="Dose who", chevron=False),
    drow("scan", "Machine and sequence", sub="MRI suite · lumbar spine protocol", name="Dose machine", chevron=False),
], footer="All of it is logged whether the study is normal or not.")

addx("Chain", "D17-prepare",
    o_desk("Org · Imaging — D17 Safety Check", ("Imaging", "Halima Sani", "Safety"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Worklist")}</Frame>'
        f'{D17_ORDER}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D17_SAFETY}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D17_STOP}{D17_DOSE}'
        f'{dbtn("Start the study","Start study D17","play","ghost",full=True)}</Frame></Frame>',
        "Worklist", dept="Imaging", who=IMAGING, badges=BADGES, persona="imaging"),
    o_head("Safety check", "Halima Sani · MRI lumbar spine",
           stats=[("3/5", "Answered"), ("45 min", "In the scanner"), ("0", "Radiation")]),
    pinned=f'{D17_ORDER}{D17_STOP}',
    sections=[
      ("safety", "shield-alert", "Before she goes near the magnet", "Five questions, two unanswered", "5", "err", D17_SAFETY, None),
      ("dose", "clipboard-list", "What gets recorded", "Every study, not only the abnormal ones", "3", None, D17_DOSE, None),
    ],
    foot=dbtn("Start the study", "Start study D17", "play", "ghost", full=True),
    tab_items=o_tabs_for("imaging"), tab=0)

# ---------------- D18 the radiologist's report
D18_STUDY = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","ACQUIRED BY TUNDE ADEBAYO · 09:58")}{status_pill("pending","Not reported")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(20,"bold","var:text/strong","Chest X-ray · Musa Ibrahim")}'
    + T(13, "regular", "var:text/muted", "51 · PA and lateral · urgent · Dr. Eze is waiting in clinic", w="fill") + '</Frame>'
    + f'<Frame w="fill" flex="row" gap={{10}}>'
    + f'<Frame grow={{1}} h={{150}} rounded={{13}} bg="var:neutral/900" flex="col" justify="center" items="center" gap={{7}}>'
    + I("file-image", 26, "#8A94A0") + T(11, "regular", "#8A94A0", "PA view") + '</Frame>'
    + f'<Frame grow={{1}} h={{150}} rounded={{13}} bg="var:neutral/900" flex="col" justify="center" items="center" gap={{7}}>'
    + I("file-image", 26, "#8A94A0") + T(11, "regular", "#8A94A0", "Lateral view") + '</Frame></Frame>'
    + alert_strip("triangle-alert", "The clinical question was chest pain with a potassium of 7.2",
                  "Read it against that, not as a screening film. What Dr. Eze needs to know is whether the heart is enlarged.", "warn"))

D18_REPORT = dcard(
    eyerow("Your report")
    + note_field("Findings", "file-text",
                 "Heart size at the upper limit of normal, cardiothoracic ratio 0.52. Lung fields clear. No pleural effusion. No focal consolidation. Bony thorax intact.",
                 "Rep findings", lines=4, template=True)
    + note_field("Impression", "message-square-quote",
                 "Borderline cardiomegaly. No acute cardiopulmonary abnormality to explain the chest pain.",
                 "Rep impression", lines=3, template=True)
    + field_chips("How urgently does the doctor need this?",
                  ["Routine", "Same day", "Ring them now"], 1, "Rep urgency")
    + dtoggle("siren", "This is a critical finding", sub="Turning this on takes it down the critical pathway — a voice call, a read-back and an escalation ladder", on=False, name="Rep critical"))

D18_CRIT = dgroup("What counts as critical here", [
    drow("siren", "Tension pneumothorax", sub="Ring the requesting doctor. Do not send it and hope.", name="Crit ptx", chevron=False, tone="err"),
    drow("siren", "Free air under the diaphragm", sub="Same — a phone call, then the report", name="Crit air", chevron=False, tone="err"),
    drow("siren", "A new mass", sub="Same day, by voice, whoever asked for the film", name="Crit mass", chevron=False, tone="err"),
    drow("circle-check", "Borderline cardiomegaly", sub="Not critical. It goes in the report and Dr. Eze reads it today.", name="Crit no", chevron=False, tone="ok"),
], footer="The department owns this list, not Medra. Changing it is recorded — it decides who gets rung at two in the morning.")

D18_SIGN = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",16,OK_IC)}'
    f'{T(14,"semibold","var:text/strong","Signed by you, as a named radiologist")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Dr. Ifeanyi Nwachukwu · MDCN 62109. Amending it later leaves both versions in the record.", w="fill")
    + consent_row("file-check", "I have read the images myself",
                  "Not the radiographer's note, not the previous report — the images from this study.", "Rep read", on=True),
    bg="var:state/success-bg", stroke=None)

addx("Chain", "D18-report",
    o_desk("Org · Imaging — D18 Report a Study", ("Imaging", "Musa Ibrahim", "Report"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Unreported studies")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D18_STUDY}{D18_REPORT}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D18_CRIT}{D18_SIGN}'
        f'{dcta("Sign and send to Dr. Eze","Sign report D18","pen-line")}</Frame></Frame>',
        "Reporting", dept="Imaging", who=RADIOL, badges=BADGES, persona="imaging", urgent=1),
    o_head("Report a study", "Musa Ibrahim · chest X-ray",
           stats=[("2 h", "Since acquired"), ("Urgent", "Priority"), ("2", "Views")]),
    pinned=f'{D18_STUDY}{D18_REPORT}',
    sections=[
      ("crit", "siren", "What counts as critical here", "Agreed by the department, not by us", "4", "err", D18_CRIT, None),
      ("sign", "shield-check", "Signing it", "Your name, and it stays", None, "ok", D18_SIGN, None),
    ],
    foot=dcta("Sign and send to Dr. Eze", "Sign report D18", "pen-line"),
    tab_items=o_tabs_for("imaging"), tab=1)

# =====================================================================================
# D19–D21  BILLING / CASHIER
# The front desk takes money at check-in; that is not the same job as running the money. A
# cashier reconciles a till, and a billing officer chases an HMO — and in a Nigerian clinic
# the second one is where the revenue actually leaks. A claim that was submitted, queried
# and never resubmitted is money the hospital earned and will not be paid.
# =====================================================================================
BILLING = ("Mr. Kunle Adeyemi", "Cashier · Billing")

D19_TILLS = rows_of([
    stat_tile("hand-coins", "₦412,000", "Taken today", "23 payments", "teal", "Stat taken", delta=("up", "on Wednesday")),
    stat_tile("clock", "₦186,500", "Outstanding", "9 people, oldest 11 days", "warn", "Open owing D20"),
    stat_tile("landmark", "₦1.24m", "With HMOs", "14 claims, 3 queried", "err", "Open claims D21"),
    stat_tile("scale", "₦0", "Unreconciled", "Cash counts against the system", "ok", "Stat recon"),
], 4, 14)

D19_METHOD = dgroup("How it came in today", [
    progress_row("Bank transfer", "₦214,000", 52, "teal"),
    progress_row("Cash", "₦96,000", 23, "amber"),
    progress_row("Card · Paystack terminal", "₦74,000", 18, "teal"),
    progress_row("HMO at the desk", "₦28,000", 7, "navy"),
], footer="Cash is the only line Medra cannot verify itself, so it is the one counted against a drawer.")

D19_OWED = dgroup("Money owed to us · 9", [
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "₦45,000 · consultation and labs · 11 days", "11 days", "Owe grace", tag="pending"),
    patient_row("avatar-5.jpg", "Halima Sani", "MDR-9012-44", "₦85,000 · MRI · part paid ₦20,000", "4 days", "Owe halima", tag="soon"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "₦31,500 · admitted, still on the ward", "Today", "Owe musa"),
    patient_row("avatar-4.jpg", "Fatima Bello", "MDR-2201-13", "₦25,000 · CT with contrast · HMO declined", "2 days", "Open claims D21", tag="new"),
], footer="Nobody here has been refused care. Chasing a bill and withholding treatment are different decisions.")

D19_SHIFT = dgroup("Closing the till", [
    checklist_row(True,  "Count the cash drawer", "₦96,000 counted against ₦96,000 recorded", "Till count"),
    checklist_row(True,  "Match the terminal", "Paystack settlement matches 8 card payments", "Till card"),
    checklist_row(False, "Two people sign it off", "You and a supervisor. Neither of you can do it alone.", "Till sign"),
], footer="A till one person opens, counts and signs off is not a till. Two named people, and it cannot be turned off.")

addx("Chain", "D19-billing",
    o_desk("Org · Billing — D19 The Money Today", ("Billing", "Thursday 14 August"),
        f'{dhead([("₦412,000 in,",False),("₦1.4m outstanding",True)],26)}'
        f'{D19_TILLS}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D19_OWED}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D19_METHOD}{D19_SHIFT}</Frame></Frame>',
        "The money", dept="Billing", who=BILLING, badges=BADGES, persona="billing", urgent=3),
    o_head("The money today", "₦412,000 in · ₦1.4m outstanding", back=False, ctx="Billing · Garki",
           stats=[("₦412k", "Taken"), ("₦186k", "Owed"), ("₦1.24m", "HMOs")]),
    # The four tiles are a desktop row. On a phone the header already carries the same three
    # numbers, so the pin is the list of people who owe money — the thing you act on.
    pinned=D19_OWED,
    sections=[
      ("method", "chart-column", "How it came in", "Cash is 23% of it", "4", None, D19_METHOD, None),
      ("shift", "lock", "Closing the till", "Two people, never one", "3", "err", D19_SHIFT, None),
    ],
    tab_items=o_tabs_for("billing"), tab=0)

# ---------------- D20 take a payment
D20_BILL = dcard(
    f'<Frame w="fill" flex="row" justify="between" items="center">'
    f'{T(11,"semibold","var:text/accent","HALIMA SANI · MDR-9012-44")}{status_pill("pending","Part paid")}</Frame>'
    + f'<Frame w="fill" flex="col" gap={{4}}>{T(24,"bold","var:text/strong","₦65,000 still to pay")}'
    + T(13, "regular", "var:text/muted", "Of ₦85,000 · she paid ₦20,000 on 10 August", w="fill") + '</Frame>'
    + hr()
    + kv("Consultation · Dr. Okafor", "₦15,000", "stethoscope")
    + kv("MRI lumbar spine", "₦65,000", "scan")
    + kv("Dressing and materials", "₦5,000", "bandage")
    + hr()
    + kv("Paid 10 August · transfer", "−₦20,000", "check-check")
    + f'<Frame w="fill" flex="row" justify="between" items="center" pt={{4}}>'
    + T(14, "semibold", "var:text/strong", "Balance") + T(18, "bold", "var:text/strong", "₦65,000") + '</Frame>')

D20_TAKE = dcard(
    eyerow("Take a payment")
    + field("How much is she paying now?", "banknote", "₦30,000", ph=False,
            helper="A part payment is normal. Record what she actually hands over, not what the bill says.")
    + field_chips("How?", ["Transfer", "Cash", "Card", "HMO"], 0, "Pay method")
    + field("Reference from the transfer", "hash", "PSK-2026-08-14-0091", ph=False,
            helper="Paystack fills this in by itself when the alert lands. Type it only if you are recording something that happened outside Medra.")
    + dtoggle("printer", "Print a receipt", sub="And send the same one to her phone", on=True, name="Pay print")
    + dtoggle("bell", "Remind her about the balance in 7 days", sub="One message, then it stops. Nobody is chased weekly by a machine.", on=True, name="Pay remind"))

D20_AFTER = dgroup("What this changes", [
    drow("receipt", "Her balance becomes ₦35,000", sub="Visible to her in her own app, itemised the same way", name="Pay bal", chevron=False, tone="ok"),
    drow("smartphone", "She gets a receipt on WhatsApp", sub="With the reference, so she can match it to her bank alert", name="Pay wa", chevron=False),
    drow("lock", "You cannot edit this afterwards", sub="A wrong amount is corrected by a second entry that says so, never by changing the first", name="Pay lock", chevron=False, tone="warn"),
], footer="Append-only, like a clinical note. A ledger you can quietly edit is worth nothing in a dispute.")

addx("Chain", "D20-payment",
    o_desk("Org · Billing — D20 Take a Payment", ("Billing", "Halima Sani"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Money owed")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D20_BILL}{D20_TAKE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D20_AFTER}'
        f'{dcta("Record ₦30,000","Save payment D20","check")}'
        f'{dbtn("She cannot pay today","Open plan D20","message-square-text","ghost",full=True)}</Frame></Frame>',
        "Owing", dept="Billing", who=BILLING, badges=BADGES, persona="billing"),
    o_head("Take a payment", "Halima Sani · ₦65,000 owing",
           stats=[("₦85k", "Bill"), ("₦20k", "Paid"), ("₦65k", "Balance")]),
    pinned=f'{D20_BILL}{D20_TAKE}',
    sections=[("after", "arrow-right", "What this changes", "Three things, one of them permanent", "3", None, D20_AFTER, None)],
    foot=f'{dcta("Record ₦30,000","Save payment D20","check")}'
         f'{dbtn("She cannot pay today","Open plan D20","message-square-text","ghost",full=True)}',
    tab_items=o_tabs_for("billing"), tab=1)

# ---------------- D21 claims
D21_CLAIMS = dgroup("Claims with HMOs and NHIS · 14", [
    ref_row("triangle-alert", "Fatima Bello · Hygeia HMO", "CT abdomen with contrast · ₦25,000 · queried: no pre-authorisation on file",
            "2 days", "Claim fatima", tone="err", tag="pending",
            actions=[dbtn("Answer the query", "Answer claim D21", "reply", "navy", size="sm"),
                     dbtn("Bill her instead", "Open payment D20", "receipt", "ghost", size="sm")]),
    ref_row("clock", "Grace Okeke · NHIS", "Consultation and labs · ₦45,000 · submitted 3 Aug, no answer",
            "11 days", "Claim grace", tone="warn", tag="soon",
            actions=[dbtn("Chase", "Chase claim grace", "bell", "ghost", size="sm")]),
    ref_row("check-check", "Emeka Nwosu · Reliance HMO", "Orthopaedic review · ₦18,000 · paid 12 Aug",
            "2 days", "Claim emeka", tone="ok", tag="completed"),
    ref_row("circle-x", "Blessing Ade · AXA Mansard", "Physiotherapy · ₦12,000 · rejected: not covered on her plan",
            "5 days", "Claim blessing", tone="err", tag="cancelled",
            actions=[dbtn("Tell her, with the reason", "Tell member D21", "message-square-text", "navy", size="sm")]),
], footer="A query nobody answers becomes a rejection, and a rejection nobody passes on becomes a bill the member was not expecting.")

D21_AGE = dgroup("How long the money has been out", [
    kpi_line("Under 30 days", "₦680,000"),
    kpi_line("30 to 60 days", "₦390,000"),
    kpi_line("Over 60 days", "₦170,000"),
    kpi_line("Written off this year", "₦88,000"),
], footer="Anything over sixty days is usually gone. The point of this list is to stop things reaching it, not to admire it once they have.")

D21_WHY = dgroup("Why claims get queried here", [
    drow("file-x", "No pre-authorisation", value="6 this month", sub="The commonest one. The desk can get it at check-in in about four minutes.", name="Why preauth", tone="err"),
    drow("user-x", "Member not active on the plan", value="3", sub="Their employer stopped paying and nobody told them", name="Why inactive", tone="warn"),
    drow("file-text", "Diagnosis code missing", value="3", sub="The doctor wrote it in words. The HMO wants the code as well.", name="Why code", tone="warn"),
    drow("calendar-x", "Submitted late", value="2", sub="Most plans give you 30 days from the visit", name="Why late", tone="err"),
], footer="Four causes, fourteen queries. Three are fixed at the front desk before the person is even seen.")

addx("Chain", "D21-claims",
    o_desk("Org · Billing — D21 Insurance Claims", ("Billing", "Claims"),
        f'<Frame w="fill" flex="row" justify="between" items="center">'
        f'{dhead([("₦1.24m sitting",False),("with HMOs",True)],26)}'
        f'{dbtn("Submit a claim","New claim D21","plus","navy",grow=False,size="sm")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{D21_CLAIMS}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{D21_AGE}{D21_WHY}</Frame></Frame>',
        "Claims", dept="Billing", who=BILLING, badges=BADGES, persona="billing", urgent=3),
    o_head("Claims", "14 open · 3 queried", back=False, ctx="Billing · Garki",
           stats=[("₦1.24m", "Outstanding"), ("3", "Queried"), ("1", "Rejected")],
           chips=[("All", "Filter claims all", True), ("Queried", "Filter claims q", False), ("Paid", "Filter claims paid", False)]),
    pinned=D21_CLAIMS,
    sections=[
      ("age", "clock", "How long the money has been out", "₦170,000 over 60 days", "4", "warn", D21_AGE, None),
      ("why", "circle-help", "Why claims get queried", "Three of the four are fixable at the desk", "4", "err", D21_WHY, None),
    ],
    foot=dbtn("Submit a claim", "New claim D21", "plus", "navy", full=True),
    tab_items=o_tabs_for("billing"), tab=2)

# =====================================================================================
# H1–H12  ONE DESTINATION PER RAIL ITEM
#
# Giving each persona its own navigation is only half the change: a rail item that leads
# nowhere is worse than a missing one. These are the screens the new rails need and the module
# did not have — a messages screen for every department rather than only the doctor's, the two
# places an organisation doctor goes that an administrator never does, and the one screen each
# for nursing, pharmacy and imaging that their job is half made of.
# =====================================================================================
def msg_screen(fid, title, persona, who, dept, threads, contacts, note_txt, tab_key=None):
    """Every department gets the same shape and a different address book. Godwin asked how
    staff talk to each other; the answer the module gives is that you message a *department*
    and whoever is on shift picks it up, so the address book is the thing that differs."""
    lst = dgroup("Your messages", threads,
                 footer="A message goes to a department and whoever is on shift picks it up.")
    new = dgroup("Start a conversation", contacts, footer=note_txt)
    addx("Chain", fid,
        o_desk(title, (dept, "Messages"),
            f'<Frame w="fill" flex="row" gap={{16}} items="start">'
            f'<Frame grow={{1}} flex="col" gap={{14}}>{lst}</Frame>'
            f'<Frame w={{344}} flex="col" gap={{14}}>{new}</Frame></Frame>',
            "Messages", dept=dept, who=who, badges=BADGES, persona=persona),
        o_head("Messages", f"{dept} · 2 unread", back=False,
               stats=[("2", "Unread"), ("3 min", "Nursing"), ("8 min", "Lab")]),
        pinned=lst,
        sections=[("new", "message-circle-plus", "Start a conversation", "A department, not a person",
                   str(len(contacts)), None, new, None)],
        tab_items=o_tabs_for(persona), tab=o_tab_index(persona, "Messages"))


DEPT_CONTACTS = {
    "nursing":  drow("heart-pulse", "Nursing", sub="Two on duty · usually answers in 3 minutes", name="Msg to nursing", tone="ok"),
    "lab":      drow("flask-conical", "Laboratory", sub="Three on duty · usually answers in 8 minutes", name="Msg to lab", tone="ok"),
    "pharm":    drow("pill", "Pharmacy", sub="One on duty · usually answers in 20 minutes", name="Msg to pharm", tone="warn"),
    "desk":     drow("concierge-bell", "Front desk", sub="Four on duty", name="Msg to desk"),
    "imaging":  drow("scan", "Imaging", sub="Two on duty · MRI list is full until 14:00", name="Msg to imaging"),
    "billing":  drow("receipt", "Billing", sub="Two on duty", name="Msg to billing"),
    "doctors":  drow("stethoscope", "Doctors on duty", sub="Six in clinic · Dr. Eze is in room 3", name="Msg to doctors"),
    "admin":    drow("building-2", "Mrs. Nwosu — the admin", sub="A named person, deliberately", name="Msg to admin"),
}
C = DEPT_CONTACTS

msg_screen("H1-desk-messages", "Org · Front Desk — H1 Messages", "desk", DESK, "Front desk", [
    msg_row("avatar-4.jpg", "Doctors on duty", "Dr. Eze: send Halima Sani up as soon as she arrives, I will fit her in.", "6 min", "Desk thread dr", unread=True),
    msg_row("avatar-3.jpg", "Nursing · Outpatient", "Ifeoma: room 3 is free now if you want to move anyone forward.", "22 min", "Desk thread nursing", unread=True),
    msg_row("avatar-5.jpg", "Billing", "Kunle: Halima Sani has a ₦65,000 balance — take something at check-in if you can.", "1 h", "Desk thread billing"),
], [C["doctors"], C["nursing"], C["lab"], C["billing"], C["admin"]],
   "You cannot see anything clinical, and nothing here changes that. A message is a sentence, not a way round a permission.", tab_key=0)

msg_screen("H2-nurse-messages", "Org · Nursing — H2 Messages", "nurse", NURSE, "Nursing", [
    msg_row("avatar-4.jpg", "Doctors on duty", "Dr. Eze: repeat Musa Ibrahim's BP in ten minutes and tell me either way.", "4 min", "Nurse thread dr", unread=True),
    msg_row("avatar-5.jpg", "Laboratory", "Sola: the potassium on Musa Ibrahim is critical — has anyone reached Dr. Eze?", "18 min", "Nurse thread lab", unread=True, channel="call"),
    msg_row("avatar-6.jpg", "Front desk", "Blessing Ade has arrived early and is asking about her dressing.", "40 min", "Nurse thread desk"),
], [C["doctors"], C["lab"], C["pharm"], C["desk"], C["admin"]],
   "An escalation is never a message. If a reading is outside the range you were given, use Escalate — it reaches a doctor in two minutes and this does not.", tab_key=0)

msg_screen("H3-lab-messages", "Org · Laboratory — H3 Messages", "lab", LAB, "Laboratory", [
    msg_row("avatar-4.jpg", "Dr. Chuka Eze", "Acknowledged the potassium at 09:52. Repeat it on a fresh sample please.", "3 min", "Lab thread dr", unread=True),
    msg_row("avatar-3.jpg", "Nursing · Outpatient", "Ifeoma: the second tube for Amara Okeke is on its way down.", "15 min", "Lab thread nursing", unread=True),
    msg_row("avatar-6.jpg", "Front desk", "Grace Okeke says she was not told to fast. Shall we rebook her?", "2 h", "Lab thread desk"),
], [C["doctors"], C["nursing"], C["desk"], C["imaging"], C["admin"]],
   "A critical value is never delivered here. It goes by voice with a read-back, and this is only for the sentence that follows it.", tab_key=0)

msg_screen("H4-pharm-messages", "Org · Pharmacy — H4 Messages", "pharm", PHARM, "Pharmacy", [
    msg_row("avatar-4.jpg", "Dr. Ngozi Okafor", "Generic salbutamol is fine for Fatima. Go ahead and dispense it.", "8 min", "Pharm thread dr", unread=True),
    msg_row("avatar-6.jpg", "Front desk", "Fatima Bello is still at the counter — any idea how long?", "12 min", "Pharm thread desk", unread=True),
    msg_row("avatar-5.jpg", "Billing", "Amlodipine price changed on the 12th. Updated on your screen already.", "Yesterday", "Pharm thread billing"),
], [C["doctors"], C["desk"], C["nursing"], C["billing"], C["admin"]],
   "A substitution is not agreed in a message. Use Cannot dispense — it goes to the prescriber with the alternatives and their prices, and it is recorded.", tab_key=0)

msg_screen("H5-img-messages", "Org · Imaging — H5 Messages", "imaging", IMAGING, "Imaging", [
    msg_row("avatar-4.jpg", "Dr. Chuka Eze", "Any chance of squeezing Musa Ibrahim's chest film in before eleven?", "9 min", "Img thread dr", unread=True),
    msg_row("avatar-2.jpg", "Dr. Ifeanyi Nwachukwu", "Three studies waiting on me — I am in until 16:00, send them through.", "25 min", "Img thread rad", unread=True),
    msg_row("avatar-3.jpg", "Nursing · Outpatient", "Halima Sani has a metal plate in her left wrist from 2019.", "1 h", "Img thread nursing"),
], [C["doctors"], C["nursing"], C["desk"], C["lab"], C["admin"]],
   "A safety question is not settled in a message. If somebody is unsure about metal or pregnancy, the study does not start.", tab_key=0)

msg_screen("H6-bill-messages", "Org · Billing — H6 Messages", "billing", BILLING, "Billing", [
    msg_row("avatar-6.jpg", "Front desk", "Ngozi: Halima Sani paid ₦30,000 at the desk just now, reference PSK-0091.", "5 min", "Bill thread desk", unread=True),
    msg_row("avatar-2.jpg", "Mrs. Adaeze Nwosu", "Hygeia have queried the CT again. Can you answer it today?", "40 min", "Bill thread admin", unread=True),
    msg_row("avatar-5.jpg", "Pharmacy", "Bayo: the generic is ₦1,900, not ₦4,200 — worth telling Fatima before she pays.", "3 h", "Bill thread pharm"),
], [C["desk"], C["admin"], C["pharm"], C["doctors"], C["lab"]],
   "Nobody on Medra is refused care over a balance. Chasing a bill and withholding treatment are different decisions.", tab_key=0)

# ---------------- H7 the organisation doctor's own patient list
H7_LIST = dgroup("Allocated to you this week · 24", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "Seen today 10:30 · hypertension review · note signed", "Today", "H7 amara", tag="completed"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "In clinic now · chest pain · potassium 7.2 unacknowledged", "Now", "Open critical D15", tag="new"),
    patient_row("avatar-6.jpg", "Halima Sani", "MDR-9012-44", "11:20 · referred in from Wuse Clinic · MRI booked", "Waiting", "H7 halima"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "11:40 · diabetes review · HbA1c back this morning", "Waiting", "H7 grace"),
    patient_row("avatar-4.jpg", "Fatima Bello", "MDR-2201-13", "Tuesday · asthma · inhaler dispensed", "2 days", "H7 fatima", tag="completed"),
], footer="Only people the hospital allocated to you, and only while they are in your care. Access closes when the visit is marked complete.")

H7_MINE = dgroup("Where they came from", [
    drow("concierge-bell", "Booked by the front desk", value="18", sub="The normal route here", name="H7 src desk", chevron=False),
    drow("share-2", "Referred in from another organisation", value="4", sub="Two still to be answered", name="Nav Referrals", tone="warn"),
    drow("user-plus", "Walked in", value="2", sub="Registered at the desk this morning", name="H7 src walk", chevron=False),
], footer="You did not book any of these. In your own practice the same screen is people who chose you.")

H7_OPEN = dgroup("Still open on you", [
    drow("notebook-pen", "2 notes unsigned", sub="Tuesday's clinic · a member sees nothing until you sign", name="H7 unsigned", tone="err"),
    drow("flask-conical", "3 results waiting", sub="One critical and unacknowledged", name="Nav Dr Results", tone="err"),
    drow("calendar-plus", "4 follow-ups to arrange", sub="The desk books them once you say when", name="H7 followups", tone="warn"),
])

addx("Clinic", "H7-dr-patients",
    o_desk("Org · Doctor — H7 My Patients", ("Clinic", "Patients"),
        f'{rows_of([stat_tile("users","24","Allocated this week","18 seen","teal","Stat h7 alloc"),stat_tile("notebook-pen","2","Notes unsigned","Tuesday","err","H7 unsigned"),stat_tile("flask-conical","3","Results waiting","1 critical","err","Nav Dr Results"),stat_tile("share-2","4","Referred in","2 unanswered","warn","Nav Referrals")],4,14)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{H7_LIST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{H7_OPEN}{H7_MINE}</Frame></Frame>',
        "Patients", dept="General practice", who=ORGDOC, badges=BADGES, persona="orgdoc"),
    o_head("My patients", "24 allocated this week", back=False,
           stats=[("24", "Allocated"), ("2", "Unsigned"), ("3", "Results")]),
    pinned=H7_LIST,
    sections=[
      ("open", "inbox", "Still open on you", "Two unsigned notes, three results", "3", "err", H7_OPEN, None),
      ("src", "route", "Where they came from", "The desk booked eighteen of them", "3", None, H7_MINE, None),
    ],
    tab_items=o_tabs_for("orgdoc"), tab=1)

# ---------------- H8 results waiting on the organisation doctor
H8_WAIT = dgroup("Waiting for you to release · 3", [
    drow("siren", "Musa Ibrahim · potassium 7.2", value="CRITICAL", sub="Verified 09:38 · the laboratory rang at 09:44 · unacknowledged", name="Open critical D15", tone="err"),
    drow("flask-conical", "Grace Okeke · HbA1c 6.8%", value="High", sub="Verified 08:12 · she is in clinic at 11:40", name="H8 grace", tone="warn"),
    drow("scan", "Halima Sani · MRI lumbar spine", value="Reported", sub="Dr. Nwachukwu signed it 14 minutes ago", name="H8 halima", tone="ok"),
], footer="Nothing reaches a member until you release it. A number with no explanation sends people to A&E at midnight.")

H8_DONE = dgroup("Released this week · 11", [
    drow("check-check", "Fatima Bello · spirometry", value="Released", sub="With your one-line explanation · she read it", name="H8 fatima", tone="ok", chevron=False),
    drow("check-check", "Emeka Nwosu · full blood count", value="Released", sub="Normal · no comment needed", name="H8 emeka", tone="ok", chevron=False),
])

H8_HOW = dgroup("Where these come from", [
    drow("building-2", "Garki's own laboratory", value="8", sub="Structured, straight into the record", name="H8 src lab", chevron=False),
    drow("scan", "Garki imaging", value="2", sub="A radiologist's report, not just the pictures", name="H8 src img", chevron=False),
    drow("link", "An outside laboratory on a single-use link", value="1", sub="Lifebridge Diagnostics · returned this morning", name="H8 src link", chevron=False),
], footer="In your private practice this list looks the same. The difference is that here the hospital pays for the tests and you never see the price.")

addx("Clinic", "H8-dr-results",
    o_desk("Org · Doctor — H8 Results", ("Clinic", "Results"),
        f'{alert_strip("siren","Musa Ibrahim, potassium 7.2, unacknowledged","The laboratory rang you at 09:44. It is climbing the escalation ladder and will reach Dr. Ade at 30 minutes.","err",dbtn("Open it","Open critical D15","arrow-right","danger",grow=False,size="sm"))}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{H8_WAIT}{H8_DONE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{H8_HOW}</Frame></Frame>',
        "Results", dept="General practice", who=ORGDOC, badges=BADGES, persona="orgdoc", urgent=1),
    o_head("Results", "3 waiting · 1 critical", back=False,
           stats=[("3", "Waiting"), ("1", "Critical"), ("11", "Released")]),
    pinned=H8_WAIT,
    sections=[
      ("done", "check-check", "Released this week", "Eleven, all read", "11", "ok", H8_DONE, None),
      ("how", "route", "Where these come from", "Two laboratories and a link", "3", None, H8_HOW, None),
    ],
    tab_items=o_tabs_for("orgdoc"), tab=2)

# ---------------- H9 nursing standing orders
H9_LIST = dgroup("Standing orders running now", [
    task_row_big("Daily", "Musa Ibrahim · MDR-7714-02", "Dr. Okafor · day 2 of 5 · 09:12",
                 "Ceftriaxone 1 g IM once daily", "SO musa", action="Record", avatar="avatar-1.jpg",
                 flags=[("syringe", "Injection")], tone="warn"),
    task_row_big("Daily", "Blessing Ade · MDR-3310-08", "Dr. Eze · day 4 of 7 · until 21 Aug",
                 "Dressing change, left leg ulcer", "SO blessing", action="Record", avatar="avatar-5.jpg",
                 flags=[("bandage", "Dressing")]),
    task_row_big("Before clinic", "Grace Okeke · MDR-8842-21", "Dr. Okafor · every review",
                 "Fasting glucose before she is seen", "SO grace", action="Record", avatar="avatar-3.jpg",
                 flags=[("droplet", "Fasting")], tone="ok"),
], footer="A standing order is a doctor's instruction that repeats. You record each time you carry it out, and the count runs down on its own.")

H9_RULES = dgroup("What you may do without asking", [
    drow("thermometer", "Record any vital sign", sub="Always. It is the reading, not a decision", name="H9 vitals", chevron=False, tone="ok"),
    drow("syringe", "Give a drug on a standing order", sub="Within the dates the doctor set, and you sign each dose", name="H9 give", chevron=False, tone="ok"),
    drow("triangle-alert", "Escalate anything out of range", sub="Two minutes to the first doctor, then the duty doctor automatically", name="Open escalate D4", tone="warn"),
    drow("ban", "Change a dose or start something new", sub="Never. Ask the prescriber — it takes a minute and it is recorded", name="H9 no", chevron=False, tone="err"),
], footer="These four are the nursing scope in this organisation. They are set by the department and cannot be widened for one person.")

H9_ENDING = dgroup("Ending soon", [
    drow("calendar-x", "Musa Ibrahim · ceftriaxone", value="3 days left", sub="Ends 20 August unless Dr. Okafor extends it", name="H9 end musa", tone="warn", chevron=False),
    drow("calendar-x", "Blessing Ade · dressing", value="3 days left", sub="Ends 21 August", name="H9 end blessing", chevron=False),
])

addx("Chain", "H9-nurse-orders",
    o_desk("Org · Nursing — H9 Standing Orders", ("Nursing", "Standing orders"),
        f'{dhead([("What the doctors",False),("have left running",True)],26)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{H9_LIST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{H9_RULES}{H9_ENDING}</Frame></Frame>',
        "Standing orders", dept="Nursing", who=NURSE, badges=BADGES, persona="nurse"),
    o_head("Standing orders", "3 running · 2 ending soon", back=False,
           stats=[("3", "Running"), ("2", "Ending"), ("6", "Doses today")]),
    pinned=H9_LIST,
    sections=[
      ("rules", "shield-check", "What you may do without asking", "Four lines, set by the department", "4", None, H9_RULES, None),
      ("end", "calendar-x", "Ending soon", "Two, both this week", "2", "warn", H9_ENDING, None),
    ],
    tab_items=o_tabs_for("nurse"), tab=2)

# ---------------- H10 pharmacy stock
H10_SHELF = data_table(
    ["Medicine", "On the shelf", "Needed today", "Status"],
    [["Amlodipine 5 mg", "240", "30", "Comfortable"],
     ["Metformin 500 mg", "18", "60", "Short"],
     ["Salbutamol inhaler", "0", "2", "Out"],
     ["Ceftriaxone 1 g", "34", "5", "Comfortable"],
     ["Paracetamol 500 mg", "1,200", "80", "Comfortable"],
     ["Insulin glargine", "6", "2", "Watch"]],
    title="What is on the shelf", name="Stock row",
    note="A count you keep here, not a warehouse system — so you can tell a member before they queue.")

H10_ACT = dgroup("Two need a decision today", [
    outcome_choice("package-x", "Salbutamol inhaler is out", "Two people are prescribed it today. Propose the generic or send them elsewhere.", "Open sub D11", sel=True, tone="err"),
    outcome_choice("package", "Metformin will not last the day", "Eighteen left against sixty needed. Tell the admin now rather than at four o'clock.", "H10 metformin", tone="warn"),
], footer="Telling somebody early is the whole value of counting. A member who is told at the door can go elsewhere; one told at the counter has already queued.")

H10_ASK = dcard(
    eyerow("Tell the admin what you need")
    + field("What is short", "package", "Metformin 500 mg · 200 tablets", ph=False)
    + field_chips("How urgent?", ["Today", "This week", "Next order"], 0, "Stock urgency")
    + dtoggle("bell", "Warn the doctors it is short", sub="They see it when they prescribe, so nobody promises what we cannot give", on=True, name="Stock warn"))

addx("Chain", "H10-pharm-stock",
    o_desk("Org · Pharmacy — H10 Stock", ("Pharmacy", "Stock"),
        f'{rows_of([stat_tile("package","6","Medicines counted","Updated 08:40","teal","Stat h10 count"),stat_tile("package-x","1","Out of stock","Salbutamol inhaler","err","Open sub D11"),stat_tile("triangle-alert","2","Short today","Metformin, insulin","warn","H10 metformin"),stat_tile("repeat","3","Substitutions","This week","info","Nav Pharm Sub")],4,14)}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{H10_SHELF}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{H10_ACT}{H10_ASK}</Frame></Frame>',
        "Stock", dept="Pharmacy", who=PHARM, badges=BADGES, persona="pharm", urgent=1),
    o_head("Stock", "1 out · 2 short today", back=False,
           stats=[("6", "Counted"), ("1", "Out"), ("2", "Short")]),
    pinned=H10_SHELF,
    sections=[
      ("act", "triangle-alert", "Two need a decision today", "Salbutamol out, metformin short", "2", "err", H10_ACT, None),
      ("ask", "send", "Tell the admin what you need", "It goes to Mrs. Nwosu", None, None, H10_ASK, None),
    ],
    tab_items=o_tabs_for("pharm"), tab=1)

# ---------------- H11 imaging rooms
H11_ROOMS = dgroup("Rooms and machines", [
    drow("scan", "MRI suite", value="In use", sub="Halima Sani · until 10:45 · Tunde running it", name="H11 mri", tone="warn"),
    drow("scan-line", "CT", value="Free", sub="Next booked 11:45 · contrast, so creatinine needed first", name="H11 ct", tone="ok"),
    drow("radiation", "X-ray room 1", value="Free", sub="Musa Ibrahim can go now", name="H11 xr1", tone="ok"),
    drow("radiation", "X-ray room 2", value="Out of service", sub="Tube fault reported 12 Aug · engineer due Friday", name="H11 xr2", tone="err"),
    drow("monitor", "Ultrasound", value="Free", sub="Sonographer in at 10:30", name="H11 us", tone="ok"),
    drow("activity", "ECG trolley", value="On ward 2", sub="Bring it back before 10:15", name="H11 ecg", tone="warn"),
], footer="A free machine, a free room and somebody to run it are three different facts. All three have to be true before a study is really bookable.")

H11_DAY = heat_grid(["08", "09", "10", "11", "12", "13"], [
    ("MRI", [1, 1, 1, 1, 0, 1]), ("CT", [0, 1, 0, 1, 1, 0]),
    ("X-ray", [2, 3, 2, 1, 1, 0]), ("US", [0, 1, 2, 2, 1, 0]),
], title="Today, room by room", unit="Studies booked",
   note="Two X-ray rooms are drawn as one line because one of them is out of service. Friday looks like this every week.")

H11_FIX = dgroup("Out of service", [
    drow("wrench", "X-ray room 2 · tube fault", value="5 days", sub="Reported 12 Aug by Tunde · engineer due Friday · admin told", name="H11 fault", tone="err"),
    drow("calendar-x", "14 studies moved", sub="All rebooked into room 1, which is why today is tight", name="H11 moved", tone="warn", chevron=False),
], footer="A machine out of service is an organisation problem, not a departmental one. The admin sees this on Today and it is what a capital request is argued from.")

addx("Chain", "H11-img-rooms",
    o_desk("Org · Imaging — H11 Rooms", ("Imaging", "Rooms"),
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{H11_ROOMS}{H11_DAY}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{H11_FIX}'
        f'{dbtn("Report a fault","H11 report","wrench","warn",full=True)}</Frame></Frame>',
        "Rooms", dept="Imaging", who=IMAGING, badges=BADGES, persona="imaging", urgent=1),
    o_head("Rooms", "5 working · 1 out of service", back=False,
           stats=[("5", "Working"), ("1", "Out"), ("6", "Booked")]),
    pinned=H11_ROOMS,
    sections=[
      ("day", "calendar-clock", "Today, room by room", "Room 1 is carrying both lists", None, "warn", H11_DAY, None),
      ("fix", "wrench", "Out of service", "X-ray 2, five days", "2", "err", H11_FIX, None),
    ],
    foot=dbtn("Report a fault", "H11 report", "wrench", "warn", full=True),
    tab_items=o_tabs_for("imaging"), tab=2)

# =====================================================================================
# 5. REFERRALS & EXTERNAL ACCESS  (Module 12)
# =====================================================================================
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
], footer="On Medra it lands in their inbox. Off it, the same information goes down a link that expires.")

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
], footer="The default is the minimum, and Amara approves it before anything leaves.")

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
    + I("link", 15, M_IC) + T(13, "regular", "var:text/strong", "medra.ng/s/7fQ2-K9mR-4vXt", w="fill")
    + f'<Frame name="Btn Copy link E3" flex="row">{I("copy",15,N_IC)}</Frame></Frame>'
    + T(11, "regular", "var:text/muted",
        "A random token, never the member's Medra ID — nobody reaches a record by guessing, and one link tells you nothing about any other.", w="fill")
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
      ("link", "link", "The link they will get", "medra.ng/s/7fQ2-K9mR-4vXt", None, None, E3_LINK, None),
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
], footer="Accepting books it and tells them both. Declining tells them too, in your words — silence is the one option not available.")

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
], footer="What she agreed to send, not everything we could ask for. Ask her and she can add to it.")

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
], footer="One job, one recipient, and it dies when they finish. Anything still open after 48 hours is chased.")

E6_HOW = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",16,A_IC)}'
    f'{T(14,"semibold","var:text/strong","Why a link and not an account")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Most Nigerian laboratories are not on Medra and will not sign up to run one test. A member should not have to carry paper because of that.", w="fill")
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
            f'{T(11,"regular","var:text/muted","medra.ng/s/3jT8-Wp5N-2bQy")}</Frame>'
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
            f'{T(10,"regular","var:text/muted","medra.ng/s/3jT8-Wp5N-2bQy")}</Frame>'
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
], footer="Ending one closes it immediately and the member is told.")

F1_RULE = dcard(
    f'<Frame flex="row" gap={{9}} items="center">{I("shield-check",17,OK_IC)}'
    f'{T(14,"semibold","var:text/strong","The organisation never owns the record")}</Frame>'
    + T(12, "regular", "var:text/default",
        "Garki holds a copy. The record belongs to the member — if Garki left Medra tomorrow, every member would keep everything.", w="fill"),
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
# =====================================================================================
# F4, F8–F10  WHAT THE ADMIN CAN SEE
#
# Godwin: "our next meeting should be the dashboard of the institutions." The console had
# one Reports screen with a bar chart and five ratios on it, which is a summary rather
# than an answer. An administrator's real questions are four, and each one is a screen:
# how many people did we see and who were they; what are the doctors actually doing with
# their time; is each department keeping up; and where is the money coming from.
#
# The charts obey the rules at the top of org_kit.py — one blue ramp light to dark, no
# green/amber/red inside a chart, a number on every mark, and a table wherever there are
# more than about seven things to tell apart.
# =====================================================================================
VISITS = [("Mar", 986, "986"), ("Apr", 1104, "1,104"), ("May", 1043, "1,043"),
          ("Jun", 1218, "1,218"), ("Jul", 1272, "1,272"), ("Aug", 1412, "1,412")]

# The week as the front desk experiences it. Monday morning and Friday afternoon are not
# the same clinic, and no ratio on the old screen could say so.
BUSY_ROWS = [("Mon", [18, 26, 31, 22, 14, 9]), ("Tue", [14, 21, 24, 19, 12, 7]),
             ("Wed", [16, 23, 27, 20, 11, 6]), ("Thu", [15, 22, 26, 21, 13, 8]),
             ("Fri", [19, 28, 33, 25, 17, 11]), ("Sat", [8, 12, 14, 9, 4, 2])]
BUSY_COLS = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00"]

F4_HERO = hero_stat("1,412", "People seen in August", "Up 11% on July · 148 expected today across three branches",
    right=f'<Frame flex="col" gap={{7}} items="end">'
          f'{dbtn("Export as a spreadsheet","Export report F4","download","ghost",grow=False,size="sm")}'
          f'{T(10,"regular","var:text/faint","Last updated 09:41")}</Frame>')

F4_CHART = col_chart(VISITS, title="Visits a month",
    action=f'<Frame name="Btn Report range" flex="row">{T(11,"semibold","var:text/accent","Last 6 months")}</Frame>',
    note="The busiest month on record, and not finished. Most of the growth is follow-ups rather than new members.")

F4_JUMP = dgroup("Look closer", [
    drow("users", "Patients", value="1,412", sub="Who they were, where they came from, who did not turn up", name="Open patients F8"),
    drow("stethoscope", "Clinicians", value="9", sub="Consultation hours, how long each doctor spends, notes signed", name="Open clinicians F9"),
    drow("building-2", "Departments and staff", value="7", sub="Throughput, turnaround, who is carrying the load", name="Open depts F10"),
    drow("banknote", "Money", value="₦8.4m", sub="Collected, outstanding, and ₦1.24m sitting with HMOs", name="Open claims D21"),
], footer="Every number here is for the branch and department in the subtitle. Change either and they all change with it.")

F4_WATCH = dgroup("Things worth watching", [
    drow("circle-slash", "No-show rate", value="7.2%", sub="Down from 11% before payment-before-booking", name="Rep noshow", tone="ok", chevron=False),
    drow("clock", "Median wait to be seen", value="14 min", sub="Up 4 minutes this week — Friday mornings are the worst", name="Rep wait", tone="warn", chevron=False),
    drow("notebook-pen", "Notes signed same day", value="94%", sub="Six unsigned notes older than 48 hours, across two doctors", name="Open clinicians F9", tone="warn"),
    drow("timer", "Laboratory turnaround", value="2h 40m", sub="Target 4 hours", name="Rep lab", tone="ok", chevron=False),
    drow("siren", "Criticals acknowledged in 15 min", value="12 of 14", sub="Two took longer. Both are in the audit log with who was rung.", name="Open critical F7", tone="warn"),
], footer="Each of these is somebody's job rather than a score.")

addx("Govern", "F4-reports",
    o_desk("Org · Reports — F4 Reports", ("Reports",),
        f'{F4_HERO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F4_CHART}'
        f'{heat_grid(BUSY_COLS, BUSY_ROWS, title="When the place is busy", unit="People arriving",note="Friday at ten is the peak, Monday close behind. This is the shape you would be staffing against.")}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F4_JUMP}{F4_WATCH}</Frame></Frame>',
        NAV["Reports"], badges=BADGES),
    o_head("Reports", "August · 1,412 seen", back=False, ctx="All branches",
           stats=[("1,412", "Seen"), ("7.2%", "No-show"), ("14m", "Wait")]),
    pinned=f'{F4_CHART}{F4_JUMP}',
    sections=[
      ("busy", "calendar-clock", "When the place is busy", "Friday at ten is the peak", None, None,
       heat_grid(BUSY_COLS, BUSY_ROWS, note="This is the shape you would be staffing against."), None),
      ("watch", "activity", "Things worth watching", "Waits are up, six notes unsigned", "5", "warn", F4_WATCH, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F8 patients
F8_HERO = hero_stat("1,412", "People seen in August", "412 of them had never been here before")

F8_SPLIT = part_bar([("Returning", 71, "1,000"), ("New to this organisation", 22, "312"),
                     ("Referred in from elsewhere", 7, "100")],
    title="New against returning", total="1,412",
    note="Seven in ten had been here before — the best single measure of whether you keep the people you treat.")

F8_SOURCE = data_table(
    ["How they got here", "August", "Share", "No-show"],
    [["Booked in Medra", "612", "43%", "4.1%"],
     ["Walked in", "487", "34%", "—"],
     ["Booked by phone", "213", "15%", "12.6%"],
     ["Referred by another organisation", "100", "7%", "6.0%"]],
    title="Where the visits came from",
    note="A phone booking is three times more likely to be a no-show: nobody paid, and nobody was reminded.")

F8_WHY = rank_bars([
    ("Hypertension review", "Mostly 45 and over", 318, "318"),
    ("Antenatal", "Booked as a course, not one visit", 224, "224"),
    ("Diabetes review", "Two thirds are repeat visits", 186, "186"),
    ("Malaria and febrile illness", "Peaks after rain", 171, "171"),
    ("Paediatric general", "Half arrive as walk-ins", 149, "149"),
    ("Everything else", "84 different reasons", 364, "364", True),
], title="Why people came",
   note="Six lines rather than a pie, because the tail is the point: 364 visits across 84 reasons.")

F8_AGE = data_table(
    ["Age", "People", "Share", "Repeat rate"],
    [["Under 5", "138", "10%", "48%"], ["5 – 17", "121", "9%", "31%"],
     ["18 – 34", "396", "28%", "52%"], ["35 – 54", "418", "30%", "74%"],
     ["55 and over", "339", "24%", "88%"]],
    title="Who they were", name="Age",
    note="Nobody over 55 comes here once. Plan follow-up capacity around them.")

F8_MISS = dgroup("Who did not turn up", [
    drow("circle-slash", "102 no-shows in August", value="7.2%", sub="Down from 11% before payment-before-booking", name="F8 noshow", tone="ok", chevron=False),
    drow("phone", "78 of them booked by phone", sub="Unpaid, unreminded. The desk can take payment at the time of booking.", name="F8 phone", tone="warn", chevron=False),
    drow("repeat", "31 rebooked within a week", sub="A missed appointment is not a lost patient unless nobody follows up", name="F8 rebook", tone="ok", chevron=False),
    drow("user-x", "9 people missed three or more", sub="Worth a call rather than another booking", name="F8 repeatmiss", tone="warn"),
], footer="Understood rather than charged for. F5 decides the charge; this decides whether it is working.")

addx("Govern", "F8-patients",
    o_desk("Org · Reports — F8 Patients", ("Reports", "Patients"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Reports")}</Frame>'
        f'{F8_HERO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F8_SPLIT}{F8_WHY}{F8_SOURCE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F8_MISS}{F8_AGE}</Frame></Frame>',
        NAV["Reports"], badges=BADGES),
    o_head("Patients", "August · 1,412 seen", ctx="All branches",
           stats=[("1,412", "Seen"), ("312", "New"), ("7.2%", "No-show")]),
    pinned=f'{F8_HERO}{F8_SPLIT}',
    sections=[
      ("why", "list", "Why people came", "Hypertension leads, and the tail is long", "6", None, F8_WHY, None),
      ("source", "route", "Where the visits came from", "Phone bookings are the no-shows", "4", "warn", F8_SOURCE, None),
      ("age", "users", "Who they were", "Nobody over 55 comes here once", "5", None, F8_AGE, None),
      ("miss", "circle-slash", "Who did not turn up", "102 no-shows, 78 booked by phone", "4", "warn", F8_MISS, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F9 clinicians
# The number Godwin asked for by name: how many hours a doctor spent consulting. It is not
# the same as hours rostered, and the gap between the two is the most useful thing on this
# screen — a doctor rostered for 40 hours who consulted for 22 is either under-booked or
# doing something else, and only one of those is a problem.
F9_HERO = hero_stat("218 h", "Consulting time in August", "Across 9 clinicians · 74% of the hours they were rostered for")

F9_HOURS = rank_bars([
    ("Dr. Ngozi Okafor", "Cardiology · 41 h rostered", 38, "38 h"),
    ("Dr. Chuka Eze", "General practice · 40 h rostered", 34, "34 h"),
    ("Dr. Amina Yusuf", "Paediatrics · 32 h rostered", 29, "29 h"),
    ("Dr. Tunde Bello", "General practice · 40 h rostered", 24, "24 h"),
    ("Dr. Femi Adeyemi", "Obstetrics · 24 h rostered", 22, "22 h"),
    ("Dr. Sade Lawal", "General practice · 36 h rostered", 21, "21 h"),
], title="Hours actually spent consulting", name="Doc",
   note="Measured from opening a consultation to signing it, not from the roster. Dr. Bello is rostered like Dr. Eze and consulted ten hours less — a question, not a verdict.")

F9_TABLE = data_table(
    ["Clinician", "Seen", "Hours", "Median", "Signed same day"],
    [["Dr. Ngozi Okafor", "214", "38 h", "11 min", "99%"],
     ["Dr. Chuka Eze", "198", "34 h", "10 min", "96%"],
     ["Dr. Amina Yusuf", "176", "29 h", "10 min", "100%"],
     ["Dr. Tunde Bello", "121", "24 h", "12 min", "78%"],
     ["Dr. Femi Adeyemi", "104", "22 h", "13 min", "94%"],
     ["Dr. Sade Lawal", "119", "21 h", "11 min", "91%"]],
    title="Every clinician, side by side", name="Doc row",
    note="Ten minutes against a twenty-minute slot cuts both ways: the slot may be too long, or people may be being hurried.")

F9_QUALITY = dgroup("Quality, not volume", [
    drow("notebook-pen", "Six notes unsigned over 48 hours", sub="Four are Dr. Bello's. A member cannot see a consultation until it is signed.", name="F9 unsigned", tone="err"),
    drow("siren", "Two criticals took over 15 minutes", sub="Both acknowledged in the end, both in the audit log", name="Open critical F7", tone="warn"),
    drow("repeat", "11% returned within 7 days", sub="Same complaint, same organisation — usually the honest signal that a first visit did not settle it", name="F9 return", tone="warn", chevron=False),
    drow("share-2", "88% of referrals answered in a day", sub="Three took longer than two days", name="Nav Referrals", tone="ok"),
], footer="Volume is easy to game. These four say whether the work was any good.")

F9_TIME = part_bar([("Consulting", 54, "218 h"), ("Notes and results", 21, "84 h"),
                    ("Waiting on a patient", 15, "62 h"), ("Referrals and messages", 10, "40 h")],
    title="Where a clinical hour goes", total="404 h",
    note="Sixty-two hours a month waiting for somebody to walk in. That is the number the booking rules can move.")

addx("Govern", "F9-clinicians",
    o_desk("Org · Reports — F9 Clinicians", ("Reports", "Clinicians"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Reports")}</Frame>'
        f'{F9_HERO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F9_HOURS}{F9_TABLE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F9_TIME}{F9_QUALITY}</Frame></Frame>',
        NAV["Reports"], badges=BADGES),
    o_head("Clinicians", "August · 218 consulting hours", ctx="All branches",
           stats=[("218 h", "Consulting"), ("74%", "Of rostered"), ("11 min", "Median")]),
    pinned=f'{F9_HERO}{F9_HOURS}',
    sections=[
      ("table", "table", "Every clinician, side by side", "Seen, hours, median, signed", "6", None, F9_TABLE, None),
      ("time", "clock", "Where a clinical hour goes", "62 hours waiting on a patient", "4", None, F9_TIME, None),
      ("quality", "shield-check", "Quality, not volume", "Six notes unsigned over 48 hours", "4", "err", F9_QUALITY, None),
    ],
    tab_items=TAB_ADMIN, tab=4)

# ---------------- F10 departments and staff
F10_HERO = hero_stat("7", "Departments", "24 people on seats · 19 worked this week")

F10_TABLE = data_table(
    ["Department", "Done", "Waiting", "Median", "Seats"],
    [["Consulting", "1,412", "9", "11 min", "11 of 12"],
     ["Nursing", "1,106", "5", "6 min", "6 of 8"],
     ["Front desk", "1,842", "12", "4 min", "5 of 5"],
     ["Laboratory", "612", "7", "2 h 40", "3 of 4"],
     ["Pharmacy", "489", "4", "9 min", "2 of 3"],
     ["Imaging", "184", "6", "1 h 10", "2 of 3"],
     ["Billing", "923", "9", "7 min", "2 of 2"]],
    title="Every department, side by side", name="Dept row",
    note="A table, not a chart: past about seven things colour stops telling them apart. Front desk has no spare seat and the highest volume in the building.")

F10_LOAD = rank_bars([
    ("Front desk", "5 people · 1,842 check-ins", 368, "368"),
    ("Nursing", "6 people · 1,106 tasks", 184, "184"),
    ("Consulting", "11 people · 1,412 visits", 128, "128"),
    ("Billing", "2 people · 923 transactions", 462, "462"),
    ("Laboratory", "3 people · 612 samples", 204, "204"),
    ("Pharmacy", "2 people · 489 dispensed", 245, "245"),
], title="Transactions per person", name="Load",
   note="Billing does the most per head on two seats, the front desk second on five. Look here before adding a clinician.")

F10_TURN = dgroup("How long each department takes", [
    progress_row("Front desk · check-in", "4 min", 20, "teal"),
    progress_row("Nursing · vitals", "6 min", 30, "teal"),
    progress_row("Pharmacy · dispense", "9 min", 45, "teal"),
    progress_row("Imaging · report back", "1 h 10", 70, "amber"),
    progress_row("Laboratory · result back", "2 h 40", 66, "amber"),
], footer="Against each department's own target, not against each other. Both amber ones are inside target.")

F10_PEOPLE = dgroup("Who is actually here", [
    shift_row("Sister Ifeoma Uche", "Nursing", "Until 15:00", "F10 ifeoma", sub="Nursing · 214 tasks this month"),
    shift_row("Mr. Sola Adeniyi", "Laboratory", "Until 17:00", "F10 sola", sub="Laboratory · 198 samples"),
    shift_row("Miss Ngozi Peter", "Front desk", "Until 16:00", "F10 ngozi", sub="Front desk · 412 check-ins"),
    shift_row("Mr. Bayo Ogun", "Pharmacy", "Off today", "F10 bayo", on=False, sub="Pharmacy · 244 dispensed"),
    shift_row("Mr. Emeka Obi", "Suspended 2 August", "Suspended", "Person emeka", on=False, sub="Front desk · seat returned"),
], footer="People rather than rows, because this is the list you read when somebody rings in sick.")

addx("Govern", "F10-departments",
    o_desk("Org · Reports — F10 Departments", ("Reports", "Departments"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Reports")}</Frame>'
        f'{F10_HERO}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F10_TABLE}{F10_LOAD}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F10_TURN}{F10_PEOPLE}</Frame></Frame>',
        NAV["Reports"], badges=BADGES),
    o_head("Departments", "7 departments · 24 on seats", ctx="All branches",
           stats=[("7", "Departments"), ("24", "On seats"), ("2", "Seats spare")]),
    pinned=f'{F10_HERO}{F10_TABLE}',
    sections=[
      ("load", "chart-column", "Transactions per person", "Billing does the most on two seats", "6", "warn", F10_LOAD, None),
      ("turn", "timer", "How long each department takes", "All five inside target", "5", None, F10_TURN, None),
      ("people", "users", "Who is actually here", "19 of 24 worked this week", "5", None, F10_PEOPLE, None),
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


# ---------------- F7 the ones nobody has answered
F7_OPEN = dgroup("Unacknowledged critical results · 2", [
    request_row("siren", "Musa Ibrahim · potassium 7.2", "Laboratory called Dr. Okafor 09:44 · she has not opened it",
                "6 min", "Crit musa", "err",
                [dbtn("Call the medical director", "Crit director", "phone-call", "danger", size="sm"),
                 dbtn("Reassign to the on-call", "Crit reassign", "user-round-check", "ghost", size="sm")]),
    request_row("siren", "Ngozi Bala · haemoglobin 4.1", "Acknowledged by Dr. Eze 08:12 · no action recorded since",
                "1h 20m", "Crit ngozi", "warn",
                [dbtn("Ask him what he did", "Crit ask", "message-square-text", "ghost", size="sm")]),
], footer="Acknowledged is not the same as acted on, and this board shows both. A result that was heard and then forgotten is the failure that reaches a coroner.")

F7_LADDER = dgroup("How an unanswered critical escalates", [
    prep_step(1, "The laboratory calls the requesting doctor", "By voice, with a read-back, recorded on D15"),
    prep_step(2, "15 minutes: the medical officer on call", "Automatically, whether or not anyone remembers"),
    prep_step(3, "30 minutes: the medical director", "And it appears on this board in red"),
    prep_step(4, "It never times out", "There is no state in which a critical value quietly stops being anyone's problem"),
], footer="The ladder is the organisation's, not Medra's. You set the two intervals and who sits on each rung in Settings.")

F7_RATE = dgroup("This month", [
    kpi_line("Critical results", "14"),
    kpi_line("Reached a doctor inside 10 minutes", "12"),
    kpi_line("Escalated past the requester", "2"),
    kpi_line("Median time to acknowledgement", "6 min"),
], footer="Two escalations in a month is normal. Two in a week is a rota problem, not a laboratory problem.")

addx("Govern", "F7-critical",
    o_desk("Org · Governance — F7 Critical Results", ("Access", "Critical results"),
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{F7_OPEN}{F7_LADDER}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{F7_RATE}'
        f'{dbtn("Open the audit log","Open audit F2","history","ghost",full=True)}</Frame></Frame>',
        NAV["Access"], badges=BADGES, urgent=2),
    o_head("Critical results", "2 open · 1 past the requester", back=False,
           stats=[("2", "Open"), ("6 min", "Median"), ("14", "This month")]),
    pinned=F7_OPEN,
    sections=[
      ("ladder", "list-checks", "How an unanswered critical escalates", "Four rungs, and it never times out", "4", "err", F7_LADDER, None),
      ("rate", "chart-column", "This month", "14 criticals, 2 escalated", None, None, F7_RATE, None),
    ],
    tab_items=TAB_ADMIN, tab=0)

# =====================================================================================
# THE DOCTOR INSIDE THE ORGANISATION
# One account, two workplaces. Dr. Eze's MDCN number is his, not Garki's, so the hospital
# inviting him added a workplace to an account that already existed — it did not make a second
# clinician. The consultation is identical to his private one; what differs is who fills his
# day, whose roster he is on, who he answers to, and that the money is not his to see.
# =====================================================================================
G1_TILES = rows_of([
    stat_tile("users", "11", "Allocated to you today", "Front desk filled your list", "teal", "Stat allocated"),
    stat_tile("clock", "20 min", "Slot length here", "The department sets it, not you", "slate", "Stat length"),
    stat_tile("flask-conical", "3", "Results waiting", "1 critical, unacknowledged", "err", "Open critical D15"),
    stat_tile("message-square-text", "4", "From the team", "2 from nursing", "info", "Open messages G3"),
], 4, 14)

G1_QUEUE = dgroup("Allocated to you", [
    patient_row("avatar-2.jpg", "Amara Okeke", "MDR-8842-19", "10:30 · hypertension review · vitals done by Ifeoma", "Ready", "G Amara", tag="today"),
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "11:00 · chest pain · potassium 7.2, not acknowledged", "Urgent", "Open critical D15", tag="new"),
    patient_row("avatar-6.jpg", "Halima Sani", "MDR-9012-44", "11:20 · referred in from Wuse Clinic", "Waiting", "G Halima"),
    patient_row("avatar-3.jpg", "Grace Okeke", "MDR-8842-21", "11:40 · diabetes review · HbA1c back", "Waiting", "G Grace"),
], footer="The front desk and the admin built this list. Ask for a change rather than editing it.")

G1_DIFF = dgroup("What is different here", [
    drow("building-2", "Garki fills your day", sub="Reception books and the admin allocates. Your own booking link is off in this workplace", name="G diff book", chevron=False),
    drow("clock", "The department sets the slot length", sub="20 minutes here. In your own rooms you use 30", name="Open dept C2", chevron=False),
    drow("banknote", "The money is the hospital's", sub="No fees, no payouts, no subscription on this workplace", name="G diff money", chevron=False),
    drow("user-round-check", "Dr. Ade supervises this department", sub="She sees what you sign. Break-glass access is reported to her the same day", name="G diff sup", chevron=False),
], footer="Switch to your private practice in the top bar and all four change back. One account either way, one MDCN number.")

addx("Clinic", "G1-orgdoc",
    o_desk("Org · Doctor — G1 My Day", ("Clinic", "Thursday 14 August"),
        f'{G1_TILES}'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G1_QUEUE}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{G1_DIFF}'
        f'{dcta("Start with Amara","Start consult","stethoscope")}'
        f'{dbtn("See my roster","Open roster G2","calendar-days","ghost",full=True)}'
        f'{dbtn("Messages","Open messages G3","message-square-text","ghost",full=True)}</Frame></Frame>',
        "My day", dept="General practice", who=ORGDOC, badges=BADGES, persona="orgdoc"),
    o_head("My day", "Garki Medical Centre · 11 allocated", back=False,
           stats=[("11", "Allocated"), ("20 min", "Each"), ("3", "Results")]),
    pinned=G1_QUEUE,
    sections=[
      ("diff", "info", "What is different here", "Four things the hospital owns, not you", "4", None, G1_DIFF, None),
    ],
    foot=f'{dcta("Start with Amara","Start consult","stethoscope")}'
         f'{dbtn("See my roster","Open roster G2","calendar-days","ghost",full=True)}'
         f'{dbtn("Messages","Open messages G3","message-square-text","ghost",full=True)}',
    tab_items=o_tabs_for("orgdoc"), tab=0)

# ---------------- G2 the roster he is on, rather than the hours he sets
G2_WEEK = dgroup("Your sessions this week", [
    drow("calendar-days", "Monday · Outpatient clinic", value="08:00 – 13:00", sub="20 booked of 15 slots — overbooked by the desk", name="G ses mon", tone="warn"),
    drow("calendar-days", "Tuesday · Outpatient clinic", value="08:00 – 13:00", sub="12 booked", name="G ses tue"),
    drow("calendar-days", "Thursday · Outpatient clinic", value="08:00 – 13:00", sub="11 booked · today", name="G ses thu", tone="ok"),
    drow("moon", "Friday · On call", value="17:00 – 08:00", sub="Covering the whole facility overnight", name="G ses fri", tone="warn"),
], footer="The hospital's roster, not your availability. You ask; Dr. Ade or the admin answers.")

G2_ASK = dgroup("Ask for a change", [
    outcome_choice("calendar-x", "I cannot make a session", "Say which and why. Cover has to be found before it is approved, so ask early.", "G ask off", tone="warn"),
    outcome_choice("repeat", "Swap with a colleague", "Dr. Bello has agreed. Both of you confirm and the desk is told.", "G ask swap", tone="info"),
    outcome_choice("clock", "This session is overbooked", "Monday has 20 people in 15 slots. Somebody decided that; this tells them what it will do.", "G ask over", sel=True, tone="err"),
], footer="Answered by a person and recorded either way. Nothing here silently changes a day somebody is booked into.")

addx("Clinic", "G2-roster",
    o_desk("Org · Doctor — G2 My Roster", ("Clinic", "Roster"),
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G2_WEEK}{G2_ASK}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>'
        f'{dcard(eyerow("Days you will not be here") + range_cal(ranges=[("22","26","22–26 Aug · leave")], booked=("23","25"), name="G off"))}'
        f'{dcta("Send the request","Send roster ask G2","send")}</Frame></Frame>',
        "Roster", dept="General practice", who=ORGDOC, badges=BADGES, persona="orgdoc"),
    o_head("My roster", "Garki Medical Centre · 4 sessions",
           stats=[("4", "Sessions"), ("1", "Overbooked"), ("1", "On call")]),
    pinned=G2_WEEK,
    sections=[
      ("ask", "message-square-text", "Ask for a change", "Three ways, all answered by a person", "3", "warn", G2_ASK, None),
    ],
    foot=dcta("Send the request", "Send roster ask G2", "send"),
    tab_items=o_tabs_for("orgdoc"), tab=0)

# =====================================================================================
# TALKING TO EACH OTHER
# Godwin asked for this directly. Until now the only way one member of staff could reach
# another was a "Message" button on their profile, which is a dead end dressed as a feature:
# it assumes you know who is on duty. A department is a destination; a person is a guess.
# =====================================================================================
G3_LIST = dgroup("Your messages", [
    msg_row("avatar-3.jpg", "Nursing · Outpatient", "Ifeoma: Musa Ibrahim's BP is 168/104 on repeat — do you want him seen first?", "4 min", "G thread nursing", unread=True, channel="inapp"),
    msg_row("avatar-5.jpg", "Laboratory", "Sola: potassium 7.2 on Musa Ibrahim. I rang you at 09:44 — please acknowledge.", "18 min", "G thread lab", unread=True, channel="inapp"),
    msg_row("avatar-4.jpg", "Dr. Ade · Supervisor", "Two unsigned notes from Tuesday. Can you close them today?", "2 h", "G thread sup", channel="inapp"),
    msg_row("avatar-6.jpg", "Front desk", "Halima Sani has arrived early. Room 3 is free if you want her now.", "Yesterday", "G thread desk", channel="inapp"),
], footer="It goes to a department and whoever is on shift picks it up. A named person is how a question waits until Monday.")

G3_NEW = dgroup("Start a conversation", [
    drow("heart-pulse", "Nursing", sub="Two on duty · usually answers in 3 minutes", name="G new nursing", tone="ok"),
    drow("flask-conical", "Laboratory", sub="Three on duty · usually answers in 8 minutes", name="G new lab", tone="ok"),
    drow("pill", "Pharmacy", sub="One on duty · usually answers in 20 minutes", name="G new pharm", tone="warn"),
    drow("concierge-bell", "Front desk", sub="Four on duty", name="G new desk"),
    drow("user-round-check", "Dr. Ade — your supervisor", sub="A named person, deliberately", name="G new sup"),
], footer="Nothing clinical is decided in a message. Orders, results and referrals keep their own record.")

addx("Clinic", "G3-messages",
    o_desk("Org · Doctor — G3 Messages", ("Clinic", "Messages"),
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G3_LIST}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{G3_NEW}</Frame></Frame>',
        "Messages", dept="General practice", who=ORGDOC, badges=BADGES, persona="orgdoc"),
    o_head("Messages", "4 conversations · 2 unread", back=False,
           stats=[("2", "Unread"), ("3 min", "Nursing"), ("8 min", "Lab")]),
    pinned=G3_LIST,
    sections=[
      ("new", "message-circle-plus", "Start a conversation", "A department, not a person", "5", None, G3_NEW, None),
    ],
    tab_items=o_tabs_for("orgdoc"), tab=3)

G4_THREAD = dcard(
    f'<Frame w="fill" flex="row" gap={{12}} items="center" pb={{4}}>'
    f'<Frame w={{40}} h={{40}} rounded={{13}} bg="var:state/success-bg" flex="row" justify="center" '
    f'items="center">{I("heart-pulse",19,OK_IC)}</Frame>'
    f'<Frame grow={{1}} flex="col" gap={{2}}>{T(15,"semibold","var:text/strong","Nursing · Outpatient")}'
    f'{T(11,"regular","var:text/muted","Ifeoma Uche is on shift until 15:00 · Adaeze takes over after",w="fill")}</Frame>'
    f'{status_pill("live","On shift")}</Frame>' + hr()
    + audit_row("Ifeoma Uche · 09:52", "Musa Ibrahim's BP is 168/104 on repeat. He says the chest tightness is back. Do you want him seen before Amara?", "4 min")
    + audit_row("You · 09:54", "Yes — put him in room 3 now and tell Amara I will be ten minutes late.", "2 min")
    + audit_row("Ifeoma Uche · 09:55", "Done. Amara has been told and she is fine with it.", "1 min")
    + note("info", "Attached to Musa Ibrahim's visit, so the next doctor can see why the day changed order.", "info")
    + field("Reply", "message-square-text", "Type a message", ph=True))

G4_ABOUT = dgroup("About this patient", [
    patient_row("avatar-1.jpg", "Musa Ibrahim", "MDR-7714-02", "51 · chest pain · potassium 7.2 critical", "Open", "Open member B3", tag="new"),
    drow("siren", "A critical result is unacknowledged", sub="Potassium 7.2 · the laboratory rang at 09:44", name="Open critical D15", tone="err"),
    drow("heart-pulse", "Vitals taken 09:41", sub="168/104 · pulse 96 · by Ifeoma Uche", name="G4 vitals", tone="warn"),
], footer="Everything in this list is a record with its own screen. The conversation sits beside them, never instead of them.")

add("Clinic", "G4-thread",
    o_desk("Org · Doctor — G4 A Conversation", ("Clinic", "Nursing"),
        f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",17,N_IC)}'
        f'{T(13,"semibold","var:text/default","Messages")}</Frame>'
        f'<Frame w="fill" flex="row" gap={{16}} items="start">'
        f'<Frame grow={{1}} flex="col" gap={{14}}>{G4_THREAD}</Frame>'
        f'<Frame w={{344}} flex="col" gap={{14}}>{G4_ABOUT}</Frame></Frame>',
        "Messages", dept="General practice", who=ORGDOC, badges=BADGES, persona="orgdoc"),
    o_mob("Org · Doctor — G4 A Conversation · Mobile",
        o_head("Nursing", "Ifeoma Uche · on shift"),
        f'{G4_THREAD}{G4_ABOUT}', o_tabs_for("orgdoc"), 3))
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
    tab_items=o_tabs_for("desk"), tab=0)

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
    open(os.path.join(OUT, fn), "w").write(sanitize(normalise(jsx)))
    manifest.setdefault(page, []).append(fn)
open(os.path.join(OUT, "pages.json"), "w").write(json.dumps(manifest, indent=2))

# A renamed or deleted section leaves its .jsx behind, and the render script then draws a
# frame the builder no longer knows about — the linker never wires it and the audit reports
# a screen nobody can reach. Prune what this build did not write.
_written = {fn for _p, fn, _j in frames}
for _stale in sorted(set(os.listdir(OUT)) - _written):
    if _stale.endswith(".jsx"):
        os.remove(os.path.join(OUT, _stale))
        print("  pruned stale frame:", _stale)


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
  # ---- one entry per rail item per persona. The sweep is global by hotspot name, so these
  # names have to be unique per destination — see the note above NAV_BY_PERSONA in org_kit.
  "Btn Nav Desk Day":      NAMES["D12-desk"],
  "Btn Nav Desk Bookings": NAMES["B2-bookings"],
  "Btn Nav Desk Walkin":   NAMES["D13-walkin"],
  "Btn Nav Desk Members":  NAMES["B3-find"],
  "Btn Nav Desk Payments": NAMES["D14-checkin"],
  "Btn Nav Desk Messages": NAMES["H1-desk-messages"],
  "Btn Nav Dr Day":        NAMES["G1-orgdoc"],
  "Btn Nav Dr Patients":   NAMES["H7-dr-patients"],
  "Btn Nav Dr Results":    NAMES["H8-dr-results"],
  "Btn Nav Dr Roster":     NAMES["G2-roster"],
  "Btn Nav Dr Messages":   NAMES["G3-messages"],
  "Btn Nav Nurse Queue":   NAMES["D1-nursing"],
  "Btn Nav Nurse Vitals":  NAMES["D2-vitals"],
  "Btn Nav Nurse Orders":  NAMES["H9-nurse-orders"],
  "Btn Nav Nurse Members": NAMES["B3-find"],
  "Btn Nav Nurse Messages":NAMES["H2-nurse-messages"],
  "Btn Nav Lab Queue":     NAMES["D5-lab-queue"],
  "Btn Nav Lab Result":    NAMES["D7-lab-result"],
  "Btn Nav Lab Critical":  NAMES["D15-critical"],
  "Btn Nav Lab Problem":   NAMES["D8-lab-problem"],
  "Btn Nav Lab Messages":  NAMES["H3-lab-messages"],
  "Btn Nav Pharm Queue":   NAMES["D9-pharmacy"],
  "Btn Nav Pharm Stock":   NAMES["H10-pharm-stock"],
  "Btn Nav Pharm Sub":     NAMES["D11-substitute"],
  "Btn Nav Pharm Messages":NAMES["H4-pharm-messages"],
  "Btn Nav Img Worklist":  NAMES["D16-imaging"],
  "Btn Nav Img Report":    NAMES["D18-report"],
  "Btn Nav Img Rooms":     NAMES["H11-img-rooms"],
  "Btn Nav Img Messages":  NAMES["H5-img-messages"],
  "Btn Nav Bill Money":    NAMES["D19-billing"],
  "Btn Nav Bill Owing":    NAMES["D20-payment"],
  "Btn Nav Bill Claims":   NAMES["D21-claims"],
  "Btn Nav Bill Messages": NAMES["H6-bill-messages"],
}

# A rail item that leads nowhere is worse than a missing one, so prove every one of them
# resolves before the build is allowed to finish.
for _p, _rail in NAV_BY_PERSONA.items():
    for _ic, _label, _hot in _rail:
        assert ("Btn " + _hot) in NAVMAP, f"{_p} rail item '{_label}' has no destination"

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
 ("D7-lab-result","Btn Crit flag","D15-critical"),("D5-lab-queue","Btn Crit waiting","D15-critical"),
 ("D15-critical","Btn Close critical D15","D5-lab-queue"),("D15-critical","Btn Back","D7-lab-result"),
 ("D15-critical","Btn Crit escalate","F7-critical"),
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
 # ---- imaging: worklist, safety stop, report
 ("B1-today","Btn Dept imaging","D16-imaging"),("B1-today","Btn Dept billing","D19-billing"),
 ("C1-departments","Btn Dept imaging","D16-imaging"),("C1-departments","Btn Dept billing","D19-billing"),
 ("D16-imaging","Btn Img halima","D17-prepare"),("D16-imaging","Btn Prepare Img halima","D17-prepare"),
 ("D16-imaging","Btn Img musa","D17-prepare"),("D16-imaging","Btn Prepare Img musa","D17-prepare"),
 ("D16-imaging","Btn Img amara","D17-prepare"),("D16-imaging","Btn Prepare Img amara","D17-prepare"),
 ("D16-imaging","Btn Img grace","D17-prepare"),("D16-imaging","Btn Prepare Img grace","D17-prepare"),
 ("D16-imaging","Btn Img fatima","D17-prepare"),("D16-imaging","Btn Prepare Img fatima","D17-prepare"),
 ("D16-imaging","Btn Open report D18","D18-report"),("D16-imaging","~Btn Stat imgdone","D18-report"),
 ("D17-prepare","Btn Back","D16-imaging"),("D17-prepare","Btn Start study D17","D18-report"),
 ("D17-prepare","Btn Open messages G3","G3-messages"),
 ("D18-report","Btn Back","D16-imaging"),("D18-report","Btn Sign report D18","D16-imaging"),
 ("D18-report","~Btn Rep critical","D15-critical"),
 # ---- billing: the till, a payment, the claims
 ("D19-billing","~Btn Open owing D20","D20-payment"),("D19-billing","Btn Open claims D21","D21-claims"),
 ("D19-billing","Btn Owe grace","D20-payment"),("D19-billing","Btn Owe halima","D20-payment"),
 ("D19-billing","Btn Owe musa","D20-payment"),("D19-billing","~Btn Stat taken","D19-billing"),
 ("D19-billing","~Btn Stat recon","D19-billing"),
 ("D20-payment","Btn Back","D19-billing"),("D20-payment","Btn Save payment D20","D19-billing"),
 ("D20-payment","Btn Open plan D20","D19-billing"),
 ("D21-claims","Btn Claim fatima","D21-claims"),("D21-claims","Btn Answer claim D21","D21-claims"),
 ("D21-claims","Btn Open payment D20","D20-payment"),("D21-claims","Btn Claim grace","D21-claims"),
 ("D21-claims","Btn Chase claim grace","D21-claims"),("D21-claims","Btn Claim emeka","D21-claims"),
 ("D21-claims","Btn Claim blessing","D21-claims"),("D21-claims","Btn Tell member D21","D21-claims"),
 ("D21-claims","Btn New claim D21","D20-payment"),("D21-claims","~Btn Why preauth","D14-checkin"),
 # ---- the doctor inside the organisation
 ("G1-orgdoc","Btn Open roster G2","G2-roster"),("G1-orgdoc","Btn Open messages G3","G3-messages"),
 ("G1-orgdoc","Btn Open critical D15","D15-critical"),("G1-orgdoc","Btn Open dept C2","C2-department"),
 ("G1-orgdoc","~Btn Stat allocated","G1-orgdoc"),("G1-orgdoc","~Btn Stat length","C2-department"),
 ("G1-orgdoc","Btn G Amara","B3-find"),("G1-orgdoc","Btn G Halima","B3-find"),
 ("G1-orgdoc","Btn G Grace","B3-find"),("G1-orgdoc","Btn Start consult","B3-find"),
 ("G2-roster","Btn Send roster ask G2","G1-orgdoc"),("G2-roster","~Btn Back","G1-orgdoc"),
 ("G3-messages","Btn G thread nursing","G4-thread"),("G3-messages","Btn G thread lab","G4-thread"),
 ("G3-messages","Btn G thread sup","G4-thread"),("G3-messages","Btn G thread desk","G4-thread"),
 ("G3-messages","Btn G new nursing","G4-thread"),("G3-messages","Btn G new lab","G4-thread"),
 ("G3-messages","Btn G new pharm","G4-thread"),("G3-messages","Btn G new desk","G4-thread"),
 ("G3-messages","Btn G new sup","G4-thread"),
 ("G4-thread","Btn Back","G3-messages"),("G4-thread","Btn Open member B3","B3-find"),
 ("G4-thread","Btn Open critical D15","D15-critical"),
 # ---- reports: four screens under one overview
 ("F4-reports","Btn Open patients F8","F8-patients"),("F4-reports","Btn Open clinicians F9","F9-clinicians"),
 ("F4-reports","Btn Open depts F10","F10-departments"),("F4-reports","Btn Open claims D21","D21-claims"),
 ("F4-reports","Btn Open critical F7","F7-critical"),("F4-reports","~Btn Export report F4","F4-reports"),
 ("F8-patients","Btn Back","F4-reports"),
 ("F9-clinicians","Btn Back","F4-reports"),("F9-clinicians","Btn Open critical F7","F7-critical"),
 ("F10-departments","Btn Back","F4-reports"),("F10-departments","Btn Person emeka","C6-person"),
 # ---- the admin's onboarding entry points, and the new per-persona destinations
 ("B1-today","Btn Open people C4","C4-people"),("B1-today","Btn Open plan A4","A4-plan"),
 ("H1-desk-messages","Btn Desk thread dr","G4-thread"),("H1-desk-messages","Btn Desk thread nursing","G4-thread"),
 ("H1-desk-messages","Btn Desk thread billing","G4-thread"),
 ("H2-nurse-messages","Btn Nurse thread dr","G4-thread"),("H2-nurse-messages","Btn Nurse thread lab","G4-thread"),
 ("H2-nurse-messages","Btn Nurse thread desk","G4-thread"),
 ("H3-lab-messages","Btn Lab thread dr","G4-thread"),("H3-lab-messages","Btn Lab thread nursing","G4-thread"),
 ("H3-lab-messages","Btn Lab thread desk","G4-thread"),
 ("H4-pharm-messages","Btn Pharm thread dr","G4-thread"),("H4-pharm-messages","Btn Pharm thread desk","G4-thread"),
 ("H4-pharm-messages","Btn Pharm thread billing","G4-thread"),
 ("H5-img-messages","Btn Img thread dr","G4-thread"),("H5-img-messages","Btn Img thread rad","G4-thread"),
 ("H5-img-messages","Btn Img thread nursing","G4-thread"),
 ("H6-bill-messages","Btn Bill thread desk","G4-thread"),("H6-bill-messages","Btn Bill thread admin","G4-thread"),
 ("H6-bill-messages","Btn Bill thread pharm","G4-thread"),
 ("H7-dr-patients","Btn H7 amara","B3-find"),("H7-dr-patients","Btn H7 halima","B3-find"),
 ("H7-dr-patients","Btn H7 grace","B3-find"),("H7-dr-patients","Btn H7 fatima","B3-find"),
 ("H7-dr-patients","Btn Open critical D15","D15-critical"),("H7-dr-patients","~Btn H7 unsigned","G1-orgdoc"),
 ("H7-dr-patients","~Btn H7 followups","G1-orgdoc"),
 ("H8-dr-results","Btn Open critical D15","D15-critical"),("H8-dr-results","Btn H8 grace","D7-lab-result"),
 ("H8-dr-results","Btn H8 halima","D18-report"),
 ("H9-nurse-orders","Btn Record SO musa","D3-administer"),("H9-nurse-orders","Btn SO musa","D3-administer"),
 ("H9-nurse-orders","Btn Record SO blessing","D3-administer"),("H9-nurse-orders","Btn SO blessing","D3-administer"),
 ("H9-nurse-orders","Btn Record SO grace","D2-vitals"),("H9-nurse-orders","Btn SO grace","D2-vitals"),
 ("H9-nurse-orders","Btn Open escalate D4","D4-escalate"),
 ("H10-pharm-stock","Btn Open sub D11","D11-substitute"),("H10-pharm-stock","~Btn H10 metformin","H10-pharm-stock"),
 ("H11-img-rooms","~Btn H11 report","H11-img-rooms"),
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
                   "Btn Dept clinic", "Btn Dept nursing", "Btn Dept lab", "Btn Dept pharmacy", "Btn Dept desk",
                   "Btn Dept imaging", "Btn Dept billing", "Btn Open roster G2", "Btn Open messages G3",
                   "Btn Open patients F8", "Btn Open clinicians F9", "Btn Open depts F10",
                   "Btn Open report D18", "Btn Open owing D20", "Btn Open claims D21", "Btn Open payment D20"])
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
 f"  const ONE_PAGE = {json.dumps(ONE_PAGE)};\n"
 f"  const Y0 = {BAND_Y0['org']};\n"
 + LAYOUT_JS +
 "  return { linked, navLinked, stayOnScreen: stay, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT, "link-org.js"), "w").write(linker)

# The content cut is only worth anything if it holds. Report the prose budget on every build —
# a screen that drifts back over shows up here rather than at the next review.
try:
    from prose_budget import report as _prose_report
    _prose_report(['org'])
except Exception as _e:      # never let a reporting tool break a build
    print("  prose budget unavailable:", _e)


# A repair pass for a canvas that was rendered before normalise.py existed. It fixes the
# spacer frames and the centred text in place, so a page does not have to be deleted and
# re-rendered to pick the fix up — and so anything changed by hand in Figma survives.
open(os.path.join(OUT, "fix-layout.js"), "w").write(
    fix_script([re.search(r'name="([^"]+)"', _j).group(1) for _p, _f, _j in frames],
               "Organisation"))

_files = [fn for _p in ORDER for fn in manifest[_p]]
open(os.path.join(OUT, "render-org.ps1"), "w").write(
    one_page_ps1("Organisation", _files, "link-org.js"))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} screen links "
      f"· {len(nav_jobs)} nav links · {len(CMP)} component states")
for p_, fs in manifest.items(): print(f"  {p_}: {len(fs)}")
