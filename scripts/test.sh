#!/usr/bin/env bash

die () { echo "$1" >&2; exit 1; }

hash docker || { die "docker is not installed. Exiting..."; }

dockerOptions="-v """$(pwd):/opt/code/""""
tag="searchapp-test"
dockerRun="docker run $dockerOptions -t $tag"

echo "Building the image..."
if ! docker build --target test -f Dockerfile -t $tag . &> /dev/null; then
    die "Failed to build the image"
fi

echo "Running the type checking..."
if ! $dockerRun mypy searchapp; then

    die "Failed type checking"
fi

echo "Running the tests..."
if ! $dockerRun pytest -v --cov searchapp; then

    die "Failed tests"
fi
