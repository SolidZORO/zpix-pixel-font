#!/usr/bin/env fontforge
# -*- mode: python; coding: utf-8 -*-

from bdflib import reader
from bdflib import writer
import fontforge

baseFont = fontforge.open("./zpix.ttf")
print(' ')
print(' ')
print(baseFont)
print('------------')

# AutoTrace all glyphs, add extrema and simplify.
print('Processing...')
# baseFont.selection.all()
# baseFont.autoTrace()
# baseFont.addExtrema()
# baseFont.simplify()
baseFont.generate('zpix.ttf', 'ttf')
baseFont.close()

print(' ')
print('🚀 Done!')
print(' ')
