Manifesto
=========
These are the main goals of the Menpo Team and the motivation behind creating and maintaining the Menpo Project.
If you want to know about:

* [What kinds of problems the Menpo Team is working on](#problems)
* [What makes the Menpo Project better than other related open-source software](#menpo_is_better)
* [Our engineering goals](#engineering)
* [The purpose of this website](#website)

then keep reading!

---------------------------------------

### <a name="problems"></a>What kinds of problems does the Menpo Team work on?
Although each member of the Menpo Team is perusing an individual research direction, there are many areas where their research overlaps. All members are working in Computer Vision, and most in some form of 2D or 3D deformable modeling.
This means that all researchers in the team need to solve similar problems, and as a result, we wanted to build tools that made the following kinds of tasks easy:

##### Working with landmarks
- Attach *landmarks* - sparse spatial points with semantic meaning - to images and 2D and 3D shapes
- Import and export a range of landmark file formats produced by different research groups

##### Working with images
- Import and export a range of image and video file formats
- Perform common image operations  (e.g. resizing, cropping, masking, warping)
  - Perform these in the context of having landmarks (e.g. crop around a set of landmarks to retain only the part of an image that is of interest)
- Extract features like SIFT, HOG, IGO on images
- For all image operations, track how any landmarks on an image are transformed

##### Working with shapes
- Import and export a range of 3D mesh file formats
- Represent a range of spatial datatypes, like pointclouds, triangle meshes, and directed and undirected graphs
  - Have n-dimensional representations where possible, so code can be reused for 2D and 3D cases
- Perform spatial transformations to shapes (translate, rotate, affine warp, Thin Plate Spline warp)
  - For all transformations, track how any landmarks on a shape are transformed

##### Linear algebra on data
- An ability to reliably move between a linear algebra parameterization of some data (an array of values) to a rich representation that is useful for interactive work (an object with methods)
- Perform statistical modeling on images and shapes (Principal Component Analysis)

The above requirements are the building blocks of the kind of deformable modeling research our team does.



### <a name="menpo_is_better"></a>What makes the Menpo Project better?
The [`menpo`](/menpo/index.md) package is a solid codebase that implements all of the above features well and makes it easy to
express a wide variety of computer vision and deformable modeling problems.
The vast majority of **existing deformable modeling software** suffers from one or more of the following
important issues:
* It is released in binary closed-source format
* It does not come with training code; only pre-trained models
* It is not well-structured which makes it very difficult to tweak and alter
* It only focuses on a single method/model

[`menpofit`](/menpofit/index.md) overcomes the above issues by providing open-source training and fitting
code for multiple state-of-the-art deformable models under a unified protocol.
We **strongly** believe that this is the only way towards reproducable and
high-quality research.



### <a name="engineering"></a>Engineering goals
Outside of the raw features needed, the team also needed flexible software that could be relied upon. That meant:

- The ability to work in an interactive environment where new research ideas can be quickly explored
- Cross platform (Linux, macOS, Windows)
- One click install and removal. No outside dependencies needed.
- Extensively tested and documented

It's from these requirements, and a desire by the team to make high quality open source research software, that the Menpo Project was born.



### <a name="website"></a>This website
This website focuses on explaining the core abstractions and datatypes which are heavily reused throughout all of the Menpo Project. If you are new to the project, this website is the best way to quickly get up to speed with how to use the Menpo Project.

As is hopefully now clear, the core concepts and datatypes defined in [`menpo`](/menpo/index.md) are reused across all of the Menpo Project. We've worked hard to keep this core API as compact as possible, as we know from experience it's never pleasant trying to get to grips with another projects sprawling API and design patterns if you just want to get a job done.

The rest of this website is devoted to getting you to grips with the core [`menpo`](/menpo/index.md) concepts and abstractions as quickly as possible. If you are at all interested in using any part of the Menpo Project, the 15 minutes it will take you to read through this website will be hugely beneficial to getting started quickly. Then we provide the same descriptions for [`menpofit`](/menpofit/index.md), [`menpodetect`](/menpodetect/index.md), [`menpowidgets`](/menpowidgets/index.md) and [`menpo3d`](/menpo3d/index.md).

There will be examples throughout which you could try out and tweak as you go.

As a final note, if you are only interested in using the Menpo Project as a black box for some of the [`menpofit`](/menpofit/index.md) functionality, you are invited to checkout [`menpocli`](/menpocli/index.md), our Command Line Interface. This is a cross platform set of executables for performing landmark detection on **facial** images, and requires no knowledge of Python or the rest of this website.
