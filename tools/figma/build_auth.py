#!/usr/bin/env python3
"""Medra — Authentication screens. Distinctive "Soft Clinical" language:
real photography, soft mesh grounds, floating white cards, ECG-pulse motif,
highlight-chip headlines. Desktop 1440x900 + Mobile 390x844. One .jsx = one frame."""
import os, re, json
OUT = "/home/user/Medra-24/figma/medra-auth"
os.makedirs(OUT, exist_ok=True)

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

frames=[]; NAMES={}; ORDER={}
def add(page,fid,d,m):
    frames.append((page,f"{fid}-d.jsx",d)); frames.append((page,f"{fid}-m.jsx",m))
    NAMES[fid]=(re.search(r'name="([^"]+)"',d).group(1), re.search(r'name="([^"]+)"',m).group(1))
    ORDER.setdefault(page,[]).append(fid)

# ============================================================ ENTRY / ONBOARDING
ONB=[("E1-onb1","onb-1.jpg","m-hero-doctor.jpg","Find care you can trust",
      [("Every doctor",False),("verified",True)],
      "We check every doctor's MDCN licence ourselves — so the person you book is the professional they say they are.",
      [("shield-check","MDCN verified"),("badge-check","Licence checked")]),
     ("E2-onb2","onb-2.jpg","onb-2.jpg","Book before you leave home",
      [("See real",False),("availability",True)],
      "No more wasted trips. See a doctor's genuinely open slots and book in-person or by video, from your phone.",
      [("calendar-check","Real-time slots"),("video","In-person or video")]),
     ("E3-onb3","onb-3.jpg","onb-3.jpg","Your history follows you",
      [("One record,",False),("everywhere",True)],
      "Diagnoses, prescriptions and results stay with you — so any doctor you see can care for you safely.",
      [("clipboard-list","Portable records"),("lock","NDPR secure")])]
for i,(fid,dimg,mimg,eb,hp,sub,pf) in enumerate(ONB):
    prs=[proof(a,b) for a,b in pf]; dots=stepper(i,3)
    add("Entry",fid,
        desk(f"Auth · Entry — {fid[:2]} Onboarding {i+1}",
             desk_panel(dimg,"Welcome to Medra",hp,sub,proofs=prs),
             f'{eyebrow("Getting started")}{head_chip([(eb,False)],32)}'
             f'{T(16,"regular","var:text/muted",sub,w="fill")}{SP(2)}{dots}{SP(6)}'
             f'{cta("Next","Next "+fid)}{ghost("Skip introduction","Skip "+fid)}'),
        mob_hero(f"Auth · Entry — {fid[:2]} Onboarding {i+1} · Mobile",mimg,"Welcome to Medra",hp,sub,
                 cta("Next","Next "+fid),[link("","Skip introduction","Skip "+fid)],dots=dots,proofs=prs))

add("Entry","E4-welcome",
    desk("Auth · Entry — E4 Welcome",
         desk_panel("d-panel-patient.jpg","Medra",[("Healthcare that",False),("follows you",True)],
                    "Verified doctors, real availability, and a medical history that travels with you.",
                    stats=[("2,400+","Patients"),("180+","Doctors"),("4.9","Rating")]),
         f'{eyebrow("Welcome")}{head_chip([("Let’s get you",False),("started",True)],32)}'
         f'{T(16,"regular","var:text/muted","One account for booking, records and care — wherever you are in Nigeria.",w="fill")}'
         f'{SP(2)}{pulse(140)}{SP(2)}'
         f'{cta("Create an account","Create account")}{ghost("I already have an account","Login entry","log-in")}'
         f'{note("shield-check","Your health data is encrypted and protected under the NDPR.","info")}'),
    mob_hero("Auth · Entry — E4 Welcome · Mobile","m-hero-patient.jpg","Welcome to Medra",
             [("Healthcare that",False),("follows you",True)],
             "Verified doctors, real availability, and records that travel with you.",
             cta("Create an account","Create account"),
             [ghost("I already have an account","Login entry","log-in")],skip=False,
             proofs=[proof("shield-check","NDPR secure"),proof("badge-check","MDCN verified")]))

ROLE=(f'<Frame w="fill" flex="col" gap={{11}}>{choice("user","I am a patient","Book doctors and keep my records","Role Patient",sel=True)}'
      f'{choice("stethoscope","I am a doctor","See patients and write consultation notes","Role Doctor")}'
      f'{choice("building-2","I represent an institution","Register a clinic or hospital","Role Institution")}</Frame>')
add("Entry","E5-role",
    desk_form("Auth · Entry — E5 Role Selection",
        desk_panel("d-panel-institution.jpg","Built for everyone in care",[("Care is a",False),("team",True)],
                   "Patients, doctors and institutions — each gets an experience shaped around how they work.",
                   proofs=[proof("users","5 roles"),proof("lock","Role-based access")]),
        "Choose your role",[("How will you use",False),("Medra?",True)],
        "Pick the one that fits you — it sets up the right experience. You can add another role later from Settings.",
        ROLE,cta("Continue","Continue role"),[link("Not sure?","See how Medra works","Help role")]),
    mob_form("Auth · Entry — E5 Role Selection · Mobile","Choose your role",
        [("How will you use",False),("Medra?",True)],"Pick the one that fits you — you can add another later.",
        ROLE,cta("Continue","Continue role"),[link("Not sure?","See how Medra works","Help role")]))

# ============================================================ PATIENT
PP=lambda **kw: desk_panel("d-panel-patient.jpg",**kw)
add("Patient","P1-create",
    desk_form("Auth · Patient — P1 Create Account",
        PP(eyebrow_t="For patients",head_parts=[("Your health,",False),("in one place",True)],
           sub="No paper to carry. No history to lose. Just care that knows you.",
           proofs=[proof("shield-check","NDPR secure"),proof("badge-check","Verified doctors")]),
        "Step 1 of 5",[("Create your",False),("account",True)],
        "Enter your phone number — we'll text you a 6-digit code to confirm it. No password needed, ever.",
        f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone number","phone","801 234 5678",prefix="+234",helper="Standard SMS rates may apply.")}'
        f'{checkbox("I agree to Medra’s Terms of Service and Privacy Policy, and consent to my health data being processed under the NDPR.","Consent")}</Frame>',
        cta("Send my code","Send code P1"),[link("Already have an account?","Log in","Login P")],step=(0,5)),
    mob_form("Auth · Patient — P1 Create Account · Mobile","Step 1 of 5",
        [("Create your",False),("account",True)],"We'll text a 6-digit code to confirm your number. No password needed.",
        f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone number","phone","801 234 5678",prefix="+234")}'
        f'{checkbox("I agree to the Terms &amp; Privacy Policy and NDPR data processing.","Consent")}</Frame>',
        cta("Send my code","Send code P1"),[link("Already have an account?","Log in","Login P")],step=(0,5)))

OTP_P=f'<Frame w="fill" flex="col" gap={{14}}>{otp("3907")}{link("Didn’t get it?","Resend in 0:24","Resend P2")}</Frame>'
add("Patient","P2-otp",
    desk_form("Auth · Patient — P2 Verify Code",
        PP(eyebrow_t="For patients",head_parts=[("Almost",False),("there",True)],
           sub="Confirming your number keeps your records secure and yours alone.",
           proofs=[proof("lock","Encrypted"),proof("smartphone","One-time code")]),
        "Step 2 of 5",[("Enter the",False),("6-digit code",True)],"We sent it to +234 801 234 5678 by SMS.",
        OTP_P,cta("Verify and continue","Verify P2"),
        [link("Wrong number?","Change it","Change number P2"),link("Code not arriving?","Get help another way","Help code P2")],step=(1,5)),
    mob_form("Auth · Patient — P2 Verify Code · Mobile","Step 2 of 5",
        [("Enter the",False),("6-digit code",True)],"Sent to +234 801 234 5678.",
        OTP_P,cta("Verify and continue","Verify P2"),
        [link("Wrong number?","Change it","Change number P2"),link("","Get help another way","Help code P2")],step=(1,5)))

NAME_B=(f'<Frame w="fill" flex="col" gap={{18}}>'
        f'<Frame w="fill" flex="row" gap={{15}} items="center">'
        f'<Frame w={{74}} h={{74}} rounded={{999}} bg="var:bg/muted" flex="col" justify="center" items="center">{I("camera",25,A_IC)}</Frame>'
        f'<Frame name="Btn Add photo" flex="row" gap={{8}} items="center" px={{16}} py={{11}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
        f'{I("upload",16,N_IC)}{T(13,"semibold","var:text/default","Add a photo (optional)")}</Frame></Frame>'
        f'{field("Full name","user","Amara Okeke",ph=False)}'
        f'{field("Date of birth","calendar-days","12 March 1994",ph=False,helper="Helps your doctor prescribe safely.")}</Frame>')
add("Patient","P3-name",
    desk_form("Auth · Patient — P3 Your Name",
        PP(eyebrow_t="For patients",head_parts=[("Care that",False),("knows you",True)],
           sub="Your details stay private and are shared only with doctors you choose to book.",
           proofs=[proof("lock","Private by default")]),
        "Step 3 of 5",[("What should we",False),("call you?",True)],
        "This is the name your doctor will see on your records.",
        NAME_B,cta("Continue","Continue P3"),[link("","Skip for now","Skip P3")],step=(2,5)),
    mob_form("Auth · Patient — P3 Your Name · Mobile","Step 3 of 5",
        [("What should we",False),("call you?",True)],"This is the name your doctor will see.",
        NAME_B,cta("Continue","Continue P3"),[link("","Skip for now","Skip P3")],step=(2,5)))

ABOUT_B=(f'<Frame w="fill" flex="col" gap={{18}}>'
         f'{field_chips("Gender",["Female","Male","Non-binary","Prefer not to say"],0,"Gender")}'
         f'{field_chips("Preferred language",["English","Hausa","Yoruba","Igbo","Pidgin"],0,"Language")}'
         f'{field_chips("Text size",["Standard","Large","Extra large"],0,"Textsize")}</Frame>')
add("Patient","P4-about",
    desk_form("Auth · Patient — P4 About You",
        PP(eyebrow_t="For patients",head_parts=[("Made for",False),("everyone",True)],
           sub="Medra works in your language, at your pace, however you need to use it.",
           proofs=[proof("globe","5 languages"),proof("accessibility","Accessible")]),
        "Step 4 of 5",[("A few things",False),("about you",True)],
        "Tap to choose. You can change any of this later in Settings.",
        ABOUT_B,cta("Continue","Continue P4"),[link("","Skip for now","Skip P4")],step=(3,5)),
    mob_form("Auth · Patient — P4 About You · Mobile","Step 4 of 5",
        [("A few things",False),("about you",True)],"Tap to choose — change any of it later.",
        ABOUT_B,cta("Continue","Continue P4"),[link("","Skip for now","Skip P4")],step=(3,5)))

HEALTH_B=(f'<Frame w="fill" flex="col" gap={{16}}>'
          f'{field_chips("Blood group",["A+","A-","B+","B-","O+","O-","AB+","Not sure"],4,"Blood")}'
          f'{field("Allergies","triangle-alert","e.g. penicillin, peanuts")}'
          f'{field("Medicines you take now","pill","e.g. metformin 500mg")}'
          f'{field("Emergency contact","phone-call","802 000 0000",prefix="+234")}</Frame>')
add("Patient","P5-health",
    desk_form("Auth · Patient — P5 Health Basics",
        PP(eyebrow_t="For patients",head_parts=[("Safer",False),("prescriptions",True)],
           sub="Knowing your allergies and current medicines helps any doctor avoid a dangerous clash.",
           proofs=[proof("heart-pulse","Clinical safety"),proof("pill","Drug-clash aware")]),
        "Step 5 of 5",[("Your",False),("health basics",True)],
        "Optional, but it helps doctors keep you safe. You can add more anytime.",
        HEALTH_B,cta("Finish and go to my home","Finish P5"),[link("","I’ll do this later","Skip P5")],step=(4,5)),
    mob_form("Auth · Patient — P5 Health Basics · Mobile","Step 5 of 5",
        [("Your",False),("health basics",True)],"Optional — but it helps doctors keep you safe.",
        HEALTH_B,cta("Finish","Finish P5"),[link("","I’ll do this later","Skip P5")],step=(4,5)))

add("Patient","P6-login",
    desk_form("Auth · Patient — P6 Log In",
        PP(eyebrow_t="Welcome back",head_parts=[("Good to see you",False),("again",True)],
           sub="Your appointments and records are exactly where you left them.",
           proofs=[proof("calendar-check","2 upcoming visits")]),
        "Log in",[("Welcome",False),("back",True)],
        "Enter your phone number and we'll text you a code. No password to remember.",
        field("Phone number","phone","801 234 5678",prefix="+234",focus=True),
        cta("Send my code","Send code P6"),
        [link("New to Medra?","Create an account","Create P6"),link("Can't access your number?","Get help","Help P6")]),
    mob_form("Auth · Patient — P6 Log In · Mobile","Log in",[("Welcome",False),("back",True)],
        "We'll text you a code — no password to remember.",
        field("Phone number","phone","801 234 5678",prefix="+234",focus=True),
        cta("Send my code","Send code P6"),
        [link("New to Medra?","Create an account","Create P6"),link("","Can't access your number?","Help P6")]))

HELPC=(f'<Frame w="fill" flex="col" gap={{11}}>'
       f'{choice("refresh-cw","Resend the code","Text the 6-digit code again","Resend help")}'
       f'{choice("phone-call","Call me instead","Get the code by automated call","Call help")}'
       f'{choice("pencil","Change my number","I entered the wrong number","Change help")}'
       f'{choice("message-square-text","Message support","Chat with the Medra team","Support help")}</Frame>')
add("Patient","P7-help",
    desk_form("Auth · Patient — P7 Cannot Get Code",
        PP(eyebrow_t="We've got you",head_parts=[("No one gets",False),("stuck",True)],
           sub="There is always another way in. If none of these work, our team will help you personally.",
           proofs=[proof("helping-hand","Human support")]),
        "Trouble signing in",[("Didn't get your",False),("code?",True)],
        "Pick an option below — we'll get you in.",HELPC,
        ghost("Back to verification","Back to OTP","arrow-left"),[]),
    mob_form("Auth · Patient — P7 Cannot Get Code · Mobile","Trouble signing in",
        [("Didn't get your",False),("code?",True)],"Pick an option — we'll get you in.",HELPC,
        ghost("Back to verification","Back to OTP","arrow-left")))

SUC_P=(f'<Frame w="fill" flex="col" gap={{16}} items="center">{big_icon("circle-check","ok")}'
       f'{T(15,"regular","var:text/muted","Your account is ready. Next: find a verified doctor near you and book your first visit.",w="fill",align="center")}'
       f'{note("info","Taking you to your patient home…","info")}</Frame>')
add("Patient","P8-success",
    desk("Auth · Patient — P8 Success",
        desk_panel("success.jpg","You're in",[("Welcome to",False),("Medra",True)],
                   "Care that follows you — everywhere in Nigeria.",
                   stats=[("180+","Verified doctors"),("24/7","Booking"),("4.9","Patient rating")]),
        f'{eyebrow("All set")}{head_chip([("You’re all set,",False),("Amara",True)],32)}{SUC_P}'
        f'{cta("Go to my home","Go home P8","house")}{ghost("Explore doctors near me","Explore P8","search")}'),
    mob_hero("Auth · Patient — P8 Success · Mobile","success.jpg","All set",
        [("You're all set,",False),("Amara",True)],"Your account is ready — let's find you care.",
        cta("Go to my home","Go home P8","house"),[ghost("Explore doctors near me","Explore P8","search")],skip=False,
        proofs=[proof("circle-check","Account verified")]))

# ============================================================ DOCTOR
DP=lambda **kw: desk_panel("d-panel-doctor.jpg",**kw)
D1B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone number","phone","803 555 0110",prefix="+234")}'
     f'{field("MDCN number","id-card","MDCN/45201",helper="Your Medical &amp; Dental Council of Nigeria licence number.")}'
     f'{field_chips("Specialisation",["Cardiology","General practice","Paediatrics","Other"],1,"Specialty")}</Frame>')
add("Doctor","D1-create",
    desk_form("Auth · Doctor — D1 Create Account",
        DP(eyebrow_t="For doctors",head_parts=[("Your practice,",False),("amplified",True)],
           sub="Reach the patients who need you, with a schedule that respects your time.",
           proofs=[proof("badge-check","MDCN verified"),proof("calendar-days","You set your hours")],
           stats=[("180+","Doctors"),("2,400+","Patients"),("48h","To verify")]),
        "Step 1 of 4",[("Join Medra as a",False),("doctor",True)],
        "We verify every doctor's MDCN licence before your profile goes live — that's why patients trust Medra.",
        D1B,cta("Continue","Continue D1","arrow-right","btn-navy.jpg"),
        [link("Already registered?","Log in","Login D")],step=(0,4)),
    mob_form("Auth · Doctor — D1 Create Account · Mobile","Step 1 of 4",
        [("Join as a",False),("doctor",True)],"We verify your MDCN licence before your profile goes live.",
        D1B,cta("Continue","Continue D1","arrow-right","btn-navy.jpg"),
        [link("Already registered?","Log in","Login D")],step=(0,4)))

OTP_D=f'<Frame w="fill" flex="col" gap={{14}}>{otp("58")}{link("Didn’t get it?","Resend in 0:20","Resend D2")}</Frame>'
add("Doctor","D2-otp",
    desk_form("Auth · Doctor — D2 Verify Code",
        DP(eyebrow_t="For doctors",head_parts=[("Security",False),("first",True)],
           sub="Two steps keep your patients' records protected — every single time.",
           proofs=[proof("lock","Encrypted"),proof("shield-check","NDPR aligned")]),
        "Step 2 of 4",[("Verify your",False),("phone",True)],
        "Enter the 6-digit code we sent to +234 803 555 0110.",
        OTP_D,cta("Verify","Verify D2","arrow-right","btn-navy.jpg"),
        [link("Wrong number?","Change it","Change number D2")],step=(1,4)),
    mob_form("Auth · Doctor — D2 Verify Code · Mobile","Step 2 of 4",[("Verify your",False),("phone",True)],
        "Code sent to +234 803 555 0110.",OTP_D,
        cta("Verify","Verify D2","arrow-right","btn-navy.jpg"),
        [link("Wrong number?","Change it","Change number D2")],step=(1,4)))

PWD=(f'<Frame w="fill" flex="col" gap={{16}}>'
     f'{field("Create password","lock","••••••••",ph=False,trailing=("eye","Show password"),helper="At least 8 characters, with a number and a symbol.")}'
     f'<Frame w="fill" flex="row" gap={{6}}><Rect grow={{1}} h={{5}} rounded={{999}} bg="var:state/success" />'
     f'<Rect grow={{1}} h={{5}} rounded={{999}} bg="var:state/success" /><Rect grow={{1}} h={{5}} rounded={{999}} bg="var:state/success" />'
     f'<Rect grow={{1}} h={{5}} rounded={{999}} bg="var:neutral/200" /></Frame>'
     f'{T(12,"medium","var:state/success","Strong password")}'
     f'{field("Confirm password","lock","••••••••",ph=False,trailing=("eye","Show confirm"))}</Frame>')
add("Doctor","D3-password",
    desk_form("Auth · Doctor — D3 Set Password",
        DP(eyebrow_t="For doctors",head_parts=[("Only you",False),("get in",True)],
           sub="A password plus your phone — proper protection for clinical data.",
           proofs=[proof("fingerprint","Two-factor login")]),
        "Step 3 of 4",[("Secure your",False),("account",True)],
        "You'll use this together with your phone each time you log in.",
        PWD,cta("Continue","Continue D3","arrow-right","btn-navy.jpg"),[],step=(2,4)),
    mob_form("Auth · Doctor — D3 Set Password · Mobile","Step 3 of 4",[("Secure your",False),("account",True)],
        "Used with your phone at each login.",PWD,
        cta("Continue","Continue D3","arrow-right","btn-navy.jpg"),[],step=(2,4)))

PEND_D=(f'<Frame w="fill" flex="col" gap={{16}} items="center">{big_icon("badge-check","warn")}'
        f'{T(15,"regular","var:text/muted","Thanks, Dr. Okafor. Our team is checking your MDCN licence against the council register — usually within 24–48 hours.",w="fill",align="center")}'
        f'{note("clock","We’ll text and email you the moment you’re approved. Your profile stays hidden until then.","warn")}</Frame>')
add("Doctor","D4-pending",
    desk_form("Auth · Doctor — D4 Verification Pending",
        DP(eyebrow_t="For doctors",head_parts=[("Trust,",False),("verified",True)],
           sub="Every doctor on Medra is a real, licensed professional. Patients count on it — so we check properly.",
           proofs=[proof("shield-check","Manual licence check")]),
        "Step 4 of 4",[("We're verifying",False),("your licence",True)],
        "You're almost in. Here's exactly what happens next.",
        PEND_D,cta("Set up my profile while I wait","Explore D4","arrow-right","btn-navy.jpg"),
        [link("Entered the wrong MDCN?","Update it","Update MDCN D4"),link("Questions?","Contact support","Support D4")],
        step=(3,4),back=False),
    mob_form("Auth · Doctor — D4 Verification Pending · Mobile","Step 4 of 4",
        [("Verifying your",False),("licence",True)],"Here's what happens next.",PEND_D,
        cta("Set up my profile","Explore D4","arrow-right","btn-navy.jpg"),
        [link("Questions?","Contact support","Support D4")],step=(3,4),back=False))

PROF_D=(f'<Frame w="fill" flex="col" gap={{18}}>'
        f'<Frame w="fill" flex="row" gap={{15}} items="center">'
        f'<Image image="assets/img/avatar-1.jpg" w={{74}} h={{74}} rounded={{999}} />'
        f'<Frame name="Btn Change photo" flex="row" gap={{8}} items="center" px={{16}} py={{11}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
        f'{I("camera",16,N_IC)}{T(13,"semibold","var:text/default","Change photo")}</Frame></Frame>'
        f'{field("Short bio","file-text","Cardiologist with 12 years experience…",ph=False)}'
        f'{field("Consultation fee","credit-card","15,000",prefix="₦",helper="You can change this anytime.")}'
        f'{field_chips("Consultation types",["In-person","Virtual","Both"],2,"Ctype")}</Frame>')
add("Doctor","D5-profile",
    desk_form("Auth · Doctor — D5 Profile Setup",
        DP(eyebrow_t="For doctors",head_parts=[("A strong first",False),("impression",True)],
           sub="A clear photo, a short bio and an honest fee help patients choose you with confidence.",
           proofs=[proof("star","Profile completeness 80%")]),
        "Your public profile",[("This is what",False),("patients see",True)],
        "You can edit all of this later from your dashboard.",
        PROF_D,cta("Finish and go to dashboard","Finish D5","arrow-right","btn-navy.jpg"),
        [link("","Do this later","Later D5")]),
    mob_form("Auth · Doctor — D5 Profile Setup · Mobile","Your public profile",
        [("What patients",False),("see",True)],"Editable later from your dashboard.",PROF_D,
        cta("Finish","Finish D5","arrow-right","btn-navy.jpg"),[link("","Do this later","Later D5")]))

D6B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone or email","user","dr.okafor@clinic.ng",ph=False)}'
     f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}'
     f'<Frame w="fill" flex="row" justify="end">{link("","Forgot password?","Forgot D6",center=False)}</Frame></Frame>')
add("Doctor","D6-login",
    desk_form("Auth · Doctor — D6 Log In",
        DP(eyebrow_t="Welcome back",head_parts=[("Your day,",False),("ready",True)],
           sub="Today's queue, patient histories and notes — one secure login away.",
           proofs=[proof("calendar-check","8 appointments today")]),
        "Doctor log in",[("Welcome back,",False),("doctor",True)],
        "Log in to see today's schedule and your patients.",
        D6B,cta("Log in","Login submit D6","arrow-right","btn-navy.jpg"),
        [link("New to Medra?","Register as a doctor","Register D6")]),
    mob_form("Auth · Doctor — D6 Log In · Mobile","Doctor log in",[("Welcome back,",False),("doctor",True)],
        "See today's schedule and patients.",
        f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone or email","user","dr.okafor@clinic.ng",ph=False)}'
        f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}</Frame>',
        cta("Log in","Login submit D6","arrow-right","btn-navy.jpg"),
        [link("Forgot password?","Reset it","Forgot D6"),link("New?","Register as a doctor","Register D6")]))

OTP_2FA=f'<Frame w="fill" flex="col" gap={{14}}>{otp("41")}{link("Didn’t get it?","Resend in 0:22","Resend D7")}</Frame>'
add("Doctor","D7-2fa",
    desk_form("Auth · Doctor — D7 Two-Factor",
        DP(eyebrow_t="Two-factor",head_parts=[("Two steps,",False),("total trust",True)],
           sub="Extra protection every time you open a patient's record.",
           proofs=[proof("fingerprint","2FA enabled")]),
        "Security check",[("Confirm",False),("it's you",True)],
        "We texted a 6-digit code to +234 803 555 0110 to protect patient data.",
        OTP_2FA,cta("Log in","2FA verify D7","arrow-right","btn-navy.jpg"),
        [link("Lost access to your phone?","Get help","Help D7")]),
    mob_form("Auth · Doctor — D7 Two-Factor · Mobile","Security check",[("Confirm",False),("it's you",True)],
        "Code sent to +234 803 555 0110.",OTP_2FA,
        cta("Log in","2FA verify D7","arrow-right","btn-navy.jpg"),
        [link("Lost your phone?","Get help","Help D7")]))

add("Doctor","D8-forgot",
    desk_form("Auth · Doctor — D8 Forgot Password",
        DP(eyebrow_t="Account recovery",head_parts=[("Locked out?",False),("No problem",True)],
           sub="A quick code and you're back with your patients."),
        "Reset password",[("Reset your",False),("password",True)],
        "Enter your phone or email and we'll send a 6-digit reset code.",
        field("Phone or email","user","dr.okafor@clinic.ng",ph=False,helper="We'll send the reset code here."),
        cta("Send reset code","Send reset D8","arrow-right","btn-navy.jpg"),
        [link("Remembered it?","Back to log in","Back login D8")]),
    mob_form("Auth · Doctor — D8 Forgot Password · Mobile","Reset password",[("Reset your",False),("password",True)],
        "We'll send a 6-digit reset code.",
        field("Phone or email","user","dr.okafor@clinic.ng",ph=False),
        cta("Send reset code","Send reset D8","arrow-right","btn-navy.jpg"),
        [link("Remembered it?","Back to log in","Back login D8")]))

NEWPWD=(f'<Frame w="fill" flex="col" gap={{16}}>'
        f'{field("New password","lock","••••••••",ph=False,trailing=("eye","Show password"),helper="At least 8 characters, with a number and a symbol.")}'
        f'{field("Confirm new password","lock","••••••••",ph=False,trailing=("eye","Show confirm"))}</Frame>')
add("Doctor","D9-reset",
    desk_form("Auth · Doctor — D9 New Password",
        DP(eyebrow_t="Account recovery",head_parts=[("Back in",False),("safe hands",True)],
           sub="New password set — let's get you back to work."),
        "New password",[("Choose a new",False),("password",True)],
        "Make it strong — it protects your patients' records.",
        NEWPWD,cta("Save and log in","Save password D9","arrow-right","btn-navy.jpg"),[]),
    mob_form("Auth · Doctor — D9 New Password · Mobile","New password",[("Choose a new",False),("password",True)],
        "It protects your patients' records.",NEWPWD,
        cta("Save and log in","Save password D9","arrow-right","btn-navy.jpg"),[]))

SUC_D=(f'<Frame w="fill" flex="col" gap={{16}} items="center">{big_icon("circle-check","ok")}'
       f'{T(15,"regular","var:text/muted","You’re verified and live. Patients in Abuja can now find and book you.",w="fill",align="center")}'
       f'{note("info","Taking you to your dashboard and today’s schedule…","info")}</Frame>')
add("Doctor","D10-success",
    desk("Auth · Doctor — D10 Success",
        desk_panel("d-panel-doctor.jpg","You're live",[("Verified on",False),("Medra",True)],
                   "Visible, bookable and ready to see patients.",
                   stats=[("Live","Profile"),("0","Pending tasks"),("48h","Verified in")]),
        f'{eyebrow("All set")}{head_chip([("Welcome aboard,",False),("Dr. Okafor",True)],32)}{SUC_D}'
        f'{cta("Go to my dashboard","Go dashboard D10","layout-dashboard","btn-navy.jpg")}'
        f'{ghost("Set my weekly availability","Availability D10","calendar-days")}'),
    mob_hero("Auth · Doctor — D10 Success · Mobile","m-hero-doctor.jpg","All set",
        [("Welcome aboard,",False),("doctor",True)],"You're verified — patients can book you now.",
        cta("Go to my dashboard","Go dashboard D10","layout-dashboard","btn-navy.jpg"),
        [ghost("Set my availability","Availability D10","calendar-days")],skip=False,
        proofs=[proof("badge-check","MDCN verified")]))

# ============================================================ INSTITUTION
IP=lambda **kw: desk_panel("d-panel-institution.jpg",**kw)
I1B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Institution name","hospital","Garki Medical Centre",ph=False)}'
     f'{field_chips("Type",["Private hospital","Clinic","Diagnostic centre"],0,"Itype")}'
     f'{field("Admin full name","user","Yusuf Bello",ph=False)}'
     f'{field("Work email","mail","admin@garkimedical.ng",ph=False)}'
     f'{field("Admin phone","phone","802 111 2233",prefix="+234")}</Frame>')
add("Institution","I1-register",
    desk_form("Auth · Institution — I1 Register",
        IP(eyebrow_t="For institutions",head_parts=[("Run your facility,",False),("digitally",True)],
           sub="Bookings, staff, records and billing — one system for the whole institution.",
           proofs=[proof("building-2","Multi-branch ready"),proof("sparkles","30-day free trial")],
           stats=[("30","Day trial"),("1-2","Days to verify"),("Free","To start")]),
        "Step 1 of 5",[("Register your",False),("institution",True)],
        "Set up your clinic or hospital on Medra. You'll be the facility admin.",
        I1B,cta("Continue","Continue I1","arrow-right","btn-navy.jpg"),
        [link("Institution already on Medra?","Admin log in","Admin login I")],step=(0,5)),
    mob_form("Auth · Institution — I1 Register · Mobile","Step 1 of 5",
        [("Register your",False),("institution",True)],"You'll be the facility admin.",
        I1B,cta("Continue","Continue I1","arrow-right","btn-navy.jpg"),
        [link("Already on Medra?","Admin log in","Admin login I")],step=(0,5)))

DOCS=(f'<Frame w="fill" flex="col" gap={{13}}>{upload("Upload licence",done=True)}'
      f'{upload("Upload cac",done=False,label="CAC certificate")}'
      f'{note("shield-check","Documents are encrypted and used only to verify your institution.","info")}</Frame>')
add("Institution","I2-documents",
    desk_form("Auth · Institution — I2 Verify Documents",
        IP(eyebrow_t="For institutions",head_parts=[("Verified",False),("institutions only",True)],
           sub="Patients trust Medra because every provider on it has been checked by a human.",
           proofs=[proof("file-check","Licence + CAC")]),
        "Step 2 of 5",[("Upload your",False),("documents",True)],
        "We verify every institution before it goes live. Add your practice licence and CAC certificate.",
        DOCS,cta("Continue","Continue I2","arrow-right","btn-navy.jpg"),
        [link("Don't have them handy?","Save and finish later","Save later I2")],step=(1,5)),
    mob_form("Auth · Institution — I2 Verify Documents · Mobile","Step 2 of 5",
        [("Upload your",False),("documents",True)],"Practice licence and CAC certificate.",DOCS,
        cta("Continue","Continue I2","arrow-right","btn-navy.jpg"),
        [link("","Save and finish later","Save later I2")],step=(1,5)))

PLANS=(f'<Frame w="fill" flex="col" gap={{11}}>'
       f'{plan("Single practice","₦___","One doctor · core booking and records")}'
       f'{plan("Multi-doctor","₦___","Up to 15 doctors · staff roles and allocation",sel=True)}'
       f'{plan("Multi-branch","Custom","Enterprise · every branch billed as one")}'
       f'{note("sparkles","Every plan starts with a 30-day free trial — no card required.","ok")}</Frame>')
add("Institution","I3-plan",
    desk_form("Auth · Institution — I3 Choose Plan",
        IP(eyebrow_t="For institutions",head_parts=[("Priced to",False),("your size",True)],
           sub="From a single practice to a multi-branch group — pay only for what you need.",
           proofs=[proof("credit-card","Paystack billing")]),
        "Step 3 of 5",[("Pick a",False),("plan",True)],
        "Choose the size that fits today — you can upgrade anytime. Final pricing is confirmed with our team.",
        PLANS,cta("Start my free trial","Start trial I3"),
        [link("Not sure which fits?","Talk to our team","Sales I3")],step=(2,5)),
    mob_form("Auth · Institution — I3 Choose Plan · Mobile","Step 3 of 5",[("Pick a",False),("plan",True)],
        "Upgrade anytime. Every plan starts with a 30-day trial.",PLANS,
        cta("Start my free trial","Start trial I3"),[link("Not sure?","Talk to our team","Sales I3")],step=(2,5)))

OTP_I=f'<Frame w="fill" flex="col" gap={{14}}>{otp("77")}{link("Didn’t get it?","Resend in 0:25","Resend I4")}</Frame>'
add("Institution","I4-otp",
    desk_form("Auth · Institution — I4 Verify Admin",
        IP(eyebrow_t="For institutions",head_parts=[("Secure the",False),("admin account",True)],
           sub="The facility admin controls staff and billing — so we protect it properly.",
           proofs=[proof("lock","Encrypted")]),
        "Step 4 of 5",[("Verify the",False),("admin phone",True)],
        "Enter the 6-digit code sent to +234 802 111 2233.",
        OTP_I,cta("Verify","Verify I4","arrow-right","btn-navy.jpg"),
        [link("Wrong number?","Change it","Change number I4")],step=(3,5)),
    mob_form("Auth · Institution — I4 Verify Admin · Mobile","Step 4 of 5",
        [("Verify the",False),("admin phone",True)],"Code sent to +234 802 111 2233.",OTP_I,
        cta("Verify","Verify I4","arrow-right","btn-navy.jpg"),
        [link("Wrong number?","Change it","Change number I4")],step=(3,5)))

PWD_I=PWD.replace("Create password","Create admin password")
add("Institution","I5-password",
    desk_form("Auth · Institution — I5 Set Password",
        IP(eyebrow_t="For institutions",head_parts=[("One",False),("key-holder",True)],
           sub="Strong protection for the account that runs your facility."),
        "Step 5 of 5",[("Secure the",False),("admin account",True)],
        "You'll use this together with the admin phone to log in.",
        PWD_I,cta("Create account","Create I5","arrow-right","btn-navy.jpg"),[],step=(4,5)),
    mob_form("Auth · Institution — I5 Set Password · Mobile","Step 5 of 5",
        [("Secure the",False),("admin account",True)],"Used with the admin phone to log in.",
        PWD_I,cta("Create account","Create I5","arrow-right","btn-navy.jpg"),[],step=(4,5)))

PEND_I=(f'<Frame w="fill" flex="col" gap={{16}} items="center">{big_icon("badge-check","warn")}'
        f'{T(15,"regular","var:text/muted","Thanks, Mr. Bello. We’re reviewing Garki Medical Centre’s documents — usually within 1–2 business days.",w="fill",align="center")}'
        f'{note("clock","We’ll email you the moment you’re approved. Meanwhile you can add staff and set up your rooms.","warn")}</Frame>')
add("Institution","I6-pending",
    desk_form("Auth · Institution — I6 Application Submitted",
        IP(eyebrow_t="Welcome to Medra for Business",head_parts=[("Your facility's new",False),("operating system",True)],
           sub="Your 30-day trial starts today — set things up while we verify.",
           proofs=[proof("sparkles","Trial active · 30 days left")]),
        "Submitted",[("Application",False),("submitted",True)],"Here's exactly what happens next.",
        PEND_I,cta("Go to admin portal","Go portal I6","layout-dashboard","btn-navy.jpg"),
        [link("Need to add a document?","Manage application","Manage I6")],back=False),
    mob_form("Auth · Institution — I6 Application Submitted · Mobile","Submitted",
        [("Application",False),("submitted",True)],"Your 30-day trial has started.",PEND_I,
        cta("Go to admin portal","Go portal I6","layout-dashboard","btn-navy.jpg"),
        [link("","Manage application","Manage I6")],back=False))

I7B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Work email","mail","admin@garkimedical.ng",ph=False)}'
     f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}'
     f'<Frame w="fill" flex="row" justify="end">{link("","Forgot password?","Forgot I7",center=False)}</Frame></Frame>')
add("Institution","I7-admin-login",
    desk_form("Auth · Institution — I7 Facility Admin Log In",
        IP(eyebrow_t="Welcome back",head_parts=[("Your facility,",False),("in control",True)],
           sub="Everything that runs your clinic, one secure login away.",
           proofs=[proof("calendar-check","12 bookings today")]),
        "Facility admin",[("Facility admin",False),("log in",True)],
        "Sign in to manage bookings, staff and billing.",
        I7B,cta("Log in","Login submit I7","arrow-right","btn-navy.jpg"),
        [link("Registering a new institution?","Start here","Register I7")]),
    mob_form("Auth · Institution — I7 Facility Admin Log In · Mobile","Facility admin",
        [("Facility admin",False),("log in",True)],"Manage bookings, staff and billing.",
        f'<Frame w="fill" flex="col" gap={{16}}>{field("Work email","mail","admin@garkimedical.ng",ph=False)}'
        f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}</Frame>',
        cta("Log in","Login submit I7","arrow-right","btn-navy.jpg"),
        [link("Forgot password?","Reset it","Forgot I7"),link("New institution?","Start here","Register I7")]))

add("Institution","I8-forgot",
    desk_form("Auth · Institution — I8 Forgot Password",
        IP(eyebrow_t="Account recovery",head_parts=[("Locked out?",False),("We'll fix that",True)],
           sub="A quick code and your facility is back online."),
        "Reset password",[("Reset admin",False),("password",True)],
        "Enter the admin email and we'll send a reset code.",
        field("Work email","mail","admin@garkimedical.ng",ph=False,helper="We'll send the reset code here."),
        cta("Send reset code","Send reset I8","arrow-right","btn-navy.jpg"),
        [link("Remembered it?","Back to log in","Back login I8")]),
    mob_form("Auth · Institution — I8 Forgot Password · Mobile","Reset password",
        [("Reset admin",False),("password",True)],"We'll send a reset code.",
        field("Work email","mail","admin@garkimedical.ng",ph=False),
        cta("Send reset code","Send reset I8","arrow-right","btn-navy.jpg"),
        [link("Remembered it?","Back to log in","Back login I8")]))

add("Institution","I9-reset",
    desk_form("Auth · Institution — I9 New Password",
        IP(eyebrow_t="Account recovery",head_parts=[("Back in",False),("control",True)],
           sub="New password set — your facility awaits."),
        "New password",[("Choose a new",False),("password",True)],
        "Make it strong — it controls your whole facility.",
        NEWPWD,cta("Save and log in","Save password I9","arrow-right","btn-navy.jpg"),[]),
    mob_form("Auth · Institution — I9 New Password · Mobile","New password",
        [("Choose a new",False),("password",True)],"It controls your whole facility.",NEWPWD,
        cta("Save and log in","Save password I9","arrow-right","btn-navy.jpg"),[]))

SUC_I=(f'<Frame w="fill" flex="col" gap={{16}} items="center">{big_icon("circle-check","ok")}'
       f'{T(15,"regular","var:text/muted","Garki Medical Centre is approved and live on Medra. Patients in Abuja can book your doctors now.",w="fill",align="center")}'
       f'{note("info","Taking you to your admin portal…","info")}</Frame>')
add("Institution","I10-success",
    desk("Auth · Institution — I10 Success",
        desk_panel("d-panel-institution.jpg","You're live",[("Your facility is",False),("on Medra",True)],
                   "Start adding doctors and taking bookings today.",
                   stats=[("Live","Status"),("30","Trial days left"),("0","Doctors added")]),
        f'{eyebrow("Approved")}{head_chip([("You’re live,",False),("Mr. Bello",True)],32)}{SUC_I}'
        f'{cta("Go to admin portal","Go portal I10","layout-dashboard","btn-navy.jpg")}'
        f'{ghost("Invite my doctors","Invite I10","user-plus")}'),
    mob_hero("Auth · Institution — I10 Success · Mobile","m-hero-institution.jpg","Approved",
        [("You're live,",False),("Mr. Bello",True)],"Your facility is verified and taking bookings.",
        cta("Go to admin portal","Go portal I10","layout-dashboard","btn-navy.jpg"),
        [ghost("Invite my doctors","Invite I10","user-plus")],skip=False,
        proofs=[proof("circle-check","Approved")]))

# ---------------- write ----------------
def sanitize(s): return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)','&amp;',s)
manifest={}
for page,fn,jsx in frames:
    open(os.path.join(OUT,fn),"w").write(sanitize(jsx))
    manifest.setdefault(page,[]).append(fn)
open(os.path.join(OUT,"pages.json"),"w").write(json.dumps(manifest,indent=2))

PAGE_FIGMA={"Entry":"Medra Auth — Entry","Patient":"Medra Auth — Patient",
            "Doctor":"Medra Auth — Doctor","Institution":"Medra Auth — Institution"}
TRN=[
 ("E1-onb1","Btn Next E1-onb1","E2-onb2"),("E1-onb1","Btn Skip E1-onb1","E4-welcome"),("E1-onb1","Btn Skip","E4-welcome"),
 ("E2-onb2","Btn Next E2-onb2","E3-onb3"),("E2-onb2","Btn Skip E2-onb2","E4-welcome"),("E2-onb2","Btn Skip","E4-welcome"),
 ("E3-onb3","Btn Next E3-onb3","E4-welcome"),("E3-onb3","Btn Skip E3-onb3","E4-welcome"),("E3-onb3","Btn Skip","E4-welcome"),
 ("E4-welcome","Btn Create account","E5-role"),("E4-welcome","Btn Login entry","P6-login"),
 ("E5-role","Btn Role Patient","P1-create"),("E5-role","Btn Role Doctor","D1-create"),
 ("E5-role","Btn Role Institution","I1-register"),("E5-role","Btn Continue role","P1-create"),
 ("E5-role","Btn Back","E4-welcome"),("E5-role","Btn Help role","E1-onb1"),("E5-role","Btn Help","P7-help"),
 ("P1-create","Btn Send code P1","P2-otp"),("P1-create","Btn Login P","P6-login"),("P1-create","Btn Back","E5-role"),("P1-create","Btn Help","P7-help"),
 ("P2-otp","Btn Verify P2","P3-name"),("P2-otp","Btn Change number P2","P1-create"),
 ("P2-otp","Btn Help code P2","P7-help"),("P2-otp","Btn Resend P2","P2-otp"),("P2-otp","Btn Back","P1-create"),("P2-otp","Btn Help","P7-help"),
 ("P3-name","Btn Continue P3","P4-about"),("P3-name","Btn Skip P3","P4-about"),("P3-name","Btn Back","P2-otp"),("P3-name","Btn Help","P7-help"),
 ("P4-about","Btn Continue P4","P5-health"),("P4-about","Btn Skip P4","P5-health"),("P4-about","Btn Back","P3-name"),("P4-about","Btn Help","P7-help"),
 ("P5-health","Btn Finish P5","P8-success"),("P5-health","Btn Skip P5","P8-success"),("P5-health","Btn Back","P4-about"),("P5-health","Btn Help","P7-help"),
 ("P6-login","Btn Send code P6","P2-otp"),("P6-login","Btn Create P6","P1-create"),
 ("P6-login","Btn Help P6","P7-help"),("P6-login","Btn Back","E4-welcome"),("P6-login","Btn Help","P7-help"),
 ("P7-help","Btn Back to OTP","P2-otp"),("P7-help","Btn Resend help","P2-otp"),("P7-help","Btn Call help","P2-otp"),
 ("P7-help","Btn Change help","P1-create"),("P7-help","Btn Support help","P7-help"),("P7-help","Btn Back","P2-otp"),("P7-help","Btn Help","P7-help"),
 ("P8-success","Btn Go home P8","E4-welcome"),("P8-success","Btn Explore P8","E4-welcome"),
 ("D1-create","Btn Continue D1","D2-otp"),("D1-create","Btn Login D","D6-login"),("D1-create","Btn Back","E5-role"),("D1-create","Btn Help","P7-help"),
 ("D2-otp","Btn Verify D2","D3-password"),("D2-otp","Btn Change number D2","D1-create"),
 ("D2-otp","Btn Resend D2","D2-otp"),("D2-otp","Btn Back","D1-create"),("D2-otp","Btn Help","P7-help"),
 ("D3-password","Btn Continue D3","D4-pending"),("D3-password","Btn Back","D2-otp"),("D3-password","Btn Help","P7-help"),
 ("D4-pending","Btn Explore D4","D5-profile"),("D4-pending","Btn Update MDCN D4","D1-create"),("D4-pending","Btn Support D4","P7-help"),("D4-pending","Btn Help","P7-help"),
 ("D5-profile","Btn Finish D5","D10-success"),("D5-profile","Btn Later D5","D10-success"),("D5-profile","Btn Back","D4-pending"),("D5-profile","Btn Help","P7-help"),
 ("D6-login","Btn Login submit D6","D7-2fa"),("D6-login","Btn Forgot D6","D8-forgot"),
 ("D6-login","Btn Register D6","D1-create"),("D6-login","Btn Back","E4-welcome"),("D6-login","Btn Help","P7-help"),
 ("D7-2fa","Btn 2FA verify D7","D10-success"),("D7-2fa","Btn Resend D7","D7-2fa"),
 ("D7-2fa","Btn Help D7","D8-forgot"),("D7-2fa","Btn Back","D6-login"),("D7-2fa","Btn Help","P7-help"),
 ("D8-forgot","Btn Send reset D8","D9-reset"),("D8-forgot","Btn Back login D8","D6-login"),("D8-forgot","Btn Back","D6-login"),("D8-forgot","Btn Help","P7-help"),
 ("D9-reset","Btn Save password D9","D6-login"),("D9-reset","Btn Back","D8-forgot"),("D9-reset","Btn Help","P7-help"),
 ("D10-success","Btn Go dashboard D10","E4-welcome"),("D10-success","Btn Availability D10","E4-welcome"),
 ("I1-register","Btn Continue I1","I2-documents"),("I1-register","Btn Admin login I","I7-admin-login"),("I1-register","Btn Back","E5-role"),("I1-register","Btn Help","P7-help"),
 ("I2-documents","Btn Continue I2","I3-plan"),("I2-documents","Btn Save later I2","I3-plan"),
 ("I2-documents","Btn Upload cac","I2-documents"),("I2-documents","Btn Back","I1-register"),("I2-documents","Btn Help","P7-help"),
 ("I3-plan","Btn Start trial I3","I4-otp"),("I3-plan","Btn Sales I3","I3-plan"),("I3-plan","Btn Back","I2-documents"),("I3-plan","Btn Help","P7-help"),
 ("I4-otp","Btn Verify I4","I5-password"),("I4-otp","Btn Change number I4","I1-register"),
 ("I4-otp","Btn Resend I4","I4-otp"),("I4-otp","Btn Back","I3-plan"),("I4-otp","Btn Help","P7-help"),
 ("I5-password","Btn Create I5","I6-pending"),("I5-password","Btn Back","I4-otp"),("I5-password","Btn Help","P7-help"),
 ("I6-pending","Btn Go portal I6","I10-success"),("I6-pending","Btn Manage I6","I2-documents"),("I6-pending","Btn Help","P7-help"),
 ("I7-admin-login","Btn Login submit I7","I10-success"),("I7-admin-login","Btn Forgot I7","I8-forgot"),
 ("I7-admin-login","Btn Register I7","I1-register"),("I7-admin-login","Btn Back","E4-welcome"),("I7-admin-login","Btn Help","P7-help"),
 ("I8-forgot","Btn Send reset I8","I9-reset"),("I8-forgot","Btn Back login I8","I7-admin-login"),("I8-forgot","Btn Back","I7-admin-login"),("I8-forgot","Btn Help","P7-help"),
 ("I9-reset","Btn Save password I9","I7-admin-login"),("I9-reset","Btn Back","I8-forgot"),("I9-reset","Btn Help","P7-help"),
 ("I10-success","Btn Go portal I10","E4-welcome"),("I10-success","Btn Invite I10","E4-welcome"),
]
resolved=[]
for a,hot,b in TRN:
    if a in NAMES and b in NAMES:
        resolved.append([NAMES[a][0],hot,NAMES[b][0]]); resolved.append([NAMES[a][1],hot,NAMES[b][1]])
order_js={PAGE_FIGMA[p]:[[NAMES[f][0],NAMES[f][1]] for f in fids] for p,fids in ORDER.items()}
starts_js={PAGE_FIGMA[p]:NAMES[fids[0]][0] for p,fids in ORDER.items()}

linker=("(async () => {\n"
 "  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();\n"
 "  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();\n"
 "  const pages = figma.root.children.filter(n => n.type==='PAGE');\n"
 "  const byName = {}; for (const pg of pages) for (const f of pg.children) if (f.type==='FRAME') byName[norm(f.name)] = f;\n"
 "  const F = n => byName[norm(n)];\n"
 "  const findAll = (root,t) => { const out=[]; const target=norm(t); const w=n=>{ if(n.name&&norm(n.name)===target) out.push(n); if('children'in n) n.children.forEach(w); }; w(root); return out; };\n"
 "  const transition = { type:'SMART_ANIMATE', easing:{type:'EASE_OUT'}, duration:0.25 };\n"
 f"  const TRN = {json.dumps(resolved)};\n"
 f"  const ORDER = {json.dumps(order_js)};\n"
 f"  const STARTS = {json.dumps(starts_js)};\n"
 "  const jobs=[], missing=[];\n"
 "  for (const [fromN,hot,toN] of TRN){ const fr=F(fromN), to=F(toN); if(!fr||!to) continue;\n"
 "    const nodes=findAll(fr,hot); if(!nodes.length){ missing.push(fromN+' -> '+hot); continue; }\n"
 "    for (const nd of nodes) jobs.push([nd,to]); }\n"
 "  let linked=0; for (const [nd,to] of jobs){ await nd.setReactionsAsync([{ trigger:{type:'ON_CLICK'}, actions:[{ type:'NODE', destinationId:to.id, navigation:'NAVIGATE', transition }] }]); linked++; }\n"
 "  const GX=170, GY=150;\n"
 "  for (const pg of pages){ const ord=ORDER[pg.name]; if(!ord) continue; let x=0, rowH=0;\n"
 "    for (const [dn,mn] of ord){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const [dn,mn] of ord){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(s&&F(s)) pg.flowStartingPoints=[{ nodeId:F(s).id, name:'Start' }]; }\n"
 "  return { linked, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT,"link-auth.js"),"w").write(linker)

ps=["# Medra Auth — render each persona onto its own Figma page (Figma Desktop open + connected).",
    'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
    'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
    "figma-cli tokens import-design-md .\\DESIGN.md",""]
for p,fids in ORDER.items():
    ps.append(f'# ---- {PAGE_FIGMA[p]} ----')
    ps.append(f'figma-cli eval "(async()=>{{const t=’{PAGE_FIGMA[p]}’;let p=figma.root.children.find(n=>n.name===t);if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"')
    lst=", ".join("'"+f+"'" for fid in fids for f in (fid+"-d.jsx",fid+"-m.jsx"))
    ps.append(f'foreach ($f in @({lst})) {{ figma-cli render (Get-Content $f -Raw) }}')
    ps.append("")
ps.append("# Wire the clickable prototype + arrange every page")
ps.append("figma-cli run .\\link-auth.js")
open(os.path.join(OUT,"render-auth.ps1"),"w").write("\n".join(ps))

print(f"{len(frames)} frames · {len(manifest)} pages · {len(resolved)} links")
for p,fs in manifest.items(): print(f"  {p}: {len(fs)}")
