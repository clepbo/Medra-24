#!/usr/bin/env python3
"""One desktop shell for every persona.

Three visual systems was my call and it was the wrong one: a reviewer had to relearn the
furniture three times, and a shared component had to be drawn three ways. This replaces them
with a single shell — the organisation module's icon rail, the doctor module's floating card,
one accent — and moves the identity into a **persona pill** in the top bar, which is the thing
that actually needs to be legible from three metres.

    ground (flat, calm)  →  inset 20  →  white card, radius 28
    ├── 76px icon rail — logo, destinations, help, avatar
    └── main column — top bar (title · persona pill · search · alerts · you)
                      content
        └── optional 340px right rail — what this section needs next

Nothing here uses coral or amber any more. Navy carries structure, teal is the only accent, and
green / amber / red are reserved for state, so a colour on screen always means something.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medra_ui import *

RAIL_W = 76
GROUND = "var:bg/subtle"

# The pill is the only place a persona is named. Everything else is identical across modules,
# which is the point — one design, and you always know whose screen you are looking at.
PERSONAS = {
    "member": ("circle-user", "Member"),
    "doctor": ("stethoscope", "Doctor"),
    "admin":  ("building-2", "Organisation · Admin"),
    "desk":   ("concierge-bell", "Organisation · Front desk"),
    "nurse":  ("heart-pulse", "Organisation · Nursing"),
    "lab":    ("flask-conical", "Organisation · Laboratory"),
    "pharm":  ("pill", "Organisation · Pharmacy"),
    "imaging":("scan", "Organisation · Imaging"),
    "billing":("receipt", "Organisation · Billing"),
    "orgdoc": ("stethoscope", "Organisation · Doctor"),
}


def persona_pill(key, size=12):
    ic, label = PERSONAS[key]
    return (f'<Frame name="Btn Persona" flex="row" gap={{7}} items="center" px={{12}} py={{7}} '
            f'rounded={{999}} bg="var:state/info-bg">'
            f'{I(ic, size + 2, "#2F8BAC")}'
            f'{T(size,"semibold","var:text/accent",label)}</Frame>')


def rail_item(ic, name, on=False, badge=None):
    """Icon only. A label under every icon is 8 more words of chrome on a screen that already
    has enough — the active state and the tooltip carry it."""
    box = ('bg="var:state/info-bg"' if on else '')
    dot = (f'<Frame w={{7}} h={{7}} rounded={{999}} bg="var:state/error" />') if badge else ''
    return (f'<Frame name="Btn {name}" w={{44}} h={{44}} rounded={{14}} {box} '
            f'flex="row" justify="center" items="center">'
            f'{I(ic, 20, "#2F8BAC" if on else "#7E8F9D")}{dot}</Frame>')


def rail(items, active=0, badges=()):
    """items: (icon, hotspot-name) in order. Bottom two are pinned: help, then you."""
    cells = "".join(rail_item(ic, nm, i == active, nm in badges)
                    for i, (ic, nm) in enumerate(items))
    return (f'<Frame w={{{RAIL_W}}} h="fill" flex="col" gap={{22}} items="center" px={{16}} py={{22}} '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Image image="assets/logo/appicon.png" w={{40}} h={{40}} rounded={{13}} />'
            f'<Frame w="fill" flex="col" gap={{6}} items="center">{cells}</Frame>'
            f'<Frame grow={{1}} w="fill" />'
            f'{rail_item("circle-help","Open help")}'
            f'<Image image="assets/img/me.jpg" w={{38}} h={{38}} rounded={{999}} />'
            f'<Frame name="Btn Sign out" flex="row">{I("log-out",18,"#A7B6C2")}</Frame></Frame>')


def topbar(title, persona, sub=None, right=None, search=True):
    subline = T(12, "regular", "var:text/muted", sub) if sub else ""
    tools = right if right is not None else (
        (f'<Frame name="Btn Search" w={{300}} flex="row" gap={{10}} items="center" px={{15}} py={{11}} '
         f'rounded={{999}} bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={{1}}>'
         f'{I("search",17,"#7E8F9D")}{T(13,"regular","var:text/faint","Search",w="fill")}</Frame>'
         if search else '')
        + f'<Frame name="Btn Notifications" w={{40}} h={{40}} rounded={{999}} bg="var:neutral/50" '
          f'stroke="var:border/subtle" strokeWidth={{1}} flex="row" justify="center" items="center">'
          f'{I("bell",18,"#1B3A5B")}</Frame>')
    return (f'<Frame w="fill" flex="row" justify="between" items="center" gap={{18}} pb={{4}}>'
            f'<Frame flex="col" gap={{3}}>'
            f'<Frame flex="row" gap={{11}} items="center">'
            f'{T(20,"bold","var:text/strong",title)}{persona_pill(persona)}</Frame>'
            f'{subline}</Frame>'
            f'<Frame flex="row" gap={{10}} items="center">{tools}</Frame></Frame>')


def app_desk(name, persona, title, children, items, active=0, sub=None,
             side=None, badges=(), right=None):
    """One shell, every persona. `side` is the optional 340px context rail."""
    rail_block = (f'<Frame w={{340}} h="fill" flex="col" gap={{14}} px={{20}} py={{22}} '
                  f'bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={{1}}>'
                  f'{side}</Frame>') if side else ''
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="col" p={{20}} bg="{GROUND}" '
            f'overflow="hidden">'
            f'<Frame w="fill" grow={{1}} flex="row" rounded={{28}} bg="var:bg/base" overflow="hidden" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{rail(items, active, badges)}'
            f'<Frame grow={{1}} h="fill" flex="col" gap={{20}} px={{30}} py={{24}}>'
            f'{topbar(title, persona, sub, right)}{children}</Frame>'
            f'{rail_block}</Frame></Frame>')


# ---------------------------------------------------------------- the pieces inside it
def stat(ic, value, label, sub=None, filled=False, name=None):
    """The tile row. One filled tile per screen, never more — it is the thing you are meant to
    look at first, and two of them is none."""
    if filled:
        return (f'<Frame name="Btn {name or label}" grow={{1}} flex="col" gap={{13}} p={{20}} rounded={{20}} '
                f'image="assets/img/btn-navy.jpg" overflow="hidden">'
                f'<Frame w={{40}} h={{40}} rounded={{13}} bg="var:bg/band-2" flex="row" justify="center" '
                f'items="center">{I(ic,19,"#FFFFFF")}</Frame>'
                f'<Frame flex="col" gap={{2}}>{T(26,"bold","var:text/on-dark",value)}'
                f'{T(13,"semibold","var:text/on-dark",label)}'
                f'{T(11,"regular","#A9C2D4",sub) if sub else ""}</Frame></Frame>')
    return (f'<Frame name="Btn {name or label}" grow={{1}} flex="col" gap={{13}} p={{20}} rounded={{20}} '
            f'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame w={{40}} h={{40}} rounded={{13}} bg="var:neutral/50" flex="row" justify="center" '
            f'items="center">{I(ic,19,"#2F8BAC")}</Frame>'
            f'<Frame flex="col" gap={{2}}>{T(26,"bold","var:text/strong",value)}'
            f'{T(13,"semibold","var:text/default",label)}'
            f'{T(11,"regular","var:text/muted",sub) if sub else ""}</Frame></Frame>')


def panel(title, body, action=None, name=None, p=20):
    head = (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(15,"bold","var:text/strong",title)}'
            + (f'<Frame name="Btn {name}" flex="row" gap={{5}} items="center">'
               f'{T(12,"semibold","var:text/accent",action)}{I("chevron-right",14,"#2F8BAC")}</Frame>'
               if action else '') + '</Frame>')
    return (f'<Frame w="fill" flex="col" gap={{13}} p={{{p}}} rounded={{20}} bg="var:bg/base" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{head}{body}</Frame>')


def row(ic, label, sub=None, value=None, name=None, tone=None, chevron=True):
    tint = {"ok": "var:state/success-bg", "warn": "var:state/warning-bg",
            "err": "var:state/error-bg", None: "var:neutral/50"}[tone]
    col = {"ok": "#2FA36B", "warn": "#E0A32E", "err": "#D14343", None: "#2F8BAC"}[tone]
    s = T(11, "regular", "var:text/muted", sub, w="fill") if sub else ""
    v = T(13, "semibold", "var:text/strong", value) if value else ""
    ch = I("chevron-right", 15, "#A7B6C2") if chevron else ""
    return (f'<Frame name="Btn {name or label}" w="fill" flex="row" gap={{12}} items="center" py={{11}}>'
            f'<Frame w={{34}} h={{34}} rounded={{11}} bg="{tint}" flex="row" justify="center" '
            f'items="center">{I(ic,16,col)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(13,"semibold","var:text/strong",label)}{s}</Frame>'
            f'{v}{ch}</Frame>')
