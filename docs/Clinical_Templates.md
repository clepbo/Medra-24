# Clinical templates — where the field lists came from

**Status: designed from published convention, awaiting a clinician.** Two items from the
14 August review were blocked because "the field list is the design" and nobody on the project
is a clinician. They are now built from documented standards rather than invented, so that the
screens exist and a doctor is reviewing *a specific proposal* instead of a blank page. Nothing
here should reach build without that review.

Two things are being proposed:

1. **A structured examination template** on `C1 In Progress` — Godwin's strongest request.
2. **A replacement for private notes** on `C7 Review & Sign` and `R2 Consultation Note` — the
   reversal Godwin asked for, built the way published guidance actually handles it rather than
   as a straight flip of the default.

---

## 1. The examination template

> **Godwin (third review):** "Blood pressure this over this, and the doctor just puts in the
> numbers… sometimes you are rushing with a patient and you forget some of the things you
> needed to do, but if you see a template of what you need to fill in, then you know."

He is describing a **checklist that prevents omission under time pressure**, not a data-entry
convenience. That is why the built version draws an unfilled field as visibly unfilled — on
`C1`, respiratory rate is empty and stays empty rather than disappearing.

### The fields, and why each one

| Field | Unit | Source |
|---|---|---|
| Blood pressure — **1st reading** | mmHg | WHO HEARTS |
| Blood pressure — **2nd reading** | mmHg | WHO HEARTS — the reading the diagnosis is made on |
| Pulse | bpm | conventional vital signs |
| Temperature | °C | conventional vital signs |
| Respiratory rate | /min | conventional vital signs |
| Oxygen saturation | % | conventional vital signs |
| Weight | kg | anthropometry |
| Height | m | anthropometry |
| **BMI** | kg/m² | **computed, never typed** — Godwin's explicit ask |

**The five conventional vital signs** — temperature, pulse, respiratory rate, blood pressure
and oxygen saturation — plus height, weight and a computed BMI are how every published
vital-signs template defines the set, and they are the variables the CDISC `VS` domain
standardises for clinical data capture. This is not a Medra invention and should not read as
one.

**Blood pressure is recorded twice.** The WHO **HEARTS** technical package defines hypertension
on blood pressure "measured twice", not once. That matters here more than anywhere else:
HEARTS is the protocol running under the **Hypertension Treatment in Nigeria (HTN) programme in
60 primary-care centres in the Federal Capital Territory** — Medra's own pilot geography — where
it has taken treatment rates past 90%. A template that captures a single reading cannot express
the diagnosis it exists for, and would not match how the clinics around the pilot already work.

**BMI is computed.** Godwin asked for this by name, and it is also the thing that stops a busy
clinic recording a height and a weight and never doing anything with them. On `C1` it carries a
"Calculated" marker so nobody mistakes it for something the doctor typed.

### What the template deliberately does not do

It **does not score, warn, or diagnose.** It tints a value that falls outside the reference
range and stops there. Anything further — a cardiovascular risk score, a treatment prompt — is a
clinical decision-support feature and needs regulatory thought that a design file cannot supply.

### Questions for the clinician

1. Is this the right field set for a **general-practice** template, or should the default be
   shorter still — blood pressure, pulse, weight, BMI — with the rest opened when needed?
2. Which **other templates** does the FCT pilot actually need on day one? Antenatal and
   paediatric are the obvious two, and neither wants this grid unchanged.
3. Should the second BP reading be **required** before the note can be signed for a
   hypertension review, or only prompted?
4. Are the reference ranges we tint against acceptable, or should they be **set per
   organisation** the way laboratory ranges already are?

**Sources:** [Vital signs template](https://www.heidihealth.com/en-us/blog/vital-signs-template) ·
[CDISC vital signs domain](https://www.cdisc.org/kb/ecrf/vital-signs) ·
[CMS record vital signs](https://www.cms.gov/Regulations-and-Guidance/Legislation/EHRIncentivePrograms/downloads/Stage2_EPCore_4_RecordVitalSigns.pdf) ·
[WHO HEARTS in Nigeria](https://www.afro.who.int/news/nigeria-collaborates-who-curb-hypertension-introduces-control-initiative) ·
[Hypertension Treatment in Nigeria programme](https://pmc.ncbi.nlm.nih.gov/articles/PMC11247806/) ·
[HEARTS implementation, 32 countries](https://www.jacc.org/doi/10.1016/j.jacc.2023.08.043)

---

## 2. Private notes → withholding on stated grounds

> **Abraham (43:19):** "I know these notes are private, the patient does not get to see them,
> right?"
> **Godwin (43:46):** "No — everything is supposed to be between the both of you… except
> psychiatry, psychology."

### What was built before

A blanket **private notes** field, off by default, where the member was told *that* a private
note existed but not what it said. PRD Module 6 and §13 AC both say private notes are never
patient-visible.

### Why a straight flip is the wrong fix

Private notes exist so a clinician can record a suspicion, a safeguarding concern, or something
a third party told them in confidence. Making everything visible removes that; making nothing
visible is what Godwin objected to. **Published practice does neither** — it defaults to open
and allows a named, narrow exception per item.

### What is built now

**Default: the member sees the note.** A clinician may withhold **one item**, and must choose a
ground. There are three, and no fourth:

| Ground | What it means | Where it comes from |
|---|---|---|
| **Serious harm** | Releasing it would likely cause serious physical or mental harm to the member or to somebody else. **Explicitly not** "she may find it upsetting" | the serious-harm test used for online record access |
| **Somebody else's information** | Given by or about a third party who has not agreed to it being shared. **A colleague is never a third party** — other clinicians stay identifiable and what they write is disclosable | third-party rules for the same |
| **Psychotherapy note** | Psychiatry and psychology only, and kept apart from the record rather than inside it | the psychotherapy-notes exception, which is the one carve-out in law that otherwise mandates full release |

**The member is told which ground.** `R2` now carries a line naming it, and offering both an
explanation from the doctor and a review of the decision — rather than the old "a private note
exists", which tells somebody that something is being kept from them and nothing else.

This lands almost exactly where Godwin did — everything is between the two of you, except
psychiatry and psychology — while keeping the two grounds a clinician genuinely needs and that
a transcript line would have removed.

### Questions for the clinician

1. Are these three grounds the right ones **for Nigeria**, and does MDCN guidance name others?
2. Should withholding on **serious harm** require a second clinician's agreement, as some
   services require?
3. Is per-item withholding workable in a rushed clinic, or will it collapse into "withhold
   everything" the way a blanket toggle did?
4. What should a member's **request to review** a withholding actually do — who answers it, and
   in what time?

**Sources:** [NHS England — redacting information for online record access](https://www.england.nhs.uk/long-read/redacting-information-for-online-record-access/) ·
[NHS England — online access to GP record information](https://www.england.nhs.uk/long-read/online-access-to-new-gp-health-record-information/) ·
[Redacting sensitive information from health records (MDDUS)](https://www.mddus.com/resources/resource-library/risk-alerts/2022/march/redacting-sensitive-information-from-medical-records) ·
[Access to psychotherapy notes: legal standards](https://www.psychiatryonline.org/doi/10.1176/appi.psychotherapy.20230036) ·
[Patient-accessible records in mental health (scoping review)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11845895/)

---

## 3. What still has no clinical answer

Neither of these is affected by the work above, and both were on the list before it:

- **The referral / recommendation gap.** Godwin distinguished a *referral* from a
  *recommendation* — "the drugs you propose, or the diet you propose". Medra has prescriptions
  and has nowhere for advice that is not a drug: diet, exercise, salt, when to come back, what
  to watch for. That is most of what a hypertension review produces.
- **Deceased and inactive record states.** Nothing in the file says what a record does when the
  person it belongs to dies, or when an account goes dormant.
