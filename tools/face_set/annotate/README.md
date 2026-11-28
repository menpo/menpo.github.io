# Correcting the landmarks by hand

The original [landmarker.io](https://github.com/menpo/landmarker.io) web client, with a small server
(`lmio_lite.py`, standard library plus Pillow and PyYAML) that replaces `landmarkerio-server`, which needs
`menpo<0.12` and the retired hosted site. It serves a folder of images that have `.pts` files and writes the
corrected landmarks back to those `.pts` files; the first time an image is saved the file it replaces is kept as
`NAME.original.pts`.

```
./fetch_client.sh                    # once: downloads the prebuilt client
python lmio_lite.py /path/to/faces   # then open http://127.0.0.1:5000/?server=http://127.0.0.1:5000
```

Drag a point to move it, press SAVE (or switch on AUTOSAVE), then go to the next image with the arrows. The `.pts`
files are in the layout of `menpo.io.import_landmark_file` (68 iBUG points, pixels counted from 1).

The client talks `/api/v2/` (mode, collections, templates, images, textures, thumbnails, landmarks). Meshes are not served.
The client sends and receives points as `[y, x]`.
