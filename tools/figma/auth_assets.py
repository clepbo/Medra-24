#!/usr/bin/env python3
"""Medra Auth — asset pipeline.
1) Downloads REAL photography from Unsplash (free licence) chosen for Nigerian/African
   representation in healthcare, crops it, applies a subtle brand grade and a text scrim.
2) Generates the procedural brand surfaces (mesh gradients), gradient CTA pills and the
   ECG pulse motif that give Medra its signature look.
"""
import os, io, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cairosvg

IMG = "/home/user/Medra-24/figma/medra-auth/assets/img"
LOGO_WHITE = "/home/user/Medra-24/brand/svg/medra-logo-white.svg"
os.makedirs(IMG, exist_ok=True)
np.random.seed(7)

NAVY_DEEP=(15,34,51); NAVY=(27,58,91); BLUE=(36,95,136); OCEAN=(46,134,168)
TEAL=(57,176,207); TEAL_L=(111,195,216); SKY=(168,221,233); MIST=(214,236,243)
MINT=(226,244,240); PAPER=(244,248,251); WHITE=(255,255,255)

# ---------------------------------------------------------------- photos
# Unsplash photo IDs, hand-verified for subject + representation.
PHOTOS = {
  "portrait-patient":  "photo-1531123897727-8f129e1688ce",  # Black woman, African print — patient
  "doctor-scrubs":     "photo-1622253692010-333f2da6031d",  # Black doctor, blue scrubs, stethoscope
  "doctor-phone":      "photo-1576091160399-112ba8d25d1d",  # Black doctor's hands + phone (booking)
  "care-team":         "photo-1666214280557-f1b5022eb634",  # diverse clinical team at work
  "pro-woman":         "photo-1573497019940-1c28c88b4f3e",  # professional woman of colour — admin
  "teal-scrubs":       "photo-1594824476967-48c8b964273f",  # clinician in teal scrubs (brand hue)
  "lab":               "photo-1609188076864-c35269136b09",  # lab technician
  "hands-care":        "photo-1584515933487-779824d29309",  # hands held — compassion
}
UNSPLASH = "https://images.unsplash.com/{id}?w={w}&h={h}&fit=crop&crop=faces,entropy&q=82"

def fetch(key, w, h):
    url = UNSPLASH.format(id=PHOTOS[key], w=w, h=h)
    dst = f"/tmp/medra_{key}_{w}x{h}.jpg"
    if not os.path.exists(dst):
        subprocess.run(["curl","-sL","--max-time","40","-o",dst,url], check=True)
    im = Image.open(dst).convert("RGB")
    return im.resize((w,h), Image.LANCZOS) if im.size != (w,h) else im

def grade(im, strength=0.16, tint=(30,110,150)):
    """Subtle cool brand grade so photography sits with the navy→teal palette."""
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(axis=2, keepdims=True) / 255.0
    t = np.array(tint, np.float32)
    graded = a*(1-strength) + (t*(0.45+0.75*lum))*strength
    return Image.fromarray(np.clip(graded,0,255).astype(np.uint8))

def scrim(im, color=NAVY_DEEP, start=0.34, end=1.0, max_a=0.90, top_a=0.18):
    """Bake a bottom-up gradient so white text is always legible."""
    w,h = im.size
    y = np.linspace(0,1,h)[:,None]
    a = np.clip((y-start)/max(1e-6,(end-start)),0,1)**1.35 * max_a
    a = np.maximum(a, top_a*np.clip((0.22-y)/0.22,0,1))   # slight top veil for status bar
    a = np.repeat(a, w, axis=1)[...,None]
    base = np.asarray(im).astype(np.float32)
    col = np.array(color, np.float32)
    out = base*(1-a) + col*a
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

def photo(key, w, h, name, do_scrim=True, **kw):
    im = grade(fetch(key,w,h))
    if do_scrim: im = scrim(im, **kw)
    im.save(os.path.join(IMG,name), quality=88)

# Desktop side panels (portrait) — carry headline + proof, so strong scrim
photo("portrait-patient", 1100,1500, "d-panel-patient.jpg", start=0.18, max_a=0.93)
photo("doctor-scrubs",    1100,1500, "d-panel-doctor.jpg",  start=0.18, max_a=0.93)
photo("care-team",        1100,1500, "d-panel-institution.jpg", start=0.16, max_a=0.94)

# Mobile hero cards
photo("portrait-patient", 900,1020, "m-hero-patient.jpg", start=0.22, max_a=0.92)
photo("doctor-scrubs",    900,1020, "m-hero-doctor.jpg",  start=0.22, max_a=0.92)
photo("care-team",        900,1020, "m-hero-institution.jpg", start=0.20, max_a=0.93)

# Onboarding slides — three real moments in the Medra story
photo("doctor-scrubs", 900,1000, "onb-1.jpg", start=0.24, max_a=0.92)   # find verified doctors
photo("doctor-phone",  900,1000, "onb-2.jpg", start=0.24, max_a=0.92)   # book from your phone
photo("lab",           900,1000, "onb-3.jpg", start=0.24, max_a=0.93)   # your records, safe with you

# Success + supporting
photo("pro-woman",   1200,900, "success.jpg", start=0.22, max_a=0.90)
photo("lab",         900,700,  "proof-lab.jpg", start=0.45, max_a=0.75)
photo("doctor-phone",900,700,  "proof-phone.jpg", start=0.45, max_a=0.70)

# Avatars (no scrim)
for k,n in (("doctor-scrubs","avatar-1.jpg"),("pro-woman","avatar-2.jpg"),("teal-scrubs","avatar-3.jpg")):
    grade(fetch(k,400,400)).save(os.path.join(IMG,n), quality=88)

# ---------------------------------------------------------------- procedural brand surfaces
def mesh(w,h,base,blobs,grain=2.2):
    yy,xx = np.mgrid[0:h,0:w]; X=xx/w; Y=yy/h; ar=h/w
    acc = np.zeros((h,w,3),np.float32) + np.array(base,np.float32)
    for cx,cy,r,color,s in blobs:
        dx=X-cx; dy=(Y-cy)*ar
        wgt=np.clip(np.exp(-((dx*dx+dy*dy)/(r*r))*2.2)*s,0,1)[...,None]
        acc = acc*(1-wgt) + np.array(color,np.float32)*wgt
    if grain: acc += np.random.normal(0,grain,(h,w,1))
    return Image.fromarray(np.clip(acc,0,255).astype(np.uint8))

def pulse_line(im, y_frac, color, alpha, width=6, amp=0.30):
    ov=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    W,H=im.size; y=H*y_frac; A=H*amp; pts=[]; x=0.0; seg=W*0.5
    while x < W:
        pts += [(x,y),(x+seg*0.34,y)]; x+=seg*0.34
        pts += [(x+seg*0.05,y-A*0.35),(x+seg*0.11,y+A*1.0),(x+seg*0.18,y-A*1.5),
                (x+seg*0.24,y+A*0.25),(x+seg*0.30,y)]; x+=seg*0.30
        pts += [(min(x+seg*0.36,W),y)]; x+=seg*0.36
    d.line(pts,fill=color+(alpha,),width=width,joint="curve")
    return Image.alpha_composite(im.convert("RGBA"),ov)

# page grounds
mesh(820,1740,PAPER,[(0.85,0.06,0.55,MIST,.95),(0.10,0.02,0.42,MINT,.75),(0.95,0.42,0.40,SKY,.55),
                     (0.50,0.95,0.60,MIST,.55),(0.20,0.30,0.35,WHITE,.75)]).save(f"{IMG}/surface-mobile.jpg",quality=92)
g = mesh(2160,1350,PAPER,[(0.06,0.05,0.40,MINT,.85),(0.32,0.02,0.34,MIST,.7),(0.92,0.14,0.44,SKY,.75),
                          (0.78,0.72,0.50,MIST,.65),(0.14,0.86,0.44,MINT,.55),(0.50,0.45,0.45,WHITE,.85)])
png = cairosvg.svg2png(url=LOGO_WHITE, output_width=int(2160*0.34))
lg = Image.open(io.BytesIO(png)).convert("RGBA"); lg.putalpha(lg.split()[3].point(lambda v:int(v*18/255)))
g = g.convert("RGBA"); g.alpha_composite(lg,(int(2160*0.60),int(1350*0.28)))
g.convert("RGB").save(f"{IMG}/surface-desktop.jpg",quality=92)

# gradient CTA pills
mesh(900,180,TEAL,[(0.0,0.5,0.85,OCEAN,.95),(1.0,0.5,0.75,TEAL,1.0),(0.5,0.0,0.5,TEAL_L,.35)],grain=0).save(f"{IMG}/btn-teal.jpg",quality=95)
mesh(900,180,NAVY,[(0.0,0.5,0.85,NAVY_DEEP,.95),(1.0,0.5,0.8,BLUE,.9)],grain=0).save(f"{IMG}/btn-navy.jpg",quality=95)

# ECG pulse motif (transparent PNG)
for col,nm in ((TEAL,"pulse-teal.png"),(WHITE,"pulse-white.png")):
    pulse_line(Image.new("RGBA",(760,120),(0,0,0,0)),0.5,col,255,7).save(f"{IMG}/{nm}")

print("assets:", len(os.listdir(IMG)), "files")
for f in sorted(os.listdir(IMG)): print("  ",f)
