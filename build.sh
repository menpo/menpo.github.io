#! /bin/bash

# Before we can build we need to check if we have the
# correct version of gitbook installed or not.
req_gb_version="3.1.1"

# Check if the gitbook CLI command is really old or not...
if gitbook --version | grep 'CLI version' -q; then

    # Relitively current CLI (good)
    gb_version=`gitbook current | awk '{print $NF}'`
    if [[ $gb_version == $req_gb_version* ]]; then
        echo "Using gitbook version $gb_version"
    else
        echo "Your gitbook version is wrong - should be $req_gb_version and is $gb_version"
        echo "Run gitbook update $req_gb_version to use the correct version"
        exit 1
    fi
else
    # Old CLI - really need to upgrade!
    echo "Your gitbook CLI version is very old! Run"
    echo "  > gitbook versions:update $req_gb_version"
    echo "To get up to date and try again"
    exit 1
fi

# Now we are good to go, build!
find . -maxdepth 1 ! -name 'googlec43c65618a70e0c8.html' ! -name '.gitignore' ! -name 'build.sh' ! -name 'src' ! -name '.git' ! -name '.' ! -name 'CNAME' -exec rm -rf {} +
cd src
gitbook install
gitbook build
mv _book/* ../
cd ..
