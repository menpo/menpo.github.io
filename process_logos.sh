#! /bin/bash
# Downsize the master logos to something more sensible
# Requires pngcrush and imagemagick
# e.g.
# macOS: brew install pngcrush imagemagick
# Ubuntu: sudo apt-get install pngcrush imagemagick
#
cd ./logo

for PHOTO_PATH in ./masters/*.png; do
    FILENAME=`basename $PHOTO_PATH`
    convert "$PHOTO_PATH" -resize "500>" "$FILENAME"
    pngcrush -ow $FILENAME
done
