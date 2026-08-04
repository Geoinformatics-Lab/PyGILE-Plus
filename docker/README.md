# PyGILE-Plus Docker

PyGILE-Plus is a containerized geospatial research environment that
includes GRASS GIS, SAGA GIS, OTB, GeoAI, and a Python-based analysis
stack.

The environment is preconfigured and consistent across tools.

------------------------------------------------------------------------

## Installation

### Pull pre-built image

```bash
docker pull dockagile/pygile-plus
```

### Build from source

```bash
git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git
cd PyGILE-Plus/docker
docker build -t pygile-plus .
```

------------------------------------------------------------------------

## Run

### CPU

```bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

### GPU

```bash
docker run -it --name pygile-plus \
  --gpus all \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

GPU usage requires:

- NVIDIA GPU
- Updated NVIDIA driver
- NVIDIA Container Toolkit

------------------------------------------------------------------------

## Access

Jupyter Lab starts automatically.

Open: http://localhost:8888

------------------------------------------------------------------------

## Environment

The container automatically configures:

- GRASS GIS (via conda, with Python bindings)
- SAGA GIS
- OTB (CLI)
- GeoAI stack
- Conda environment: `pygile`

GRASS-native raster and vector maps are readable through GDAL, OGR, and
GeoPandas via the bundled GDAL-GRASS driver.

------------------------------------------------------------------------

## Verify

```bash
docker run --rm dockagile/pygile-plus pygile-verify
```

Confirms GDAL 3.12 from the conda environment, GRASS raster and vector
drivers registered, and OTB CLI availability.

------------------------------------------------------------------------

## Usage

Activate environment:

```bash
conda activate pygile
```

Basic checks:

```bash
python -c "import grass.script as g; print('GRASS OK')"
grass --version
otbcli_BandMath -help
```

------------------------------------------------------------------------

## GPU Check

```bash
python -c "import torch; print(torch.cuda.is_available())"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

------------------------------------------------------------------------

## HPC (Apptainer)

```bash
apptainer pull docker://dockagile/pygile-plus
apptainer run --nv pygile-plus_latest.sif
```

------------------------------------------------------------------------

## Container Management

```bash
docker stop pygile-plus
docker start pygile-plus
docker restart pygile-plus
docker logs pygile-plus
docker rm pygile-plus
```