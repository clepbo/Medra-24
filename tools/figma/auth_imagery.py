#!/usr/bin/env python3
"""On-brand imagery for the Medra Auth module (offline; swap for real photos later)."""
import os, math, io
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import cairosvg

IMG = "/home/user/Medra-24/figma/medra-auth/assets/img"
LOGO = "/home/user/Medra-24/brand/svg/medra-logo-white.svg"
os.makedirs(IMG, exist_ok=True)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

NAVY_DEEP=(15,34,51); NAVY=(27,58,91); BLUE=(36,95,136); BLUEL=(47,139,172); TEAL=(57,176,207); TEALB=(90,196,222)

def panel(w, h, stops, angle, name, rings=True, ring_color=(255,255,255), ring_alpha=26, logo=True, logo_alpha=32):
    """Duotone gradient panel with faint concentric 'pulse' rings + faint logo."""
    base = Image.new("RGB", (w, h))
    px = base.load()
    rad = math.radians(angle); dx, dy = math.cos(rad), math.sin(rad)
    corners=[(0,0),(w,0),(0,h),(w,h)]; projs=[cx*dx+cy*dy for cx,cy in corners]
    pmin,pmax=min(projs),max(projs)
    def col(t):
        for i in range(len(stops)-1):
            p0,c0=stops[i]; p1,c1=stops[i+1]
            if p0<=t<=p1: return lerp(c0,c1,(t-p0)/(p1-p0) if p1>p0 else 0)
        return stops[-1][1]
    for y in range(h):
        for x in range(w):
            px[x,y]=col(((x*dx+y*dy)-pmin)/(pmax-pmin))
    over = Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(over)
    if rings:
        cx,cy = int(w*0.72), int(h*0.32)
        for r in range(60, int(max(w,h)*1.1), 74):
            d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=ring_color+(ring_alpha,), width=3)
    base = Image.alpha_composite(base.convert("RGBA"), over)
    if logo:
        png = cairosvg.svg2png(url=LOGO, output_width=int(w*0.5))
        lg = Image.open(io.BytesIO(png)).convert("RGBA")
        a = lg.split()[3].point(lambda v: int(v*logo_alpha/255))
        lg.putalpha(a)
        base.alpha_composite(lg, (int(w*0.5-lg.width*0.5), int(h*0.62)))
    base.convert("RGB").save(os.path.join(IMG, name))

# Persona brand panels (desktop left column) — portrait
panel(1000,1300,[(0,NAVY_DEEP),(0.5,BLUE),(1,TEAL)],55,"panel-patient.png")
panel(1000,1300,[(0,NAVY_DEEP),(0.55,NAVY),(1,BLUEL)],55,"panel-doctor.png")
panel(1000,1300,[(0,(11,26,40)),(0.6,NAVY),(1,BLUE)],55,"panel-institution.png")
# Mobile hero bands — landscape
panel(1200,620,[(0,NAVY_DEEP),(0.5,BLUE),(1,TEAL)],35,"band-patient.png")
panel(1200,620,[(0,NAVY_DEEP),(0.55,NAVY),(1,BLUEL)],35,"band-doctor.png")
panel(1200,620,[(0,(11,26,40)),(0.6,NAVY),(1,BLUE)],35,"band-institution.png")
# Success / confirmation soft image
panel(1200,900,[(0,(20,50,72)),(0.6,BLUEL),(1,TEALB)],48,"success.png", ring_alpha=34)
# Neutral abstract (duotone tint) for form-side accents
panel(900,900,[(0,NAVY),(1,BLUEL)],60,"accent.png", ring_alpha=20, logo=False)

print("wrote:", ", ".join(sorted(os.listdir(IMG))))
