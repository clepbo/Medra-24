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
  "care-in-action":    "photo-1631815588090-d4bfec5b1ccb",  # practitioner taking a patient's BP — warm, hopeful
  "hopeful-doctor":    "photo-1651008376811-b90baee60c1f",  # seated doctor, bright and optimistic
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
photo("care-in-action",   1100,1500, "d-panel-member.jpg", start=0.18, max_a=0.93)
photo("doctor-scrubs",    1100,1500, "d-panel-doctor.jpg",  start=0.18, max_a=0.93)
photo("care-team",        1100,1500, "d-panel-institution.jpg", start=0.16, max_a=0.94)

# Mobile hero cards
photo("care-in-action",   900,1020, "m-hero-member.jpg", start=0.22, max_a=0.92)
photo("doctor-scrubs",    900,1020, "m-hero-doctor.jpg",  start=0.22, max_a=0.92)
photo("care-team",        900,1020, "m-hero-institution.jpg", start=0.20, max_a=0.93)

# Onboarding slides — three real moments in the Medra story
photo("doctor-scrubs", 900,1000, "onb-1.jpg", start=0.24, max_a=0.92)   # find verified doctors
photo("doctor-phone",  900,1000, "onb-2.jpg", start=0.24, max_a=0.92)   # book from your phone
photo("lab",           900,1000, "onb-3.jpg", start=0.24, max_a=0.93)   # your records, safe with you

# Success + supporting
photo("hopeful-doctor", 1200,900, "success.jpg", start=0.22, max_a=0.90)
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
mesh(820,1740,(248,250,252),[(0.88,0.04,0.50,(238,245,249),.55),(0.06,0.30,0.45,(243,247,250),.45),
                     (0.50,0.95,0.55,(238,245,249),.35)],grain=1.6).save(f"{IMG}/surface-mobile.jpg",quality=92)
g = mesh(2160,1350,(248,250,252),[(0.04,0.04,0.38,(238,245,249),.5),(0.95,0.10,0.40,(238,245,249),.45),
                          (0.80,0.85,0.45,(243,247,250),.4),(0.45,0.45,0.5,(248,250,252),.6)],grain=1.6)
png = cairosvg.svg2png(url=LOGO_WHITE, output_width=int(2160*0.34))
lg = Image.open(io.BytesIO(png)).convert("RGBA"); lg.putalpha(lg.split()[3].point(lambda v:int(v*10/255)))
g = g.convert("RGBA"); g.alpha_composite(lg,(int(2160*0.60),int(1350*0.28)))
g.convert("RGB").save(f"{IMG}/surface-desktop.jpg",quality=92)

# gradient CTA pills
mesh(900,180,TEAL,[(0.0,0.5,0.85,OCEAN,.95),(1.0,0.5,0.75,TEAL,1.0),(0.5,0.0,0.5,TEAL_L,.35)],grain=0).save(f"{IMG}/btn-teal.jpg",quality=95)
mesh(900,180,NAVY,[(0.0,0.5,0.85,NAVY_DEEP,.95),(1.0,0.5,0.8,BLUE,.9)],grain=0).save(f"{IMG}/btn-navy.jpg",quality=95)

# ECG pulse motif (transparent PNG)
for col,nm in ((TEAL,"pulse-teal.png"),(WHITE,"pulse-white.png")):
    pulse_line(Image.new("RGBA",(760,120),(0,0,0,0)),0.5,col,255,7).save(f"{IMG}/{nm}")


# ---------------------------------------------------------------- social brand marks
GOOGLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>"""
APPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
<path fill="#0F2233" d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>"""
cairosvg.svg2png(bytestring=GOOGLE_SVG.encode(), write_to=f"{IMG}/brand-google.png", output_width=144)
cairosvg.svg2png(bytestring=APPLE_SVG.encode(),  write_to=f"{IMG}/brand-apple.png",  output_height=144)

print("assets:", len(os.listdir(IMG)), "files")
for f in sorted(os.listdir(IMG)): print("  ",f)
