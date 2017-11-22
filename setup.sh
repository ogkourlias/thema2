#!/usr/bin/env bash

# Get the remote Vapory library
git submodule init
git submodule update

# Set symlinks for easy-import of Vapory library
ln -s vapory/vapory/*.py vapory/

echo "\nAll done, please don't forget to edit the 'default.ini' file and then run one of the 'template' Python scripts.\n"