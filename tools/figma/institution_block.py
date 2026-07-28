# ============================================================ INSTITUTION
IP=lambda **kw: desk_panel("d-panel-institution.jpg",**kw)
I1B=(f'<Frame w="fill" flex="col" gap={16}>{field("Institution name","hospital","Garki Medical Centre",ph=False)}'
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
        "Step 1 of 6",[("Register your",False),("institution",True)],
        "Set up your clinic or hospital on Medra. You’ll be the facility admin.",
        I1B,cta("Continue","Continue I1","arrow-right","btn-navy.jpg"),
        [link("Institution already on Medra?","Admin log in","Admin login I")],step=(0,6)),
    mob_form("Auth · Institution — I1 Register · Mobile","Step 1 of 6",
        [("Register your",False),("institution",True)],"You’ll be the facility admin.",
        I1B,cta("Continue","Continue I1","arrow-right","btn-navy.jpg"),
        [link("Already on Medra?","Admin log in","Admin login I")],step=(0,6)))

DOCS=(f'<Frame w="fill" flex="col" gap={13}>{upload("Upload licence",done=True)}'
      f'{upload("Upload cac",done=False,label="CAC certificate")}'
      f'{note("shield-check","Documents are encrypted and used only to verify your institution.","info")}</Frame>')
add("Institution","I2-documents",
    desk_form("Auth · Institution — I2 Verify Documents",
        IP(eyebrow_t="For institutions",head_parts=[("Verified",False),("institutions only",True)],
           sub="Patients trust Medra because every provider on it has been checked by a human.",
           proofs=[proof("file-check","Licence + CAC")]),
        "Step 2 of 6",[("Upload your",False),("documents",True)],
        "We verify every institution before it goes live. Add your practice licence and CAC certificate.",
        DOCS,cta("Continue","Continue I2","arrow-right","btn-navy.jpg"),
        [link("Don’t have them handy?","Save and finish later","Save later I2")],step=(1,6)),
    mob_form("Auth · Institution — I2 Verify Documents · Mobile","Step 2 of 6",
        [("Upload your",False),("documents",True)],"Practice licence and CAC certificate.",DOCS,
        cta("Continue","Continue I2","arrow-right","btn-navy.jpg"),
        [link("","Save and finish later","Save later I2")],step=(1,6)))

SIZE_B=(f'<Frame w="fill" flex="col" gap={17}>'
        f'{stepper_ctl("Doctors &amp; practitioners",8,"Practitioners","Everyone who will see patients on Medra.")}'
        f'{stepper_ctl("Branches / locations",2,"Branches","Each physical site you operate.")}'
        f'{stepper_ctl("Admin &amp; front-desk seats",4,"Seats","Staff who manage bookings but don’t consult.")}'
        f'{field_chips("Patients seen each month",["Under 200","200 – 1,000","1,000 – 5,000","5,000+"],1,"Volume")}</Frame>')
add("Institution","I3-orgsize",
    desk_form("Auth · Institution — I3 Organisation Size",
        IP(eyebrow_t="For institutions",head_parts=[("Pay for",False),("what you use",True)],
           sub="Tell us your size and we’ll recommend the right plan — no guessing, no overpaying.",
           proofs=[proof("users","Per-practitioner pricing"),proof("building","Per-branch pricing")]),
        "Step 3 of 6",[("How big is your",False),("organisation?",True)],
        "Adjust these numbers and we’ll work out your plan on the next screen. You can change them anytime.",
        SIZE_B,cta("See my plan","See plan I3","arrow-right","btn-navy.jpg"),
        [link("Not sure yet?","Skip and see all plans","Skip size I3")],step=(2,6)),
    mob_form("Auth · Institution — I3 Organisation Size · Mobile","Step 3 of 6",
        [("How big is your",False),("organisation?",True)],"We’ll work out the right plan from this.",
        SIZE_B,cta("See my plan","See plan I3","arrow-right","btn-navy.jpg"),
        [link("Not sure yet?","Skip and see all plans","Skip size I3")],step=(2,6)))

RECOMMENDED=(f'<Frame w="fill" flex="col" gap={13} p={20} rounded={22} bg="var:state/info-bg" stroke="var:border/accent" strokeWidth={2}>'
             f'<Frame w="fill" flex="row" justify="between" items="center">'
             f'<Frame flex="row" gap={8} items="center">{I("sparkles",16,A_IC)}{T(12,"semibold","var:text/accent","RECOMMENDED FOR YOU")}</Frame>'
             f'{T(12,"medium","var:text/muted","8 practitioners · 2 branches")}</Frame>'
             f'{T(22,"bold","var:text/strong","Practice plan")}'
             f'<Frame flex="row" gap={5} items="end">{T(34,"bold","var:text/strong","₦145,000")}{T(14,"regular","var:text/muted","/month")}</Frame>'
             f'<Rect w="fill" h={1} bg="var:border/default" />'
             f'{price_line("Practice plan · up to 10 practitioners","₦120,000")}'
             f'{price_line("1 extra branch × ₦25,000","₦25,000")}'
             f'{price_line("4 admin seats · included","₦0")}'
             f'<Rect w="fill" h={1} bg="var:border/default" />'
             f'{price_line("Total per month","₦145,000",strong=True)}'
             f'{T(12,"regular","var:text/muted","Billed monthly after your 30-day free trial. Switch to annual and get 2 months free.")}</Frame>')
ADJUST=(f'<Frame w="fill" flex="col" gap={13} p={18} rounded={22} bg="var:bg/base" stroke="var:border/subtle" strokeWidth={1}>'
        f'<Frame flex="row" gap={8} items="center">{I("sliders-horizontal",16,N_IC)}{T(14,"semibold","var:text/strong","Adjust your numbers")}</Frame>'
        f'<Frame w="fill" flex="row" gap={12}>'
        f'<Frame grow={1} flex="col">{stepper_ctl("Practitioners",8,"Adj practitioners")}</Frame>'
        f'<Frame grow={1} flex="col">{stepper_ctl("Branches",2,"Adj branches")}</Frame></Frame>'
        f'{T(12,"regular","var:text/muted","Your price updates instantly. Extra practitioner ₦8,000/mo · extra branch ₦25,000/mo.")}</Frame>')
OTHER_PLANS=(f'<Frame w="fill" flex="col" gap={11}>'
             f'{plan("Starter","₦45,000","1 practitioner · 1 branch · core booking &amp; records")}'
             f'{plan("Group","₦280,000","Up to 30 practitioners · up to 3 branches · analytics")}'
             f'{plan("Enterprise","Custom","Unlimited practitioners &amp; branches · SSO · dedicated support")}</Frame>')
PLAN_B=(f'<Frame w="fill" flex="col" gap={16}>{segmented(["Monthly","Annual · 2 months free"],0,"Billing")}'
        f'{RECOMMENDED}{ADJUST}'
        f'{T(13,"semibold","var:text/default","Other plans")}{OTHER_PLANS}'
        f'{note("sparkles","Every plan starts with a 30-day free trial — no card required.","ok")}</Frame>')
add("Institution","I4-plan",
    desk_form("Auth · Institution — I4 Your Plan",
        IP(eyebrow_t="For institutions",head_parts=[("Priced to",False),("your size",True)],
           sub="From a single practice to a multi-branch group — pay only for what you need.",
           proofs=[proof("credit-card","Paystack billing"),proof("receipt","Cancel anytime")]),
        "Step 4 of 6",[("Your recommended",False),("plan",True)],
        "Based on 8 practitioners across 2 branches. Change anything below — the price updates as you go.",
        PLAN_B,cta("Start my free trial","Start trial I4"),
        [link("Need something custom?","Talk to our team","Sales I4")],step=(3,6)),
    mob_form("Auth · Institution — I4 Your Plan · Mobile","Step 4 of 6",
        [("Your recommended",False),("plan",True)],"Based on 8 practitioners across 2 branches.",
        PLAN_B,cta("Start my free trial","Start trial I4"),
        [link("Need something custom?","Talk to our team","Sales I4")],step=(3,6)))

OTP_I=(f'<Frame w="fill" flex="col" gap={14}>{otp("77")}{link("Didn’t get it?","Resend in 0:25","Resend I5")}'
       f'{checkbox("Trust this device for 30 days","Trust device I5")}</Frame>')
add("Institution","I5-otp",
    desk_form("Auth · Institution — I5 Verify Admin",
        IP(eyebrow_t="For institutions",head_parts=[("Secure the",False),("admin account",True)],
           sub="The facility admin controls staff and billing — so we protect it properly.",
           proofs=[proof("lock","Encrypted")]),
        "Step 5 of 6",[("Verify the",False),("admin phone",True)],
        "Enter the 6-digit code sent to +234 802 111 2233.",
        OTP_I,cta("Verify","Verify I5","arrow-right","btn-navy.jpg"),
        [link("Wrong number?","Change it","Change number I5")],step=(4,6)),
    mob_form("Auth · Institution — I5 Verify Admin · Mobile","Step 5 of 6",
        [("Verify the",False),("admin phone",True)],"Code sent to +234 802 111 2233.",OTP_I,
        cta("Verify","Verify I5","arrow-right","btn-navy.jpg"),
        [link("Wrong number?","Change it","Change number I5")],step=(4,6)))

PWD_I=PWD.replace("Create password","Create admin password")
add("Institution","I6-password",
    desk_form("Auth · Institution — I6 Set Password",
        IP(eyebrow_t="For institutions",head_parts=[("One",False),("key-holder",True)],
           sub="Strong protection for the account that runs your facility."),
        "Step 6 of 6",[("Secure the",False),("admin account",True)],
        "You’ll use this together with the admin phone to log in.",
        PWD_I,cta("Create account","Create I6","arrow-right","btn-navy.jpg"),[],step=(5,6)),
    mob_form("Auth · Institution — I6 Set Password · Mobile","Step 6 of 6",
        [("Secure the",False),("admin account",True)],"Used with the admin phone to log in.",
        PWD_I,cta("Create account","Create I6","arrow-right","btn-navy.jpg"),[],step=(5,6)))

PEND_I=(f'<Frame w="fill" flex="col" gap={16} items="center">{big_icon("badge-check","warn")}'
        f'{T(15,"regular","var:text/muted","Thanks, Mr. Bello. We’re reviewing Garki Medical Centre’s documents — usually within 1–2 business days.",w="fill",align="center")}'
        f'{note("clock","We’ll email you the moment you’re approved. Meanwhile you can add staff and set up your rooms.","warn")}</Frame>')
add("Institution","I7-pending",
    desk_form("Auth · Institution — I7 Application Submitted",
        IP(eyebrow_t="Welcome to Medra for Business",head_parts=[("Your facility’s new",False),("operating system",True)],
           sub="Your 30-day trial starts today — set things up while we verify.",
           proofs=[proof("sparkles","Trial active · 30 days left")]),
        "Submitted",[("Application",False),("submitted",True)],"Here’s exactly what happens next.",
        PEND_I,cta("Go to admin portal","Go portal I7","layout-dashboard","btn-navy.jpg"),
        [link("Need to add a document?","Manage application","Manage I7")],back=False),
    mob_form("Auth · Institution — I7 Application Submitted · Mobile","Submitted",
        [("Application",False),("submitted",True)],"Your 30-day trial has started.",PEND_I,
        cta("Go to admin portal","Go portal I7","layout-dashboard","btn-navy.jpg"),
        [link("","Manage application","Manage I7")],back=False))

I8B=(f'<Frame w="fill" flex="col" gap={16}>{field("Work email","mail","admin@garkimedical.ng",ph=False)}'
     f'{field("Password","lock","••••••••",ph=False,trailing=("eye","Show password"))}'
     f'{checkbox("Keep me signed in for 30 days","Stay signed in I8")}'
     f'<Frame w="fill" flex="row" justify="end">{link("","Forgot password?","Forgot I8",center=False)}</Frame></Frame>')
add("Institution","I8-admin-login",
    desk_form("Auth · Institution — I8 Facility Admin Log In",
        IP(eyebrow_t="Welcome back",head_parts=[("Your facility,",False),("in control",True)],
           sub="Everything that runs your clinic, one secure login away.",
           proofs=[proof("calendar-check","12 bookings today")]),
        "Facility admin",[("Facility admin",False),("log in",True)],
        "Sign in to manage bookings, staff and billing.",
        I8B,cta("Log in","Login submit I8","arrow-right","btn-navy.jpg"),
        [divider_or("or continue with"), social_btn("google","Continue with Google","Google admin"),
         link("Registering a new institution?","Start here","Register I8")]),
    mob_form("Auth · Institution — I8 Facility Admin Log In · Mobile","Facility admin",
        [("Facility admin",False),("log in",True)],"Manage bookings, staff and billing.",I8B,
        cta("Log in","Login submit I8","arrow-right","btn-navy.jpg"),
        [social_btn("google","Continue with Google","Google admin"),
         link("Forgot password?","Reset it","Forgot I8"),link("New institution?","Start here","Register I8")]))

add("Institution","I9-forgot",
    desk_form("Auth · Institution — I9 Forgot Password",
        IP(eyebrow_t="Account recovery",head_parts=[("Locked out?",False),("We’ll fix that",True)],
           sub="A quick code and your facility is back online."),
        "Reset password",[("Reset admin",False),("password",True)],
        "Enter the admin email and we’ll send a reset code.",
        field("Work email","mail","admin@garkimedical.ng",ph=False,helper="We’ll send the reset code here."),
        cta("Send reset code","Send reset I9","arrow-right","btn-navy.jpg"),
        [link("Remembered it?","Back to log in","Back login I9")]),
    mob_form("Auth · Institution — I9 Forgot Password · Mobile","Reset password",
        [("Reset admin",False),("password",True)],"We’ll send a reset code.",
        field("Work email","mail","admin@garkimedical.ng",ph=False),
        cta("Send reset code","Send reset I9","arrow-right","btn-navy.jpg"),
        [link("Remembered it?","Back to log in","Back login I9")]))

add("Institution","I10-reset",
    desk_form("Auth · Institution — I10 New Password",
        IP(eyebrow_t="Account recovery",head_parts=[("Back in",False),("control",True)],
           sub="New password set — your facility awaits."),
        "New password",[("Choose a new",False),("password",True)],
        "Make it strong — it controls your whole facility.",
        NEWPWD,cta("Save and log in","Save password I10","arrow-right","btn-navy.jpg"),[]),
    mob_form("Auth · Institution — I10 New Password · Mobile","New password",
        [("Choose a new",False),("password",True)],"It controls your whole facility.",NEWPWD,
        cta("Save and log in","Save password I10","arrow-right","btn-navy.jpg"),[]))

SUC_I=(f'<Frame w="fill" flex="col" gap={16} items="center">{big_icon("circle-check","ok")}'
       f'{T(15,"regular","var:text/muted","Garki Medical Centre is approved and live on Medra. Patients in Abuja can book your doctors now.",w="fill",align="center")}'
       f'{note("info","Taking you to your admin portal…","info")}</Frame>')
add("Institution","I11-success",
    desk("Auth · Institution — I11 Success",
        desk_panel("d-panel-institution.jpg","You’re live",[("Your facility is",False),("on Medra",True)],
                   "Start adding doctors and taking bookings today.",
                   stats=[("Live","Status"),("30","Trial days left"),("₦145k","Monthly plan")]),
        f'{eyebrow("Approved")}{head_chip([("You’re live,",False),("Mr. Bello",True)],32)}{SUC_I}'
        f'{cta("Go to admin portal","Go portal I11","layout-dashboard","btn-navy.jpg")}'
        f'{ghost("Invite my doctors","Invite I11","user-plus")}'),
    mob_hero("Auth · Institution — I11 Success · Mobile","m-hero-institution.jpg","Approved",
        [("You’re live,",False),("Mr. Bello",True)],"Your facility is verified and taking bookings.",
        cta("Go to admin portal","Go portal I11","layout-dashboard","btn-navy.jpg"),
        [ghost("Invite my doctors","Invite I11","user-plus")],skip=False,
        proofs=[proof("circle-check","Approved")]))

