---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# The server

The page at <https://menpo.github.io/landmarker.io/> keeps no data: your assets and landmarks live on a **server** that you run. `landmarkerio-server` is
that server, built on Menpo. It serves a folder of images or meshes, and writes the landmarks back next to them. This page describes landmarkerio-server {{ landmarkerio_server_version }}.

## Install

```bash
pip install landmarkerio-server            # images
pip install "landmarkerio-server[mesh]"    # also meshes (adds menpo3d)
```

It needs Python 3.10 or newer and Menpo 0.12 or newer, which are pure Python.

## Run

To annotate a folder of images, or of meshes:

```bash
lmio image ./path_to_images
lmio mesh ./path_to_meshes
```

and open <https://menpo.github.io/landmarker.io/?server=http://localhost:5000>. Use `-p` for another port, `-r` to search folders recursively, and `-t` to give a folder of
[templates](specifications.md). Without one, the `ibug68` template that ships with the package is used.

The options of the command, as the installed version has them:

```{code-cell} ipython3
:tags: [remove-input]

import subprocess
import sys

result = subprocess.run([sys.executable, "-m", "landmarkerio.scripts.lmio", "--help"],
                        capture_output=True, text=True, check=True)
print(result.stdout)
```

## What it keeps

The first time `lmio` sees a folder it makes a cache of web-sized textures and thumbnails (a temporary folder, or `--cache DIR` to keep it between runs).
The landmarks are saved as `.ljson` files **next to the assets**: `face_01.png` gets `face_01.ljson`. Delete the cache when you are done; the landmarks stay with your data.

`lmioconvert` rewrites old LJSON files in the current format, and `lmiocache` and `lmioserve` split `lmio` in two (build the cache once, then serve it with the landmarks
in another folder and, if you want it, HTTP basic authentication).

## Reaching it from the hosted page

The page is served over https and your server is not. Browsers allow exactly this case: a server on your own machine (`localhost`, `127.0.0.1`). Chrome may ask you to
allow the page to reach devices on your local network, and the server answers the request that goes with it. For a server on another machine give it an https address, or
tunnel its port with SSH (`ssh -L 5000:localhost:5000 host`) and use `localhost`.

## The API

The page talks to the server with a small REST API under `/api/v2/`: `mode`, `collections`, `templates`, `images`, `meshes`, `textures/<id>`, `thumbnails/<id>`, and
`landmarks/<id>/<template>` (GET and PUT). Any server that implements it works with the page, and the [specifications](specifications.md) describe the files.
