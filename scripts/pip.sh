#!/usr/bin/env bash

init() {
    pip install twine
}

build(){
    python setup.py sdist bdist_wheel
}

upload() {
    init

    twine upload \
        --username ${PYPI_USERNAME} \
        --password ${PYPI_PASSWORD} \
        --repository pypi \
        --repository-url https://upload.pypi.org/legacy/ \
        dist/*
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