#!/bin/bash
set -e

OUTDIR=$1
PKG=$2

if [ -z "$PKG" ]; then
    echo "missing package name" >&2
    echo "./$0 {outputdir} {package}" >&2
    exit 1
fi

pkg=$(basename $PKG | sed 's/.spec//')
RPM_VERSION=$(sed -ne "s/^Version: *\(.*\).*/\1/p" $PKG)
RPM_RELEASE=$(sed -ne "s/^Release: *\(.*\)%.*/\1/p" $PKG)
tag=${RPM_VERSION}-${RPM_RELEASE}

echo "Build srpm for package $pkg ($tag)"
spectool -g $PKG
rpmbuild -bs --define "_sourcedir $PWD" --define "_srcrpmdir $PWD" $PKG
mv -v *.src.rpm $OUTDIR
