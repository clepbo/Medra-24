#!/usr/bin/env python3
"""Apply review feedback to the Medra auth builder.
Blocks below are written with SINGLE braces for numeric literals; _esc() doubles them
on f-string source lines so the generated JSX emits {n} correctly."""
import re
P='/home/user/Medra-24/tools/figma/build_auth.py'
src=open(P).read()

def _esc(block):
    out=[]
    for ln in block.split("\n"):
        if "f'" in ln or 'f"' in ln:
            ln=re.sub(r'(?<!\{)\{(\d+)\}(?!\})', r'{{\1}}', ln)
        out.append(ln)
    return "\n".join(out)

# ---------------------------------------------------------------- 1. components
COMPONENTS = '''
def segmented(options, sel=0, name="seg"):
    out=""
    for i,o in enumerate(options):
        s=i==sel
        st=('bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}' if s else 'bg="var:neutral/100"')
        out+=(f'<Frame name="Btn {name} {o}" grow={1} flex="row" justify="center" px={16} py={11} rounded={999} {st}>'
              f'{T(14,"semibold","var:text/strong" if s else "var:text/muted",o)}</Frame>')
    return f'<Frame w="fill" flex="row" gap={4} p={4} rounded={999} bg="var:neutral/100">{out}</Frame>'

def social_btn(brand,label,name):
    img={"google":"brand-google.png","apple":"brand-apple.png"}[brand]
    return (f'<Frame name="Btn {name}" w="fill" flex="row" gap={10} justify="center" items="center" px={22} py={15} '
            f'rounded={999} bg="var:bg/base" stroke="var:border/default" strokeWidth={1}>'
            f'<Image image="assets/img/{img}" w={20} h={20} />{T(15,"semibold","var:text/default",label)}</Frame>')

def divider_or(txt="or"):
    return (f'<Frame w="fill" flex="row" gap={12} items="center"><Rect grow={1} h={1} bg="var:border/subtle" />'
            f'{T(12,"medium","var:text/faint",txt)}<Rect grow={1} h={1} bg="var:border/subtle" /></Frame>')

def stepper_ctl(label, value, name, helper=None):
    sub=T(12,"regular","var:text/muted",helper) if helper else ""
    return (f'<Frame w="fill" flex="col" gap={7}>{T(13,"medium","var:text/default",label)}'
            f'<Frame w="fill" flex="row" gap={12} items="center" px={12} py={9} rounded={16} bg="var:neutral/50" stroke="var:border/subtle" strokeWidth={1}>'
            f'<Frame name="Btn {name} minus" w={36} h={36} rounded={999} bg="var:bg/base" stroke="var:border/default" strokeWidth={1} flex="col" justify="center" items="center">{I("minus",17,N_IC)}</Frame>'
            f'<Frame grow={1} flex="col" items="center">{T(20,"bold","var:text/strong",str(value))}</Frame>'
            f'<Frame name="Btn {name} plus" w={36} h={36} rounded={999} image="assets/img/btn-navy.jpg" overflow="hidden" flex="col" justify="center" items="center">{I("plus",17,W_IC)}</Frame>'
            f'</Frame>{sub}</Frame>')

def price_line(label, amount, strong=False):
    return (f'<Frame w="fill" flex="row" justify="between" items="center">'
            f'{T(14,"semibold" if strong else "regular","var:text/strong" if strong else "var:text/muted",label)}'
            f'{T(16 if strong else 14,"bold" if strong else "medium","var:text/strong",amount)}</Frame>')

def biometric_btn(name):
    return (f'<Frame name="Btn {name}" w={108} h={108} rounded={999} image="assets/img/btn-teal.jpg" overflow="hidden" '
            f'flex="col" justify="center" items="center">{I("fingerprint",46,W_IC)}</Frame>')

'''
COMPONENTS=_esc(COMPONENTS)
src = src.replace("# ---------- mobile chrome ----------", COMPONENTS + "# ---------- mobile chrome ----------")

# ---------------------------------------------------------------- 2. MEMBER replaces PATIENT
MEMBER = '''# ============================================================ MEMBER (people using Medra for their own care)
MP=lambda **kw: desk_panel("d-panel-member.jpg",**kw)
SIGNUP_B=(f'<Frame w="fill" flex="col" gap={16}>'
          f'{segmented(["Phone number","Email"],0,"Method")}'
          f'{field("Phone number","phone","801 234 5678",prefix="+234",helper="We’ll text a 6-digit code once to confirm it.")}'
          f'{checkbox("I agree to Medra’s Terms of Service and Privacy Policy, and consent to my health data being processed under the NDPR.","Consent")}</Frame>')
SOCIALS=[divider_or("or continue with"), social_btn("google","Continue with Google","Google signup"),
         social_btn("apple","Continue with Apple","Apple signup"),
         link("Already have an account?","Log in","Login M")]
add("Member","M1-create",
    desk_form("Auth · Member — M1 Create Account",
        MP(eyebrow_t="For members",head_parts=[("Your health,",False),("in one place",True)],
           sub="No paper to carry. No history to lose. Just care that knows you.",
           proofs=[proof("shield-check","NDPR secure"),proof("badge-check","Verified doctors")]),
        "Step 1 of 5",[("Create your",False),("account",True)],
        "Choose how you’d like to sign up. You’ll only need to verify once — after that we remember your device.",
        SIGNUP_B,cta("Continue","Send code M1"),SOCIALS,step=(0,5)),
    mob_form("Auth · Member — M1 Create Account · Mobile","Step 1 of 5",
        [("Create your",False),("account",True)],"Sign up your way — verify once, then we remember this device.",
        SIGNUP_B,cta("Continue","Send code M1"),SOCIALS,step=(0,5)))

OTP_M=(f'<Frame w="fill" flex="col" gap={14}>{otp("3907")}'
       f'{link("Didn’t get it?","Resend in 0:24","Resend M2")}'
       f'{checkbox("Keep me signed in on this device","Trust device")}'
       f'{note("shield-check","We’ll remember this device for 30 days — no code needed next time. Always ask on a shared phone.","info")}</Frame>')
add("Member","M2-otp",
    desk_form("Auth · Member — M2 Verify Once",
        MP(eyebrow_t="For members",head_parts=[("Verify once,",False),("not every time",True)],
           sub="Confirming your number keeps your records yours alone — then we stay out of your way.",
           proofs=[proof("lock","Encrypted"),proof("smartphone","Trusted device")]),
        "Step 2 of 5",[("Enter the",False),("6-digit code",True)],"We sent it to +234 801 234 5678 by SMS.",
        OTP_M,cta("Verify and continue","Verify M2"),
        [link("Wrong number?","Change it","Change number M2"),link("Code not arriving?","Get help another way","Help code M2")],step=(1,5)),
    mob_form("Auth · Member — M2 Verify Once · Mobile","Step 2 of 5",
        [("Enter the",False),("6-digit code",True)],"Sent to +234 801 234 5678.",
        OTP_M,cta("Verify and continue","Verify M2"),
        [link("Wrong number?","Change it","Change number M2"),link("","Get help another way","Help code M2")],step=(1,5)))

NAME_B=(f'<Frame w="fill" flex="col" gap={18}>'
        f'<Frame w="fill" flex="row" gap={15} items="center">'
        f'<Frame w={74} h={74} rounded={999} bg="var:bg/muted" flex="col" justify="center" items="center">{I("camera",25,A_IC)}</Frame>'
        f'<Frame name="Btn Add photo" flex="row" gap={8} items="center" px={16} py={11} rounded={999} bg="var:bg/base" stroke="var:border/default" strokeWidth={1}>'
        f'{I("upload",16,N_IC)}{T(13,"semibold","var:text/default","Add a photo (optional)")}</Frame></Frame>'
        f'{field("Full name","user","Amara Okeke",ph=False)}'
        f'{field("Date of birth","calendar-days","12 March 1994",ph=False,helper="Helps your doctor prescribe safely.")}</Frame>')
add("Member","M3-name",
    desk_form("Auth · Member — M3 Your Name",
        MP(eyebrow_t="For members",head_parts=[("Care that",False),("knows you",True)],
           sub="Your details stay private and are shared only with doctors you choose to book.",
           proofs=[proof("lock","Private by default")]),
        "Step 3 of 5",[("What should we",False),("call you?",True)],
        "This is the name your doctor will see on your records.",
        NAME_B,cta("Continue","Continue M3"),[link("","Skip for now","Skip M3")],step=(2,5)),
    mob_form("Auth · Member — M3 Your Name · Mobile","Step 3 of 5",
        [("What should we",False),("call you?",True)],"This is the name your doctor will see.",
        NAME_B,cta("Continue","Continue M3"),[link("","Skip for now","Skip M3")],step=(2,5)))

ABOUT_B=(f'<Frame w="fill" flex="col" gap={18}>'
         f'{field_chips("Gender",["Female","Male","Non-binary","Prefer not to say"],0,"Gender")}'
         f'{field_chips("Preferred language",["English","Hausa","Yoruba","Igbo","Pidgin"],0,"Language")}'
         f'{field_chips("Text size",["Standard","Large","Extra large"],0,"Textsize")}</Frame>')
add("Member","M4-about",
    desk_form("Auth · Member — M4 About You",
        MP(eyebrow_t="For members",head_parts=[("Made for",False),("everyone",True)],
           sub="Medra works in your language, at your pace, however you need to use it.",
           proofs=[proof("globe","5 languages"),proof("accessibility","Accessible")]),
        "Step 4 of 5",[("A few things",False),("about you",True)],
        "Tap to choose. You can change any of this later in Settings.",
        ABOUT_B,cta("Continue","Continue M4"),[link("","Skip for now","Skip M4")],step=(3,5)),
    mob_form("Auth · Member — M4 About You · Mobile","Step 4 of 5",
        [("A few things",False),("about you",True)],"Tap to choose — change any of it later.",
        ABOUT_B,cta("Continue","Continue M4"),[link("","Skip for now","Skip M4")],step=(3,5)))

HEALTH_B=(f'<Frame w="fill" flex="col" gap={16}>'
          f'{field_chips("Blood group",["A+","A-","B+","B-","O+","O-","AB+","Not sure"],4,"Blood")}'
          f'{field("Allergies","triangle-alert","e.g. penicillin, peanuts")}'
          f'{field("Medicines you take now","pill","e.g. metformin 500mg")}'
          f'{field("Emergency contact","phone-call","802 000 0000",prefix="+234")}</Frame>')
add("Member","M5-health",
    desk_form("Auth · Member — M5 Health Basics",
        MP(eyebrow_t="For members",head_parts=[("Safer",False),("prescriptions",True)],
           sub="Knowing your allergies and current medicines helps any doctor avoid a dangerous clash.",
           proofs=[proof("heart-pulse","Clinical safety"),proof("pill","Drug-clash aware")]),
        "Step 5 of 5",[("Your",False),("health basics",True)],
        "Optional, but it helps doctors keep you safe. You can add more anytime.",
        HEALTH_B,cta("Finish and go to my home","Finish M5"),[link("","I’ll do this later","Skip M5")],step=(4,5)),
    mob_form("Auth · Member — M5 Health Basics · Mobile","Step 5 of 5",
        [("Your",False),("health basics",True)],"Optional — but it helps doctors keep you safe.",
        HEALTH_B,cta("Finish","Finish M5"),[link("","I’ll do this later","Skip M5")],step=(4,5)))

LOGIN_B=(f'<Frame w="fill" flex="col" gap={16}>{segmented(["Phone number","Email"],0,"Login method")}'
         f'{field("Phone number","phone","801 234 5678",prefix="+234",focus=True)}'
         f'{checkbox("Keep me signed in on this device","Stay signed in")}</Frame>')
LOGIN_X=[divider_or("or continue with"), social_btn("google","Continue with Google","Google login"),
         social_btn("apple","Continue with Apple","Apple login"),
         link("New to Medra?","Create an account","Create M6"),
         link("Can’t access your number?","Get help","Help M6")]
add("Member","M6-login",
    desk_form("Auth · Member — M6 Log In",
        MP(eyebrow_t="Welcome back",head_parts=[("Good to see you",False),("again",True)],
           sub="Your appointments and records are exactly where you left them.",
           proofs=[proof("calendar-check","2 upcoming visits")]),
        "Log in",[("Welcome",False),("back",True)],
        "Use whichever is easiest — we only ask for a code on a new device.",
        LOGIN_B,cta("Continue","Send code M6"),LOGIN_X),
    mob_form("Auth · Member — M6 Log In · Mobile","Log in",[("Welcome",False),("back",True)],
        "We only ask for a code on a new device.",
        LOGIN_B,cta("Continue","Send code M6"),LOGIN_X))

UNLOCK_B=(f'<Frame w="fill" flex="col" gap={18} items="center">'
          f'<Image image="assets/img/avatar-2.jpg" w={92} h={92} rounded={999} />'
          f'{T(20,"bold","var:text/strong","Amara Okeke")}'
          f'{T(14,"regular","var:text/muted","+234 801 234 5678",align="center")}'
          f'{SP(4)}{biometric_btn("Biometric unlock")}'
          f'{T(14,"medium","var:text/default","Tap to unlock with fingerprint",align="center")}'
          f'{note("shield-check","This device is trusted — no code needed. Trust expires after 30 days of not signing in.","ok")}</Frame>')
add("Member","M7-unlock",
    desk_form("Auth · Member — M7 Quick Unlock",
        MP(eyebrow_t="Trusted device",head_parts=[("No codes,",False),("no waiting",True)],
           sub="You verified this device already — from now on it’s one tap to get back in.",
           proofs=[proof("fingerprint","Biometric unlock"),proof("clock","30-day trust")]),
        "Quick unlock",[("Welcome back,",False),("Amara",True)],
        "Unlock with your fingerprint or face — no code required on this device.",
        UNLOCK_B,cta("Unlock","Unlock M7","fingerprint"),
        [link("","Use a one-time code instead","Use code M7"),link("Not you?","Switch account","Switch M7")],back=False),
    mob_form("Auth · Member — M7 Quick Unlock · Mobile","Quick unlock",
        [("Welcome back,",False),("Amara",True)],"Unlock with your fingerprint — no code needed.",
        UNLOCK_B,cta("Unlock","Unlock M7","fingerprint"),
        [link("","Use a one-time code instead","Use code M7"),link("Not you?","Switch account","Switch M7")],back=False))

HELPC=(f'<Frame w="fill" flex="col" gap={11}>'
       f'{choice("refresh-cw","Resend the code","Text the 6-digit code again","Resend help")}'
       f'{choice("phone-call","Call me instead","Get the code by automated call","Call help")}'
       f'{choice("mail","Use my email instead","Send the code to my email address","Email help")}'
       f'{choice("message-square-text","Message support","Chat with the Medra team","Support help")}</Frame>')
add("Member","M8-help",
    desk_form("Auth · Member — M8 Cannot Get Code",
        MP(eyebrow_t="We’ve got you",head_parts=[("No one gets",False),("stuck",True)],
           sub="There is always another way in. If none of these work, our team will help you personally.",
           proofs=[proof("helping-hand","Human support")]),
        "Trouble signing in",[("Didn’t get your",False),("code?",True)],
        "Pick an option below — we’ll get you in.",HELPC,
        ghost("Back to verification","Back to OTP","arrow-left"),[]),
    mob_form("Auth · Member — M8 Cannot Get Code · Mobile","Trouble signing in",
        [("Didn’t get your",False),("code?",True)],"Pick an option — we’ll get you in.",HELPC,
        ghost("Back to verification","Back to OTP","arrow-left")))

SUC_M=(f'<Frame w="fill" flex="col" gap={16} items="center">{big_icon("circle-check","ok")}'
       f'{T(15,"regular","var:text/muted","Your account is ready and this device is trusted — next time you’ll go straight in.",w="fill",align="center")}'
       f'{note("info","Taking you to your home…","info")}</Frame>')
add("Member","M9-success",
    desk("Auth · Member — M9 Success",
        desk_panel("success.jpg","You’re in",[("Welcome to",False),("Medra",True)],
                   "Care that follows you — everywhere in Nigeria.",
                   stats=[("180+","Verified doctors"),("24/7","Booking"),("4.9","Member rating")]),
        f'{eyebrow("All set")}{head_chip([("You’re all set,",False),("Amara",True)],32)}{SUC_M}'
        f'{cta("Go to my home","Go home M9","house")}{ghost("Explore doctors near me","Explore M9","search")}'),
    mob_hero("Auth · Member — M9 Success · Mobile","m-hero-member.jpg","All set",
        [("You’re all set,",False),("Amara",True)],"Your account is ready — let’s find you care.",
        cta("Go to my home","Go home M9","house"),[ghost("Explore doctors near me","Explore M9","search")],skip=False,
        proofs=[proof("circle-check","Account verified"),proof("fingerprint","Device trusted")]))

'''
MEMBER=_esc(MEMBER)
i0=src.index("# ============================================================ PATIENT")
i1=src.index("# ============================================================ DOCTOR")
src = src[:i0] + MEMBER + src[i1:]

# ---------------------------------------------------------------- 3. Doctor tweaks
src = src.replace(
 '''D1B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone number","phone","803 555 0110",prefix="+234")}'
     f'{field("MDCN number","id-card","MDCN/45201",helper="Your Medical &amp; Dental Council of Nigeria licence number.")}'
     f'{field_chips("Specialisation",["Cardiology","General practice","Paediatrics","Other"],1,"Specialty")}</Frame>')''',
 '''D1B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Full name","user","Dr. Ngozi Okafor",ph=False)}'
     f'{field("Work email","mail","dr.okafor@clinic.ng",ph=False,helper="You can sign in with this, your phone or your MDCN number.")}'
     f'{field("Phone number","phone","803 555 0110",prefix="+234")}'
     f'{field("MDCN number","id-card","MDCN/45201",helper="Your Medical &amp; Dental Council of Nigeria registration number.")}'
     f'{field_chips("Specialisation",["Cardiology","General practice","Paediatrics","Other"],1,"Specialty")}</Frame>')''')
src = src.replace(
 '''D6B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone or email","user","dr.okafor@clinic.ng",ph=False)}''',
 '''D6B=(f'<Frame w="fill" flex="col" gap={{16}}>{field("Email, phone or MDCN number","id-card","MDCN/45201",ph=False,helper="Any of the three works.")}''')
src = src.replace(
 '''f'<Frame w="fill" flex="col" gap={{16}}>{field("Phone or email","user","dr.okafor@clinic.ng",ph=False)}'
        f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}</Frame>',
        cta("Log in","Login submit D6","arrow-right","btn-navy.jpg"),''',
 '''f'<Frame w="fill" flex="col" gap={{16}}>{field("Email, phone or MDCN","id-card","MDCN/45201",ph=False)}'
        f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}'
        f'{checkbox("Keep me signed in for 30 days","Stay signed in D6")}</Frame>',
        cta("Log in","Login submit D6","arrow-right","btn-navy.jpg"),''')
src = src.replace(
 '''        field("Phone or email","user","dr.okafor@clinic.ng",ph=False,helper="We’ll send the reset code here."),''',
 '''        field("Email, phone or MDCN number","id-card","dr.okafor@clinic.ng",ph=False,helper="We’ll send the reset code to the email or phone on file."),''')
src = src.replace(
 '''        field("Phone or email","user","dr.okafor@clinic.ng",ph=False),
        cta("Send reset code","Send reset D8","arrow-right","btn-navy.jpg"),''',
 '''        field("Email, phone or MDCN","id-card","dr.okafor@clinic.ng",ph=False),
        cta("Send reset code","Send reset D8","arrow-right","btn-navy.jpg"),''')
src = src.replace('"We texted a 6-digit code to +234 803 555 0110 to protect patient data.",',
                  '"New device detected. We texted a 6-digit code to +234 803 555 0110 — you won’t need this on a device you trust.",')
src = src.replace(
 '''OTP_2FA=f'<Frame w="fill" flex="col" gap={{14}}>{otp("41")}{link("Didn’t get it?","Resend in 0:22","Resend D7")}</Frame>\'''',
 '''OTP_2FA=(f'<Frame w="fill" flex="col" gap={{14}}>{otp("41")}{link("Didn’t get it?","Resend in 0:22","Resend D7")}'
         f'{checkbox("Trust this device for 30 days","Trust device D7")}</Frame>')''')

# ---------------------------------------------------------------- 4. INSTITUTION
INSTITUTION = open('/tmp/claude-0/-home-user-Medra-24/8ebde5d2-f0cd-50ad-bd51-1083d4c052a2/scratchpad/institution_block.py').read()
INSTITUTION=_esc(INSTITUTION)
i0=src.index("# ============================================================ INSTITUTION")
i1=src.index("# ---------------- write ----------------")
src = src[:i0] + INSTITUTION + src[i1:]

# ---------------------------------------------------------------- 5. role card, page map, transitions
src = src.replace('choice("user","I am a patient","Book doctors and keep my records","Role Patient",sel=True)',
                  'choice("user","I’m here for my own care","Book doctors and keep my records","Role Member",sel=True)')
src = src.replace('"Entry":"Medra Auth — Entry","Patient":"Medra Auth — Patient",',
                  '"Entry":"Medra Auth — Entry","Member":"Medra Auth — Member",')
TRN = open('/tmp/claude-0/-home-user-Medra-24/8ebde5d2-f0cd-50ad-bd51-1083d4c052a2/scratchpad/trn_block.py').read()
i0=src.index("TRN=[")
i1=src.index("resolved=[]")
src = src[:i0] + TRN + src[i1:]

open(P,'w').write(src)
print("patched build_auth.py")
