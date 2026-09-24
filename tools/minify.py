#!/usr/bin/env fontforge
# -*- mode: python; coding: utf-8 -*-

# install fontforge for macOS
# brew install fontforge
#
# Re-generates ./zpix.ttf with fontforge (shrinks the BitsNPicas output).
# NOTE: this step truncates the OS/2 table while keeping the version 5
# header; tools/fix-os2.py repairs that right after (see tools/build.sh).
# This script intentionally depends only on fontforge, not on bdflib.

import fontforge
import os


def main():
    path = "./zpix.ttf"
    print("[minify] opening %s (%d bytes)" % (path, os.path.getsize(path)))
    baseFont = fontforge.open(path)

    # AutoTrace all glyphs, add extrema and simplify.
    # baseFont.selection.all()
    # baseFont.autoTrace()
    # baseFont.addExtrema()
    # baseFont.simplify()
    baseFont.generate("zpix.ttf", "ttf")
    baseFont.close()

    print("[minify] done: %s (%d bytes)" % (path, os.path.getsize(path)))


main()
