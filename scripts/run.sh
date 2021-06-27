#!/usr/bin/env bash

die () { echo "$1" >&2; exit 1; }

hash docker || { die "docker is not installed. Exiting..."; }

tag="searchapp"

echo "Building the image..."
if ! docker build --target app -f Dockerfile -t $tag . &> /dev/null; then
    die "Failed to build the image"
fi

echo "Running..."
docker run -it -t $tag
