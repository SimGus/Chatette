#!/usr/bin/env bash

set -ex;

IMAGE_NAME="simgus/chatette"

login() {
    echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" \
        --password-stdin
}

build() {
    [ ! -z $1 ] && VERSION_TAG=$1 || VERSION_TAG='latest'

    echo "Current working directory $(pwd) ->"
    tree -L 1

    echo "Dist directory ->"
    tree dist

    docker build -t "${IMAGE_NAME}:${VERSION_TAG}" .
}

run() {
    docker run meiblorn/boltun "$@"
}

push() {
    login

    VERSION_TAGS="${@}"
    for VERSION_TAG in ${VERSION_TAGS}
    do
        build ${VERSION_TAG}
        docker push "${IMAGE_NAME}:${VERSION_TAG}"
    done
}


if declare -f $1 > /dev/null
then
  # call arguments verbatim
  "$@"
else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  exit 1
fi