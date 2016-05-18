#!/usr/bin/env bash

set -x

cd $HOME/work

R -e "IRkernel::installspec()"
ipcluster nbextension enable

exec jupyter notebook $*
