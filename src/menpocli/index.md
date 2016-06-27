<link rel="stylesheet" type="text/css"  href="../menpostyle.css">

<div style="display: flex; align-items: center; flex-direction: column;">
  <img src="../../logo/menpocli.png" alt="menpocli" width="30%" style="display: flex;">
  </br>
  <div style="display: flex; align-items: center; justify-content: center; margin-top: 4px; margin-bottom: 20px">
    <a href="https://github.com/menpo/menpocli" style="display: flex;">
      <img src="http://img.shields.io/github/release/menpo/menpocli.svg?style=flat-square" alt="Github Release"/>
    </a>
    <a style="text-decoration: none; color: grey; margin: 5px 25px;" href="https://github.com/menpo/menpocli">
      <button class="download_button">View on Github</button>
    </a>
    <a href="https://github.com/menpo/menpocli/blob/master/LICENSE.txt" style="display: flex;">
      <img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/>
    </a>
  </div>
</div>

`menpocli` provides a command line interface for performing either face alignment or face detection on folders of images. For example, to perform face detection on a folder of images:

```shell
> menpodetect ./folder_of_images
```

which will save a number of `PTS` files containing the corners of the bounding box for each face in the image. Similarly, to perform face alignment:

```shell
> menpofit ./folder_of_images
```

which will use a pre-trained AAM to fit facial landmarks to the faces detected within the images.