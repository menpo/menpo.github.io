Active Pictorial Structures
===========================

1. [Definition](#definition)
2. [Gaussian Markov Random Field](#gmrf)
3. [Model](#model)
4. [Cost Function and Optimization](#cost)  
5. [Fitting Example](#fitting)
6. [References](#references)
7. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/atm/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

<p><div style="background-color: #F2DEDE; width: 100%; border: 1px solid #A52A2A; padding: 1%;">
<p style="float: left;"><i class="fa fa-exclamation-circle" aria-hidden="true" style="font-size:4em; padding-right: 15%; padding-bottom: 10%; padding-top: 10%;"></i></p>
We highly recommend that you render all matplotlib figures <b>inline</b> the Jupyter notebook for the best <a href="../menpowidgets/index.md"><em>menpowidgets</em></a> experience.
This can be done by running</br>
<center><code>%matplotlib inline</code></center>
in a cell. Note that you only have to run it once and not in every rendering cell.
</div></p>

### <a name="definition"></a>1. Definition
Active Pictorial Structures (APS) is a statistical deformable model of the shape and appearance of a deformable object class.
It is a generative model that takes advantage of the strengths, and overcomes the disadvantages, of both Pictorial Structures (PS) [[3](#3)] and Active Appearance Models (AAMs) [[2](#2)].
APS is motivated by the tree-based structure of PS and further expands on it, as it can for­mulate the relations between parts using any graph struc­ture; not only trees. From AAMs, it borrows the use of the Gauss-Newton algorihtm in combination with a statis­tical shape model. The weighted inverse compositional al­gorithm with fixed Jacobian and Hessian that is used for optimization is very fast. In this page, we provide a basic mathematical definition of APS. For a more in-depth explanation, please refer to the relevant literature in [References](#references) and especially [[1](#1)].

A shape instance of a deformable object is represented as $$\mathbf{s}=\big[{\mathbf{\ell}_1}^{\mathsf{T}},{\mathbf{\ell}_2}^{\mathsf{T}},\ldots,{\mathbf{\ell}_L}^{\mathsf{T}}\big]^{\mathsf{T}}=\big[x_1,y_1,\ldots,x_L,y_L\big]^{\mathsf{T}}$$, a $$2L\times 1$$ vector consisting of $$L$$ landmark points coordinates $$\mathbf{\ell}_i=[x_i,y_i],\forall i=1,\ldots,L$$. Moreover, let us denote by $$\mathcal{A}(\mathbf{I}, \mathbf{s})$$ a patch-based feature extraction function that returns an $$M\times 1$$ feature vector given an input image $$\mathbf{I}$$ and a shape instance $$\mathbf{s}$$. The features (e.g. SIFT) are computed on patches that are centered around the landmark points.


### <a name="gmrf"></a>2. Gaussian Markov Random Field
Let us define an undirected graph between the $$L$$ land­mark points of an object as $$G=(V, E)$$, where $$V=\big\lbrace v_1, v_2, \ldots, v_L\big\rbrace$$ is the set of $$L$$ vertexes and there is an edge $$(v_i, v_j)\in E$$ for each pair of connected landmark points. Moreover, let us assume that we have a set of random vari­ables
$$X=\{X_i\},~\forall i:v_i\in V$$ which represent an abstract feature vector of length $$k$$ extracted from each vertex $$v_i$$, i.e. $$\mathbf{x}_i,~\forall i:v_i\in V$$. We model the likelihood probability of two ran­dom variables that correspond to connected vertexes with a normal distribution
$$
p(X_i=\mathbf{x}_i, X_j=\mathbf{x}_j|G)\sim\mathcal{N}(\mathbf{m}_{ij}, \mathbf{\Sigma}_{ij}),~\forall i,j: (v_i,v_j)\in E
$$
where $$\mathbf{m}_{ij}$$ is the $$2k\times 1$$ mean vector and $$\mathbf{\Sigma}_{ij}$$ is the $$2k\times 2k$$ covariance matrix. Consequently, the cost of observing a set of feature vectors $$\{\mathbf{x}_i\},~\forall i: v_i\in V$$ can be computed using a Mahalanobis distance per edge, i.e.
$$
\sum_{\forall i,j: (v_i,v_j)\in E}\left(\left[\begin{array}{c}\mathbf{x}_i\\ \mathbf{x}_j\end{array}\right]-\mathbf{m}_{ij}\right)^{\mathsf{T}} {\mathbf{\Sigma}_{ij}}^{-1} \left(\left[\begin{array}{c}\mathbf{x}_i\\ \mathbf{x}_j\end{array}\right]-\mathbf{m}_{ij}\right)
$$
In practice, the computational cost of computing this cost is too expensive because it requires looping over all the edges of the graph. Inference can be much faster if we convert this cost to an equivalent matrical form as
$$
(\mathbf{x}-\mathbf{m})^{\mathsf{T}}\mathbf{\Sigma}^{-1}(\mathbf{x}-\mathbf{m})
$$
This is equivalent to modelling the set of random variables $$X$$ with a Gaussian Markov Random Field (GMRF) [[4](#4)]. A GMRF is described by an undirected graph, where the vertexes stand for random variables and the edges impose statistical constraints on these random variables. Thus, the GMRF models the set of random variables with a multivari­ate normal distribution $$p(X=\mathbf{x}|G)\sim\mathcal{N}(\mathbf{m},\mathbf{\Sigma})$$, where $$\mathbf{m}=\big[{\mathbf{m}_1}^{\mathsf{T}},\ldots,{\mathbf{m}_L}^{\mathsf{T}}\big]^{\mathsf{T}}=\big[E(X_1)^{\mathsf{T}},\ldots,E(X_L)^{\mathsf{T}}\big]^{\mathsf{T}}$$ is the $$kL\times 1$$ mean vectors and $$\mathbf{\Sigma}$$ the $$kL\times kL$$ overall covariance matrix. We denote by $$\mathbf{Q}$$ the block-sparse pre­cision matrix that is the inverse of the covariance matrix, i.e. $$\mathbf{Q}=\mathbf{\Sigma}^{-1}$$. By applying the GMRF we make the as­sumption that the random variables satisfy the three Markov properties (pairwise, local and global) and that the blocks of the precision matrix that correspond to disjoint vertexes are zero, i.e. $$\mathbf{Q}_{ij}=\mathbf{0}_{k\times k},~\forall i,j: (v_i, v_j)\notin E$$. By defining $$\mathcal{G}_i=\big\lbrace(i-1)k+1, (i-1)k+2, \ldots, ik\big\rbrace$$ to be a set of indices for sampling a matrix, we can prove that the structure of the precision matrix is
$$
\mathbf{Q}=\left\lbrace\begin{array}{ll}
\sum_{\forall j: (v_i, v_j)\in E}{\mathbf{\Sigma}_{ij}}^{-1}(\mathcal{G}_1,\mathcal{G}_1) + \sum_{\forall j: (v_j, v_i)\in E}{\mathbf{\Sigma}_{ji}}^{-1}(\mathcal{G}_2,\mathcal{G}_2),~\forall i: v_i\in V, & \text{at~}(\mathcal{G}_i, \mathcal{G}_i)\\\\
{\mathbf{\Sigma}_{ij}}^{-1}(\mathcal{G}_1,\mathcal{G}_2),~\forall i,j: (v_i, v_j)\in E, & \text{at~}(\mathcal{G}_i, \mathcal{G}_j)\text{~and~}(\mathcal{G}_j, \mathcal{G}_i)\\\\
0, & \text{elsewhere}
\end{array}\right.
$$

Using the same assumptions and given a directed graph (cyclic or acyclic) $$G = (V, E)$$, where $$(v_i, v_j)\in E$$ means that $$v_i$$ is the parent of $$v_j$$, we can show that
$$
(\mathbf{x}-\mathbf{m})^{\mathsf{T}}\mathbf{\Sigma}^{-1}(\mathbf{x}-\mathbf{m}) = \sum_{\forall i,j: (v_i, v_j)\in E} (\mathbf{x}_i-\mathbf{x}_j-\mathbf{m}_{ij})^{\mathsf{T}}{\mathbf{\Sigma}_{ij}}^{-1}(\mathbf{x}_i-\mathbf{x}_j-\mathbf{m}_{ij})
$$
is true if
$$
\mathbf{Q}=\left\lbrace\begin{array}{ll}
\sum_{\forall j: (v_i, v_j)\in E}{\mathbf{\Sigma}_{ij}}^{-1} + \sum_{\forall j: (v_j, v_i)\in E}{\mathbf{\Sigma}_{ji}}^{-1},~\forall i: v_i\in V, & \text{at~}(\mathcal{G}_i, \mathcal{G}_i)\\\\
-{\mathbf{\Sigma}_{ij}}^{-1},~\forall i,j: (v_i, v_j)\in E, & \text{at~}(\mathcal{G}_i, \mathcal{G}_j)\text{~and~}(\mathcal{G}_j, \mathcal{G}_i)\\\\
0, & \text{elsewhere}
\end{array}\right.
$$
where $$\mathbf{m}_{ij}=E(X_i-X_j)$$ and $$\mathbf{m}=\big[{\mathbf{m}_1}^{\mathsf{T}},\ldots,{\mathbf{m}_L}^{\mathsf{T}}\big]^{\mathsf{T}}=\big[E(X_1)^{\mathsf{T}},\ldots,E(X_L)^{\mathsf{T}}\big]^{\mathsf{T}}$$. In this case, if $$G$$ is a tree, then we have a Bayesian network. Please refer to the supplementary material of [[1](#1)] for detailed proofs of the above.


### <a name="model"></a>3. Model
An APS [[1](#1)] is trained using a set of $$N$$ images $$\big\lbrace\mathbf{I}_1,\mathbf{I}_2,\ldots,\mathbf{I}_N\big\rbrace$$ that are annotated with a set of $$L$$ landmarks. It consists of the following parts:

* **Shape Model**  
  The shape model is trained as explained in the [Point Distributon Model section](pdm.md "Point Distribution Model basics"). The training shapes $$\big\lbrace\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\big\rbrace$$ are first aligned using Generalized Procrustes Analysis and then an orthonormal basis is created using Principal Component Analysis (PCA) which is further augmented with four eigenvectors that represent the similarity transform (scaling, in-plane rotation and translation). This results in
  $$
  \big\lbrace\bar{\mathbf{s}}, \mathbf{U}\big\rbrace
  $$
  where $$\mathbf{U}\in\mathbb{R}^{2L\times n}$$ is the orthonormal basis of $$n$$ eigenvectors (including the four similarity components) and $$\bar{\mathbf{s}}\in\mathbb{R}^{2L\times 1}$$ is the mean shape vector. We define $$\mathcal{S}\in\mathbb{R}^{2L}$$ which generates a new shape instance given the shape model's basis, an input shape and the shape parameters vector as
  $$
  \mathcal{S}(\mathbf{s}, \mathbf{p}) = \mathbf{s} + \mathbf{U}\mathbf{p}
  $$
  where $$\mathbf{p}=\big[p_1,p_2,\ldots,p_n\big]^{\mathsf{T}}$$ are the parameters' values. Similarly we define the set of functions $$\mathcal{S}_i\in\mathbb{R}^{2L},~\forall i=1,\ldots,L$$ that return the coordinates of the $$i^{\text{th}}$$ landmark of the shape instance as
  $$
  \mathcal{S}_i(\mathbf{s}, \mathbf{s}) = \mathbf{s}_{2i-1, 2i} + \mathbf{U}_{2i-1, 2i}\mathbf{p},~\forall i=1,\ldots,L
  $$
  where $$\mathbf{s}_{2i-1, 2i}$$ denotes the coordinates' vector of the $$i^{\text{th}}$$ landmark point and $$\mathbf{U}_{2i-1, 2i}$$ denotes the $$2i-1$$ and $$2i$$ rows of the shape subspace $$\mathbf{U}$$.

  Another way to build the shape model is by using a GMRF structure. Specifically, given an undi­rected graph $$G^s = (V^s, E^s)$$ and assuming that the pairwise locations' vector of two connected landmarks fol­lows a normal distribution as $$\big[x_i, y_i, x_j, y_j\big]^{\mathsf{T}}\sim\mathcal{N}(\mathbf{m}_{ij}^s, \mathbf{\Sigma}_{ij}^s)$$, we formulate a GMRF. Thus, this can be expressed in matricial format as shown in the [GMRF paragraph](#gmrf) as $$p(\mathbf{s}|G^s)\sim\mathcal{N}(\bar{\mathbf{s}}, \mathbf{\Sigma}^s)$$. After obtaining the GMRF precision matrix $$\mathbf{Q}^s$$, we can invert it and apply PCA on the resulting covariance matrix in order to obtain a linear shape model. Note that as shown in [[1](#1)], it is more beneficial to directly apply PCA rather than using a GMRF for the shape model.

* **Appearance Model**  
  Given an undirected graph $$G^a=(V^a, E^a)$$ and assuming that the concatenation of the appearance vectors of two connected landmarks follows a normal distribution, we form a GMRF that can be expressed as $$p(\mathcal{A}(\mathbf{I},\mathbf{s})|G^a)\sim\mathcal{N}(\bar{\mathbf{a}},\mathbf{\Sigma}^a)$$ where $$\bar{\mathbf{a}}$$ is the $$M\times 1$$ mean appearance vector and $$\mathbf{Q}^a={\mathbf{\Sigma}^a}^{-1}$$ is the $$M\times M$$ precision matrix that is formulated as shown in the [GMRF paragraph](#gmrf). During the training of the appear­ance model, the low rank representation of each edgewise covariance matrix $$\mathbf{\Sigma}_{ij}^a$$ is utilized by using the first $$m$$ sin­gular values of its SVD factorization. Given $$\bar{\mathbf{a}}$$ and $$\mathbf{Q}^a$$, the cost of an observed appearance vector $$\mathcal{A}(\mathbf{I},\mathbf{s})$$ corresponding to a shape instance $$\mathbf{s}=\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})$$ in an image $$\mathbf{I}$$ is
  $$
  \big\lVert\mathcal{A}\big(\mathbf{I},\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})\big)-\bar{\mathbf{a}}\big\rVert^2_{\mathbf{Q}^a} = \big[\mathcal{A}\big(\mathbf{I},\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})\big)-\bar{\mathbf{a}}\big]^{\mathsf{T}} \mathbf{Q}^a \big[\mathcal{A}\big(\mathbf{I},\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})\big)-\bar{\mathbf{a}}\big]
  $$

* **Deformation Prior**  
  This is similar to the deformation model of Pictorial Structures [[3](#3)]. Specifically, we define a directed (cyclic or acyclic) graph between the landmark points $$G^d=(V^d,E^d)$$ and model the relative locations between the parent and child of each edge with a GMRF. We assume that the relative loaction between the vertexes of each edge follows a normal distribution $$[x_i-x_j, y_i-y_j]^{\mathsf{T}}\sim\mathcal{N}(\mathbf{m}_{ij}^d, \mathbf{\Sigma}_{ij}^d)$$, $$\forall i,j: (v_i^d,v_j^d)\in E^d$$ and model the overall structure with a GMRF that has a $$2L\times 2L$$ block-sparse precision matrix. $$\mathbf{Q}^d$$ computed as shown in the [GMRF paragraph](#gmrf). Note that the mean relative location vector is the same as the mean shape vector. This spring-like prior model manages to constrain extreme shape configurations that could be evoked during fitting with very bad initialization, leading the optimization process towards a better result. Given $$\bar{\mathbf{s}}$$ and $$\mathbf{Q}^d$$, the cost of observing a shape instance $$\mathbf{s}=\mathcal{S}(\bar{\mathbf{s}}, \mathbf{p})$$ is
  $$
  \big\lVert\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})-\bar{\mathbf{s}}\big\rVert^2_{\mathbf{Q}^d} = \big\lVert\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})-\mathcal{S}(\bar{\mathbf{s}},\mathbf{0})\big\rVert^2_{\mathbf{Q}^d} = \mathcal{S}(\mathbf{0},\mathbf{p})^{\mathsf{T}} \mathbf{Q}^d \mathcal{S}(\mathbf{0},\mathbf{p})
  $$
  where we use the properties $$\mathcal{S}(\bar{\mathbf{s}},\mathbf{0})=\bar{\mathbf{s}}+\mathbf{U}\mathbf{0}=\bar{\mathbf{s}}$$ and $$\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})-\bar{\mathbf{s}}=\bar{\mathbf{s}}+\mathbf{U}\mathbf{p}-\bar{\mathbf{s}}=\mathcal{S}(\mathbf{0},\mathbf{p})$$.


### <a name="cost"></a>4. Cost Function and Optimization
Given a test image $$\mathbf{I}$$, the optimization cost function of APS is
$$
\arg\min_{\mathbf{p}} \big\lVert\mathcal{A}\big(\mathbf{I},\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})\big)-\bar{\mathbf{a}}\big\rVert^2_{\mathbf{Q}^a} + \lambda\big\lVert\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})-\bar{\mathbf{s}}\big\rVert^2_{\mathbf{Q}^d}
$$
The minimization of this function with respect to the shape parameters $$\mathbf{p}$$ is performed with a variant of the Gauss-Newton algorithm. The hyper-parameter $$\lambda$$ controls the weighting between the appearance and deformation costs, which give the generative nature of the model it can greatly determine the performance. An optimal value of this hyper-parameter can be found using a validation dataset. The optimization procedure can be ap­plied in two different ways, depending on the coordinate system in which the shape parameters are updated: __(1)__ for­ward and __(2)__ inverse. Additionally, the parameters update could be carried out either in an additive or compositional manner. The compositional update has the form $$\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})\leftarrow\mathcal{S}(\mathbf{s},\mathbf{p})\circ\mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p})^{-1}=\mathcal{S}(\mathcal{S}(\bar{\mathbf{s}},-\Delta\mathbf{p}),\mathbf{p}) = \mathcal{S}(\bar{\mathbf{s}},\mathbf{p}-\Delta\mathbf{p})$$. Consequently, due to the translational nature of the motion model, the compositional parameters update is reduced to the parameters subtraction, as $$\mathbf{p}\leftarrow\mathbf{p}-\Delta\mathbf{p}$$, which is equivalent to the additive update.

* **Weighted Inverse Compositional with fixed Jacobian and Hessian**  
  By using this compositional update of the parameters and having an initial estimate of $$\mathbf{p}$$, the cost function of APS is expressed as minimizing
  $$
  \arg\min_{\Delta\mathbf{p}} \big\lVert\mathcal{A}\big(\mathbf{I}, \mathcal{S}(\bar{\mathbf{s}},\mathbf{p})\big)-\bar{\mathbf{a}}(\mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p}))\big\rVert^2_{\mathbf{Q}^a} + \lambda\big\lVert\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})-\mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p})\big\rVert^2_{\mathbf{Q}^d}
  $$
  with respect to $$\Delta\mathbf{p}$$. With some abuse of notation due to $$\bar{\mathbf{a}}$$ being a vector, $$\bar{\mathbf{a}}(\mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p}))$$ can be described as
  $$
  \bar{\mathbf{a}}(\mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p}))=\left[\begin{array}{c}\mathbf{m}_1^a(\mathcal{S}_1(\bar{\mathbf{s}},\Delta\mathbf{p}))\\ \\\vdots\\ \\\mathbf{m}_L^a(\mathcal{S}_L(\bar{\mathbf{s}},\Delta\mathbf{p}))\end{array}\right]
  $$
  where $$\mathbf{m}_i^a, \forall i=1,\ldots,L$$ is the mean appearance vector per patch. In order to find the solution we need to linearize around $$\Delta\mathbf{p}=\mathbf{0}$$ as
  $$
  \left\lbrace\begin{array}{l}\bar{\mathbf{a}}(\mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p}))\approx\bar{\mathbf{a}} + {\left.\mathbf{J}_{\bar{\mathbf{a}}}\right|}_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}\\
  \mathcal{S}(\bar{\mathbf{s}},\Delta\mathbf{p})\approx\bar{\mathbf{s}} + {\left.\mathbf{J}_{\mathcal{S}}\right|}_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p} \end{array}\right.
  $$
  where $${\left.\mathbf{J}_{\mathcal{S}}\right|}_{\mathbf{p}=\mathbf{0}} = \mathbf{J}_{\mathcal{S}} = \frac{\partial\mathcal{S}}{\partial\mathbf{p}}=\mathbf{U}$$ is the $$2L\times n$$ shape Jacobian and $${\left.\mathbf{J}_{\bar{\mathbf{a}}}\right|}_{\mathbf{p}=\mathbf{0}} = \mathbf{J}_{\bar{\mathbf{a}}}$$ is the $$M\times n$$ appearance Jacobian
  $$
  \mathbf{J}_{\bar{\mathbf{a}}} = \nabla\bar{\mathbf{a}}\frac{\partial\mathcal{S}}{\partial\mathbf{p}} = \nabla\bar{\mathbf{a}}\mathbf{U} = \left[\begin{array}{c}\nabla\mathbf{m}_1^a\mathbf{U}_{1,2}\\ \vdots\\ \nabla\mathbf{m}_L^a\mathbf{U}_{2L-1,2L}\end{array}\right]
  $$
  where $$\mathbf{U}_{2i-1,2i}$$ denotes the $$2i-1$$ and $$2i$$ row vectors of the basis $$\mathbf{U}$$. Note that we make an abuse of notation by writing $$\nabla\mathbf{m}_i^a$$ because $$\mathbf{m}_i^a$$ is a vector. However, it represents the gradient of the mean patch-based appearance that corresponds to landmark $$i$$. By substituting, taking the partial derivative with respect to $$\Delta\mathbf{p}$$, equating it to $$\mathbf{0}$$ and solving for $$\Delta\mathbf{p}$$ we get
  $$
  \Delta\mathbf{p}=\mathbf{H}^{-1} \big[{\mathbf{J}_{\bar{\mathbf{a}}}}^T \mathbf{Q}^a \left(\mathcal{A}(\mathbf{I}, \mathcal{S}(\bar{\mathbf{s}},\mathbf{p}))-\bar{\mathbf{a}}\right) + \lambda\mathbf{H}_{\mathcal{S}}\mathbf{p}\big]
  $$
  where
  $$
  \left.\begin{array}{l}\mathbf{H}_{\bar{\mathbf{a}}}={\mathbf{J}_{\bar{\mathbf{a}}}}^T \mathbf{Q}^a \mathbf{J}_{\bar{\mathbf{a}}}\\ \mathbf{H}_{\mathcal{S}}={\mathbf{J}_{\mathcal{S}}}^T \mathbf{Q}^d \mathbf{J}_{\mathcal{S}}=\mathbf{U}^T\mathbf{Q}^d\mathbf{U}\end{array}\right\rbrace\Rightarrow \mathbf{H}=\mathbf{H}_{\bar{\mathbf{a}}}+\lambda\mathbf{H}_{\mathcal{S}}
  $$
  is the combined $$n\times n$$ Hessian matrix and we use the property $${\mathbf{J}_{\mathcal{S}}}^T \mathbf{Q}^d \left(\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})-\bar{\mathbf{s}}\right) =  \mathbf{U}^T\mathbf{Q}^d\mathbf{U}\mathbf{p}=\mathbf{H}_{\mathcal{S}}\mathbf{p}$$. Note that $$\mathbf{J}_{\bar{\mathbf{a}}}$$, $$\mathbf{H}_{\bar{\mathbf{a}}}$$, $$\mathbf{H}_{\mathcal{S}}$$ and $$\mathbf{H}^{-1}$$ can be precomputed. The computational cost per iteration is only $$\mathcal{O}(nM)$$ which is practically a multiplication between an $$n\times M$$ matrix and a $$M\times1$$ vector that leads to a very fast fitting algorithm.

* **Forward**  
  The cost function in this case takes the form of minimizing
  $$
  \arg\min_{\Delta\mathbf{p}} \big\lVert\mathcal{A}\big(\mathbf{I},\mathcal{S}(\bar{\mathbf{s}},\mathbf{p}+\Delta\mathbf{p})\big)-\bar{\mathbf{a}}\big\rVert^2_{\mathbf{Q}^a} + \lambda\big\lVert\mathcal{S}(\mathbf{0},\mathbf{p}+\Delta\mathbf{p})\big\rVert^2_{\mathbf{Q}^d}
  $$
  with respect to $$\Delta\mathbf{p}$$. In order to find the solution we need to linearize around $$\mathbf{p}$$, thus using first order Taylor expansion at $$\mathbf{p}+\Delta\mathbf{p}=\mathbf{p}\Rightarrow\Delta\mathbf{p}=\mathbf{0}$$ as
  $$
  \left\lbrace\begin{array}{l}\mathcal{A}(\mathcal{S}(\bar{\mathbf{s}},\mathbf{p}+\Delta\mathbf{p}))\approx\mathcal{A}(\mathcal{S}(\bar{\mathbf{s}},\mathbf{p})) + {\left.\mathbf{J}_{\mathcal{A}}\right|}_{\mathbf{p}=\mathbf{p}}\Delta\mathbf{p}\\
  \mathcal{S}(\mathbf{0},\mathbf{p}+\Delta\mathbf{p})\approx\mathcal{S}(\mathbf{0},\mathbf{p}) + {\left.\mathbf{J}_{\mathcal{S}}\right|}_{\mathbf{p}=\mathbf{p}}\Delta\mathbf{p}\end{array}\right.
  $$
  where $${\left.\mathbf{J}_{\mathcal{S}}\right|}_{\mathbf{p}=\mathbf{p}} = \mathbf{J}_{\mathcal{S}}$$ is the $$2L\times n$$ shape Jacobian $$\mathbf{J}_{\mathcal{S}} = \frac{\partial\mathcal{S}}{\partial\mathbf{p}}=\mathbf{U}$$ and $${\left.\mathbf{J}_{\mathcal{A}}\right|}_{\mathbf{p}=\mathbf{p}} = \mathbf{J}_{\mathcal{A}}$$ is the $$M\times n$$ appearance Jacobian
  $$
  \mathbf{J}_{\mathcal{A}} = \nabla_{\mathcal{A}}\frac{\partial\mathcal{S}}{\partial\mathbf{p}} = \nabla_{\mathcal{A}}\mathbf{U} = \left[\begin{array}{c}\nabla\mathcal{A}(\mathbf{I},\mathcal{S}_1(\bar{\mathbf{s}},\mathbf{p}))\mathbf{U}_{1,2}\\\nabla\mathcal{A}(\mathbf{I},\mathcal{S}_2(\bar{\mathbf{s}},\mathbf{p}))\mathbf{U}_{3,4}\\\vdots\\\nabla\mathcal{A}(\mathbf{I},\mathcal{S}_L(\bar{\mathbf{s}},\mathbf{p}))\mathbf{U}_{2L-1,2L}\end{array}\right]
  $$
  where $$\mathbf{U}_{2i-1,2i}$$ denotes the $$2i-1$$ and $$2i$$ row vectors of the basis $$\mathbf{U}$$. By substituting, taking the partial derivative with respect to $$\Delta\mathbf{p}$$, equating it to $$\mathbf{0}$$ and solving for $$\Delta\mathbf{p}$$ we get
  $$
  \Delta\mathbf{p}=-\mathbf{H}^{-1} \big[{\mathbf{J}_{\mathcal{A}}}^T \mathbf{Q}^a \left(\mathcal{A}(\mathcal{S}(\bar{\mathbf{s}},\mathbf{p}))-\bar{\mathbf{a}}\right) + \lambda\mathbf{H}_{\mathcal{S}}\mathbf{p}\big]
  $$
  where
  $$
  \left.\begin{array}{l}\mathbf{H}_{\mathcal{A}}={\mathbf{J}_{\mathcal{A}}}^T \mathbf{Q}^a \mathbf{J}_{\mathcal{A}}\\ \mathbf{H}_{\mathcal{S}}={\mathbf{J}_{\mathcal{S}}}^T \mathbf{Q}^s \mathbf{J}_{\mathcal{S}}=\mathbf{U}^T\mathbf{Q}^s\mathbf{U}\end{array}\right\rbrace\Rightarrow \mathbf{H}=\mathbf{H}_{\mathcal{A}}+\lambda\mathbf{H}_{\mathcal{S}}
  $$
  is the combined $$n\times n$$ Hessian matrix with getting into account that $${\mathbf{J}_{\mathcal{S}}}^T \mathbf{Q}^s \mathcal{S}(\mathbf{0},\mathbf{p}) = \mathbf{U}^T\mathbf{Q}^s\mathbf{U}\mathbf{p} = \mathbf{H}_{\mathcal{S}}\mathbf{p}$$. $$\mathbf{H}_{\mathcal{S}}$$ can be precomputed but $$\mathbf{J}_{\mathcal{A}}$$ and $$\mathbf{H}^{-1}$$ need to be computed at each iteration. Consequently, the total computational cost is $$\mathcal{O}(nM^2 + nM + n^3)$$ which is much slower than the cost of the weighted inverse compositional algorithm with fixed Jacobian and Hessian.

### <a name="references"></a>5. References
<a name="1"></a>[1] E. Antonakos, J. Alabort-i-Medina, and S. Zafeiriou. "Active Pictorial Structures", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015.

<a name="2"></a>[2] I. Matthews, and S. Baker. "Active Appearance Models Revisited", International Journal of Computer Vision, vol. 60, no. 2, pp. 135-164, 2004.

<a name="3"></a>[3] P. F. Felzenszwalb and D. P. Huttenlocher. "Pictorial Struc­tures for Object Recognition", International Journal of Com­puter Vision (IJCV), 61(1):55-79, 2005.

<a name="4"></a>[4] H. Rue and L. Held. "Gaussian Markov Random Fields: Theory and Applications", CRC Press, 2005.
