#!/usr/bin/env python3
"""Medra — Doctor app imagery.

The doctor app deliberately looks unlike the member app. Members get soft mesh grounds and
generous radii; the doctor gets a **clinical workstation**: a graph-paper ground, a deep navy
icon rail, squarer corners and denser type. Same brand, unmistakably a different tool.
"""
import os, shutil
import numpy as np
from PIL import Image

SRC = "/home/user/Medra-24/figma/medra-member-2/assets/img"
IMG = "/home/user/Medra-24/figma/medra-doctor/assets/img"
os.makedirs(IMG, exist_ok=True)
np.random.seed(23)

SHARED = ["btn-teal.jpg", "btn-navy.jpg", "tint-teal.jpg", "tint-blue.jpg", "tint-navy.jpg",
          "tint-ocean.jpg", "tint-mint.jpg", "tint-amber.jpg", "pulse-teal.png", "pulse-white.png",
          "me.jpg", "avatar-1.jpg", "avatar-2.jpg", "avatar-3.jpg", "avatar-4.jpg",
          "avatar-5.jpg", "avatar-6.jpg", "thumb-lab.jpg", "thumb-scan.jpg",
          "call-doctor-d.jpg", "call-doctor-m.jpg", "call-self.jpg"]
for f in SHARED:
    shutil.copyfile(os.path.join(SRC, f), os.path.join(IMG, f))

NAVY_DEEP = (15, 34, 51); NAVY = (27, 58, 91); BLUE = (36, 95, 136); OCEAN = (46, 134, 168)
TEAL = (57, 176, 207); INK = (9, 20, 31)


def mesh(w, h, base, blobs, grain=1.2):
    yy, xx = np.mgrid[0:h, 0:w]; X = xx / w; Y = yy / h; ar = h / w
    acc = np.zeros((h, w, 3), np.float32) + np.array(base, np.float32)
    for cx, cy, r, color, s in blobs:
        dx = X - cx; dy = (Y - cy) * ar
        wgt = np.clip(np.exp(-((dx * dx + dy * dy) / (r * r)) * 2.2) * s, 0, 1)[..., None]
        acc = acc * (1 - wgt) + np.array(color, np.float32) * wgt
    if grain: acc += np.random.normal(0, grain, (h, w, 1))
    return np.clip(acc, 0, 255)


def graph_paper(w, h, base=(246, 249, 251), line=(226, 234, 241), major=(214, 226, 236),
                step=24, major_every=5):
    """The doctor's ground: a faint square grid, like the paper a clinic already runs on."""
    a = np.zeros((h, w, 3), np.float32) + np.array(base, np.float32)
    for x in range(0, w, step):
        a[:, x] = major if (x // step) % major_every == 0 else line
    for y in range(0, h, step):
        a[y, :] = major if (y // step) % major_every == 0 else line
    # a breath of brand tint in two corners so it is not dead flat
    tint = mesh(w, h, (0, 0, 0), [(0.02, 0.02, 0.42, (10, 26, 40), .16),
                                  (0.98, 0.9, 0.45, (12, 40, 60), .12)], grain=0)
    a = a * (1 - tint / 255.0 * 0.30)
    a += np.random.normal(0, 0.8, (h, w, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


graph_paper(1560, 1400).save(f"{IMG}/surface-clinic.jpg", quality=94)
graph_paper(560, 1900, step=22).save(f"{IMG}/surface-clinic-m.jsx.jpg", quality=94)
graph_paper(560, 1900, step=22).save(f"{IMG}/surface-clinic-m.jpg", quality=94)
os.remove(f"{IMG}/surface-clinic-m.jsx.jpg")

# The icon rail — narrower and darker than the member sidebar, with a single teal seam.
rail = mesh(180, 1900, INK, [(0.5, 0.02, 0.9, NAVY, .85), (0.5, 0.55, 0.8, (18, 46, 72), .5),
                             (0.5, 1.0, 0.8, INK, .95)], grain=0.8)
rail[:, -3:] = np.array(TEAL, np.float32) * 0.55 + rail[:, -3:] * 0.45
Image.fromarray(np.clip(rail, 0, 255).astype(np.uint8)).save(f"{IMG}/rail.jpg", quality=94)

# The contextual panel behind the rail — very light, one shade off the page
Image.fromarray(np.clip(mesh(520, 1900, (250, 252, 254),
                             [(0.5, 0.0, 0.7, (243, 247, 250), .8),
                              (0.5, 1.0, 0.7, (246, 249, 252), .7)], grain=0.6),
                        0, 255).astype(np.uint8)).save(f"{IMG}/panel.jpg", quality=94)

# Mobile header block — deep navy, so the doctor app never reads like the member app
Image.fromarray(np.clip(mesh(800, 520, INK, [(0.15, 0.1, 0.8, NAVY, .8), (0.95, 0.9, 0.7, BLUE, .45)],
                             grain=0.9), 0, 255).astype(np.uint8)).save(f"{IMG}/head-m.jpg", quality=94)

# Command-bar ground for the desktop top strip
Image.fromarray(np.clip(mesh(2400, 180, INK, [(0.02, 0.5, 0.7, NAVY, .8), (0.98, 0.5, 0.6, (20, 52, 80), .5)],
                             grain=0.7), 0, 255).astype(np.uint8)).save(f"{IMG}/command.jpg", quality=94)

# Attention tints for the clinical alert rows
for nm, col in (("tint-red.jpg", (196, 62, 62)), ("tint-slate.jpg", (62, 76, 89))):
    Image.fromarray(np.clip(mesh(600, 400, col,
                                 [(0.15, 0.15, 0.8, tuple(min(255, c + 40) for c in col), .7),
                                  (0.9, 0.9, 0.6, tuple(max(0, c - 25) for c in col), .6)], grain=0),
                            0, 255).astype(np.uint8)).save(f"{IMG}/{nm}", quality=94)

print("doctor imagery:", len(os.listdir(IMG)), "files")
for f in sorted(os.listdir(IMG)): print("   ", f)
