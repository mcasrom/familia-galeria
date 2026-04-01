#!/bin/bash

FILE=$1
TAGS=$2

cd "$(dirname "$0")"

./optimize.sh "$FILE"
python3 thumbs.py
./sync_images.sh
python3 ingest.py "../processed/$(basename "$FILE" | sed 's/\.[^.]*$/.jpg/')" "$TAGS"

echo "✔ Pipeline completo ejecutado"
