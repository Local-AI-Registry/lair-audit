#!/bin/bash
# Rebuilds ai-audit/index.html (and the dark map) from the template + business files.
# Add a new business: put its files in biz/ and add biz/<slug>.json to the list below.
cd "$(dirname "$0")"
python3 darkmap.py mapbg.html ../map-bg.html || exit 1
python3 hudbuild3.py ../index.html quiktox \
  biz/spiritleaf-sherwood-park.json biz/spiritleaf-salisbury.json \
  biz/elevate-cannabis-belton.json biz/key-cannabis-kc-north.json \
  biz/bridge-city-east-dubuque.json biz/esthetixmd-bend.json \
  biz/hello-smooth.json biz/illume-med-spa.json
# Sales-call version (ai-audit/v2/): same businesses, built from sales.tpl.html. Test: tests/serve.sh node tests/v2.js <slugs>
python3 sales.py ../v2/index.html \
  biz/spiritleaf-sherwood-park.json biz/spiritleaf-salisbury.json \
  biz/elevate-cannabis-belton.json biz/key-cannabis-kc-north.json \
  biz/bridge-city-east-dubuque.json biz/esthetixmd-bend.json \
  biz/hello-smooth.json biz/illume-med-spa.json
