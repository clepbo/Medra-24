#!/usr/bin/env python3
"""Generate the Medra design-system .jsx frames (Editorial Light). One file = one frame."""
import os, re
OUT = "/home/user/Medra-24/figma/medra-ds"
os.makedirs(OUT, exist_ok=True)

# ---------- helpers ----------
def sideband():
    return ('<Frame w={64} h="fill" bg="var:bg/band" flex="col" justify="between" items="center" pt={40} pb={40}>'
            '<Image image="assets/logo/appicon.png" w={36} h={36} rounded={8} />'
            '<Frame flex="col" gap={8} items="center">'
            '<Rect w={4} h={80} bg="var:brand/teal" rounded={999} />'
            '</Frame>'
            '</Frame>')

def hairline():
    return ('<Frame w="fill" flex="row" gap={0} items="center">'
            '<Rect w={72} h={3} bg="var:brand/teal" rounded={999} />'
            '<Rect grow={1} h={1} bg="var:border/subtle" />'
            '</Frame>')

def header(num, kicker, title, sub=None):
    subrow = (f'<Text font="Inter" size={{16}} weight="regular" color="var:text/muted" w="fill">{sub}</Text>'
              if sub else '')
    return (f'<Frame w="fill" flex="row" justify="between" items="start">'
            f'<Frame flex="col" gap={{10}} grow={{1}}>'
            f'<Text font="Inter" size={{13}} weight="semibold" color="var:text/accent">{kicker}</Text>'
            f'<Text font="Inter" size={{46}} weight="bold" color="var:text/strong">{title}</Text>'
            f'{subrow}'
            f'</Frame>'
            f'<Text font="Inter" size={{150}} weight="bold" color="var:neutral/100">{num}</Text>'
            f'</Frame>'
            f'{hairline()}')

def footer(next_label="Next"):
    return ('<Frame w="fill" flex="row" justify="between" items="center" pt={16}>'
            '<Frame name="Btn Contents" flex="row" gap={8} items="center" px={16} py={10} rounded={999} bg="var:bg/subtle" stroke="var:border/default" strokeWidth={1}>'
            '<Icon name="lucide:layout-dashboard" size={16} color="#5B6B7A" />'
            '<Text font="Inter" size={14} weight="semibold" color="var:text/default">Contents</Text>'
            '</Frame>'
            '<Text font="Inter" size={12} weight="regular" color="var:text/faint">Medra Design System · v1.0</Text>'
            f'<Frame name="Btn Next" flex="row" gap={{8}} items="center" px={{18}} py={{10}} rounded={{999}} bg="var:brand/navy">'
            f'<Text font="Inter" size={{14}} weight="semibold" color="var:text/on-dark">{next_label}</Text>'
            '<Icon name="lucide:arrow-right" size={16} color="#FFFFFF" />'
            '</Frame>'
            '</Frame>')

def frame(name, body, pad=True):
    inner_pad = 'pl={72} pr={72} pt={56} pb={40}' if pad else ''
    return (f'<Frame name="{name}" w={{1440}} minH={{1024}} flex="row" bg="var:bg/base">'
            f'{sideband()}'
            f'<Frame grow={{1}} h="fill" flex="col" gap={{28}} {inner_pad}>'
            f'{body}'
            f'</Frame>'
            f'</Frame>')

def card(children, grow=1, bg="var:bg/base", pad=24, gap=14, extra=""):
    return (f'<Frame {("grow={%d}"%grow) if grow else ""} flex="col" gap={{{gap}}} p={{{pad}}} '
            f'rounded={{16}} bg="{bg}" stroke="var:border/subtle" strokeWidth={{1}} {extra}>{children}</Frame>')

def swatch(name, hexv, token, dark=False):
    txt = "var:text/on-dark" if dark else "var:text/strong"
    sub = "var:text/on-dark-muted" if dark else "var:text/muted"
    return (f'<Frame w={{212}} flex="col" gap={{0}} rounded={{14}} overflow="hidden" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Rect w="fill" h={{120}} bg="{hexv}" />'
            f'<Frame w="fill" flex="col" gap={{2}} p={{14}} bg="var:bg/base">'
            f'<Text font="Inter" size={{15}} weight="semibold" color="var:text/strong">{name}</Text>'
            f'<Text font="Inter" size={{13}} weight="regular" color="var:text/muted">{hexv.upper()}</Text>'
            f'<Text font="Inter" size={{12}} weight="regular" color="var:text/faint">{token}</Text>'
            f'</Frame>'
            f'</Frame>')

frames = []  # (order, filename, jsx)

# ============================================================ 00 COVER
cover = (f'<Frame name="Medra DS — 00 Cover" w={{1440}} minH={{1024}} flex="row" bg="var:bg/base">'
    f'{sideband()}'
    '<Frame grow={1} h="fill" flex="row" items="center">'
      '<Frame grow={1} h="fill" flex="col" justify="between" pl={72} pr={56} pt={72} pb={72}>'
        '<Frame flex="col" gap={12}>'
          '<Text font="Inter" size={13} weight="semibold" color="var:text/accent">MEDRA · BRAND &amp; DESIGN SYSTEM</Text>'
          '<Rect w={56} h={3} bg="var:brand/teal" rounded={999} />'
        '</Frame>'
        '<Frame flex="col" gap={18}>'
          '<Text font="Inter" size={132} weight="bold" color="var:text/strong">Medra</Text>'
          '<Text font="Inter" size={22} weight="regular" color="var:text/muted" w={520}>A unified medical records &amp; consultation-booking platform for Nigeria. Brand &amp; design system — Version 1.0</Text>'
        '</Frame>'
        '<Frame flex="col" gap={6}>'
          '<Text font="Inter" size={17} weight="semibold" color="var:text/default">Every touchpoint is a brand touchpoint.</Text>'
          '<Text font="Inter" size={13} weight="regular" color="var:text/faint">medra.health · Abuja, Nigeria · 2026</Text>'
        '</Frame>'
      '</Frame>'
      '<Frame w={600} h="fill" bg="var:bg/subtle" overflow="hidden" flex="col" justify="center" items="center" p={40}>'
        '<Image image="assets/logo/logo-primary-glow.png" w={520} h={399} />'
      '</Frame>'
    '</Frame>'
  '</Frame>')
frames.append((0,"00-cover.jsx",cover))

# ============================================================ 01 CONTENTS
def toc_row(num, title, desc):
    return (f'<Frame name="Nav {title}" w="fill" flex="row" gap={{20}} items="center" px={{20}} py={{18}} rounded={{14}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Text font="Inter" size={{22}} weight="bold" color="var:brand/teal" w={{44}}>{num}</Text>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>'
            f'<Text font="Inter" size={{18}} weight="semibold" color="var:text/strong">{title}</Text>'
            f'<Text font="Inter" size={{13}} weight="regular" color="var:text/muted">{desc}</Text>'
            f'</Frame>'
            f'<Icon name="lucide:chevron-right" size={{20}} color="#39B0CF" />'
            f'</Frame>')
toc_left = "".join([
    toc_row("02","Brand Story","Purpose, positioning & voice"),
    toc_row("03","Brand Goals","The pillars behind Medra"),
    toc_row("04","Logo System","Primary, mark, construction"),
    toc_row("06","Colour","Palette & semantic colour"),
    toc_row("10","Gradient & Elevation","Signature gradient, surfaces"),
])
toc_right = "".join([
    toc_row("11","Typography","Typeface, scale & hierarchy"),
    toc_row("13","Iconography","Lucide icon system"),
    toc_row("14","Layout","Grid, spacing & radius"),
    toc_row("15","Components","Buttons, forms, cards, alerts"),
    toc_row("19","Imagery & Contact","Photography direction"),
])
contents_body = (header("","INDEX","Table of Contents","A creative, product-grounded system — from brand foundations to production-ready UI components.")
    + '<Frame w="fill" flex="row" gap={20} items="start">'
      f'<Frame grow={{1}} flex="col" gap={{14}}>{toc_left}</Frame>'
      f'<Frame grow={{1}} flex="col" gap={{14}}>{toc_right}</Frame>'
    '</Frame>'
    + footer())
frames.append((1,"01-contents.jsx",frame("Medra DS — 01 Contents", contents_body)))

# ============================================================ 02 BRAND STORY
def pill(text):
    return (f'<Frame flex="row" gap={{8}} items="center" px={{16}} py={{10}} rounded={{999}} bg="var:bg/muted">'
            f'<Icon name="lucide:heart-pulse" size={{16}} color="#2F8BAC" />'
            f'<Text font="Inter" size={{14}} weight="medium" color="var:text/default">{text}</Text></Frame>')
story_body = (header("02","THE BRAND","Brand Story")
    + '<Frame w="fill" flex="row" gap={28} items="start">'
      '<Frame grow={1} flex="col" gap={22}>'
        '<Text font="Inter" size={30} weight="bold" color="var:text/strong" w="fill">One record. Every doctor. No paper.</Text>'
        '<Text font="Inter" size={17} weight="regular" color="var:text/muted" w="fill">Medra replaces paper filing and WhatsApp booking with a single system for finding care, booking consultations, and carrying a portable medical history. Booking is the entry point — the durable value is a unified medical database that follows the patient across providers.</Text>'
        '<Frame w="fill" flex="row" gap={12} wrap="wrap">'
          + pill("Trustworthy") + pill("Clinical, not cold") + pill("Clear over clever") + pill("Human") +
        '</Frame>'
      '</Frame>'
      '<Frame w={420} flex="col" gap={16} p={28} rounded={20} image="assets/img/gradient-diag.png" overflow="hidden">'
        '<Icon name="lucide:activity" size={28} color="#FFFFFF" />'
        '<Text font="Inter" size={26} weight="bold" color="var:text/on-dark" w="fill">“Every touchpoint is a brand touchpoint.”</Text>'
        '<Text font="Inter" size={14} weight="regular" color="var:text/on-dark-muted" w="fill">From the booking button to the SMS reminder, every moment should feel safe, precise, and unmistakably Medra.</Text>'
      '</Frame>'
    '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Voice</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Plain, reassuring, exact. We explain, we never alarm.</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Tone</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Warm authority — a good doctor, not a machine.</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Promise</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Your history, wherever you are cared for.</Text>')
    + '</Frame>'
    + footer())
frames.append((2,"02-brand-story.jsx",frame("Medra DS — 02 Brand Story", story_body)))

# ============================================================ 03 BRAND GOALS
def goal(icon, title, desc):
    return (f'<Frame grow={{1}} flex="col" gap={{14}} p={{26}} rounded={{18}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{52}} h={{52}} rounded={{14}} bg="var:bg/muted" flex="col" justify="center" items="center">'
            f'<Icon name="{icon}" size={{24}} color="#2F8BAC" /></Frame>'
            f'<Text font="Inter" size={{18}} weight="semibold" color="var:text/strong">{title}</Text>'
            f'<Text font="Inter" size={{14}} weight="regular" color="var:text/muted" w="fill">{desc}</Text></Frame>')
goals_body = (header("03","WHY WE EXIST","Brand Goals","Four pillars that every product and design decision must serve.")
    + '<Frame w="fill" flex="row" gap={16}>'
      + goal("lucide:search","Find care fast","One place to find verified doctors and institutions with real, bookable availability.")
      + goal("lucide:calendar-check","Book before leaving home","See open slots and confirm — in-person or virtual — before travelling.")
      + goal("lucide:clipboard-list","Carry your history","A continuous, structured record any authorised doctor can read to decide safely.")
      + goal("lucide:shield-check","Protect the data","Consent, access control and audit built in — medical data treated as sacred.")
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16} image="assets/img/pulse-navy.png" overflow="hidden" rounded={18} p={28} items="center" justify="between">'
      '<Frame flex="col" gap={6}>'
        '<Text font="Inter" size={22} weight="bold" color="var:text/on-dark">The core loop</Text>'
        '<Text font="Inter" size={14} weight="regular" color="var:text/on-dark-muted">Search → see availability → book → attend → record written → history readable.</Text>'
      '</Frame>'
      '<Icon name="lucide:heart-pulse" size={40} color="#39B0CF" />'
    '</Frame>'
    + footer())
frames.append((3,"03-brand-goals.jsx",frame("Medra DS — 03 Brand Goals", goals_body)))

# ============================================================ 04 LOGO PRIMARY
logo_body = (header("04","IDENTITY","Logo — Primary","The Medra mark: a script “M” ribbon flowing into a medical cross with an ECG pulse.")
    + '<Frame w="fill" flex="row" gap={20}>'
      '<Frame grow={1} h={360} rounded={20} bg="var:bg/subtle" stroke="var:border/subtle" strokeWidth={1} flex="col" justify="center" items="center">'
        '<Image image="assets/logo/logo-gradient.png" w={360} h={267} />'
      '</Frame>'
      '<Frame w={360} h={360} rounded={20} bg="var:bg/band" overflow="hidden" flex="col" justify="center" items="center">'
        '<Image image="assets/logo/logo-white.png" w={300} h={223} />'
      '</Frame>'
    '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Meaning</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">The looping “M” is continuity of care; the cross + pulse signal medical trust and life.</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Gradient</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Navy → teal, left to right. Never reorder or recolour the gradient.</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Minimum size</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Use the app-icon below 32px; the script detail muddies when tiny.</Text>')
    + '</Frame>'
    + footer())
frames.append((4,"04-logo-primary.jsx",frame("Medra DS — 04 Logo Primary", logo_body)))

# ============================================================ 05 LOGO CONSTRUCTION
constr_body = (header("05","IDENTITY","Logo — Construction &amp; Clear Space","Protect the mark with clear space equal to the height of the cross on every side.")
    + '<Frame w="fill" flex="row" gap={20}>'
      '<Frame grow={1} h={380} rounded={20} bg="var:bg/base" stroke="var:border/default" strokeWidth={1} flex="col" justify="center" items="center" p={40}>'
        '<Frame p={40} rounded={16} stroke="var:brand/teal" strokeWidth={2} bg="var:bg/subtle" flex="col" justify="center" items="center">'
          '<Image image="assets/logo/logo-gradient.png" w={300} h={223} />'
        '</Frame>'
        '<Text font="Inter" size={13} weight="regular" color="var:text/faint" >Clear space = height of the cross (X)</Text>'
      '</Frame>'
      '<Frame w={360} flex="col" gap={16}>'
        + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Clear space</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Keep padding of at least 1× the cross height around the mark. Never crowd it.</Text>', grow=0)
        + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Alignment</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Optically centre on the ribbon mass, not the bounding box.</Text>', grow=0)
        + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Scaling</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Always scale proportionally. Never stretch, skew or rotate.</Text>', grow=0)
      + '</Frame>'
    + '</Frame>'
    + footer())
frames.append((5,"05-logo-construction.jsx",frame("Medra DS — 05 Logo Construction", constr_body)))

# ============================================================ 06 LOGO VARIATIONS
def logo_tile(img, label, dark=False, gradient=False):
    if gradient:
        bg='image="assets/img/gradient-hero.png" overflow="hidden"'
    elif dark:
        bg='bg="var:bg/band"'
    else:
        bg='bg="var:bg/subtle" stroke="var:border/subtle" strokeWidth={1}'
    lblcol = "var:text/on-dark" if (dark or gradient) else "var:text/default"
    return (f'<Frame grow={{1}} flex="col" gap={{12}} items="center" justify="center" h={{200}} rounded={{16}} {bg}>'
            f'<Image image="{img}" w={{180}} h={{135}} />'
            f'<Text font="Inter" size={{13}} weight="medium" color="{lblcol}">{label}</Text></Frame>')
var_body = (header("06","IDENTITY","Logo — Variations","Use the version with the strongest contrast for its background. Never invent new colourways.")
    + '<Frame w="fill" flex="row" gap={16}>'
      + logo_tile("assets/logo/logo-gradient.png","Primary gradient")
      + logo_tile("assets/logo/logo-navy.png","Navy blue")
      + logo_tile("assets/logo/logo-teal.png","Solid teal")
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + logo_tile("assets/logo/logo-white.png","Reverse / white", dark=True)
      + logo_tile("assets/logo/logo-inverse.png","Inverse")
      + logo_tile("assets/logo/logo-stroke.png","Stroke")
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Lockups</Text>'
             '<Frame w="fill" flex="row" gap={24} items="center" pt={4}>'
             '<Image image="assets/logo/lockup-horizontal.png" w={280} h={78} />'
             '<Image image="assets/logo/lockup-stacked.png" w={150} h={124} />'
             '</Frame>')
    + '</Frame>'
    + footer())
frames.append((6,"06-logo-variations.jsx",frame("Medra DS — 06 Logo Variations", var_body)))

# ============================================================ 07 LOGO MISUSE
def dont(icon, text):
    return (f'<Frame grow={{1}} flex="col" gap={{12}} p={{22}} rounded={{16}} bg="var:state/error-bg" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{40}} h={{40}} rounded={{999}} bg="var:bg/base" flex="col" justify="center" items="center">'
            f'<Icon name="lucide:ban" size={{20}} color="#D14343" /></Frame>'
            f'<Text font="Inter" size={{14}} weight="medium" color="var:text/default" w="fill">{text}</Text></Frame>')
misuse_body = (header("07","IDENTITY","Logo — Misuse","The mark is fixed. These are always wrong.")
    + '<Frame w="fill" flex="row" gap={16}>'
      + dont("x","Don’t stretch, squash or skew the mark.")
      + dont("x","Don’t rotate or flip the logo.")
      + dont("x","Don’t recolour outside the brand palette.")
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + dont("x","Don’t add drop shadows, glows or outlines.")
      + dont("x","Don’t place the gradient mark on a busy photo — use reverse.")
      + dont("x","Don’t reorder the gradient (teal must end at the cross).")
    + '</Frame>'
    + footer())
frames.append((7,"07-logo-misuse.jsx",frame("Medra DS — 07 Logo Misuse", misuse_body)))

# ============================================================ 08 COLOUR PRIMARY
col_primary = (header("08","FOUNDATIONS","Colour — Primary","The navy-to-teal spectrum carries the brand. Navy grounds, teal energises.")
    + '<Frame w="fill" flex="row" gap={14} wrap="wrap">'
      + swatch("Navy Deep","#0F2233","brand/navy-deep")
      + swatch("Navy","#1B3A5B","brand/navy")
      + swatch("Blue","#245F88","brand/blue")
      + swatch("Blue Light","#2F8BAC","brand/blue-light")
      + swatch("Teal","#39B0CF","brand/teal")
      + swatch("Teal Bright","#3BB6D2","brand/teal-bright")
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Primary — Navy #1B3A5B</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Headlines, primary buttons, the deep end of the gradient and dark surfaces.</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Accent — Teal #39B0CF</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Highlights, active states, links, the ECG pulse and the bright end of the gradient.</Text>')
    + '</Frame>'
    + footer())
frames.append((8,"08-colour-primary.jsx",frame("Medra DS — 08 Colour Primary", col_primary)))

# ============================================================ 09 COLOUR SECONDARY / SEMANTIC
def semantic(name, hexv, token, icon):
    return (f'<Frame grow={{1}} flex="col" gap={{12}} p={{20}} rounded={{16}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame flex="row" gap={{10}} items="center">'
            f'<Frame w={{36}} h={{36}} rounded={{10}} bg="{hexv}" flex="col" justify="center" items="center"><Icon name="{icon}" size={{18}} color="#FFFFFF" /></Frame>'
            f'<Frame flex="col" gap={{0}}><Text font="Inter" size={{15}} weight="semibold" color="var:text/strong">{name}</Text>'
            f'<Text font="Inter" size={{12}} weight="regular" color="var:text/muted">{hexv.upper()} · {token}</Text></Frame>'
            f'</Frame></Frame>')
col_sec = (header("09","FOUNDATIONS","Colour — Semantic &amp; Neutrals","Status colours map to real Medra states; neutrals build the calm, clinical canvas.")
    + '<Frame w="fill" flex="row" gap={14}>'
      + semantic("Success · Verified","#2FA36B","state/success","lucide:circle-check")
      + semantic("Warning · Pending","#E0A32E","state/warning","lucide:circle-alert")
      + semantic("Error · No-show","#D14343","state/error","lucide:triangle-alert")
      + semantic("Info · Virtual","#2F8BAC","state/info","lucide:info")
    + '</Frame>'
    + '<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Neutral scale</Text>'
    + '<Frame w="fill" flex="row" gap={0} rounded={14} overflow="hidden" stroke="var:border/subtle" strokeWidth={1}>'
      + "".join([f'<Frame grow={{1}} h={{72}} bg="{h}" flex="col" justify="end" p={{8}}><Text font="Inter" size={{11}} weight="medium" color="{"#FFFFFF" if i>=4 else "#0F2233"}">{s}</Text></Frame>'
                 for i,(s,h) in enumerate([("50","#F7F9FB"),("100","#EEF2F6"),("200","#E1E8EE"),("300","#CBD6DF"),("400","#A7B6C2"),("500","#7E8F9D"),("600","#5B6B7A"),("700","#3E4C59"),("800","#26323D"),("900","#0F2233")])])
    + '</Frame>'
    + footer())
frames.append((9,"09-colour-semantic.jsx",frame("Medra DS — 09 Colour Semantic", col_sec)))

# ============================================================ 10 GRADIENT & ELEVATION
grad_body = (header("10","FOUNDATIONS","Gradient &amp; Elevation","The signature gradient is the brand’s hero surface. Elevation stays soft and subtle.")
    + '<Frame w="fill" flex="row" gap={16}>'
      '<Frame grow={1} h={200} rounded={18} image="assets/img/gradient-h.png" overflow="hidden" flex="col" justify="end" p={22}>'
        '<Text font="Inter" size={16} weight="semibold" color="var:text/on-dark">Horizontal · Navy → Teal</Text>'
        '<Text font="Inter" size={13} weight="regular" color="var:text/on-dark-muted">Banners, hero panels, empty-state backgrounds</Text>'
      '</Frame>'
      '<Frame w={260} h={200} rounded={18} image="assets/img/gradient-diag.png" overflow="hidden" flex="col" justify="end" p={22}>'
        '<Text font="Inter" size={16} weight="semibold" color="var:text/on-dark">Diagonal 55°</Text>'
        '<Text font="Inter" size={13} weight="regular" color="var:text/on-dark-muted">Cards & tiles</Text>'
      '</Frame>'
    '</Frame>'
    + '<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Elevation (soft, low-spread)</Text>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + '<Frame grow={1} flex="col" gap={12} p={22} rounded={16} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}><Text font="Inter" size={14} weight="semibold" color="var:text/strong">E0 · Flat</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted" w="fill">Border only. Base surfaces & wells.</Text></Frame>'
      + '<Frame grow={1} flex="col" gap={12} p={22} rounded={16} bg="var:bg/base" stroke="var:border/default" strokeWidth={1}><Text font="Inter" size={14} weight="semibold" color="var:text/strong">E1 · Card</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted" w="fill">y2 · blur8 · navy 6%. Cards, list items.</Text></Frame>'
      + '<Frame grow={1} flex="col" gap={12} p={22} rounded={16} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1}><Text font="Inter" size={14} weight="semibold" color="var:text/strong">E2 · Popover</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted" w="fill">y8 · blur24 · navy 12%. Menus, dialogs.</Text></Frame>'
    + '</Frame>'
    + '<Text font="Inter" size={12} weight="regular" color="var:text/faint">Shadow values are specs for build — Figma layers apply them as effects (soft navy, never pure black).</Text>'
    + footer())
frames.append((10,"10-gradient-elevation.jsx",frame("Medra DS — 10 Gradient Elevation", grad_body)))

# ============================================================ 11 TYPOGRAPHY TYPEFACE
type_body = (header("11","FOUNDATIONS","Typography — Typeface","Inter across the system — geometric, legible at small sizes, calm at large ones.")
    + '<Frame w="fill" flex="row" gap={16}>'
      '<Frame grow={1} flex="col" gap={10} p={30} rounded={18} bg="var:bg/subtle" stroke="var:border/subtle" strokeWidth={1}>'
        '<Text font="Inter" size={120} weight="bold" color="var:text/strong">Aa</Text>'
        '<Text font="Inter" size={16} weight="semibold" color="var:text/default">Inter</Text>'
        '<Text font="Inter" size={14} weight="regular" color="var:text/muted">Primary typeface · headings &amp; body</Text>'
        '<Text font="Inter" size={15} weight="regular" color="var:text/muted" w="fill">ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 ₦ + —</Text>'
      '</Frame>'
      '<Frame w={340} flex="col" gap={12}>'
        + card('<Text font="Inter" size={22} weight="bold" color="var:text/strong">Bold</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted">Headlines, numbers, primary CTAs</Text>', grow=0)
        + card('<Text font="Inter" size={22} weight="semibold" color="var:text/strong">Semibold</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted">Sub-heads, labels, card titles</Text>', grow=0)
        + card('<Text font="Inter" size={22} weight="medium" color="var:text/strong">Medium</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted">Buttons, chips, nav</Text>', grow=0)
        + card('<Text font="Inter" size={22} weight="regular" color="var:text/strong">Regular</Text><Text font="Inter" size={13} weight="regular" color="var:text/muted">Body &amp; long-form</Text>', grow=0)
      + '</Frame>'
    + '</Frame>'
    + footer())
frames.append((11,"11-typography-typeface.jsx",frame("Medra DS — 11 Typography Typeface", type_body)))

# ============================================================ 12 TYPOGRAPHY SCALE
def type_row(label, size, weight, sample):
    return (f'<Frame w="fill" flex="row" gap={{24}} items="center" px={{20}} py={{16}} rounded={{14}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{150}} flex="col" gap={{2}}><Text font="Inter" size={{14}} weight="semibold" color="var:text/strong">{label}</Text>'
            f'<Text font="Inter" size={{12}} weight="regular" color="var:text/muted">{size} · {weight}</Text></Frame>'
            f'<Text font="Inter" size={{{size}}} weight="{weight}" color="var:text/strong" grow={{1}}>{sample}</Text></Frame>')
scale_body = (header("12","FOUNDATIONS","Typography — Scale","A tight modular scale. Sizes in px; line-height 1.3–1.5 by role.")
    + '<Frame w="fill" flex="col" gap={12}>'
      + type_row("Display", 64, "bold", "Book before you leave")
      + type_row("H1 · Page", 40, "bold", "Find a verified doctor")
      + type_row("H2 · Section", 30, "bold", "Upcoming appointments")
      + type_row("H3 · Sub", 22, "semibold", "Consultation note")
      + type_row("Title", 18, "semibold", "Dr. Ngozi Okafor")
      + type_row("Body", 16, "regular", "Your next visit is Tuesday, 10:30 AM.")
      + type_row("Caption", 13, "medium", "VERIFIED · MDCN 45201")
    + '</Frame>'
    + footer())
frames.append((12,"12-typography-scale.jsx",frame("Medra DS — 12 Typography Scale", scale_body)))

# ============================================================ 13 ICONOGRAPHY
icon_names = ["activity","heart-pulse","stethoscope","calendar-days","calendar-check","clock",
    "user","users","user-check","search","filter","map-pin","building-2","hospital",
    "shield-check","badge-check","bell","message-square-text","video","phone","credit-card",
    "wallet","lock","settings","file-text","pill","syringe","thermometer","clipboard-list",
    "star","image","eye","download","share-2","house","log-out"]
def icon_cell(n):
    return (f'<Frame w={{96}} h={{88}} flex="col" gap={{10}} justify="center" items="center" rounded={{14}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Icon name="lucide:{n}" size={{24}} color="#1B3A5B" />'
            f'<Text font="Inter" size={{10}} weight="regular" color="var:text/muted">{n}</Text></Frame>')
icon_body = (header("13","FOUNDATIONS","Iconography","Lucide, 1.75px stroke, 24px grid. Rounded caps to echo the mark. Navy default, teal when active.")
    + '<Frame w="fill" flex="row" gap={12} wrap="wrap">'
      + "".join(icon_cell(n) for n in icon_names)
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Sizes</Text><Frame flex="row" gap={18} items="center" pt={4}><Icon name="lucide:heart-pulse" size={16} color="#1B3A5B" /><Icon name="lucide:heart-pulse" size={20} color="#1B3A5B" /><Icon name="lucide:heart-pulse" size={24} color="#1B3A5B" /><Icon name="lucide:heart-pulse" size={32} color="#1B3A5B" /></Frame><Text font="Inter" size={13} weight="regular" color="var:text/muted">16 · 20 · 24 · 32</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">States</Text><Frame flex="row" gap={18} items="center" pt={4}><Icon name="lucide:calendar-check" size={24} color="#5B6B7A" /><Icon name="lucide:calendar-check" size={24} color="#1B3A5B" /><Icon name="lucide:calendar-check" size={24} color="#39B0CF" /></Frame><Text font="Inter" size={13} weight="regular" color="var:text/muted">Muted · Default · Active</Text>')
    + '</Frame>'
    + footer())
frames.append((13,"13-iconography.jsx",frame("Medra DS — 13 Iconography", icon_body)))

# ============================================================ 14 LAYOUT GRID & SPACING
def space_chip(n):
    return (f'<Frame flex="col" gap={{8}} items="center">'
            f'<Rect w={{n}} h={{40}} bg="var:brand/teal" rounded={{4}} />'
            f'<Text font="Inter" size={{12}} weight="medium" color="var:text/muted">{n}</Text></Frame>')
def radius_chip(r,label):
    return (f'<Frame flex="col" gap={{8}} items="center">'
            f'<Rect w={{72}} h={{72}} bg="var:bg/muted" stroke="var:border/default" strokeWidth={{1}} rounded={{r}} />'
            f'<Text font="Inter" size={{12}} weight="medium" color="var:text/muted">{label}</Text></Frame>')
layout_body = (header("14","FOUNDATIONS","Layout — Grid, Spacing &amp; Radius","A 4-pt spacing base and a 12-column grid keep every screen on rhythm.")
    + '<Frame w="fill" flex="row" gap={16}>'
      '<Frame grow={1} flex="col" gap={14} p={22} rounded={16} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
        '<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Spacing scale · 4-pt base</Text>'
        '<Frame flex="row" gap={16} items="end">'
          + space_chip(4)+space_chip(8)+space_chip(12)+space_chip(16)+space_chip(24)+space_chip(32)+space_chip(48)+space_chip(64) +
        '</Frame>'
      '</Frame>'
    '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      '<Frame grow={1} flex="col" gap={14} p={22} rounded={16} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
        '<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Corner radius</Text>'
        '<Frame flex="row" gap={20} items="center">'
          + radius_chip(8,"8 · sm")+radius_chip(12,"12 · md")+radius_chip(16,"16 · lg")+radius_chip(24,"24 · xl")+radius_chip(999,"pill") +
        '</Frame>'
      '</Frame>'
      '<Frame w={420} flex="col" gap={10} p={22} rounded={16} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
        '<Text font="Inter" size={15} weight="semibold" color="var:text/strong">12-column grid</Text>'
        '<Frame w="fill" flex="row" gap={8}>'
          + "".join('<Rect grow={1} h={90} bg="var:state/info-bg" rounded={4} />' for _ in range(12)) +
        '</Frame>'
        '<Text font="Inter" size={13} weight="regular" color="var:text/muted">72px margins · 24px gutter · 1440 canvas</Text>'
      '</Frame>'
    '</Frame>'
    + footer())
frames.append((14,"14-layout-grid.jsx",frame("Medra DS — 14 Layout Grid", layout_body)))

# ============================================================ 15 COMPONENTS BUTTONS
def btn(label, kind, icon=None):
    ic = f'<Icon name="lucide:{icon}" size={{16}} color="{"#FFFFFF" if kind in ("primary","danger") else "#1B3A5B" if kind=="secondary" else "#2F8BAC"}" />' if icon else ''
    styles = {
        "primary": 'bg="var:brand/navy"',
        "teal":    'bg="var:brand/teal"',
        "secondary":'bg="var:bg/base" stroke="var:border/strong" strokeWidth={1}',
        "ghost":   'bg="var:bg/subtle"',
        "danger":  'bg="var:state/error"',
    }
    txt = "var:text/on-dark" if kind in ("primary","teal","danger") else "var:text/default" if kind=="secondary" else "var:text/accent"
    return (f'<Frame name="Btn {label}" flex="row" gap={{8}} items="center" justify="center" px={{20}} py={{12}} rounded={{999}} {styles[kind]}>'
            f'{ic}<Text font="Inter" size={{15}} weight="semibold" color="{txt}">{label}</Text></Frame>')
btn_body = (header("15","COMPONENTS","Buttons","Pill buttons, 12px vertical padding. Navy is primary; teal drives the key booking action.")
    + '<Frame w="fill" flex="row" gap={16} items="start">'
      + card('<Text font="Inter" size={14} weight="semibold" color="var:text/strong">Variants</Text>'
             '<Frame flex="row" gap={12} wrap="wrap" items="center" pt={4}>'
             + btn("Book now","teal","calendar-check")+btn("Primary","primary")+btn("Secondary","secondary")+btn("Ghost","ghost")+btn("Cancel","danger","ban") +
             '</Frame>')
    + '</Frame>'
    + '<Frame w="fill" flex="row" gap={16} items="start">'
      + card('<Text font="Inter" size={14} weight="semibold" color="var:text/strong">Sizes</Text>'
             '<Frame flex="row" gap={12} items="center" pt={4}>'
             '<Frame flex="row" gap={6} items="center" px={14} py={8} rounded={999} bg="var:brand/navy"><Text font="Inter" size={13} weight="semibold" color="var:text/on-dark">Small</Text></Frame>'
             '<Frame flex="row" gap={8} items="center" px={20} py={12} rounded={999} bg="var:brand/navy"><Text font="Inter" size={15} weight="semibold" color="var:text/on-dark">Medium</Text></Frame>'
             '<Frame flex="row" gap={8} items="center" px={28} py={16} rounded={999} bg="var:brand/navy"><Text font="Inter" size={17} weight="semibold" color="var:text/on-dark">Large</Text></Frame>'
             '</Frame>')
      + card('<Text font="Inter" size={14} weight="semibold" color="var:text/strong">States</Text>'
             '<Frame flex="row" gap={12} items="center" pt={4}>'
             '<Frame flex="row" gap={8} items="center" px={20} py={12} rounded={999} bg="var:brand/navy"><Text font="Inter" size={15} weight="semibold" color="var:text/on-dark">Default</Text></Frame>'
             '<Frame flex="row" gap={8} items="center" px={20} py={12} rounded={999} bg="var:brand/navy-deep"><Text font="Inter" size={15} weight="semibold" color="var:text/on-dark">Hover</Text></Frame>'
             '<Frame flex="row" gap={8} items="center" px={20} py={12} rounded={999} bg="var:neutral/200"><Text font="Inter" size={15} weight="semibold" color="var:text/faint">Disabled</Text></Frame>'
             '</Frame>')
    + '</Frame>'
    + footer())
frames.append((15,"15-components-buttons.jsx",frame("Medra DS — 15 Components Buttons", btn_body)))

# ============================================================ 16 COMPONENTS FORMS
def field(label, value, icon, placeholder=False):
    valcol = "var:text/faint" if placeholder else "var:text/strong"
    return (f'<Frame w="fill" flex="col" gap={{8}}>'
            f'<Text font="Inter" size={{13}} weight="medium" color="var:text/default">{label}</Text>'
            f'<Frame w="fill" flex="row" gap={{10}} items="center" px={{16}} py={{14}} rounded={{12}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
            f'<Icon name="lucide:{icon}" size={{18}} color="#7E8F9D" />'
            f'<Text font="Inter" size={{15}} weight="regular" color="{valcol}" grow={{1}}>{value}</Text></Frame></Frame>')
forms_body = (header("16","COMPONENTS","Forms &amp; Inputs","Generous 14px padding, 12px radius, teal focus ring. Built for phones first.")
    + '<Frame w="fill" flex="row" gap={20} items="start">'
      '<Frame grow={1} flex="col" gap={16}>'
        + field("Full name","Amara Okeke","user")
        + field("Phone number","+234 801 234 5678","phone")
        + '<Frame w="fill" flex="col" gap={8}><Text font="Inter" size={13} weight="medium" color="var:text/accent">Search doctors (focused)</Text>'
          '<Frame w="fill" flex="row" gap={10} items="center" px={16} py={14} rounded={12} bg="var:bg/base" stroke="var:border/accent" strokeWidth={2}>'
          '<Icon name="lucide:search" size={18} color="#39B0CF" /><Text font="Inter" size={15} weight="regular" color="var:text/faint" grow={1}>Cardiologist near Abuja…</Text></Frame></Frame>'
      '</Frame>'
      '<Frame w={420} flex="col" gap={16}>'
        + '<Frame flex="col" gap={12} p={22} rounded={16} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
          '<Text font="Inter" size={14} weight="semibold" color="var:text/strong">Selection controls</Text>'
          '<Frame flex="row" gap={12} items="center"><Frame w={22} h={22} rounded={6} bg="var:brand/teal" flex="col" justify="center" items="center"><Icon name="lucide:check" size={14} color="#FFFFFF" /></Frame><Text font="Inter" size={14} weight="regular" color="var:text/default">In-person consultation</Text></Frame>'
          '<Frame flex="row" gap={12} items="center"><Rect w={22} h={22} rounded={6} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} /><Text font="Inter" size={14} weight="regular" color="var:text/default">Virtual consultation</Text></Frame>'
          '<Frame flex="row" gap={12} items="center" pt={4}><Frame w={44} h={26} rounded={999} bg="var:brand/teal" flex="row" justify="end" items="center" px={3}><Ellipse w={20} h={20} bg="#FFFFFF" /></Frame><Text font="Inter" size={14} weight="regular" color="var:text/default">SMS reminders on</Text></Frame>'
          '<Frame flex="row" gap={12} items="center"><Frame w={44} h={26} rounded={999} bg="var:neutral/300" flex="row" justify="start" items="center" px={3}><Ellipse w={20} h={20} bg="#FFFFFF" /></Frame><Text font="Inter" size={14} weight="regular" color="var:text/muted">Marketing emails off</Text></Frame>'
        '</Frame>'
      '</Frame>'
    '</Frame>'
    + footer())
frames.append((16,"16-components-forms.jsx",frame("Medra DS — 16 Components Forms", forms_body)))

# ============================================================ 17 COMPONENTS CARDS
cards_body = (header("17","COMPONENTS","Cards","Product-real cards — the doctor result, an appointment, and a KPI tile.")
    + '<Frame w="fill" flex="row" gap={16} items="start">'
      # doctor card
      '<Frame grow={1} flex="col" gap={14} p={22} rounded={18} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
        '<Frame flex="row" gap={14} items="center">'
          '<Image image="assets/img/avatar-1.png" w={56} h={56} rounded={999} />'
          '<Frame grow={1} flex="col" gap={2}>'
            '<Frame flex="row" gap={8} items="center"><Text font="Inter" size={17} weight="semibold" color="var:text/strong">Dr. Ngozi Okafor</Text><Icon name="lucide:badge-check" size={18} color="#39B0CF" /></Frame>'
            '<Text font="Inter" size={13} weight="regular" color="var:text/muted">Cardiologist · Garki, Abuja</Text>'
          '</Frame>'
        '</Frame>'
        '<Frame flex="row" gap={8} items="center"><Frame flex="row" gap={6} items="center" px={12} py={6} rounded={999} bg="var:state/success-bg"><Icon name="lucide:clock" size={13} color="#2FA36B" /><Text font="Inter" size={12} weight="medium" color="var:state/success">Today · 3 slots</Text></Frame><Text font="Inter" size={14} weight="semibold" color="var:text/default">₦15,000</Text></Frame>'
        '<Frame name="Btn Book Ngozi" flex="row" gap={8} items="center" justify="center" px={18} py={12} rounded={999} bg="var:brand/teal"><Text font="Inter" size={15} weight="semibold" color="var:text/on-dark">Book appointment</Text></Frame>'
      '</Frame>'
      # appointment card
      '<Frame grow={1} flex="col" gap={14} p={22} rounded={18} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
        '<Frame flex="row" justify="between" items="center"><Text font="Inter" size={14} weight="semibold" color="var:text/muted">UPCOMING</Text><Frame flex="row" gap={6} items="center" px={12} py={6} rounded={999} bg="var:state/info-bg"><Icon name="lucide:video" size={13} color="#2F8BAC" /><Text font="Inter" size={12} weight="medium" color="var:state/info">Virtual</Text></Frame></Frame>'
        '<Text font="Inter" size={22} weight="bold" color="var:text/strong">Tue, 12 Aug · 10:30</Text>'
        '<Frame flex="row" gap={10} items="center"><Image image="assets/img/avatar-2.png" w={36} h={36} rounded={999} /><Frame flex="col" gap={0}><Text font="Inter" size={14} weight="semibold" color="var:text/default">Dr. Femi Adeyemi</Text><Text font="Inter" size={12} weight="regular" color="var:text/muted">General Practitioner</Text></Frame></Frame>'
        '<Frame flex="row" gap={10}><Frame name="Btn Reschedule" grow={1} flex="row" justify="center" px={14} py={10} rounded={999} bg="var:bg/subtle" stroke="var:border/default" strokeWidth={1}><Text font="Inter" size={14} weight="semibold" color="var:text/default">Reschedule</Text></Frame><Frame grow={1} flex="row" justify="center" px={14} py={10} rounded={999} bg="var:brand/navy"><Text font="Inter" size={14} weight="semibold" color="var:text/on-dark">Join</Text></Frame></Frame>'
      '</Frame>'
      # KPI tile (gradient)
      '<Frame w={280} flex="col" gap={10} p={24} rounded={18} image="assets/img/gradient-diag.png" overflow="hidden">'
        '<Icon name="lucide:activity" size={24} color="#FFFFFF" />'
        '<Text font="Inter" size={44} weight="bold" color="var:text/on-dark">1,284</Text>'
        '<Text font="Inter" size={14} weight="regular" color="var:text/on-dark-muted">Consultations this month</Text>'
        '<Frame flex="row" gap={6} items="center"><Icon name="lucide:arrow-up-right" size={15} color="#FFFFFF" /><Text font="Inter" size={13} weight="medium" color="var:text/on-dark">+18% vs last month</Text></Frame>'
      '</Frame>'
    '</Frame>'
    + footer())
frames.append((17,"17-components-cards.jsx",frame("Medra DS — 17 Components Cards", cards_body)))

# ============================================================ 18 COMPONENTS BADGES & ALERTS
def badge(text, icon, bg, fg):
    return (f'<Frame flex="row" gap={{6}} items="center" px={{12}} py={{6}} rounded={{999}} bg="{bg}">'
            f'<Icon name="lucide:{icon}" size={{13}} color="{fg}" /><Text font="Inter" size={{12}} weight="semibold" color="{fg.replace("#2FA36B","var:state/success").replace("#E0A32E","var:state/warning").replace("#D14343","var:state/error").replace("#2F8BAC","var:state/info").replace("#39B0CF","var:brand/teal")}">{text}</Text></Frame>')
def alert(icon, title, body, bg, fg):
    return (f'<Frame w="fill" flex="row" gap={{14}} items="start" p={{18}} rounded={{14}} bg="{bg}">'
            f'<Icon name="lucide:{icon}" size={{20}} color="{fg}" />'
            f'<Frame grow={{1}} flex="col" gap={{2}}><Text font="Inter" size={{15}} weight="semibold" color="var:text/strong">{title}</Text>'
            f'<Text font="Inter" size={{14}} weight="regular" color="var:text/muted" w="fill">{body}</Text></Frame></Frame>')
badge_body = (header("18","COMPONENTS","Badges, Status &amp; Alerts","Status is colour-coded consistently: green confirmed, amber pending, red cancelled, teal virtual.")
    + '<Frame w="fill" flex="row" gap={16} items="start">'
      + card('<Text font="Inter" size={14} weight="semibold" color="var:text/strong">Status badges</Text>'
             '<Frame flex="row" gap={10} wrap="wrap" pt={4}>'
             + badge("Verified","badge-check","var:state/success-bg","#2FA36B")
             + badge("Confirmed","circle-check","var:state/success-bg","#2FA36B")
             + badge("Pending","clock","var:state/warning-bg","#E0A32E")
             + badge("Cancelled","ban","var:state/error-bg","#D14343")
             + badge("No-show","triangle-alert","var:state/error-bg","#D14343")
             + badge("Virtual","video","var:state/info-bg","#2F8BAC")
             + badge("Trial","sparkles","var:bg/muted","#39B0CF")
             + '</Frame>')
    + '</Frame>'
    + '<Frame w="fill" flex="col" gap={12}>'
      + alert("circle-check","Booking confirmed","Your appointment with Dr. Okafor is set for Tue, 12 Aug at 10:30. An SMS confirmation is on its way.","var:state/success-bg","#2FA36B")
      + alert("circle-alert","Trial ending in 4 days","Add a payment method to keep your clinic dashboard active after the free trial.","var:state/warning-bg","#E0A32E")
      + alert("triangle-alert","Appointment cancelled","This slot was cancelled. The time has been released and the patient notified by SMS.","var:state/error-bg","#D14343")
    + '</Frame>'
    + footer())
frames.append((18,"18-components-badges.jsx",frame("Medra DS — 18 Components Badges", badge_body)))

# ============================================================ 19 IMAGERY
imagery_body = (header("19","EXPRESSION","Imagery","Warm, real, human. Duotone navy-teal treatment for hero imagery; honest clinical moments.")
    + '<Frame w="fill" flex="row" gap={16}>'
      '<Frame grow={1} h={260} rounded={18} image="assets/img/photo-1.png" overflow="hidden" />'
      '<Frame grow={1} h={260} rounded={18} image="assets/img/photo-2.png" overflow="hidden" />'
      '<Frame grow={1} h={260} rounded={18} image="assets/img/photo-3.png" overflow="hidden" />'
    '</Frame>'
    + '<Frame w="fill" flex="row" gap={16}>'
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Do</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">Natural light, real caregivers, calm expressions. Subtle navy→teal duotone for heroes.</Text>')
      + card('<Text font="Inter" size={15} weight="semibold" color="var:text/strong">Don’t</Text><Text font="Inter" size={14} weight="regular" color="var:text/muted" w="fill">No stocky handshakes, no fear imagery, no heavy filters that hide skin tone.</Text>')
    + '</Frame>'
    + footer())
frames.append((19,"19-imagery.jsx",frame("Medra DS — 19 Imagery", imagery_body)))

# ============================================================ 20 CONTACT
contact = (f'<Frame name="Medra DS — 20 Contact" w={{1440}} minH={{1024}} flex="row" bg="var:bg/band">'
    '<Frame w={64} h="fill" bg="var:bg/band-2" flex="col" justify="between" items="center" pt={40} pb={40}>'
      '<Image image="assets/logo/appicon.png" w={36} h={36} rounded={8} />'
      '<Rect w={4} h={80} bg="var:brand/teal" rounded={999} />'
    '</Frame>'
    '<Frame grow={1} h="fill" flex="col" justify="between" pl={72} pr={72} pt={72} pb={64}>'
      '<Frame flex="col" gap={12}>'
        '<Text font="Inter" size={13} weight="semibold" color="var:brand/teal">MEDRA · DESIGN SYSTEM</Text>'
        '<Rect w={56} h={3} bg="var:brand/teal" rounded={999} />'
      '</Frame>'
      '<Frame flex="col" gap={20}>'
        '<Image image="assets/logo/hero-white-glow.png" w={470} h={361} />'
        '<Text font="Inter" size={40} weight="bold" color="var:text/on-dark" w={720}>Every touchpoint is a brand touchpoint.</Text>'
      '</Frame>'
      '<Frame flex="row" gap={40} items="center">'
        '<Frame flex="row" gap={10} items="center"><Icon name="lucide:phone" size={18} color="#39B0CF" /><Text font="Inter" size={15} weight="regular" color="var:text/on-dark-muted">+234 800 000 0000</Text></Frame>'
        '<Frame flex="row" gap={10} items="center"><Icon name="lucide:mail" size={18} color="#39B0CF" /><Text font="Inter" size={15} weight="regular" color="var:text/on-dark-muted">hello@medra.health</Text></Frame>'
        '<Frame flex="row" gap={10} items="center"><Icon name="lucide:map-pin" size={18} color="#39B0CF" /><Text font="Inter" size={15} weight="regular" color="var:text/on-dark-muted">Abuja, Nigeria</Text></Frame>'
        '<Frame name="Btn Contents" flex="row" gap={8} items="center" px={18} py={10} rounded={999} bg="var:brand/teal"><Icon name="lucide:layout-dashboard" size={16} color="#FFFFFF" /><Text font="Inter" size={14} weight="semibold" color="var:text/on-dark">Contents</Text></Frame>'
      '</Frame>'
    '</Frame>'
  '</Frame>')
frames.append((20,"20-contact.jsx",contact))

# ---------- write ----------
def sanitize(s):
    # escape bare & (keep existing entities) so text is valid in strict parsers too
    return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)', '&amp;', s)
for order, fname, jsx in frames:
    open(os.path.join(OUT, fname), "w").write(sanitize(jsx))
print(f"wrote {len(frames)} frames to {OUT}")
for _,f,_ in frames: print("  ", f)
