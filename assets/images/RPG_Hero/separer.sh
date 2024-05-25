#!/bin/bash

SPRITESHEET_PATH="attack_right_40x40.png"

OUTPUT_BASE=""

WIDTH=40
HEIGHT=40

COLUMNS=7
ROWS=1

INDEX=0

for ((row=0; row<$ROWS; row++)); do
  for ((col=0; col<$COLUMNS; col++)); do
    X=$(($col*$WIDTH))
    Y=$(($row*$HEIGHT))

    OUTPUT_FILE="${OUTPUT_BASE}$(printf "%02d" $INDEX).png"

    convert "$SPRITESHEET_PATH" -crop ${WIDTH}x${HEIGHT}+${X}+${Y} "$OUTPUT_FILE"

    INDEX=$((INDEX+1))
  done
done

echo "Images séparées avec succès."
