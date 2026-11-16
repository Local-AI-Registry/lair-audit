#!/bin/bash
# Rebuilds ai-audit/index.html (and the dark map) from the template + business files.
# Add a new business: put its files in biz/ and add biz/<slug>.json to the list below.
cd "$(dirname "$0")"
python3 darkmap.py mapbg.html ../map-bg.html || exit 1
python3 hudbuild3.py ../classic.html quiktox \
  biz/spiritleaf-sherwood-park.json biz/spiritleaf-salisbury.json \
  biz/elevate-cannabis-belton.json biz/key-cannabis-kc-north.json \
  biz/bridge-city-east-dubuque.json biz/esthetixmd-bend.json \
  biz/hello-smooth.json biz/illume-med-spa.json
# Main page (ai-audit/index.html): the sales-call version, built from sales.tpl.html. The older version builds to classic.html. Test: tests/serve.sh node tests/v2.js <slugs>
python3 sales.py ../index.html \
  biz/spiritleaf-sherwood-park.json biz/spiritleaf-salisbury.json \
  biz/elevate-cannabis-belton.json biz/key-cannabis-kc-north.json \
  biz/bridge-city-east-dubuque.json biz/esthetixmd-bend.json \
  biz/hello-smooth.json biz/illume-med-spa.json
