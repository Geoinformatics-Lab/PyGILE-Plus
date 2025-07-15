# PyGILE-Plus: Python GeoInformatics Lab Environment-Plus

A comprehensive, headless Docker environment for geospatial research with **1700+ algorithms** across multiple platforms.

## What's Included

**Major GIS Platforms:**
- **QGIS LTR 3.40** - ~400 processing algorithms
- **GRASS GIS 8.4.0** - ~500 modules for vector/raster analysis
- **SAGA GIS 9.3.2** - ~500 geoprocessing tools
- **Orfeo ToolBox (OTB) 9.1.1** - ~100 remote sensing algorithms
- **WhiteboxTools** (Latest) - ~450 geospatial analysis tools

**Python Ecosystem:**
- Complete geospatial stack: GDAL, PROJ, GEOS, Shapely, Fiona, Rasterio, GeoPandas
- Machine Learning: PyTorch, TensorFlow, scikit-learn, scikit-image
- Visualization: Matplotlib, Plotly, Folium, Holoviews
- Jupyter Lab for interactive analysis

**Key Features:**
- Headless operation (no GUI required)


## Quick Start

```bash
# Clone the repository
git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git
cd PyGILE-Plus/docker

# Pull the image
docker pull dockagile/pygile-plus

OR

# Build the image
docker build -t pygile-plus .

# Run with Jupyter Lab
docker run -p 8888:8888 -v $(pwd)/data:/workspace/data pygile-plus

# Access Jupyter Lab at http://localhost:8888
```

### Docker (Recommended)
- Go to [docker/](https://github.com/Geoinformatics-Lab/PyGILE-Plus/tree/main/docker) → Follow README.md


## Use Cases

- Remote sensing analysis and classification
- Spatial data processing and geostatistics
- Machine learning on geospatial data
- Raster and vector analysis workflows
- Educational geospatial computing

## System Requirements

- Docker with 8GB+ RAM recommended
- 10GB+ storage for the image
- Network access for initial build

For detailed algorithm listings and capabilities, see the comprehensive PDF guide.

## License for Packages
All the software and packages present in this container are made available under their respective licenses. Please refer to the original documentations.

- https://github.com/Geoinformatics-Lab/PyGILE
- https://github.com/OSGeo/grass
- https://saga-gis.sourceforge.io/
- https://github.com/qgis/QGIS
- https://github.com/jblindsay/whitebox-tools
- https://github.com/pytorch/pytorch
- https://github.com/tensorflow
- https://github.com/keras-team/keras
- https://github.com/conda-forge/miniforge
