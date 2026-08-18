#!/usr/bin/env python3
"""How much a screen asks a person to read.

`validate.js` proves a frame will render and `proto_check.py` proves it can be reached. Neither
says anything about the thing the product owner actually objected to: *"there are too much of
irrelevant information been added to the screen while some major functions are been left out."*
This is the missing check.

**It counts sentences, not text.** Every `<Text>` node would punish a table for having cells,
which is not what the objection meant. What a reviewer wades through is prose — anything over
24 characters that is not a value, a label or a heading.

**The budgets differ by who is reading.** A member opens Medra once a month and is often
anxious; a doctor uses it between patients and an admin stares at it all day, and both of those
are reading a professional tool they have been trained on. So:

    member  500 characters of prose per screen   (~80 words)
    doctor  700                                  (~110 words)
    org     700
    auth    700

**The rule behind the budget is one explanation per screen.** A screen may say *why* once. Every
other group on it either says nothing or states a fact in under sixty characters. Footers that
explain a rule — who may see this, what cannot be undone, what is charged, what is logged — are
the product speaking and they stay; footers that re-narrate the rows above them are the ones to
cut, and they are usually the longest.

    python3 tools/figma/prose_budget.py              # all four bundles
    python3 tools/figma/prose_budget.py doctor -v    # one, with the offending lines

Exits non-zero when anything is over budget, so a builder can call it and mean it.
"""
import re, sys, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TXT = re.compile(r'<Text[^>]*>(.*?)</Text>', re.S)
# What the user is typing into is content, not chrome. A consultation note is *supposed* to be
# a paragraph of prose; counting it would tell a doctor their own note is too long, which is
# both wrong and none of the design's business. Everything a person authors lives inside a
# field, and a field is a frame named "Btn Field …" holding one Text.
FIELD = re.compile(r'<Frame name="Btn Field [^"]*"[^>]*>.*?</Frame>', re.S)
BUDGET = {"member": 500, "doctor": 700, "org": 700, "auth": 700}
MIN_SENTENCE = 60          # shorter than this is a label, a value or a row subtitle


def is_prose(t):
    """A sentence, not a row of data.

    The first version of this counted anything over 24 characters and got the wrong answer on
    exactly the screens that matter. `C11 Send the order` came out as one of the worst in the
    file — but its longest line is 99 characters and the other thirty-two are row subtitles
    like "Open now · 3 samples in the queue · median 4 hours". That is not a screen explaining
    itself too much; that is six destinations each carrying the fact you choose between them
    on, which is the opposite of the problem the product owner reported.

    So prose is a line long enough to be a sentence *and* punctuated like one. A fragment
    strung together with middots is data wearing a lot of characters."""
    return len(t) >= MIN_SENTENCE and (". " in t or t.rstrip().endswith("."))

# Some screens exist in order to explain. A consent screen that does not say what saying no
# costs you is not a shorter screen, it is a worse one; the same is true of the screen that
# deletes an account, the one that stops an MRI, and the one that says who was rung about a
# critical potassium. Holding those to the same budget as a booking screen would cut exactly
# the sentences the product cannot afford to lose, so they get a wider one — and they are
# named here individually, so that "this screen is special" stays a decision somebody made
# rather than a habit.
EXPLAINS = {
    # consent, revocation and what cannot be undone
    "R11-approve", "R12-shared", "R5-share", "R6-access", "P8-privacy",
    "P9-delete", "P9b-delete-confirm", "C13-link", "C14-consent", "C15-links",
    # safety: a value that can kill somebody, and a scanner that can injure them
    "K10-critical", "D15-critical", "F7-critical", "D17-prepare",
    # the rules that make a shared record safe to hand around a hospital
    "C7-roles", "F3-compliance", "C7-sign", "S5-undertaking", "E7-ext-notice",
}
WIDE = 1150


def prose_of(path):
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    s = FIELD.sub("", s)
    out = [html.unescape(t).strip() for t in TXT.findall(s)]
    return [p for p in out if is_prose(p)]


def budget_for(bundle, screen):
    return WIDE if screen in EXPLAINS else BUDGET[bundle]


def screens(bundle):
    """Desktop frames only. A mobile hub re-uses the same strings, so counting both would
    double every number and change nothing about which screen is worst."""
    d = os.path.join(ROOT, "figma", "medra-" + bundle)
    if not os.path.isdir(d):
        return
    for fn in sorted(os.listdir(d)):
        if fn.endswith("-d.jsx"):
            yield fn[:-6], os.path.join(d, fn)


def report(bundles=None, verbose=False, top=25):
    bundles = bundles or list(BUDGET)
    rows, over = [], []
    for b in bundles:
        for name, path in screens(b):
            p = prose_of(path)
            n = sum(len(x) for x in p)
            rows.append((b, name, n, p))
            if n > budget_for(b, name):
                over.append((b, name, n, p))
    if not rows:
        print("no frames found — build first")
        return 1
    over.sort(key=lambda r: -(r[2] - budget_for(r[0], r[1])))
    total = sum(r[2] for r in rows)
    excess = sum(r[2] - budget_for(r[0], r[1]) for r in over)
    print(f"PROSE BUDGET  {len(rows)} screens · {len(over)} over · "
          f"{total:,} characters, {excess:,} of them over budget")
    for b, name, n, p in over[:top]:
        print(f"  {b:<7}{name:<24}{n:>6}  (+{n - budget_for(b, name)})")
        if verbose:
            for line in sorted(p, key=len, reverse=True)[:4]:
                print(f"          {len(line):>4}  {line[:96]}")
    if len(over) > top:
        print(f"  … and {len(over) - top} more")
    if not over:
        print("  every screen within budget ✓")
    return 1 if over else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sys.exit(report(args or None, verbose="-v" in sys.argv))
