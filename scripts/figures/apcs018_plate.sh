#!/bin/zsh
# Build the apcs018 plate: python → plate018.html → headless Chrome → PNG.
#
#   zsh scripts/figures/apcs018_plate.sh
#
# `screenshot --full` is what pins the output to the authored canvas size; the
# viewport setting does not, and a plain `screenshot` silently returns whatever
# the last viewport happened to be.
set -eu
HERE=${0:a:h}
trap 'rm -f "$HERE/plate018.html"' EXIT
ROOT=${HERE:h:h}
OUT=$ROOT/docs/public/assets/challenge/apcs018/圖一.png
export AGENT_BROWSER_SESSION=${AGENT_BROWSER_SESSION:-apcs018-fan-plate}

python3 "$HERE/apcs018_plate.py"
mkdir -p "${OUT:h}"
agent-browser open "file://$HERE/plate018.html" >/dev/null
agent-browser wait 1200 >/dev/null
agent-browser screenshot --full "$OUT" >/dev/null
python3 -c "
import os, sys
from PIL import Image
p = sys.argv[1]
im = Image.open(p)
print('%s  %dx%d  %d KB' % (os.path.basename(p), im.size[0], im.size[1], os.path.getsize(p)//1024))
if im.size != (1280, 2716):
    raise SystemExit('unexpected canvas size %r — screenshot did not honour --full' % (im.size,))
" "$OUT"
rm -f "$HERE/plate018.html"
