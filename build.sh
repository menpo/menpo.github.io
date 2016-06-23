find . -maxdepth 1 ! -name 'build.sh' ! -name 'src' ! -name '.git' ! -name '.' ! -name 'CNAME' -exec rm -rf {} +
cd src
gitbook install
gitbook build
mv _book/* ../
cd ..
