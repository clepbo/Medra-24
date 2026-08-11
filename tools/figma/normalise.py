#!/usr/bin/env python3
"""Normalise generated JSX before it is written to a bundle.

Two defects were being emitted at scale, both invisible in the source and both obvious the
moment the file is open in Figma. Each one had to be fixed by hand, per frame, by the designer.

1. **An empty frame keeps Figma's 100×100 default on whatever axis you did not set.**
   `<Frame grow={1} />` is a spacer — it means "push the next thing to the far end". It has no
   height, so Figma gives it 100, and a 34px-tall row becomes 100px tall with a hole in it.
   The same applies to `<Frame w={7} />` in a row (100 tall) and `<Frame h={12} />` in a
   column (100 wide). The fix is to fill the *cross* axis: a spacer should take the size of
   the row it sits in, never dictate it.

2. **Text in a centred container is still left-aligned inside its own box.** `items="center"`
   centres the text *node*; it does not centre the text *inside* the node. Where the node
   ends up wider than the glyphs — which is most of the time, because the renderer fills —
   the label reads as left-aligned in a visibly centred card. The specialty grid is the
   clearest case.

Both rules are structural, so they are applied to the tree rather than to the string: a tag is
only rewritten when its parent says so, and nothing else in the source is touched.

    from normalise import normalise
    jsx = normalise(jsx)
"""
import re

TAG = re.compile(r'<(/?)([A-Z][A-Za-z]*)((?:[^<>"]|"[^"]*")*?)(/?)>')

SELF_CLOSING = {"Icon", "Rect", "Ellipse", "Image"}


class Node:
    __slots__ = ("tag", "attrs", "start", "end", "attr_start", "attr_end", "children", "empty")

    def __init__(self, tag, attrs, start, end, attr_start, attr_end, empty):
        self.tag, self.attrs = tag, attrs
        self.start, self.end = start, end            # span of the opening tag
        self.attr_start, self.attr_end = attr_start, attr_end
        self.children = []
        self.empty = empty                            # self-closed, so it has no children


def parse(jsx):
    """A light DOM over the tag stream. Text between tags is ignored — every element we care
    about is an element, and leaving the source untouched between tags is the point."""
    root = Node("#root", "", 0, 0, 0, 0, False)
    stack = [root]
    for m in TAG.finditer(jsx):
        closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        if closing:
            if len(stack) > 1:
                stack.pop()
            continue
        # insert after the last real attribute character, not inside the trailing space
        attr_end = m.start(3) + len(attrs.rstrip())
        node = Node(tag, attrs, m.start(), m.end(),
                    m.start(3), attr_end, bool(selfclose) or tag in SELF_CLOSING)
        stack[-1].children.append(node)
        if not node.empty:
            stack.append(node)
    return root


def has(attrs, name):
    return re.search(r'(?:^|\s)' + name + r'=', attrs) is not None


def axis(node):
    """'row', 'col', or None if this frame is not an auto-layout container."""
    m = re.search(r'flex="(row|col)"', node.attrs)
    return m.group(1) if m else None


def normalise(jsx):
    root = parse(jsx)
    edits = []          # (position, text-to-insert)

    def walk(node):
        ax = axis(node)
        kids = node.children
        for kid in kids:
            if kid.tag == "Frame" and kid.empty and ax:
                # An empty frame must never dictate the cross-axis size of its parent. Fill it.
                # Guarded on having a sibling: a row made only of spacers would collapse.
                if len(kids) > 1:
                    cross = "h" if ax == "row" else "w"
                    if not has(kid.attrs, cross):
                        edits.append((kid.attr_end, f' {cross}="fill"'))
            elif kid.tag == "Text" and not has(kid.attrs, "align"):
                centred = (ax == "col" and 'items="center"' in node.attrs) or \
                          (ax == "row" and 'justify="center"' in node.attrs)
                if centred:
                    edits.append((kid.attr_end, ' align="center"'))
            if not kid.empty:
                walk(kid)

    walk(root)
    if not edits:
        return jsx
    out, last = [], 0
    for pos, text in sorted(edits):
        out.append(jsx[last:pos]); out.append(text); last = pos
    out.append(jsx[last:])
    return "".join(out)


def report(jsx):
    """(spacers fixed, text centred) — for the build summary."""
    before = jsx
    after = normalise(jsx)
    return (after.count('="fill" />') - before.count('="fill" />'),
            after.count(' align="center"') - before.count(' align="center"'))
