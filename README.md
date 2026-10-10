<table>
  <tr>
    <td width="270">
      <img src="https://raw.githubusercontent.com/Geoinformatics-Lab/PyGILE-Plus/main/image/pygile_plus.png" width="250">
    </td>
    <td>
      <h3>Python GeoInformatics Lab Environment-Plus</h3>
      <p>
        A headless Docker environment combining SAGA GIS, GRASS GIS, WhiteboxTools, and OTB with a complete Python geospatial stack for spatial analysis, remote sensing, and machine learning — with GPU acceleration support.
      </p>
    </td>
  </tr>
</table>



https://github.com/user-attachments/assets/e7759b71-6145-4d54-b300-119e70dd026d


Watch the full video for installation and usage

https://www.youtube.com/watch?v=hnf8vN7IZdc

## What is included

### GIS platforms

-   SAGA GIS 9.3.2
-   GRASS GIS 8.4.2
-   WhiteboxTools 2.4.0
-   Orfeo ToolBox 9.1.1

### Python stack

-   Core geospatial libraries: GDAL 3.12.2, PROJ 9.7.1, GEOS 3.14.1,
    Shapely, Fiona, Rasterio, GeoPandas
-   Scientific computing: NumPy, SciPy, Pandas, Xarray
-   Terrain and hydrology: RichDEM, pysheds, Landlab, TopoToolbox,
    xarray-spatial
-   Machine learning: PyTorch, TensorFlow, scikit-learn, scikit-image
-   GPU computing: CuPy, CUDA-enabled PyTorch and TensorFlow
-   Visualization: Matplotlib, Plotly, Folium, Holoviews, Seaborn
-   Image processing: OpenCV, scikit-image
-   Web mapping: Leafmap, Geemap, ipyleaflet, localtileserver
-   Cloud and remote sensing tools: Earth Engine API, STAC tools,
    odc-stac, Planetary Computer
-   Point clouds: laspy, PDAL
-   Documentation tools: Sphinx, Jupyter Book
-   Jupyter Lab

### Core characteristics

-   Headless operation
-   Preconfigured environment
-   Version-pinned and reproducible: every package is fixed to an exact
    version, and a build manifest is written into the image
-   CLI and Python access to supported tools
-   Docker and Apptainer workflows
-   GPU-capable machine learning stack, subject to host driver
    compatibility

## Getting started

### Pull from Docker Hub

``` bash
docker pull dockagile/pygile-plus
```

### Build from source

``` bash
git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git
cd PyGILE-Plus/docker
docker build -t pygile-plus .
```

The Dockerfile is self-contained; no additional files are required.

## Run

### CPU

``` bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

### GPU

``` bash
docker run -it --name pygile-plus \
  --gpus all \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

GPU use requires: - NVIDIA GPU - compatible NVIDIA driver - NVIDIA
Container Toolkit on the host

Jupyter Lab starts automatically at `http://localhost:8888`.

Only `/workspace/data` is mounted in the examples above. Files written
elsewhere in the container are lost when it is removed. Mount the whole
`/workspace` directory to persist notebooks and outputs as well.

For more detailed Docker usage, see `docker/README.md`.


## Usage inside container

``` bash
conda activate pygile
```

### Basic checks

```bash
python -c "import grass.script as g; print('GRASS OK')"
grass --version
saga_cmd --version
whitebox_tools --version
otbcli_BandMath -help
```

## GPU verification

``` bash
python -c "import torch; print(torch.cuda.is_available())"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"
```

If GPU is not detected, verify host driver compatibility.

## Reproducibility

Every package is pinned to an exact version, and source tarballs are
checksum-verified during the build. A manifest recording engine
versions, compiler, checksums, library linkage, and the full resolved
package list is written into the image:

``` bash
docker run --rm dockagile/pygile-plus \
  cat /opt/manifest/build_manifest.txt
```

Also in `/opt/manifest/`: `conda_explicit.txt` (exact conda package URLs
and build hashes) and `pip_freeze.txt`.

The environment can be verified at any time:

``` bash
docker run --rm dockagile/pygile-plus pygile-verify
```

Deterministic numerics are enabled by default (`OMP_NUM_THREADS=1` and
equivalents) so floating-point results are reproducible across runs.
Override at run time if throughput matters more than bit-identical
output.

For citation, record the image digest:

``` bash
docker inspect --format='{{index .RepoDigests 0}}' \
  dockagile/pygile-plus
```

## Known limitations

-   OTB Python bindings (`otbApplication`) target Python 3.8 and are
    unavailable in this Python 3.11 environment. The OTB CLI is fully
    functional.
-   `saga_cmd` returns exit code 134 on teardown despite writing correct
    output. When scripting SAGA, check for output files rather than
    return codes.
-   SAGA links the system GDAL 3.0.4 while the Python stack uses GDAL
    3.12.2. Raster read and write are bit-identical between the two, so
    values are unaffected.
-   PyTorch is present as both a conda build and a CUDA wheel; the wheel
    takes precedence in `site-packages`.

## Tool locations

``` python
conda_env_path = "/opt/conda/envs/pygile"
saga_cmd = "/opt/saga/bin/saga_cmd"
grass_command = "grass"
otb_bin = "/opt/otb/bin"
whitebox_tools = "/opt/conda/envs/pygile/bin/whitebox_tools"
build_manifest = "/opt/manifest/build_manifest.txt"
```

## Applications

-   Remote sensing analysis and classification
-   Raster and vector processing
-   Terrain and hydrological analysis across multiple engines
-   Spatial statistics and geostatistics
-   Machine learning on geospatial data
-   Educational and research workflows
-   Web mapping and interactive visualization
-   Cloud-based geospatial analysis
-   HPC workflows through Apptainer

## System requirements

-   Docker
-   Recommended memory: 8 GB minimum, more for large workloads
-   Recommended storage: about 25 GB or more for the image and data
-   Network access for initial pull or build
-   For GPU use: NVIDIA GPU and compatible host setup
-   For HPC: Apptainer or Singularity with `--nv` support when GPU
    passthrough is needed

## HPC and Apptainer

``` bash
apptainer pull docker://dockagile/pygile-plus
apptainer run --nv pygile-plus_latest.sif
```

## License information

All included software remains under its respective upstream license.
Refer to the original project documentation for specific license terms.

## Reference and citation

Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2026). Geoinformatics-Lab/PyGILE-Plus: PyGILE-Plus v1.1.0 (v1.1.0). Zenodo. https://doi.org/10.5281/zenodo.18512474

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18512474.svg)]( https://doi.org/10.5281/zenodo.18512474)

Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2025). PyGILE-Plus: Python GeoInformatics Lab Environment-Plus (1.0.0). Zenodo. https://doi.org/10.5281/zenodo.16146572

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16146572.svg)](https://doi.org/10.5281/zenodo.16146572)
