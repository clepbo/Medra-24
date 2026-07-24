#!/usr/bin/env python3
"""Generate all image assets for the Medra Figma design-system bundle."""
import os, shutil, math
from PIL import Image, ImageDraw, ImageFont
import cairosvg

BUNDLE = "/home/user/Medra-24/figma/medra-ds"
LOGO   = os.path.join(BUNDLE, "assets/logo")
IMG    = os.path.join(BUNDLE, "assets/img")
SVGSRC = "/home/user/Medra-24/brand/svg"
for d in (LOGO, IMG): os.makedirs(d, exist_ok=True)

NAVY="#1b3a5b"; NAVY_DEEP="#0f2233"; BLUE="#245f88"; BLUEL="#2f8bac"; TEAL="#39b0cf"; TEALB="#3bb6d2"

def font(sz, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, sz)

# ---- 1. logo PNGs from the vector masters ----
logo_map = {
    "medra-logo-primary.svg":     "logo-primary.png",
    "medra-logo-white.svg":       "logo-white.png",
    "medra-logo-navy.svg":        "logo-navy.png",
    "medra-logo-teal.svg":        "logo-teal.png",
    "medra-logo-black.svg":       "logo-black.png",
    "medra-lockup-horizontal.svg":"lockup-horizontal.png",
    "medra-lockup-stacked.svg":   "lockup-stacked.png",
    "medra-appicon.svg":          "appicon.png",
}
for s, out in logo_map.items():
    cairosvg.svg2png(url=os.path.join(SVGSRC, s),
                     write_to=os.path.join(LOGO, out), output_width=1200)
# hero placeholder (until 3D uploaded) — large primary on transparent
cairosvg.svg2png(url=os.path.join(SVGSRC,"medra-logo-primary.svg"),
                 write_to=os.path.join(LOGO,"hero.png"), output_width=1600)
cairosvg.svg2png(url=os.path.join(SVGSRC,"medra-logo-white.svg"),
                 write_to=os.path.join(LOGO,"hero-white.png"), output_width=1600)

def lerp(a,b,t):
    ah=a.lstrip('#'); bh=b.lstrip('#')
    return tuple(round(int(ah[i:i+2],16)+(int(bh[i:i+2],16)-int(ah[i:i+2],16))*t) for i in (0,2,4))

def gradient(w,h,stops,angle=0,name="grad.png"):
    """stops: list of (pos,hex). angle 0 = left->right, 90 = top->bottom, 45 diagonal."""
    im = Image.new("RGB",(w,h))
    px = im.load()
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    # projection range
    corners=[(0,0),(w,0),(0,h),(w,h)]
    projs=[cx*dx+cy*dy for cx,cy in corners]
    pmin,pmax=min(projs),max(projs)
    def color_at(t):
        for i in range(len(stops)-1):
            p0,c0=stops[i]; p1,c1=stops[i+1]
            if p0<=t<=p1:
                lt=(t-p0)/(p1-p0) if p1>p0 else 0
                return lerp(c0,c1,lt)
        return lerp(stops[0][1],stops[-1][1],0 if t<stops[0][0] else 1)
    for y in range(h):
        for x in range(w):
            t=((x*dx+y*dy)-pmin)/(pmax-pmin)
            px[x,y]=color_at(t)
    im.save(os.path.join(IMG,name))

# ---- 2. gradient panels ----
STOPS=[(0.0,NAVY),(0.42,BLUE),(0.72,BLUEL),(1.0,TEAL)]
gradient(1600,400,STOPS,angle=0,  name="gradient-h.png")     # horizontal band
gradient(1200,1200,STOPS,angle=55,name="gradient-diag.png")  # diagonal square
gradient(1600,900,[(0.0,NAVY_DEEP),(0.5,NAVY),(1.0,BLUEL)],angle=60,name="gradient-hero.png")
gradient(600,600,[(0.0,TEAL),(1.0,BLUEL)],angle=90,name="gradient-teal.png")
# swatch strips for single colors (used as bg images where handy)

# ---- 3. abstract "pulse" texture band (navy with faint ECG line) ----
def pulse_band(w,h,bg,line,name):
    im=Image.new("RGB",(w,h),bg); d=ImageDraw.Draw(im)
    midy=h//2; amp=h*0.16; step=w/8
    pts=[]
    x=0
    import random; random.seed(3)
    while x<w:
        pts.append((x,midy)); x+=step*0.6
        pts.append((x,midy-amp*0.2)); x+=step*0.12
        pts.append((x,midy+amp)); x+=step*0.1
        pts.append((x,midy-amp*1.4)); x+=step*0.1
        pts.append((x,midy+amp*0.3)); x+=step*0.1
        pts.append((x,midy)); x+=step*0.5
    d.line(pts,fill=line,width=4,joint="curve")
    im.save(os.path.join(IMG,name))
pulse_band(1600,300,NAVY_DEEP,"#2f8bac","pulse-navy.png")

# ---- 4. avatars (doctor placeholders) ----
def avatar(name, initials, c1, c2):
    S=400; im=Image.new("RGB",(S,S)); px=im.load()
    a=lerp(c1,c2,0);
    for y in range(S):
        for x in range(S):
            px[x,y]=lerp(c1,c2,(x+y)/(2*S))
    d=ImageDraw.Draw(im)
    f=font(150,bold=True)
    bb=d.textbbox((0,0),initials,font=f)
    d.text(((S-(bb[2]-bb[0]))/2-bb[0],(S-(bb[3]-bb[1]))/2-bb[1]),initials,font=f,fill="#ffffff")
    im.save(os.path.join(IMG,name))
avatar("avatar-1.png","NA",NAVY,BLUEL)
avatar("avatar-2.png","FA",BLUEL,TEAL)
avatar("avatar-3.png","AO",NAVY_DEEP,BLUE)
avatar("avatar-4.png","BE",BLUE,TEAL)

# ---- 5. imagery placeholders (abstract medical, duotone-ish) ----
def photo(name, base, accent):
    W,H=800,600; im=Image.new("RGB",(W,H)); px=im.load()
    for y in range(H):
        for x in range(W):
            px[x,y]=lerp(base,accent,(math.sin(x/90)+math.cos(y/70)+2)/4)
    d=ImageDraw.Draw(im)
    # faint circles motif
    for i,r in enumerate([120,220,320]):
        d.ellipse([W*0.7-r,H*0.3-r,W*0.7+r,H*0.3+r],outline="#ffffff",width=2)
    im.save(os.path.join(IMG,name))
photo("photo-1.png",NAVY_DEEP,BLUEL)
photo("photo-2.png",NAVY,TEAL)
photo("photo-3.png",BLUE,TEALB)

print("assets generated:")
for d in (LOGO,IMG):
    for f in sorted(os.listdir(d)): print("  ",os.path.relpath(os.path.join(d,f),BUNDLE))
