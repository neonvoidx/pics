#!/bin/bash

# Check for folder argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

folder="$1"

# Loop through all jpg and png images in the specified folder
shopt -s nullglob
for img in "$folder"/*.jpg "$folder"/*.jpeg "$folder"/*.png; do
  # Skip if no files match
  [ -e "$img" ] || continue

  # Get image dimensions
  read width height < <(identify -format "%w %h" "$img")

  # Only resize if both dimensions exceed the target
  if [ "$width" -gt 3440 ] && [ "$height" -gt 1440 ]; then
    # Calculate aspect ratio for logging
    aspect_ratio=$(awk "BEGIN { printf \"%.5f\", $width/$height }")
    # Calculate scale factors
    width_scale=$(awk "BEGIN { print 3440/$width }")
    height_scale=$(awk "BEGIN { print 1440/$height }")
    # Use the smaller scale to fit within both limits
    scale=$(awk "BEGIN { if ($width_scale < $height_scale) print $width_scale; else print $height_scale }")
    new_width=$(awk "BEGIN { printf \"%d\", $width*$scale }")
    new_height=$(awk "BEGIN { printf \"%d\", $height*$scale }")
    # Only resize if neither dimension will go below the limit
    if [ "$new_width" -ge 3440 ] && [ "$new_height" -ge 1440 ]; then
      # Try to match common aspect ratios
      common_ratio="unknown"
      if awk "BEGIN { exit !($aspect_ratio > 1.76 && $aspect_ratio < 1.79) }"; then
        common_ratio="16:9"
      elif awk "BEGIN { exit !($aspect_ratio > 2.32 && $aspect_ratio < 2.4) }"; then
        common_ratio="21:9"
      elif awk "BEGIN { exit !($aspect_ratio > 1.32 && $aspect_ratio < 1.35) }"; then
        common_ratio="4:3"
      elif awk "BEGIN { exit !($aspect_ratio > 1.49 && $aspect_ratio < 1.51) }"; then
        common_ratio="3:2"
      fi
      magick "$img" -resize "3440x1440\>" "$img"
      # Get new dimensions after resizing
      read actual_width actual_height < <(identify -format "%w %h" "$img")
      echo "Resized $img: ${width}x${height} -> ${actual_width}x${actual_height} (ratio: $aspect_ratio, approx $common_ratio)"
    else
      echo "Skipping $img: resizing would reduce below limits (would become ${new_width}x${new_height})"
    fi
  fi
done
