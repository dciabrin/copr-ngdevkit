#!/bin/bash

# Copyright (c) 2021 Damien Ciabrini
# This file is part of ngdevkit

set -ue

# Disable verbose to prevent leaking credentials
set +x


help() {
    echo "Usage: $0 --secret=\"{copr-uuid}\" --package=\"{package}\"" >&2
    exit ${1:-0}
}

error() {
    echo "Error: $1" >&2
    help 1
}


# ----------------- config parsing -----------------
#
DRYRUN=
PACKAGE=

OPTS=$(/usr/bin/getopt -n $0 --long help,dry-run,package:,secret: -- $0 $@)
if [ $? != 0 ]; then
    error "parsing arguments failed"
fi

eval set -- "$OPTS"
while true; do
    case "$1" in
        --help) help;;
        --dry-run ) DRYRUN=1; shift ;;
        --package ) PACKAGE="$2"; shift 2 ;;
        --secret ) COPR_SECRET="$2"; shift 2 ;;
        -- ) shift; break ;;
        * ) break ;;
    esac
done


if [ -z "$PACKAGE" ]; then
    error "No package specified"
fi
if [ -z "$COPR_SECRET" ]; then
    error "No COPR webhook secret specified"
fi

if [ -n "$DRYRUN" ]; then
    echo curl -X POST https://copr.fedorainfracloud.org/webhooks/custom/${COPR_SECRET}/${PACKAGE}/
else
    curl -X POST https://copr.fedorainfracloud.org/webhooks/custom/${COPR_SECRET}/${PACKAGE}/
fi

echo "COPR code rebuild webhook called succesfully"
