#!/usr/bin/env python3
"""Medra Member app, batch 2 (Visits · Records · Medicines · Profile) — imagery.

Shared surfaces, buttons, avatars and tints are copied from the batch-1 bundle so the two
batches are pixel-identical. Only the genuinely new artwork is produced here:
  · the virtual-visit video frames (doctor on camera, self-view, blurred "connecting" plate)
  · the records / capture / family banners
  · a deep navy call-chrome ground and a blank "no signal" plate
All photography is real licensed Unsplash work from the same hand-verified ID set used across
the project (Nigerian / African representation in healthcare).
"""
import os, shutil, subprocess
import numpy as np
from PIL import Image, ImageFilter

SRC = "/home/user/Medra-24/figma/medra-member/assets/img"
IMG = "/home/user/Medra-24/figma/medra-member/assets/img"
os.makedirs(IMG, exist_ok=True)
np.random.seed(11)

# ---------------------------------------------------------------- 1. shared, copied verbatim
SHARED = ["surface-mobile.jpg","surface-desktop.jpg","sidebar.jpg","hero-banner.jpg",
          "btn-teal.jpg","btn-navy.jpg","tint-teal.jpg","tint-blue.jpg","tint-navy.jpg",
          "tint-ocean.jpg","pulse-teal.png","pulse-white.png","me.jpg",
          "avatar-1.jpg","avatar-2.jpg","avatar-3.jpg","avatar-4.jpg","avatar-5.jpg","avatar-6.jpg",
          "card-care.jpg","card-lab.jpg","card-team.jpg"]
for f in SHARED:
    shutil.copyfile(os.path.join(SRC,f), os.path.join(IMG,f))

# ---------------------------------------------------------------- 2. new photography
PHOTOS = {
  "doctor-oncall":  "photo-1651008376811-b90baee60c1f",  # seated doctor, bright, looking to camera
  "doctor-phone":   "photo-1576091160399-112ba8d25d1d",  # clinician's hands + phone (capture/upload)
  "hands-care":     "photo-1584515933487-779824d29309",  # hands held — dependants / people you care for
  "lab":            "photo-1609188076864-c35269136b09",  # diagnostics — records header
  "care-in-action": "photo-1631815588090-d4bfec5b1ccb",  # BP check — visit history header
}
U = "https://images.unsplash.com/{id}?w={w}&h={h}&fit=crop&crop=faces,entropy&q=82"

def fetch(key,w,h):
    dst = f"/tmp/medra_m2_{PHOTOS[key]}_{w}x{h}.jpg"
    if not os.path.exists(dst):
        subprocess.run(["curl","-sL","--max-time","40","-o",dst,U.format(id=PHOTOS[key],w=w,h=h)],check=True)
    im = Image.open(dst).convert("RGB")
    return im.resize((w,h), Image.LANCZOS) if im.size != (w,h) else im

def grade(im, strength=0.14, tint=(30,110,150)):
    a = np.asarray(im).astype(np.float32); lum = a.mean(axis=2,keepdims=True)/255.0
    return Image.fromarray(np.clip(a*(1-strength)+(np.array(tint,np.float32)*(0.45+0.75*lum))*strength,0,255).astype(np.uint8))

def scrim(im, start=0.45, max_a=0.80, color=(15,34,51), top_a=0.0):
    w,h = im.size; y = np.linspace(0,1,h)[:,None]
    a = np.clip((y-start)/max(1e-6,1-start),0,1)**1.3 * max_a
    if top_a: a = np.maximum(a, top_a*np.clip((0.20-y)/0.20,0,1))
    a = np.repeat(a,w,axis=1)[...,None]
    base = np.asarray(im).astype(np.float32)
    return Image.fromarray(np.clip(base*(1-a)+np.array(color,np.float32)*a,0,255).astype(np.uint8))

def save(im,name,q=88): im.save(os.path.join(IMG,name), quality=q)

# --- virtual visit: the doctor's camera feed ------------------------------------------------
# Mobile is a tall full-bleed feed; desktop is a 16:10 stage. Both get a very light top+bottom
# veil so the white call controls and the name plate stay legible over any part of the frame.
# Unsplash's tall face crop leaves the subject off to one side, so pull a wider plate and take
# the centre 900px — that lands her mid-frame, the way a real front-facing camera would.
def tall_feed():
    return fetch("doctor-oncall",1200,1500).crop((150,0,1050,1500))

save(scrim(grade(tall_feed()), start=0.58, max_a=0.72, top_a=0.30), "call-doctor-m.jpg", 90)
save(scrim(grade(fetch("doctor-oncall",1400,900)),  start=0.60, max_a=0.66, top_a=0.26), "call-doctor-d.jpg", 90)

# "Connecting…" plate — same feed, heavily blurred + darkened, so the transition smart-animates
blur = grade(tall_feed()).filter(ImageFilter.GaussianBlur(26))
save(scrim(blur, start=0.0, max_a=0.55), "call-connecting.jpg", 88)

# Self view (picture-in-picture) — the member, from the shared avatar photo
me = Image.open(os.path.join(SRC,"me.jpg")).convert("RGB").resize((420,560), Image.LANCZOS)
save(me, "call-self.jpg", 90)

# --- section banners -----------------------------------------------------------------------
save(scrim(grade(fetch("care-in-action",1400,520)), start=0.18, max_a=0.88), "banner-visits.jpg", 90)
save(scrim(grade(fetch("lab",1400,520)),            start=0.18, max_a=0.90), "banner-records.jpg", 90)
save(scrim(grade(fetch("doctor-phone",900,620)),    start=0.22, max_a=0.88), "banner-capture.jpg", 90)
save(scrim(grade(fetch("hands-care",900,620)),      start=0.30, max_a=0.84), "banner-family.jpg", 90)

# --- record thumbnails (a scan of a paper result, shown small) ------------------------------
save(grade(fetch("lab",600,420), strength=0.10), "thumb-lab.jpg", 86)
save(grade(fetch("doctor-phone",600,420), strength=0.10), "thumb-scan.jpg", 86)

# ---------------------------------------------------------------- 3. procedural grounds
def mesh(w,h,base,blobs,grain=1.4):
    yy,xx = np.mgrid[0:h,0:w]; X=xx/w; Y=yy/h; ar=h/w
    acc = np.zeros((h,w,3),np.float32)+np.array(base,np.float32)
    for cx,cy,r,color,s in blobs:
        dx=X-cx; dy=(Y-cy)*ar
        wgt=np.clip(np.exp(-((dx*dx+dy*dy)/(r*r))*2.2)*s,0,1)[...,None]
        acc = acc*(1-wgt)+np.array(color,np.float32)*wgt
    if grain: acc += np.random.normal(0,grain,(h,w,1))
    return Image.fromarray(np.clip(acc,0,255).astype(np.uint8))

NAVY_DEEP=(15,34,51); NAVY=(27,58,91); BLUE=(36,95,136); OCEAN=(46,134,168)
TEAL=(57,176,207); MINT=(226,244,240); INK=(10,22,34)

# Call chrome / waiting room ground — deep, quiet, so the video is the brightest thing on screen
mesh(900,1500,INK,[(0.3,0.06,0.8,NAVY,.75),(0.85,0.6,0.7,(20,52,80),.5),(0.1,0.95,0.7,INK,.9)],
     grain=1.0).save(f"{IMG}/call-ground.jpg", quality=92)
mesh(1400,900,INK,[(0.15,0.1,0.7,NAVY,.7),(0.9,0.7,0.7,(20,52,80),.5)],
     grain=1.0).save(f"{IMG}/call-ground-d.jpg", quality=92)

# "No signal" plate for the connection-lost state
mesh(900,1500,(24,38,52),[(0.5,0.4,0.9,(32,50,66),.6)],grain=3.0).save(f"{IMG}/call-nosignal.jpg", quality=88)

# Soft mint ground for the medicines module (no stock photo needed — the pill iconography carries it)
mesh(1400,520,MINT,[(0.05,0.2,0.6,(214,236,243),.7),(0.95,0.8,0.6,(226,244,240),.8),
                    (0.5,0.0,0.5,(240,250,248),.6)],grain=1.0).save(f"{IMG}/banner-meds.jpg", quality=92)

# Extra tints for the batch-2 stat cards
for nm,col in (("tint-mint.jpg",(46,163,107)),("tint-amber.jpg",(224,163,46))):
    mesh(600,400,col,[(0.15,0.15,0.8,tuple(min(255,c+40) for c in col),.7),
                      (0.9,0.9,0.6,tuple(max(0,c-25) for c in col),.6)],grain=0).save(f"{IMG}/{nm}", quality=92)

print("member-2 imagery:", len(os.listdir(IMG)), "files")
for f in sorted(os.listdir(IMG)): print("   ", f)
