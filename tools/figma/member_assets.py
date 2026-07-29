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
