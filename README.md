<table>
  <tr>
    <td width="270">
      <img src="https://raw.githubusercontent.com/Geoinformatics-Lab/PyGILE-Plus/main/image/pygile_plus.png" width="250">
    </td>
    <td>
      <h3>Python GeoInformatics Lab Environment-Plus</h3>
      <p>
        A step-by-step course in Python and GIS for absolute beginners, and a headless Docker environment combining SAGA GIS, GRASS GIS, WhiteboxTools, and OTB with a complete Python geospatial stack for spatial analysis, remote sensing, and machine learning — with GPU acceleration support.
      </p>
    </td>
  </tr>
</table>



https://github.com/user-attachments/assets/e7759b71-6145-4d54-b300-119e70dd026d


Watch the full YouTube video for step wise tutorial for installation via the following link:

https://www.youtube.com/watch?v=hnf8vN7IZdc

## How PyGILE-Plus is organised

PyGILE-Plus consists of three parts that build on each other:

| | Contents | Location |
| --- | --- | --- |
| **1. Computing environment** | One Docker image with a complete Python geospatial stack, SAGA GIS, GRASS GIS, WhiteboxTools and OTB | [`docker/`](docker/README.md) |
| **2. Core curriculum** | The PyGILE course: Python and GIS from zero, in 39 lessons | [`PyGILE_course/`](PyGILE_course/README.md) |
| **3. Thematic modules** | Geospatial analysis applied to one field, built on the core curriculum | [`thematic_modules/`](thematic_modules/README.md) |

All three run in the same Docker image, so the environment a learner sets up for the first lesson serves every thematic module. **New in version 2.0:** the core curriculum, and the first thematic module, Landslide Susceptibility Mapping.

## Core curriculum: the PyGILE course

A step-by-step course for absolute beginners, in [`PyGILE_course/`](PyGILE_course/README.md). Every step has theory, a worked example on real data from Nepal, and practice questions with worked solutions; the lessons are linked in order like a book.

- **Part A · Python (12 lessons)**: from Python as a calculator to tables, plots and good habits
- **Part B · Vector GIS (12 lessons)**: the map of Nepal, from coordinates to interactive web maps
- **Part C · Rasters (9 lessons)**: the terrain of the Kathmandu Valley and Melamchi, from a DEM to interpolation and spatial statistics
- **Part D · Satellite imagery (6 lessons)**: the 2021 Melamchi flood in Sentinel-2 images, from bands to data cubes

Together: 39 lessons and 1,061 practice questions. The data are real: rainfall from Nepal's Department of Hydrology and Meteorology, landslides from NASA and the USGS, boundaries from the Survey Department, Sentinel-2 and the Copernicus DEM.

- Every answer is **marked automatically** as you run it, offline and with no account, and an optional **free AI tutor** gives a personal hint and answers follow-up questions. See [the tutor guide](PyGILE_course/AI_TUTOR.md).
- The last lesson of each part ends with a project on **your own country**, and [a guide](PyGILE_course/YOUR_OWN_DATA.md) shows how to run all 39 lessons on your own country's data.

### Start the course

1. **Install Docker Desktop** from [docker.com](https://docs.docker.com/get-started/get-docker/) and start it. On Windows, accept WSL 2 when it asks. Keep about 30 GB free: the image is large because it also holds the research tools.
2. **Get this repository**: `git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git`, or click **Code → Download ZIP** above and unzip it.
3. **Open a terminal in the `PyGILE-Plus` folder** and start the image with that folder inside it. The first time, Docker downloads the image, which takes a while.

   macOS and Linux:

   ``` bash
   docker run -it --name pygile-plus -p 8888:8888 \
     -v "$(pwd)":/workspace/PyGILE-Plus \
     dockagile/pygile-plus
   ```

   Windows (PowerShell):

   ``` powershell
   docker run -it --name pygile-plus -p 8888:8888 -v "${PWD}:/workspace/PyGILE-Plus" dockagile/pygile-plus
   ```

4. **Open http://localhost:8888** in your browser, then `PyGILE-Plus` → `PyGILE_course` → `A_Python` → `A01_Python_as_your_calculator.ipynb`, and run the first cell.
5. **Next time**, start the same container again with `docker start -ai pygile-plus` and open http://localhost:8888. Your notebooks are saved in your `PyGILE-Plus` folder, and the same container keeps your tutor setup. (If Docker says the name `pygile-plus` is already in use, that container exists: start it with this command, or remove it with `docker rm pygile-plus` and run step 3 again.)

## Thematic modules

After the core curriculum, a thematic module applies the same tools to one field. See [`thematic_modules/`](thematic_modules/README.md).

- **[Landslide Susceptibility Mapping](thematic_modules/landslide_susceptibility/README.md)**: six notebooks from a DEM and the landslides of the 2015 Gorkha earthquake to a susceptibility map, with WhiteboxTools, SAGA and GRASS. Prerequisites: Parts A to C.

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
## Support & Community

- **Issues**: Report bugs and suggest features via GitHub Issues:[PyGILE-Issues](https://github.com/Geoinformatics-Lab/PyGILE-Plus/issues)
- **Discussions**: Join community conversations on PyGILE mailing list: [PyGILE-Discuss](https://lists.geoinfo-lab.org/postorius/lists/pygile.geoinfo-lab.org/)

## License information

PyGILE-Plus, including the PyGILE course, is released under the GNU GPL-2.0 (see [LICENSE](LICENSE)).
The course's concept diagrams come from the pyGIS project and keep its GPL-3.0 licence, and the course data keep the terms of their sources: see [`PyGILE_course/images/README.md`](PyGILE_course/images/README.md) and [`PyGILE_course/data/README.md`](PyGILE_course/data/README.md).

All included software remains under its respective upstream license.
Refer to the original project documentation for specific license terms.

## Reference and citation

If you use PyGILE-Plus or the PyGILE course, please cite:

Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2026). PyGILE-Plus: Python GeoInformatics Lab Environment-Plus. Zenodo. https://doi.org/10.5281/zenodo.18512473

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18512473-blue)](https://doi.org/10.5281/zenodo.18512473)

### Version history

| Version | Released | DOI |
| --- | --- | --- |
| 2.0.0 | November 2026 | [10.5281/zenodo.24433621](https://doi.org/10.5281/zenodo.24433621) |
| 1.1.1 | May 2026 | [10.5281/zenodo.20084413](https://doi.org/10.5281/zenodo.20084413) |
| 1.1.0 | February 2026 | [10.5281/zenodo.18512474](https://doi.org/10.5281/zenodo.18512474) |
| 1.0.0 | July 2025 | [10.5281/zenodo.16146572](https://doi.org/10.5281/zenodo.16146572) |
