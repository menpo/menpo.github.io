#!/bin/sh
# Download the prebuilt landmarker.io web client (the gh-pages branch of menpo/landmarker.io, BSD-3-Clause) into ./static
set -e
cd "$(dirname "$0")"
mkdir -p static
base=https://raw.githubusercontent.com/menpo/landmarker.io/gh-pages
for f in index.html bundle.js manifest.json favicon-16x16.png favicon-32x32.png favicon-96x96.png favicon-194x194.png apple-touch-icon.png android-chrome-192x192.png mstile-144x144.png; do
  curl -fsSL "$base/$f" -o "static/$f"
done
echo "client in $(pwd)/static"
