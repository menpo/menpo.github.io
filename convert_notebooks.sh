#! /bin/bash
# Generate markdown from each notebook
find ./notebooks -name '*.ipynb' -exec jupyter nbconvert --to markdown {} \;
