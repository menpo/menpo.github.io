<link rel="stylesheet" type="text/css"  href="menpostyle.css">
<center>
  <div class="hero_container">
    <div class="hero_logo_container">
      <img class="hero_logo" src="logo/menpoproject.png" alt="The Menpo Project">
    </div>
    <div class="hero_rightcolumn">
      <div>
        <strong style="font-size: 200%; font-family: 'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif; font-weight: 500;">The Menpo Project</strong>
        <div style="max-width: 200px;">The Python framework for deformable modelling</div>
      </div>
      <div style="display: flex; flex-direction: row; align-items: center;">
        <div style="width: 30px; height: 30px;"></div>
        <a style="text-decoration: none; color: grey" href="installation/playground.html">
          <button class="download_button">Download Playground</button>
        </a>
        <button class="playground_help">
          ?
          <div class="playground_help_speach"></div>
          <div class="playground_help_popup">
            <p>A playground is a standalone installation of menpo that will get you up and running as quickly as possible.</p>
            <p>If you are new to menpo or Python in general you may want to start with the playground.</p>
            <p>Head to our <a style="font-weight: bold; color: white;" href="installation">installation page</a> for more options.</p>
          </div>
        </button>
      </div>
      <div>
        <div style="font-size: 80%">comfortable with <a href="http://conda.pydata.org">conda</a>?</div>
        <code style="padding: 7px;">conda install -c menpo menpoproject</code>
        <div style="font-size: 80%; margin-top: 10px;"><a href="installation">more install options (inc. pip)</a></div>
      </div>
    </div>
  </div>
</center>
<br>
<!---
MAIN DESCRIPTION
-->
The Menpo Project is a set of BSD 3-Clause licensed Python frameworks and associated tooling that provide end-to-end solutions for 2D and 3D deformable modeling. The project includes training and fitting code for various state-of-the-art methods such as:

* Active Appearance Model (AAM)
* Supervised Descent Method (SDM)
* Ensemble of Regression Trees (ERT) (powered by [dlib](http://dlib.net/ "dlib C++ Library"))
* Constrained Local Model (CLM)
* Active Shape Model (ASM)
* Active Pictorial Structures (APS)
* Lucas-Kanade (LK) and Active Template Model (ATM)

The Menpo Project also provides:
* a web-based tool for **annotation of bulk data** for model training
* a **command line tool** for landmark localisation with state-of-the-art **pre-trained** models
* generic **object detection** in terms of a bounding box
* an **elegant standard library** with simple dependencies, useful for many areas of computer vision
* sophisticated visualization with **interactive IPython/Jupyter widgets**

All of the code is Open Source and can be found over on the [Menpo Github Organisation](https://github.com/menpo/ "The Menpo Project on Github").

---------------------------------------

## Packages

The Menpo project is a consists of a family of packages (primarily Python), each designed to solve one problem well:

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/menpo/index.md" title="menpo"><img style="max-height: 140px; max-width: none;" src="logo/menpo.png" alt="menpo"></a>
</p>
<p><a href="/menpo/index.md" title="menpo"><strong style="font-size: 125%">menpo</strong></a>
The heart of the Menpo Project. <code>menpo</code> contains all core functionality needed for the project in well tested, mature, stable package.
<code>menpo</code> is the <code>numpy</code> of the Menpo ecosystem - the foundation upon which all else is built. Even if you aren't interested
in deformable modelling, <code>menpo</code>'s minimal dependencies and general algorthims and data structures makes it an ideal standalone library
for use in a wide variety of Computer Vision situations.</p>
</div>

<div style="clear: both;"></div>

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/menpofit/index.md" title="menpofit"><img style="max-height: 140px; max-width: none;" src="logo/menpofit.png" alt="menpofit"></a>
</p>
<p><a href="/menpofit/index.md" title="menpofit"><strong style="font-size: 125%">menpofit</strong></a>
Implementations of state-of-the-art 2D deformable models. Each implementation includes training and fitting code.
<code>menpofit</code> contains the crown jewels of the Menpo Project - most people are interested in using the Menpo Project for the
<code>menpofit</code> package.</p>
</div>

<div style="clear: both;"></div>

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/menpodetect/index.md" title="menpodetect"><img style="max-height: 140px; max-width: none;" src="logo/menpodetect.png" alt="menpodetect"></a>
</p>
<p><a href="/menpodetect/index.md" title="menpodetect"><strong style="font-size: 125%">menpodetect</strong></a>
Wraps a number of existing projects that provide functionalities for training and fitting generic object detection techniques.
It is designed in order to have full compatibility with <code>menpofit</code>. Not all of the wrapped
projects fall under the same BSD license and so care must be taken when using this project to adhere to the sub-project licenses.</p>
</div>

<div style="clear: both;"></div>

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/menpo3d/index.md" title="menpo3d"><img style="max-height: 140px; max-width: none;" src="logo/menpo3d.png" alt="menpo3d"></a>
</p>
<p><a href="/menpo3d/index.md" title="menpo3d"><strong style="font-size: 125%">menpo3d</strong></a>
A specialized library for working with 3D data. It is largely separate from the core <code>menpo</code> library as it has
dependencies on a number of large, 3D specific projects (like <code>VTK</code>, <code>mayavi</code>, <code>assimp</code>) which many people using
the Menpo Project would have no use for. You'll want to install <code>menpo3d</code> if you need to import and export 3D mesh data or perform advanced mesh processing.</p>
</div>

<div style="clear: both;"></div>

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/menpowidgets/index.md" title="menpowidgets"><img style="max-height: 140px; max-width: none;" src="logo/menpowidgets.png" alt="menpowidgets"></a>
</p>
<p><a href="/menpowidgets/index.md" title="menpowidgets"><strong style="font-size: 125%">menpowidgets</strong></a>
A key goal of the Menpo Project is to accelerate research in 2D and 3D computer vision by providing powerful visualization tools.
<code>menpowidgets</code> contains a collection of Jupyter Notebook Widgets for sophisticated visualization and interactive
inspection of the state of all Menpo objects.</p>
<div>

<div style="clear: both;"></div>

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/menpocli/index.md" title="menpocli"><img style="max-height: 140px; max-width: none;" src="logo/menpocli.png" alt="menpocli"></a>
</p>
<p><a href="/menpocli/index.md" title="menpocli"><strong style="font-size: 125%">menpocli</strong></a>
Command Line Interface (CLI) for the Menpo Project that allows to readily use pre-trained
state-of-the-art <code>menpofit</code> facial models. This is useful for people that only care to quickly acquire facial landmarks on their images.</p>
</div>

<div style="clear: both;"></div>

<div>
<p style="float: left; padding-right: 10px;">
  <a href="/landmarkerio/index.md" title="landmarker.io"><img style="max-height: 140px; max-width: none;" src="logo/landmarkerio_with_logo_2.png" alt="landmarker.io"></a>
</p>
<p><a href="/landmarkerio/index.md" title="landmarker.io"><strong style="font-size: 125%">landmarker.io</strong></a>
An interactive web-based tool for manual annotation of
2D images and 3D meshes. Useful to quickly landmark a single image, or organize a large annotation effort for thousands of files.
Features like Snap Mode and Dropbox compatibility make it unique.</p>
</div>

<div style="clear: both;"></div>

---------------------------------------

## Next Steps

We _strongly_ suggest you head over to the [installation instructions](installation/index.md "Full Installation Instructions") to get started.

Once you have installed the Menpo Project, you can visit our [Examples](examples/index.md) to get an idea of what you can do with Menpo.

---------------------------------------

## User Group and Issues
If you wish to get in contact with the Menpo developers, you can do so via various channels.
If you have found a bug, or if any part of Menpo behaves in a way you do not expect, please raise an issue on the corresponding package on [Github](https://github.com/menpo/ "The Menpo Project on Github").

If you want to ask a theoretical question, or are having problems setting up or using the Menpo Project, please visit the [user group](https://groups.google.com/forum/#!forum/menpo-users "menpo-users").

Follow [@teammenpo](www.twitter.com/teammenpo "The Menpo Project on Twitter") for updates on the Menpo Project, or tweet at us any questions you have.
