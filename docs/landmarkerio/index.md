# landmarker.io

<div style="text-align: center">
  <img src="../_static/logo/landmarkerio.png" alt="landmarker.io" width="30%">
</div>

`landmarker.io` is a web app for annotating images and 3D meshes with landmarks, in the browser. It is how the training data of `menpofit` models gets made.

**It is live at <https://menpo.github.io/landmarker.io/>**: a static page, with nothing to install. Try it first in demo mode: [**open the demo**](https://menpo.github.io/landmarker.io/?server=demo) annotates a textured 3D head.

To annotate your own images or meshes, run the [server](server.md) on your machine and point the page at it:

```bash
pip install landmarkerio-server
lmio image ./my_images        # or: lmio mesh ./my_meshes
```

then open <https://menpo.github.io/landmarker.io/?server=http://localhost:5000>.

* [User guide](userguide.md): annotating, the sidebar, autosave, keyboard shortcuts.
* [Snap mode](snap_mode.md): selecting and moving landmarks.
* [The server](server.md): installing and running it, and what it keeps.
* [Specifications](specifications.md): the landmark (LJSON) and template formats.

The source of the app is [menpo/landmarker.io](https://github.com/menpo/landmarker.io) and of the server [menpo/landmarkerio-server](https://github.com/menpo/landmarkerio-server).

```{toctree}
:titlesonly:
:hidden:

User guide </landmarkerio/userguide>
Snap mode </landmarkerio/snap_mode>
The server </landmarkerio/server>
Specifications </landmarkerio/specifications>
```
