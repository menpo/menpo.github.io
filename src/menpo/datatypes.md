Data Types
==========

1. [Why have Menpo types - what's wrong with numpy arrays?](#why)
2. [Key Points](#keypoints)

---------------------------------------

### 1. Why have Menpo types - what's wrong with numpy arrays? {#why}
`menpo`'s data types are thin wrappers around `numpy` arrays. They give semantic meaning to the underlying array through providing clearly named and consistent properties. As an example let's take a look at `PointCloud`, `menpo`'s workhorse for spatial data. Construction requires a `numpy` array:

```python
import numpy as np
from menpo.shape import PointCloud

x = np.random.rand(3, 2)
pc = PointCloud(x)
```

It's natural to ask the question:

> Is this a collection of three 2D points, or two 3D points?

In `menpo`, you never do this - just look at the properties on the `PointCloud`:

```python
print("{} points".format(pc.n_points))
print("{} dimensions".format(pc.n_dims))
# Outputs:
# 3 points
# 2 dimensions
```

If we take a look at the properties we can see they are trivial:
```python
@property
def n_points(self):
    return self.points.shape[0]

@property
def n_dims(self):
    return self.points.shape[1]
```

Using these properties makes code much more readable in algorithms accepting `menpo`'s types.
Let's imagine a routine that does some operation on an image and a related point cloud. If it accepted `numpy` arrays, we might see something like this on the top line:
```python
def foo_arrays(x, img):
    # preallocate the result
    y = np.zeros(x.shape[1],
                 x.shape[2],
                 img.shape[-1])
    ...
```

On first glance, it is not at all apparent what `y`'s shape is semantically. Now let's take a look at the equivalent code using `menpo`'s types:
```python
def foo_menpo(pc, img):
    # preallocate the result
    y = np.zeros(pc.n_dims,
                 pc.n_points,
                 img.n_channels)
    ...
```

This time it's immediately apparent what `y`'s shape is. Although this is a somewhat contrived example, you will find this pattern applied consistently across `menpo`, and it aids greatly in keeping the code readable.


### 2. Key Points {#keypoints}
**Menpo types always store the underlying numpy array in an easy to access attribute.** For the `PointCloud` family it's `.points`. On `Image` and subclasses, it's `.pixels`.

**Menpo types store the minimal amount of data possible.** For the vast majority of Menpo types, the only data stored in the class is the single numpy array the type wraps. This makes it easy to reason about Menpo types - if you swap out the `.pixels` array on an `Image` instance for a new numpy array and `print(image.width)` you will get the correct answer for the new array, as all properties are computed from `.pixels`.

**Menpo types print really nicely.** If you are ever unsure what an object is, just `print()` it to get an immediate summary:
```python
print(img)
# 512W x 512H 2D Image with 3 channels
print(pointcloud)
# PointCloud: n_points: 68, n_dims: 2
```

**Importing assets though [`menpo.io`](http://docs.menpo.org/en/stable/api/menpo/io/index.html) will result in our data containers, not `numpy` arrays**. This means in a lot of situations you never need to remember the `menpo` conventions for ordering of array data - just ask for an image and you will get an `Image` object.

**Menpo types behave as immutable data containers**. Methods on Menpo types return modified copies rather than mutating self (and mutating the underlying numpy array). This encourages chaining together method calls on types, each method call returning a fresh instance with it's own numpy array.
```python
import menpo.io as mio
img = mio.import_builtin_asset.lenna_png()
img_resized = img.resize((200, 200))
# methods in Menpo return modified copies - so img is unchanged by the resize call.
print(img)
print(img_resized)
# Output:
# 512W x 512H 2D Image with 3 channels
# 200W x 200H 2D Image with 3 channels

# If you don't need the intermediate copies, just chain methods back-to-back:
greyscale_vector = img.as_greyscale().resize((200, 200)).as_vector()
print(greyscale_vector)
# Outputs:
# [ 0.63622375  0.63370722  0.61733637 ...,  0.37906707  0.39924645]
```
Good Menpo code feels functional and following this style makes it easy to write elegant bug free code. If you are worried about performance, don't be - Menpo is architected to be smart about avoiding redundent copies wherever possible. It does so by internally making use of `copy=False` keyword arguments that you will see on many methods and constructors when we know that a copy has already been performed so a second would be redundent. You can use this keyword argument yourself in performance-critical sections of code, but we strongly suggest you only do so after profiling shows that it would really be a performance win (the vast majority of times, it won't be).

**Menpo types perform sanity checks to help catch bugs**. As Menpo types are more structured, we can perform sanity checks in lots of cases and report nice clean error messages. Pro-tip: You can suppress these checks for extra performance with the `skip_checks=True` keyword argument. Again, you should rarely need this though - Menpo internally uses these escape hatches when it knows it's safe to do so to keep everything performant.
