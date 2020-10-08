#! /bin/bash

cd "$(dirname "$0")" || exit

rm -f ./*.ttf

#java -jar ./bin/BitsNPicas.jar convertbitmap -f ttf -o ./zpix.ttf ../src/zpix.bdf
java -jar ./bin/BitsNPicas.jar convertbitmap -f ttf -o ./zpix.ttf ../src/zpix.sfd

# ./minify.py

mv -f ./zpix.ttf ../dist/zpix.ttf