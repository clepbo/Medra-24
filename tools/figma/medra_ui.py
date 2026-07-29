#!/usr/bin/env python3
"""Medra shared UI kit — the "Soft Clinical" component vocabulary used by every module.
Extracted from the auth build so all modules stay visually identical."""
import os, re, json

W_IC="#FFFFFF"; N_IC="#1B3A5B"; T_IC="#39B0CF"; M_IC="#7E8F9D"; A_IC="#2F8BAC"
OK_IC="#2FA36B"; WARN_IC="#E0A32E"; ERR_IC="#D14343"

def T(size,weight,color,txt,w=None,align=None):
    a=f' align="{align}"' if align else ''
    ww=f' w={{{w}}}' if isinstance(w,int) else (' w="fill"' if w=="fill" else '')
    return f'<Text font="Inter" size={{{size}}} weight="{weight}" color="{color}"{ww}{a}>{txt}</Text>'
def I(n,s=18,c=M_IC): return f'<Icon name="lucide:{n}" size={{{s}}} color="{c}" />'
def SP(h): return f'<Frame h={{{h}}} />'

def eyebrow(t,c="var:text/accent"): return T(12,"semibold",c,t.upper())
def pulse(w=120,white=False): return f'<Image image="assets/img/pulse-{"white" if white else "teal"}.png" w={{{w}}} h={{{int(w*120/760)}}} />'

def head_chip(parts,size=30,color="var:text/strong"):
    out=""
    for txt,chip in parts:
        out += (f'<Frame px={{12}} py={{2}} rounded={{12}} bg="var:brand/teal"><Text font="Inter" size={{{size}}} weight="bold" color="var:text/on-dark">{txt}</Text></Frame>'
                if chip else T(size,"bold",color,txt))
    return f'<Frame w="fill" flex="row" gap={{9}} items="center" wrap="wrap">{out}</Frame>'

def circle_btn(icon,name,dark=False):
    bg='bg="var:bg/band-2"' if dark else 'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}'
    return (f'<Frame name="Btn {name}" w={{44}} h={{44}} rounded={{999}} {bg} flex="col" justify="center" items="center">'
            f'{I(icon,19,W_IC if dark else N_IC)}</Frame>')

def stepper(i,n):
    d=""
    for k in range(n):
        if k<i: d+='<Rect w={20} h={6} rounded={999} bg="var:brand/teal" />'
        elif k==i: d+='<Rect w={30} h={6} rounded={999} bg="var:brand/navy" />'
        else: d+='<Rect w={12} h={6} rounded={999} bg="var:neutral/200" />'
    return f'<Frame flex="row" gap={{5}} items="center">{d}</Frame>'

def card(children,p=22,gap=16,r=28,bg="var:bg/base"):
    """Generic floating white surface — the base of the Soft Clinical language."""
    return (f'<Frame w="fill" flex="col" gap={{{gap}}} p={{{p}}} rounded={{{r}}} bg="{bg}" '
            f'stroke="var:border/subtle" strokeWidth={{1}}>{children}</Frame>')

def field(label,ic,value,ph=True,helper=None,error=None,focus=False,prefix=None,trailing=None):
    bd="var:state/error" if error else ("var:border/accent" if focus else "var:border/subtle")
    bw=2 if (focus or error) else 1
    col="var:text/faint" if ph else "var:text/strong"
    pre=(f'{T(15,"semibold","var:text/default",prefix)}<Rect w={{1}} h={{20}} bg="var:border/default" />') if prefix else ''
    tr=f'<Frame name="Btn {trailing[1]}" flex="row">{I(trailing[0],18,M_IC)}</Frame>' if trailing else ''
    sub=''
    if error: sub=f'<Frame flex="row" gap={{6}} items="center">{I("circle-alert",14,ERR_IC)}{T(12,"medium","var:state/error",error)}</Frame>'
    elif helper: sub=T(12,"regular","var:text/muted",helper)
    return (f'<Frame w="fill" flex="col" gap={{7}}>{T(13,"medium","var:text/default",label)}'
            f'<Frame w="fill" flex="row" gap={{10}} items="center" px={{16}} py={{15}} rounded={{16}} bg="var:neutral/50" stroke="{bd}" strokeWidth={{{bw}}}>'
            f'{I(ic,18,T_IC if focus else M_IC)}{pre}{T(15,"regular",col,value,w="fill")}{tr}</Frame>{sub}</Frame>')

def otp(filled="",n=6,err=False):
    b=""
    for i in range(n):
        f=i<len(filled); act=i==len(filled)
        c="var:state/error" if err else ("var:border/accent" if act else ("var:brand/navy" if f else "var:border/subtle"))
        bw=2 if (act or err or f) else 1
        b+=(f'<Frame grow={{1}} h={{64}} flex="col" justify="center" items="center" rounded={{18}} bg="var:bg/base" stroke="{c}" strokeWidth={{{bw}}}>'
            f'{T(26,"bold","var:text/strong",filled[i]) if f else ""}</Frame>')
    return f'<Frame w="fill" flex="row" gap={{9}}>{b}</Frame>'

def cta(label,name,icon="arrow-right",img="btn-teal.jpg"):
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{10}} justify="center" items="center" px={{24}} py={{17}} '
            f'rounded={{999}} image="assets/img/{img}" overflow="hidden">{T(16,"semibold","var:text/on-dark",label)}'
            f'{I(icon,18,W_IC) if icon else ""}</Frame>')

def ghost(label,name,icon=None):
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{9}} justify="center" items="center" px={{22}} py={{16}} '
            f'rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
            f'{I(icon,18,N_IC) if icon else ""}{T(15,"semibold","var:text/default",label)}</Frame>')

def link(pre,lk,name,center=True):
    j=' justify="center"' if center else ''
    return (f'<Frame w="fill" flex="row" gap={{6}}{j} items="center">{T(14,"regular","var:text/muted",pre) if pre else ""}'
            f'<Frame name="Btn {name}" flex="row">{T(14,"semibold","var:text/accent",lk)}</Frame></Frame>')

def note(ic,txt,tone="info"):
    bg={"info":"var:state/info-bg","ok":"var:state/success-bg","warn":"var:state/warning-bg"}[tone]
    c={"info":A_IC,"ok":OK_IC,"warn":WARN_IC}[tone]
    return (f'<Frame w="fill" flex="row" gap={{10}} items="start" p={{14}} rounded={{16}} bg="{bg}">{I(ic,17,c)}'
            f'{T(13,"regular","var:text/default",txt,w="fill")}</Frame>')

def checkbox(label,name,checked=True):
    b=(f'<Frame w={{22}} h={{22}} rounded={{7}} bg="var:brand/teal" flex="col" justify="center" items="center">{I("check",14,W_IC)}</Frame>'
       if checked else '<Rect w={22} h={22} rounded={7} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />')
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{11}} items="start">{b}'
            f'{T(13,"regular","var:text/muted",label,w="fill")}</Frame>')

def chips(options,sel=0,name="chip"):
    out=""
    for i,o in enumerate(options):
        s=i==sel
        st='image="assets/img/btn-navy.jpg" overflow="hidden"' if s else 'bg="var:bg/base" stroke="var:border/default" strokeWidth={1}'
        out+=(f'<Frame name="Btn {name} {o}" flex="row" px={{16}} py={{11}} rounded={{999}} {st}>'
              f'{T(14,"medium","var:text/on-dark" if s else "var:text/default",o)}</Frame>')
    return f'<Frame w="fill" flex="row" gap={{9}} wrap="wrap">{out}</Frame>'

def field_chips(label,options,sel=0,name="chip"):
    return f'<Frame w="fill" flex="col" gap={{9}}>{T(13,"medium","var:text/default",label)}{chips(options,sel,name)}</Frame>'

def choice(ic,title,desc,name,sel=False):
    bd="var:border/accent" if sel else "var:border/subtle"; bw=2 if sel else 1
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{15}} items="center" p={{18}} rounded={{22}} bg="var:bg/base" stroke="{bd}" strokeWidth={{{bw}}}>'
            f'<Frame w={{50}} h={{50}} rounded={{16}} bg="var:bg/muted" flex="col" justify="center" items="center">{I(ic,23,A_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{2}}>{T(16,"semibold","var:text/strong",title)}{T(13,"regular","var:text/muted",desc,w="fill")}</Frame>'
            f'{I("chevron-right",20,T_IC)}</Frame>')

def proof(ic,label,dark=True):
    bg='bg="var:bg/band-2"' if dark else 'bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}'
    return (f'<Frame flex="row" gap={{8}} items="center" px={{14}} py={{9}} rounded={{999}} {bg}>{I(ic,15,T_IC)}'
            f'{T(12,"medium","var:text/on-dark" if dark else "var:text/default",label)}</Frame>')

def stat_row(items):
    cells="".join(f'<Frame grow={{1}} flex="col" gap={{1}} items="center">{T(20,"bold","var:text/on-dark",v)}'
                  f'{T(11,"regular","var:text/on-dark-muted",l)}</Frame>' for v,l in items)
    return f'<Frame w="fill" flex="row" gap={{6}} items="center" px={{16}} py={{14}} rounded={{20}} bg="var:bg/band-2">{cells}</Frame>'

def plan(title,price,sub,sel=False):
    bd="var:border/accent" if sel else "var:border/subtle"; bw=2 if sel else 1
    tick=(f'<Frame w={{22}} h={{22}} rounded={{999}} bg="var:brand/teal" flex="col" justify="center" items="center">{I("check",13,W_IC)}</Frame>'
          if sel else '<Rect w={22} h={22} rounded={999} bg="var:bg/base" stroke="var:border/strong" strokeWidth={1} />')
    return (f'<Frame name="Btn Plan {title}" w="fill" flex="row" gap={{14}} items="center" p={{18}} rounded={{22}} bg="var:bg/base" stroke="{bd}" strokeWidth={{{bw}}}>'
            f'<Frame grow={{1}} flex="col" gap={{3}}>{T(15,"semibold","var:text/strong",title)}'
            f'<Frame flex="row" gap={{4}} items="center">{T(22,"bold","var:text/strong",price)}{T(12,"regular","var:text/muted","/month")}</Frame>'
            f'{T(12,"regular","var:text/muted",sub,w="fill")}</Frame>{tick}</Frame>')

def upload(name,done=False,label="Practice licence"):
    if done:
        return (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{15}} rounded={{18}} bg="var:state/success-bg">{I("file-check",22,OK_IC)}'
                f'<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"semibold","var:text/strong","practice-licence.pdf")}'
                f'{T(12,"regular","var:text/muted","1.2 MB · uploaded")}</Frame>'
                f'<Frame name="Btn Remove doc" flex="row">{I("x",18,M_IC)}</Frame></Frame>')
    return (f'<Frame name="Btn {name}" w="fill" flex="col" gap={{7}} items="center" py={{26}} px={{18}} rounded={{18}} bg="var:state/info-bg" stroke="var:border/accent" strokeWidth={{1}}>'
            f'{I("upload",25,A_IC)}{T(14,"semibold","var:text/default",label)}'
            f'{T(12,"regular","var:text/muted","PDF, JPG or PNG · up to 10 MB")}'
            f'<Frame flex="row" gap={{8}} pt={{3}}>'
            f'<Frame flex="row" gap={{6}} items="center" px={{12}} py={{7}} rounded={{999}} bg="var:bg/base">{I("camera",14,N_IC)}{T(12,"medium","var:text/default","Camera")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{12}} py={{7}} rounded={{999}} bg="var:bg/base">{I("file-text",14,N_IC)}{T(12,"medium","var:text/default","Files")}</Frame>'
            f'</Frame></Frame>')

def big_icon(ic,tone="ok",size=96):
    bg={"ok":"var:state/success-bg","warn":"var:state/warning-bg","info":"var:state/info-bg"}[tone]
    c={"ok":OK_IC,"warn":WARN_IC,"info":A_IC}[tone]
    return f'<Frame w={{{size}}} h={{{size}}} rounded={{999}} bg="{bg}" flex="col" justify="center" items="center">{I(ic,int(size*0.45),c)}</Frame>'


def segmented(options, sel=0, name="seg"):
    out=""
    for i,o in enumerate(options):
        s=i==sel
        st=('bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}' if s else 'bg="var:neutral/100"')
        out+=(f'<Frame name="Btn {name} {o}" grow={{1}} flex="row" justify="center" px={{16}} py={{11}} rounded={{999}} {st}>'
              f'{T(14,"semibold","var:text/strong" if s else "var:text/muted",o)}</Frame>')
    return f'<Frame w="fill" flex="row" gap={{4}} p={{4}} rounded={{999}} bg="var:neutral/100">{out}</Frame>'

def social_btn(brand,label,name):
    img={"google":"brand-google.png","apple":"brand-apple.png"}[brand]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{10}} justify="center" items="center" px={{22}} py={{15}} '
            f'rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
            f'<Image image="assets/img/{img}" w={{20}} h={{20}} />{T(15,"semibold","var:text/default",label)}</Frame>')

def divider_or(txt="or"):
    return (f'<Frame w="fill" flex="row" gap={{12}} items="center"><Rect grow={{1}} h={{1}} bg="var:border/subtle" />'
            f'{T(12,"medium","var:text/faint",txt)}<Rect grow={{1}} h={{1}} bg="var:border/subtle" /></Frame>')

def stepper_ctl(label, value, name, helper=None):
    sub=T(12,"regular","var:text/muted",helper) if helper else ""
    return (f'<Frame w="fill" flex="col" gap={{7}}>{T(13,"medium","var:text/default",label)}'
            f'<Frame w="fill" flex="row" gap={{12}} items="center" px={{12}} py={{9}} rounded={{16}} bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'<Frame name="Btn {name} minus" w={{36}} h={{36}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}} flex="col" justify="center" items="center">{I("minus",17,N_IC)}</Frame>'
            f'<Frame grow={{1}} flex="col" items="center">{T(20,"bold","var:text/strong",str(value))}</Frame>'
            f'<Frame name="Btn {name} plus" w={{36}} h={{36}} rounded={{999}} image="assets/img/btn-navy.jpg" overflow="hidden" flex="col" justify="center" items="center">{I("plus",17,W_IC)}</Frame>'
            f'</Frame>{sub}</Frame>')

def price_line(label, amount, strong=False):
    return (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(14,"semibold" if strong else "regular","var:text/strong" if strong else "var:text/muted",label)}'
            f'{T(16 if strong else 14,"bold" if strong else "medium","var:text/strong",amount)}</Frame>')

def biometric_btn(name):
    return (f'<Frame name="Btn {name}" w={{108}} h={{108}} rounded={{999}} image="assets/img/btn-teal.jpg" overflow="hidden" '
            f'flex="col" justify="center" items="center">{I("fingerprint",46,W_IC)}</Frame>')

# ---------- mobile chrome ----------
def statusbar(dark=False):
    c="var:text/on-dark" if dark else "var:text/strong"
    hexc="#FFFFFF" if dark else "#1B3A5B"
    bars="".join(f'<Rect w={{3}} h={{{h}}} rounded={{2}} bg="{hexc}" />' for h in (5,7,9,11))
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{24}} pt={{14}} pb={{2}}>'
            f'{T(13,"semibold",c,"9:41")}'
            f'<Frame flex="row" gap={{6}} items="center"><Frame flex="row" gap={{2}} items="end">{bars}</Frame>'
            f'{I("globe",13,hexc)}'
            f'<Frame w={{22}} h={{11}} rounded={{3}} stroke="{hexc}" strokeWidth={{1}} flex="col" justify="center" px={{2}}>'
            f'<Rect w={{13}} h={{6}} rounded={{1}} bg="{hexc}" /></Frame></Frame></Frame>')

def mob_form(name, eyebrow_t, head_parts, sub, body, primary, extras=(), step=None, back=True, help_btn=True):
    hdr=(f'<Frame w="fill" flex="row" justify="between" items="center" px={{22}} pt={{10}} pb={{6}}>'
         f'{circle_btn("arrow-left","Back") if back else "<Frame w={44} />"}'
         f'{stepper(*step) if step else "<Frame />"}'
         f'{circle_btn("circle-help","Help") if help_btn else "<Frame w={44} />"}</Frame>')
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/surface-mobile.jpg" overflow="hidden">'
            f'{statusbar()}{hdr}'
            f'<Frame grow={{1}} w="fill" flex="col" gap={{18}} px={{22}} pt={{10}} pb={{26}}>'
            f'<Frame w="fill" flex="col" gap={{9}}>{eyebrow(eyebrow_t)}{head_chip(head_parts,28)}'
            f'{T(15,"regular","var:text/muted",sub,w="fill")}</Frame>'
            f'{body}<Frame grow={{1}} />'
            f'<Frame w="fill" flex="col" gap={{11}}>{primary}{"".join(extras)}</Frame></Frame></Frame>')

def mob_hero(name, img, eyebrow_t, head_parts, sub, primary, extras=(), dots=None, skip=True, proofs=None, hero_h=566):
    skipbtn=(f'<Frame name="Btn Skip" flex="row" px={{14}} py={{8}} rounded={{999}} bg="var:bg/band-2">'
             f'{T(13,"semibold","var:text/on-dark","Skip")}</Frame>') if skip else '<Frame />'
    proofrow=f'<Frame w="fill" flex="row" gap={{8}} wrap="wrap">{"".join(proofs)}</Frame>' if proofs else ''
    hero=(f'<Frame w="fill" h={{{hero_h}}} image="assets/img/{img}" overflow="hidden" flex="col" justify="between" pb={{24}}>'
          f'{statusbar(dark=True)}'
          f'<Frame w="fill" flex="row" justify="between" items="center" px={{22}} pt={{6}}>'
          f'<Image image="assets/logo/logo-white.png" w={{74}} h={{55}} />{skipbtn}</Frame>'
          f'<Frame grow={{1}} />'
          f'<Frame w="fill" flex="col" gap={{10}} px={{24}}>{eyebrow(eyebrow_t,"var:brand/teal")}'
          f'{head_chip(head_parts,29,"var:text/on-dark")}{T(15,"regular","var:text/on-dark-muted",sub,w="fill")}{proofrow}</Frame></Frame>')
    sheet=(f'<Frame grow={{1}} w="fill" flex="col" gap={{16}} px={{24}} pt={{22}} pb={{28}}>'
           f'{dots or ""}<Frame grow={{1}} />{primary}{"".join(extras)}</Frame>')
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" image="assets/img/surface-mobile.jpg" overflow="hidden">'
            f'{hero}{sheet}</Frame>')

# ---------- desktop chrome ----------
def desk_topbar():
    return (f'<Frame w="fill" flex="row" justify="between" items="center" px={{56}} pt={{28}}>'
            f'<Image image="assets/logo/logo-gradient.png" w={{104}} h={{77}} />'
            f'<Frame flex="row" gap={{10}} items="center">'
            f'<Frame name="Btn Language" flex="row" gap={{8}} items="center" px={{15}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>{I("globe",16,N_IC)}{T(13,"medium","var:text/default","English")}{I("chevron-down",15,M_IC)}</Frame>'
            f'<Frame name="Btn Help" flex="row" gap={{8}} items="center" px={{15}} py={{10}} rounded={{999}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>{I("circle-help",16,N_IC)}{T(13,"medium","var:text/default","Need help?")}</Frame>'
            f'</Frame></Frame>')

def desk_panel(img, eyebrow_t, head_parts, sub, proofs=None, stats=None, h=664, w=560):
    pr=f'<Frame w="fill" flex="row" gap={{8}} wrap="wrap">{"".join(proofs)}</Frame>' if proofs else ''
    st=stat_row(stats) if stats else ''
    return (f'<Frame w={{{w}}} h={{{h}}} rounded={{32}} image="assets/img/{img}" overflow="hidden" flex="col" justify="end" gap={{14}} p={{30}}>'
            f'{eyebrow(eyebrow_t,"var:brand/teal")}{head_chip(head_parts,30,"var:text/on-dark")}'
            f'{T(15,"regular","var:text/on-dark-muted",sub,w="fill")}{pr}{st}</Frame>')

def desk(name, panel, form_children, form_w=500):
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="col" image="assets/img/surface-desktop.jpg" overflow="hidden">'
            f'{desk_topbar()}'
            f'<Frame grow={{1}} w="fill" flex="row" justify="center" items="center" gap={{48}} px={{56}} py={{28}}>'
            f'{panel}'
            f'<Frame w={{{form_w}}} flex="col" gap={{18}} p={{38}} rounded={{32}} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={{1}}>'
            f'{form_children}</Frame></Frame></Frame>')

def desk_form(name, panel, eyebrow_t, head_parts, sub, body, primary, extras=(), step=None, back=True):
    backbtn=(f'<Frame name="Btn Back" flex="row" gap={{7}} items="center">{I("arrow-left",18,N_IC)}'
             f'{T(14,"semibold","var:text/default","Back")}</Frame>') if back else '<Frame />'
    hdr=f'<Frame w="fill" flex="row" justify="between" items="center">{backbtn}{stepper(*step) if step else "<Frame />"}</Frame>'
    return desk(name, panel,
        f'{hdr}<Frame w="fill" flex="col" gap={{9}}>{eyebrow(eyebrow_t)}{head_chip(head_parts,32)}'
        f'{T(15,"regular","var:text/muted",sub,w="fill")}</Frame>{body}'
        f'<Frame w="fill" flex="col" gap={{11}}>{primary}{"".join(extras)}</Frame>')

