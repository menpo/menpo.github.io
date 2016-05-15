Changelog
=========

0.7.0 (2016/03/21)
------------------

New release that contains some minor breaking changes. In general, the biggest two changes are:

> -   Use ImageIO rather than Pillow for basic importing of some image types. The most important aspect of this change is that we now support importing videos! Our GIF support also became much more robust.
> -   Change multi-asset importing to use a new type - the `LazyList`. Lazy lists are a generic concept for a container that holds onto a list of callables which are invoked on indexing. This means that image importing, for example, returns immediately but can be **randomly indexed**. This is in contrast to generators, which have to be sequentially accessed. This is particularly important for video support, as the frames can be accessed randomly or sliced from the end (rather than having to pay the penalty of importing the entirety of a long video just to access the last frame, for example).

These changes should not affect code currently in production - since these are behavioural breaking changes rather than syntax. Note that this release also officially supports Python 3.5!

### Breaking Changes

> -   ImageIO is used for importing. Therefore, the pixel values of some images have changed due to the difference in underlying importing code.
> -   Multi-asset importers are now `LazyList`s.
> -   HOG previously returned negative values due to rounding errors on binning. This has been rectified, so the output values of HOG are now slightly different.

### New Features

> -   `from_tri_mask` method added to `TriMesh`
> -   `LazyList` type that holds a list of callables that are invoked on indexing.
> -   New rasterize methods. Given an image and a landmark group, return a new image with the landmarks rasterized onto the image. Useful for saving results to disk.
> -   Python 3.5 support!
> -   Better support for non `float64` image types. For example, `as_greyscale` can be called on a `uint8` image.

### Deprecated

> -   The previously deprecated `inplace` image methods **were not removed in this release**.
> -   `set_h_matrix` is deprecated for `Homogeneous` transforms.

### Github Pull Requests

-   [\#682](https://github.com/menpo/menpo/pull/682) Update the view\_patches to show only the selected landmarks. (@grigorisg9gr)
-   [\#639](https://github.com/menpo/menpo/pull/639) add from\_tri\_mask method to TriMesh instances (@patricksnape, @jabooth)
-   [\#680](https://github.com/menpo/menpo/pull/680) Expose file extension to exporters (Fix PIL exporter bug) (@patricksnape)
-   [\#672](https://github.com/menpo/menpo/pull/672) Use Conda environment.yml on RTD (@patricksnape)
-   [\#678](https://github.com/menpo/menpo/pull/678) Deprecate set\_h\_matrix and fix \#677 (@patricksnape)
-   [\#676](https://github.com/menpo/menpo/pull/676) Implement LazyList \_\_add\_\_ (@patricksnape)
-   [\#633](https://github.com/menpo/menpo/pull/633) BREAKING: Imageio (@patricksnape)
-   [\#648](https://github.com/menpo/menpo/pull/648) Try turning coverage checking back on (@patricksnape)
-   [\#670](https://github.com/menpo/menpo/pull/670) Rasterize 2D Landmarks Method (@patricksnape)
-   [\#606](https://github.com/menpo/menpo/pull/606) Fix negative values in HOG calculation (@patricksnape)
-   [\#673](https://github.com/menpo/menpo/pull/673) Fix the widgets in PCA. (@grigorisg9gr)
-   [\#669](https://github.com/menpo/menpo/pull/669) BREAKING: Add LazyList - default importing is now Lazy (@patricksnape)
-   [\#668](https://github.com/menpo/menpo/pull/668) Speedup as\_greyscale (@patricksnape)
-   [\#666](https://github.com/menpo/menpo/pull/666) Add the protocol option in exporting pickle. (@grigorisg9gr)
-   [\#665](https://github.com/menpo/menpo/pull/665) Fix bug with patches of different type than float64 (@patricksnape)
-   [\#664](https://github.com/menpo/menpo/pull/664) Python 3.5 builds (@patricksnape)
-   [\#661](https://github.com/menpo/menpo/pull/661) Return labels - which maps to a KeysView as a list (@patricksnape)

0.6.2 (2015/12/13)
------------------

Add axes ticks option to `view_patches`.

### Github Pull Requests

- \#659\_ Add axes ticks options to view\_patches (@nontas) .. \_\#659: <https://github.com/menpo/menpo/pull/659>

0.6.1 (2015/12/09)
------------------

Fix a nasty bug pertaining to a Diamond inheritance problem in PCA. Add the Gaussion Markov Random Field (GRMF) model. Also a couple of other bugfixes for visualization.

### Github Pull Requests

-   [\#658](https://github.com/menpo/menpo/pull/658) PCA Diamond problem fix (@patricksnape)
-   [\#655](https://github.com/menpo/menpo/pull/655) Bugfix and improvements in visualize package (@nontas)
-   [\#656](https://github.com/menpo/menpo/pull/656) print\_dynamic bugfix (@nontas)
-   [\#635](https://github.com/menpo/menpo/pull/635) Gaussian Markov Random Field (@nontas, @patricksnape)

0.6.0 (2015/11/26)
------------------

This release is another set of breaking changes for Menpo. All `in_place` methods have been deprecated to make the API clearer (always copy). The largest change is the removal of all widgets into a subpackage called [menpowidgets](https://github.com/menpo/menpowidgets). To continue using widgets within the Jupyter notebook, you should install menpowidgets.

### Breaking Changes

> -   Procrustes analysis now checks for mirroring and disables it by default. This is a change in behaviour.
> -   The `sample_offsets` argument of menpo.image.Image.extract\_patches now expects a numpy array rather than a PointCloud.
> -   All widgets are removed and now exist as part of the [menpowidgets](https://github.com/menpo/menpowidgets) project. The widgets are now only compatible with Jupyter 4.0 and above.
> -   Landmark labellers have been totally refactored and renamed. They have not been deprecated due to the changes. However, the new changes mean that the naming scheme of labels is now much more intuitive. Practically, the usage of labelling has only changed in that now it is possible to label not only LandmarkGroup but also PointCloud and numpy arrays directly.
> -   Landmarks are now warped by default, where previously they were not.
> -   All vlfeat features have now become optional and will not appear if cyvlfeat is not installed.
> -   All `label` keyword arguments have been removed. They were not found to be useful. For the same effect, you can always create a new landmark group that only contains that label and use that as the `group` key.

### New Features

> -   New SIFT type features that return vectors rather than dense features. (menpo.feature.vector\_128\_dsift, menpo.feature.hellinger\_vector\_128\_dsift)
> -   menpo.shape.PointCloud.init\_2d\_grid static constructor for PointCloud and subclasses.
> -   Add PCAVectorModel class that allows performing PCA directly on arrays.
> -   New static constructors on PCA models for building PCA directly from covariance matrices or components (menpo.model.PCAVectorModel.init\_from\_components and menpo.model.PCAVectorModel.init\_from\_covariance\_matrix).
> -   New menpo.image.Image.mirror method on images.
> -   New menpo.image.Image.set\_patches methods on images.
> -   New menpo.image.Image.rotate\_ccw\_about\_centre method on images.
> -   When performing operations on images, you can now add the `return_transform` kwarg that will return both the new image **and** the transform that created the image. This can be very useful for processing landmarks after images have been cropped and rescaled for example.

### Github Pull Requests

-   [\#652](https://github.com/menpo/menpo/pull/652) Deprecate a number of inplace methods (@jabooth)
-   [\#653](https://github.com/menpo/menpo/pull/653) New features (vector dsift) (@patricksnape)
-   [\#651](https://github.com/menpo/menpo/pull/651) remove deprecations from 0.5.0 (@jabooth)
-   [\#650](https://github.com/menpo/menpo/pull/650) PointCloud init\_2d\_grid (@patricksnape)
-   [\#646](https://github.com/menpo/menpo/pull/646) Add ibug\_49 -&gt; ibug\_49 labelling (@patricksnape)
-   [\#645](https://github.com/menpo/menpo/pull/645) Add new PCAVectorModel class, refactor model package (@patricksnape, @nontas)
-   [\#644](https://github.com/menpo/menpo/pull/644) Remove label kwarg (@patricksnape)
-   [\#643](https://github.com/menpo/menpo/pull/643) Build fixes (@patricksnape)
-   [\#638](https://github.com/menpo/menpo/pull/638) bugfix 2D triangle areas sign was ambiguous (@jabooth)
-   [\#634](https://github.com/menpo/menpo/pull/634) Fixing @patricksnape and @nontas foolish errors (@yuxiang-zhou)
-   [\#542](https://github.com/menpo/menpo/pull/542) Add mirroring check to procrustes (@nontas, @patricksnape)
-   [\#632](https://github.com/menpo/menpo/pull/632) Widgets Migration (@patricksnape, @nontas)
-   [\#631](https://github.com/menpo/menpo/pull/631) Optional transform return on Image methods (@nontas)
-   [\#628](https://github.com/menpo/menpo/pull/628) Patches Visualization (@nontas)
-   [\#629](https://github.com/menpo/menpo/pull/629) Image counter-clockwise rotation (@nontas)
-   [\#630](https://github.com/menpo/menpo/pull/630) Mirror image (@nontas)
-   [\#625](https://github.com/menpo/menpo/pull/625) Labellers Refactoring (@patricksnape)
-   [\#623](https://github.com/menpo/menpo/pull/623) Fix widgets for new Jupyter/IPython 4 release (@patricksnape)
-   [\#620](https://github.com/menpo/menpo/pull/620) Define patches offsets as ndarray (@nontas)

0.5.3 (2015/08/12)
------------------

Tiny point release just fixing a typo in the `unique_edge_indices` method.

0.5.2 (2015/08/04)
------------------

Minor bug fixes and impovements including:

> -   Menpo is now better at preserving dtypes other than np.float through common operations
> -   Image has a new convenience constructor `init_from_rolled_channels()` to handle building images that have the channels at the back of the array.
> -   There are also new `crop_to_pointcloud()` and `crop_to_pointcloud_proportion()` methods to round out the Image API, and a deprecation of `rescale_to_reference_shape()` in favour of `rescale_to_pointcloud()` to make things more consistent.
> -   The `gradient()` method is deprecated (use `menpo.feature.gradient` instead)
> -   Propagation of the `.path` property when using `as_masked()` was fixed
> -   Fix for exporting 3D LJSON landmark files
> -   A new `shuffle` kwarg (default `False`) is present on all multi importers.

### Github Pull Requests

-   [\#617](https://github.com/menpo/menpo/pull/617) add shuffle kwarg to multi import generators (@jabooth)
-   [\#619](https://github.com/menpo/menpo/pull/619) Ensure that LJSON landmarks are read in as floats (@jabooth)
-   [\#618](https://github.com/menpo/menpo/pull/618) Small image fix (@patricksnape)
-   [\#613](https://github.com/menpo/menpo/pull/613) Balance out rescale/crop methods (@patricksnape)
-   [\#615](https://github.com/menpo/menpo/pull/615) Allow exporting of 3D landmarks. (@mmcauliffe)
-   [\#612](https://github.com/menpo/menpo/pull/612) Type maintain (@patricksnape)
-   [\#602](https://github.com/menpo/menpo/pull/602) Extract patches types (@patricksnape)
-   [\#608](https://github.com/menpo/menpo/pull/608) Slider for selecting landmark group on widgets (@nontas)
-   [\#605](https://github.com/menpo/menpo/pull/605) tmp move to master condaci (@jabooth)

0.5.1 (2015/07/16)
------------------

A small point release that improves the Cython code (particularly extracting patches) compatibility with different data types. In particular, more floating point data types are now supported. `print_progress` was added and widgets were fixed after the Jupyter 4.0 release. Also, upgrade cyvlfeat requirement to 0.4.0.

### Github Pull Requests

-   [\#604](https://github.com/menpo/menpo/pull/604) print\_progress enhancements (@jabooth)
-   [\#603](https://github.com/menpo/menpo/pull/603) Fixes for new cyvlfeat (@patricksnape)
-   [\#599](https://github.com/menpo/menpo/pull/599) Add erode and dilate methods to MaskedImage (@jalabort)
-   [\#601](https://github.com/menpo/menpo/pull/601) Add sudo: false to turn on container builds (@patricksnape)
-   [\#600](https://github.com/menpo/menpo/pull/600) Human3.6M labels (@nontas)

0.5.0 (2015/06/25)
------------------

This release of Menpo makes a number of very important **BREAKING** changes to the format of Menpo's core data types. Most importantly is [\#524](https://github.com/menpo/menpo/pull/524) which swaps the position of the channels on an image from the last axis to the first. This is to maintain row-major ordering and make iterating over the pixels of a channel efficient. This made a huge improvement in speed in other packages such as MenpoFit. It also makes common operations such as iterating over the pixels in an image much simpler:

``` sourceCode
for channels in image.pixels:
    print(channels.shape)  # This will be a (height x width) ndarray
```

Other important changes include:

> -   Updating all widgets to work with IPython 3
> -   Incremental PCA was added.
> -   non-inplace cropping methods
> -   Dense SIFT features provided by vlfeat
> -   The implementation of graphs was changed to use sparse matrices by default. **This may cause breaking changes.**
> -   Many other improvements detailed in the pull requests below!

If you have serialized data using Menpo, you will likely find you have trouble reimporting it. If this is the case, please visit the user group for advice.

### Github Pull Requests

-   [\#598](https://github.com/menpo/menpo/pull/598) Visualize sum of channels in widgets (@nontas, @patricksnape)
-   [\#597](https://github.com/menpo/menpo/pull/597) test new dev tag behavior on condaci (@jabooth)
-   [\#591](https://github.com/menpo/menpo/pull/591) Scale around centre (@patricksnape)
-   [\#596](https://github.com/menpo/menpo/pull/596) Update to versioneer v0.15 (@jabooth, @patricksnape)
-   [\#495](https://github.com/menpo/menpo/pull/495) SIFT features (@nontas, @patricksnape, @jabooth, @jalabort)
-   [\#595](https://github.com/menpo/menpo/pull/595) Update mean\_pointcloud (@patricksnape, @jalabort)
-   [\#541](https://github.com/menpo/menpo/pull/541) Add triangulation labels for ibug\_face\_(66/51/49) (@jalabort)
-   [\#590](https://github.com/menpo/menpo/pull/590) Fix centre and diagonal being properties on Images (@patricksnape)
-   [\#592](https://github.com/menpo/menpo/pull/592) Refactor out bounding\_box method (@patricksnape)
-   [\#566](https://github.com/menpo/menpo/pull/566) TriMesh utilities (@jabooth)
-   [\#593](https://github.com/menpo/menpo/pull/593) Minor bugfix on AnimationOptionsWidget (@nontas)
-   [\#587](https://github.com/menpo/menpo/pull/587) promote non-inplace crop methods, crop performance improvements (@jabooth, @patricksnape)
-   [\#586](https://github.com/menpo/menpo/pull/586) fix as\_matrix where the iterator finished early (@jabooth)
-   [\#574](https://github.com/menpo/menpo/pull/574) Widgets for IPython3 (@nontas, @patricksnape, @jabooth)
-   [\#588](https://github.com/menpo/menpo/pull/588) test condaci 0.2.1, less noisy slack notifications (@jabooth)
-   [\#568](https://github.com/menpo/menpo/pull/568) rescale\_pixels() for rescaling the range of pixels (@jabooth)
-   [\#585](https://github.com/menpo/menpo/pull/585) Hotfix: suffix change led to double path resolution. (@patricksnape)
-   [\#581](https://github.com/menpo/menpo/pull/581) Fix the landmark importer in case the landmark file has a '.' in its filename. (@grigorisg9gr)
-   [\#584](https://github.com/menpo/menpo/pull/584) new print\_progress visualization function (@jabooth)
-   [\#580](https://github.com/menpo/menpo/pull/580) export\_pickle now ensures pathlib.Path save as PurePath (@jabooth)
-   [\#582](https://github.com/menpo/menpo/pull/582) New readers for Middlebury FLO and FRGC ABS files (@patricksnape)
-   [\#579](https://github.com/menpo/menpo/pull/579) Fix the image importer in case of upper case letters in the suffix (@grigorisg9gr)
-   [\#575](https://github.com/menpo/menpo/pull/575) Allowing expanding user paths in exporting pickle (@patricksnape)
-   [\#577](https://github.com/menpo/menpo/pull/577) Change to using run\_test.py (@patricksnape)
-   [\#570](https://github.com/menpo/menpo/pull/570) Zoom (@jabooth, @patricksnape)
-   [\#569](https://github.com/menpo/menpo/pull/569) Add new point\_in\_pointcloud kwarg to constrain (@patricksnape)
-   [\#563](https://github.com/menpo/menpo/pull/563) TPS Updates (@patricksnape)
-   [\#567](https://github.com/menpo/menpo/pull/567) Optional cmaps (@jalabort)
-   [\#559](https://github.com/menpo/menpo/pull/559) Graphs with isolated vertices (@nontas)
-   [\#564](https://github.com/menpo/menpo/pull/564) Bugfix: PCAModel print (@nontas)
-   [\#565](https://github.com/menpo/menpo/pull/565) fixed minor typo in introduction.rst (@evanjbowling)
-   [\#562](https://github.com/menpo/menpo/pull/562) IPython3 widgets (@patricksnape, @jalabort)
-   [\#558](https://github.com/menpo/menpo/pull/558) Channel roll (@patricksnape)
-   [\#524](https://github.com/menpo/menpo/pull/524) BREAKING CHANGE: Channels flip (@patricksnape, @jabooth, @jalabort)
-   [\#512](https://github.com/menpo/menpo/pull/512) WIP: remove\_all\_landmarks convienience method, quick lm filter (@jabooth)
-   [\#554](https://github.com/menpo/menpo/pull/554) Bugfix:visualize\_images (@nontas)
-   [\#553](https://github.com/menpo/menpo/pull/553) Transform docs fixes (@nontas)
-   [\#533](https://github.com/menpo/menpo/pull/533) LandmarkGroup.init\_with\_all\_label, init\_\* convenience constructors (@jabooth, @patricksnape)
-   [\#552](https://github.com/menpo/menpo/pull/552) Many fixes for Python 3 support (@patricksnape)
-   [\#532](https://github.com/menpo/menpo/pull/532) Incremental PCA (@patricksnape, @jabooth, @jalabort)
-   [\#528](https://github.com/menpo/menpo/pull/528) New as\_matrix and from\_matrix methods (@patricksnape)

0.4.4 (2015/03/05)
------------------

A hotfix release for properly handling nan values in the landmark formats. Also, a few other bug fixes crept in:

> -   Fix 3D Ljson importing
> -   Fix trim\_components on PCA
> -   Fix setting None key on the landmark manager
> -   Making mean\_pointcloud faster

Also makes an important change to the build configuration that syncs this version of Menpo to IPython 2.x.

### Github Pull Requests

-   [\#560](https://github.com/menpo/menpo/pull/560) Assorted fixes (@patricksnape)
-   [\#557](https://github.com/menpo/menpo/pull/557) Ljson nan fix (@patricksnape)

0.4.3 (2015/02/19)
------------------

Adds the concept of nan values to the landmarker format for labelling missing landmarks.

### Github Pull Requests

-   [\#556](https://github.com/menpo/menpo/pull/556) \[0.4.x\] Ljson nan/null fixes (@patricksnape)

0.4.2 (2015/02/19)
------------------

A hotfix release for landmark groups that have no connectivity.

### Github Pull Requests

-   [\#555](https://github.com/menpo/menpo/pull/555) don't try and build a Graph with no connectivity (@jabooth)

0.4.1 (2015/02/07)
------------------

A hotfix release to enable compatibility with landmarker.io.

### Github Pull Requests

-   [\#551](https://github.com/menpo/menpo/pull/551) HOTFIX: remove incorrect tojson() methods (@jabooth)

0.4.0 (2015/02/04)
------------------

The 0.4.0 release (pending any currently unknown bugs), represents a very significant overhaul of Menpo from v0.3.0. In particular, Menpo has been broken into four distinct packages: Menpo, MenpoFit, Menpo3D and MenpoDetect.

Visualization has had major improvements for 2D viewing, in particular through the use of IPython widgets and explicit options on the viewing methods for common tasks (like changing the landmark marker color). This final release is a much smaller set of changes over the alpha releases, so please check the full changelog for the alphas to see all changes from v0.3.0 to v0.4.0.

**Summary of changes since v0.4.0a2**:

> -   Lots of documentation rendering fixes and style fixes including this changelog.
> -   Move the LJSON format to V2. V1 is now being deprecated over the next version.
> -   More visualization customization fixes including multiple marker colors for landmark groups.

### Github Pull Requests

-   [\#546](https://github.com/menpo/menpo/pull/546) IO doc fixes (@jabooth)
-   [\#545](https://github.com/menpo/menpo/pull/545) Different marker colour per label (@nontas)
-   [\#543](https://github.com/menpo/menpo/pull/543) Bug fix for importing an image, case of a dot in image name. (@grigorisg9gr)
-   [\#544](https://github.com/menpo/menpo/pull/544) Move docs to Sphinx 1.3b2 (@patricksnape)
-   [\#536](https://github.com/menpo/menpo/pull/536) Docs fixes (@patricksnape)
-   [\#530](https://github.com/menpo/menpo/pull/530) Visualization and Widgets upgrade (@patricksnape, @nontas)
-   [\#540](https://github.com/menpo/menpo/pull/540) LJSON v2 (@jabooth)
-   [\#537](https://github.com/menpo/menpo/pull/537) fix BU3DFE connectivity, pretty JSON files (@jabooth)
-   [\#529](https://github.com/menpo/menpo/pull/529) BU3D-FE labeller added (@jabooth)
-   [\#527](https://github.com/menpo/menpo/pull/527) fixes paths for pickle importing (@jabooth)
-   [\#525](https://github.com/menpo/menpo/pull/525) Fix .rst doc files, auto-generation script (@jabooth)

v0.4.0a2 (2014/12/03)
---------------------

Alpha 2 moves towards extending the graphing API so that visualization is more dependable.

**Summary:**

> -   Add graph classes, PointUndirectedGraph, PointDirectedGraph, PointTree. This makes visualization of landmarks much nicer looking.
> -   Better support of pickling menpo objects
> -   Add a bounding box method to PointCloud for calculating the correctly oriented bounding box of point clouds.
> -   Allow PCA to operate in place for large data matrices.

### Github Pull Requests

-   [\#522](https://github.com/menpo/menpo/pull/522) Add bounding box method to pointclouds (@patricksnape)
-   [\#523](https://github.com/menpo/menpo/pull/523) HOTFIX: fix export\_pickle bug, add path support (@jabooth)
-   [\#521](https://github.com/menpo/menpo/pull/521) menpo.io add pickle support, move to pathlib (@jabooth)
-   [\#520](https://github.com/menpo/menpo/pull/520) Documentation fixes (@patricksnape, @jabooth)
-   [\#518](https://github.com/menpo/menpo/pull/518) PCA memory improvements, inplace dot product (@jabooth)
-   [\#519](https://github.com/menpo/menpo/pull/519) replace wrapt with functools.wraps - we can pickle (@jabooth)
-   [\#517](https://github.com/menpo/menpo/pull/517) (@jabooth)
-   [\#514](https://github.com/menpo/menpo/pull/514) Remove the use of triplot (@patricksnape)
-   [\#516](https://github.com/menpo/menpo/pull/516) Fix how images are converted to PIL (@patricksnape)
-   [\#515](https://github.com/menpo/menpo/pull/515) Show the path in the image widgets (@patricksnape)
-   [\#511](https://github.com/menpo/menpo/pull/511) 2D Rotation convenience constructor, Image.rotate\_ccw\_about\_centre (@jabooth)
-   [\#510](https://github.com/menpo/menpo/pull/510) all menpo io glob operations are now always sorted (@jabooth)
-   [\#508](https://github.com/menpo/menpo/pull/508) visualize image on MaskedImage reports Mask proportion (@jabooth)
-   [\#509](https://github.com/menpo/menpo/pull/509) path is now preserved on image warping (@jabooth)
-   [\#507](https://github.com/menpo/menpo/pull/507) fix rounding issue in n\_components (@jabooth)
-   [\#506](https://github.com/menpo/menpo/pull/506) is\_tree update in Graph (@nontas)
-   [\#505](https://github.com/menpo/menpo/pull/505) (@nontas)
-   [\#504](https://github.com/menpo/menpo/pull/504) explicitly have kwarg in IO for landmark extensions (@jabooth)
-   [\#503](https://github.com/menpo/menpo/pull/503) Update the README (@patricksnape)

v0.4.0a1 (2014/10/31)
---------------------

This first alpha release makes a number of large, breaking changes to Menpo from v0.3.0. The biggest change is that Menpo3D and MenpoFit were created and thus all AAM and 3D visualization/rasterization code has been moved out of the main Menpo repository. This is working towards Menpo being pip installable.

**Summary:**

> -   Fixes memory leak whereby weak references were being kept between landmarks and their host objects. The Landmark manager now no longer keeps references to its host object. This also helps with serialization.
> -   Use pathlib instead of strings for paths in the `io` module.
> -   Importing of builtin assets from a simple function
> -   Improve support for image importing (including ability to import without normalising)
> -   Add fast methods for image warping, `warp_to_mask` and `warp_to_shape` instead of `warp_to`
> -   Allow masking of triangle meshes
> -   Add IPython visualization widgets for our core types
> -   All expensive properties (properties that would be worth caching in a variable and are not merely a lookup) are changed to methods.

### Github Pull Requests

-   [\#502](https://github.com/menpo/menpo/pull/502) Fixes pseudoinverse for Alignment Transforms (@jalabort, @patricksnape)
-   [\#501](https://github.com/menpo/menpo/pull/501) Remove menpofit widgets (@nontas)
-   [\#500](https://github.com/menpo/menpo/pull/500) Shapes widget (@nontas)
-   [\#499](https://github.com/menpo/menpo/pull/499) spin out AAM, CLM, SDM, ATM and related code to menpofit (@jabooth)
-   [\#498](https://github.com/menpo/menpo/pull/498) Minimum spanning tree bug fix (@nontas)
-   [\#492](https://github.com/menpo/menpo/pull/492) Some fixes for PIL image importing (@patricksnape)
-   [\#494](https://github.com/menpo/menpo/pull/494) Widgets bug fix and Active Template Model widget (@nontas)
-   [\#491](https://github.com/menpo/menpo/pull/491) Widgets fixes (@nontas)
-   [\#489](https://github.com/menpo/menpo/pull/489) remove \_view, fix up color\_list -&gt; colour\_list (@jabooth)
-   [\#486](https://github.com/menpo/menpo/pull/486) Image visualisation improvements (@patricksnape)
-   [\#488](https://github.com/menpo/menpo/pull/488) Move expensive image properties to methods (@jabooth)
-   [\#487](https://github.com/menpo/menpo/pull/487) Change expensive PCA properties to methods (@jabooth)
-   [\#485](https://github.com/menpo/menpo/pull/485) MeanInstanceLinearModel.mean is now a method (@jabooth)
-   [\#452](https://github.com/menpo/menpo/pull/452) Advanced widgets (@patricksnape, @nontas)
-   [\#481](https://github.com/menpo/menpo/pull/481) Remove 3D (@patricksnape)
-   [\#480](https://github.com/menpo/menpo/pull/480) Graphs functionality (@nontas)
-   [\#479](https://github.com/menpo/menpo/pull/479) Extract patches on image (@patricksnape)
-   [\#469](https://github.com/menpo/menpo/pull/469) Active Template Models (@nontas)
-   [\#478](https://github.com/menpo/menpo/pull/478) Fix residuals for AAMs (@patricksnape, @jabooth)
-   [\#474](https://github.com/menpo/menpo/pull/474) remove HDF5able making room for h5it (@jabooth)
-   [\#475](https://github.com/menpo/menpo/pull/475) Normalize norm and std of Image object (@nontas)
-   [\#472](https://github.com/menpo/menpo/pull/472) Daisy features (@nontas)
-   [\#473](https://github.com/menpo/menpo/pull/473) Fix from\_mask for Trimesh subclasses (@patricksnape)
-   [\#470](https://github.com/menpo/menpo/pull/470) expensive properties should really be methods (@jabooth)
-   [\#467](https://github.com/menpo/menpo/pull/467) get a progress bar on top level feature computation (@jabooth)
-   [\#466](https://github.com/menpo/menpo/pull/466) Spin out rasterization and related methods to menpo3d (@jabooth)
-   [\#465](https://github.com/menpo/menpo/pull/465) 'me\_norm' error type in tests (@nontas)
-   [\#463](https://github.com/menpo/menpo/pull/463) goodbye ioinfo, hello path (@jabooth)
-   [\#464](https://github.com/menpo/menpo/pull/464) make mayavi an optional dependency (@jabooth)
-   [\#447](https://github.com/menpo/menpo/pull/447) Displacements in fitting result (@nontas)
-   [\#451](https://github.com/menpo/menpo/pull/451) AppVeyor Windows continuous builds from condaci (@jabooth)
-   [\#445](https://github.com/menpo/menpo/pull/445) Serialize fit results (@patricksnape)
-   [\#444](https://github.com/menpo/menpo/pull/444) remove pyramid\_on\_features from Menpo (@jabooth)
-   [\#443](https://github.com/menpo/menpo/pull/443) create\_pyramid now applies features even if pyramid\_on\_features=False, SDM uses it too (@jabooth)
-   [\#369](https://github.com/menpo/menpo/pull/369) warp\_to\_mask, warp\_to\_shape, fast resizing of images (@nontas, @patricksnape, @jabooth)
-   [\#442](https://github.com/menpo/menpo/pull/442) add rescale\_to\_diagonal, diagonal property to Image (@jabooth)
-   [\#441](https://github.com/menpo/menpo/pull/441) adds constrain\_to\_landmarks on BooleanImage (@jabooth)
-   [\#440](https://github.com/menpo/menpo/pull/440) pathlib.Path can no be used in menpo.io (@jabooth)
-   [\#439](https://github.com/menpo/menpo/pull/439) Labelling fixes (@jabooth, @patricksnape)
-   [\#438](https://github.com/menpo/menpo/pull/438) extract\_channels (@jabooth)
-   [\#437](https://github.com/menpo/menpo/pull/437) GLRasterizer becomes HDF5able (@jabooth)
-   [\#435](https://github.com/menpo/menpo/pull/435) import\_builtin\_asset.ASSET\_NAME (@jabooth)
-   [\#434](https://github.com/menpo/menpo/pull/434) check\_regression\_features unified with check\_features, classmethods removed from SDM (@jabooth)
-   [\#433](https://github.com/menpo/menpo/pull/433) tidy classifiers (@jabooth)
-   [\#432](https://github.com/menpo/menpo/pull/432) aam.fitter, clm.fitter, sdm.trainer packages (@jabooth)
-   [\#431](https://github.com/menpo/menpo/pull/431) More fitmultilevel tidying (@jabooth)
-   [\#430](https://github.com/menpo/menpo/pull/430) Remove classmethods from DeformableModelBuilder (@jabooth)
-   [\#412](https://github.com/menpo/menpo/pull/412) First visualization widgets (@jalabort, @nontas)
-   [\#429](https://github.com/menpo/menpo/pull/429) Masked image fixes (@patricksnape)
-   [\#426](https://github.com/menpo/menpo/pull/426) rename 'feature\_type' to 'features throughout Menpo (@jabooth)
-   [\#427](https://github.com/menpo/menpo/pull/427) Adds HDF5able serialization support to Menpo (@jabooth)
-   [\#425](https://github.com/menpo/menpo/pull/425) Faster cached piecewise affine, Cython varient demoted (@jabooth)
-   [\#424](https://github.com/menpo/menpo/pull/424) (@nontas)
-   [\#378](https://github.com/menpo/menpo/pull/378) Fitting result fixes (@jabooth, @nontas, @jalabort)
-   [\#423](https://github.com/menpo/menpo/pull/423) name now displays on constrained features (@jabooth)
-   [\#421](https://github.com/menpo/menpo/pull/421) Travis CI now makes builds, Linux/OS X Python 2.7/3.4 (@jabooth, @patricksnape)
-   [\#400](https://github.com/menpo/menpo/pull/400) Features as functions (@nontas, @patricksnape, @jabooth)
-   [\#420](https://github.com/menpo/menpo/pull/420) move IOInfo to use pathlib (@jabooth)
-   [\#405](https://github.com/menpo/menpo/pull/405) import menpo is now twice as fast (@jabooth)
-   [\#416](https://github.com/menpo/menpo/pull/416) waffle.io Badge (@waffle-iron)
-   [\#415](https://github.com/menpo/menpo/pull/415) export\_mesh with .OBJ exporter (@jabooth, @patricksnape)
-   [\#410](https://github.com/menpo/menpo/pull/410) Fix the render\_labels logic (@patricksnape)
-   [\#407](https://github.com/menpo/menpo/pull/407) Exporters (@patricksnape)
-   [\#406](https://github.com/menpo/menpo/pull/406) Fix greyscale PIL images (@patricksnape)
-   [\#404](https://github.com/menpo/menpo/pull/404) LandmarkGroup tojson method and PointGraph (@patricksnape)
-   [\#403](https://github.com/menpo/menpo/pull/403) Fixes a couple of viewing problems in fitting results (@patricksnape)
-   [\#402](https://github.com/menpo/menpo/pull/402) Landmarks fixes (@jabooth, @patricksnape)
-   [\#401](https://github.com/menpo/menpo/pull/401) Dogfood landmark\_resolver in menpo.io (@jabooth)
-   [\#399](https://github.com/menpo/menpo/pull/399) bunch of Python 3 compatibility fixes (@jabooth)
-   [\#398](https://github.com/menpo/menpo/pull/398) throughout Menpo. (@jabooth)
-   [\#397](https://github.com/menpo/menpo/pull/397) Performance improvements for Similarity family (@jabooth)
-   [\#396](https://github.com/menpo/menpo/pull/396) More efficient initialisations of Menpo types (@jabooth)
-   [\#395](https://github.com/menpo/menpo/pull/395) remove cyclic target reference from landmarks (@jabooth)
-   [\#393](https://github.com/menpo/menpo/pull/393) Groundwork for dense correspondence pipeline (@jabooth)
-   [\#394](https://github.com/menpo/menpo/pull/394) weakref to break cyclic references (@jabooth)
-   [\#389](https://github.com/menpo/menpo/pull/389) assorted fixes (@jabooth)
-   [\#390](https://github.com/menpo/menpo/pull/390) (@jabooth)
-   [\#387](https://github.com/menpo/menpo/pull/387) Adds landmark label for tongues (@nontas)
-   [\#386](https://github.com/menpo/menpo/pull/386) Adds labels for the ibug eye annotation scheme (@jalabort)
-   [\#382](https://github.com/menpo/menpo/pull/382) BUG fixed: block element not reset if norm=0 (@dubzzz)
-   [\#381](https://github.com/menpo/menpo/pull/381) Recursive globbing (@jabooth)
-   [\#384](https://github.com/menpo/menpo/pull/384) Adds support for odd patch shapes in function extract\_local\_patches\_fast (@jalabort)
-   [\#379](https://github.com/menpo/menpo/pull/379) imported textures have ioinfo, docs improvements (@jabooth)

v0.3.0 (2014/05/27)
-------------------

First public release of Menpo, this release coincided with submission to the ACM Multimedia Open Source Software Competition 2014. This provides the basic scaffolding for Menpo, but it is not advised to use this version over the improvements in 0.4.0.

### Github Pull Requests

-   [\#377](https://github.com/menpo/menpo/pull/377) Simple fixes (@patricksnape)
-   [\#375](https://github.com/menpo/menpo/pull/375) improvements to importing multiple assets (@jabooth)
-   [\#374](https://github.com/menpo/menpo/pull/374) Menpo's User guide (@jabooth)

