#!/usr/bin/env python3
"""Approximate renderer: figma-ds-cli JSX -> HTML, for offline visual QA before Figma.

Usage:  python3 tools/figma/preview_bundle.py <bundle-dir> [out.html]

Not the real CLI — but it uses the same auto-layout rules, so it catches the two things
that actually broke in Figma: rows that overflow their frame, and mobile screens taller
than 844. Images are referenced relatively so the file stays small.
"""
import os, re, sys, html as ihtml
import xml.etree.ElementTree as ET

BUNDLE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(BUNDLE, "preview.html")

tok = {}
for line in open(os.path.join(BUNDLE, "DESIGN.md")):
    m = re.match(r'\|\s*([a-z0-9]+/[a-z0-9-]+)\s*\|\s*(#[0-9A-Fa-f]{6})', line)
    if m: tok[m.group(1)] = m.group(2)

def color(v):
    if v is None: return None
    if v.startswith("var:"): return tok.get(v[4:], "#FF00FF")
    return v

WEIGHT = {"bold": "700", "semibold": "600", "medium": "500", "regular": "400"}
JUS = {"center": "center", "between": "space-between", "start": "flex-start", "end": "flex-end"}
ITEMS = {"start": "flex-start", "center": "center", "end": "flex-end"}

def num(v):
    v = v[3:] if v.startswith("js:") else v
    try: return float(v)
    except: return None

def icon_svg(name, size, col):
    bare = name.replace("lucide:", "")
    f = os.path.join(BUNDLE, "assets/icon-cache", "lucide_" + re.sub(r'[^a-z0-9]', '_', bare, flags=re.I) + ".svg")
    if not os.path.exists(f): return f'<span style="width:{size}px;height:{size}px;display:inline-block"></span>'
    svg = open(f).read()
    svg = re.sub(r'width="[^"]*"', '', svg, 1); svg = re.sub(r'height="[^"]*"', '', svg, 1)
    svg = svg.replace("<svg", f'<svg style="width:{size}px;height:{size}px;flex:0 0 auto;color:{col}" ', 1)
    return svg

def style_for(tag, a, parent_dir):
    s = []
    def has(k): return k in a
    def g(k): return a.get(k)
    if has("flex"):
        s.append("display:flex")
        s.append("flex-direction:" + ("row" if g("flex") == "row" else "column"))
    mydir = g("flex") if has("flex") else None
    if has("gap"): s.append(f"gap:{num(g('gap'))}px")
    if has("rowGap"): s.append(f"row-gap:{num(g('rowGap'))}px")
    if g("wrap") == "wrap": s.append("/* wrap ignored by the CLI */")
    if has("justify"): s.append("justify-content:" + JUS.get(g("justify"), "flex-start"))
    s.append("align-items:" + (ITEMS.get(g("items"), "flex-start") if has("items") else "flex-start"))
    for dim, prop in (("w", "width"), ("h", "height")):
        if has(dim):
            v = g(dim)
            if v == "fill":
                if (dim == "w" and parent_dir == "row") or (dim == "h" and parent_dir == "column"):
                    s.append("flex:1 1 0;min-width:0;min-height:0")
                elif dim == "w": s.append("width:100%")
                else: s.append("align-self:stretch")
            elif v == "hug":
                s.append(f"{prop}:fit-content")
            else:
                n = num(v)
                if n is not None:
                    s.append(f"{prop}:{n}px")
                    # only lock flex on the parent's main axis — a fixed height on a column
                    # inside a row must still be allowed to grow horizontally
                    if (dim == "w" and parent_dir == "row") or (dim == "h" and parent_dir != "row"):
                        s.append("flex:0 0 auto")
    if has("minH"): s.append(f"min-height:{num(g('minH'))}px")
    if has("grow"): s.append(f"flex:{num(g('grow'))} 1 0;min-width:0;min-height:0")
    if has("p"): s.append(f"padding:{num(g('p'))}px")
    if has("px"): s.append(f"padding-left:{num(g('px'))}px;padding-right:{num(g('px'))}px")
    if has("py"): s.append(f"padding-top:{num(g('py'))}px;padding-bottom:{num(g('py'))}px")
    for k, prop in (("pt", "padding-top"), ("pr", "padding-right"), ("pb", "padding-bottom"), ("pl", "padding-left")):
        if has(k): s.append(f"{prop}:{num(g(k))}px")
    if has("bg"): s.append("background-color:" + color(g("bg")))
    if has("image"):
        s.append(f"background-image:url('{g('image')}')")
        s.append("background-size:cover;background-position:center")
    if has("stroke"):
        w = num(g("strokeWidth")) or 1
        s.append(f"border:{w}px solid " + color(g("stroke")))
    if has("rounded"):
        r = num(g("rounded")) or 0
        s.append(f"border-radius:{9999 if r >= 999 else r}px")
    if g("overflow") == "hidden": s.append("overflow:hidden")
    if tag == "Text":
        if has("size"): s.append(f"font-size:{num(g('size'))}px")
        s.append("font-weight:" + WEIGHT.get(g("weight"), "400"))
        s.append("font-family:'Inter','DejaVu Sans',sans-serif")
        s.append("line-height:1.35")
        if has("color"): s.append("color:" + color(g("color")))
        if has("align"): s.append("text-align:" + g("align"))
        s.append("margin:0;white-space:pre-wrap;overflow-wrap:anywhere")
    return ";".join(x for x in s if x), mydir

def render(el, parent_dir=None):
    tag = el.tag; a = el.attrib
    st, mydir = style_for(tag, a, parent_dir)
    if tag == "Icon":
        return icon_svg(a.get("name", ""), num(a.get("size", "16")) or 16, color(a.get("color", "#000000")))
    if tag == "Image":
        return f'<img src="{a.get("image","")}" style="{st};object-fit:cover" />'
    if tag in ("Rect", "Ellipse"):
        if tag == "Ellipse": st += ";border-radius:9999px"
        return f'<div style="{st}"></div>'
    if tag == "Text":
        return f'<div style="{st}">{ihtml.escape(el.text or "")}</div>'
    inner = "".join(render(c, mydir) for c in el)
    return f'<div style="{st}">{inner}</div>'

def preprocess(src):
    return re.sub(r'(\w+)=\{([^}]*)\}', lambda m: f'{m.group(1)}="js:{m.group(2).strip()}"', src)

frames = []
for fn in sorted(os.listdir(BUNDLE)):
    if not fn.endswith(".jsx"): continue
    src = preprocess(open(os.path.join(BUNDLE, fn)).read())
    try:
        root = ET.fromstring(src)
    except ET.ParseError as e:
        print("PARSE ERR", fn, e); continue
    w = root.attrib.get("w", "")
    frames.append((fn, root.attrib.get("name", fn), num(w[3:] if w.startswith("js:") else w) or 1440, render(root)))

cards = "".join(
    f'<div class="wrap"><div class="cap">{fn} — {ihtml.escape(nm)}</div>'
    f'<div class="frame" data-file="{fn}" data-w="{int(w)}" style="width:{int(w)}px">{h}</div></div>'
    for fn, nm, w, h in frames)

open(OUT, "w").write(f"""<!doctype html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#c9d2da;font-family:'Inter','DejaVu Sans',sans-serif}}
.wrap{{padding:24px}} .cap{{font-size:12px;color:#26323d;margin-bottom:6px;font-weight:600}}
img{{display:block}}
</style></head><body>{cards}</body></html>""")
print(f"wrote {OUT} with {len(frames)} frames")
