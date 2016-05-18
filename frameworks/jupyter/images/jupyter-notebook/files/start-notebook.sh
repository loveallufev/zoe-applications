#!/usr/bin/env bash

set -x

R -e "IRkernel::installspec()"
ipcluster nbextension enable

exec jupyter notebook $*
