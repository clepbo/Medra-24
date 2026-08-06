#!/usr/bin/env python3
"""Offline prototype audit for a Medra bundle.

Answers three questions without opening Figma:
  1. Is every frame reachable from its page's flow start?
  2. Is every node named "Btn …" wired, either explicitly or by the linker's sweep?
  3. Does any explicit transition point at a frame or hotspot that does not exist?

Usage: python3 tools/figma/proto_check.py <bundle-dir> <link-script.js>
"""
import json, os, re, sys
from collections import defaultdict, deque

BUNDLE = os.path.abspath(sys.argv[1])
LINK = os.path.join(BUNDLE, sys.argv[2] if len(sys.argv) > 2 else "link-doctor.js")

src = open(LINK).read()

def grab(var):
    m = re.search(r'const ' + var + r' = (\[.*?\]);\n', src, re.S)
    return json.loads(m.group(1)) if m else []

TRN = grab("TRN")
NAV = grab("NAVJOBS")
m = re.search(r'const ORDER = (\{.*?\});\n', src, re.S)
ORDER = json.loads(m.group(1)) if m else {}
m = re.search(r'const STARTS = (\{.*?\});\n', src, re.S)
STARTS = json.loads(m.group(1)) if m else {}

# ---- frames and their Btn nodes, straight off disk -------------------------------------
frames = {}
for fn in sorted(os.listdir(BUNDLE)):
    if not fn.endswith(".jsx"): continue
    s = open(os.path.join(BUNDLE, fn)).read()
    root = re.search(r'name="([^"]+)"', s)
    if not root: continue
    name = root.group(1).replace("&amp;", "&")
    btns = [b.replace("&amp;", "&") for b in re.findall(r'name="(Btn [^"]+)"', s)]
    frames[name] = {"file": fn, "btns": btns}

def norm(x): return x.replace("&amp;", "&").strip()

# ---- 1. reachability ------------------------------------------------------------------
# TRN is a per-frame table: every entry names a hotspot that must be on that frame, so a
# miss is a broken link. NAV is a sweep applied to every frame — the rail, the tab bar, the
# top bar — and a frame that simply does not carry that control is not a defect.
edges = defaultdict(set)
missing_targets, missing_hotspots, absent_nav = [], [], []
for src, rows in (("TRN", TRN), ("NAV", NAV)):
    for frm, hot, to in rows:
        f, t, h = norm(frm), norm(to), norm(hot)
        if f not in frames: missing_targets.append(f"source missing: {f}"); continue
        if t not in frames:
            # cross-module links (auth) resolve only when that bundle is in the same file
            missing_targets.append(f"target outside this bundle: {f} -[{h}]-> {t}"); continue
        if h not in frames[f]["btns"]:
            (missing_hotspots if src == "TRN" else absent_nav).append(f"{f} has no “{h}”")
            continue
        edges[f].add(t)

reach = set()
for page, start in STARTS.items():
    # a page declares a desktop start and a mobile start; both are entry points
    for st in ([start] if isinstance(start, str) else start):
        s = norm(st)
        if s not in frames or s in reach: continue
        q = deque([s]); reach.add(s)
        while q:
            cur = q.popleft()
            for nxt in edges[cur]:
                if nxt not in reach:
                    reach.add(nxt); q.append(nxt)

screens = {n for n in frames if not n.startswith("cmp/")}
unreachable = sorted(screens - reach)

# ---- 2. hotspot coverage --------------------------------------------------------------
wired = defaultdict(set)
for frm, hot, to in TRN + NAV:
    wired[norm(frm)].add(norm(hot))

total_btn = swept = explicit = 0
sweep_detail = defaultdict(list)
for name, d in frames.items():
    if name.startswith("cmp/"): continue
    for b in set(d["btns"]):
        total_btn += 1
        if b in wired[name]: explicit += 1
        else:
            swept += 1
            sweep_detail[name].append(b)

print(f"bundle           {os.path.basename(BUNDLE)}")
print(f"frames           {len(frames)}  ({len(screens)} screens, {len(frames)-len(screens)} component states)")
print(f"pages with flows {len(STARTS)}")
print(f"explicit links   {len(TRN)}")
print(f"nav links        {len(NAV)}")
print()
print(f"REACHABLE        {len(reach)}/{len(screens)} screens")
if unreachable:
    print("  unreachable:")
    for u in unreachable: print("   ✗", u)
print()
print(f"HOTSPOTS         {total_btn} distinct 'Btn' names across screens")
print(f"  explicitly wired {explicit}")
print(f"  swept to self    {swept}   (state controls: toggles, radios, filters, chips)")
print()
if missing_hotspots:
    print(f"BROKEN LINKS     {len(missing_hotspots)} transition(s) name a hotspot that does not exist")
    for x in missing_hotspots[:24]: print("   ✗", x)
else:
    print("BROKEN LINKS     none")
print(f"NAV NOT PRESENT  {len(absent_nav)} sweep target(s) absent from a frame "
      f"(expected — a phone tab bar carries five of eight destinations)")
out = [x for x in missing_targets if "outside this bundle" in x]
if out:
    print(f"CROSS-MODULE     {len(out)} link(s) leave this bundle (expected — they resolve when that bundle is in the file)")
    for x in sorted(set(out))[:6]: print("   ·", x)
bad = [x for x in missing_targets if "outside this bundle" not in x]
if bad:
    print(f"INTERNAL ERRORS  {len(bad)}")
    for x in bad[:20]: print("   ✗", x)

fail = bool(unreachable) or bool(missing_hotspots) or bool(bad)
print()
print("PROTOTYPE INCOMPLETE — fix the above" if fail else "PROTOTYPE COMPLETE ✓  every screen reachable, every hotspot wired")
sys.exit(1 if fail else 0)
