# PyGILE-Plus: Python GeoInformatics Lab Environment-Plus

PyGILE-Plus is a headless Docker environment for geospatial research that combines major GIS platforms with a Python geospatial and machine learning stack.

## What is included

### GIS platforms
- SAGA GIS 9.3.2
- GRASS GIS 8.4.0
- WhiteboxTools
- Orfeo ToolBox 9.1.1

### Python stack
- Core geospatial libraries: GDAL, PROJ, GEOS, Shapely, Fiona, Rasterio, GeoPandas
- Scientific computing: NumPy, SciPy, Pandas, Xarray
- Machine learning: PyTorch, TensorFlow, scikit-learn, scikit-image
- Visualization: Matplotlib, Plotly, Folium, Holoviews, Seaborn
- Image processing: OpenCV, scikit-image
- Web mapping: Leafmap, Geemap, ipyleaflet, localtileserver
- Cloud and remote sensing tools: Earth Engine API, STAC tools, Planetary Computer
- Documentation tools: Sphinx, Jupyter Book
- Jupyter Lab

### Core characteristics
- Headless operation
- Preconfigured environment
- CLI and Python access to supported tools
- Docker and Apptainer workflows
- GPU-capable machine learning stack, subject to host driver compatibility

## Getting started

### Pull from Docker Hub

```bash
docker pull dockagile/pygile-plus
```

### Build from source

```bash
git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git
cd PyGILE-Plus/docker
docker build -t pygile-plus .
```

## Run

### CPU

```bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  pygile-plus
```

### GPU

```bash
docker run -it --name pygile-plus \
  --gpus all \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  pygile-plus
```

GPU use requires:
- NVIDIA GPU
- compatible NVIDIA driver
- NVIDIA Container Toolkit on the host

Jupyter Lab starts automatically at `http://localhost:8888`.

For more detailed Docker usage, see `docker/README.md`.

## Environment behavior

The container configures the working environment internally. No notebook initialization cell or manual environment script is required for the standard Docker workflow.

The following components are configured in the container:
- GRASS GIS CLI and Python bindings
- SAGA GIS
- OTB CLI and Python bindings
- WhiteboxTools
- GeoAI
- Conda environment `pygile`

## Usage inside container

```bash
conda activate pygile
```

### Basic checks

```bash
python -c "import grass.script as g; print('GRASS OK')"
otbcli_BandMath -help
python -c "import otbApplication; print('OTB OK')"
python -c "import geoai; print('GeoAI OK')"
```

## GPU verification

```bash
python -c "import torch; print(torch.cuda.is_available())"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

If GPU is not detected, verify host driver compatibility.

## HPC and Apptainer

```bash
apptainer pull docker://dockagile/pygile-plus
apptainer run --nv pygile-plus_latest.sif
```

## Tool locations

These are the standard locations in the Docker image:

```python
conda_env_path = "/opt/conda/envs/pygile"
saga_cmd = "/opt/saga/bin/saga_cmd"
grass_command = "grass"
otb_bin = "/opt/otb/bin"
whitebox_tools = "/opt/conda/envs/pygile/bin/whitebox_tools"
```

## Available workflows

- Remote sensing analysis and classification
- Raster and vector processing
- Spatial statistics and geostatistics
- Machine learning on geospatial data
- Educational and research workflows
- Web mapping and interactive visualization
- Cloud-based geospatial analysis
- HPC workflows through Apptainer

## System requirements

- Docker
- Recommended memory: 8 GB minimum, more for large workloads
- Recommended storage: about 16 GB or more for the image and data
- Network access for initial pull or build
- For GPU use: NVIDIA GPU and compatible host setup
- For HPC: Apptainer or Singularity with `--nv` support when GPU passthrough is needed

## Documentation

For algorithm listings, see the CSV files in `algorithms_toc/`.

## License information

All included software remains under its respective upstream license. Refer to the original project documentation for specific license terms.

## Reference and citation

Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2026). Geoinformatics-Lab/PyGILE-Plus: PyGILE-Plus v1.1.0 (v1.1.0). Zenodo. https://doi.org/10.5281/zenodo.18512474

Awasthi, B., Ninsawat, S., Raghavan, V., & Nemoto, T. (2025). PyGILE-Plus: Python GeoInformatics Lab Environment-Plus (1.0.0). Zenodo. https://doi.org/10.5281/zenodo.16146572
