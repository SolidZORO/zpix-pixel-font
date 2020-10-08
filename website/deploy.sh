#! /bin/bash

cd "$(dirname "$0")" || exit

vercel --prod
