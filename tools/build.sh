#! /bin/bash

cd "$(dirname "$0")" || exit

rm -f ./*.ttf
java -jar ./bin/BitsNPicas.jar convertbitmap -f ttf -o ./zpix.ttf ../src/zpix.sfd

# minify has a bug for web, OTS parsing error: OS/2: Failed to parse table
# so I'm going to convert woff2 here
# `ttf2woff2` is a npm module, RUN `npm i -g ttf2woff2` install
cat < ./zpix.ttf | ttf2woff2 > ../website/zpix.woff2

./minify.py
mv -f ./zpix.ttf ../dist/zpix.ttf


rm -f ./*.bdf
java -jar ./bin/BitsNPicas.jar convertbitmap -f bdf -o ./zpix.bdf ../src/zpix.sfd
mv -f ./zpix.bdf ../dist/zpix.bdf
