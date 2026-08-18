#!/usr/bin/env python3
"""Medra Member app — imagery. Real Unsplash photography (verified IDs) for doctor
avatars and cards, plus the shared brand surfaces."""
import os, subprocess
import numpy as np
from PIL import Image

IMG="/home/user/Medra-24/figma/medra-member/assets/img"
os.makedirs(IMG, exist_ok=True)

DOCTORS = {                     # verified in earlier review passes
  "avatar-1.jpg": "photo-1622253692010-333f2da6031d",  # Dr. Chuka — scrubs
  "avatar-2.jpg": "photo-1573497019940-1c28c88b4f3e",  # Dr. Amina
  "avatar-3.jpg": "photo-1594824476967-48c8b964273f",  # Dr. Kemi — teal scrubs
  "avatar-4.jpg": "photo-1651008376811-b90baee60c1f",  # Dr. Ngozi
  "avatar-5.jpg": "photo-1666887360742-974c8fce8e6b",  # Dr. Tunde
  "avatar-6.jpg": "photo-1612531386530-97286d97c2d2",  # Dr. Idris
  "me.jpg":       "photo-1531123897727-8f129e1688ce",  # Amara (the member)
}
CARDS = {
  "card-care.jpg":  ("photo-1631815588090-d4bfec5b1ccb", 900, 520),   # care in action
  "card-lab.jpg":   ("photo-1609188076864-c35269136b09", 900, 520),   # diagnostics
  "card-team.jpg":  ("photo-1666214280557-f1b5022eb634", 900, 520),   # hospital
}
U="https://images.unsplash.com/{id}?w={w}&h={h}&fit=crop&crop=faces,entropy&q=82"

def fetch(pid,w,h):
    dst=f"/tmp/medra_m_{pid}_{w}x{h}.jpg"
    if not os.path.exists(dst):
        subprocess.run(["curl","-sL","--max-time","40","-o",dst,U.format(id=pid,w=w,h=h)],check=True)
    im=Image.open(dst).convert("RGB")
    return im.resize((w,h),Image.LANCZOS) if im.size!=(w,h) else im

def grade(im,strength=0.14,tint=(30,110,150)):
    a=np.asarray(im).astype(np.float32); lum=a.mean(axis=2,keepdims=True)/255.0
    return Image.fromarray(np.clip(a*(1-strength)+(np.array(tint,np.float32)*(0.45+0.75*lum))*strength,0,255).astype(np.uint8))

def scrim(im,start=0.45,max_a=0.80,color=(15,34,51)):
    w,h=im.size; y=np.linspace(0,1,h)[:,None]
    a=np.repeat(np.clip((y-start)/(1-start),0,1)**1.3*max_a,w,axis=1)[...,None]
    base=np.asarray(im).astype(np.float32)
    return Image.fromarray(np.clip(base*(1-a)+np.array(color,np.float32)*a,0,255).astype(np.uint8))

for name,pid in DOCTORS.items():
    grade(fetch(pid,400,400)).save(f"{IMG}/{name}",quality=88)
for name,(pid,w,h) in CARDS.items():
    scrim(grade(fetch(pid,w,h))).save(f"{IMG}/{name}",quality=88)

print("member imagery:", len(DOCTORS)+len(CARDS), "files")

# ---------------------------------------------------------------- subtle surfaces + panels
def mesh(w,h,base,blobs,grain=1.6):
    yy,xx=np.mgrid[0:h,0:w]; X=xx/w; Y=yy/h; ar=h/w
    acc=np.zeros((h,w,3),np.float32)+np.array(base,np.float32)
    for cx,cy,r,color,s in blobs:
        dx=X-cx; dy=(Y-cy)*ar
        wgt=np.clip(np.exp(-((dx*dx+dy*dy)/(r*r))*2.2)*s,0,1)[...,None]
        acc=acc*(1-wgt)+np.array(color,np.float32)*wgt
    if grain: acc+=np.random.normal(0,grain,(h,w,1))
    return Image.fromarray(np.clip(acc,0,255).astype(np.uint8))

NAVY_DEEP=(15,34,51); NAVY=(27,58,91); BLUE=(36,95,136); OCEAN=(46,134,168)
TEAL=(57,176,207); TEAL_L=(111,195,216)
PAPER=(248,250,252); WHISPER=(243,247,250); HINT=(238,245,249)

# Backgrounds — almost white, just a breath of tint
mesh(820,1740,PAPER,[(0.88,0.04,0.50,HINT,.55),(0.06,0.30,0.45,WHISPER,.45),
                     (0.50,0.95,0.55,HINT,.35)]).save(f"{IMG}/surface-mobile.jpg",quality=92)
mesh(2160,1350,PAPER,[(0.04,0.04,0.38,HINT,.5),(0.95,0.10,0.40,HINT,.45),
                      (0.80,0.85,0.45,WHISPER,.4),(0.45,0.45,0.5,PAPER,.6)]).save(f"{IMG}/surface-desktop.jpg",quality=92)

# Sidebar — deep navy gradient rail
mesh(560,1800,NAVY_DEEP,[(0.2,0.06,0.75,NAVY,.9),(0.9,0.55,0.7,BLUE,.55),
                         (0.1,0.95,0.7,NAVY_DEEP,.9)],grain=1.2).save(f"{IMG}/sidebar.jpg",quality=92)
# Hero banner — brand gradient for the dashboard greeting
mesh(2200,520,OCEAN,[(0.02,0.5,0.7,NAVY,.95),(0.55,0.2,0.6,BLUE,.7),
                     (1.0,0.7,0.7,TEAL,.85)],grain=1.0).save(f"{IMG}/hero-banner.jpg",quality=92)
# Soft tinted stat-card grounds
for nm,col in (("tint-teal.jpg",TEAL),("tint-blue.jpg",BLUE),("tint-navy.jpg",NAVY),("tint-ocean.jpg",OCEAN)):
    mesh(600,400,col,[(0.15,0.15,0.8,tuple(min(255,c+40) for c in col),.7),
                      (0.9,0.9,0.6,tuple(max(0,c-25) for c in col),.6)],grain=0).save(f"{IMG}/{nm}",quality=92)

# ---------------------------------------------------------------------------------------
# THE CALM REGISTER — member mobile only
#
# "Look at how subtle and calm the interface looks, the use of cards and icons to illustrate
# functions, and also the glass effects… not too much colours/gradients, just subtle, calm and
# minimal."
#
# The renderer has no blur and no shadow, so glass cannot be live — it is baked here as a
# near-white panel with the faintest vertical lift, which is what a frosted card actually looks
# like against a pale ground. The calm button is the other half: the old primary was a bright
# teal gradient, the most saturated thing on any member screen. This one runs deep ocean into
# navy, so it still reads as the action without shouting.
CALM_DEEP = (23, 62, 84); CALM = (32, 92, 118)
mesh(600, 400, CALM, [(0.12, 0.12, 0.85, CALM_DEEP, .8), (0.95, 0.9, 0.6, (28, 78, 102), .7)],
     grain=0).save(f"{IMG}/btn-calm.jpg", quality=92)

# A frosted card. Almost white, warmer at the top than the bottom, so a stack of them separates
# by tone rather than by a drawn line.
mesh(800, 600, (252, 253, 254), [(0.5, 0.0, 0.9, (255, 255, 255), .9),
                                 (0.5, 1.0, 0.8, (243, 247, 250), .7)],
     grain=0.5).save(f"{IMG}/glass-card.jpg", quality=94)

# The function tile behind an icon — a breath of colour, never a block of it.
for nm, col in (("soft-teal.jpg", (226, 241, 246)), ("soft-blue.jpg", (228, 238, 247)),
                ("soft-mint.jpg", (228, 243, 236)), ("soft-sand.jpg", (247, 241, 230)),
                ("soft-lilac.jpg", (238, 236, 248)), ("soft-rose.jpg", (250, 236, 238))):
    mesh(300, 300, col, [(0.25, 0.2, 0.9, tuple(min(255, c + 6) for c in col), .8)],
         grain=0).save(f"{IMG}/{nm}", quality=94)

print("surfaces + panels regenerated (subtle) + calm register")
