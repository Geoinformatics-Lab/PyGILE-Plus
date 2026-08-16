# PyGILE-Plus Docker

PyGILE-Plus is a containerized geospatial research environment that
includes GRASS GIS, SAGA GIS, OTB, WhiteboxTools, GeoAI, and a
Python-based analysis stack.

The environment is preconfigured, version-pinned, and consistent across
tools.

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

The Dockerfile is self-contained. No additional files are required.

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

Only `/workspace/data` is mounted above. Files written elsewhere in the
container are lost when it is removed. Mount the whole `/workspace`
directory to persist notebooks and outputs as well.

------------------------------------------------------------------------

## Access

Jupyter Lab starts automatically.

Open: http://localhost:8888

------------------------------------------------------------------------

## Environment

The container automatically configures:

- GRASS GIS 8.4.2 (via conda, with Python bindings)
- SAGA GIS 9.3.2 (built from source, headless)
- WhiteboxTools 2.4.0
- OTB 9.1.1 (CLI)
- GDAL 3.12.2 / PROJ 9.7.1 / GEOS 3.14.1
- GeoAI stack
- Conda environment: `pygile`

GRASS-native raster and vector maps are readable through GDAL, OGR, and
GeoPandas via the bundled GDAL-GRASS driver.

### Terrain and hydrology

Alongside the four GIS engines, the environment provides independent
implementations of common terrain and flow-routing algorithms:

- RichDEM 2.3.0 (Priority-Flood, Planchon and Darboux, D8/D-infinity)
- pysheds 0.5 (flow accumulation, watershed delineation)
- Landlab 2.10.1 (landscape evolution)
- TopoToolbox 0.0.12 (quantitative geomorphology)
- xarray-spatial 0.5.3 (with CuPy 14.1.1 GPU backend)

### Data access and point clouds

- odc-stac 0.5.3, pystac-client, planetary-computer, earthaccess
- laspy 2.7.0, python-pdal 3.5.3

------------------------------------------------------------------------

## Verify

```bash
docker run --rm dockagile/pygile-plus pygile-verify
```

Confirms GDAL 3.12 from the conda environment, GRASS raster and vector
drivers registered, SAGA tool libraries loadable, WhiteboxTools and OTB
availability, and that key package versions match the build.

------------------------------------------------------------------------

## Reproducibility

Every package is pinned to an exact version. Source tarballs are
checksum-verified at build time.

A build manifest is written into the image, recording engine versions,
compiler, tarball checksums, library linkage, and the full resolved
package list:

```bash
docker run --rm dockagile/pygile-plus \
  cat /opt/manifest/build_manifest.txt
```

Also available in `/opt/manifest/`:

- `conda_explicit.txt` - exact conda package URLs and build hashes
- `pip_freeze.txt` - resolved pip environment

For citation, record the image digest:

```bash
docker inspect --format='{{index .RepoDigests 0}}' \
  dockagile/pygile-plus
```

Deterministic numerics are enabled by default (`OMP_NUM_THREADS=1` and
equivalents) so floating-point results are reproducible across runs.
Override at run time if throughput matters more than bit-identical
output.

------------------------------------------------------------------------

## Known limitations

- OTB Python bindings (`otbApplication`) target Python 3.8 and are
  unavailable in this Python 3.11 environment. The OTB CLI is fully
  functional.
- `saga_cmd` returns exit code 134 on teardown despite writing correct
  output. Check for output files rather than return codes when scripting
  SAGA.
- SAGA links the system GDAL 3.0.4 while the Python stack uses GDAL
  3.12.2. Raster read and write are bit-identical between the two; the
  difference has no effect on values.
- PyTorch is present as both a conda build and a CUDA wheel. The wheel
  takes precedence in `site-packages`.

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
saga_cmd --version
whitebox_tools --version
otbcli_BandMath -help
```

------------------------------------------------------------------------

## GPU Check

```bash
python -c "import torch; print(torch.cuda.is_available())"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"
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
