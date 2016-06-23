Pip installation
================

Due to our complex dependencies, we strongly recommend that Menpo users consider using [conda](conda.md) as their Python distribution.

Saying that, we know many users already have Python environments and virtualenvs set up and don't want to migrate to a new Python distribution, regardless of the benefits. For these users, we ensure that the core `menpo` library is `pip` installable.

You'll need `numpy`, and `cython` installed before you can pip install menpo:
```
pip install numpy cython
```
We've these installed, you can pip install:
```
pip install menpo
``` 
To be clear, we are currently only able to offer the core `menpo` library through `pip`. If you want to use `menpofit` or `menpodetect`, for now you'll need to switch to [conda](conda.md), or try a standalone [Menpo Playground](playground.md) (which is simply a folder you can download with the whole project ready to go inside it).
