#!/bin/bash
# $1: package name
set -eu
PKG=$1
MASTER_BRANCH=${2:-master}

if [ -f configure.ac ]; then
    HEAD_VERSION=$(sed -ne 's/AC_INIT.*\[\([^]]*\)\].*/\1/p' configure.ac)
elif [ -f Makefile ]; then
    HEAD_VERSION=$(sed -ne 's%VERSION=\(.*\)$%\1%p' Makefile)
else
    echo "Cannot parse head version for $PKG in $(pwd)" >&2
    exit 1
fi

COPR_BASEDIR=$(dirname $(dirname $0))
export GIT_ASKPASS=$(realpath ${COPR_BASEDIR}/.ci/git-ask-pass.sh)

git checkout ${MASTER_BRANCH}
HEAD_COMMIT_DATE=$(TZ=UTC git show --quiet --date='format-local:%Y%m%d%H%M' --format='%cd')
echo $HEAD_COMMIT_DATE
if ! (git tag -l | grep -q nightly-$HEAD_COMMIT_DATE); then
    echo "Tagging $PKG with new version ${HEAD_COMMIT_DATE} on tip of ${MASTER_BRANCH}"
    git tag nightly-$HEAD_COMMIT_DATE
    if ! git push origin nightly-$HEAD_COMMIT_DATE; then
        # If the tag has been created by somebody else in the mean time
        # the push will fail. This is alright for us though
        if [ "$(git ls-remote origin refs/tags/nightly-$HEAD_COMMIT_DATE)" != "" ]; then
            echo "Tag already exists on origin, tag push in unecessary"
        else
            echo "Tagging $PKG with ${HEAD_COMMIT_DATE} failed" >&2
            exit 1
        fi
    fi
else
    echo "Tagging ${HEAD_COMMIT_DATE} for $PKG already exists, not retagging"
fi

echo "Computing archive URL and SHA256 for $PKG $HEAD_COMMIT_DATE"
ARCHIVE=$(echo "https://github.com/dciabrin/$PKG/archive/nightly-${HEAD_COMMIT_DATE}.tar.gz" | sed 's/ngdevkit-gngeo/gngeo/')
# HASH=$(curl -sL $ARCHIVE | sha256sum | cut -d' ' -f1)

RPM_VERSION=${HEAD_VERSION}+${HEAD_COMMIT_DATE}
cd $COPR_BASEDIR
git checkout main

RPM_CURRENT_VERSION=$(sed -ne "s/^Release: *\(.*\)%.*/\1/p" $PKG.spec)
if grep '^Version:' $PKG.spec | grep -qw "$RPM_VERSION"; then
    echo "Package $PKG already uses version $RPM_VERSION, bumping release accordingly"
    RPM_CURRENT_RELEASE=$(sed -ne "s/^Release: *\(.*\)%.*/\1/p" $PKG.spec)
    RPM_NEXT_RELEASE=$(($RPM_CURRENT_RELEASE + 1))
else
    echo "New version for package $PKG detected"
    RPM_NEXT_RELEASE=1
fi

COPR_VERSION=${HEAD_VERSION}+${HEAD_COMMIT_DATE}-${RPM_NEXT_RELEASE}
echo "Updating nightly release $COPR_VERSION of $PKG in specfile"

sed -i -e "s/^\(Version: *\)\(.*\)/\1${RPM_VERSION}/" $PKG.spec
sed -i -e "s/^\(Release: *\)\(.*\)\(%.*\)/\1${RPM_NEXT_RELEASE}\3/" $PKG.spec

CHANGELOG_DATE=$(date '+%a %b %d %Y')
sed -i '/^%changelog/q' $PKG.spec
echo -e "* $CHANGELOG_DATE CI Build Bot <> - $COPR_VERSION" >> $PKG.spec
echo -e "- Nightly build for tag nightly-${HEAD_COMMIT_DATE}" >> $PKG.spec

git add $PKG.spec
git commit -m "Nightly build ${PKG} ${HEAD_COMMIT_DATE}"
git push
echo "New nightly version ready to be rebuilt in COPR"
