# PyGILE-Plus: Python GeoInformatics Lab Environment-Plus

A headless Docker environment combining SAGA GIS, GRASS GIS, Whitebox Tools, and OTB with a complete Python geospatial stack for spatial analysis, remote sensing, and machine learning — with GPU acceleration support.

## Quick Start

```bash
docker pull dockagile/pygile-plus

# Run with GPU support
docker run -it --gpus all -p 8888:8888 -v $(pwd)/data:/workspace/data dockagile/pygile-plus

# Run without GPU (CPU only)
docker run -it -p 8888:8888 -v $(pwd)/data:/workspace/data dockagile/pygile-plus
```

Access Jupyter Lab at `http://localhost:8888`

For detailed setup instructions, see [docker/README.md](docker/README.md)

## What's Included

### GIS Processing Platforms

- **SAGA GIS 9.3.2** - Command-line geoprocessing
- **GRASS GIS 8.4.0** - Command-line + Python integration  
- **Whitebox Tools** - Command-line geospatial analysis
- **Orfeo ToolBox 9.1.1** - Remote sensing processing

### Python Libraries (60+ packages)

**Core Geospatial**
```
gdal, proj, geos, libspatialindex, boost-cpp
shapely, fiona, pyproj
geopandas, rasterio
cartopy, geoplot, osmnx, earthpy
```

**Scientific Computing**
```
numpy, scipy, pandas
xarray, netcdf4, h5py, h5netcdf, zarr
scikit-learn, scikit-image
```

**Machine Learning & Deep Learning**
```
pytorch (CUDA 12.4), torchvision, torchaudio, pytorch-lightning
tensorflow (CUDA), keras
albumentations, timm
pyspatialml, sklearn-xarray
```

**Visualization**
```
matplotlib, seaborn, plotly, bokeh
folium, contextily, mapclassify
holoviews, hvplot
pyvista, pythreejs
keplergl
```

**Web Mapping**
```
leafmap, geemap
ipyleaflet, owslib
localtileserver, rio-cogeo, rioxarray
```

**Cloud & Remote Sensing**
```
earthengine-api
pystac, stackstac, planetary-computer
```

**Image Processing**
```
opencv
tifffile, imageio-ffmpeg
```

**Spatial Analysis**
```
rasterstats, xarray-spatial
libpysal, esda
pykrige
```

**Data & Utilities**
```
census, us
geojson
dask-geopandas
pygis, whitebox, PySAGA-cmd
numpy-groupies, sympy
```

**Development Tools**
```
jupyter, jupyterlab, ipywidgets
sphinx, sphinx_sitemap, sphinxcontrib.bibtex
sphinx_inline_tabs, pydata-sphinx-theme
jupyter-book, ghp-import
git, nodejs, npm
black, flake8, nbconvert
streamlit-folium
```

## Usage Examples

### Initialize Environment (Jupyter)
```python
import os, sys
os.environ['LD_LIBRARY_PATH'] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib"
os.environ['SAGA_CMD'] = '/opt/saga/bin/saga_cmd'
os.environ['SAGA_MLB'] = '/opt/saga/lib/saga'
os.environ['GISBASE'] = '/opt/grass'
os.environ['OTB_APPLICATION_PATH'] = '/opt/otb/lib/otb/applications'
sys.path.insert(0, '/opt/grass/etc/python')
```

### GPU Verification (Jupyter)
```python
import torch
import tensorflow as tf
print("PyTorch CUDA:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")
print("TensorFlow GPUs:", tf.config.list_physical_devices('GPU'))
```

### SAGA GIS
```bash
saga_cmd ta_morphometry 0 -ELEVATION=dem.tif -SLOPE=slope.tif
```

### GRASS GIS
```python
import grass.script as gscript
gscript.run_command('r.slope.aspect', elevation='dem', slope='slope')
```

### Whitebox Tools
```bash
whitebox_tools --run=Slope --input=dem.tif --output=slope.tif
```

### OTB
```bash
otbcli_BandMath -il image.tif -out result.tif -exp "im1b1+im1b2"
```

### Python ML
```python
from pyspatialml import Raster
from sklearn.ensemble import RandomForestClassifier

stack = Raster(['B2.tif', 'B3.tif', 'B4.tif', 'B8.tif'])
X, y, coords = stack.extract_vector('training.shp', field='class')
clf = RandomForestClassifier(n_estimators=200)
clf.fit(X, y)
prediction = stack.predict(clf, output='landcover.tif')
```

## HPC / Apptainer (Singularity)

```bash
# Pull and convert from Docker Hub
apptainer pull docker://dockagile/pygile-plus

# Run with GPU passthrough
apptainer run --nv pygile-plus_latest.sif
```

## Environment Details

- **Base Image:** condaforge/mambaforge:24.9.0-0
- **Python Version:** 3.10
- **Package Manager:** Mamba (conda-forge)
- **Operation Mode:** Headless (no GUI)
- **Jupyter Port:** 8888
- **GPU Support:** CUDA 12.4 (PyTorch + TensorFlow)

## Tool Paths

```python
conda_env_path = "/opt/conda/envs/pygile"
saga_cmd       = "/opt/saga/bin/saga_cmd"
saga_lib       = "/opt/saga/lib/saga"
grass_bin      = "/opt/grass/bin"
otb_bin        = "/opt/otb/bin"
whitebox_tools = "/opt/conda/envs/pygile/bin/whitebox_tools"
```

## Directory Structure

```
/workspace/
  ├── data/         # Input data
  ├── output/       # Processing results
  ├── scripts/      # Python/bash scripts
  ├── notebooks/    # Jupyter notebooks
  └── samples/      # Example datasets

/opt/
  ├── grass/        # GRASS GIS 8.4.0 installation
  ├── saga/         # SAGA GIS 9.3.2 installation
  └── otb/          # OTB 9.1.1 installation
```

## System Requirements

**Minimum:**
- 8 GB RAM
- 15 GB storage
- 4 CPU cores
- Docker 20.10+

**For GPU Support:**
- NVIDIA GPU
- NVIDIA Container Toolkit installed on host
- For HPC: Apptainer/Singularity with `--nv` flag support

## Documentation

- **Setup Guide:** [docker/README.md](docker/README.md)
- **Example Notebooks**: [notebooks/](notebooks/)



## Links

- GitHub: https://github.com/Geoinformatics-Lab/PyGILE-Plus
- Docker Hub: https://hub.docker.com/r/dockagile/pygile-plus
- DOI: https://doi.org/10.5281/zenodo.18512474


## Citation
Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2026). Geoinformatics-Lab/PyGILE-Plus: PyGILE-Plus v1.1.0 (v1.1.0). Zenodo. https://doi.org/10.5281/zenodo.18512474

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18512474.svg)]( https://doi.org/10.5281/zenodo.18512474)

Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2025). PyGILE-Plus: Python GeoInformatics Lab Environment-Plus (1.0.0). Zenodo. https://doi.org/10.5281/zenodo.16146572

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16146572.svg)](https://doi.org/10.5281/zenodo.16146572)
