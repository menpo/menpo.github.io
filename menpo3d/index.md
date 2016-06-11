<center>
  <img src="../../logo/menpo3d.png" alt="menpo3d" width="30%">
  </br>
  </br>
  <a href="http://github.com/menpo/menpo3d"><img src="http://img.shields.io/github/release/menpo/menpo3d.svg" alt="Github Release"/></a>
  <a href="https://github.com/menpo/menpo3d/blob/master/LICENSE.txt"><img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/></a>
  <img src="https://img.shields.io/badge/Python-2.7-green.svg" alt="Python 2.7 Support"/>
  <iframe src="https://ghbtns.com/github-btn.html?user=menpo&repo=menpo3d&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>
  </br>
</center>

A library inside the Menpo Project that makes manipulating 3D mesh data a simple task. In particular, this project provides the ability to import, visualize and rasterize 3D meshes. Although 3D meshes can be created within the main [`menpo`](../menpo/index.md) package, this package adds the real functionality for working with 3D data.


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
