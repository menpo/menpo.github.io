---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.7
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Image Features

This notebook provides a guide on how to extract features from an image. The contents of the notebook are:

1. Dense Scale-Invariant Feature Transform (**SIFT**) ([D. G. Lowe, "Object recognition from local scale-invariant features", ICCV, 1999.](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=790410&tag=1))
2. Image Gradient Orientations (**IGO**) ([G. Tzimiropoulos, S. Zafeiriou and M. Pantic, "Subspace learning from image gradient orientations", TPAMI, 2012.](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6138864))
3. Edge Structures (**ES**) ([T. Cootes and C. Taylor, "On representing edge structure for model matching", CVPR, 2001.](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=990655))
4. **Daisy** ([E. Tola, V. Lepetit and P. Fua, "Daisy: An efficient dense descriptor applied to wide-baseline stereo", TPAMI, 2010.](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4815264))
5. Others

+++

Let's begin by importing the necessary packages:

```{code-cell}
%matplotlib inline
import menpo.io as mio
import matplotlib.pyplot as plt
```

As shown in the Image Basics tutorial, it is simple to import an image and crop it's mask to the landmark points.

```{code-cell}
breaking_bad = mio.import_builtin_asset.breakingbad_jpg()
breaking_bad = breaking_bad.as_masked()
breaking_bad = breaking_bad.crop_to_landmarks(boundary=20)
breaking_bad = breaking_bad.constrain_mask_to_landmarks()
breaking_bad.view(masked=False);
print(breaking_bad.mask)
```

The landmarks on the breaking bad image are given as:

```{code-cell}
breaking_bad.view_landmarks();
```

and the Breaking Bad image has 3 channels in total (it is an RGB image).

```{code-cell}
breaking_bad.view(channels='all');
```

# 2. Dense SIFT Features

+++

The Dense Scale-Invariant Feature Transform (SIFT) features are very similar to HOG with the difference that the orientations histograms are computed with respect to each point’s dominant orientation. We employ the VLFeat implementation of dsift. The SIFT features extraction is as simple as:

```{code-cell}
from menpo.feature import dsift

%time dsift_img = dsift(breaking_bad)
```

As you can see, even though they are very similar to HOG, it is actually much faster to compute them. Let' visualize all channels:

```{code-cell}
dsift_img.view(masked=False);
print(dsift)
```

# 3. IGO Features

+++

The IGO (Image Gradient Orientations) features concatenate the `cos` and `sin` of the gradient orientation angles for each image pixel. The `cos` and `sin` can be computed either on the orientation angles or on both the angle and double angle of the pixel orientations.

+++

## 3.1 Single angles

+++

Computing the orientation angle is as simple as:

```{code-cell}
from menpo.feature import igo

%time igo_img = igo(breaking_bad)
```

```{code-cell}
print(igo_img)
```

There are 6 channels total, a `sin` and a `cos` for for `RGB` channel

```{code-cell}
igo_img.view(channels='all');
```

### 3.2 Double angles

+++

IGOs only have one parameter, the `double_angles` flag. This parameter determines whether or not the double angle is also computed. The double angle is particularly useful for IGOs as it helps mitigate against the ambiguity of the sign of the angle.

```{code-cell}
from menpo.feature import double_igo

%time igo_img = double_igo(breaking_bad)
```

With `double_angle=True`, there are now 12 channels (the angle and double angle of each of the `RGB` channels).

```{code-cell}
igo_img.view(channels='all');
```

# 4. ES Features

+++

The ES (Edge Structure) feature provides a measure which captures the orientation of image edge structure at each pixel, together with an indication of how accurate the orientation estimate is. The accuracy belief measure penalizes the orientations in flat, noisy regions and favours the ones near strong edges. Here is an example:

```{code-cell}
from menpo.feature import es

%time es_img = es(breaking_bad)
```

```{code-cell}
es_img.view(channels=[0, 1]);
```

# 6. Daisy

+++

The Daisy descriptor is based on gradient orientation histograms. It is formulated in a way that allows for fast dense extraction which is useful for e.g. bag-of-features image representations. Note that we use the implementation of _scikit-image_.

```{code-cell}
from menpo.feature import daisy
```

```{code-cell}
%%time 

daisy_img = daisy(breaking_bad, normalization='daisy')
```

```{code-cell}
daisy_img.view_landmarks(channels=range(3));
```

Daisy features have several options, such as `step`

```{code-cell}
daisy(breaking_bad, step=2, verbose=True).view(channels=0, masked=False);
```

# 7. Others

+++

The `feature` package has also `gradient`. For example

```{code-cell}
from menpo.feature import gradient
```

```{code-cell}
%%time
gradient_img = gradient(breaking_bad);
```

```{code-cell}
gradient_img.view(channels=[0, 3]);
```

Moreover, there is the `no_op()` function that stands for _no operation_. This means that the input image will be returned untouched.
