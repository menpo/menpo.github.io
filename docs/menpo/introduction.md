Introduction
============

1. <a href="#containers">Core Types</a>
2. <a href="#interfaces">Core Interfaces</a>

---------------------------------------

<a id="containers"></a>

# 1. Core Types
`menpo` is a relatively high-level software package. It is not a replacement for <a href="http://python-pillow.org/">`pillow`<i class="fa fa-external-link"></i></a>, <a href="http://scikit-image.org/">`scikit-image`<i class="fa fa-external-link"></i></a>, or <a href="http://opencv.org/">`opencv`<i class="fa fa-external-link"></i></a> - it ties all these lower-level packages together in to a unified higher-level framework. As a result, we have a family of core types that wrap `numpy` arrays and provide an elegant API. You will find that the vast majority of functions and methods in Menpo take and return these core types, so it's well worth getting used to them - there are only a handful.

**Images**
-   {py:class}`Image <menpo.image.Image>` - n-dimensional image with k-channels of `dtype` data
-   {py:class}`BooleanImage <menpo.image.BooleanImage>` - `Image` restricted to 1 channel of `np.bool` data, and with additional methods for masking operations
-   {py:class}`MaskedImage <menpo.image.MaskedImage>` - `Image` with a `BooleanImage` attached. Has methods for masking operations on an image with k-channels of `dtype` data

**Shapes**
-   {py:class}`PointCloud <menpo.shape.PointCloud>` - n-dimensional ordered point collection
-   {py:class}`PointUndirectedGraph <menpo.shape.PointUndirectedGraph>` - `PointCloud` with undirected connectivity
-   {py:class}`PointDirectedGraph <menpo.shape.PointDirectedGraph>` - `PointCloud` with directed connectivity
-   {py:class}`PointTree <menpo.shape.PointTree>` - `PointCloud` with directed connectivity and without loops
-   {py:class}`TriMesh <menpo.shape.TriMesh>` -  `PointCloud` with a triangulation


<a id="interfaces"></a>

## 2. Core Interfaces
`menpo` is an object oriented framework built around a set of three core interfaces, each one governing a particular facet of `menpo`'s design:

-   {py:class}`Vectorizable <menpo.base.Vectorizable>` - efficient bi-directional conversion of `menpo` types to a numpy vector. Most `menpo` types are `Vectorizable`.
-   {py:class}`Landmarkable <menpo.landmark.Landmarkable>` - objects that can be annotated with spatial labelled landmarks. In `menpo` all images and shapes are `Landmarkable`.
-   {py:class}`Transform <menpo.transform.Transform>` - spatial transformations that can be applied to any shape and used to drive image warps

We will see how these interfaces lead to common patterns throughout `menpo` later in this guide.
