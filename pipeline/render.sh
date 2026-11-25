#!/usr/bin/env bash
# Renders every shot listed in timeline.json into frames/<shot>/.
# Usage: ./render.sh            (all shots)    ./render.sh pit roman   (some shots)
# On Linux servers without a display, it wraps Blender in xvfb-run.
cd "$(dirname "$0")"
SHOTS=${@:-$(python3 -c "import json;print(' '.join(s['shot'] for s in json.load(open('timeline.json'))['shots']))")}
BL="blender"
if [ -z "$DISPLAY" ] && command -v xvfb-run >/dev/null; then BL="xvfb-run -a -s '-screen 0 1280x1024x24' blender"; fi
for s in $SHOTS; do
  rm -rf "frames/$s"
  echo "== $s"
  eval $BL -b -P scenes.py -- "$s" > "logs_$s.txt" 2>&1 || echo "FAILED $s (see logs_$s.txt)"
done
echo DONE
