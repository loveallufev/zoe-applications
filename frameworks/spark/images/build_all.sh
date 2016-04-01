#!/usr/bin/env bash

set -e

REGISTRY=''
VERSION=''
PUSH=0

while getopts ":hr:v:p" opt; do
    case ${opt} in
        \?|h)
          echo "Usage: $0 [-r registry] [-v version] [-p] <repository>"
          echo
          echo "Will build Docker images names [registry]/<repository>/<image name>:version"
          echo "If -p is specified, docker push will be called at the end of the build"
          exit
          ;;
        r)
          REGISTRY=/$OPTARG
          ;;
        v)
          VERSION=:$OPTARG
          ;;
        p)
          PUSH=1
          ;;
    esac
done

REPOSITORY=$1

for d in spark-master spark-worker spark-submit spark-jupyter-notebook; do
  pushd $d
  docker build -t ${REGISTRY}${REPOSITORY}${d}${VERSION} .
  if ${PUSH}; then
    docker push ${REGISTRY}${REPOSITORY}${d}${VERSION}
  fi
  popd
done


