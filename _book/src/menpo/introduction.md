Introduction
============

1. [Core Types](#containers)
2. [Core Interfaces](#interfaces)

---------------------------------------

### 1. Core Types {#containers}

`menpo` is a relatively high-level software package. It is not a replacement for <a href="http://python-pillow.org/">`pillow`<i class="fa fa-external-link"></i></a>, <a href="http://scikit-image.org/">`scikit-image`<i class="fa fa-external-link"></i></a>, or <a href="http://opencv.org/">`opencv`<i class="fa fa-external-link"></i></a> - it ties all these lower-level packages together in to a unified higher-level framework. As a result, we have a family of core types that wrap `numpy` arrays and provide an elegant API. You will find that the vast majority of functions and methods in Menpo take and return these core types, so it's well worth getting used to them - there are only a handful.

**Images**
-   [`Image`](http://docs.menpo.org/en/stable/api/menpo/image/Image.html) - n-dimensional image with k-channels of `dtype` data
-   [`BooleanImage`](http://docs.menpo.org/en/stable/api/menpo/image/BooleanImage.html) - `Image` restricted to 1 channel of `np.bool` data, and with additional methods for masking operations
-   [`MaskedImage`](http://docs.menpo.org/en/stable/api/menpo/image/MaskedImage.html) - `Image` with a `BooleanImage` attached. Has methods for masking operations on an image with k-channels of `dtype` data

**Shapes**
-   [`PointCloud`](http://docs.menpo.org/en/stable/api/menpo/shape/PointCloud.html) - n-dimensional ordered point collection
-   [`PointUndirectedGraph`](http://docs.menpo.org/en/stable/api/menpo/shape/PointUndirectedGraph.html) - `PointCloud` with undirected connectivity
-   [`PointDirectedGraph`](http://docs.menpo.org/en/stable/api/menpo/shape/PointDirectedGraph.html) - `PointCloud` with directed connectivity
-   [`PointTree`](http://docs.menpo.org/en/stable/api/menpo/shape/PointTree.html) - `PointCloud` with directed connectivity and without loops
-   [`TriMesh`](http://docs.menpo.org/en/stable/api/menpo/shape/TriMesh.html) -  `PointCloud` with a triangulation


### 2. Core Interfaces {#interfaces}

`menpo` is an object oriented framework built around a set of three core interfaces, each one governing a particular facet of `menpo`'s design:

-   [`Vectorizable`](http://docs.menpo.org/en/stable/api/menpo/base/Vectorizable.html) - efficient bi-directional conversion of `menpo` types to a numpy vector. Most `menpo` types are `Vectorizable`.
-   [`Landmarkable`](http://docs.menpo.org/en/stable/api/menpo/landmark/Landmarkable.html) - objects that can be annotated with spatial labelled landmarks. In `menpo` all images and shapes are `Landmarkable`.
-   [`Transform`](http://docs.menpo.org/en/stable/api/menpo/transform/Transform.html) - spatial transformations that can be applied to any shape and used to drive image warps

We will see how these interfaces lead to common patterns throughout `menpo` later in this guide.
