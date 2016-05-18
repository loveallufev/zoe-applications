#!/usr/bin/env bash

set -x

R -e "IRkernel::installspec()"
ipcluster nbextension enable

rm -f jupyter_notebook_config.json

exec jupyter notebook $*
