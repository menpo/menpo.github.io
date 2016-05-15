Introduction
============

This user guide is a general introduction to Menpo, aiming to provide a bird's eye of Menpo's design. After reading this guide you should be able to go explore Menpo's extensive Notebooks and not be too suprised by what you see.

Core Interfaces
---------------

Menpo is an object oriented framework built around a set of core abstract interfaces, each one governing a single facet of Menpo's design. Menpo's key interfaces are:

-   Shape - spatial data containers
-   Vectorizable - efficient bi-directional conversion of types to a vector representation
-   Targetable - objects that generate some spatial data
-   Transform - flexible spatial transformations
-   Landmarkable - objects that can be annotated with spatial labelled landmarks

Data containers
---------------

Most numerical data in Menpo is passed around in one of our core data containers. The features of each of the data containers is explained in great detail in the notebooks - here we just list them to give you a feel for what to expect:

-   LazyList - a list that calls a function when indexed
-   Image - n-dimensional image with k-channels of data
-   MaskedImage - As Image, but with a boolean mask
-   BooleanImage - As boolean image that is used for masking images.
-   PointCloud - n-dimensional ordered point collection
-   PointUndirectedGraph - n-dimensional ordered point collection with undirected connectivity
-   PointDirectedGraph - n-dimensional ordered point collection with directed connectivity
-   TriMesh - As PointCloud, but with a triangulation

