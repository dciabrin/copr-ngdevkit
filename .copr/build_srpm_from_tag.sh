#!/bin/bash
set -e

OUTDIR=$1

# emudbg-0.2+202105012058-1
tag=$(git tag --sort=-creatordate | grep -E '[^0-9]*-[0-9.]*\+[0-9]*-[0-9]*' | head -1)
pkg=$(echo $tag | sed -E 's%^([^0-9]*)-[0-9].*$%\1%')

echo "Build srpm for package $pkg ($tag)"

cd $pkg
spectool -g $pkg.spec
rpmbuild -bs --define "_sourcedir $PWD" --define "_srcrpmdir $PWD" $pkg.spec
mv -v *.src.rpm $OUTDIR
