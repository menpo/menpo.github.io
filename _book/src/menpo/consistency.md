Consistency
===========

`menpo` takes an opinionated stance on certain issues - one of which is establishing sensible rules for how to work with spatial data and image data in the same framework.

1. [Working with Images and PointClouds](#images_and_pointclouds)
2. [Our Approach](#approach)
3. [Key Points](#keypoints)

---------------------------------------

### 1. Working with Images and PointClouds {#images_and_pointclouds}
Let's start with a quiz - which of the following is correct?
<center>
  <img src="media/indexing.jpg" alt="Indexing quiz" style="width: 60%">
</center>

Most would answer **b** - images are indexed from the top left, with `x` going across and `y` going down.

Now another question - how do I access that pixel in the pixels array? :

```
a: lenna[30, 50]
b: lenna[50, 30]
```

The correct answer is **b** - pixels get stored in a `y`, `x` order so we have to flip the points to access the array.

As `menpo` blends together use of `PointClouds` and `Images` frequently this can cause a lot of confusion. You might create a `Translation` of `5` in the `y` direction as the following:
```python
t = menpo.transform.Translation([0, 5])
```

And then expect to use it to warp an image:
```python
img.warp_to(reference_shape, t)
```

and then some spatial data related to the image:
```python
t.apply(some_data)
```

Unfortunately the meaning of `y` in these two domains is different - some code would have to flip the order of applying the translation of the transform to an image, a potential cause of confusion.

The *worst* part about this is that once we go to voxel data (which `Image` largely supports, and will fully support in the future), a `z`-axis is added.

**There is one important caveat**, unfortunately. The **first axis of an image represents the channels**. Unlike in other software, such as Matlab, which follows the fortran convention of being column major, Python and other C-like languages generally conform to a row major order. Practically this means that if you want to iterate over each channel of an image, you need the memory layout to reflect this. This means you want the pixel data of each channel to be contiguous in memory. **For row major memory, this implies that the first axis should represent an iteration over the channel data.**

Now, as was mentioned, we want to drop all the swapping business. Therefore, forgiving that the **first axis indexes the channel data**, the following axes always match the spatial data. For example, The zeroth axis of the spatial data once more corresponds with the first axis (the first axis is *after the zeroth axis representing the channel data*) of the image data. Trying to keep track of these rules muddies an otherwise very simple concept.


### 2. Our Approach {#approach}
`menpo`'s solution to this problem is simple - **drop the insistence of calling axes `x`, `y`, and `z`**. Skipping the channel data, which represents the zeroth axis, the first axis of the pixel data is simply that - the first axis. It corresponds exactly with the zeroth axis on the point cloud. If you have an image with annotations provided the zeroth axis of the `PointCloud` representing the annotations will correspond with the first axis of the image. This rule makes working with images and spatial data simple -short you should never have to think about flipping axes in `menpo`.

It's natural to be concerned at this point that establishing such rules must make it really difficult ingest data which follows different conventions. This is incorrect - one of the biggest strengths of the [menpo.io](http://docs.menpo.org/en/stable/api/menpo/io/index.html) module is that each asset importer normalizes the format of the data to format `menpo`'s rules.


### 3. Key Points {#keypoints}
-   **Menpo is n-dimensional**. We try and avoid speaking of `x` and `y`, because there are many different conventions in use.
-   **The IO module ensures that different data formats are normalized** upon loading into `menpo`. For example, `Image` types are imported as 64-bit floating point numbers normalised between \[0, 1\], by default.
-   **axis 0 of landmarks corresponds to axis 0 of the container it is an annotation of**.
-   **The first axis of image types is always the channel data. The remaining axes map exactly to the other spatial axes.** Therefore, the first image axis maps exactly to the zeroth axis of a `PointCloud`.
