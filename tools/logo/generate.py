#!/usr/bin/env python3
"""Medra logo system generator — master mark + all variant forms (SVG + PNG)."""
import cairosvg, os

SVG_DIR = "/home/user/Medra-24/brand/svg"
PNG_DIR = "/home/user/Medra-24/brand/png"
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

# ---------------- palette ----------------
NAVY  = "#1b3a5b"
TEAL  = "#39b0cf"
DARKBG = "#0f2233"
STROKE_W = 66

# ---------------- artwork geometry ----------------
M_PATH = ("M 175 560 C 120 410 170 235 295 215 C 400 196 388 370 315 460 "
          "C 255 535 232 445 292 338 C 330 255 420 196 505 220 "
          "C 585 242 582 382 520 455 C 486 505 452 470 486 412 "
          "C 512 368 560 392 606 420")
CROSS_H = '<rect x="596" y="388" width="212" height="72" rx="24"/>'
CROSS_V = '<rect x="666" y="318" width="72" height="212" rx="24"/>'
ECG_FULL = "M 566 424 L 614 424 L 634 396 L 654 462 L 676 366 L 692 424 L 798 424"
ECG_CROSS = "M 600 424 L 614 424 L 634 396 L 654 462 L 676 366 L 692 424 L 798 424"

# content bbox (user units), used for tight framing
BB = (119.5, 180.5, 808.0, 593.0)
PAD = 46
VB_X = BB[0]-PAD; VB_Y = BB[1]-PAD
VB_W = (BB[2]-BB[0])+2*PAD; VB_H = (BB[3]-BB[1])+2*PAD

GRADS = f"""
  <linearGradient id="g" x1="120" y1="0" x2="800" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#1b3a5b"/><stop offset=".42" stop-color="#245f88"/>
    <stop offset=".72" stop-color="#2f8bac"/><stop offset="1" stop-color="#39b0cf"/>
  </linearGradient>
  <linearGradient id="gc" x1="600" y1="300" x2="800" y2="510" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#34a1c4"/><stop offset="1" stop-color="#3bb6d2"/>
  </linearGradient>"""

def mark_defs(mode):
    d = GRADS if mode == "gradient" else ""
    if mode != "gradient":
        # knockout mask so the ECG reads as negative space in one-colour marks
        d += f"""
  <mask id="ecg_ko" maskUnits="userSpaceOnUse" x="0" y="0" width="900" height="700">
    <rect x="0" y="0" width="900" height="700" fill="white"/>
    <path d="{ECG_CROSS}" fill="none" stroke="black" stroke-width="14"
          stroke-linecap="round" stroke-linejoin="round"/>
  </mask>"""
    return d

def mark_body(mode):
    if mode == "gradient":
        ribbon = f'<path d="{M_PATH}" fill="none" stroke="url(#g)" stroke-width="{STROKE_W}" stroke-linecap="round" stroke-linejoin="round"/>'
        cross  = f'<g fill="url(#gc)">{CROSS_H}{CROSS_V}</g>'
        ecg    = f'<path d="{ECG_FULL}" fill="none" stroke="#ffffff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
        return ribbon + cross + ecg
    c = {"navy": NAVY, "teal": TEAL, "black": "#111111", "white": "#ffffff"}[mode]
    ribbon = f'<path d="{M_PATH}" fill="none" stroke="{c}" stroke-width="{STROKE_W}" stroke-linecap="round" stroke-linejoin="round"/>'
    cross  = f'<g fill="{c}" mask="url(#ecg_ko)">{CROSS_H}{CROSS_V}</g>'
    return ribbon + cross

def mark_svg(mode="gradient", bg=None, vb=None, extra_defs="", pre="", post=""):
    x, y, w, h = vb or (VB_X, VB_Y, VB_W, VB_H)
    bgrect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}">'
            f'<defs>{mark_defs(mode)}{extra_defs}</defs>{bgrect}{pre}'
            f'{mark_body(mode)}{post}</svg>')

# ---------------- wordmark ----------------
def wordmark(color, x, y, size):
    return (f'<text x="{x}" y="{y}" font-family="DejaVu Sans, Arial, Helvetica, sans-serif" '
            f'font-weight="700" font-size="{size}" letter-spacing="{size*0.06:.1f}" '
            f'fill="{color}">MEDRA</text>')

def lockup_h(mode="gradient", bg=None, wm_color=NAVY):
    # mark scaled into left area, wordmark to the right
    mk = mark_svg(mode)
    # place mark via nested svg
    inner = (f'<svg x="0" y="0" width="470" height="360" viewBox="{VB_X:.1f} {VB_Y:.1f} {VB_W:.1f} {VB_H:.1f}"'
             f' overflow="visible"><defs>{mark_defs(mode)}</defs>{mark_body(mode)}</svg>')
    total_w, total_h = 1180, 360
    bgrect = f'<rect width="{total_w}" height="{total_h}" fill="{bg}"/>' if bg else ""
    wm = wordmark(wm_color, 500, 210, 132)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}">'
            f'{bgrect}{inner}{wm}</svg>')

def lockup_stacked(mode="gradient", bg=None, wm_color=NAVY):
    inner = (f'<svg x="180" y="0" width="440" height="330" viewBox="{VB_X:.1f} {VB_Y:.1f} {VB_W:.1f} {VB_H:.1f}"'
             f' overflow="visible"><defs>{mark_defs(mode)}</defs>{mark_body(mode)}</svg>')
    total_w, total_h = 800, 470
    bgrect = f'<rect width="{total_w}" height="{total_h}" fill="{bg}"/>' if bg else ""
    wm = (f'<text x="400" y="430" text-anchor="middle" font-family="DejaVu Sans, Arial, Helvetica, sans-serif" '
          f'font-weight="700" font-size="112" letter-spacing="7" fill="{wm_color}">MEDRA</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}">'
            f'{bgrect}{inner}{wm}</svg>')

def app_icon(mode="white", bg_fill='url(#bgrad)', radius=180):
    # square rounded icon, mark centred
    defs = ('<linearGradient id="bgrad" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#173350"/><stop offset="1" stop-color="#0f2233"/></linearGradient>')
    S = 1024
    inner = (f'<svg x="112" y="176" width="800" height="672" viewBox="{VB_X:.1f} {VB_Y:.1f} {VB_W:.1f} {VB_H:.1f}"'
             f' overflow="visible"><defs>{mark_defs(mode)}</defs>{mark_body(mode)}</svg>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">'
            f'<defs>{defs}</defs>'
            f'<rect width="{S}" height="{S}" rx="{radius}" fill="{bg_fill}"/>{inner}</svg>')

# ---------------- write helpers ----------------
def write(name, svg, png_sizes=()):
    p = os.path.join(SVG_DIR, name+".svg")
    open(p, "w").write(svg)
    for s in png_sizes:
        cairosvg.svg2png(bytestring=svg.encode(),
                         write_to=os.path.join(PNG_DIR, f"{name}-{s}.png"),
                         output_width=s)
    print("  ", name)

print("Master marks:")
write("medra-logo-primary",        mark_svg("gradient"),                 (1200, 512))
write("medra-logo-primary-onwhite",mark_svg("gradient", bg="#ffffff"),   (1200,))
write("medra-logo-primary-ondark", mark_svg("gradient", bg=DARKBG),      (1200,))
write("medra-logo-navy",           mark_svg("navy"),                     (512,))
write("medra-logo-teal",           mark_svg("teal"),                     (512,))
write("medra-logo-black",          mark_svg("black"),                    (512,))
write("medra-logo-white",          mark_svg("white"),                    ())
write("medra-logo-white-ondark",   mark_svg("white", bg=DARKBG),         (1200, 512))

print("Wordmark lockups:")
write("medra-lockup-horizontal",      lockup_h("gradient", wm_color=NAVY),          (1600,))
write("medra-lockup-horizontal-dark", lockup_h("gradient", bg=DARKBG, wm_color="#ffffff"), (1600,))
write("medra-lockup-stacked",         lockup_stacked("gradient", wm_color=NAVY),    (1200,))
write("medra-lockup-stacked-dark",    lockup_stacked("gradient", bg=DARKBG, wm_color="#ffffff"), (1200,))

print("App icon & favicons:")
write("medra-appicon",       app_icon("white"),                (1024, 512))
write("medra-appicon-light", app_icon("gradient", bg_fill="#ffffff"), (1024,))
fav = mark_svg("gradient")
open(os.path.join(SVG_DIR,"medra-favicon.svg"),"w").write(fav)
for s in (16,32,48,64,128,256):
    cairosvg.svg2png(bytestring=fav.encode(), write_to=os.path.join(PNG_DIR,f"medra-favicon-{s}.png"), output_width=s)
print("   medra-favicon (16-256)")

print("Done.")
