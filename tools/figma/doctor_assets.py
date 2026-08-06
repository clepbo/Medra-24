#!/usr/bin/env python3
"""Medra — Doctor app imagery.

Second pass. The clinical "graph paper + dark command strip" read as wired-up and technical.
This direction takes the reference dashboard's warmth instead: the whole app is a **white card
floating on a soft blue canvas**, with a navy sidebar, a light right rail, pastel chips and a
flat illustration in the welcome banner.

It stays distinct from the member app by structure, not by coldness:
  member  = full-bleed, two columns (navy sidebar + main)
  doctor  = floating card, three columns (navy sidebar + main + light right rail with a calendar)
"""
import os, io, math, shutil
import numpy as np
from PIL import Image
import cairosvg

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
TEAL = (57, 176, 207); INK = (9, 20, 31); CORAL = (240, 122, 82); AMBER = (224, 163, 46)


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


# ---------------------------------------------------------------- 1. the page canvas
# Soft blue, a little cooler at the top-left, with two faint panels echoing the reference's
# pale blue blocks behind the card.
def canvas(w, h):
    a = mesh(w, h, (238, 243, 251), [(0.02, 0.02, 0.55, (228, 237, 250), .8),
                                     (0.98, 0.05, 0.40, (224, 234, 249), .7),
                                     (0.92, 0.96, 0.45, (231, 239, 250), .8),
                                     (0.45, 0.5, 0.6, (243, 247, 253), .6)], grain=0.7)
    return a


save(canvas(1560, 1100), "canvas.jpg")
save(canvas(520, 1900), "canvas-m.jpg")

# ---------------------------------------------------------------- 2. the navy sidebar
side = mesh(420, 1900, NAVY_DEEP, [(0.35, 0.02, 0.85, (23, 50, 78), .9),
                                   (0.9, 0.5, 0.7, (26, 60, 92), .5),
                                   (0.1, 1.0, 0.8, NAVY_DEEP, .95)], grain=0.6)
save(side, "sidebar-dr.jpg")

# The brand gradient block used for the mobile header and the welcome banner
save(mesh(1800, 620, NAVY, [(0.02, 0.5, 0.7, NAVY_DEEP, .9), (0.6, 0.1, 0.6, BLUE, .6),
                            (1.0, 0.8, 0.7, OCEAN, .8)], grain=0.7), "band.jpg")
save(mesh(900, 560, NAVY, [(0.1, 0.1, 0.8, NAVY_DEEP, .9), (1.0, 0.9, 0.7, BLUE, .55)],
          grain=0.7), "head-m.jpg")

# Warm accent fills — the reference leans on an orange next to the blue. Medra keeps its brand,
# so the warmth comes from amber and coral used only for chips and attention states.
for nm, col in (("tint-coral.jpg", CORAL), ("tint-red.jpg", (196, 62, 62)),
                ("tint-slate.jpg", (62, 76, 89)), ("tint-lilac.jpg", (122, 132, 196))):
    save(mesh(600, 400, col, [(0.15, 0.15, 0.8, tuple(min(255, c + 40) for c in col), .7),
                              (0.9, 0.9, 0.6, tuple(max(0, c - 25) for c in col), .6)], grain=0), nm)

# Pale pastel chip grounds
for nm, col in (("pale-blue.jpg", (228, 240, 245)), ("pale-mint.jpg", (230, 245, 238)),
                ("pale-amber.jpg", (251, 241, 221)), ("pale-coral.jpg", (253, 235, 228)),
                ("pale-lilac.jpg", (237, 238, 250))):
    save(mesh(300, 300, col, [(0.2, 0.2, 0.8, tuple(min(255, c + 6) for c in col), .6)], grain=0), nm)


# ---------------------------------------------------------------- 3. donut charts
# The DSL cannot draw an arc, so each ring the design needs is baked once.
def donut(pct, size=420, thick=46, fg=TEAL, fg2=NAVY, bg=(233, 239, 246)):
    S = size * 3
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    pad = thick * 3 // 2 + 6
    box = [pad, pad, S - pad, S - pad]
    d.ellipse(box, outline=bg + (255,), width=thick * 3)
    # two-tone like the reference: the first two thirds in teal, the remainder in navy
    start = -90
    split = start + 360 * pct / 100 * 0.62
    end = start + 360 * pct / 100
    d.arc(box, start, split, fill=fg + (255,), width=thick * 3)
    d.arc(box, split, end, fill=fg2 + (255,), width=thick * 3)
    img = img.resize((size, size), Image.LANCZOS)
    return img


for p in (38, 62, 84, 92, 96):
    donut(p).save(f"{IMG}/donut-{p}.png")


# ---------------------------------------------------------------- 4. the welcome illustration
# Flat, geometric, brand-coloured. Deliberately abstract rather than a badly drawn person:
# a consultation reduced to the objects a doctor actually touches.
ILLO = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 460">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#39B0CF"/><stop offset="1" stop-color="#245F88"/>
    </linearGradient>
    <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EAF1F5"/>
    </linearGradient>
  </defs>

  <!-- soft backdrop -->
  <circle cx="392" cy="228" r="196" fill="#E4F0F5"/>
  <circle cx="560" cy="106" r="46" fill="#FDEBE4"/>
  <circle cx="214" cy="352" r="30" fill="#E6F5EE"/>

  <!-- back card: the week -->
  <g transform="rotate(-7 300 210)">
    <rect x="176" y="118" width="196" height="180" rx="22" fill="url(#g2)" stroke="#D3DEE7"/>
    <rect x="198" y="146" width="86" height="12" rx="6" fill="#CBD6DF"/>
    <g fill="#E1E8EE">
      <rect x="198" y="176" width="34" height="30" rx="8"/><rect x="240" y="176" width="34" height="30" rx="8"/>
      <rect x="282" y="176" width="34" height="30" rx="8"/><rect x="198" y="214" width="34" height="30" rx="8"/>
    </g>
    <rect x="240" y="214" width="34" height="30" rx="8" fill="#39B0CF"/>
    <rect x="282" y="214" width="34" height="30" rx="8" fill="#F07A52"/>
    <rect x="198" y="252" width="118" height="12" rx="6" fill="#E1E8EE"/>
  </g>

  <!-- front card: the consultation note -->
  <g transform="rotate(4 460 240)">
    <rect x="352" y="122" width="252" height="216" rx="24" fill="#FFFFFF" stroke="#D3DEE7"/>
    <circle cx="392" cy="164" r="17" fill="#39B0CF"/>
    <rect x="420" y="155" width="104" height="11" rx="5.5" fill="#1B3A5B"/>
    <rect x="420" y="173" width="66" height="9" rx="4.5" fill="#CBD6DF"/>
    <rect x="376" y="204" width="204" height="9" rx="4.5" fill="#E1E8EE"/>
    <rect x="376" y="222" width="168" height="9" rx="4.5" fill="#E1E8EE"/>
    <rect x="376" y="240" width="188" height="9" rx="4.5" fill="#E1E8EE"/>
    <!-- ECG -->
    <path d="M376 288 h34 l10 -22 l14 46 l14 -60 l12 36 h108"
          fill="none" stroke="#F07A52" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="376" y="308" width="86" height="16" rx="8" fill="#E6F5EE"/>
    <rect x="470" y="308" width="60" height="16" rx="8" fill="#E4F0F5"/>
  </g>

  <!-- stethoscope arc -->
  <path d="M150 250 q-26 78 46 96 q66 16 78 -44" fill="none" stroke="url(#g1)"
        stroke-width="13" stroke-linecap="round"/>
  <circle cx="276" cy="296" r="22" fill="#1B3A5B"/>
  <circle cx="276" cy="296" r="10" fill="#39B0CF"/>
  <rect x="140" y="228" width="22" height="34" rx="11" fill="#245F88"/>

  <!-- floating pills -->
  <g transform="rotate(28 620 300)">
    <rect x="592" y="286" width="72" height="30" rx="15" fill="#F07A52"/>
    <rect x="628" y="286" width="36" height="30" rx="15" fill="#FDEBE4"/>
  </g>
  <g transform="rotate(-16 172 132)">
    <rect x="146" y="120" width="56" height="24" rx="12" fill="#39B0CF"/>
    <rect x="174" y="120" width="28" height="24" rx="12" fill="#D6ECF3"/>
  </g>

  <!-- check badge -->
  <circle cx="588" cy="372" r="30" fill="#2FA36B"/>
  <path d="M574 372 l10 11 l20 -23" fill="none" stroke="#FFFFFF" stroke-width="7"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""
cairosvg.svg2png(bytestring=ILLO.encode(), write_to=f"{IMG}/illo-welcome.png", output_width=1140)

# A compact square crop of the same language, for the mobile banner
ILLO_M = ILLO.replace('viewBox="0 0 760 460"', 'viewBox="150 90 470 330"')
cairosvg.svg2png(bytestring=ILLO_M.encode(), write_to=f"{IMG}/illo-welcome-m.png", output_width=760)

print("doctor imagery:", len(os.listdir(IMG)), "files")
