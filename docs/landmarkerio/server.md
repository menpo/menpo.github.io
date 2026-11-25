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
# run as a module here; the installed command is called lmio
print(result.stdout.replace("lmio.py", "lmio"))
```

## What it keeps

The first time `lmio` sees a folder it makes a cache of web-sized textures and thumbnails (a temporary folder, or `--cache DIR` to keep it between runs).
The landmarks are saved as `.ljson` files **next to the assets**: `face_01.png` gets `face_01.ljson`. Delete the cache when you are done; the landmarks stay with your data.

`lmioconvert` rewrites old LJSON files in the current format, and `lmiocache` and `lmioserve` split `lmio` in two (build the cache once, then serve it with the landmarks
in another folder and, if you want it, HTTP basic authentication).

## Auto-fit: models that fit for you

```bash
pip install "landmarkerio-server[fit]"
lmio image ./my_images --fit fit.yml        # --fit alone: an AAM that learns from what you save
```

The server keeps one or more models and uses them to place landmarks: the **Fit…** panel of the [user guide](userguide.md) drives them. They are set in a YAML file, not on the command line:

```yaml
model: patch-aam          # a short name (below) or your own class: package.module:Class
options:                  # the arguments of the model
  patch_sizes: [15, 23]
initial_state: faces.pkl  # start from a model that was trained elsewhere: it fits before anything is labelled
save_state: learnt.pkl    # written after every update; use it as initial_state next time
learn_on_save: false      # learn from each image as it is saved (needs a model that can increment)
from_saved: true          # learn only from images saved through landmarker.io
min_images: 8             # saved images before a model is built from scratch
```

| short name | what it is |
| --- | --- |
| `patch-aam` (default) | menpofit `PatchAAM`: can build, and increment |
| `holistic-aam` | menpofit `HolisticAAM`: can build, and increment |

`max_shape_components` and `max_appearance_components` of the AAMs take a number, or a list with one per scale. Your own model is a subclass of `landmarkerio.fit.FitModel`; what the server offers follows from what it can do (it must have `fitter` and `fit`; `increment` allows learning as you save, `build` training from nothing, `initialize` fitting an image that has no landmarks).

**The model learns only from saved landmarks**, never from what it predicted: saving through landmarker.io is what marks an image as reviewed.

### Several models and a pre-fit

Give a list to use several models and choose between them: for instance a pretrained detector to start, then an AAM that learns from the first few images you correct, then that AAM on the rest of the frames of a video. Settings at the top are the defaults of every model, and the first is the one the panel opens with.

```yaml
learn_on_save: false
models:
  - name: detector                        # what you choose in landmarker.io
    model: mypackage.mediapipe:Landmarker # your own FitModel, trained elsewhere
    options: {path: face_landmarker.task}
  - name: aam
    model: patch-aam
prefit:                   # optional: fit the images that have no landmarks, up front
  model: detector
  template: ibug68        # the layout the landmarks are written in
  on_start: true
  chain: false            # true: start each image from the one before it (video frames)
  overwrite: false        # true: fit again the images that already have a proposal
```

The pre-fit keeps its result as **proposals**, in a `.prefit/<model>/` folder next to the images and never as saved files. landmarker.io shows a proposal as the landmarks of the image, and saving it, with or without changes, writes the real `.ljson` (reviewed, with `fitted_by` set to the model) and removes the proposal. Proposals are never counted as annotations and never trained on. MediaPipe is not built in: it is the worked example of a model of your own.

## Reaching it from the hosted page

The page is served over https and your server is not. Browsers allow exactly this case: a server on your own machine (`localhost`, `127.0.0.1`). Chrome may ask you to
allow the page to reach devices on your local network, and the server answers the request that goes with it. For a server on another machine give it an https address, or
tunnel its port with SSH (`ssh -L 5000:localhost:5000 host`) and use `localhost`.

## The API

The page talks to the server with a small REST API under `/api/v2/`: `mode`, `collections`, `templates`, `images`, `meshes`, `textures/<id>`, `thumbnails/<id>`, and
`landmarks/<id>/<template>` (GET and PUT), and `fit` for the models above (`GET /api/v2/fit` is the status of each). Any server that implements it works with the page, and the [specifications](specifications.md) describe the files.
