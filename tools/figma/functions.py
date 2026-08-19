#!/usr/bin/env python3
"""What a person can actually DO on Medra, and which screens do it.

The file has been organised by *module* since the first render — member, doctor, organisation,
auth — because that is how it was built. That is a producer's order. It answers "where does this
screen live in the codebase" and not the question anybody actually arrives with, which is
**"show me how somebody books a visit"**.

So this is the other index: persona → function → the screens that carry it, end to end, in the
order a person meets them. It is the single source of truth for two generated artefacts, so they
cannot drift apart:

    docs/Functions.md              the readable inventory
    figma/arrange-by-function.js   the script that lays the Figma page out this way

**A screen may belong to more than one function**, and several do — a lab result is part of
"order a test and get it back" for the doctor and part of "see what happened" for the member.
The first function that claims a screen owns the original frame; every later claim gets a copy.
That is deliberate, and the report says which screens were copied and why.

    python3 tools/figma/functions.py            # regenerate both artefacts
    python3 tools/figma/functions.py --check    # verify every id resolves, change nothing
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =====================================================================================
# THE MAP
#
# (persona, one-line description) -> [(function, why it exists, [screen ids…]), …]
#
# A screen id is "<bundle>/<file stem>", e.g. "member/B1-slot". The order inside a function is
# the order a person meets those screens, not alphabetical — that ordering is the whole value
# of this index, so it is worth keeping right when screens are added.
# =====================================================================================
PERSONAS = [

 ("Member", "A person using Medra for their own care, and their family's", [

  ("Join Medra",
   "From never having heard of it to a working account. Verify once; the device is trusted after that.",
   ["auth/E1-onb1", "auth/E2-onb2", "auth/E3-onb3", "auth/E4-welcome", "auth/E5-role",
    "auth/M1-create", "auth/M2-otp", "auth/M3-name", "auth/M4-about", "auth/M5-health",
    "auth/M9-success", "auth/M6-login", "auth/M7-unlock", "auth/M8-help"]),

  ("Find a doctor",
   "Search, narrow, and read a profile well enough to choose. The first-run home screen is here because an empty home is where finding starts.",
   ["member/H2-home-empty", "member/H1-home", "member/S1-results", "member/S2-filters",
    "member/S3-empty", "member/P1-profile"]),

  ("Book a visit",
   "Pick a time, see the price before agreeing to it, pay, and get a confirmation you can show at a desk.",
   ["member/P1-profile", "member/B1-slot", "member/B2-taken", "member/B3-review",
    "member/B4-payment", "member/C1-confirmed"]),

  ("Attend a visit",
   "What happens between booking and being seen — including the video path and the two ways a visit does not happen.",
   ["member/V1-visits", "member/V4-visit", "member/V3-visits-empty", "member/W0-join",
    "member/W1-precall", "member/W2-incall", "member/W4-lost", "member/W3-callend",
    "member/V5-reschedule", "member/V6-cancel", "member/V7-cancelled"]),

  ("See what happened",
   "Everything a visit produces, from the member's side: the note, the results, the trend.",
   ["member/V2-past", "member/R2-note", "member/R3-lab", "member/R4-vitals",
    "member/R10-summary"]),

  ("Keep my records",
   "The record is the member's, travels with them, and can be added to by hand — most Nigerian history is on paper.",
   ["member/R1-records", "member/R9-records-empty", "member/R7-upload", "member/R8-added",
    "member/R10-summary"]),

  ("Share my records, and take it back",
   "Consent, in both directions. Every screen here is one a member has to be able to act on under pressure.",
   ["member/R5-share", "member/R11-approve", "member/R6-access", "member/R12-shared"]),

  ("Take my medicines",
   "What to take, when, and how to get more without a trip to the clinic for a piece of paper.",
   ["member/M1-meds", "member/M2-med", "member/M4-reminders", "member/M3-refill",
    "member/M5-meds-empty"]),

  ("Care for my family",
   "A child's records until they are eighteen, and an adult's only with their say-so.",
   ["member/P3-dependants", "member/P4-add-dependant", "member/P3b-family"]),

  ("Manage my account",
   "Identity, devices, what Medra is allowed to send, and the two screens that end the relationship.",
   ["member/P0-profile", "member/P2-details", "member/P5-security", "member/P6-notifs",
    "member/P7-language", "member/P8-privacy", "member/P9-delete", "member/P9b-delete-confirm"]),

  ("Be told things",
   "Notifications, and the preference screen that decides which of them ever arrive.",
   ["member/N0-panel", "member/N1-notifs", "member/N2-notifs-empty", "member/P6-notifs"]),

  ("When something breaks",
   "The three states every screen can fall into. Kept together because they are reviewed together.",
   ["member/X1-loading", "member/X2-offline", "member/X3-error"]),
 ]),

 ("Doctor — own practice", "A clinician working for themselves, not inside an organisation", [

  ("Join and get verified",
   "MDCN is checked by a person, which is the slowest thing Medra does and the reason anybody trusts it.",
   ["auth/D1-create", "auth/D2-otp", "auth/D3-password", "auth/D4-pending", "auth/D5-profile",
    "auth/D10-success", "auth/D6-login", "auth/D7-2fa", "auth/D8-forgot", "auth/D9-reset",
    "doctor/G1-checklist", "doctor/G2-verification"]),

  ("Run my day",
   "The queue, the person in front of you, and the four things that go wrong in a clinic day.",
   ["doctor/K1-today", "doctor/K9-more", "doctor/K2-requests", "doctor/K3-late",
    "doctor/K5-outcome", "doctor/K10-critical", "doctor/X2-empty"]),

  ("See a patient",
   "Read the file, hold the consultation, and sign it. Nothing reaches the member until it is signed.",
   ["doctor/K4-file", "doctor/C1-room", "doctor/C2-templates", "doctor/C10-virtual",
    "doctor/C7-sign", "doctor/C8-signed", "doctor/C9-drafts"]),

  ("Prescribe",
   "Including the interaction check, which is the one place the software is allowed to stop a doctor.",
   ["doctor/C3-prescribe", "doctor/P6-refills"]),

  ("Order a test and get it back",
   "The longest chain in the product: order, route it, watch it, read it, release it.",
   ["doctor/C4-tests", "doctor/C11-route", "doctor/C12-order", "doctor/C5-upload",
    "doctor/P7-results", "doctor/P8-result", "doctor/K10-critical"]),

  ("Send a member somewhere else",
   "A referral inside Medra, and the single-use link for the laboratory that is not on it.",
   ["doctor/C6-refer", "doctor/C13-link", "doctor/C14-consent", "doctor/C15-links"]),

  ("Look after my patients between visits",
   "The work that happens when nobody is in the room.",
   ["doctor/P1-patients", "doctor/P2-record", "doctor/P3-access", "doctor/P4-followups",
    "doctor/P5-messages", "doctor/P6-refills"]),

  ("Manage my schedule",
   "Availability is a promise: if a slot shows on Medra it is genuinely open.",
   ["doctor/K6-week", "doctor/K7-availability", "doctor/K8-timeoff"]),

  ("Run my practice",
   "Fees, channels, where I practise, what I am paid, and what I pay.",
   ["doctor/S1-profile", "doctor/S2-fees", "doctor/S3-virtual", "doctor/S4-contact",
    "doctor/S7-practice", "doctor/S5-earnings", "doctor/S6-billing", "doctor/S8-security",
    "doctor/X1-locked"]),

  ("Grow my practice",
   "The three screens that decide whether a doctor stays on the platform.",
   ["doctor/R1-insights", "doctor/R2-reviews", "doctor/R3-link", "doctor/G3-invite"]),

  ("When something breaks",
   "",
   ["doctor/X6-loading", "doctor/X4-offline", "doctor/X5-error", "doctor/X3-notifications"]),
 ]),

 ("Organisation admin", "The person who owns the whole building — and the only one who can create a seat", [

  ("Register the organisation",
   "RC number, practice licence, size, plan. Checked by a person before it can take a public booking.",
   ["auth/I1-register", "auth/I2-documents", "auth/I3-orgsize", "auth/I4-plan", "auth/I5-otp",
    "auth/I6-password", "auth/I7-pending", "auth/I11-success", "auth/I8-admin-login",
    "auth/I9-forgot", "auth/I10-reset"]),

  ("Set the organisation up",
   "Branches, seats and the public profile — everything that has to be true before anybody works.",
   ["org/A1-setup", "org/A2-verify", "org/A3-branches", "org/A4-plan", "org/A5-profile",
    "org/X2-unverified"]),

  ("Onboard a department or a member of staff",
   "The admin's defining job. A department is the unit; permissions follow it, never the person.",
   ["org/C1-departments", "org/C3-add-dept", "org/C2-department", "org/C4-people",
    "org/C5-invite", "org/C6-person", "org/C7-roles", "org/X1-seats"]),

  ("Run the day across the organisation",
   "Every department, every branch, and the four bookings nobody has been allocated to.",
   ["org/B1-today", "org/B2-bookings", "org/B3-find", "org/X4-empty"]),

  ("Read the numbers",
   "The four questions an administrator actually arrives with, one screen each.",
   ["org/F4-reports", "org/F8-patients", "org/F9-clinicians", "org/F10-departments"]),

  ("Govern who sees what",
   "Access is per episode of care. This is the group that makes a shared record safe to hand around a hospital.",
   ["org/F1-access", "org/F2-audit", "org/F3-compliance", "org/C7-roles", "org/F7-critical"]),

  ("Settings and money",
   "",
   ["org/F5-settings", "org/F6-billing", "org/X3-locked"]),

  ("When something breaks",
   "",
   ["org/X7-loading", "org/X5-offline", "org/X6-error"]),
 ]),

 ("Front desk", "Registration, check-in and payment — the busiest seat in the building", [

  ("Join the organisation as staff",
   "Shared by every organisation persona: the invitation an admin sent, through to a working seat.",
   ["auth/S1-invite", "auth/S2-verify", "auth/S3-details", "auth/S4-registration",
    "auth/S5-undertaking", "auth/S6-password", "auth/S7-pending", "auth/S8-ready",
    "auth/S9-workplace", "auth/S10-expired"]),

  ("Run the front desk day",
   "Who is here, who is late, who has not paid.",
   ["org/D12-desk", "org/B2-bookings", "org/X5-offline"]),

  ("Register somebody who just walked in",
   "Most Nigerian clinic visits start this way, not with a booking.",
   ["org/D13-walkin", "org/B3-find"]),

  ("Check in and take payment",
   "",
   ["org/D14-checkin"]),

  ("Talk to the rest of the building",
   "",
   ["org/H1-desk-messages", "org/G4-thread"]),
 ]),

 ("Doctor — inside an organisation", "The same clinician, in a workplace they do not own", [

  ("Add a workplace to my account",
   "One account, two workplaces. The MDCN number is the doctor's, so nothing is re-verified.",
   ["auth/S9-workplace", "auth/S1-invite", "auth/S8-ready"]),

  ("My day here",
   "A list the doctor did not build — reception booked it and the admin allocated it.",
   ["org/G1-orgdoc", "org/H7-dr-patients"]),

  ("Results waiting on me",
   "",
   ["org/H8-dr-results", "org/D15-critical"]),

  ("The roster I am on",
   "The hospital's roster, not the doctor's availability. They ask; a named person answers.",
   ["org/G2-roster"]),

  ("Talk to the team",
   "A message goes to a department, and whoever is on shift picks it up.",
   ["org/G3-messages", "org/G4-thread"]),
 ]),

 ("Nurse", "Vitals, injections, observations — and the escalation that must never wait", [

  ("Work my queue",
   "Ordered by when the doctor needs them, not by when they arrived.",
   ["org/D1-nursing"]),

  ("Record vitals",
   "",
   ["org/D2-vitals"]),

  ("Administer and record",
   "Five rights, shortened to the four a queue actually gets wrong.",
   ["org/D3-administer"]),

  ("Escalate something out of range",
   "Two minutes to the first doctor, then the duty doctor automatically. Never a message that waits.",
   ["org/D4-escalate"]),

  ("Standing orders",
   "A doctor's instruction that repeats, and the four things nursing may do without asking.",
   ["org/H9-nurse-orders"]),

  ("Talk to the team",
   "",
   ["org/H2-nurse-messages", "org/G4-thread"]),
 ]),

 ("Laboratory", "Samples in, structured results out — and the value that has to be phoned", [

  ("Work the order queue",
   "",
   ["org/D5-lab-queue", "org/D6-lab-order"]),

  ("Enter a result",
   "A form rather than a paragraph, because prose cannot be trended or compared.",
   ["org/D7-lab-result"]),

  ("Reject a bad sample",
   "In a paper laboratory this happens silently. Here it always tells somebody.",
   ["org/D8-lab-problem"]),

  ("Handle a critical value",
   "The one result that cannot be sent. It reaches a named human by voice, with a read-back.",
   ["org/D15-critical", "org/F7-critical", "doctor/K10-critical"]),

  ("Talk to the team",
   "",
   ["org/H3-lab-messages", "org/G4-thread"]),
 ]),

 ("Pharmacy", "Dispensing against a prescription, and what happens when you cannot", [

  ("Work the prescription queue",
   "Somebody standing at the counter comes first, whatever order they arrived in.",
   ["org/D9-pharmacy"]),

  ("Dispense",
   "",
   ["org/D10-dispense"]),

  ("When you cannot dispense",
   "A substitution is a proposal, never a decision — it goes back to the prescriber.",
   ["org/D11-substitute"]),

  ("Watch the shelf",
   "A count you keep, not a warehouse system: so you can tell a member before they queue.",
   ["org/H10-pharm-stock"]),

  ("Talk to the team",
   "",
   ["org/H4-pharm-messages", "org/G4-thread"]),
 ]),

 ("Imaging", "The department where the patient has to be present, prepared and safe", [

  ("Work the worklist",
   "Ordered by appointment, because an image needs the person, the room and the machine at once.",
   ["org/D16-imaging"]),

  ("Check it is safe to scan",
   "The only screen in Medra that refuses to move.",
   ["org/D17-prepare"]),

  ("Report a study",
   "A radiologist's sentence, not a picture. Signed by name, amendable only by a second version.",
   ["org/D18-report"]),

  ("Rooms and machines",
   "",
   ["org/H11-img-rooms"]),

  ("Talk to the team",
   "",
   ["org/H5-img-messages", "org/G4-thread"]),
 ]),

 ("Billing", "Running the money, which is a different job from taking it at the desk", [

  ("The money today",
   "Cash is the only line Medra cannot verify itself, so it is the one counted against a drawer.",
   ["org/D19-billing"]),

  ("Take a payment",
   "Part payment is a first-class case. Entries are append-only.",
   ["org/D20-payment"]),

  ("Chase an insurance claim",
   "Where the revenue actually leaks: submitted, queried, never resubmitted.",
   ["org/D21-claims"]),

  ("Talk to the team",
   "",
   ["org/H6-bill-messages", "org/G4-thread"]),
 ]),

 ("Referrals", "Sending a member elsewhere and receiving one — it spans several personas, so it is its own group", [

  ("Refer a member out",
   "",
   ["org/E1-outbound", "org/E2-create", "org/E3-sent", "doctor/C6-refer"]),

  ("Receive a referral",
   "Accepting books it and tells them both. Declining tells them too — silence is not available.",
   ["org/E4-inbound", "org/E5-inbound-detail"]),

  ("Send work to somebody not on Medra",
   "A scoped, single-use, consent-gated link. The address is a random token, never a Medra ID.",
   ["doctor/C13-link", "doctor/C14-consent", "doctor/C15-links", "org/E6-links",
    "member/R11-approve", "member/R12-shared"]),
 ]),

 ("Outside party", "Somebody with no Medra account, doing one job from a link that dies after it", [

  ("Do one job from a single-use link",
   "Four screens, no account, no training, no way back in. Finishable on a phone in a waiting room.",
   ["org/E7-ext-notice", "org/E8-ext-task", "org/E9-ext-upload", "org/E10-ext-done",
    "org/E11-ext-expired"]),
 ]),
]

# =====================================================================================
BAND = re.compile(r'name="([^"]+)"')


def resolve():
    """Every id → (the desktop frame name, every frame name in that screen's family).

    The family is read from the files rather than guessed from the desktop name, because two
    screens do not follow the convention: `H2 First Visit (empty state)` has a mobile frame
    called `H2 First Visit · Mobile`, and `R3 Lab Results & Diagnostics` has `R3 Lab Result ·
    Mobile`. A prefix match silently drops both — the dry run caught it, which is the whole
    reason the dry run exists. Reading the actual files cannot drift.

    Fails loudly on a typo: a map that silently skips a screen is worse than no map."""
    names, fams, missing = {}, {}, []
    for bundle in ("member", "doctor", "org", "auth"):
        d = os.path.join(ROOT, "figma", "medra-" + bundle)
        if not os.path.isdir(d):
            continue
        stems = sorted(fn for fn in os.listdir(d) if fn.endswith("-d.jsx"))
        for fn in stems:
            stem = fn[:-6]
            key = f"{bundle}/{stem}"
            fam = []
            for part in sorted(os.listdir(d)):
                if not part.endswith(".jsx"):
                    continue
                if part == stem + "-d.jsx" or part == stem + "-m.jsx" \
                        or part.startswith(stem + "-m-"):
                    with open(os.path.join(d, part), encoding="utf-8") as fh:
                        m = BAND.search(fh.read())
                    if m:
                        fam.append(m.group(1).replace("&amp;", "&"))
            if fam:
                names[key] = fam[0] if fn.endswith("-d.jsx") else fam[0]
                with open(os.path.join(d, fn), encoding="utf-8") as fh:
                    names[key] = BAND.search(fh.read()).group(1).replace("&amp;", "&")
                fams[key] = fam
    used = []
    for _p, _d, funcs in PERSONAS:
        for _f, _w, ids in funcs:
            for i in ids:
                used.append(i)
                if i not in names:
                    missing.append(i)
    return names, fams, missing, used


def build():
    names, fams, missing, used = resolve()
    if missing:
        print("UNRESOLVED SCREEN IDS — fix the map before generating:")
        for m in sorted(set(missing)):
            print("   ", m)
        return None
    seen, plan = set(), []
    for persona, pdesc, funcs in PERSONAS:
        for func, why, ids in funcs:
            rows = []
            for i in ids:
                rows.append({"id": i, "name": names[i], "frames": fams[i], "copy": i in seen})
                seen.add(i)
            plan.append({"persona": persona, "personaDesc": pdesc,
                         "function": func, "why": why, "screens": rows})
    orphans = sorted(set(names) - set(used))
    return {"plan": plan, "names": names, "fams": fams, "orphans": orphans,
            "counts": {"screens": len(names), "placed": len(set(used)),
                       "functions": len(plan), "personas": len(PERSONAS),
                       "copies": sum(1 for g in plan for s in g["screens"] if s["copy"])}}


# =====================================================================================
# ARTEFACT 1 — the readable inventory
# =====================================================================================
def emit_md(d):
    c = d["counts"]
    out = [
"# What you can do on Medra",
"",
"Every function in the product, grouped by the person who performs it, with the screens that",
"carry it end to end. Generated from `tools/figma/functions.py` — edit the map there, not this",
"file.",
"",
f"**{c['personas']} personas · {c['functions']} functions · {c['screens']} screens**, every one",
f"placed. {c['copies']} screens appear in more than one function, because they genuinely do two",
"jobs — a lab result is part of *order a test and get it back* for the doctor and part of *see",
"what happened* for the member. Those are marked **·copy** below; the first function to claim a",
"screen owns the original.",
"",
"Screens are listed in the order a person meets them, not alphabetically. That ordering is the",
"point of this index — keep it right when screens are added.",
"",
"---",
"",
"## Contents",
"",
]
    for persona, pdesc, funcs in PERSONAS:
        anchor = persona.lower().replace(" — ", "--").replace(" ", "-").replace(",", "")
        out.append(f"- [{persona}](#{anchor}) — {len(funcs)} functions")
    out += ["", "---", ""]
    for persona, pdesc, funcs in PERSONAS:
        out += [f"## {persona}", "", f"*{pdesc}*", ""]
        for func, why, ids in funcs:
            rows = next(g for g in d["plan"] if g["persona"] == persona and g["function"] == func)
            out.append(f"### {func}")
            if why:
                out += ["", why]
            out += ["", f"| # | Screen | |", "|---:|---|---|"]
            for n, s in enumerate(rows["screens"], 1):
                mark = " **·copy**" if s["copy"] else ""
                out.append(f"| {n} | {s['name']} | `{s['id']}`{mark} |")
            out.append("")
    out += [
"---",
"",
"## The screens that do two jobs",
"",
"These are the ones that will be duplicated when the Figma page is arranged this way. Each is",
"listed under the function that owns the original first, then everywhere it is copied to.",
"",
]
    firsts, copies = {}, {}
    for g in d["plan"]:
        for s in g["screens"]:
            key = s["name"]
            if s["copy"]:
                copies.setdefault(key, []).append(f"{g['persona']} → {g['function']}")
            else:
                firsts[key] = f"{g['persona']} → {g['function']}"
    out += ["| Screen | Original lives under | Also copied into |", "|---|---|---|"]
    for k in sorted(copies):
        out.append(f"| {k} | {firsts.get(k,'—')} | {' · '.join(copies[k])} |")
    out.append("")
    return "\n".join(out)


# =====================================================================================
# ARTEFACT 2 — the script that lays Figma out this way
# =====================================================================================
JS_HEAD = r"""// Medra — arrange the page by FUNCTION rather than by module.
//
//     figma-cli run .\arrange-by-function.js
//
// GENERATED by tools/figma/functions.py. Do not hand-edit — regenerate.
//
// WHAT IT DOES. The page is currently laid out by module, in four bands, because that is how it
// was built. This re-lays it out by what a person can DO: a banner for each persona, a banner
// for each function under it, and beneath each function the screens that carry it, in the order
// somebody meets them. A screen that does two jobs is COPIED into the second one.
//
// READ THIS BEFORE RUNNING IT
//
//  1. **Render and link first.** This moves frames the linkers created. Running a linker
//     afterwards re-lays that module's band out and undoes the arrangement. Order is:
//     render-all.ps1 → check the linker reports → then this.
//
//  2. **It moves originals and clones copies.** Every screen keeps exactly one original, which
//     is the frame carrying the prototype wiring. Copies are clones with their reactions
//     stripped, so the prototype is not silently doubled — they are there to read, not to click.
//
//  3. **It is idempotent.** Re-running it removes the banners it made last time and rebuilds
//     the arrangement from the current frames. Clones from a previous run are removed too, so
//     copies do not multiply.
//
//  4. **Nothing is deleted except its own output.** A frame it cannot find is reported, not
//     invented; a frame on the page it does not know about is left exactly where it is.

const PLAN = __PLAN__;

const BAND = { personaH: 220, funcH: 130, gapX: 140, gapY: 90, colW: 1440, padTop: 120 };
const MARK_P = "§ PERSONA — ";
const MARK_F = "§ FUNCTION — ";
const MARK_C = " (copy)";

(async () => {
  const page = figma.currentPage;
  const report = { personas: 0, functions: 0, moved: 0, copied: 0, missing: [], strays: 0, cleared: 0 };

  await figma.loadFontAsync({ family: "Inter", style: "Bold" });
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });

  // ---- 1. clear what a previous run of THIS script made, and nothing else
  for (const n of [...page.children]) {
    const nm = n.name || "";
    if (nm.startsWith(MARK_P) || nm.startsWith(MARK_F) || nm.endsWith(MARK_C)) {
      n.remove(); report.cleared++;
    }
  }

  // ---- 2. index what is on the page now
  // Frame names come back with "&" sometimes escaped and sometimes not, depending on how they
  // were written — the linkers already normalise for exactly this reason, so do the same here
  // rather than reporting half a dozen screens missing over an ampersand.
  const norm = s => (s || "").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim();
  const index = {};
  for (const f of page.children) (index[norm(f.name)] ||= []).push(f);
  // Match on the exact frame list the builder produced, never on a name prefix. Two screens do
  // not follow the naming convention — "H2 First Visit (empty state)" has a mobile frame called
  // "H2 First Visit · Mobile" — and a prefix match drops both without ever saying so.
  const family = (wanted) => {
    const out = [];
    for (const w of wanted) for (const f of (index[norm(w)] || [])) out.push(f);
    return out;
  };

  const banner = (text, sub, w, big) => {
    const fr = figma.createFrame();
    fr.name = (big ? MARK_P : MARK_F) + text;
    fr.resize(Math.max(w, 1440), big ? BAND.personaH : BAND.funcH);
    fr.fills = [{
      type: "GRADIENT_LINEAR",
      gradientTransform: [[1, 0, 0], [0, 1, 0]],
      gradientStops: [
        { position: 0, color: { r: 0.059, g: 0.133, b: 0.200, a: 1 } },   // #0F2233
        { position: 1, color: { r: 0.141, g: 0.373, b: 0.533, a: 1 } },   // #245F88
      ],
    }];
    fr.layoutMode = "VERTICAL";
    fr.primaryAxisAlignItems = "CENTER";
    fr.counterAxisAlignItems = "MIN";
    fr.paddingLeft = 56; fr.paddingRight = 56; fr.itemSpacing = 10;
    fr.clipsContent = true;

    const t = figma.createText();
    t.fontName = { family: "Inter", style: "Bold" };
    t.characters = big ? text.toUpperCase() : text;
    t.fontSize = big ? 62 : 34;
    t.letterSpacing = { unit: "PIXELS", value: big ? 2 : 0 };
    t.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
    fr.appendChild(t);

    if (sub) {
      const s = figma.createText();
      s.fontName = { family: "Inter", style: "Regular" };
      s.characters = sub;
      s.fontSize = big ? 20 : 16;
      s.fills = [{ type: "SOLID", color: { r: 0.70, g: 0.80, b: 0.88 } }];
      fr.appendChild(s);
    }
    page.appendChild(fr);
    return fr;
  };

  // ---- 3. lay it out
  let y = BAND.padTop, lastPersona = null;

  for (const g of PLAN) {
    // gather every frame this function needs, before drawing anything
    const blocks = [];
    for (const s of g.screens) {
      const fam = family(s.frames || [s.name]);
      if (!fam.length) { report.missing.push(`${g.persona} → ${g.function}: ${s.name}`); continue; }
      blocks.push({ frames: fam, copy: s.copy, name: s.name });
    }
    if (!blocks.length) continue;

    const width = blocks.length * BAND.colW + (blocks.length - 1) * BAND.gapX;

    if (g.persona !== lastPersona) {
      y += lastPersona ? 260 : 0;
      banner(g.persona, g.personaDesc, Math.max(width, 3000), true).y = y;
      y += BAND.personaH + 90;
      lastPersona = g.persona; report.personas++;
    }

    const sub = g.why ? g.why : `${blocks.length} screen${blocks.length === 1 ? "" : "s"}`;
    const b = banner(g.function, sub, width, false);
    b.x = 0; b.y = y;
    y += BAND.funcH + 60;
    report.functions++;

    let x = 0, tallest = 0;
    for (const blk of blocks) {
      let cy = y;
      for (const src of blk.frames) {
        let node = src;
        if (blk.copy) {
          node = src.clone();
          node.name = src.name + MARK_C;
          // A clone carries the original's reactions. Two frames answering the same click is
          // how a prototype quietly becomes untrustworthy, so the copy is made inert.
          try { node.reactions = []; } catch (e) {}
          page.appendChild(node);
          report.copied++;
        } else {
          report.moved++;
        }
        node.x = x; node.y = cy;
        cy += node.height + 40;
      }
      tallest = Math.max(tallest, cy - y);
      x += BAND.colW + BAND.gapX;
    }
    y += tallest + BAND.gapY;
  }

  // ---- 4. anything left where it was
  const known = new Set();
  for (const g of PLAN) for (const s of g.screens)
    for (const w of (s.frames || [s.name])) known.add(norm(w));
  const strayNames = [];
  for (const f of page.children) {
    const nm = norm(f.name);
    if (nm.startsWith(MARK_P) || nm.startsWith(MARK_F) || nm.endsWith(norm(MARK_C))) continue;
    if (!known.has(nm) && !nm.startsWith("cmp/")) { report.strays++; strayNames.push(nm); }
  }
  report.strayExamples = strayNames.slice(0, 12);

  return report;
})()
"""


def emit_js(d):
    slim = [{"persona": g["persona"], "personaDesc": g["personaDesc"], "function": g["function"],
             "why": g["why"],
             "screens": [{"name": s["name"], "frames": s["frames"], "copy": s["copy"]}
                         for s in g["screens"]]}
            for g in d["plan"]]
    return JS_HEAD.replace("__PLAN__", json.dumps(slim, ensure_ascii=False))


if __name__ == "__main__":
    d = build()
    if d is None:
        sys.exit(1)
    c = d["counts"]
    if "--check" in sys.argv:
        print(f"OK — {c['personas']} personas · {c['functions']} functions · "
              f"{c['placed']}/{c['screens']} screens placed · {c['copies']} copies")
        print(f"orphans: {len(d['orphans'])}")
        sys.exit(0)
    with open(os.path.join(ROOT, "docs", "Functions.md"), "w", encoding="utf-8") as fh:
        fh.write(emit_md(d))
    with open(os.path.join(ROOT, "figma", "arrange-by-function.js"), "w", encoding="utf-8") as fh:
        fh.write(emit_js(d))
    print(f"docs/Functions.md and figma/arrange-by-function.js — "
          f"{c['personas']} personas · {c['functions']} functions · {c['placed']} screens · {c['copies']} copies")
    if d["orphans"]:
        print("screens in no function:", ", ".join(d["orphans"]))
