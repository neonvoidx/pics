#!/bin/bash

# Usage: ./log_ratios.sh <folder>
# Prints: filename width height aspect_ratio nearest_common_ratio

if [ $# -ne 1 ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

folder="$1"
if [ ! -d "$folder" ]; then
  echo "Error: $folder is not a directory"
  exit 1
fi

# List of common aspect ratios (name, width, height)
declare -a RATIOS=(
  "16:9 16 9"
  "4:3 4 3"
  "3:2 3 2"
  "1:1 1 1"
  "5:4 5 4"
  "21:9 21 9"
)

printf "%-35s %6s %6s %8s %10s\n" "Filename" "Width" "Height" "Aspect" "Nearest"

for file in "$folder"/*; do
  # Check if file is a regular file
  [ -f "$file" ] || continue
  # Use identify to get image dimensions
  dims=$(identify -format "%w %h" "$file" 2>/dev/null)
  if [ -z "$dims" ]; then
    continue
  fi
  width=$(echo $dims | cut -d' ' -f1)
  height=$(echo $dims | cut -d' ' -f2)
  if [ "$height" -eq 0 ]; then
    continue
  fi
  aspect=$(awk -v w="$width" -v h="$height" 'BEGIN { printf "%.4f", w/h }')

  # Find nearest common aspect ratio
  min_diff=1000
  nearest=""
  for ratio in "${RATIOS[@]}"; do
    name=$(echo $ratio | cut -d' ' -f1)
    rw=$(echo $ratio | cut -d' ' -f2)
    rh=$(echo $ratio | cut -d' ' -f3)
    r=$(awk -v w="$rw" -v h="$rh" 'BEGIN { printf "%.4f", w/h }')
    diff=$(awk -v a="$aspect" -v r="$r" 'BEGIN { d=(a-r); if(d<0)d=-d; print d }')
    cmp=$(awk -v d="$diff" -v m="$min_diff" 'BEGIN { print (d<m)?1:0 }')
    if [ "$cmp" -eq 1 ]; then
      min_diff=$diff
      nearest=$name
    fi
  done
  fname=$(basename "$file")
  printf "%-35s %6s %6s %8s %10s\n" "$fname" "$width" "$height" "$aspect" "$nearest"

done
