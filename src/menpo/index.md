<link rel="stylesheet" type="text/css"  href="../menpostyle.css">

<div style="display: flex; align-items: center; flex-direction: column;">
  <img src="../../logo/menpo.png" alt="menpo" width="30%" style="display: flex;">
  </br>
  <div style="display: flex; align-items: center; justify-content: center; margin-top: 4px; margin-bottom: 20px">
    <a href="https://github.com/menpo/menpo" style="display: flex;">
      <img src="http://img.shields.io/github/release/menpo/menpo.svg?style=flat-square" alt="Github Release"/>
    </a>
    <a style="text-decoration: none; color: grey; margin: 5px 25px;" href="https://github.com/menpo/menpo">
      <button class="download_button">View on Github</button>
    </a>
    <a href="https://github.com/menpo/menpo/blob/master/LICENSE.txt" style="display: flex;">
      <img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/>
    </a>
  </div>
</div>

`menpo` is a Python package designed from the ground up to make importing, manipulating and visualizing image and mesh data as simple as possible.
Beyond it's elegant design, `menpo` has some unique characteristics that make it particlarly well suited to working with **annotated or landmarked** data:
```python
import menpo.io as mio
img = mio.import_image('foo.png')

if img.n_channels != 1:
  img = img.as_greyscale()

img.landmarks['face'] = mio.import_landmark_file('face.pts')

# objects return copies rather than mutating self, so we can chain calls
img = (img.crop_to_landmarks(group='face', boundary=10)
          .rescale_landmarks_to_diagonal_range(100, group='face'))

# now lets take an image feature...
from menpo.feature import fast_dsift
img = fast_dsift(img)

# ...and extract the vector of pixels contained in the
# convex hull of the face...
vector = img.as_masked().constrain_mask_to_landmarks(group='face').as_vector()

print(type(vector), vector.shape)
# output: <class 'numpy.ndarray'> (3801,)
```
`menpo` is the standard library of the Menpo Project, but due to it's simple dependencies and generic types and routines, is well suited as a **preprocessing library for many computer vision tasks**.

The following user guide is a general introduction to `menpo`, aiming to provide a bird's eye of `menpo`'s design.
It is also very helpful for understanding the main philosophy behind all the packages of the Menpo Project.
The contents of this user guide are:
1. [Introduction](introduction.md)
2. [Data Types](datatypes.md)
3. [Consistency](consistency.md)
4. [Vectorizing](vectorizing.md)
5. [Visualization](visualization.md)
