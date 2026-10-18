#!/bin/bash

SITE="sites/tolkien-fan-club"

python3 src/main.py "$SITE" "/"

echo "Starting server..."

cd "$SITE/docs" && python3 -m http.server 8888