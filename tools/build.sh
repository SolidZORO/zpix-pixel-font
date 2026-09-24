#! /bin/bash

cd "$(dirname "$0")" || exit

rm -f ./*.ttf
java -jar ./bin/BitsNPicas-2.2.2.jar convertbitmap -f ttf -o ./zpix.ttf ../src/zpix.sfd

# minify has a bug for web, OTS parsing error: OS/2: Failed to parse table
# so I'm going to convert woff2 here
# `ttf2woff2` is a npm module, RUN `npm i -g ttf2woff2` install
cat < ./zpix.ttf | ttf2woff2 > ../dist/zpix.woff2

./minify.py
# Rename glyphs misnamed by BitsNPicas (hyphen/mu/fraction/periodcentered/
# Delta/Omega at the wrong codepoints), otherwise fontforge warns on open.
python3 ./fix-glyph-names.py ./zpix.ttf || exit 1
# Fix truncated OS/2 v5 header (fontforge writes 96 bytes but declares v5),
# otherwise fontTools fails with "struct.error: unpack requires a buffer of 22 bytes".
python3 ./fix-os2.py ./zpix.ttf || exit 1
mv -f ./zpix.ttf ../dist/zpix.ttf


rm -f ./*.bdf
java -jar ./bin/BitsNPicas-2.2.2.jar convertbitmap -f bdf -o ./zpix.bdf ../src/zpix.sfd
mv -f ./zpix.bdf ../dist/zpix.bdf
