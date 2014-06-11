#!/bin/sh

#######################################################################
# This script shows how to setup the virtualenv and how to install the
# dependencies into this virtualenv.
# Usually this scirpt has to be executed only once on a new install of
# the django application or in case the dependencies have changed.
#######################################################################

ENV_DIR=$HOME/geoenv
REQUIRES_FILE=$HOME/requirements.txt
INTERPRETER=python3

# create virtualenv
if [ -d "$ENV_DIR" ]; then
  echo "**> virtualenv exists"
else
  echo "**> creating virtualenv"
  virtualenv -p $INTERPRETER "$ENV_DIR"
fi

. "$ENV_DIR/bin/activate"

# install dependencies
pip install -U -r "$REQUIRES_FILE"
