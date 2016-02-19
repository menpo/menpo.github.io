The Menpo Project
=================

The Menpo Project is a collection of high quality open-source research software that provides end-to-end solution for 2D and 3D deformable modeling. The Menpo Project is composed of a number of components, each one designed to solve one problem well:

#### Menpo (`import menpo`)
At the heart of the Menpo Project is the Python package Menpo. Menpo contains all core functionality needed for the project in well tested, mature, stable package. `menpo` is the `numpy` of the Menpo ecosystem - the foundation upon which all else is built.

#### MenpoFit (`import menpofit`)
MenpoFit contains implementations of state of the art 2D deformable models, including Active Appearance Models, Constrained Local Models, and Supervised Decent Method. Each implementation includes training and fitting code. MenpoFit contains the crown jewels of the Menpo Project - most people are interested in using the Menpo Project for the `menpofit` package.
Naturally, `menpofit` is built using the building blocks found in `menpo`.

#### MenpoDetect (`import menpodetect`)
MenpoDetect contains detection methods.
`menpodetect` works on and returns images and landmarks defined in `menpo`.

#### Menpo3D (`import menpo3d`)
Menpo3D is a specialized library for working with 3D data. It is largely separate from the core `menpo` library as it has dependencies on a number of large, 3D specific projects (like VTK, mayavi, assimp) which many people using the Menpo Project would have no use for. You'll want to install `menpo3d` if you need to import and export 3D mesh data or perform advanced mesh processing.

#### Landmarker.io ([www.landmarker.io](https://www.landmarker.io))
- An interactive tool to place landmarks on images and meshes
  - Quickly landmark a single image, or organize a large annotation effort for thousands of files

# Motivation

## The Menpo Team

The Menpo Team are a group of researchers from the Intelligent Behavior Understandings Group (iBUG) in the Department of Computing, Imperial College London. Follow [@teammenpo](www.twitter.com/teammenpo) for updates on the Menpo Project, or tweet at us any questions you have.

## What kinds of problems does the Menpo Team work on?

Although each member of the Menpo Team is perusing an individual research direction, there are many areas where their research overlaps. All members are working in Computer Vision, and most in some form of 2D or 3D deformable modeling.
This means that all researchers in the team need to solve similar problems, and as a result, we wanted to build tools that made the following kinds of tasks easy:

#### Working with landmarks
- Attach *landmarks* - sparse spatial points with semantic meaning - to images and 2D and 3D shapes
- Import and export a range landmark file formats produced by different research groups

#### Working with images
- Import and export a range of image file formats
- Perform common image operations  (e.g. resizing, cropping, masking, warping)
  - Perform these in the context of having landmarks (e.g. crop around a set of landmarks to retain only the part of an image that is of interest)
- Extract features like SIFT, HOG, IGO on images
- For all image operations, track how any landmarks on an image are transformed

#### Working with shapes
- Import and export a range of 3D mesh file formats
- Represent a range of spatial datatypes, like pointclouds, triangle meshes, and directed and undirected graphs
  - Have n-dimensional representations where possible, so code can be reused for 2D and 3D cases
- Perform spatial transformations to shapes (translate, rotate, affine warp, Thin Plate Spline warp)
  - For all transformations, track how any landmarks on a shape are transformed

#### Linear algebra on data
- An ability to reliably move between a linear algebra parameterization of some data (an array of values) to a rich representation that is useful for interactive work (an object with methods)
- Perform statistical modeling on images and shapes (Principal Component Analysis)

The above requirements are the building blocks of the kind of deformable modeling research our team does. If we had a codebase that implemented all of these features well, it would be easy to express a wide variety of computer vision and deformable modeling problems.

## Engineering goals

Outside of the raw features needed, the team also needed flexible software that could be relied upon. That meant:

- The ability to work in an interactive environment where new research ideas can be quickly explored
- Cross platform (Linux, OS X, Windows)
- One click install and removal. No outside dependencies needed.
- Extensively tested and documented

It's from these requirements, and a desire by the team to make high quality open source research software, that the Menpo Project was born.

# This Book

This book focuses on explaining the core Menpo abstractions and datatypes which are heavily reused throughout all of the Menpo Project. If you are new to the project, this book is the best way to quickly get up to speed with how to use Menpo.

As is hopefully now clear, the core concepts and datatypes defined in `menpo` are reused across all of the Menpo Project. We've worked hard to keep this core API as compact as possible, as we know from experience it's never pleasant trying to get to grips with another projects sprawling API and design patterns if you just want to get a job done.

The rest of this book is devoted to getting you to grips with the core `menpo` concepts and abstractions as quickly as possible. If you are at all interested in using any part of the Menpo Project, the 15 minutes it will take you to read through this book will be hugely beneficial to getting started quickly.

There will be examples throughout, and in fact all future pages of this book will be generated from an IPython notebook, so you can install Menpo, and follow along, trying and tweaking examples as you go.

As a final note, if you are only interested in using Menpo as a black box for some of the MenpoFit functionality, you are invited to checkout `menpocli`, our Command Line Interface. This is a cross platform set of executables for performing landmark detection on images, and requires no knowledge of Python or the rest of this book.

### API Reference

This book is one of two parts of Menpo's documentation, the other being the [API Reference](http://docs.menpo.org/en/stable/). The API Reference is a complete technical description about how every function and method operates in Menpo ([example](http://docs.menpo.org/en/stable/api/menpo/io/import_images.html)). The API Reference is the place to go if you want to know exactly how an individual component functions in Menpo.

The API Reference is generated from docstrings in the source code, so you can also use the `?` IPython magic to check the documentation of a function whilst working interactively:
```py
import menpo
menpo.io.import_images?<Enter>
```
