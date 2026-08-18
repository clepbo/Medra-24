# Third review — 14 August 2026

**Present:** Godwin Okwor (product) · Abraham Peter (advisor) · Israel Oni (UI/UX)
**Covered:** the doctor module only. The member module was passed over ("just a few touches"),
and the organisation module was not reached.

The transcript is machine-generated and heavily garbled. Everything below is an item I am
confident of; where a reading is uncertain it is marked.

**Status, 14 Aug:** the five unblocked items are **built**.

**Status, 17 Aug:** the two blocked items are now **designed from published convention** rather
than left blank — the examination template from the conventional vital-signs set and the WHO
HEARTS protocol running in the FCT, and private notes from the serious-harm / third-party /
psychotherapy-note grounds used for patient record access. Sources and the open questions for a
clinician are in `docs/Clinical_Templates.md`. **Neither should reach build without that
review** — what has changed is that a doctor is now reviewing a specific proposal.

---

## 1. Three items that contradict what is already designed

These are not additions. Each one reverses a decision that is currently baked into screens, the
PRD, or both, so each needs an explicit yes before it is applied.

### 1.1 Private notes — the patient should see almost everything — ⚠️ designed, needs a clinician

> **Abraham (43:19):** "I know these notes are private, the patient does not get to see them,
> right?"
> **Godwin (43:46):** "No — everything is supposed to be between the both of you… except
> psychiatry, psychology. Only there do the patient not see their notes. Otherwise the patient
> is supposed to see their notes."

**What is built today is the opposite.** PRD Module 6 says private notes are "not patient-visible";
§13 AC says "private notes **never** shown"; `C7 Review & Sign` ships the private-notes switch
**off by default** and states that the member is told a private note exists but not what it says.

**What Godwin is asking for** is that the default flips: the member sees the note unless the
speciality is psychiatry or psychology, where it is withheld.

**This one should not be applied on a transcript line.** Private notes exist so a clinician can
record a suspicion, a safeguarding concern or a differential they are not ready to state — and
Nigerian practice, MDCN guidance and the eventual NDPA position all bear on it. It is a clinical
governance decision, not a design preference. **Take it to a doctor before changing it.**

If it is confirmed, the change is small in the file and large in meaning: `C7`'s share toggles
default on, the private toggle becomes speciality-conditional, and `R2` on the member side gains
the section.

### 1.2 The clinic-progress donut does not belong to the doctor — ✅ done

> **Godwin (15:11):** "Clinic progress is for the whole clinic. It should go to the
> administrators or the receptionists… this part is not necessary for the doctor."
> **Godwin (16:46):** "We already have it as three of it and then a chart… I don't think there
> is any point having it in two places."

Abraham defended it on the grounds that a dashboard should be visual; the meeting landed on
"find something better or leave it".

**Recommendation: remove it from `K1`.** Godwin is right twice over — it duplicates the stat
tiles beside it, and a doctor genuinely does not care how the clinic is doing. It moves to the
organisation admin and front-desk dashboards, where it is the actual subject. This is already
item 5 on the content cut-list, so it costs nothing extra.

### 1.3 Consultation length is set by the practice, not by the patient — ✅ done

> **Godwin (13:16):** "I think we can standardise everything… a private practitioner can say my
> consultation is 30 minutes, and we leave a room for the institution where we ask them how many
> minutes they are allocating to each patient. So if I am booking, what I see is 10:30, 11:00,
> 11:30."

Today the slot grid on `B1` shows times without a stated rule, and neither `K7 Availability` nor
any organisation screen sets a duration. Israel's answer in the meeting — that booking blocks the
doctor's calendar — is about *collision*, not about *length*, which is what Godwin was asking.

**Needed:** a consultation-length setting in two places — the doctor's own availability, and the
organisation's department settings for its doctors — and a slot grid on `B1` that visibly derives
from it.

---

## 2. Additions

| # | What | Where | Size |
|---|---|---|---|
| 2.1 | ✅ **Block specific dates ahead**, on a **single month calendar with drag-selectable ranges**, not from/to dropdowns. "I can just pick the dates on the calendar and it is easier that way." Multiple ranges in one view | `K7`, `K8` | 2 screens redrawn |
| 2.2 | ✅ **Instrumental diagnostics** — ECG, echo, CT, MRI, gastroscopy, colonoscopy — alongside blood and urine. Agreed resolution: rename the section **"Lab results and diagnostics"** and put a type toggle inside rather than splitting it in two | member `R3`, doctor `P2`/`P8` | rename + a toggle |
| 2.3 | ⚠️ **A structured examination template.** "Blood pressure this over this, and the doctor just puts in the numbers… sometimes you are rushing with a patient and you forget some of the things you needed to do, but if you see a template of what you need to fill in, then you know." Blood pressure, pulse, weight, height, and **BMI computed** rather than typed | doctor `C1` | 1 section redrawn |
| 2.4 | ✅ **Earnings shown against the previous period**, with a direction arrow | doctor `K1`, `S5` | 1 tile |

### On 2.3 — this is the strongest request in the review

Godwin is describing a checklist that prevents omission under time pressure, not a data-entry
convenience. It is the single most clinically useful thing anyone asked for across the three
reviews, and it should be built with a clinician rather than from a transcript: the field list is
the design.

---

## 3. Confirmed, no change needed

- **Refill requests stay.** Godwin questioned whether a doctor should handle them, then confirmed
  Nigeria does have prescription-only medicines and the flow is worth it. `P6` stands.
- **"Referral" is the right word** for sending a member to another hospital, doctor or laboratory.
  Godwin separately used "recommendation" for proposed drugs or diet — see §5.
- **Video stays external for MVP.** Abraham confirmed Google's meeting APIs need an Enterprise
  account. `W0` is the ship path; `W1`/`W2`/`W4` stay badged Phase 2.
- **The single-use external link** was walked through and approved without changes.
- **The "next patient" rail** was singled out as good: "sometimes you forget that you have another
  person next in line."

---

## 4. Priority, stated directly

> **Godwin (51:52):** "It is mostly hospitals, medical institutions, not just personal… I think
> our next meeting should be the dashboard of the institutions. Because when institutions
> incorporate, then they will have doctors."
>
> **Israel:** "I have started that but it is not fully completed yet."

**The organisation module is what the next review is for.** That confirms the sequence already
agreed — org before member mobile.

Abraham added a caution that bears directly on the staff-onboarding work:

> **(51:04)** "Even with new features you have KYC for that feature… before you know it, it gets
> too complicated."
> **Godwin (51:21):** "All they need to do now is set up an account, put and verify information.
> That is enough."

**Read as:** keep staff onboarding lean. The ten-screen plan should be pressure-tested against
this — prove identity, prove registration, accept the undertaking, wait for a seat. Anything
beyond that is a later release.

---

## 5. One thing nobody has designed, surfaced accidentally

Godwin distinguished **referral** (sending the member elsewhere) from **recommendation** — "what
you propose, the drugs you propose to the patient, or the diet you propose the patient to take".

Medra has prescriptions. It has no place for **advice that is not a drug**: diet, exercise, weight,
salt, when to come back, what to watch for. That is most of what a hypertension review actually
produces, and every screen in the file currently drops it on the floor or buries it in free text.

Worth raising at the next review as a question rather than assuming it.
