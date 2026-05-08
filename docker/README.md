# PyGILE-Plus Docker

PyGILE-Plus is a containerized geospatial research environment that
includes GRASS GIS, SAGA GIS, OTB, GeoAI, and a Python-based analysis
stack.

The environment is preconfigured and consistent across tools.

------------------------------------------------------------------------

## Installation

### Pull pre-built image

docker pull dockagile/pygile-plus

### Build from source

git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git\
cd PyGILE-Plus/docker\
docker build -t pygile-plus .

------------------------------------------------------------------------

## Run

### CPU

docker run -it --name pygile-plus\
-p 8888:8888\
-v \$(pwd)/data:/workspace/data\
pygile-plus

### GPU

docker run -it --name pygile-plus\
--gpus all\
-p 8888:8888\
-v \$(pwd)/data:/workspace/data\
pygile-plus

GPU usage requires: - NVIDIA GPU - Updated NVIDIA driver - NVIDIA
Container Toolkit

------------------------------------------------------------------------

## Access

Jupyter Lab starts automatically.

Open:\
http://localhost:8888

------------------------------------------------------------------------

## Environment

The container automatically configures:

-   GRASS GIS (via conda, with Python bindings)
-   SAGA GIS
-   OTB (CLI and Python)
-   GeoAI stack
-   Conda environment: `pygile`

------------------------------------------------------------------------

## Usage

Activate environment:

conda activate pygile

Basic checks:

python -c "import grass.script as g; print('GRASS OK')" grass --version
otbcli_BandMath -help python -c "import otbApplication; print('OTB OK')"

------------------------------------------------------------------------

## GPU Check

python -c "import torch; print(torch.cuda.is_available())" python -c
"import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

------------------------------------------------------------------------

## HPC (Apptainer)

apptainer pull docker://dockagile/pygile-plus apptainer run --nv
pygile-plus_latest.sif

------------------------------------------------------------------------

## Container Management

docker stop pygile-plus docker start pygile-plus docker restart
pygile-plus docker logs pygile-plus docker rm pygile-plus
