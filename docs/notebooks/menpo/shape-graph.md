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

# Graph

This notebook presents the basic concepts behind Menpo's `Graph` class and subclasses. The aim of this notebook is to introduce the user to Graph _very_ basic functionality; a preliminary step before moving on to the `PointGraph` notebook. For higher level functionality along with visualization methods, the user is encouraged to go through the `PointGraph` notebook.

The basic `Graph` subclasses are:
* `UndirectedGraph`: graphs with undirected edge connections
* `DirectedGraph`: graphs with directed edge connections
* `Tree`: directed graph in which any two vertices are connected with exactly one path

**The corresponding subclasses of `PointGraph` are basically `Graph`s with geometry (`PointCloud`)**. This means that apart from the edge connections between vertices, they also define spatial location coordinates for each vertex. The `PointGraph` subclasses are:
* `PointUndirectedGraph`: graphs with undirected edge connections
* `PointDirectedGraph`: graphs with directed edge connections
* `PointTree`: directed graph in which any two vertices are connected with exactly one path

Below, we split the presentation for `Graph` only in the following sections:

1. Mathematical notation
2. Graphs representation
3. Undirected graph
4. Isolated vertices
5. Directed graph
6. Tree
7. Basic graph properties
8. Basic tree properties

+++

## 1. Mathematical notation

+++

A graph is mathematically defined as 
$$G = (V, E)$$, 
where $V$ is the set of vertices and $E$ is the set of edges. In Menpo, we assume that the vertices in $V$ are numbered with consecutive positive integer numbers starting from 0, i.e. $V=\{0, 1, \ldots, |V|\}$. By defining an edge between two vertices $v_i, v_j\in V$ as $e_{ij}=(v_i,v_j)$, the set of edges can be represented as $E=\{e_{ij}\}, \forall i,j:(v_i,v_j)~\text{is edge}$.

In Menpo, a graph is represented using the _adjacency matrix_, which stores which vertices are adjacent to which other vertices. This is mathematically expressed as the $|V|\times|V|$ _sparse_ matrix
$$A=\left\lbrace\begin{array}{rl}w_{ij}, & \text{for}~i,j:e_{ij}\in E\\ 0, & \text{otherwise}\end{array}\right.$$
where $w_{ij}$ is the weight of edge $e_{ij}$.

Note the following:
* The adjacency matrix $A$ of an _undirected graph_ must be _symmetric_.
* An edge $e_{ij}$ stored in the adjacency matrix $A$ of a _directed graph_ or _tree_ denote the edge that starts from vertex $v_i$ and ends to vertex $v_j$. So the _rows_ of matrix $A$ are the parent vertices and the _columns_ are the children vertices.

+++

## 2. Graphs representation

+++

Based on the above, the adjacency matrix of size $|V|\times|V|$ that gets passed to a Graph constructor can be defined either as a `numpy.ndarray` or a `scipy.sparse.csr_matrix`. Then it is internally stored as a `scipy.sparse.csr_matrix` for memory efficiency reasons.

So let's make the necessary imports.

```{code-cell}
import numpy as np
from scipy.sparse import csr_matrix

from menpo.shape import UndirectedGraph, DirectedGraph, Tree
```

## 3. Undirected graph

+++

The following undirected graph:

```
        |---0---|
        |       |
        |       |
        1-------2
        |       |
        |       |
        3-------4
        |
        |
        5
```
can be defined as:

```{code-cell}
adj_undirected = np.array([[0, 1, 1, 0, 0, 0],
                           [1, 0, 1, 1, 0, 0], 
                           [1, 1, 0, 0, 1, 0],
                           [0, 1, 0, 0, 1, 1],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0]])
undirected_graph = UndirectedGraph(adj_undirected)
print(undirected_graph)
```

or

```{code-cell}
adj_undirected = csr_matrix(([1] * 14, ([0, 1, 0, 2, 1, 2, 1, 3, 2, 4, 3, 4, 3, 5], 
                                        [1, 0, 2, 0, 2, 1, 3, 1, 4, 2, 4, 3, 5, 3])), 
                            shape=(6, 6))
undirected_graph = UndirectedGraph(adj_undirected)
print(undirected_graph)
```

## 4. Isolated vertices

+++

Note that any directed or undirected graph (_not_ a tree) can have isolated vertices, i.e. vertices with no edge connections. For example the following undirected graph:
```
            0---|
                |
                |
        1       2
                |
                |
        3-------4


        5
```
can be defined as:

```{code-cell}
adj_isolated = np.array([[0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 1, 0],
                         [0, 0, 1, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0]])
isolated_graph = UndirectedGraph(adj_isolated)
print(isolated_graph)
```

or

```{code-cell}
adj_isolated = csr_matrix(([1] * 6, ([0, 2, 2, 4, 3, 4], [2, 0, 4, 2, 4, 3])), shape=(6, 6))
isolated_graph = UndirectedGraph(adj_isolated)
print(isolated_graph)
```

## 5. Directed graph

+++

The following directed graph:

```
        |-->0<--|
        |       |
        |       |
        1<----->2
        |       |
        v       v
        3------>4
        |
        v
        5
```
can be defined as:

```{code-cell}
adj_directed = np.array([[0, 0, 0, 0, 0, 0],
                         [1, 0, 1, 1, 0, 0],
                         [1, 1, 0, 0, 1, 0],
                         [0, 0, 0, 0, 1, 1],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0]])
directed_graph = DirectedGraph(adj_directed)
print(directed_graph)
```

or

```{code-cell}
adj_directed = csr_matrix(([1] * 8, ([1, 2, 1, 2, 1, 2, 3, 3], [0, 0, 2, 1, 3, 4, 4, 5])), shape=(6, 6))
directed_graph = DirectedGraph(adj_directed)
print(directed_graph)
```

## 6. Tree

+++

A Tree in Menpo is defined as a directed graph, thus `Tree` is a subclass of `DirectedGraph`. The following tree:

```
               0
               |
            ___|___
           1       2
           |       |
          _|_      |
         3   4     5
         |   |     |
         |   |     |
         6   7     8
```
can be defined as:

```{code-cell}
adj_tree = np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]])
tree = Tree(adj_tree, root_vertex=0)
print(tree)
```

or

```{code-cell}
adj_tree = csr_matrix(([1] * 8, ([0, 0, 1, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8])), shape=(9, 9))
tree = Tree(adj_tree, root_vertex=0)
print(tree)
```

## 7. Basic graph properties

+++

Below we show how to retrieve basic properties from all the previously defined graphs, i.e. `undirected_graph`, `isolated_graph`, `directed_graph` and `tree` of Sections 3, 4, 5 and 6 repsectively.

### Number of vertices and edges
For all the above defined graphs, we can get the number of vertices $|V|$ and number of edges $|E|$ as:

```{code-cell}
print("The undirected_graph has {} vertices and {} edges.".format(undirected_graph.n_vertices, undirected_graph.n_edges))
print("The isolated_graph has {} vertices and {} edges.".format(isolated_graph.n_vertices, isolated_graph.n_edges))
print("The directed_graph has {} vertices and {} edges.".format(directed_graph.n_vertices, directed_graph.n_edges))
print("The tree has {} vertices and {} edges.".format(tree.n_vertices, tree.n_edges))
```

#### Sets of vertices and edges
We can also get the sets of vertices and edges, i.e. $V$ and $E$ respectively, as:

```{code-cell}
print("undirected_graph: The set of vertices $V$ is")
print(undirected_graph.vertices)
print("and the set of edges $E$ is")
print(undirected_graph.edges)
```

#### Adjacency list
We can also retrieve the _adjacency list_, i.e. a list that for each vertex stores the list of its neighbours (or children in the case of directed graphs). For example:

```{code-cell}
print("The adjacency list of the undirected_graph is {}.".format(undirected_graph.get_adjacency_list()))
print("The adjacency list of the directed_graph is {}.".format(directed_graph.get_adjacency_list()))
```

#### Isolated vertices
There are methods to check and retrieve _isolated vertices_, for example:

```{code-cell}
print("Has the undirected_graph any isolated vertices? {}.".format(undirected_graph.has_isolated_vertices()))
print("Has the isolated_graph any isolated vertices? {}, it has {}.".format(isolated_graph.has_isolated_vertices(), 
                                                                            isolated_graph.isolated_vertices()))
```

#### Neighbours and is_edge
We can check if a pair of vertices are connected with an edge:

```{code-cell}
i = 4
j = 7
print("Are vertices {} and {} of the tree connected? {}.".format(i, j, tree.is_edge(i, j)))

i = 5
j = 1
print("Are vertices {} and {} of the directed_graph connected? {}.".format(i, j, directed_graph.is_edge(i, j)))
```

We can also retrieve whether a vertex has neighbours (or children) and who are they, as:

```{code-cell}
v = 1
print("How many neighbours does vertex {} of the isolated_graph have? {}.".format(v, isolated_graph.n_neighbours(v)))
print("How many children does vertex {} of the directed_graph have? {}, they are {}.".format(v, directed_graph.n_children(v), 
                                                                                             directed_graph.children(v)))
print("Who is the parent of vertex {} of the tree? Vertex {}.".format(v, tree.parent(v)))
```

#### Cycles and trees
We can check whether a graph has cycles

```{code-cell}
print("Does the undirected_graph have cycles? {}.".format(undirected_graph.has_cycles()))
print("Does the isolated_graph have cycles? {}.".format(isolated_graph.has_cycles()))
print("Does the directed_graph have cycles? {}.".format(directed_graph.has_cycles()))
print("Does the tree have cycles? {}.".format(tree.has_cycles()))
```

and, of course whether a graph is a tree

```{code-cell}
print("Is the undirected_graph a tree? {}.".format(undirected_graph.is_tree()))
print("Is the directed_graph a tree? {}.".format(directed_graph.is_tree()))
print("Is the tree a tree? {}.".format(tree.is_tree()))
```

## 8. Basic tree properties

+++

Menpo's `Tree` instance has additional basic properties.

### Predecessors list
Apart from the adjacency list mentioned above, a tree can also be represented by a predecessors list, i.e. a list that stores the parent for each vertex. ``None`` denotes the root vertex. For example

```{code-cell}
print(tree.predecessors_list)
```

#### Depth
We can find the maximum depth of a tree

```{code-cell}
print(tree.maximum_depth)
```

as well as the depth of a specific vertex

```{code-cell}
print("The depth of vertex 4 is {}.".format(tree.depth_of_vertex(4)))
print("The depth of vertex 0 is {}.".format(tree.depth_of_vertex(0)))
```

#### Leaves
Finally, we can get the number of leaves as well as whether a specific vertex is a leaf (has no children):

```{code-cell}
print("The tree has {} leaves.".format(tree.n_leaves))
print("Is vertex 7 a leaf? {}.".format(tree.is_leaf(7)))
```
