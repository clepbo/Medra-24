#!/usr/bin/env python3
"""Approximate renderer: figma-ds-cli JSX -> HTML, for offline visual QA (not the real CLI)."""
import os, re, html as ihtml, base64
import xml.etree.ElementTree as ET

BUNDLE="/home/user/Medra-24/figma/medra-ds"
OUT=os.path.join(BUNDLE,"preview.html")

_datacache={}
def datauri(rel):
    if rel in _datacache: return _datacache[rel]
    p=os.path.join(BUNDLE,rel)
    if not os.path.exists(p): _datacache[rel]=rel; return rel
    b=base64.b64encode(open(p,"rb").read()).decode()
    uri=f"data:image/png;base64,{b}"; _datacache[rel]=uri; return uri

# token map from DESIGN.md
tok={}
for line in open(os.path.join(BUNDLE,"DESIGN.md")):
    m=re.match(r'\|\s*([a-z0-9]+/[a-z0-9-]+)\s*\|\s*(#[0-9A-Fa-f]{6})',line)
    if m: tok[m.group(1)]=m.group(2)

def color(v):
    if v is None: return None
    if v.startswith("var:"): return tok.get(v[4:], "#FF00FF")
    return v

WEIGHT={"bold":"700","semibold":"600","medium":"500","regular":"400"}
JUS={"center":"center","between":"space-between","start":"flex-start","end":"flex-end"}
ITEMS={"start":"flex-start","center":"center","end":"flex-end"}

def num(v):
    v=v[3:] if v.startswith("js:") else v
    try: return float(v)
    except: return None

def icon_svg(name,size,col):
    bare=name.replace("lucide:","")
    f=os.path.join(BUNDLE,"assets/icon-cache","lucide_"+re.sub(r'[^a-z0-9]','_',bare,flags=re.I)+".svg")
    if not os.path.exists(f): return f'<span style="width:{size}px;height:{size}px"></span>'
    svg=open(f).read()
    svg=re.sub(r'width="[^"]*"','',svg,1); svg=re.sub(r'height="[^"]*"','',svg,1)
    svg=svg.replace("<svg",f'<svg style="width:{size}px;height:{size}px;color:{col}" ',1)
    return svg

def style_for(tag,a,parent_dir):
    s=[]; disp_flex=False
    def has(k): return k in a
    def g(k): return a.get(k)
    # layout
    if has("flex"):
        disp_flex=True; s.append("display:flex")
        s.append("flex-direction:"+("row" if g("flex")=="row" else "column"))
    mydir = g("flex") if has("flex") else None
    if has("gap"): s.append(f"gap:{num(g('gap'))}px")
    if has("rowGap"): s.append(f"row-gap:{num(g('rowGap'))}px")
    if g("wrap")=="wrap": s.append("flex-wrap:wrap")
    if has("justify"): s.append("justify-content:"+JUS.get(g("justify"),"flex-start"))
    if has("items"): s.append("align-items:"+ITEMS.get(g("items"),"flex-start"))
    # sizing
    if has("grow"): s.append(f"flex:{num(g('grow'))} 1 0")
    for dim,prop in (("w","width"),("h","height")):
        if has(dim):
            v=g(dim)
            if v=="fill":
                if (dim=="w" and parent_dir=="row") or (dim=="h" and parent_dir=="column"):
                    s.append("flex:1 1 0")
                elif dim=="w": s.append("width:100%")
                else: s.append("align-self:stretch")
            elif v=="hug":
                s.append(f"{prop}:fit-content")
            else:
                n=num(v)
                if n is not None: s.append(f"{prop}:{n}px")
    if has("minH"): s.append(f"min-height:{num(g('minH'))}px")
    # padding
    if has("p"): s.append(f"padding:{num(g('p'))}px")
    if has("px"): s.append(f"padding-left:{num(g('px'))}px;padding-right:{num(g('px'))}px")
    if has("py"): s.append(f"padding-top:{num(g('py'))}px;padding-bottom:{num(g('py'))}px")
    for k,prop in (("pt","padding-top"),("pr","padding-right"),("pb","padding-bottom"),("pl","padding-left")):
        if has(k): s.append(f"{prop}:{num(g(k))}px")
    # paint
    if has("bg"): s.append("background-color:"+color(g("bg")))
    if has("image"):
        s.append(f"background-image:url('{datauri(g('image'))}')")
        s.append("background-size:cover;background-position:center")
    if has("stroke"):
        w=num(g("strokeWidth")) or 1
        s.append(f"border:{w}px solid "+color(g("stroke")))
    if has("rounded"):
        r=num(g("rounded")) or 0; s.append(f"border-radius:{9999 if r>=999 else r}px")
    if g("overflow")=="hidden": s.append("overflow:hidden")
    if g("position")=="absolute":
        s.append("position:absolute")
        for k in ("top","right","bottom","left"):
            if has(k): s.append(f"{k}:{num(g(k))}px")
    # text
    if tag=="Text":
        if has("size"): s.append(f"font-size:{num(g('size'))}px")
        s.append("font-weight:"+WEIGHT.get(g("weight"),"400"))
        s.append("font-family:'Inter','DejaVu Sans',sans-serif")
        s.append("line-height:1.35")
        if has("color"): s.append("color:"+color(g("color")))
        if has("align"): s.append("text-align:"+g("align"))
        s.append("margin:0;white-space:pre-wrap")
    return ";".join(s), mydir

def render(el,parent_dir=None):
    tag=el.tag; a=el.attrib
    st,mydir=style_for(tag,a,parent_dir)
    if tag=="Icon":
        return icon_svg(a.get("name",""), num(a.get("size","16")) or 16, color(a.get("color","#000000")))
    if tag=="Image":
        return f'<img src="{datauri(a.get("image",""))}" style="{st};object-fit:contain" />'
    if tag in ("Rect","Ellipse"):
        if tag=="Ellipse": st+=";border-radius:9999px"
        return f'<div style="{st}"></div>'
    if tag=="Text":
        txt=ihtml.escape(el.text or "")
        return f'<div style="{st}">{txt}</div>'
    # Frame
    inner="".join(render(c,mydir) for c in el)
    return f'<div style="{st}">{inner}</div>'

def preprocess(src):
    # name={expr} -> name="js:expr"
    src=re.sub(r'(\w+)=\{([^}]*)\}', lambda m: f'{m.group(1)}="js:{m.group(2).strip()}"', src)
    return src

frames=[]
for fn in sorted(os.listdir(BUNDLE)):
    if not fn.endswith(".jsx"): continue
    src=preprocess(open(os.path.join(BUNDLE,fn)).read())
    try:
        root=ET.fromstring(src)
    except ET.ParseError as e:
        print("PARSE ERR",fn,e); continue
    frames.append((fn,render(root)))

cards="".join(f'<div class="wrap"><div class="cap">{fn}</div><div id="f{i}" class="frame">{h}</div></div>'
              for i,(fn,h) in enumerate(frames))
open(OUT,"w").write(f"""<!doctype html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#c9d2da;font-family:'Inter','DejaVu Sans',sans-serif}}
.wrap{{padding:24px}} .cap{{font-size:12px;color:#333;margin-bottom:6px}}
.frame{{width:1440px}}
img{{display:block}}
</style></head><body>{cards}</body></html>""")
print(f"wrote {OUT} with {len(frames)} frames")
