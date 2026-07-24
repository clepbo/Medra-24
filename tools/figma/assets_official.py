#!/usr/bin/env python3
"""Rasterise the official Medra logo SVGs + derive glow / app-icon / favicon / lockups.
Writes into the Figma bundle and the brand/ master set."""
import cairosvg, io, os, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

SRC   = "/home/user/Medra-24/assets/logo"          # official SVGs (user-provided)
FIG   = "/home/user/Medra-24/figma/medra-ds/assets/logo"
BRAND_SVG = "/home/user/Medra-24/brand/svg"
BRAND_PNG = "/home/user/Medra-24/brand/png"
for d in (FIG, BRAND_SVG, BRAND_PNG): os.makedirs(d, exist_ok=True)

SVGS = {
    "gradient": "Logo - Gradient.svg",
    "navy":     "Logo - Navy Blue.svg",
    "teal":     "Logo - Teal.svg",
    "white":    "Logo - White.svg",
    "inverse":  "Logo - Inverse.svg",
    "stroke":   "Logo - Stroke.svg",
}
NAVY = (27, 58, 91)
TEAL = (57, 176, 207)

def render(svg, w=1600):
    png = cairosvg.svg2png(url=os.path.join(SRC, svg), output_width=w)
    return Image.open(io.BytesIO(png)).convert("RGBA")

# 1. core PNGs (transparent) into the Figma bundle
marks = {}
for key, svg in SVGS.items():
    im = render(svg, 1600)
    im.save(os.path.join(FIG, f"logo-{key}.png"))
    marks[key] = im
# keep legacy name used by some frames
marks["gradient"].save(os.path.join(FIG, "logo-primary.png"))
print("core marks:", ", ".join(marks))

def add_glow(logo, teal=TEAL, opacity=0.30, radius=22, pad=90):
    W, H = logo.size
    canvas = Image.new("RGBA", (W + 2*pad, H + 2*pad), (0,0,0,0))
    canvas.paste(logo, (pad, pad), logo)
    ga = np.asarray(canvas.split()[3].filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)/255.0*opacity
    Wc, Hc = canvas.size
    glow = np.dstack([np.full((Hc,Wc),teal[0],np.uint8), np.full((Hc,Wc),teal[1],np.uint8),
                      np.full((Hc,Wc),teal[2],np.uint8), (ga*255).astype(np.uint8)])
    return Image.alpha_composite(Image.fromarray(glow,"RGBA"), canvas)

# 2. glow variants
add_glow(marks["white"]).save(os.path.join(FIG, "hero-white-glow.png"))
add_glow(marks["gradient"], opacity=0.20, radius=24).save(os.path.join(FIG, "logo-primary-glow.png"))

# 3. app icon — white mark on dark rounded square
def app_icon(S=1024, radius=180):
    bg = Image.new("RGBA", (S, S), (0,0,0,0))
    d = ImageDraw.Draw(bg)
    # vertical dark gradient
    top, bot = (23,51,80), (15,34,51)
    grad = Image.new("RGB", (1, S))
    for y in range(S):
        t = y/S
        grad.putpixel((0,y), tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    grad = grad.resize((S,S))
    mask = Image.new("L", (S,S), 0); ImageDraw.Draw(mask).rounded_rectangle([0,0,S,S], radius=radius, fill=255)
    bg.paste(grad, (0,0), mask)
    mk = marks["white"].copy(); mw = int(S*0.66); mk.thumbnail((mw, mw))
    bg.alpha_composite(mk, ((S-mk.width)//2, (S-mk.height)//2))
    return bg
app_icon().save(os.path.join(FIG, "appicon.png"))

# 4. favicon (gradient mark, tight) into brand png
fav = marks["gradient"]
for s in (16,32,48,64,128,256):
    fav.resize((s, int(s*fav.height/fav.width))).save(os.path.join(BRAND_PNG, f"medra-favicon-{s}.png"))

# 5. lockups — mark + MEDRA wordmark
def font(sz):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
def wordmark_img(color=NAVY, h=150, tracking=8):
    text="MEDRA"; f=font(h)
    tmp=Image.new("RGBA",(2000,int(h*1.6)),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    x=0;
    for ch in text:
        d.text((x,0),ch,font=f,fill=color+(255,)); x+=int(d.textlength(ch,font=f))+tracking
    bbox=tmp.getbbox(); return tmp.crop(bbox)
def lockup_h(mark, wm_color=NAVY):
    m=mark.copy(); mh=300; m.thumbnail((10000,mh))
    wm=wordmark_img(wm_color, h=150); gap=48
    W=m.width+gap+wm.width; H=max(m.height, wm.height)
    c=Image.new("RGBA",(W,H),(0,0,0,0))
    c.alpha_composite(m,(0,(H-m.height)//2))
    c.alpha_composite(wm,(m.width+gap,(H-wm.height)//2))
    return c
def lockup_stacked(mark, wm_color=NAVY):
    m=mark.copy(); mh=300; m.thumbnail((10000,mh))
    wm=wordmark_img(wm_color, h=120, tracking=10); gap=36
    W=max(m.width, wm.width); H=m.height+gap+wm.height
    c=Image.new("RGBA",(W,H),(0,0,0,0))
    c.alpha_composite(m,((W-m.width)//2,0))
    c.alpha_composite(wm,((W-wm.width)//2,m.height+gap))
    return c
lockup_h(marks["gradient"]).save(os.path.join(FIG,"lockup-horizontal.png"))
lockup_stacked(marks["gradient"]).save(os.path.join(FIG,"lockup-stacked.png"))
lockup_h(marks["white"], wm_color=(255,255,255)).save(os.path.join(FIG,"lockup-horizontal-white.png"))

# 6. refresh brand/ master set with the OFFICIAL svgs + png exports
import shutil
rename = {"gradient":"medra-logo-primary","navy":"medra-logo-navy","teal":"medra-logo-teal",
          "white":"medra-logo-white","inverse":"medra-logo-inverse","stroke":"medra-logo-stroke"}
for key, svg in SVGS.items():
    shutil.copy(os.path.join(SRC, svg), os.path.join(BRAND_SVG, rename[key]+".svg"))
    marks[key].resize((1200,int(1200*marks[key].height/marks[key].width))).save(os.path.join(BRAND_PNG, rename[key]+".png"))
app_icon().save(os.path.join(BRAND_PNG,"medra-appicon.png"))
lockup_h(marks["gradient"]).save(os.path.join(BRAND_PNG,"medra-lockup-horizontal.png"))
lockup_stacked(marks["gradient"]).save(os.path.join(BRAND_PNG,"medra-lockup-stacked.png"))

print("aspect", round(marks['gradient'].width/marks['gradient'].height,3))
print("done")
