#!/usr/bin/env python3
"""Keep each bundle's offline icon cache honest.

`render-*.ps1` copies `assets/icon-cache/*.svg` into figma-ds-cli's own cache before it renders
anything, so an icon that is not in that folder does not render — it fails quietly, mid-run,
after a hundred frames are already on the canvas. This scans the JSX a builder just wrote,
finds every `lucide:<name>` it actually uses, and fetches the ones that are missing.

    python3 tools/figma/icons.py                 # all four bundles
    python3 tools/figma/icons.py medra-org       # one

It only ever adds files. An icon that is cached but no longer used costs nothing and may be
used again by the next screen, so nothing is deleted.
"""
import os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUNDLES = ["medra-member", "medra-doctor", "medra-org", "medra-auth"]
CDN = "https://cdn.jsdelivr.net/npm/lucide-static@1.26.0/icons/{}.svg"
USE = re.compile(r'lucide:([a-z0-9\-]+)')


def used_in(bundle):
    names = set()
    for dirpath, _, files in os.walk(os.path.join(ROOT, "figma", bundle)):
        if "icon-cache" in dirpath:
            continue
        for f in files:
            if f.endswith((".jsx", ".js", ".ps1")):
                with open(os.path.join(dirpath, f), encoding="utf-8", errors="ignore") as fh:
                    names |= set(USE.findall(fh.read()))
    return names


def sync(bundle):
    cache = os.path.join(ROOT, "figma", bundle, "assets", "icon-cache")
    if not os.path.isdir(cache):
        return None
    os.makedirs(cache, exist_ok=True)
    need = used_in(bundle)
    added, failed = [], []
    for n in sorted(need):
        path = os.path.join(cache, "lucide_" + n.replace("-", "_") + ".svg")
        if os.path.exists(path):
            continue
        try:
            with urllib.request.urlopen(CDN.format(n), timeout=30) as r:
                svg = r.read()
            if b"<svg" not in svg:
                raise ValueError("not an svg")
            with open(path, "wb") as fh:
                fh.write(svg)
            added.append(n)
        except Exception as e:
            failed.append((n, str(e).split("\n")[0]))
    return len(need), added, failed


if __name__ == "__main__":
    targets = sys.argv[1:] or BUNDLES
    bad = 0
    for b in targets:
        r = sync(b)
        if r is None:
            print(f"{b:<15} no icon-cache folder — skipped")
            continue
        used, added, failed = r
        line = f"{b:<15} {used} icons used"
        if added:
            line += f" · fetched {len(added)}: " + ", ".join(added)
        else:
            line += " · cache already complete"
        print(line)
        for n, why in failed:
            print(f"                MISSING {n} — {why}")
            bad += 1
    sys.exit(1 if bad else 0)
