#! /bin/bash

cd "$(dirname "$0")" || exit

rm -f ./*.ttf

java -jar ./bin/BitsNPicas.jar convertbitmap -f ttf -o ./zpix.ttf ../src/zpix.sfd
./minify.py
mv -f ./zpix.ttf ../dist/zpix.ttf


rm -f ./*.bdf

java -jar ./bin/BitsNPicas.jar convertbitmap -f bdf -o ./zpix.bdf ../src/zpix.sfd
mv -f ./zpix.bdf ../dist/zpix.bdf
