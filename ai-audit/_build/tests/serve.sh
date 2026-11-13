#!/bin/bash
# Serves the repo at http://localhost:9314 while a test runs. Usage: tests/serve.sh node tests/audt.js
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
mkdir -p "$(dirname "$0")/shots"
python3 -m http.server 9314 -d "$ROOT" >/dev/null 2>&1 & P=$!
sleep 1.2; "$@"; R=$?; kill $P 2>/dev/null; exit $R
