#!/usr/bin/env bash
# Pan each 2160x1920 board left -> right into a 1080x1920 clip, then concatenate.
# For a film in this repo you do NOT need this: `film init` gives a board
# `move: columns` and `cross:` puts the pan on the words. This is the
# standalone route (a board video with no film around it), kept from the plan.
# Usage: bash slides/boards/make_pans.sh projects/<Film>/boards [hold_A=3] [pan=12] [hold_B=3] [fps=30]
set -euo pipefail
VD="$1"; A="${2:-3}"; P="${3:-12}"; B="${4:-3}"; FPS="${5:-30}"
T=$(awk "BEGIN{print $A+$P+$B}")
mkdir -p "$VD/mp4"; LIST="$VD/mp4/list.txt"; : > "$LIST"
for png in "$VD"/png/[0-9][0-9]_*.png; do
  name=$(basename "$png" .png)
  ffmpeg -y -loglevel error -loop 1 -framerate "$FPS" -t "$T" -i "$png" \
    -vf "crop=1080:1920:x='if(lt(t,$A),0,if(lt(t,$A+$P),1080*(1-cos(PI*(t-$A)/$P))/2,1080))':y=0,format=yuv420p" \
    -c:v libx264 -preset slow -crf 18 -r "$FPS" "$VD/mp4/$name.mp4"
  echo "file '$name.mp4'" >> "$LIST"; echo "clip $name (${T}s)"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy "$VD/mp4/all_slides.mp4"
echo "done: $VD/mp4/all_slides.mp4"
