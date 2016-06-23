<style>
button:focus {
  outline: none;
}
.header_container {
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  flex-wrap: wrap; 
  max-width: 600px;
}
.header_columns {
  display: flex; 
  flex-direction: row; 
  align-items: center; 
  justify-content: space-between;
}
.install_card {
  color: grey; 
  border: none; 
  margin: 5px 15px; 
  max-width: 200px;
  box-shadow: 2px 2px 5px #C7C7C7; 
  font-weight: 300;
}
.install_header {
  background: rgb(103, 167, 243); 
  color: white; 
  border: none; 
  padding: 12px; 
  font-weight: 300;
  font-size: large;
}
.install_card li {
  font-size: small;
  text-align: start;
}
.install_card li {
  padding: 5px;
}
.playground_help {
  position: relative;
  background: none; 
  color: #A6AAA9; 
  border: 1px solid #A6AAA9; 
  width: 30px; 
  height: 30px; 
  border-radius: 30px; 
  font-weight: 300;
}
.playground_help_popup {
  position: absolute;
  background: #70BF41;
  color: white;
  box-shadow: 2px 2px 5px #C7C7C7;
  min-width: 320px;
  border-radius: 10px;
  font-weight: 300;
  top: 55px;
  right: -40px;
  padding: 12px;
  visibility: hidden;
  opacity: 0;
  transition:visibility 0s linear 0.3s,opacity 0.3s ease;
}
.playground_help_speach {
  position: absolute;
  color: white;
  border-color: transparent;
  border-bottom-color: #70BF41;
  border-style: solid;
  border-width: 12px;
  border-bottom-width: 20px;
  font-weight: 300;
  right: 2px;
  visibility: hidden;
  opacity: 0;
  transition:visibility 0s linear 0.3s,opacity 0.3s ease;
}
.playground_help:hover .playground_help_popup {
    opacity: 1;
    visibility: visible;
    transition-delay: 0s;
}
.playground_help:hover .playground_help_speach {
    opacity: 1;
    visibility: visible;
    transition-delay: 0s;
}
</style>
<center>
  <div class="header_container">
    <div>Installation</div>
    <div>choose an option to find out more.</div>
    <div class="header_columns">
      <div>
        <div>Heres the top.</div>
        <div class="install_card">
          <div class="install_header">playground</div>
          <ul>
            <li>Standalone build of menpo - everything you need in one folder</li>
            <li>No install - just download and use</li>
            <li>Includes pre-trained models, command line toolsfor face detection and landmark localization, and example notebooks</li>
            <li>Easy to migrate to a full conda installation when you are ready</li>
          </ul>
        </div>
        <div>isolated & hassle free</div>
      </div>
      <div>
        <div>Heres the top.</div>
        <div class="install_card">
          <div class="install_header">conda</div>
          <ul>
            <li>The Python distribution of choice for many researchers</li>
            <li>Quickly and easily install all of the Menpo Project</li>
            <li>Easily install more Python packages with conda and pip</li>
            <li>Define multiple isolated environments and switch between them easily</li>
            <li>Contribute to all Menpo easily</li>

          </ul>
        </div>
        <div>flexible & powerful</div>
      </div>
      <div>
        <div>Heres the top.</div>
        <div class="install_card">
          <div class="install_header">pip</div>
          <ul>
            <li>Standalone build of menpo - everything you need in one folder</li>
            <li>No install - just download and use</li>
          </ul>
        </div>
        <div>integrate with what you have</div>
      </div>
    </div>
  </div>
</center>
<br>


The _Menpo Project_ supports Windows, macOS, and Linux.
Given that the Menpo project is designed to provide a suite of tools to
solve complex problems, it therefore has a complex set of dependencies.
In order to make things as simple as possible for Python developers (new and experienced),
we advocate the use of [Conda](http://conda.pydata.org/). Therefore, our
installation instructions focus on getting Conda installed on each of the
platforms.

#### Installation Instructions
We provide detailed guides for installing the Menpo Project.
Choose an operating system:

  - [Windows](windows/index.md)
  - [macOS](macos/index.md)
  - [Linux](linux/index.md)

#### Expert Quick Start
If you are an advanced user who is comfortable in the terminal, use the following quick start guide:
  - [Quick Start](expert_quick_start.md)

#### Setting Up A Development Environment
If you want to develop within the Menpo Project, please read the following guide:
  - [Development Setup](development.md)

---------------------------------------

Upgrading
=========
Assuming you have followed the installation instructions above, you may need
to upgrade your version of the Menpo Project packages to the latest. You can check if you
have the latest version by running the following commands within a Python
interpreter:

```python
>>> import menpo
>>> print(menpo.__version__)
```
Similarly for `menpofit`, `menpodetect`, `menpowidgets`, `menpo3d` and `menpocli`.
If you need to upgrade, you can do this using `conda` **(make
sure the `menpo` environment is activated)**.

##### macOS/Linux
To upgrade all packages (`menpofit`, `menpodetect`, `menpowidgets`, `menpocli`) do:
```
$ source activate menpo
(menpo) $ conda update -c menpo menpoproject
```
To explicitly upgrade a specific package do:
```
$ source activate menpo
(menpo) $ conda update -c menpo menpo
(menpo) $ conda update -c menpo menpofit
(menpo) $ conda update -c menpo menpodetect
(menpo) $ conda update -c menpo menpowidgets
(menpo) $ conda update -c menpo menpocli
(menpo) $ conda update -c menpo menpo3d
```

##### Windows
To upgrade all packages (`menpofit`, `menpodetect`, `menpowidgets`, `menpocli`) do:
```
C:\>activate menpo
[menpo] C:\>conda update -c menpo menpoproject
```
To explicitly upgrade a specific package do:
```
C:\>activate menpo
[menpo] C:\>conda update -c menpo menpo
[menpo] C:\>conda update -c menpo menpofit
[menpo] C:\>conda update -c menpo menpodetect
[menpo] C:\>conda update -c menpo menpowidgets
[menpo] C:\>conda update -c menpo menpocli
[menpo] C:\>conda update -c menpo menpo3d
```
