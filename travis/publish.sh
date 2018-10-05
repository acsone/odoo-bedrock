#!/bin/bash

set -e

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  docker login --username="$REGISTRY_USERNAME" --password="$REGISTRY_PASSWORD" $REGISTRY

  if [ "$TRAVIS_BRANCH" == "master" ]; then
    make VERSION=$VERSION TAG=latest tag push
  elif [ ! -z "$TRAVIS_TAG" ]; then
    make VERSION=$VERSION TAG=$TRAVIS_TAG tag push
  else
    echo "Not pushing any image"
  fi

fi
