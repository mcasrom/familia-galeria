#!/bin/bash

FILE=$1
TAGS=$2

cd "$(dirname "$0")"

./optimize.sh "$FILE"
python3 thumbs.py
python3 ingest.py "../processed/$(basename $FILE)" "$TAGS"

echo "✔ Pipeline completo ejecutado"
