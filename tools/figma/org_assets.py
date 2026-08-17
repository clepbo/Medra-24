#!/usr/bin/env python3
"""Medra — Organisation console imagery.

Three products, three structures, three grounds:
  member  full-bleed, soft blue mesh, teal          — used monthly, one thing at a time
  doctor  white card floating on soft blue, 3 cols  — used between patients, clinical
  org     graphite operations console, amber        — used all day by a front desk

The organisation console is the only one that is dark-chrome-first: an operations surface a
receptionist stares at for eight hours, not a page you visit. Warm graphite rather than navy so
it never reads as "the doctor app with a different sidebar".
"""
import os, shutil
import numpy as np
from PIL import Image

SRC = "/home/user/Medra-24/figma/medra-doctor/assets/img"
IMG = "/home/user/Medra-24/figma/medra-org/assets/img"
os.makedirs(IMG, exist_ok=True)
np.random.seed(41)

SHARED = ["btn-teal.jpg", "btn-navy.jpg", "tint-teal.jpg", "tint-blue.jpg", "tint-navy.jpg",
          "tint-ocean.jpg", "tint-mint.jpg", "tint-amber.jpg", "tint-red.jpg", "tint-coral.jpg",
          "tint-slate.jpg", "tint-lilac.jpg", "pale-blue.jpg", "pale-mint.jpg", "pale-amber.jpg",
          "pale-coral.jpg", "pale-lilac.jpg", "pulse-teal.png", "pulse-white.png",
          "me.jpg", "avatar-1.jpg", "avatar-2.jpg", "avatar-3.jpg", "avatar-4.jpg",
          "avatar-5.jpg", "avatar-6.jpg", "thumb-lab.jpg", "thumb-scan.jpg"]
for f in SHARED:
    shutil.copyfile(os.path.join(SRC, f), os.path.join(IMG, f))

GRAPHITE_DEEP = (22, 26, 32); GRAPHITE = (34, 40, 48); SLATE = (52, 62, 74)
AMBER = (214, 148, 46); AMBER_DEEP = (166, 108, 28); TEAL = (57, 176, 207)


def mesh(w, h, base, blobs, grain=1.0):
    yy, xx = np.mgrid[0:h, 0:w]; X = xx / w; Y = yy / h; ar = h / w
    acc = np.zeros((h, w, 3), np.float32) + np.array(base, np.float32)
    for cx, cy, r, color, s in blobs:
        dx = X - cx; dy = (Y - cy) * ar
        wgt = np.clip(np.exp(-((dx * dx + dy * dy) / (r * r)) * 2.2) * s, 0, 1)[..., None]
        acc = acc * (1 - wgt) + np.array(color, np.float32) * wgt
    if grain: acc += np.random.normal(0, grain, (h, w, 1))
    return np.clip(acc, 0, 255)


def save(a, name, q=94):
    Image.fromarray(a.astype(np.uint8)).save(f"{IMG}/{name}", quality=q)


# the page ground — warm off-white with a faint graphite wash, so the dark chrome sits on it
save(mesh(1560, 1100, (240, 239, 236), [(0.02, 0.02, 0.5, (233, 232, 229), .8),
                                        (0.98, 0.9, 0.45, (236, 234, 230), .7)], grain=0.6), "canvas-org.jpg")
save(mesh(520, 1900, (240, 239, 236), [(0.1, 0.05, 0.6, (234, 233, 230), .7)], grain=0.6), "canvas-org-m.jpg")

# the icon rail and the context bar — the two pieces of chrome that make this console
save(mesh(240, 1900, GRAPHITE_DEEP, [(0.5, 0.02, 0.9, GRAPHITE, .9),
                                     (0.5, 1.0, 0.7, (18, 22, 27), .9)], grain=0.5), "rail-org.jpg")
save(mesh(2400, 160, GRAPHITE, [(0.0, 0.5, 0.6, GRAPHITE_DEEP, .8),
                                (1.0, 0.5, 0.7, SLATE, .6)], grain=0.5), "ctxbar.jpg")
save(mesh(900, 560, GRAPHITE, [(0.1, 0.1, 0.8, GRAPHITE_DEEP, .9),
                               (1.0, 0.9, 0.7, SLATE, .6)], grain=0.7), "head-org-m.jpg")

# amber is the organisation's accent — used for counts, seats and anything the admin owns
save(mesh(600, 400, AMBER, [(0.15, 0.15, 0.8, (232, 172, 70), .7),
                            (0.9, 0.9, 0.6, AMBER_DEEP, .6)], grain=0), "btn-amber.jpg")
save(mesh(300, 300, (250, 243, 228), [(0.2, 0.2, 0.8, (252, 246, 234), .6)], grain=0), "pale-gold.jpg")
save(mesh(600, 400, SLATE, [(0.15, 0.15, 0.8, (66, 78, 92), .7)], grain=0), "btn-slate.jpg")

# per-department tints, so a queue reads by colour before it reads by label
for nm, col in (("dept-nursing.jpg", (72, 140, 122)), ("dept-lab.jpg", (66, 108, 160)),
                ("dept-pharmacy.jpg", (150, 96, 156)), ("dept-desk.jpg", (196, 128, 58)),
                ("dept-clinic.jpg", (58, 122, 150)), ("dept-imaging.jpg", (96, 104, 168)),
                ("dept-billing.jpg", (86, 132, 96))):
    save(mesh(400, 260, col, [(0.2, 0.2, 0.8, tuple(min(255, c + 34) for c in col), .7),
                              (0.9, 0.9, 0.6, tuple(max(0, c - 22) for c in col), .6)], grain=0), nm)

print("org imagery:", len(os.listdir(IMG)), "files")
