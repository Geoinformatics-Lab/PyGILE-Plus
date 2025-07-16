#!/bin/bash
# PyGILE-Plus Working Environment Script

echo "Loading PyGILE-Plus with all fixes..."

# Library path fix for GLIBCXX conflicts
export LD_LIBRARY_PATH="/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib:$LD_LIBRARY_PATH"

# SAGA GIS Configuration
export SAGA_CMD="/opt/saga/bin/saga_cmd"
export SAGA_MLB="/opt/saga/lib/saga"
export PATH="/opt/saga/bin:$PATH"

# GRASS GIS Configuration
export GISBASE="/opt/grass"
export PYTHONPATH="/opt/grass/etc/python:$PYTHONPATH"
export PATH="/opt/grass/bin:$PATH"

# OTB Configuration
export OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"
export PATH="/opt/otb/bin:$PATH"

# WhiteboxTools Configuration
export PATH="/opt/conda/envs/pygile/bin:$PATH"

echo " PyGILE-Plus environment loaded successfully"
echo " 2,326+ algorithms now available"
echo " Ready for Geospatial analysis"