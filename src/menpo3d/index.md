<link rel="stylesheet" type="text/css"  href="../menpostyle.css">

<div style="display: flex; align-items: center; flex-direction: column;">
  <img src="../../logo/menpo3d.png" alt="menpo3d" width="30%" style="display: flex;">
  </br>
  <div style="display: flex; align-items: center; justify-content: center; margin-top: 4px; margin-bottom: 20px">
    <a href="https://github.com/menpo/menpo3d" style="display: flex;">
      <img src="http://img.shields.io/github/release/menpo/menpo3d.svg?style=flat-square" alt="Github Release"/>
    </a>
    <a style="text-decoration: none; color: grey; margin: 5px 25px;" href="https://github.com/menpo/menpo3d">
      <button class="download_button">View on Github</button>
    </a>
    <a href="https://github.com/menpo/menpo3d/blob/master/LICENSE.txt" style="display: flex;">
      <img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/>
    </a>
  </div>
</div>

`menpo3d` makes manipulating 3D mesh data a simple task. In particular, this package provides the ability to import, visualize and rasterize 3D meshes. Although 3D meshes can be created within the main [`menpo`](../menpo/index.md) package, this package adds the real functionality for working with 3D data.


Visualizing 3D objects
----------------------
menpo3d adds support for viewing 3D objects through
[Mayavi](http://code.enthought.com/projects/mayavi/), which is based on VTK.
One of the main reasons menpo3d is a seperate project to the menpo core
library is to isolate the more complex dependencies that this brings to the
project. 3D visualization is not yet supported in the browser, so we rely on
platform-specific viewing mechanisms like `QT` or `WX`. It also limits `menpo3d` to
be Python 2 only, as `VTK` does not yet support Python 3.

In order to view 3D items you will need to first use the `%matplotlib qt`
IPython magic command to set up `QT` for rendering (you do this instead of
`%matplotlib inline` which is what is needed for using the usual Menpo
Widgets). As a complete example, to view a mesh in `IPython` you
would run something like:
```python
import menpo3d
mesh = menpo3d.io.import_builtin_asset('james.obj')
```
```python
%matplotlib qt
mesh.view()
```
 If you are on Linux and get an error like:
```
ValueError: API 'QString' has already been set to version 1
```
Try adding the following to your `.bashrc` file:
```bash
export QT_API=pyqt
export ETS_TOOLKIT=qt4
```
Open a new terminal and re-run IPython notebook in here, this should fix the issue.

If you are running Windows and recieve this error, try:
```cmd
set QT_API=pyqt
set ETS_TOOLKIT=qt4
```
Alternatively, try installing wxPython:
```cmd
conda install wxpython
```
and using `%matplotlib wx`.
