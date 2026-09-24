#!/usr/bin/env python3
"""Fix wrong glyph names left by BitsNPicas (needs fontTools).

BitsNPicas assigns its own PostScript names, some of which clash with the
Adobe Glyph List and make fontforge complain on open/generate::

    hyphen         -> U+00AD (should be U+002D; U+00AD is `softhyphen`)
    mu             -> U+03BC (should be U+00B5; U+03BC is `mugreek`)
    fraction       -> U+2215 (should be U+2044; U+2215 is `divisionslash`)
    periodcentered -> U+2219 (should be U+00B7; U+2219 is `bulletoperator`)
    Delta          -> U+0394 (fontforge expects `Deltagreek`, U+2206 is `Delta`)
    Omega          -> U+03A9 (fontforge expects `Omegagreek`, U+2126 is `Omega`)

(BitsNPicas disambiguates duplicates with a `.1` suffix, e.g. `hyphen.1`
for U+00AD, but fontforge validates the base name and still warns.)

This script renames by codepoint, so the shipped font opens warning-free.
Run from ``tools/``, after ``minify.py``::

    python3 ./fix-glyph-names.py ./zpix.ttf

Requires ``pip install fonttools``. Exit code 0 = fixed or already fine,
1 = collision / unfixable (fail the build).
"""

import sys

# codepoint -> correct glyph name
RENAME = {
    0x00AD: "softhyphen",
    0x0394: "Deltagreek",
    0x03A9: "Omegagreek",
    0x03BC: "mugreek",
    0x2215: "divisionslash",
    0x2219: "bulletoperator",
}


def fail(message):
    print("[fix-names] ERROR: %s" % message)
    return 1


def main(path):
    from fontTools.ttLib import TTFont

    font = TTFont(path)
    cmap = font.getBestCmap()
    order = font.getGlyphOrder()
    names = set(order)
    rename_map = {}  # old name -> new name
    changed = 0

    for codepoint, correct in sorted(RENAME.items()):
        current = cmap.get(codepoint)
        if current is None:
            print(
                "[fix-names] U+%04X: no glyph mapped, want `%s`, skipping"
                % (codepoint, correct)
            )
            continue
        if current == correct:
            print("[fix-names] U+%04X: already `%s`, nothing to do" % (codepoint, correct))
            continue
        if correct in names:
            return fail(
                "U+%04X `%s` -> `%s` blocked: `%s` already used by another glyph"
                % (codepoint, current, correct, correct)
            )
        print("[fix-names] U+%04X: `%s` -> `%s`" % (codepoint, current, correct))
        order[order.index(current)] = correct
        rename_map[current] = correct
        names.discard(current)
        names.add(correct)
        changed += 1

    if changed:
        font.setGlyphOrder(order)
        # cmap subtables reference glyphs by name; keep them in sync,
        # otherwise saving fails with KeyError on the old names.
        for subtable in font["cmap"].tables:
            subtable.cmap = {
                cp: rename_map.get(name, name) for cp, name in subtable.cmap.items()
            }
        font.save(path)
        print("[fix-names] done: %s saved (%d renamed)" % (path, changed))
    else:
        print("[fix-names] done: %s already clean" % path)

    # Verify from disk.
    check = TTFont(path)
    check_cmap = check.getBestCmap()
    bad = [
        "U+%04X is `%s`, want `%s`" % (cp, check_cmap.get(cp), name)
        for cp, name in sorted(RENAME.items())
        if check_cmap.get(cp) not in (None, name)
    ]
    check.close()
    if bad:
        return fail("verification failed: %s" % "; ".join(bad))
    print("[fix-names] verify: all mapped names correct")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 fix-glyph-names.py <font.ttf>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
