"""OS/2 table regression test (fontTools subset breakage).

Background: shipped ``zpix.ttf`` declares OS/2 version 5 but only stores
96 bytes (a version 4 length body, missing ``usLowerOpticalPointSize`` /
``usUpperOpticalPointSize``). Any fontTools code path that touches OS/2
(``TTFont`` eager load, ``font["OS/2"]``, ``fontTools.subset``) dies with::

    struct.error: unpack requires a buffer of 22 bytes

Root cause: ``tools/minify.py`` re-generates the BitsNPicas output with
fontforge, which truncates the table while keeping the version 5 header.

Run::

    python3 __tests__/test_os2_table_regression.py
    # or: pytest __tests__/test_os2_table_regression.py
    # or against another file: ZPIX_TTF=/path/to/zpix.ttf python3 ...

Fonts under ``__tests__/__IGNORE_GIT_FILES__/`` are local-only fixtures
(git-ignored) and are all checked when present.

Version matrix (measured 2026-09-24, fontTools 4.60.2)::

    GOOD (OS/2 v5 / 100 bytes, parses + subsets fine):
      v3.1.8 ~ v3.1.13 dist — minify.py crashed (no bdflib in the build
      env), so the raw BitsNPicas output shipped untouched.
    BAD (OS/2 v5 / 96 bytes, struct.error: unpack requires a buffer of
    22 bytes):
      v3.1.2 ~ v3.1.7 dist — minify.py ran (bdflib present) and fontforge
      truncated the table while keeping the v5 header.
      v3.2.0 release (CI) — same cause: the new workflow installs bdflib,
      so minify.py runs again. Fixed by tools/fix-os2.py in the pipeline.

Note: a file once named ``zpix-v3.1.11.ttf`` floating around was actually
the v3.2.0 release bytes (same MD5); the real v3.1.11 dist is GOOD.
"""

import glob
import os
import struct
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIR = os.path.join(REPO_ROOT, "__tests__", "__IGNORE_GIT_FILES__")


def find_fonts():
    """Local fixture fonts plus an optional ZPIX_TTF override."""
    paths = sorted(glob.glob(os.path.join(FIXTURE_DIR, "*.ttf")))
    override = os.environ.get("ZPIX_TTF", "")
    if override and os.path.isfile(override) and override not in paths:
        paths.append(override)
    dist_font = os.path.join(REPO_ROOT, "dist", "zpix.ttf")
    if os.path.isfile(dist_font) and dist_font not in paths:
        paths.append(dist_font)
    return paths


def read_os2_header(path):
    """Return (declared_version, table_length) without decompiling OS/2."""
    from fontTools.ttLib import TTFont

    font = TTFont(path, lazy=True)
    try:
        entry = font.reader.tables["OS/2"]
        font.reader.file.seek(entry.offset)
        data = font.reader.file.read(entry.length)
    finally:
        font.close()
    (version,) = struct.unpack(">H", data[:2])
    return version, len(data)


# Minimum OS/2 body length per version (spec + fontTools O_S_2f_2.py):
# v0 = 78, v1 = 86, v2/v3/v4 = 96, v5 = 100.
MIN_LENGTH_FOR_VERSION = {0: 78, 1: 86, 2: 96, 3: 96, 4: 96, 5: 100}

# Fixtures with a known-truncated OS/2 (v5 header, 96-byte body).
# Kept here so failures point at the matrix in the docstring above.
KNOWN_BROKEN = frozenset(
    "zpix-v3.1.%d-dist.ttf" % v for v in range(2, 8)
) | frozenset(["zpix-v3.2.0-release.ttf"])

FONT_PATHS = find_fonts()


@unittest.skipIf(not FONT_PATHS, "no .ttf fixture found")
class TestOS2TableRegression(unittest.TestCase):
    def test_os2_version_readable(self):
        """Every fixture font's OS/2 must decompile (no struct.error)."""
        from fontTools.ttLib import TTFont

        for path in FONT_PATHS:
            with self.subTest(font=os.path.basename(path)):
                font = TTFont(path)
                try:
                    self.assertIn(font["OS/2"].version, (0, 1, 2, 3, 4, 5))
                finally:
                    font.close()

    def test_os2_length_matches_version(self):
        """Declared OS/2 version must fit in the stored table length."""
        for path in FONT_PATHS:
            with self.subTest(font=os.path.basename(path)):
                version, length = read_os2_header(path)
                self.assertIn(version, MIN_LENGTH_FOR_VERSION)
                hint = (
                    " (known-broken fixture, see version matrix in docstring)"
                    if os.path.basename(path) in KNOWN_BROKEN
                    else ""
                )
                self.assertGreaterEqual(
                    length,
                    MIN_LENGTH_FOR_VERSION[version],
                    "%s: OS/2 declares version %d (needs >= %d bytes)"
                    " but stores %d bytes%s"
                    % (
                        os.path.basename(path),
                        version,
                        MIN_LENGTH_FOR_VERSION[version],
                        length,
                        hint,
                    ),
                )


if __name__ == "__main__":
    if not FONT_PATHS:
        print("SKIP: no .ttf fixture found")
        sys.exit(0)
    print("Testing fonts:")
    for path in FONT_PATHS:
        print("  - %s" % path)
    unittest.main(argv=[sys.argv[0], "-v"])
