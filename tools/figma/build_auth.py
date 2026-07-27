#!/usr/bin/env python3
"""Medra — Authentication module screens (Editorial Light+). Desktop 1440x900 + Mobile 390x844.
One .jsx = one Figma frame. Organised by persona (rendered onto separate pages)."""
import os, re
OUT = "/home/user/Medra-24/figma/medra-auth"
os.makedirs(OUT, exist_ok=True)

# icon colours use hex (avoids the /-in-token Icon parser bug)
IC_MUTED="#7E8F9D"; IC_NAVY="#1B3A5B"; IC_TEAL="#39B0CF"; IC_ACCENT="#2F8BAC"; IC_WHITE="#FFFFFF"
IC_OK="#2FA36B"; IC_WARN="#E0A32E"; IC_ERR="#D14343"

# ---------------- shared components ----------------
def T(size, weight, color, txt, w=None, align=None):
    a=f' align="{align}"' if align else ''
    ww=f' w={{{w}}}' if isinstance(w,int) else (' w="fill"' if w=="fill" else '')
    return f'<Text font="Inter" size={{{size}}} weight="{weight}" color="{color}"{ww}{a}>{txt}</Text>'

def icon(n,size=18,color=IC_MUTED):
    return f'<Icon name="lucide:{n}" size={{{size}}} color="{color}" />'

def eyebrow(txt, color="var:text/accent"):
    return T(12,"semibold",color,txt.upper())

def hairline(w=64):
    return (f'<Frame w="fill" flex="row" items="center" gap={{0}}>'
            f'<Rect w={{{w}}} h={{3}} bg="var:brand/teal" rounded={{999}} />'
            f'<Rect grow={{1}} h={{1}} bg="var:border/subtle" /></Frame>')

def field(label, ic, value, placeholder=True, helper=None, error=None, focus=False, trailing=None, prefix=None):
    border = "var:state/error" if error else ("var:border/accent" if focus else "var:border/default")
    bw = 2 if (focus or error) else 1
    valcol = "var:text/faint" if placeholder else "var:text/strong"
    pre = (f'<Text font="Inter" size={{15}} weight="semibold" color="var:text/default">{prefix}</Text>'
           f'<Rect w={{1}} h={{22}} bg="var:border/default" />') if prefix else ''
    tr = (f'<Frame name="Btn {trailing[1]}" flex="row" items="center">{icon(trailing[0],18,IC_MUTED)}</Frame>') if trailing else ''
    sub = ''
    if error: sub = f'<Frame flex="row" gap={{6}} items="center">{icon("circle-alert",14,IC_ERR)}{T(12,"medium","var:state/error",error)}</Frame>'
    elif helper: sub = T(12,"regular","var:text/muted",helper)
    return (f'<Frame w="fill" flex="col" gap={{7}}>'
            f'<Text font="Inter" size={{13}} weight="medium" color="var:text/default">{label}</Text>'
            f'<Frame w="fill" flex="row" gap={{10}} items="center" px={{16}} py={{14}} rounded={{12}} bg="var:bg/base" stroke="{border}" strokeWidth={{{bw}}}>'
            f'{icon(ic,18,IC_TEAL if focus else IC_MUTED)}{pre}'
            f'<Text font="Inter" size={{15}} weight="regular" color="{valcol}" grow={{1}}>{value}</Text>{tr}</Frame>'
            f'{sub}</Frame>')

def select_field(label, ic, value, placeholder=True):
    valcol="var:text/faint" if placeholder else "var:text/strong"
    return (f'<Frame w="fill" flex="col" gap={{7}}>'
            f'<Text font="Inter" size={{13}} weight="medium" color="var:text/default">{label}</Text>'
            f'<Frame w="fill" flex="row" gap={{10}} items="center" px={{16}} py={{14}} rounded={{12}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
            f'{icon(ic,18,IC_MUTED)}<Text font="Inter" size={{15}} weight="regular" color="{valcol}" grow={{1}}>{value}</Text>{icon("chevron-down",18,IC_MUTED)}</Frame></Frame>')

def otp(n=6, filled="", error=False):
    boxes=""
    for i in range(n):
        f = i < len(filled)
        active = i == len(filled)
        col = "var:state/error" if error else ("var:border/accent" if active else ("var:brand/navy" if f else "var:border/default"))
        bw = 2 if (active or error or f) else 1
        ch = filled[i] if f else ""
        boxes += (f'<Frame grow={{1}} h={{60}} flex="col" justify="center" items="center" rounded={{12}} bg="var:bg/base" stroke="{col}" strokeWidth={{{bw}}}>'
                  f'{T(24,"bold","var:text/strong",ch) if ch else ""}</Frame>')
    return f'<Frame w="fill" flex="row" gap={{10}}>{boxes}</Frame>'

def button(label, kind="primary", ic=None, block=True, name=None, trailing=None):
    styles={"primary":'bg="var:brand/navy"',"teal":'bg="var:brand/teal"',
            "secondary":'bg="var:bg/base" stroke="var:border/strong" strokeWidth={1}',
            "ghost":'bg="var:bg/subtle"',"disabled":'bg="var:neutral/200"'}
    txt={"primary":"var:text/on-dark","teal":"var:text/on-dark","secondary":"var:text/default",
         "ghost":"var:text/default","disabled":"var:text/faint"}[kind]
    icol=IC_WHITE if kind in ("primary","teal") else IC_NAVY
    lead=icon(ic,18,icol) if ic else ''
    trail=icon(trailing,18,icol) if trailing else ''
    nm=f' name="Btn {name or label}"'
    grow=' w="fill"' if block else ''
    return (f'<Frame{nm}{grow} flex="row" gap={{8}} items="center" justify="center" px={{22}} py={{15}} rounded={{12}} {styles[kind]}>'
            f'{lead}<Text font="Inter" size={{15}} weight="semibold" color="{txt}">{label}</Text>{trail}</Frame>')

def linkrow(pre, link, name):
    return (f'<Frame w="fill" flex="row" gap={{6}} justify="center" items="center">'
            f'{T(14,"regular","var:text/muted",pre)}'
            f'<Frame name="Btn {name}" flex="row"><Text font="Inter" size={{14}} weight="semibold" color="var:text/accent">{link}</Text></Frame></Frame>')

def stepper(i,total):
    dots=""
    for k in range(total):
        if k<i: dots+=f'<Rect w={{22}} h={{6}} rounded={{999}} bg="var:brand/teal" />'
        elif k==i: dots+=f'<Rect w={{28}} h={{6}} rounded={{999}} bg="var:brand/navy" />'
        else: dots+=f'<Rect w={{14}} h={{6}} rounded={{999}} bg="var:neutral/200" />'
    return f'<Frame flex="row" gap={{6}} items="center">{dots}</Frame>'

def note(ic, txt, tone="info"):
    bg={"info":"var:state/info-bg","ok":"var:state/success-bg","warn":"var:state/warning-bg"}[tone]
    col={"info":IC_ACCENT,"ok":IC_OK,"warn":IC_WARN}[tone]
    return (f'<Frame w="fill" flex="row" gap={{10}} items="start" p={{14}} rounded={{12}} bg="{bg}">'
            f'{icon(ic,17,col)}<Text font="Inter" size={{13}} weight="regular" color="var:text/default" grow={{1}}>{txt}</Text></Frame>')

def checkbox(label, checked=True, name="consent"):
    box=(f'<Frame w={{22}} h={{22}} rounded={{6}} bg="var:brand/teal" flex="col" justify="center" items="center">{icon("check",14,IC_WHITE)}</Frame>'
         if checked else f'<Rect w={{22}} h={{22}} rounded={{6}} bg="var:bg/base" stroke="var:border/strong" strokeWidth={{1}} />')
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{10}} items="start">{box}'
            f'<Text font="Inter" size={{13}} weight="regular" color="var:text/muted" grow={{1}}>{label}</Text></Frame>')

def choice_card(ic, title, desc, name):
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={{16}} items="center" p={{20}} rounded={{16}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>'
            f'<Frame w={{52}} h={{52}} rounded={{14}} bg="var:bg/muted" flex="col" justify="center" items="center">{icon(ic,24,IC_ACCENT)}</Frame>'
            f'<Frame grow={{1}} flex="col" gap={{3}}>{T(17,"semibold","var:text/strong",title)}{T(13,"regular","var:text/muted",desc,w="fill")}</Frame>'
            f'{icon("chevron-right",20,IC_TEAL)}</Frame>')

def plan_card(title, price, sub, selected=False):
    bd="var:border/accent" if selected else "var:border/default"; bw=2 if selected else 1
    tick=(f'<Frame w={{22}} h={{22}} rounded={{999}} bg="var:brand/teal" flex="col" justify="center" items="center">{icon("check",13,IC_WHITE)}</Frame>'
          if selected else f'<Rect w={{22}} h={{22}} rounded={{999}} stroke="var:border/strong" strokeWidth={{1}} bg="var:bg/base" />')
    return (f'<Frame grow={{1}} flex="col" gap={{10}} p={{20}} rounded={{16}} bg="var:bg/base" stroke="{bd}" strokeWidth={{{bw}}}>'
            f'<Frame w="fill" flex="row" justify="between" items="center">{T(15,"semibold","var:text/strong",title)}{tick}</Frame>'
            f'<Frame flex="row" gap={{4}} items="end">{T(26,"bold","var:text/strong",price)}{T(13,"regular","var:text/muted","/mo")}</Frame>'
            f'{T(12,"regular","var:text/muted",sub,w="fill")}</Frame>')

def upload_box(name="licence", done=False):
    if done:
        return (f'<Frame w="fill" flex="row" gap={{12}} items="center" p={{16}} rounded={{14}} bg="var:state/success-bg" stroke="var:border/subtle" strokeWidth={{1}}>'
                f'{icon("file-check",22,IC_OK)}<Frame grow={{1}} flex="col" gap={{1}}>{T(14,"semibold","var:text/strong","practice-licence.pdf")}{T(12,"regular","var:text/muted","1.2 MB · uploaded")}</Frame>'
                f'<Frame name="Btn Remove licence" flex="row">{icon("x",18,IC_MUTED)}</Frame></Frame>')
    return (f'<Frame name="Btn Upload {name}" w="fill" flex="col" gap={{8}} items="center" py={{28}} px={{20}} rounded={{14}} bg="var:bg/subtle" stroke="var:border/accent" strokeWidth={{1}}>'
            f'{icon("upload",26,IC_ACCENT)}'
            f'{T(14,"semibold","var:text/default","Tap to upload or drag &amp; drop")}'
            f'{T(12,"regular","var:text/muted","PDF, JPG or PNG · up to 10 MB")}'
            f'<Frame flex="row" gap={{8}} pt={{4}}>'
            f'<Frame flex="row" gap={{6}} items="center" px={{12}} py={{7}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{icon("camera",14,IC_NAVY)}{T(12,"medium","var:text/default","Camera")}</Frame>'
            f'<Frame flex="row" gap={{6}} items="center" px={{12}} py={{7}} rounded={{999}} bg="var:bg/base" stroke="var:border/default" strokeWidth={{1}}>{icon("file-text",14,IC_NAVY)}{T(12,"medium","var:text/default","Files")}</Frame>'
            f'</Frame></Frame>')

def back_link(name="Back"):
    return (f'<Frame name="Btn {name}" flex="row" gap={{6}} items="center">{icon("arrow-left",18,IC_NAVY)}'
            f'{T(14,"semibold","var:text/default","Back")}</Frame>')

# ---------------- shells ----------------
PANEL_H = {"patient":"panel-patient.png","doctor":"panel-doctor.png","institution":"panel-institution.png","entry":"panel-patient.png"}
BAND = {"patient":"band-patient.png","doctor":"band-doctor.png","institution":"band-institution.png","entry":"band-patient.png"}
PLABEL = {"patient":"For patients","doctor":"For doctors","institution":"For institutions","entry":"Welcome to Medra"}

def desktop(name, persona, head, sub, body, primary, secondaries=(), footer=None, eb=None, back=False, step=None, panel_head=None, panel_sub=None, panel_img=None):
    img = panel_img or PANEL_H[persona]
    sec = "".join(secondaries)
    steprow = f'{stepper(step[0],step[1])}' if step else ''
    ebrow = eyebrow(eb) if eb else ''
    backrow = back_link() if back else ''
    footrow = footer or ''
    panelH = panel_head or "Your health, in one place."
    panelS = panel_sub or "Find verified care, book before you leave home, and carry your history everywhere."
    return (f'<Frame name="{name}" w={{1440}} minH={{900}} flex="row" bg="var:bg/base">'
      f'<Frame w={{548}} h="fill" image="assets/img/{img}" overflow="hidden" flex="col" justify="between" p={{48}}>'
        f'<Image image="assets/logo/logo-white.png" w={{128}} h={{95}} />'
        f'<Frame flex="col" gap={{16}} w="fill">'
          f'{eyebrow(PLABEL[persona], color="var:text/on-dark-muted")}'
          f'{T(40,"bold","var:text/on-dark",panelH,w="fill")}'
          f'{T(17,"regular","var:text/on-dark-muted",panelS,w="fill")}'
        f'</Frame>'
        f'<Frame flex="row" gap={{10}} items="center" px={{16}} py={{12}} rounded={{999}} bg="var:bg/band-2">'
          f'{icon("shield-check",18,IC_TEAL)}{T(13,"medium","var:text/on-dark","NDPR-aligned · your data is encrypted")}</Frame>'
      f'</Frame>'
      f'<Frame grow={{1}} h="fill" flex="col" justify="center" items="center" px={{48}} py={{48}}>'
        f'<Frame w={{440}} flex="col" gap={{22}}>'
          f'<Frame w="fill" flex="row" justify="between" items="center">{backrow}{steprow}</Frame>'
          f'<Frame flex="col" gap={{10}}>{ebrow}{T(34,"bold","var:text/strong",head)}{T(16,"regular","var:text/muted",sub,w="fill")}</Frame>'
          f'{body}'
          f'<Frame w="fill" flex="col" gap={{12}}>{primary}{sec}</Frame>'
          f'{footrow}'
        f'</Frame>'
      f'</Frame>'
    f'</Frame>')

def mobile(name, persona, head, sub, body, primary, secondaries=(), footer=None, eb=None, back=False, step=None, hero=False, header_right=None):
    sec="".join(secondaries)
    steprow=f'{stepper(step[0],step[1])}' if step else '<Frame />'
    left = back_link() if back else f'<Image image="assets/logo/appicon.png" w={{34}} h={{34}} rounded={{8}} />'
    right = header_right or '<Frame w={34} />'
    herorow = (f'<Frame w="fill" h={{150}} image="assets/img/{BAND[persona]}" overflow="hidden" />') if hero else ''
    ebrow=eyebrow(eb) if eb else ''
    footrow=footer or ''
    return (f'<Frame name="{name}" w={{390}} minH={{844}} flex="col" bg="var:bg/base">'
      f'<Frame w="fill" flex="row" justify="between" items="center" px={{20}} pt={{22}} pb={{10}}>{left}{steprow}{right}</Frame>'
      f'{herorow}'
      f'<Frame grow={{1}} w="fill" flex="col" gap={{18}} px={{24}} pt={{16}} pb={{28}}>'
        f'<Frame flex="col" gap={{8}}>{ebrow}{T(26,"bold","var:text/strong",head)}{T(15,"regular","var:text/muted",sub,w="fill")}</Frame>'
        f'{body}'
        f'<Frame grow={{1}} />'
        f'<Frame w="fill" flex="col" gap={{12}}>{primary}{sec}{footrow}</Frame>'
      f'</Frame>'
    f'</Frame>')

frames=[]  # (page, filename, jsx)
NAMES={}   # fid -> (desktop_name, mobile_name)
PAGEOF={}  # fid -> persona page key
ORDER={}   # page key -> [fid,...] in flow order
def add(page, fid, desktop_jsx, mobile_jsx):
    frames.append((page, f"{fid}-d.jsx", desktop_jsx))
    frames.append((page, f"{fid}-m.jsx", mobile_jsx))
    dn=re.search(r'name="([^"]+)"', desktop_jsx).group(1)
    mn=re.search(r'name="([^"]+)"', mobile_jsx).group(1)
    NAMES[fid]=(dn,mn); PAGEOF[fid]=page
    ORDER.setdefault(page,[]).append(fid)

# ============================================================ ENTRY
# E1 Splash / get started
e1_body = ('<Frame w="fill" flex="col" gap={14} items="center" py={8}>'
           '<Image image="assets/logo/logo-gradient.png" w={200} h={148} />'
           + T(15,"regular","var:text/muted","Find verified care. Book before you leave home. Carry your medical history everywhere.",w="fill",align="center") + '</Frame>')
e1_primary = button("Create an account","teal",name="Create account · Entry")
add("Entry","E1-splash",
    desktop("Auth · Entry — E1 Get Started","entry","Welcome to Medra","One account for booking, records and care — wherever you are.",
            e1_body, e1_primary, [linkrow("Already have an account?","Log in","Login · Entry"),
            note("globe","Available in English, Hausa, Yoruba, Igbo & Pidgin.","info")],
            panel_head="Healthcare that follows you.", panel_sub="Verified doctors, real availability, and a medical history that travels with you."),
    mobile("Auth · Entry — E1 Get Started · Mobile","entry","Welcome to Medra","One account for booking, records and care.",
           e1_body, e1_primary, [linkrow("Already have an account?","Log in","Login · Entry")], hero=True))

# E2 Role selection
e2_body=('<Frame w="fill" flex="col" gap={12}>'
         + choice_card("user","I'm a patient","Book doctors and keep my records","Role Patient")
         + choice_card("stethoscope","I'm a doctor","See patients and write consultation notes","Role Doctor")
         + choice_card("building-2","I represent an institution","Register a clinic or hospital","Role Institution")
         + '</Frame>')
add("Entry","E2-role",
    desktop("Auth · Entry — E2 Role Selection","entry","How will you use Medra?","Choose the option that fits you. You can only pick one — it sets up the right experience.",
            e2_body, button("Continue","primary",trailing="arrow-right",name="Continue · Role"),
            [linkrow("Not sure?","See how Medra works","Help · Role")], back=True,
            panel_head="Built for everyone in care.", panel_sub="Patients, doctors and institutions — each with a tailored, secure experience."),
    mobile("Auth · Entry — E2 Role Selection · Mobile","entry","How will you use Medra?","Choose the option that fits you.",
           e2_body, button("Continue","primary",trailing="arrow-right",name="Continue · Role"), back=True))

# ============================================================ PATIENT
P="patient"; PN="Patient"
add(PN,"P1-create",
    desktop("Auth · Patient — P1 Create Account",P,"Create your account","Enter your phone number — we'll text you a 6-digit code to confirm it.",
            field("Phone number","phone","801 234 5678",prefix="🇳🇬 +234",helper="Standard SMS rates may apply.") + '<Frame h={4}/>' + checkbox("I agree to Medra's Terms of Service and Privacy Policy, and consent to my health data being processed under the NDPR."),
            button("Send my code","teal",trailing="arrow-right",name="Send code · P1"),
            [linkrow("Already have an account?","Log in","Login · P")], eb="Step 1 of 3", step=(0,3), back=True,
            panel_head="Your health, in one place.", panel_sub="No paper to carry, no history to lose."),
    mobile("Auth · Patient — P1 Create Account · Mobile",P,"Create your account","We'll text a 6-digit code to confirm your number.",
           field("Phone number","phone","801 234 5678",prefix="+234") + '<Frame h={2}/>' + checkbox("I agree to the Terms &amp; Privacy Policy and NDPR data processing."),
           button("Send my code","teal",trailing="arrow-right",name="Send code · P1"),
           [linkrow("Already have an account?","Log in","Login · P")], step=(0,3), back=True))

add(PN,"P2-otp",
    desktop("Auth · Patient — P2 Verify Code",P,"Enter the 6-digit code","We sent it to +234 801 234 5678.",
            otp(6,"3907") + '<Frame w="fill" flex="row" gap={6} justify="center" items="center">' + T(13,"regular","var:text/muted","Didn't get it?") + '<Frame name="Btn Resend · P2" flex="row"><Text font="Inter" size={13} weight="semibold" color="var:text/faint">Resend in 0:24</Text></Frame></Frame>',
            button("Verify","teal",name="Verify · P2"),
            [linkrow("Wrong number?","Change it","Change number · P2"), linkrow("Code not arriving?","Get help","Help code · P2")],
            eb="Step 2 of 3", step=(1,3), back=True,
            panel_head="Almost there.", panel_sub="Confirming your number keeps your records secure and yours alone."),
    mobile("Auth · Patient — P2 Verify Code · Mobile",P,"Enter the 6-digit code","Sent to +234 801 234 5678.",
           otp(6,"3907") + linkrow("Didn't get it?","Resend in 0:24","Resend · P2"),
           button("Verify","teal",name="Verify · P2"),
           [linkrow("Wrong number?","Change it","Change number · P2")], step=(1,3), back=True))

p3_body=(select_field("Full name","user","Amara Okeke",placeholder=False)
        + select_field("Date of birth","calendar","12 March 1994",placeholder=False)
        + select_field("Gender","users","Select — Female · Male · Non-binary · Prefer not to say")
        + select_field("Preferred language","globe","English"))
add(PN,"P3-onboard",
    desktop("Auth · Patient — P3 Onboarding",P,"Tell us about you","This helps doctors care for you safely. You can change any of it later.",
            p3_body + note("accessibility","Need larger text or screen-reader support? Turn on Accessibility mode in Settings anytime.","info"),
            button("Continue","teal",trailing="arrow-right",name="Continue · P3"),
            [linkrow("","Skip for now","Skip · P3")], eb="Step 3 of 3", step=(2,3), back=True,
            panel_head="Care that knows you.", panel_sub="Your details stay private and are shared only with doctors you book."),
    mobile("Auth · Patient — P3 Onboarding · Mobile",P,"Tell us about you","You can change any of this later.",
           p3_body, button("Continue","teal",trailing="arrow-right",name="Continue · P3"),
           [linkrow("","Skip for now","Skip · P3")], step=(2,3), back=True))

add(PN,"P4-login",
    desktop("Auth · Patient — P4 Log In",P,"Welcome back","Enter your phone number and we'll text you a code to log in.",
            field("Phone number","phone","801 234 5678",prefix="🇳🇬 +234"),
            button("Send my code","teal",trailing="arrow-right",name="Send code · P4"),
            [linkrow("New to Medra?","Create an account","Create · P4"), linkrow("Can't access your number?","Get help","Help · P4")], back=True,
            panel_head="Good to see you again.", panel_sub="Your appointments and records are right where you left them."),
    mobile("Auth · Patient — P4 Log In · Mobile",P,"Welcome back","We'll text you a code to log in.",
           field("Phone number","phone","801 234 5678",prefix="+234"),
           button("Send my code","teal",trailing="arrow-right",name="Send code · P4"),
           [linkrow("New to Medra?","Create an account","Create · P4")], back=True))

p5_body=('<Frame w="fill" flex="col" gap={12}>'
         + choice_card("refresh-cw","Resend the code","Text the 6-digit code again","Resend · P5")
         + choice_card("phone","Call me instead","Get the code by an automated call","Call · P5")
         + choice_card("pencil","Change my number","I entered the wrong number","Change · P5")
         + choice_card("message-square-text","Message support","Chat with the Medra team","Support · P5") + '</Frame>')
add(PN,"P5-help",
    desktop("Auth · Patient — P5 Can't Get Code",P,"Trouble getting your code?","Pick an option below — we'll get you in.",
            p5_body, button("Back to verification","secondary",ic="arrow-left",name="Back to OTP · P5"),
            [], back=True, panel_head="We've got you.", panel_sub="There's always a way in — no one gets stuck."),
    mobile("Auth · Patient — P5 Can't Get Code · Mobile",P,"Trouble getting your code?","Pick an option — we'll get you in.",
           p5_body, button("Back to verification","secondary",ic="arrow-left",name="Back to OTP · P5"), back=True))

p6_body=('<Frame w="fill" flex="col" gap={16} items="center" py={8}>'
         '<Frame w={92} h={92} rounded={999} bg="var:state/success-bg" flex="col" justify="center" items="center">'+icon("circle-check",44,IC_OK)+'</Frame>'
         + T(15,"regular","var:text/muted","Your account is ready. Taking you to your home to find care and view appointments.",w="fill",align="center")
         + note("info","Redirecting you to your patient home…","info") + '</Frame>')
add(PN,"P6-success",
    desktop("Auth · Patient — P6 Success",P,"You're all set, Amara","Welcome to Medra.",
            p6_body, button("Go to my home","teal",trailing="arrow-right",name="Go home · P6"),
            [linkrow("","Explore doctors near me","Explore · P6")],
            panel_head="Welcome to Medra.", panel_sub="Care that follows you — everywhere."),
    mobile("Auth · Patient — P6 Success · Mobile",P,"You're all set, Amara","Welcome to Medra.",
           p6_body, button("Go to my home","teal",trailing="arrow-right",name="Go home · P6"),
           [linkrow("","Explore doctors near me","Explore · P6")]))

# ============================================================ DOCTOR
D="doctor"; DN="Doctor"
d1_body=(field("Phone number","phone","803 555 0110",prefix="🇳🇬 +234")
        + field("MDCN number","id-card","MDCN/45201",placeholder=True,helper="Your Medical & Dental Council of Nigeria licence number.")
        + select_field("Specialisation","stethoscope","Select your specialty"))
add(DN,"D1-create",
    desktop("Auth · Doctor — D1 Create Account",D,"Join Medra as a doctor","We verify every doctor's MDCN licence before your profile goes live.",
            d1_body, button("Continue","primary",trailing="arrow-right",name="Continue · D1"),
            [linkrow("Already registered?","Log in","Login · D")], eb="Step 1 of 4", step=(0,4), back=True,
            panel_head="Your practice, amplified.", panel_sub="Reach patients who need you, with a schedule that respects your time."),
    mobile("Auth · Doctor — D1 Create Account · Mobile",D,"Join as a doctor","We verify your MDCN licence before you go live.",
           d1_body, button("Continue","primary",trailing="arrow-right",name="Continue · D1"),
           [linkrow("Already registered?","Log in","Login · D")], step=(0,4), back=True))

add(DN,"D2-otp",
    desktop("Auth · Doctor — D2 Verify Code",D,"Verify your phone","Enter the 6-digit code sent to +234 803 555 0110.",
            otp(6,"58") + linkrow("Didn't get it?","Resend in 0:20","Resend · D2"),
            button("Verify","primary",name="Verify · D2"),
            [linkrow("Wrong number?","Change it","Change number · D2")], eb="Step 2 of 4", step=(1,4), back=True,
            panel_head="Security first.", panel_sub="Two steps keep your patients' records protected."),
    mobile("Auth · Doctor — D2 Verify Code · Mobile",D,"Verify your phone","Code sent to +234 803 555 0110.",
           otp(6,"58") + linkrow("Didn't get it?","Resend in 0:20","Resend · D2"),
           button("Verify","primary",name="Verify · D2"), [], eb="Step 2 of 4", step=(1,4), back=True))

d3_body=(field("Create password","lock","••••••••",placeholder=False,trailing=("eye","Show password · D3"),helper="At least 8 characters, with a number and a symbol.")
        + '<Frame w="fill" flex="row" gap={6}><Rect grow={1} h={5} rounded={999} bg="var:state/success" /><Rect grow={1} h={5} rounded={999} bg="var:state/success" /><Rect grow={1} h={5} rounded={999} bg="var:state/success" /><Rect grow={1} h={5} rounded={999} bg="var:neutral/200" /></Frame>'
        + T(12,"medium","var:state/success","Strong password")
        + field("Confirm password","lock","••••••••",placeholder=False,trailing=("eye","Show confirm · D3")))
add(DN,"D3-password",
    desktop("Auth · Doctor — D3 Set Password",D,"Secure your account","You'll use this with your phone each time you log in.",
            d3_body, button("Continue","primary",trailing="arrow-right",name="Continue · D3"),
            [], eb="Step 3 of 4", step=(2,4), back=True,
            panel_head="Only you get in.", panel_sub="A password plus your phone — proper protection for clinical data."),
    mobile("Auth · Doctor — D3 Set Password · Mobile",D,"Secure your account","Used with your phone each login.",
           d3_body, button("Continue","primary",trailing="arrow-right",name="Continue · D3"), [], step=(2,4), back=True))

d4_body=('<Frame w="fill" flex="col" gap={16} items="center" py={8}>'
         '<Frame w={92} h={92} rounded={999} bg="var:state/warning-bg" flex="col" justify="center" items="center">'+icon("badge-check",44,IC_WARN)+'</Frame>'
         + T(15,"regular","var:text/muted","Thanks, Dr. Okafor. Our team is verifying your MDCN licence — this usually takes 24–48 hours.",w="fill",align="center")
         + note("clock","We'll text and email you the moment you're approved. Your profile stays hidden until then.","warn") + '</Frame>')
add(DN,"D4-pending",
    desktop("Auth · Doctor — D4 Verification Pending",D,"We're verifying your licence","You're almost in. Here's what happens next.",
            d4_body, button("Explore Medra while you wait","primary",trailing="arrow-right",name="Explore · D4"),
            [linkrow("Entered the wrong MDCN?","Update it","Update MDCN · D4"), linkrow("Questions?","Contact support","Support · D4")], eb="Step 4 of 4", step=(3,4),
            panel_head="Trust, verified.", panel_sub="Every doctor on Medra is a real, licensed professional — patients count on it."),
    mobile("Auth · Doctor — D4 Verification Pending · Mobile",D,"Verifying your licence","Here's what happens next.",
           d4_body, button("Explore while you wait","primary",trailing="arrow-right",name="Explore · D4"),
           [linkrow("Questions?","Contact support","Support · D4")], step=(3,4)))

d5_body=('<Frame w="fill" flex="row" gap={16} items="center"><Frame w={72} h={72} rounded={999} bg="var:bg/muted" flex="col" justify="center" items="center">'+icon("camera",26,IC_ACCENT)+'</Frame>'
         + '<Frame name="Btn Add photo · D5" flex="row" gap={8} items="center" px={16} py={10} rounded={999} bg="var:bg/subtle" stroke="var:border/default" strokeWidth={1}>'+icon("upload",16,IC_NAVY)+T(13,"semibold","var:text/default","Add profile photo")+'</Frame></Frame>'
         + select_field("Short bio","file-text","Tell patients about your experience…")
         + field("Consultation fee","credit-card","15,000",prefix="₦",helper="You can change this anytime."))
add(DN,"D5-profile",
    desktop("Auth · Doctor — D5 Profile Setup",D,"Set up your public profile","This is what patients see before they book you.",
            d5_body, button("Finish &amp; go to dashboard","primary",trailing="arrow-right",name="Finish · D5"),
            [linkrow("","Do this later","Later · D5")], back=True,
            panel_head="Make a strong first impression.", panel_sub="A clear photo and bio help patients choose you with confidence."),
    mobile("Auth · Doctor — D5 Profile Setup · Mobile",D,"Set up your profile","What patients see before booking.",
           d5_body, button("Finish","primary",trailing="arrow-right",name="Finish · D5"),
           [linkrow("","Do this later","Later · D5")], back=True))

add(DN,"D6-login",
    desktop("Auth · Doctor — D6 Log In",D,"Welcome back, doctor","Log in to see today's schedule and your patients.",
            field("Phone or email","user","dr.okafor@clinic.ng",placeholder=False) + field("Password","lock","••••••••",placeholder=False,trailing=("eye","Show · D6")) + '<Frame w="fill" flex="row" justify="end"><Frame name="Btn Forgot · D6" flex="row"><Text font="Inter" size={13} weight="semibold" color="var:text/accent">Forgot password?</Text></Frame></Frame>',
            button("Log in","primary",trailing="arrow-right",name="Login submit · D6"),
            [linkrow("New to Medra?","Register as a doctor","Register · D6")], back=True,
            panel_head="Your day, ready.", panel_sub="Today's queue, patient histories and notes — one login away."),
    mobile("Auth · Doctor — D6 Log In · Mobile",D,"Welcome back, doctor","See today's schedule and patients.",
           field("Phone or email","user","dr.okafor@clinic.ng",placeholder=False) + field("Password","lock","••••••••",placeholder=False,trailing=("eye","Show · D6")),
           button("Log in","primary",trailing="arrow-right",name="Login submit · D6"),
           [linkrow("Forgot password?","Reset it","Forgot · D6"), linkrow("New?","Register as a doctor","Register · D6")], back=True))

add(DN,"D7-2fa",
    desktop("Auth · Doctor — D7 Two-Factor",D,"Confirm it's you","We texted a 6-digit code to +234 803 555 0110 to protect patient data.",
            otp(6,"41") + linkrow("Didn't get it?","Resend in 0:22","Resend · D7"),
            button("Log in","primary",name="2FA verify · D7"),
            [linkrow("Lost access to your phone?","Get help","Help · D7")], back=True,
            panel_head="Two steps, total trust.", panel_sub="Extra protection every time you open a patient's record."),
    mobile("Auth · Doctor — D7 Two-Factor · Mobile",D,"Confirm it's you","Code sent to +234 803 555 0110.",
           otp(6,"41") + linkrow("Didn't get it?","Resend in 0:22","Resend · D7"),
           button("Log in","primary",name="2FA verify · D7"), [linkrow("Lost your phone?","Get help","Help · D7")], back=True))

d8_body=(field("Phone or email","user","dr.okafor@clinic.ng",placeholder=False,helper="We'll send a 6-digit reset code here."))
add(DN,"D8-forgot",
    desktop("Auth · Doctor — D8 Forgot Password",D,"Reset your password","Enter your phone or email and we'll send a code to reset it.",
            d8_body, button("Send reset code","primary",trailing="arrow-right",name="Send reset · D8"),
            [linkrow("Remembered it?","Back to log in","Back login · D8")], back=True,
            panel_head="Locked out? No problem.", panel_sub="A quick code and you're back to your patients."),
    mobile("Auth · Doctor — D8 Forgot Password · Mobile",D,"Reset your password","We'll send a code to reset it.",
           d8_body, button("Send reset code","primary",trailing="arrow-right",name="Send reset · D8"),
           [linkrow("Remembered it?","Back to log in","Back login · D8")], back=True))

d9_body=(field("New password","lock","••••••••",placeholder=False,trailing=("eye","Show · D9"),helper="At least 8 characters, with a number and a symbol.")
        + field("Confirm new password","lock","••••••••",placeholder=False,trailing=("eye","Show confirm · D9")))
add(DN,"D9-reset",
    desktop("Auth · Doctor — D9 New Password",D,"Choose a new password","Make it strong — it protects your patients' records.",
            d9_body, button("Save &amp; log in","primary",trailing="arrow-right",name="Save password · D9"),
            [], back=True, panel_head="Back in safe hands.", panel_sub="New password set — let's get you to work."),
    mobile("Auth · Doctor — D9 New Password · Mobile",D,"Choose a new password","It protects your patients' records.",
           d9_body, button("Save &amp; log in","primary",trailing="arrow-right",name="Save password · D9"), [], back=True))

d10_body=('<Frame w="fill" flex="col" gap={16} items="center" py={8}>'
          '<Frame w={92} h={92} rounded={999} bg="var:state/success-bg" flex="col" justify="center" items="center">'+icon("circle-check",44,IC_OK)+'</Frame>'
          + T(15,"regular","var:text/muted","You're verified and logged in. Taking you to your dashboard and today's schedule.",w="fill",align="center")
          + note("info","Redirecting you to your doctor dashboard…","info") + '</Frame>')
add(DN,"D10-success",
    desktop("Auth · Doctor — D10 Success",D,"Welcome aboard, Dr. Okafor","Your profile is live and patients can book you.",
            d10_body, button("Go to dashboard","primary",trailing="arrow-right",name="Go dashboard · D10"), [],
            panel_head="You're live on Medra.", panel_sub="Verified, visible and ready to see patients."),
    mobile("Auth · Doctor — D10 Success · Mobile",D,"Welcome aboard","Your profile is live.",
           d10_body, button("Go to dashboard","primary",trailing="arrow-right",name="Go dashboard · D10"), []))

# ============================================================ INSTITUTION
IN="institution"; INN="Institution"
i1_body=(field("Institution name","hospital","Garki Medical Centre",placeholder=False)
        + select_field("Type","building-2","Private hospital")
        + field("Admin full name","user","Yusuf Bello",placeholder=False)
        + field("Work email","mail","admin@garkimedical.ng",placeholder=False)
        + field("Admin phone","phone","802 111 2233",prefix="+234"))
add(INN,"I1-register",
    desktop("Auth · Institution — I1 Register",IN,"Register your institution","Set up your clinic or hospital. You'll be the facility admin.",
            i1_body, button("Continue","primary",trailing="arrow-right",name="Continue · I1"),
            [linkrow("Institution already on Medra?","Admin log in","Admin login · I")], eb="Step 1 of 5", step=(0,5), back=True,
            panel_head="Run your facility, digitally.", panel_sub="Bookings, staff, records and billing — one system for the whole institution."),
    mobile("Auth · Institution — I1 Register · Mobile",IN,"Register your institution","You'll be the facility admin.",
           i1_body, button("Continue","primary",trailing="arrow-right",name="Continue · I1"),
           [linkrow("Already on Medra?","Admin log in","Admin login · I")], step=(0,5), back=True))

i2_body=(upload_box("licence",done=True) + upload_box("cac",done=False)
        + note("shield-check","Documents are encrypted and used only to verify your institution.","info"))
add(INN,"I2-documents",
    desktop("Auth · Institution — I2 Verify Documents",IN,"Upload your documents","We verify every institution before it goes live. Add your practice licence and CAC certificate.",
            i2_body, button("Continue","primary",trailing="arrow-right",name="Continue · I2"),
            [linkrow("Don't have them handy?","Save &amp; finish later","Save later · I2")], eb="Step 2 of 5", step=(1,5), back=True,
            panel_head="Verified institutions only.", panel_sub="Patients trust Medra because every provider is checked."),
    mobile("Auth · Institution — I2 Verify Documents · Mobile",IN,"Upload your documents","Practice licence + CAC certificate.",
           i2_body, button("Continue","primary",trailing="arrow-right",name="Continue · I2"),
           [linkrow("","Save &amp; finish later","Save later · I2")], step=(1,5), back=True))

i3_body=('<Frame w="fill" flex="col" gap={12}>'
         + plan_card("Single practice","₦___","1 doctor · core booking &amp; records",selected=False)
         + plan_card("Multi-doctor","₦___","Up to 15 doctors · staff roles &amp; allocation",selected=True)
         + plan_card("Multi-branch","Custom","Enterprise · branches billed as one",selected=False)
         + note("sparkles","Every plan starts with a 30-day free trial — no card required.","ok") + '</Frame>')
add(INN,"I3-plan",
    desktop("Auth · Institution — I3 Choose Plan",IN,"Pick a plan","Choose the size that fits today — you can upgrade anytime. Pricing is confirmed with our team.",
            i3_body, button("Start free trial","teal",trailing="arrow-right",name="Start trial · I3"),
            [linkrow("Not sure which fits?","Talk to sales","Sales · I3")], eb="Step 3 of 5", step=(2,5), back=True,
            panel_head="Priced to your size.", panel_sub="From a single practice to a multi-branch group — pay for what you need."),
    mobile("Auth · Institution — I3 Choose Plan · Mobile",IN,"Pick a plan","Upgrade anytime. 30-day free trial.",
           i3_body, button("Start free trial","teal",trailing="arrow-right",name="Start trial · I3"),
           [linkrow("Not sure?","Talk to sales","Sales · I3")], step=(2,5), back=True))

add(INN,"I4-otp",
    desktop("Auth · Institution — I4 Verify Admin",IN,"Verify the admin phone","Enter the 6-digit code sent to +234 802 111 2233.",
            otp(6,"77") + linkrow("Didn't get it?","Resend in 0:25","Resend · I4"),
            button("Verify","primary",name="Verify · I4"),
            [linkrow("Wrong number?","Change it","Change number · I4")], eb="Step 4 of 5", step=(3,5), back=True,
            panel_head="Secure the admin account.", panel_sub="The facility admin controls staff and billing — so we protect it well."),
    mobile("Auth · Institution — I4 Verify Admin · Mobile",IN,"Verify the admin phone","Code sent to +234 802 111 2233.",
           otp(6,"77") + linkrow("Didn't get it?","Resend in 0:25","Resend · I4"),
           button("Verify","primary",name="Verify · I4"), [], eb="Step 4 of 5", step=(3,5), back=True))

i5_body=(field("Create admin password","lock","••••••••",placeholder=False,trailing=("eye","Show · I5"),helper="At least 8 characters, with a number and a symbol.")
        + field("Confirm password","lock","••••••••",placeholder=False,trailing=("eye","Show confirm · I5")))
add(INN,"I5-password",
    desktop("Auth · Institution — I5 Set Password",IN,"Secure the admin account","You'll use this with the admin phone to log in.",
            i5_body, button("Create account","primary",trailing="arrow-right",name="Create · I5"),
            [], eb="Step 5 of 5", step=(4,5), back=True,
            panel_head="One key-holder.", panel_sub="Strong protection for the account that runs your facility."),
    mobile("Auth · Institution — I5 Set Password · Mobile",IN,"Secure the admin account","Used with the admin phone to log in.",
           i5_body, button("Create account","primary",trailing="arrow-right",name="Create · I5"), [], step=(4,5), back=True))

i6_body=('<Frame w="fill" flex="col" gap={16} items="center" py={8}>'
         '<Frame w={92} h={92} rounded={999} bg="var:state/warning-bg" flex="col" justify="center" items="center">'+icon("badge-check",44,IC_WARN)+'</Frame>'
         + T(15,"regular","var:text/muted","Thanks, Mr. Bello. We're reviewing Garki Medical Centre's documents — usually within 1–2 business days.",w="fill",align="center")
         + note("clock","We'll email you the moment you're approved. Meanwhile, you can start inviting staff.","warn") + '</Frame>')
add(INN,"I6-pending",
    desktop("Auth · Institution — I6 Application Submitted",IN,"Application submitted","Your 30-day trial has started. Here's what happens next.",
            i6_body, button("Go to admin portal","primary",trailing="arrow-right",name="Go portal · I6"),
            [linkrow("Need to add a document?","Manage application","Manage · I6")],
            panel_head="Welcome to Medra for Business.", panel_sub="Your facility's new operating system starts now."),
    mobile("Auth · Institution — I6 Application Submitted · Mobile",IN,"Application submitted","Your 30-day trial has started.",
           i6_body, button("Go to admin portal","primary",trailing="arrow-right",name="Go portal · I6"),
           [linkrow("","Manage application","Manage · I6")]))

add(INN,"I7-admin-login",
    desktop("Auth · Institution — I7 Facility Admin Log In",IN,"Facility admin log in","Sign in to manage bookings, staff and billing.",
            field("Work email","mail","admin@garkimedical.ng",placeholder=False) + field("Password","lock","••••••••",placeholder=False,trailing=("eye","Show · I7")) + '<Frame w="fill" flex="row" justify="end"><Frame name="Btn Forgot · I7" flex="row"><Text font="Inter" size={13} weight="semibold" color="var:text/accent">Forgot password?</Text></Frame></Frame>',
            button("Log in","primary",trailing="arrow-right",name="Login submit · I7"),
            [linkrow("Registering a new institution?","Start here","Register · I7")], back=True,
            panel_head="Your facility, in control.", panel_sub="Everything that runs your clinic, one secure login away."),
    mobile("Auth · Institution — I7 Facility Admin Log In · Mobile",IN,"Facility admin log in","Manage bookings, staff and billing.",
           field("Work email","mail","admin@garkimedical.ng",placeholder=False) + field("Password","lock","••••••••",placeholder=False,trailing=("eye","Show · I7")),
           button("Log in","primary",trailing="arrow-right",name="Login submit · I7"),
           [linkrow("Forgot password?","Reset it","Forgot · I7"), linkrow("New institution?","Start here","Register · I7")], back=True))

i8_body=(field("Work email","mail","admin@garkimedical.ng",placeholder=False,helper="We'll send a 6-digit reset code here."))
add(INN,"I8-forgot",
    desktop("Auth · Institution — I8 Forgot Password",IN,"Reset admin password","Enter the admin email and we'll send a reset code.",
            i8_body, button("Send reset code","primary",trailing="arrow-right",name="Send reset · I8"),
            [linkrow("Remembered it?","Back to log in","Back login · I8")], back=True,
            panel_head="Locked out? We'll fix that.", panel_sub="A quick code and your facility is back online."),
    mobile("Auth · Institution — I8 Forgot Password · Mobile",IN,"Reset admin password","We'll send a reset code.",
           i8_body, button("Send reset code","primary",trailing="arrow-right",name="Send reset · I8"),
           [linkrow("Remembered it?","Back to log in","Back login · I8")], back=True))

add(INN,"I9-reset",
    desktop("Auth · Institution — I9 New Password",IN,"Choose a new password","Make it strong — it controls your whole facility.",
            i5_body.replace("Create admin password","New password").replace("Show · I5","Show · I9").replace("Show confirm · I5","Show confirm · I9"),
            button("Save &amp; log in","primary",trailing="arrow-right",name="Save password · I9"), [], back=True,
            panel_head="Back in control.", panel_sub="New password set — your facility awaits."),
    mobile("Auth · Institution — I9 New Password · Mobile",IN,"Choose a new password","It controls your whole facility.",
           i5_body.replace("Create admin password","New password").replace("Show · I5","Show · I9").replace("Show confirm · I5","Show confirm · I9"),
           button("Save &amp; log in","primary",trailing="arrow-right",name="Save password · I9"), [], back=True))

i10_body=('<Frame w="fill" flex="col" gap={16} items="center" py={8}>'
          '<Frame w={92} h={92} rounded={999} bg="var:state/success-bg" flex="col" justify="center" items="center">'+icon("circle-check",44,IC_OK)+'</Frame>'
          + T(15,"regular","var:text/muted","Garki Medical Centre is approved and live. Taking you to your admin portal.",w="fill",align="center")
          + note("info","Redirecting you to your admin portal…","info") + '</Frame>')
add(INN,"I10-success",
    desktop("Auth · Institution — I10 Success",IN,"You're live, Mr. Bello","Garki Medical Centre is verified and on Medra.",
            i10_body, button("Go to admin portal","primary",trailing="arrow-right",name="Go portal · I10"), [],
            panel_head="Your facility is on Medra.", panel_sub="Start adding doctors and taking bookings today."),
    mobile("Auth · Institution — I10 Success · Mobile",IN,"You're live, Mr. Bello","Your facility is verified.",
           i10_body, button("Go to admin portal","primary",trailing="arrow-right",name="Go portal · I10"), []))

# ---------------- write ----------------
def sanitize(s):
    return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9A-Fa-f]+;)', '&amp;', s)
manifest={}
for page, fn, jsx in frames:
    open(os.path.join(OUT, fn), "w").write(sanitize(jsx))
    manifest.setdefault(page, []).append(fn)
import json
open(os.path.join(OUT,"pages.json"),"w").write(json.dumps(manifest, indent=2))

# ---------------- prototype flow (no dead ends) ----------------
PAGE_FIGMA={"Entry":"Medra Auth — Entry","Patient":"Medra Auth — Patient",
            "Doctor":"Medra Auth — Doctor","Institution":"Medra Auth — Institution"}
TRN=[
 ("E1-splash","Btn Create account · Entry","E2-role"),("E1-splash","Btn Login · Entry","P4-login"),
 ("E2-role","Btn Role Patient","P1-create"),("E2-role","Btn Role Doctor","D1-create"),
 ("E2-role","Btn Role Institution","I1-register"),("E2-role","Btn Continue · Role","P1-create"),
 ("E2-role","Btn Back","E1-splash"),("E2-role","Btn Help · Role","E1-splash"),
 # patient
 ("P1-create","Btn Send code · P1","P2-otp"),("P1-create","Btn Login · P","P4-login"),("P1-create","Btn Back","E2-role"),
 ("P2-otp","Btn Verify · P2","P3-onboard"),("P2-otp","Btn Change number · P2","P1-create"),
 ("P2-otp","Btn Help code · P2","P5-help"),("P2-otp","Btn Resend · P2","P2-otp"),("P2-otp","Btn Back","P1-create"),
 ("P3-onboard","Btn Continue · P3","P6-success"),("P3-onboard","Btn Skip · P3","P6-success"),("P3-onboard","Btn Back","P2-otp"),
 ("P4-login","Btn Send code · P4","P6-success"),("P4-login","Btn Create · P4","P1-create"),
 ("P4-login","Btn Help · P4","P5-help"),("P4-login","Btn Back","E1-splash"),
 ("P5-help","Btn Back to OTP · P5","P2-otp"),("P5-help","Btn Resend · P5","P2-otp"),("P5-help","Btn Call · P5","P2-otp"),
 ("P5-help","Btn Change · P5","P1-create"),("P5-help","Btn Support · P5","P5-help"),("P5-help","Btn Back","P2-otp"),
 ("P6-success","Btn Go home · P6","E1-splash"),("P6-success","Btn Explore · P6","E1-splash"),
 # doctor
 ("D1-create","Btn Continue · D1","D2-otp"),("D1-create","Btn Login · D","D6-login"),("D1-create","Btn Back","E2-role"),
 ("D2-otp","Btn Verify · D2","D3-password"),("D2-otp","Btn Change number · D2","D1-create"),
 ("D2-otp","Btn Resend · D2","D2-otp"),("D2-otp","Btn Back","D1-create"),
 ("D3-password","Btn Continue · D3","D4-pending"),("D3-password","Btn Back","D2-otp"),
 ("D4-pending","Btn Explore · D4","D5-profile"),("D4-pending","Btn Update MDCN · D4","D1-create"),("D4-pending","Btn Support · D4","D4-pending"),
 ("D5-profile","Btn Finish · D5","D10-success"),("D5-profile","Btn Later · D5","D10-success"),("D5-profile","Btn Back","D4-pending"),
 ("D6-login","Btn Login submit · D6","D7-2fa"),("D6-login","Btn Forgot · D6","D8-forgot"),
 ("D6-login","Btn Register · D6","D1-create"),("D6-login","Btn Back","E1-splash"),
 ("D7-2fa","Btn 2FA verify · D7","D10-success"),("D7-2fa","Btn Resend · D7","D7-2fa"),
 ("D7-2fa","Btn Help · D7","D8-forgot"),("D7-2fa","Btn Back","D6-login"),
 ("D8-forgot","Btn Send reset · D8","D9-reset"),("D8-forgot","Btn Back login · D8","D6-login"),("D8-forgot","Btn Back","D6-login"),
 ("D9-reset","Btn Save password · D9","D6-login"),("D9-reset","Btn Back","D8-forgot"),
 ("D10-success","Btn Go dashboard · D10","E1-splash"),
 # institution
 ("I1-register","Btn Continue · I1","I2-documents"),("I1-register","Btn Admin login · I","I7-admin-login"),("I1-register","Btn Back","E2-role"),
 ("I2-documents","Btn Continue · I2","I3-plan"),("I2-documents","Btn Save later · I2","I3-plan"),
 ("I2-documents","Btn Upload cac","I2-documents"),("I2-documents","Btn Back","I1-register"),
 ("I3-plan","Btn Start trial · I3","I4-otp"),("I3-plan","Btn Sales · I3","I3-plan"),("I3-plan","Btn Back","I2-documents"),
 ("I4-otp","Btn Verify · I4","I5-password"),("I4-otp","Btn Change number · I4","I1-register"),
 ("I4-otp","Btn Resend · I4","I4-otp"),("I4-otp","Btn Back","I3-plan"),
 ("I5-password","Btn Create · I5","I6-pending"),("I5-password","Btn Back","I4-otp"),
 ("I6-pending","Btn Go portal · I6","I10-success"),("I6-pending","Btn Manage · I6","I2-documents"),
 ("I7-admin-login","Btn Login submit · I7","I10-success"),("I7-admin-login","Btn Forgot · I7","I8-forgot"),
 ("I7-admin-login","Btn Register · I7","I1-register"),("I7-admin-login","Btn Back","E1-splash"),
 ("I8-forgot","Btn Send reset · I8","I9-reset"),("I8-forgot","Btn Back login · I8","I7-admin-login"),("I8-forgot","Btn Back","I7-admin-login"),
 ("I9-reset","Btn Save password · I9","I7-admin-login"),("I9-reset","Btn Back","I8-forgot"),
 ("I10-success","Btn Go portal · I10","E1-splash"),
]
# resolve transitions for both platforms
resolved=[]
for a,hot,b in TRN:
    if a not in NAMES or b not in NAMES: continue
    resolved.append([NAMES[a][0], hot, NAMES[b][0]])  # desktop
    resolved.append([NAMES[a][1], hot, NAMES[b][1]])  # mobile
order_js={PAGE_FIGMA[p]:[[NAMES[f][0],NAMES[f][1]] for f in fids] for p,fids in ORDER.items()}
starts_js={PAGE_FIGMA[p]:NAMES[fids[0]][0] for p,fids in ORDER.items()}

linker=("(async () => {\n"
 "  if (figma.loadAllPagesAsync) await figma.loadAllPagesAsync();\n"
 "  const norm = s => (s||'').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();\n"
 "  const pages = figma.root.children.filter(n => n.type==='PAGE');\n"
 "  const byName = {}; for (const pg of pages) for (const f of pg.children) if (f.type==='FRAME') byName[norm(f.name)] = f;\n"
 "  const F = n => byName[norm(n)];\n"
 "  const findNamed = (root,t) => { let hit=null; const target=norm(t); const w=n=>{ if(hit)return; if(n.name&&norm(n.name)===target){hit=n;return;} if('children'in n)n.children.forEach(w); }; w(root); return hit; };\n"
 "  const transition = { type:'SMART_ANIMATE', easing:{type:'EASE_OUT'}, duration:0.25 };\n"
 f"  const TRN = {json.dumps(resolved)};\n"
 f"  const ORDER = {json.dumps(order_js)};\n"
 f"  const STARTS = {json.dumps(starts_js)};\n"
 "  const jobs=[], missing=[];\n"
 "  for (const [fromN,hot,toN] of TRN){ const fr=F(fromN), to=F(toN); if(!fr||!to) continue; const node=findNamed(fr,hot); if(!node){ missing.push(fromN+' → '+hot); continue; } jobs.push([node,to]); }\n"
 "  let linked=0; for (const [node,to] of jobs){ await node.setReactionsAsync([{ trigger:{type:'ON_CLICK'}, actions:[{ type:'NODE', destinationId:to.id, navigation:'NAVIGATE', transition }] }]); linked++; }\n"
 "  const GX=160, GY=140;\n"
 "  for (const pg of pages){ const ord=ORDER[pg.name]; if(!ord) continue; let x=0, rowH=0;\n"
 "    for (const [dn,mn] of ord){ const df=F(dn); if(df){ df.x=x; df.y=0; x+=df.width+GX; rowH=Math.max(rowH,df.height);} }\n"
 "    let mx=0; for (const [dn,mn] of ord){ const mf=F(mn); if(mf){ mf.x=mx; mf.y=rowH+GY; mx+=mf.width+GX; } } }\n"
 "  for (const pg of pages){ const s=STARTS[pg.name]; if(s&&F(s)) pg.flowStartingPoints=[{ nodeId:F(s).id, name:'Start' }]; }\n"
 "  return { linked, framesFound: Object.keys(byName).length, missing };\n"
 "})();\n")
open(os.path.join(OUT,"link-auth.js"),"w").write(linker)

# ---------------- per-page render script ----------------
ps=["# Medra Auth — render each persona onto its own Figma page (Figma Desktop open + connected).",
    "# Run from inside this folder. Installs client cache first (once per machine).",
    'New-Item -ItemType Directory -Force "$HOME\\.figma-ds-cli\\icon-cache" | Out-Null',
    'Copy-Item .\\assets\\icon-cache\\*.svg "$HOME\\.figma-ds-cli\\icon-cache\\" -Force',
    "figma-cli tokens import-design-md .\\DESIGN.md",""]
for p, fids in ORDER.items():
    pg=PAGE_FIGMA[p]
    ps.append(f'# ---- {pg} ----')
    ps.append(f'figma-cli eval "(async()=>{{const t=\'{pg}\';let p=figma.root.children.find(n=>n.name===t);if(!p){{p=figma.createPage();p.name=t;}}await figma.setCurrentPageAsync(p);return p.name;}})()"')
    files=" ".join(sorted(f"{fid}-d.jsx" for fid in fids)+ [f"{fid}-m.jsx" for fid in fids])
    ps.append(f'foreach ($f in @({", ".join(chr(39)+f+chr(39) for fid in fids for f in (fid+"-d.jsx",fid+"-m.jsx"))})) {{ figma-cli render (Get-Content $f -Raw) }}')
    ps.append("")
ps.append("# Wire the clickable prototype + arrange every page")
ps.append("figma-cli run .\\link-auth.js")
open(os.path.join(OUT,"render-auth.ps1"),"w").write("\n".join(ps))

print(f"wrote {len(frames)} frames across {len(manifest)} pages, {len(resolved)} links")
for p,fs in manifest.items(): print(f"  {p}: {len(fs)} frames")
