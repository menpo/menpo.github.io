Introduction
============

1. [Core interfaces](#interfaces)
2. [Data containers](#containers)

---------------------------------------

### <a name="interfaces"></a>1. Core Interfaces
`menpo` is an object oriented framework built around a set of core abstract interfaces, each one governing a single facet of `menpo`'s design. The key interfaces are:

-   [`Shape`](http://docs.menpo.org/en/stable/api/menpo/shape/Shape.html) - spatial data containers
-   [`Vectorizable`](http://docs.menpo.org/en/stable/api/menpo/base/Vectorizable.html) - efficient bi-directional conversion of types to a vector representation
-   [`Targetable`](http://docs.menpo.org/en/stable/api/menpo/base/Targetable.html) - objects that generate some spatial data
-   [`Transform`](http://docs.menpo.org/en/stable/api/menpo/transform/Transform.html) - flexible spatial transformations
-   [`Landmarkable`](http://docs.menpo.org/en/stable/api/menpo/landmark/Landmarkable.html) - objects that can be annotated with spatial labelled landmarks


### <a name="containers"></a>2. Data Containers
Most numerical data in `menpo` is passed around in one of our core data containers, which include:

-   [`LazyList`](http://docs.menpo.org/en/stable/api/menpo/base/LazyList.html) - a list that calls a function when indexed
-   [`Image`](http://docs.menpo.org/en/stable/api/menpo/image/Image.html) - n-dimensional image with k-channels of data
-   [`MaskedImage`](http://docs.menpo.org/en/stable/api/menpo/image/MaskedImage.html) - As `Image`, but with a boolean mask
-   [`BooleanImage`](http://docs.menpo.org/en/stable/api/menpo/image/BooleanImage.html) - As boolean image that is used for masking images.
-   [`PointCloud`](http://docs.menpo.org/en/stable/api/menpo/shape/PointCloud.html) - n-dimensional ordered point collection
-   [`PointUndirectedGraph`](http://docs.menpo.org/en/stable/api/menpo/shape/PointUndirectedGraph.html) - n-dimensional ordered point collection with undirected connectivity
-   [`PointDirectedGraph`](http://docs.menpo.org/en/stable/api/menpo/shape/PointDirectedGraph.html) - n-dimensional ordered point collection with directed connectivity
-   [`PointTree`](http://docs.menpo.org/en/stable/api/menpo/shape/PointTree.html) - n-dimensional ordered point collection with directed connectivity and without loops
-   [`TriMesh`](http://docs.menpo.org/en/stable/api/menpo/shape/TriMesh.html) - As `PointCloud`, but with a triangulation
