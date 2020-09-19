#!/bin/bash

git config credential.helper "store --file=.git/credentials"
echo "https://${GH_TOKEN}:@github.com" > .git/credentials

# get highest tag number
VERSION=`git describe --abbrev=0 --tags`

# replace . with space so can split into an array
VERSION_BITS=(${VERSION//./ })

# get number parts and increase last one by 1
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM2=$((VNUM2+1))

# create new tag
NEW_TAG="$VNUM1.$VNUM2"

echo "Updating $VERSION to $NEW_TAG"

# get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT`

# only tag if no tag already
if [ -z "$NEEDS_TAG" ]; then
    git checkout master
    sed -i -E "s/(version=).+?,/\1$NEW_TAG,/" setup.py
    git add setup.py
    git commit -m "updating to version $NEW_TAG"
    echo "Tagged with $NEW_TAG"
    git tag $NEW_TAG
    git push
    git push --tags
else
    echo "Already a tag on this commit"
fi
