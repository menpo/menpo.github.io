#! /bin/bash

find . -maxdepth 1 ! -name 'googlec43c65618a70e0c8.html' ! -name '.gitignore' ! -name 'build.sh' ! -name 'src' ! -name '.git' ! -name '.' ! -name 'CNAME' -exec rm -rf {} +
cd src
gitbook install
gitbook build
mv _book/* ../
cd ..
