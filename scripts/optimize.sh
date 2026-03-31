#!/bin/bash
INPUT=$1
OUTPUT="../processed/$(basename $INPUT)"

mkdir -p ../processed

convert "$INPUT" -auto-orient -resize 1920x1920 -quality 85 "$OUTPUT"

echo "Optimized -> $OUTPUT"
